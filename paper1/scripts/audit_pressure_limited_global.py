#!/usr/bin/env python3
"""B2-15 printed components with synthetic inputs; not native CO2BLOCK replay."""
from __future__ import annotations
import csv
import hashlib
import json
import math
from pathlib import Path

from scipy.special import lambertw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/comprehensive_review"


def positive(values, *, allow_zero=False):
    if not values or any(not math.isfinite(v) or (v < 0 if allow_zero else v <= 0) for v in values):
        raise ValueError("Finite values in the stated positive/nonnegative domain required")


def dimensionless_lambert_rate(a, b, reference_rate=1., branch=-1):
    """Literal Figure1 inversion ONLY for explicitly dimensionless a and b.

    The publication does not state the normalization or Lambert branch. This
    helper is never applied to raw MPa or native basin inputs. It independently
    solves a=q*(b-ln(q)); both real branches can exist.
    """
    positive([a, b, reference_rate])
    if branch not in (0, -1):
        raise ValueError("Only the two real Lambert branches are considered")
    z = -a * math.exp(-b)
    if z >= 0 or z < -1 / math.e - 1e-14:
        raise ValueError("Outside the finite real-branch domain")
    if abs(z + 1 / math.e) < 1e-14:
        w = -1.
    else:
        value = lambertw(z, branch)
        if abs(value.imag) > 1e-12 or not math.isfinite(value.real):
            raise ValueError("No finite real root")
        w = float(value.real)
    q = -a / w
    return dict(a=a, b=b, branch=branch, scaled_rate=q, rate=q * reference_rate,
                implicit_residual=q * (b - math.log(q)) - a,
                increasing_pressure_branch=(b - math.log(q) - 1 >= -1e-12),
                status="analyst_dimensionless_literal_component_not_native_injection")


def pressure_example(sigma1, p0, effective_ratio, friction_degrees, cohesion, tensile_strength):
    """Compare literal and conventional terms under disclosed analyst definitions.

    Native theta, C, stress conventions and defaults remain unverified. The
    conventional calculation does not correct the source's cohesion factor.
    """
    positive([sigma1, p0, effective_ratio])
    positive([cohesion, tensile_strength], allow_zero=True)
    if sigma1 <= p0 or not 0 < effective_ratio <= 1 or not 0 < friction_degrees < 90:
        raise ValueError("Analyst effective-stress/friction assumptions not satisfied")
    phi = math.radians(friction_degrees)
    theta = (1 - math.sin(phi)) / (1 + math.sin(phi))
    sigma3 = p0 + effective_ratio * (sigma1 - p0)
    tensile = sigma3 - p0 + tensile_strength
    base = (effective_ratio - theta) / (1 - theta) * (sigma1 - p0)
    literal_shear = base + cohesion * math.cos(phi) * math.sin(phi)
    conventional_shear = ((sigma1 + sigma3) / 2 -
                          (sigma1 - sigma3) / (2 * math.sin(phi)) +
                          cohesion / math.tan(phi) - p0)
    return dict(theta=theta, sigma3_MPa=sigma3, tensile_headroom_MPa=tensile,
                literal_shear_MPa=literal_shear, conventional_shear_MPa=conventional_shear,
                conditional_controlling_literal_MPa=min(tensile, literal_shear),
                conditional_controlling_conventional_MPa=min(tensile, conventional_shear),
                scope="Synthetic conventional effective-stress/MC definitions only; native C/theta unknown")


def cumulative_cylinder_diameter(total_rate_Mt_y, years, sites, porosity, thickness_m, density_kg_m3):
    positive([total_rate_Mt_y, years, sites, porosity, thickness_m, density_kg_m3])
    if sites != int(sites) or porosity > 1:
        raise ValueError("Integer site count and porosity <=1 required")
    mass_kg = total_rate_Mt_y * 1e9 * years
    diameter = 2 * math.sqrt(mass_kg / (sites * math.pi * porosity * thickness_m * density_kg_m3))
    return dict(years=years, cumulative_mass_kg=mass_kg, diameter_m=diameter,
                status="analyst_constant_density_mass_balance_not_native_plume")


def load_inputs():
    data = json.loads((ROOT / "evidence/comprehensive_review_inputs/B2-15.json").read_text())
    if hashlib.sha256((ROOT / data["source_path"]).read_bytes()).hexdigest() != data["source_sha256"]:
        raise ValueError("Stale source")
    return data


def calculate(data):
    checks, designs = [], []

    def add(item, value, unit, scope):
        checks.append(dict(item=item, value=value, unit=unit, scope=scope))

    model = data["model"]
    for source in data["scenarios"]:
        n, d = source["sites"], source["spacing_km"]
        designs.append(dict(**source, nominal_cell_footprint_km2=n * d ** 2,
                            centre_hull_km2=(math.sqrt(n) - 1) ** 2 * d ** 2,
                            technical_ceiling_Mt_y=n * model["site_rate_ceiling_Mt_y"],
                            technical_ceiling_30y_Gt=n * 5 * 30 / 1000,
                            technical_ceiling_80y_Gt=n * 5 * 80 / 1000,
                            native_pressure_limited_rate="", scope="Source design and technical ceiling only, not feasible basin injection"))
    for quote in data["global_quotes"]:
        name = quote["group"] + "_" + str(quote["years"]) + "y"
        rate = quote["mass_Gt"] / quote["years"]
        add(name + "_mass_over_duration", rate, "Gt/y", "Separate constant-rate horizon case, not one deployment rate trajectory")
        add(name + "_minus_quoted_rate", rate - quote["rate_Gt_y"], "Gt/y", "Compatible with rounded reported annual rates; not native model validation")
    for years in model["duration_years"]:
        unrestricted = next(x["mass_Gt"] for x in data["global_quotes"] if x["group"] == "unrestricted_M" and x["years"] == years)
        for group in ["hydrocarbon_history_M", "readiness_AB_M"]:
            mass = next(x["mass_Gt"] for x in data["global_quotes"] if x["group"] == group and x["years"] == years)
            add(group + "_" + str(years) + "y_reduction", 100 * (1 - mass / unrestricted), "%", "Endpoint-specific quote comparison; not the source's across-scenario17%average")
        for rate in [5.6, 10]:
            add(str(rate) + "Gt_y_" + str(years) + "y_cumulative", rate * years, "Gt", "Flat-rate benchmark conversion, not actual IAM deployment integration")

    inv = data["source_inventory"]
    for label, numerator, denominator in [
        ("modelled_over_scheme", inv["modelled_basins"], inv["basin_scheme_count"]),
        ("history_over_modelled", inv["hydrocarbon_history_basins"], inv["modelled_basins"]),
        ("europe_data_completion", inv["europe_modelled_basins"], inv["europe_basins_scheme"]),
        ("europe_depth_retained_entries", inv["europe_depth_filtered_entries"], inv["europe_entries"])]:
        add(label, 100 * numerator / denominator, "%", "Source selection/count arithmetic, not coverage probability or validation")
    add("265_minus_248", inv["sufficient_basins_other_prose"] - inv["modelled_basins"], "basins", "Unreconciled populations; no inferred filter correction")
    add("europe_entries_per_field", inv["europe_entries"] / inv["europe_fields"], "ratio", "Repeated fields/strata are not independent reservoir samples")

    wells = data["well_analogues"]
    add("scenario123_implied_basins", wells["scenario123_sites"] / 4, "basins", "Source992sites supports248basin basis, without resolving265")
    add("scenario11_implied_eligible_basins", wells["scenario11_sites"] / 400, "basins", "If source50800sites all follow400-site scenario")
    add("reference_wells_per_site", 5 / wells["well_reference_rate_Mt_y"], "wells/site", "Analogue based on average per-well rate, not actual required wells")
    add("M_projects_four_sites", wells["scenarioM_sites"] / 4, "projects", "Source arithmetic with four-site analogue, not an actual project inventory")
    add("M_wells_nine_per_site", wells["scenarioM_sites"] * 9, "wells", "Rounded-rate analogue; site-count horizon and actual well rates unresolved")
    add("M_well_analogue_share_of_petroleum", 100 * wells["scenarioM_sites"] * 9 / wells["petroleum_wells_comparison"], "%", "Count comparison only; no eligibility/integrity inference")
    add("north_sea_nine_well_site_equivalents", wells["north_sea_registered_wells"] / 9, "site equivalents", "Historical count analogy, not CCS-ready wells")
    for count in wells["offshore_well_range"]:
        add(str(count) + "_wells_as_nine_well_sites", count / 9, "site equivalents", "Rounded per-well-rate analogue only")
    add("M_technical_site_rate_ceiling", wells["scenarioM_sites"] * 5 / 1000, "Gt/y", "Hypothetical site ceiling before pressure; not a native sustainable rate")

    compare = data["comparison_quotes"]
    for country, physical, volume in [("Australia", 90.2, 471), ("USA", 699, 8613), ("UK", 71.2, 77.6), ("Norway", 80.7, 79.4)]:
        add(country + "_pressure_over_volumetric", 100 * physical / volume, "%", "Different data, methods, geography and horizons; not isolated pressure effect or validation")
    add("UK_quoted_difference", compare["UK_volumetric_Gt"] - compare["UK_pressure_30y_Gt"], "Gt", "Literal reported comparison")
    add("Scenario3_average_rate", compare["Scenario3_Gt_30y"] / 30, "Gt/y", "Constant-rate global scenario, not project schedule")
    add("Scenario3_above_IEA120Gt", compare["Scenario3_Gt_30y"] - compare["IEA_midcentury_cumulative_Gt"], "Gt", "Meets cumulative120 benchmark, not10Gt/y")

    examples = data["analyst_examples"]
    pressure = examples["pressure"]
    envelope = pressure_example(pressure["sigma1_MPa"], pressure["p0_MPa"], pressure["effective_stress_ratio"],
                                pressure["friction_degrees"], pressure["analyst_cohesion_strength_MPa"], pressure["tensile_strength_MPa"])
    for key, value in envelope.items():
        if key != "scope":
            add("analyst_" + key, value, "MPa" if key.endswith("MPa") else "dimensionless", envelope["scope"])
    add("analyst_cohesion_term_difference", envelope["conventional_shear_MPa"] - envelope["literal_shear_MPa"], "MPa",
        "Conditional conventional strength versus undefined source cohesion factor; no source correction")
    roots = [dimensionless_lambert_rate(a, b, examples["reference_rate_arbitrary"], branch)
             for a, b in examples["lambert_dimensionless_pairs"] for branch in [0, -1]]
    add("analyst_max_implicit_root_residual", max(abs(r["implicit_residual"]) for r in roots), "dimensionless",
        "Mathematical inversion only; bare MPa inputs are not permitted")
    plume = examples["plume"]
    cylinders = [cumulative_cylinder_diameter(plume["total_rate_Mt_y"], years, plume["sites"], plume["porosity"],
                                             plume["thickness_m"], plume["density_kg_m3"]) for years in plume["years"]]
    add("analyst_plume_diameter_80_over_30", cylinders[1]["diameter_m"] / cylinders[0]["diameter_m"], "ratio",
        "Cumulative-mass conservation scales with sqrt(time); not native CO2BLOCK geometry or prediction")
    return checks, designs, roots, cylinders


def main():
    data = load_inputs()
    checks, designs, roots, cylinders = calculate(data)
    OUT.mkdir(exist_ok=True, parents=True)
    for name, rows in [("checks", checks), ("source_designs", designs), ("analyst_lambert", roots), ("analyst_mass_geometry", cylinders)]:
        with (OUT / ("B2-15_" + name + ".csv")).open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader(); writer.writerows(rows)
    summary = dict(study_id="B2-15", source_sha256=data["source_sha256"], limited_checks=len(checks),
                   source_design_rows=len(designs), analyst_lambert_rows=len(roots), analyst_geometry_rows=len(cylinders),
                   native_CO2BLOCK_global_model_reproduced=False, public_reservoir_dataset_acquired=False,
                   accepted_Paper1_inputs_added=0, scope="Reported arithmetic and synthetic printed components only; commercial data cannot be shared by authors",
                   missing_native=data["missing_native"])
    (OUT / "B2-15_reproduction_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
