#!/usr/bin/env python3
"""B2-17 source arithmetic and synthetic unit components; no native models."""
from __future__ import annotations
import csv
import hashlib
import json
import math
from pathlib import Path

from CoolProp.CoolProp import PropsSI

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/comprehensive_review"


def positive(values, *, zero=False):
    if not values or any(not math.isfinite(x) or (x < 0 if zero else x <= 0) for x in values):
        raise ValueError("Finite values in the stated positive/nonnegative domain required")


def fraction(values):
    positive(values, zero=True)
    if max(values) > 1:
        raise ValueError("Fractions, not whole percentages, required")


def pore_volume(area_m2, thickness_m, porosity):
    positive([area_m2, thickness_m]); fraction([porosity])
    return area_m2 * thickness_m * porosity


def oil_material_mass(pv, density, recovery, water_saturation, injected, produced):
    positive([pv, density]); fraction([recovery, water_saturation]); positive([injected, produced], zero=True)
    volume = recovery * pv * (1 - water_saturation) - injected + produced
    if volume < 0:
        raise ValueError("Negative available volume under the disclosed water convention")
    return density * volume


def dissolved_mass(pv, density_saturated, fraction_saturated, density_initial, fraction_initial):
    positive([pv, density_saturated, density_initial]); fraction([fraction_saturated, fraction_initial])
    return pv * (density_saturated * fraction_saturated - density_initial * fraction_initial)


def coal_material_mass(volume, gas_density, coal_mass_per_volume, gas_volume_per_coal_mass, ash, moisture):
    positive([volume, gas_density, coal_mass_per_volume, gas_volume_per_coal_mass]); fraction([ash, moisture])
    if ash + moisture > 1:
        raise ValueError("Ash plus moisture exceeds one")
    return gas_density * volume * coal_mass_per_volume * gas_volume_per_coal_mass * (1 - ash - moisture)


def shen_literal_mass(pv, density, sw, recovery, injected, produced, cws, cos):
    """Literal Table3 bracket; Cws/Cos dimensionless ONLY for this toy.

    The publication gives no units for these solubilities. No native solvent,
    gas-volume, pressure or EOS convention is inferred from this helper.
    """
    positive([pv, density]); fraction([sw, recovery]); positive([injected, produced, cws, cos], zero=True)
    water = pv * sw + injected - produced
    free = pv * (1 - sw) - injected + produced
    if min(water, free) < 0:
        raise ValueError("Negative phase volume under the analyst assumptions")
    return density * (free + cws * water + cos * (1 - recovery) * pv * (1 - sw))


def molal_mass_kg(water_mass_kg, solubility_mol_kg, molar_mass_g_mol):
    """Explicit analyst molal convention; source R units remain unknown."""
    positive([water_mass_kg, solubility_mol_kg, molar_mass_g_mol], zero=True)
    return water_mass_kg * solubility_mol_kg * molar_mass_g_mol / 1000


def hydrostatic_screen(depth_m, surface_C, gradient_C_km):
    """Analyst pure-CO2 critical-state screen, not a field pressure estimate."""
    positive([depth_m, gradient_C_km]); positive([surface_C], zero=True)
    t = surface_C + gradient_C_km * depth_m / 1000
    p = .101325 + 1000 * 9.80665 * depth_m / 1e6
    tc = PropsSI("Tcrit", "CO2") - 273.15
    pc = PropsSI("pcrit", "CO2") / 1e6
    return dict(depth_m=depth_m, surface_C=surface_C, gradient_C_km=gradient_C_km,
                temperature_C=t, pressure_MPa_absolute=p, critical_temperature_C=tc,
                critical_pressure_MPa=pc, pure_critical_pair_passes=(t > tc and p > pc),
                scope="Synthetic hydrostatic/geothermal assumptions; no actual mixture, well or injection limit")


def weighted_median(values, weights):
    if len(values) != len(weights) or not values:
        raise ValueError("Matching nonempty values/weights required")
    positive(weights, zero=True)
    if not all(math.isfinite(x) for x in values) or sum(weights) == 0:
        raise ValueError("Finite values and positive total weight required")
    cumulative = 0.
    for value, weight in sorted(zip(values, weights)):
        cumulative += weight
        if cumulative >= sum(weights) / 2:
            return value


def load_inputs():
    data = json.loads((ROOT / "evidence/comprehensive_review_inputs/B2-17.json").read_text())
    if hashlib.sha256((ROOT / data["source_path"]).read_bytes()).hexdigest() != data["source_sha256"]:
        raise ValueError("Stale source")
    return data


def calculate(d):
    checks = []

    def add(item, value, unit, scope):
        checks.append(dict(item=item, value=value, unit=unit, scope=scope))

    add("GHG_pie_sum", sum(d["GHG_shares_percent"].values()), "%", "Reported emission shares; not atmospheric composition or field retention")
    add("CO2_fossil_plus_landuse", 65 + 11, "%", "Fig5 components of reported76% CO2 share")
    add("five_region_2024_mass_sum", sum(d["region_emissions_Gt"].values()), "Gt/y", "IEA-labelled source series; not the separate36.3Gt dataset")
    add("five_region_2024_mass_share", sum(d["region_emissions_Gt"].values()) / 37.8 * 100, "%", "Compatible with source>62.1% statement")
    add("emission_total_series_difference", 37.8 - 36.3, "Gt/y", "Different cited datasets/boundaries; not automatically an arithmetic error")
    add("implied_preindustrial_ppm", 422.5 / 1.5, "ppm", "Rounded50% statement algebra, not an independently verified historical concentration")
    add("Fig1_country_share_sum", sum(d["figure1_country_emission_shares"]), "%", "Whole-percent labels; rounding can reconcile sum101%")
    add("Fig1_avoided_share_sum", sum(d["figure1_avoided_shares"]), "%", "Scope4-labelled shares; rounding can reconcile99%; no actual future emissions measured")
    resource = d["figure3_resource_rows"]
    add("Fig3_country_resource_sum", sum(r["mass_Gt"] for r in resource), "Gt", "Retains all16 labels, including identical Canada/UK values")
    add("Fig3_country_share_sum", sum(r["share_percent"] for r in resource), "%", "Exceeds100 if all countries share one nonoverlapping global denominator; original allocation unresolved")
    add("Fig3_top3_share_sum", sum(r["share_percent"] for r in resource[:3]), "%", "Rounded89.8% headline compatible")
    add("Fig3_facility_count_sum", sum(d["figure3_facility_counts"].values()), "facilities", "Mixed operating/construction/development/suspended categories, not current operating count")
    add("China_three_basin_mass", sum(d["China_saline_basins_Gt"]), "Gt", "Three quoted basin resources")
    add("China_three_basin_saline_share", sum(d["China_saline_basins_Gt"]) / 2420 * 100, "%", "About71.8%, not50% if quoted2.42T saline total is denominator; case basis unresolved")
    add("conditional_global_stock_low", 6 + 2, "trillion t", "Only if quoted onshore/offshore ranges are nonoverlapping")
    add("conditional_global_stock_high", 42 + 13, "trillion t", "Resource envelope, not annual service or a probability interval")
    add("cement_low_table_over_body", 794 / 79.4, "ratio", "Same229–627plants/20–60% description; preserve both source cost ranges")
    add("cement_high_table_over_body", 2695 / 269.5, "ratio", "Tenfold source cost discrepancy; native originalR238 remains unverified")
    add("integrated_industry_plant_sum", 658 + 101 + 357, "plants", "Different case from the1186-source shared-network study")
    add("conditional_shared_sector_sum", 175 + 77 + 56 + 23, "million t", "Only first sector explicitly /year in prose; require native common period before treating sum as annual")
    add("conditional_India_flat_stock", 170 * 237 / 1000, "Gt", "Flat170Mt/y over237years; not a demonstrated sustainable injection history")
    add("conditional_Netherlands_per_site", 32 / 176, "Mt/site", "Literal32million-ton source quote, no unverified replacement with32Gt")
    add("place_factor_count_closure", 22 + 16, "projects", "Reported38-project study, not a global probability sample")
    add("stochastic_99_buffer_over_ship", 5120 / 5000 * 100, "%", "R172 originalB2-08p7; not18% above ship")
    add("stochastic_100_buffer_over_ship", 5890 / 5000 * 100, "%", "R172 originalB2-08p8; different100% service case")
    add("stochastic_99_buffer_over_cycle", 5120 / 4330 * 100, "%", "Approximate cycle denominator, distinct from ship capacity")
    add("weather_cost_penalty_relative_base", 1.9 / 33.8 * 100, "%", "Source5–5.6% weather-aware versus neglected comparison, not a zero-buffer baseline")
    add("selected_global_flow_sum", 58.61 + 33.39, "Gt", "R200 domestic cumulative case; not a cross-border delivery solution")
    intervals = []
    for row in d["table4_rows"]:
        lo, hi, emission = row["low_1e10t"], row["high_1e10t"], row["emissions_1e10t"]
        midpoint = (lo + hi) / 2
        intervals.append(dict(**row, midpoint_1e10t=midpoint, midpoint_minus_Fig10=midpoint - row["Fig10_1e10t"],
                              stock_over_emissions_low=lo / emission, stock_over_emissions_high=hi / emission,
                              scope="Printed interval midpoint and cumulative stock/emission ratios; no probability median or annual rate"))
    # A distribution on the same endpoints can have a median at the low endpoint.
    add("analyst_China_interval_midpoint", (121 + 413) / 2, "1e10t", "Source bounds only; not a probability median")
    add("analyst_China_weighted_median", weighted_median([121, 267, 413], [.8, .1, .1]), "1e10t", "Explicit synthetic80/10/10% probabilities; not source uncertainty")
    a = d["analyst_geometry"]
    pv = pore_volume(a["area_m2"], a["thickness_m"], a["porosity"])
    rho, sw = a["CO2_density_kg_m3"], a["water_saturation"]
    add("analyst_pore_volume", pv, "m3", "Disclosed geometry only; no actual basin")
    add("analyst_oil_material_mass", oil_material_mass(pv, rho, a["recovery"], sw, a["water_injected_m3"], a["water_produced_m3"]), "kg", "Literal Table3 component under analyst water-volume convention")
    add("analyst_oil_volumetric_mass", rho * pv * (1 - sw) * a["B"] * a["efficiency"], "kg", "Literal B multiplier retained; in-situ/surface conversion remains unverified")
    add("analyst_saline_volumetric_mass", rho * pv * a["efficiency"], "kg", "Literal DOE saline component with disclosed geometry and efficiency; no pressure limit")
    structural, residual = rho * pv * (1 - sw), rho * pv * a["residual_saturation"]
    add("analyst_saline_structural_mass", structural, "kg", "Alternative source component, not an independent additive inventory")
    add("analyst_saline_residual_mass", residual, "kg", "Same synthetic pore volume for overlap illustration only")
    add("analyst_summed_components_over_pore_mass", (structural + residual) / (rho * pv), "ratio", "Shows why capacities on overlapping pore volumes cannot automatically be summed; no author summation error claimed")
    dissolved = dissolved_mass(pv, 1050, .02, 1000, .001)
    add("analyst_saline_dissolved_mass", dissolved, "kg", "Conditional densities/mass fractions, not native equilibrium chemistry")
    add("analyst_dissolution_with_C", dissolved * .1, "kg", "Disclosed dimensionless0.1 factor; native C unknown")
    add("analyst_areal_mass", .5 * a["area_m2"] * 4, "kg", "Disclosed coverage0.5 and4kg/m2 coefficient")
    add("analyst_coal_material_mass", coal_material_mass(50000, 1.977, 1400, .02, .1, .05), "kg", "Disclosed kg-coal/m3 and m3-gas/kg-coal basis; native nc definition unresolved")
    add("analyst_coal_volumetric_mass", 1.977 * 50000 * 20 * .1, "kg", "Disclosed20standard-m3-gas/m3-coal and0.1 efficiency")
    add("analyst_Shen_literal_mass", shen_literal_mass(pv, rho, sw, a["recovery"], a["water_injected_m3"], a["water_produced_m3"], .02, .1), "kg", "rho multiplies the ENTIRE printed bracket; Cws/Cos dimensionless in toy only")
    water_mass = .01 * .1 * pv * 1000
    add("analyst_molal_mass_conversion", molal_mass_kg(water_mass, .5, 44.01), "kg", "Only under declared mol/kg-water solubility; source R units remain unknown, so no corrected source mass inferred")
    phases = [hydrostatic_screen(depth, surface, 25) for depth in [801, 1000] for surface in [0, 10, 15]]
    return checks, intervals, phases


def main():
    data = load_inputs(); checks, intervals, phases = calculate(data)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, rows in [("checks", checks), ("resource_intervals", intervals), ("analyst_phase_screen", phases),
                       ("source_GWP", data["table1_GWP_rows"]), ("source_resource_labels", data["figure3_resource_rows"])]:
        with (OUT / ("B2-17_" + name + ".csv")).open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader(); writer.writerows(rows)
    summary = dict(study_id="B2-17", source_sha256=data["source_sha256"], limited_checks=len(checks),
                   resource_interval_rows=len(intervals), analyst_phase_rows=len(phases), source_GWP_rows=len(data["table1_GWP_rows"]),
                   native_literature_selection_reproduced=False, cited_author_models_reproduced=False,
                   accepted_Paper1_inputs_added=0, scope="Source accounting and explicitly synthetic dimensional/state components only",
                   missing_native=data["missing_native"])
    (OUT / "B2-17_reproduction_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
