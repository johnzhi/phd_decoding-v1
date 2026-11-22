#!/usr/bin/env python3
"""B2-16 printed arithmetic and synthetic components, not native C3IAM/GCOP."""
from __future__ import annotations
import csv
import hashlib
import json
import math
from pathlib import Path

from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/comprehensive_review"


def finite(values, *, nonnegative=False):
    if not values or any(not math.isfinite(x) or (x < 0 if nonnegative else x <= 0) for x in values):
        raise ValueError("Finite values in the stated positive/nonnegative domain required")


def deployment(year, start, u, maximum):
    """Literal Eq28 on its disclosed rising segment; no native U/SD is supplied."""
    finite([year, start]); finite([u, maximum], nonnegative=True)
    if start >= 2050 or not start <= year <= 2050 or maximum > 1:
        raise ValueError("Require start <= year <=2050, start<2050 and maximum<=1")
    return maximum * math.exp(-(u * (1 - (year - start) / (2050 - start))) ** 2)


def learning_cost(capacity, initial_capacity, initial_cost, rate):
    finite([capacity, initial_capacity, initial_cost])
    if not math.isfinite(rate) or not 0 <= rate < 1:
        raise ValueError("Learning rate must lie in [0,1)")
    # This is the positive-domain Eq16 component, without source maturity/onset.
    return initial_cost * (capacity / initial_capacity) ** math.log2(1 - rate)


def avoided_unit_cost(lcoe_ref, lcoe_ccs, er_ref, er_ccs):
    finite([lcoe_ref, lcoe_ccs, er_ref, er_ccs], nonnegative=True)
    if er_ref <= er_ccs:
        raise ValueError("Positive avoided emissions per unit output required")
    return (lcoe_ccs - lcoe_ref) / (er_ref - er_ccs)


def lcoe_learning_example(d):
    """Reconstruct Eq22/24 using explicit analyst annual cost/CF assumptions."""
    i, om, f0, fd = (d[k] for k in ["capital_USD", "annual_OM_USD", "annual_fuel_initial_USD", "annual_fuel_doubled_USD"])
    crf, cf0, cfd, hours, power = (d[k] for k in ["CRF_per_year", "CF_initial", "CF_doubled", "hours_per_year", "power_MW"])
    li, lo = d["capital_learning"], d["OM_learning"]
    finite([i, om, f0, fd, crf, cf0, cfd, hours, power])
    if max(cf0, cfd) > 1 or not 0 <= min(li, lo) <= max(li, lo) < 1:
        raise ValueError("Invalid capacity factor or learning fraction")
    initial = (crf * i + om + f0) / (cf0 * hours * power)
    doubled = (crf * (1 - li) * i + (1 - lo) * om + fd) / (cfd * hours * power)
    printed_lr = 1 - (crf * (1 - li) * i + (1 - lo) * om + fd) / (crf * i + om + f0) * cf0 / cfd
    return dict(initial_USD_MWh=initial, doubled_USD_MWh=doubled,
                learning_direct=1 - doubled / initial, learning_Eq24=printed_lr,
                residual=printed_lr - (1 - doubled / initial))


def aggregate_lp(d, oil_price, *, exact_targets=False):
    """One-country, two-source/two-sink synthetic Eq3/7–14 example.

    All flows are cumulative Mt, cost is million USD. This is not a native
    country, route, power path or author case. Separate source sectors avoid
    pretending to resolve the publication's mixed-cluster attribution.
    """
    finite([oil_price], nonnegative=True)
    limits, targets = d["source_limits_Mt"], d["sector_targets_Mt"]
    finite(limits); finite(targets)
    finite([d["EOR_capacity_Mt"], d["saline_capacity_Mt"], d["displacement_t_per_bbl"]])
    gross = d["gross_unit_cost_USD_t"]
    finite(gross)
    revenue = oil_price / d["displacement_t_per_bbl"]
    # x: power->EOR, power->saline, nonpower->EOR, nonpower->saline.
    costs = [gross[0] - revenue, gross[0], gross[1] - revenue, gross[1]]
    matrix = [[1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1]]
    upper = [*limits, d["EOR_capacity_Mt"], d["saline_capacity_Mt"]]
    sectors = [[1, 1, 0, 0], [0, 0, 1, 1]]
    if exact_targets:
        result = linprog(costs, A_ub=matrix, b_ub=upper,
                         A_eq=sectors, b_eq=targets, bounds=(0, None), method="highs")
    else:
        result = linprog(costs, A_ub=matrix + [[-v for v in row] for row in sectors],
                         b_ub=upper + [-t for t in targets], bounds=(0, None), method="highs")
    if not result.success:
        raise ValueError("Synthetic case infeasible: " + result.message)
    x = result.x
    return dict(oil_price_USD_bbl=oil_price, exact_targets=exact_targets,
                power_EOR_Mt=x[0], power_saline_Mt=x[1], nonpower_EOR_Mt=x[2], nonpower_saline_Mt=x[3],
                total_Mt=sum(x), target_Mt=sum(targets), excess_Mt=sum(x) - sum(targets),
                EOR_Mt=x[0] + x[2], objective_million_USD=float(result.fun),
                scope="Analyst cumulative LP only; no native global flows or annual pressure limit")


def load_inputs():
    data = json.loads((ROOT / "evidence/comprehensive_review_inputs/B2-16.json").read_text())
    if hashlib.sha256((ROOT / data["source_path"]).read_bytes()).hexdigest() != data["source_sha256"]:
        raise ValueError("Stale source")
    return data


def calculate(d):
    checks = []

    def add(item, value, unit, scope):
        checks.append(dict(item=item, value=value, unit=unit, scope=scope))

    q = d["source_quotes"]
    add("target_from_IEA", q["IEA_target_Gt"] - q["excluded_Gt"], "Gt", "Source target accounting only; not net avoided GHG")
    add("sector_target_sum", sum(q["sector_targets_Gt"]), "Gt", "Global lower bounds in Eq9/10")
    add("sink_flow_sum", q["saline_flow_Gt"] + q["EOR_flow_Gt"], "Gt", "Reported cumulative injection, not annual pressure service")
    for typ in ["saline", "EOR"]:
        add(typ + "_flow_share", 100 * q[typ + "_flow_Gt"] / q["target_Gt"], "%", "Cumulative source case")
        add(typ + "_global_stock_utilization", 100 * q[typ + "_flow_Gt"] / q[typ + "_stock_Gt"], "%", "Global mass/stock ratio; not necessarily country-average utilization")
    add("basin_count_sum", sum(q["basin_type_counts"]), "basins", "Reported inventory")
    add("selected_sink_count_sum", sum(q["selected_sink_type_counts"]), "sinks", "Reported selected basins")
    add("stock_sum", q["saline_stock_Gt"] + q["EOR_stock_Gt"], "Gt", "Volumetric cumulative resource")
    for key, numerator, denominator in [("clusters_selected", 3093, 4220), ("sinks_selected", 432, 794), ("regions_selected", 85, 87)]:
        add(key, 100 * numerator / denominator, "%", "Source population fraction; not probability or validation")
    add("cluster_threshold_ratio", q["methods_threshold_Mt_y"] * 1e6 / q["body_threshold_t_y"], "ratio", "Literal method/body threshold conflict; no correction")
    rows = d["figure1_country_rows"]
    total = sum(r["mass_Gt"] for r in rows)
    add("fig1_mass_sum", total, "Gt", "Rounded nine-row source transcription")
    add("fig1_sum_minus_global", total - q["global_emissions_Gt"], "Gt", "Within nine nearest 0.1 Gt intervals and global interval")
    add("fig1_display_share_sum", sum(r["share_percent"] for r in rows), "%", "Compatible with nine nearest 0.1 percentage-point intervals")
    add("fig1_weighted_power", sum(r["mass_Gt"] * r["power_percent"] / 100 for r in rows), "Gt", "Rounded pie weights, not original emission arrays")
    add("eight_country_emission_share", 100 * sum(r["mass_Gt"] for r in rows[:-1]) / q["global_emissions_Gt"], "%", "These eight Fig1 regions differ from eight selected Fig4 regions")
    add("eight_country_emission_share_rounding_upper", 100 * (sum(r["mass_Gt"] for r in rows[:-1]) + .4) / (q["global_emissions_Gt"] - .05), "%", "Nearest-display upper still below 83.5%; denominator/case unresolved for the 84% prose")
    add("fig4_eight_mass_sum", sum(d["figure4_country_mass_Gt"]), "Gt", "Different selected-country set from Fig1")
    add("fig4_eight_target_share", 100 * sum(d["figure4_country_mass_Gt"]) / q["target_Gt"], "%", "Compatible with the 76% headline")
    add("power_inventory_fraction", 100 * q["power_emissions_Gt"] / q["global_emissions_Gt"], "%", "Source inventory, not captured-power fraction")
    add("nonpower_inventory", q["global_emissions_Gt"] - q["power_emissions_Gt"], "Gt", "Source inventory difference")
    add("EOR_66percent_power", .66 * q["EOR_flow_Gt"], "Gt", "Approximate source sector share only")
    add("China_72percent_nonpower", .72 * 26.68, "Gt", "Approximate reported national sector share")
    add("US_EOR_fraction", 100 * 5.27 / 16.09, "%", "Reported cumulative mass ratio")
    add("Australia_98percent_power", .98 * 1.86, "Gt", "Approximate source sector share")
    cost = d["cost_quotes"]
    gross = sum(cost["components_trillion_USD"])
    net = gross - cost["EOR_benefit_trillion_USD"]
    add("gross_cost", gross, "trillion 2019 USD", "Rounded cumulative component sum")
    add("net_cost", net, "trillion 2019 USD", "Financial net, not net lifecycle emissions")
    add("gross_average", gross * 1000 / q["target_Gt"], "USD/t", "Gross investment/cumulative reported mass")
    add("net_average", net * 1000 / q["target_Gt"], "USD/t", "Rounded aggregates give 62.6087; 62.65 is compatible with display intervals")
    add("quoted_unit_cost_implied_total", cost["unit_USD_t"] * q["target_Gt"] / 1000, "trillionUSD", "Compare rounded 5.76 trillion without silently changing the quote")
    add("capture_share_of_gross", 100 * cost["components_trillion_USD"][0] / gross, "%", "Gross cost composition")
    add("capture_share_of_net", 100 * cost["components_trillion_USD"][0] / net, "%", "Explains >77% wording using net denominator")
    add("country_mean_cost_total", 85 * 67.81 / 1000, "trillionUSD", "Rounded arithmetic mean of national net costs")
    add("country_mean_benefit_total", 85 * 28.68 / 1000, "trillionUSD", "Rounded arithmetic mean of national benefits")
    add("implied_cumulative_GDP", net / (cost["GDP_cost_percent"] / 100), "trillionUSD", "Normalization only; not annual GDP or causal growth")
    add("groupII_count_by_remainder", 85 - 3 - 64 - 8, "regions", "Group count remainder, not new primary data")
    add("groupIV_mass_remainder", 100 - 3.7 - 79 - 10, "%", "Rounded group mass remainder, not source native allocation")
    for name, oil in [("base", 55), ("high", 95)]:
        rev = oil / d["printed_displacement_value"]
        benefit = rev * q["EOR_flow_Gt"] / 1000
        add(name + "_conditional_Eq6_revenue", rev, "USD/t", "ONLY if printed 4 means t/bbl; unit is not stated")
        add(name + "_conditional_fixed_flow_benefit", benefit, "trillionUSD", "Literal Eq6 and fixed 33.39 Gt; no native reoptimization or inferred correction")
    add("quoted_benefit_per_EOR_mass", cost["EOR_benefit_trillion_USD"] * 1000 / q["EOR_flow_Gt"], "USD/t", "Conditional global ratio; reconcile with Eq6/units/time/case")
    add("quoted_benefit_implied_displacement_at55", 55 * q["EOR_flow_Gt"] / (1000 * cost["EOR_benefit_trillion_USD"]), "t/bbl", "Diagnostic only; not an accepted corrected displacement")
    add("high_cost_unit_implied_total", 80.26 * 92 / 1000, "trillionUSD", "Compatible with the 7.38 trillion rounded reoptimized case")
    add("low_cost_unit_from_saving", 62.65 - 17.77, "USD/t", "Reported saving algebra")
    add("low_cost_implied_total", (62.65 - 17.77) * 92 / 1000, "trillionUSD", "Compatible with the 4.13 trillion rounded reoptimized case")
    add("high_oil_unit_implied_total", 40.26 * 92 / 1000, "trillionUSD", "Conditional same 92 Gt case; not native result array")
    add("inclusive_year_count", len(range(2020, 2051)), "calendar entries", "Eq15/17 sum; not automatically a duration error")
    for duration in [30, 31]:
        add("flat_average_" + str(duration), 92 / duration, "Gt/y", "Analyst cumulative/duration conversion, not source annual injection history")
    a = d["analyst_examples"]
    add("saline_synthetic_mass", a["area_m2"] * a["effective_area_ratio"] * a["thickness_m"] * a["porosity"] * 710 * .05 / 1000,
        "t", "Literal Eq2 with disclosed analyst geometry; not a site estimate or service rate")
    add("oil_synthetic_standard_volume_mass", a["OOIP_m3"] * 1.977 * .6 / 1000, "t", "Literal Eq1 ONLY under explicit volume convention; does not establish correct oil-to-storage conversion")
    add("reservoir_to_standard_density", 710 / 1.977, "ratio", "Different states; not a permission to replace Eq1 density")
    add("five_year_cost_multiplier_six_cycles", .75 ** 6, "dimensionless", "Conditional Eq29 cost recurrence; not deployment decline")
    add("avoided_cost_synthetic", avoided_unit_cost(50, 90, .8, .1), "USD/tavoided", "Eq23 per equal electricity output; captured mass requires separate inventory")
    add("captured_cost_synthetic", (90 - 50) / .8, "USD/tcaptured", "Disclosed analyst 0.8 t captured/MWh, different from 0.7 t avoided/MWh")
    add("mixed_cluster_true_capture_bound", 10 * (.7 * .9 + .3 * .6), "Mt", "Analyst 70/30 emissions and 90/60% capture; native mixed-source mapping unknown")
    add("mixed_cluster_all_power_bound", 10 * .9, "Mt", "Counterexample to treating a mixed cluster as all power")
    add("mixed_cluster_all_nonpower_bound", 10 * .6, "Mt", "Counterexample to treating a mixed cluster as all nonpower")
    learning = lcoe_learning_example(a["lcoe"])
    for key, value in learning.items():
        add("analyst_LCOE_" + key, value, "USD/MWh" if key.endswith("MWh") else "dimensionless", "Eq22/24 component with explicit analyst costs; not native technology optimization")
    deployment_rows = [dict(U=u, SD=2020, year=t, maximum=.8, fraction=deployment(t, 2020, u, .8),
                            scope="Analyst Eq28 segment only; native U/SD/maximum unknown")
                       for u in [1, 2, 3] for t in range(2020, 2051, 5)]
    lp_rows = [aggregate_lp(a["lp"], oil, exact_targets=exact) for oil in [0, 55, 95] for exact in [False, True]]
    return checks, deployment_rows, lp_rows


def main():
    data = load_inputs()
    checks, deployment_rows, lp_rows = calculate(data)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, rows in [("checks", checks), ("analyst_deployment", deployment_rows), ("analyst_LP", lp_rows),
                       ("source_country_emissions", data["figure1_country_rows"])]:
        with (OUT / ("B2-16_" + name + ".csv")).open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader(); writer.writerows(rows)
    summary = dict(study_id="B2-16", source_sha256=data["source_sha256"], limited_checks=len(checks),
                   source_country_rows=len(data["figure1_country_rows"]), analyst_deployment_rows=len(deployment_rows),
                   analyst_LP_rows=len(lp_rows), native_C3IAM_GCOP_global_model_reproduced=False,
                   accepted_Paper1_inputs_added=0, scope="Printed arithmetic and explicitly synthetic components only",
                   missing_native=data["missing_native"])
    (OUT / "B2-16_reproduction_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
