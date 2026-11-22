#!/usr/bin/env python3
"""B2-14 source arithmetic and disclosed diagnostics; no native ITEAM replay."""
from __future__ import annotations
import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/comprehensive_review"


def nonnegative(values):
    if not values or any(not math.isfinite(x) or x < 0 for x in values):
        raise ValueError("Finite nonnegative values required")


def fraction_percent(numerator, denominator):
    nonnegative([numerator, denominator])
    if denominator == 0:
        raise ValueError("Positive denominator required")
    return 100 * numerator / denominator


def spherical_cell(latitude, delta_degrees, radius_km=6371):
    """Analyst spherical geometry; not the source's unknown GIS projection."""
    if not all(math.isfinite(v) for v in [latitude, delta_degrees, radius_km]):
        raise ValueError("Finite coordinates required")
    if delta_degrees <= 0 or delta_degrees >= 180 or radius_km <= 0:
        raise ValueError("Positive cell and radius required")
    if abs(latitude) + delta_degrees / 2 >= 90:
        raise ValueError("Cell cannot cross a pole")
    half = math.radians(delta_degrees) / 2
    lat = math.radians(latitude)
    return dict(latitude_deg=latitude, width_at_centre_km=radius_km * 2 * half * math.cos(lat),
                height_km=radius_km * 2 * half,
                area_km2=radius_km ** 2 * 2 * half * (math.sin(lat + half) - math.sin(lat - half)),
                status="analyst_spherical_example_not_native_GIS")


def unresolved_field(spacing, baseline=1., amplitude=1.):
    """Two positive fields agree at both coarse samples but differ in between."""
    nonnegative([spacing, baseline, amplitude])
    if spacing <= 0 or spacing != int(spacing):
        raise ValueError("Positive integer kilometre spacing required")
    return [dict(coarse_spacing_km=spacing, x_km=i, linear_interpolant=baseline,
                 alternative_field=baseline + amplitude * math.sin(math.pi * i / spacing) ** 2,
                 status="analyst_nonuniqueness_example_not_native_geology")
            for i in range(int(spacing) + 1)]


def shared_sink(demands, unit_costs, capacity):
    """Two-stage LP: maximize service, then minimize cost at that service.

    Every source has a geographic candidate. Shared capacity may still prevent
    complete delivery. This is a disclosed counterexample, not ITEAM's algorithm.
    """
    nonnegative(demands)
    nonnegative(unit_costs)
    nonnegative([capacity])
    if len(demands) != len(unit_costs) or sum(demands) == 0:
        raise ValueError("Matched nonzero demands and costs required")
    bounds = [(0, v) for v in demands]
    service = linprog(-np.ones(len(demands)), A_ub=[np.ones(len(demands))], b_ub=[capacity],
                      bounds=bounds, method="highs")
    if not service.success:
        raise ValueError(service.message)
    served = float(sum(service.x))
    economic = linprog(unit_costs, A_ub=[np.ones(len(demands))], b_ub=[capacity],
                       A_eq=[np.ones(len(demands))], b_eq=[served], bounds=bounds, method="highs")
    if not economic.success:
        raise ValueError(economic.message)
    return dict(sink_capacity_Mt_y=capacity, geographically_eligible_percent=100.,
                served_Mt_y=served, served_percent=fraction_percent(served, sum(demands)),
                disclosed_cost=float(economic.fun), flows=economic.x.tolist(),
                status="analyst_shared_sink_LP_not_native_pairing")


def load_inputs():
    data = json.loads((ROOT / "evidence/comprehensive_review_inputs/B2-14.json").read_text())
    if hashlib.sha256((ROOT / data["source_path"]).read_bytes()).hexdigest() != data["source_sha256"]:
        raise ValueError("Stale source")
    return data


def calculate(data):
    checks = []

    def add(item, value, unit, scope):
        checks.append(dict(item=item, value=value, unit=unit, scope=scope))

    quality = data["quality_table"]
    for stage, area, spacing in zip(quality["stages"], quality["area_per_well_km2"], quality["spacing_upper_km"]):
        add(stage + "_square_root_area", math.sqrt(area), "km", "Square-grid convention only; not equivalence for irregular wells")
        add(stage + "_square_grid_spacing_residual", math.sqrt(area) - spacing, "km", "Printed spacing boundary is strict <; source map-scale inequalities retained literally")
        add(stage + "_nominal_1km_cells_per_well", area / quality["grid_km"] ** 2, "count", "Conditional nominal area ratio, not new independent observations")
    emission = data["emissions_table"]
    sectors = emission["sectors"]
    add("Table2_count_sum", sum(x["count"] for x in sectors), "count", "Printed sector rows")
    total = sum(x["Mt_y"] for x in sectors)
    add("Table2_emission_sum", total, "Mt/y", "Literal displayed sector rows, no correction")
    add("Table2_sum_minus_total", total - emission["total_Mt_y"], "Mt/y", "0.1 discrepancy can fit display rounding")
    add("Table2_conditional_rounding_overlap", abs(total - emission["total_Mt_y"]) <= .05 * (len(sectors) + 1),
        "boolean", emission["rounding_assumption"])
    captured = emission["total_Mt_y"] * emission["net_capture_fraction"]
    add("printed_total_times_85percent", captured, "Mt/y", "Scenario product, not measured avoided or retained CO2")
    for sector in sectors:
        add(sector["name"] + "_times_85percent", sector["Mt_y"] * emission["net_capture_fraction"],
            "Mt/y", "Conditional common capture fraction; no native source-case reproduction")
    captive = emission["captive_power_Mt_y"]
    add("captive_share_of_power", fraction_percent(captive, sectors[0]["Mt_y"]), "%", "Magnitude comparison, not a justified negligible-error criterion")
    add("power_minus_captive", sectors[0]["Mt_y"] - captive, "Mt/y", "Conditional subtraction reproduces rounded4.34Gt prose; no accepted correction")
    add("conditional_total_minus_captive", emission["total_Mt_y"] - captive, "Mt/y", "Hypothesis only; exact enterprise overlap remains unknown")
    add("conditional_capture_difference", captive * emission["net_capture_fraction"], "Mt/y", "Hypothesis only; source total preserved")
    add("conditional_capture_after_removing_captive", (emission["total_Mt_y"] - captive) * emission["net_capture_fraction"],
        "Mt/y", "No corrected native input adopted")

    capacity = data["capacities_table"]
    for kind in ["theoretical", "effective"]:
        add("Table3_" + kind + "_sum_residual", capacity["onshore_" + kind + "_Gt"] + capacity["offshore_" + kind + "_Gt"] - capacity["total_" + kind + "_Gt"], "Gt", "Printed stock sums")
        add("Table3_" + kind + "_onshore_percent", fraction_percent(capacity["onshore_" + kind + "_Gt"], capacity["total_" + kind + "_Gt"]), "%", "Resource stock share, not annual flow share")
    for group in ["onshore", "offshore", "total"]:
        add("Table3_" + group + "_effective_over_theoretical", fraction_percent(capacity[group + "_effective_Gt"], capacity[group + "_theoretical_Gt"]), "%", "Reported hierarchy ratio, not independently calibrated efficiency")
    for match in capacity["matching"]:
        name = "matched_" + str(match["radius_km"]) + "km_"
        add(name + "sum_residual", match["onshore_Mt_y"] + match["offshore_Mt_y"] - match["total_Mt_y"], "Mt/y", "Printed annual matched-flow sums")
        add(name + "onshore_percent", fraction_percent(match["onshore_Mt_y"], match["total_Mt_y"]), "%", "Matching result share, not pressure-safe service")
        add(name + "captured_percent", fraction_percent(match["total_Mt_y"], captured), "%", "85% times printed Table2 total as conditional common denominator")
        add(name + "gross_emission_percent", fraction_percent(match["total_Mt_y"], emission["total_Mt_y"]), "%", "Gross-emission denominator differs from captured mass")
    add("effective_stock_over_800km_annual_flow", capacity["total_effective_Gt"] * 1000 / capacity["matching"][-1]["total_Mt_y"], "y", "Stock/flow arithmetic, not lifetime or sustainable injection capacity")

    quotes = data["source_quotes"]
    for flow in quotes["body_under90_flow_Gt_y"]:
        add("body_" + str(flow) + "Gt_over_7.6", fraction_percent(flow, emission["captured_rounded_Gt_y"]), "%", "Source mass-denominator comparison; no replaced source result")
    # Conditional nearest0.1Gt displays and nearest1% claim: no overlap with59%.
    upper = 100 * (4.2 + .05) / (7.6 - .05)
    add("4.2_over_7.6_rounding_upper", upper, "%", "Conditional displayed precision, not measured uncertainty")
    add("rounding_upper_below_59_lower", 58.5 - upper, "percentage points", "Positive gap rules out this specific rounding explanation; actual denominator unresolved")
    add("implied_denominator_for_4.2_at59percent", 4.2 / .59, "Gt/y", "Inverse diagnostic only, not a recovered native denominator")
    add("300km_all_matches_over_gross", fraction_percent(capacity["matching"][1]["total_Mt_y"], emission["total_Mt_y"]), "%", "Same-case conditional upper bound before applyingcost90; native industrial-emissions denominator unresolved")
    add("Figure9_named_basin_curves", len(data["figure_legends"]["F9_basins"]), "count", "Named curves, not all national basin sites or independent optima")
    add("Figure10_named_regions", len(data["figure_legends"]["F10_regions"]), "count", "Native labels preserved as geography, not a jurisdictional inference")
    add("proposed_coalitions", len(data["coalitions"]), "count", "Policy proposal, not implemented sharing infrastructure")

    analyst = data["analyst_examples"]
    cells = [spherical_cell(lat, analyst["grid_delta_deg"], analyst["spherical_radius_km"])
             for lat in analyst["cell_latitudes_deg"]]
    grids = []
    for spacing in analyst["coarse_spacing_km"]:
        rows = unresolved_field(spacing, analyst["interpolant_baseline"], analyst["unobserved_peak_amplitude"])
        grids.extend(rows)
        add("analyst_" + str(spacing) + "km_unresolved_peak", max(r["alternative_field"] - r["linear_interpolant"] for r in rows),
            "dimensionless", "Two fields agree at observed coarse endpoints; no native property error inferred")
    lps = [shared_sink(analyst["LP_source_demands_Mt_y"], analyst["LP_unit_costs"], cap) for cap in analyst["LP_sink_caps_Mt_y"]]
    for row in lps:
        row["flows"] = json.dumps(row["flows"])
    return checks, cells, grids, lps


def main():
    data = load_inputs()
    checks, cells, grids, lps = calculate(data)
    OUT.mkdir(exist_ok=True, parents=True)
    for name, rows in [("checks", checks), ("analyst_cells", cells), ("analyst_grid", grids), ("analyst_LP", lps)]:
        with (OUT / ("B2-14_" + name + ".csv")).open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader(); writer.writerows(rows)
    summary = dict(study_id="B2-14", source_sha256=data["source_sha256"], limited_checks=len(checks),
                   analyst_cell_rows=len(cells), analyst_grid_rows=len(grids), analyst_LP_rows=len(lps),
                   native_ITEAM_GIS_cost_model_reproduced=False, accepted_Paper1_inputs_added=0,
                   scope="Printed arithmetic and disclosed geometry/nonuniqueness/shared-sink examples only", missing_native=data["missing_native"])
    (OUT / "B2-14_reproduction_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
