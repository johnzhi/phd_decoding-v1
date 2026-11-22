#!/usr/bin/env python3
"""B2-10 taxonomy, unit and disclosed economic/buffer diagnostics only.

No native MoMilp/CPLEX case, cost model, annual route/fleet schedule, geological
model or LCI is reproduced. No accepted operating or GHG inputs are changed.
"""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/comprehensive_review"


def load_inputs():
    data = json.loads((ROOT / "evidence/comprehensive_review_inputs/B2-10.json").read_text())
    for source in [data["source"], *data["cited_sources"]]:
        if hashlib.sha256((ROOT / source["path"]).read_bytes()).hexdigest() != source["sha256"]:
            raise ValueError(f"Changed source: {source['path']}")
    return data


def pv(values, rate):
    values = np.asarray(values, dtype=float)
    if (values.ndim != 1 or not len(values) or not np.all(np.isfinite(values))
            or not np.isfinite(rate) or rate <= -1):
        raise ValueError("Finite annual series and positive discount factors required")
    return float(values @ (1.0 + rate) ** -np.arange(1, len(values) + 1))


def choose_plan(costs, annual_mass, rate, enabled):
    """Analyst LP selecting a plan by undiscounted total cost, not the author model."""
    costs = np.asarray(costs, dtype=float)
    if (costs.ndim != 2 or costs.shape[1] != len(annual_mass)
            or len(enabled) != len(costs) or not any(enabled)
            or not np.all(np.isfinite(costs))):
        raise ValueError("Matching finite plan profiles and enabled choices required")
    denominator = pv(annual_mass, rate)
    if denominator <= 0:
        raise ValueError("Positive discounted service required")
    result = linprog(costs.sum(axis=1), A_eq=[np.ones(len(costs))], b_eq=[1],
                     bounds=[(0, 1 if value else 0) for value in enabled], method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    profile = result.x @ costs
    return dict(weights=result.x.tolist(), total=float(result.fun),
                pv_cost=pv(profile, rate), levelized=pv(profile, rate) / denominator)


def gap_shortfall(capacity, arrivals, demand):
    """Analyst inventory LP with a full initial tank and no required terminal stock."""
    arrivals = np.asarray(arrivals, dtype=float); demand = np.asarray(demand, dtype=float)
    n = len(demand)
    if (capacity < 0 or arrivals.shape != demand.shape or not n
            or not np.all(np.isfinite([capacity, *arrivals, *demand]))
            or np.any(arrivals < 0) or np.any(demand < 0)):
        raise ValueError("Nonnegative matching interval inputs required")
    matrix = np.zeros((n, 2 * n))
    for i in range(n):
        matrix[i, i] = 1
        if i:
            matrix[i, i - 1] = -1
        matrix[i, n + i] = -1
    rhs = arrivals - demand
    rhs[0] += capacity
    result = linprog([0] * n + [1] * n, A_eq=matrix, b_eq=rhs,
                     bounds=[(0, capacity)] * n + [(0, x) for x in demand], method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    return dict(unmet=float(result.fun), inventory=result.x[:n].tolist(),
                shortfall=result.x[n:].tolist())


def calculate(data):
    rows = []
    case = data["case"]
    def add(item, value, unit, basis, locator, interpretation):
        rows.append(dict(item=item, value=value, unit=unit, basis=basis,
                         source_locator=locator, interpretation=interpretation))

    ids = [i for group in data["groups"] for i in group["ids"]]
    bases = {group["base"] for group in data["groups"]}
    alternatives = set(ids) - bases
    for group in data["groups"]:
        add(group["name"] + "_labelled_designs", len(group["ids"]), "designs",
            "printed taxonomy", "pp4–8", "Baseline is included; labels are not probability-weighted outcomes")
    add("labelled_designs_total", len(ids), "designs", "printed taxonomy", "p6 Figure4", "Fifteen includes three baselines")
    add("baseline_designs", len(bases), "designs", "printed taxonomy", "pp3–6", "0,1,2")
    add("what_if_alternatives", len(alternatives), "designs", "printed taxonomy", "pp4–8", "Twelve nonbaseline labels, not fifteen alternatives plus three bases")
    add("missing_Table1_label", ",".join(sorted(set(ids) - set(data["table1_ids"]))), "identifier", "printed taxonomy", "pp4–5", "z occurs in Table2 and plots but is absent from Table1's standalone storage-delay cell")
    for kind in ["growth", "source_delay", "storage_delay", "interconnection"]:
        add(kind + "_alternatives", sum(item["driver"] == kind for item in data["scenarios"]), "designs",
            "printed taxonomy", "pp4–5", "Counts identified alternatives only")
    endpoints = data["emission_endpoints_kt"]
    first = sum(x["first"] for x in endpoints); last = sum(x["last"] for x in endpoints)
    add("combined_first_year", first, "ktCO2/year", "printed endpoint accounting", "p4", "Assumed handled-source profile, not actual net GHG or verified injected mass")
    add("combined_last_year", last, "ktCO2/year", "printed endpoint accounting", "p4", "No complete annual array reconstructed")
    add("reported_horizon_average", data["reported_total_Mt"] * 1000 / case["years"], "ktCO2/year", "printed total accounting", "p4", "333.8Mt does not uniquely define thirty annual values")
    add("monotone_endpoint_lower_total", (first * (case["years"] - 1) + last) / 1000, "Mt", "conditional analyst bound", "p4", "Assumes nondecreasing profile; not a reconstructed native schedule")
    add("monotone_endpoint_upper_total", (first + last * (case["years"] - 1)) / 1000, "Mt", "conditional analyst bound", "p4", "Wide bounds demonstrate insufficiency of endpoints")
    add("UK_baseline_endpoint_growth", 100 * (endpoints[0]["last"] / endpoints[0]["first"] - 1), "%",
        "printed endpoint accounting", "p4", "Baseline endpoint change is distinct from the alternative 2% annual-growth instruction")
    for intervals in [24, 29, 30]:
        add(f"conditional_2percent_growth_{intervals}_intervals", 100 * (1.02 ** intervals - 1), "%",
            "analyst calendar comparison", "pp4,7", "Different growth start/calendars change endpoint uplift; none selected as the missing native calendar")
    add("remaining_years_after_six_year_delay", case["years"] - case["delay_years"], "years",
        "calendar accounting", "pp4–5", "A truncated delay need not preserve total captured/handled mass")
    add("first_delayed_active_year_if_six_full_years_excluded", case["delay_years"] + 1, "year index",
        "explicit analyst convention", "pp4–5", "Native delay/index convention and graph mapping still needed")
    for capacity in case["ship_capacities_kt"]:
        add(f"ship_{capacity}kt_mass", capacity * 1000, "tCO2/cargo", "exact unit conversion", "p2", "Cargo capacity does not give annual ship throughput or availability")
    for location, sizes in case["pipe_inches"].items():
        for size in sizes:
            add(f"{location}_pipe_{size}inch", size * .0254, "m", "exact unit conversion", "p2", "No thickness, roughness, pressure or hydraulic capacity inferred")
    for metric, contexts in data["appendix_extremes"].items():
        low = min(x[0] for x in contexts.values()); high = max(x[1] for x in contexts.values())
        add(metric + "_minimum_across_contexts", low, data["extreme_units"][metric], "printed appendix extrema", "pp7–8", "Changing units/denominators preserved; no frequency or likelihood inferred")
        add(metric + "_maximum_across_contexts", high, data["extreme_units"][metric], "printed appendix extrema", "pp7–8", "Matches reported outer range where stated; not independent optimizer validation")
    for group in data["cost_ranges"]:
        for metric, endpoints in group["ranges"].items():
            lo, hi = endpoints
            add(f"{group['driver']}_{metric}_printed_endpoint_order", int(lo <= hi), "boolean",
                "literal table audit", "p5 Table2", f"Preserve printed endpoints {lo},{hi}; do not sort or insert a missing sign")
    base = choose_plan([[100, 0], [0, 101]], [1, 1], .1, [False, True])
    optional = choose_plan([[100, 0], [0, 101]], [1, 1], .1, [True, True])
    for name, result in [("restricted", base), ("optional", optional)]:
        for metric in ["total", "pv_cost", "levelized"]:
            add("analyst_" + name + "_" + metric, result[metric], "analyst currency/service units",
                "disclosed two-plan LP", "pp3,5–6", "Optional choices lower the minimized undiscounted objective but may raise a different discounted metric; no native discount convention asserted")
    for hours, capacity in [(10, 20), (12, 20), (12, 24)]:
        result = gap_shortfall(capacity, [0] * hours, [2] * hours)
        add(f"analyst_gap_{hours}h_capacity_{capacity}_unmet", result["unmet"], "analyst mass units",
            "disclosed inventory LP", "p3 buffer rule", "Full initial cargo, no arrivals during interval; weather probability and native storage policy not estimated")
    return rows


def main():
    data = load_inputs(); rows = calculate(data)
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "B2-10_checks.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0], lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    with (OUT / "B2-10_scenario_register.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data["scenarios"][0], lineterminator="\n")
        writer.writeheader(); writer.writerows(data["scenarios"])
    report = dict(study_id="B2-10",checks=len(rows),baseline_designs=3,what_if_alternatives=12,
                  labelled_designs=15,author_model="not_reproduced",accepted_inputs_changed=False,
                  excluded_missing_inputs=data["missing_inputs"])
    (OUT / "B2-10_reconciliation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
