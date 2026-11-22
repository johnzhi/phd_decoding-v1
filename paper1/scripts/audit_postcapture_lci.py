#!/usr/bin/env python3
"""B2-12 printed inventory components and disclosed mathematical examples.

No native MoMILP, cost regression, GaBi/CML inventory, pressure service or
complete author case is reproduced. Literal source units remain separate from
conditional comparisons. The previously excluded combined15 quote stays HOLD.
"""
from __future__ import annotations
import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/comprehensive_review"


def load_inputs():
    data = json.loads((ROOT / "evidence/comprehensive_review_inputs/B2-12.json").read_text())
    for source in [data["source"], *data["cited_sources"]]:
        if hashlib.sha256((ROOT / source["path"]).read_bytes()).hexdigest() != source["sha256"]:
            raise ValueError(f"Changed source: {source['path']}")
    return data


def cylinder(diameter, height, thickness):
    """Analyst cylindrical volume plus two flat ends; no pressure-vessel code."""
    if not all(math.isfinite(v) and v > 0 for v in [diameter, height, thickness]):
        raise ValueError("Positive finite dimensions required")
    volume = math.pi * diameter**2 * height / 4
    area = math.pi * diameter * height + math.pi * diameter**2 / 2
    return dict(volume_m3=volume, area_m2=area, thin_shell_volume_m3=area * thickness)


def choose_plan(cost, emissions, weight=None, emission_limit=None):
    """Disclosed one-of-N MILP, not an author network or native normalization."""
    c = np.asarray(cost, dtype=float); e = np.asarray(emissions, dtype=float)
    if c.ndim != 1 or not len(c) or c.shape != e.shape or not np.all(np.isfinite([c, e])):
        raise ValueError("Matching finite one-dimensional alternatives required")
    if (weight is None) == (emission_limit is None):
        raise ValueError("Exactly one scalarization or epsilon constraint required")
    constraints = [LinearConstraint(np.ones((1, len(c))), 1, 1)]
    if weight is not None:
        if not math.isfinite(weight) or not 0 <= weight <= 1:
            raise ValueError("Weight in[0,1] required")
        objective = (1 - weight) * c + weight * e
    else:
        if not math.isfinite(emission_limit):
            raise ValueError("Finite emission limit required")
        objective = c
        constraints.append(LinearConstraint(e.reshape(1, -1), -np.inf, emission_limit))
    result = milp(objective, integrality=np.ones(len(c)),
                  bounds=Bounds(np.zeros(len(c)), np.ones(len(c))), constraints=constraints,
                  options={"mip_rel_gap": 0})
    if not result.success:
        raise RuntimeError(result.message)
    selected = int(np.argmax(result.x))
    return dict(selected=selected, cost=float(c[selected]), emissions=float(e[selected]))


def active_and_increment_fugitives(active, years, factor_t_h, hours=8760):
    """Compare stated-state and literal activation-increment components only."""
    active = np.asarray(active, dtype=float); years = np.asarray(years, dtype=float)
    if (active.ndim != 1 or not len(active) or active.shape != years.shape
            or not np.all(np.isfinite([active, years])) or np.any(years <= 0)
            or np.any((active < 0) | (active > 1)) or not math.isfinite(factor_t_h)
            or not math.isfinite(hours) or factor_t_h < 0 or hours <= 0):
        raise ValueError("Matching finite activity/year series and positive calendar required")
    delta = np.diff(np.r_[0, active])
    return dict(active_state_t=float((active * years).sum() * factor_t_h * hours),
                activation_increment_t=float((delta * years).sum() * factor_t_h * hours))


def calculate(data):
    rows = []
    def add(item, value, unit, basis, locator, interpretation):
        rows.append(dict(item=item, value=value, unit=unit, basis=basis,
                         source_locator=locator, interpretation=interpretation))
    g = data["geometry"]; tank = data["tanks"]; construction = data["ship_construction"]
    for j, pressure in enumerate(g["pressure_MPa"]):
        geo = cylinder(g["diameter_m"][j], g["height_m"], g["thickness_m"])
        add(f"tank_{pressure}MPa_thinwall_diameter", 2 * g["thickness_m"] * g["allowable_stress_MPa"] / pressure,
            "m", "analyst thin-wall hoop-stress relation", "p7 Table3", "Comparison only; no native equation, ASME design or thickness tolerance reproduced")
        for key, value in geo.items():
            add(f"tank_{pressure}MPa_{key}", value, "m3" if "m3" in key else "m2",
                "analyst cylinder with two flat ends", "pp7,9 Tables3–4", "Uses displayed diameter; real heads, allowance and engineering code missing")
        add(f"tank_{pressure}MPa_mass_if_steel_unit_kg_m3", geo["thin_shell_volume_m3"] * g["steel_density_printed"] / 1000,
            "tsteel", "explicit alternative unit interpretation", "pp7,9 Tables3–4", "Table3 prints7861t/m3; kg/m3 interpretation approximates Table4, not a source correction")
        add(f"tank_{pressure}MPa_mass_if_literal_t_m3", geo["thin_shell_volume_m3"] * g["steel_density_printed"],
            "tsteel", "literal printed steel-density unit", "p7 Table3", "Factor1000 larger than kg/m3 interpretation; native unit unresolved")
        add(f"tank_{pressure}MPa_conditional_CO2_mass", g["table4"]["volume_m3"][j] * g["CO2_density_kg_m3"][j] / 1e6,
            "ktCO2", "printed volume/density component", "pp7,9 Tables3–4", "Gross capacity; no98% fill or actual EOS/purity validation")
    add("assumed_density_decrease", 100 * (1 - g["CO2_density_kg_m3"][1] / g["CO2_density_kg_m3"][0]),
        "%", "source assumed-density arithmetic", "pp3,7", "13% wording agrees with1150/1000 assumptions, not a general pressure-only EOS law")
    add("Table4_low_high_volume_ratio", g["table4"]["volume_m3"][0] / g["table4"]["volume_m3"][1],
        "ratio", "printed tank volume comparison", "p9 Table4", "About4.6 volume versus5.28 mass ratio; preserve approximate five-times wording")
    for j, capacity in enumerate(tank["ship_capacity_kt"]):
        for pressure, count_key, steel_key, GHG_key, tank_mass, tank_capacity in [
                (.7, "number_low", "steel_low_t", "GHG_low_t", 574, 5.28),
                (1.5, "number_high", "steel_high_t", "GHG_high_t", 241, 1)]:
            add(f"{capacity}kt_{pressure}MPa_ceil_tanks", math.ceil(capacity / tank_capacity), "tanks",
                "printed capacity ceiling component", "p9 Tables4–5", "Matches printed count; no buffer availability or headspace feasibility inferred")
            add(f"{capacity}kt_{pressure}MPa_rounded_mass_residual", tank[steel_key][j] - tank[count_key][j] * tank_mass,
                "tsteel", "rounded table comparison", "p9 Tables4–5", "Displayed one-tank mass is rounded; residual is not a proven material error")
            if tank[GHG_key][j] is not None:
                add(f"{capacity}kt_{pressure}MPa_steel_GWP", tank[steel_key][j] * tank["steel_EF_t_t"], "tCO2e",
                    "printed steel-factor component", "p9 Table5", "Compare rounded table values only; no complete construction LCI reproduced")
    for j, capacity in enumerate(construction["capacity_t"]):
        add(f"ship_{capacity}t_DWT_from85percent_cargo", capacity / (1 - construction["noncargo_DWT_fraction"]), "tDWT",
            "source cargo/DWT assumption", "p10 Table10", "Not legal payload, stability, power or shipyard validation")
        add(f"ship_{capacity}t_base_plus_tanks", construction["base_GHG_t"][j] + construction["low_tank_GHG_t"][j], "tCO2e",
            "printed construction accounting", "p10 Table10", "Reported total reconstructs; source inventory/regression remains unverified")
        add(f"ship_{capacity}t_tank_GHG_if_continuous_count", capacity / 1000 / 5.28 * 574 * 2.19, "tCO2e",
            "explicit continuous-count comparison", "pp9–10 Tables5,10", "Pattern approximates ship tank column, not integer facility table; native sizing basis unresolved")
    add("high10kt_construction_sum", construction["base_GHG_t"][1] + construction["high_10kt_tank_GHG_t"], "tCO2e",
        "printed component sum", "p10 Table10", "10061 remains reported construction factor, not independent ship LCA")
    add("facility_site_component_sum", sum(tank["site_components_t_per_kt"]), "tCO2e/ktcapacity",
        "printed component sum", "pp9,23", "767.59 rounds to Appendix768; ship-capacity versus stored-flow unit still needs mapping")
    add("50kt_storage_appendix_minus_body", data["appendix"]["storage_50kt_GHG_t"] - tank["GHG_low_t"][-1], "tCO2e",
        "literal body/appendix comparison", "pp9,23", "12027 versus12567; do not select a corrected cell")
    op = data["operation"]
    add("ship_WtW_component_sum", op["combustion_g_kWh"] + op["supply_g_kWh"], "gCO2e/kWh",
        "printed fuel-boundary sum", "p10", "488+141=629; underlying methane/carbon factors not reproduced")
    for cap, energy, reported in zip(op["ship_capacities_kt"], op["energy_MWh_day"], op["WtW_t_day"]):
        value = energy * op["total_g_kWh"] / 1000
        add(f"ship_{cap}kt_energy_times_WtW_factor", value, "tCO2e/day", "conditional power/energy basis comparison", "pp22–23",
            "Requires compatible engine-output versus fuel-energy basis; exact unrounded daily factors missing")
        add(f"ship_{cap}kt_daily_factor_residual", reported - value, "tCO2e/day", "printed daily-factor comparison", "pp22–23",
            "Do not silently replace either source factor;6kt residual about0.3%")
    for label, factor in [("body", op["terminal_fugitive_body_t_h"]), ("appendix", op["terminal_fugitive_appendix_t_h"])]:
        add(label + "_terminal_fugitive_30y", factor * 8760 * 30, "tCO2e/site",
            "conditional uninterrupted30year activity", "pp8,23", "Literal factors differ tenfold; no actual-site count or availability assigned")
        comparison = active_and_increment_fugitives([1] * 5, [6] * 5, factor)
        for key, value in comparison.items():
            add(label + "_toy_" + key, value, "tCO2e", "disclosed five-period activity example", "p17 Eq12",
                "Active state and activation increment differ; no claim native code follows printed increment")
    retired = active_and_increment_fugitives([1, 1, 0], [6, 6, 6], op["terminal_fugitive_body_t_h"])
    add("toy_retired_increment_total", retired["activation_increment_t"], "tCO2e", "disclosed activity example", "p17 Eq12",
        "Negative retirement increments can cancel earlier release; source monotonicity/implementation unknown")
    lorry = data["lorry"]
    add("lorry_construction_component_sum", lorry["construction_vehicle_t"] + lorry["construction_tank_t"], "tCO2e/lorry",
        "printed component sum", "p12", "25.1+44.9=70; no truck/tank geometry or native LCA reproduced")
    # Conventional factors inferred here only test the table's displayed unit
    # conversion. They are not adopted as a new lifecycle inventory.
    for species, value, factor in zip(lorry["species"], lorry["input_values"], [1, 28, 265]):
        for interpretation, scale in [("literal_g_to_kg", .001), ("alternative_input_kg", 1)]:
            add(species + "_" + interpretation, value * factor * scale, "kgCO2e/km",
                "conditional unit/characterisation comparison", "p12 Table12", "Input g/km versus output kg/km differs1000; native Shires/CML conversion unresolved")
    add("lorry_appendix_body_factor_difference", lorry["appendix_total_kg_km"] - lorry["body_total_kg_km"], "kgCO2e/km",
        "literal body/appendix comparison", "pp12,23", "7.7 versus7.78; no source value corrected")
    handling = data["handling"]
    for cap, value in zip(handling["capacity_t"], handling["reported_kg_trip"]):
        for stages in [1, 2]:
            expected = cap * handling["body_kWh_t"] * handling["NO_grid_kg_kWh"] * stages
            add(f"handling_{cap}t_{stages}stages", expected, "kgCO2e/trip", "explicit one/two-operation comparison", "p12 Table13",
                "Ships' two-operation implied grid approximately0.03131 can round to0.03; native loading convention/unrounded input unresolved")
        add(f"handling_{cap}t_implied_two_stage_grid", value / (cap * handling["body_kWh_t"] * 2), "kgCO2e/kWh",
            "conditional inverse component", "p12 Table13", "Not an accepted supplier factor; truck rounding/mass basis remains open")
    for cap, energy in zip(handling["appendix_ship_capacity_t"], handling["appendix_MWh_trip"]):
        add(f"appendix_handling_{cap}t_specific_work", energy * 1000 / cap, "kWh/t",
            "printed appendix energy/cargo conversion", "p23 TableA2", "20/50kt entries yield0.1 versus body0.2; stage/batch basis unresolved")
    case = data["case"]
    add("storage_resource_sum", sum(case["resource_Mt"]), "MtCO2", "printed stock sum", "p15 Table14",
        "6051Mt resource is not annual pressure-constrained injection service")
    add("profile_rounded_source_sum", sum(case["profile_rounded_source_Mt"]), "MtCO2", "rounded legend sum", "p16 Figure15",
        "296 is compatible with296.3 rounded total; source with zero printed is not known zero flow")
    for name, endpoints in case["endpoint_Mt_year"].items():
        for intervals in [24, 30]:
            add(f"{name}_CAGR_{intervals}year_interval", 100 * ((endpoints[1] / endpoints[0]) ** (1 / intervals) - 1), "%",
                "conditional calendar comparison", "p15", "Thirty-year equivalent roughly matches reported7/14/10%; no complete period-average/calendar arrays inferred")
    for reported in data["best_reported"]:
        add(reported["case"] + "_quoted_mass_equivalent", reported["total_kt"] / reported["GWP_kg_t"], "MtCO2stored",
            "prose-only denominator diagnostic", "pp18,20,22", "Not native mass proof; combined15 remainsHOLD despite internally compatible prose ratios")
        add(reported["case"] + "_quoted_GWP_mass_percent", reported["GWP_kg_t"] / 10, "%",
            "unit conversion of reported quote", "pp18,20,22", "Postcapture burden/stored-mass ratio, not loss fraction, capture efficiency or whole-chain avoidance")
    for count in [3, 4, 6, 9]:
        add(f"conditional_{count}well_construction", count * data["appendix"]["well_construction_t"] / 1000, "ktCO2e",
            "conditional integer-well accounting", "pp19–21,23", "Approximates labels191/254/381/572; no actual well schedule or pressure feasibility reconstructed")
    add("one_well_30y_fugitive", data["appendix"]["well_fugitive_g_h"] / 1e6 * 8760 * 30, "tCO2e",
        "literal grams-to-tonnes and hypothetical continuous activity", "p23", "0.76212t per well is not measured field leakage or retention")
    for days in [1, 10, 46, 50]:
        add(f"literal_vent_ratio_{days}days", days / op["buildup_days"] * op["vent_fraction_per_day"], "fraction under printed-percentage interpretation",
            "literal Eq8 algebra treating EF4 as dimensionless percentage", "pp12,16–17", "Positive before46days; body per-day rate versus printed percentage definition unresolved. Not an actual cargo-loss estimate")
        add(f"conditional_threshold_vent_{days}days", max(0, days - op["buildup_days"]) * op["vent_fraction_per_day"], "fraction of initial capacity/trip",
            "explicit alternative threshold/constant-volume interpretation", "p12", "Not a corrected native BOG law; density/compounding/pressure controller unknown")
    add("days_divided_by24_ratio", 1 / 24, "ratio", "literal unit diagnostic", "pp16–17 Eq8",
        "TRIP defined in days and factor per day; dividing by24 would reduce by24 unless native TRIP uses hours")
    weights = []
    for weight in np.linspace(0, 1, 11):
        result = choose_plan([0, 6, 10], [10, 6, 0], weight=float(weight))
        weights.append(dict(emission_weight=float(weight), **result, basis="Analyst three-plan MILP; not an author CCS case"))
    eps = choose_plan([0, 6, 10], [10, 6, 0], emission_limit=6)
    add("toy_weighted_sum_middle_plan_selected", sum(r["selected"] == 1 for r in weights), "runs",
        "disclosed nonconvex three-plan example", "pp16,18–19", "Weighted sums miss a nondominated discrete point; sampled native runs do not certify complete Pareto coverage")
    add("toy_epsilon_middle_plan", eps["selected"], "plan index", "independent epsilon-constrained MILP", "pp16,18–19",
        "Selects nondominated middle plan in the example; no native optimum tested")
    for label, scale in [("tonne", 1), ("kilogram", 1000)]:
        result = choose_plan([100, 120], [10 * scale, scale], weight=.5)
        add("toy_weighted_choice_" + label, result["selected"], "plan index", "disclosed unnormalised cost/mass example", "p16 Eq2",
            "Same numeric percentage weight changes choice under mass units; native normalisation/implicit carbon price missing")
    designs = []
    for design in data["generic_designs"]:
        row = dict(design)
        if design["mode"] == "ship":
            index = op["ship_capacities_kt"].index(design["capacity_t"] / 1000)
            speed = op["ship_speed_kmh"]; loading = op["ship_loading_h"][index]; hours = op["ship_hours_year"]
        else:
            speed = op["lorry_speed_kmh"]; loading = op["lorry_loading_h"]; hours = op["lorry_hours_year"]
        row.update(analyst_one_leg_h=design["distance_km"] / speed,
                   analyst_roundtrip_with_loading_h=2 * design["distance_km"] / speed + loading)
        trips = math.floor(hours / row["analyst_roundtrip_with_loading_h"])
        row.update(analyst_integer_trips_year=trips, analyst_full_cargo_t_year=trips * design["capacity_t"],
                   analyst_98percent_cargo_t_year=trips * design["capacity_t"] * .98,
                   author_GWP_kg_t="", basis="Source design labels; disclosed roundtrip/combined-loading/full-or98% examples only. No native annual GWP/availability reproduced.")
        designs.append(row)
    return rows, designs, weights


def main():
    data = load_inputs(); rows, designs, weights = calculate(data)
    for name, values in [("B2-12_checks.csv", rows), ("B2-12_generic_designs.csv", designs), ("B2-12_scalarization_example.csv", weights)]:
        with (OUT / name).open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=values[0], lineterminator="\n")
            writer.writeheader(); writer.writerows(values)
    report = dict(study_id="B2-12", limited_checks=len(rows), source_design_rows=len(designs),
                  analyst_scalarization_rows=len(weights), author_model="not_reproduced",
                  combined15_status="HOLD_CONFLICTING_BEST_SOLUTION_CASE",
                  source_quotes_not_repaired=True, existing_case_exclusion_7045333_preserved=True,
                  newly_accepted_operating_GHG_inputs=0, excluded_missing_inputs=data["missing_inputs"])
    (OUT / "B2-12_reconciliation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
