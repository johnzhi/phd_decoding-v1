#!/usr/bin/env python3
"""B2-09 printed accounting and disclosed analyst CVaR diagnostics.

No native network optimizer, pressure model, scenario calibration or LCA is
reproduced. Outputs stay outside accepted operating and GHG inputs.
"""
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


def load_inputs():
    data = json.loads((ROOT / "evidence/comprehensive_review_inputs/B2-09.json").read_text())
    for source in [data["source"], *data["cited_sources"]]:
        if hashlib.sha256((ROOT / source["path"]).read_bytes()).hexdigest() != source["sha256"]:
            raise ValueError(f"Changed source: {source['path']}")
    return data


def discrete_cvar(losses, probabilities, alpha):
    """Exact upper-tail integral, including partial mass at a discrete atom."""
    losses = np.asarray(losses, dtype=float)
    probabilities = np.asarray(probabilities, dtype=float)
    if (losses.ndim != 1 or not len(losses) or probabilities.shape != losses.shape
            or not np.all(np.isfinite(losses)) or not np.all(np.isfinite(probabilities))
            or np.any(probabilities < 0) or not math.isclose(float(probabilities.sum()), 1)
            or not 0 <= alpha < 1):
        raise ValueError("Finite losses, normalized nonnegative probabilities and 0<=alpha<1 required")
    remaining = 1 - alpha
    total = 0.
    for index in np.argsort(-losses):
        mass = min(remaining, probabilities[index])
        total += mass * losses[index]
        remaining -= mass
        if remaining <= 0:
            break
    return float(total / (1 - alpha))


def cvar_lp(losses, probabilities, alpha):
    """Independent implementation of printed Equations 15–16 as a linear program."""
    discrete_cvar(losses, probabilities, alpha)  # validate before constructing LP
    losses = np.asarray(losses, dtype=float)
    n = len(losses)
    result = linprog(
        [1, *(np.asarray(probabilities) / (1 - alpha))],
        A_ub=np.column_stack((-np.ones(n), -np.eye(n))),
        b_ub=-losses, bounds=[(None, None), *[(0, None)] * n], method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    return float(result.fun)


def discounted_sum(values, rate):
    if rate <= -1 or not values:
        raise ValueError("Positive discount factors and nonempty horizon required")
    return math.fsum(value / (1 + rate) ** t for t, value in enumerate(values, 1))


def percent_interval(base, final, half_width):
    if min(base, final) <= half_width or half_width < 0:
        raise ValueError("Positive denominator interval required")
    return (100 * ((final - half_width) / (base + half_width) - 1),
            100 * ((final + half_width) / (base - half_width) - 1))


def calculate(data):
    rows = []
    case = data["case"]
    sources = data["sources"]
    sinks = data["sinks"]
    distance = {(x["origin"], x["destination"]): x["km"] for x in data["arcs"]}
    flows = data["reported_baseline"]["flows"]

    def add(item, value, unit, basis, locator, interpretation):
        rows.append(dict(item=item, value=value, unit=unit, basis=basis,
                         source_locator=locator, interpretation=interpretation))

    gross = math.fsum(s["emissions_Mt_year"] for s in sources)
    target = case["target_fraction_capturable"] * case["capture_fraction"] * gross
    add("gross_annual_emissions", gross, "Mt/year", "printed accounting", "p8 Table2", "Synthetic potential supply, not observed emissions")
    add("annual_target", target, "Mt/year", "printed accounting", "pp8–9", "90% of 90% capturable supply; not 90% of gross emissions")
    add("gross_target_percent", 100 * target / gross, "%", "printed accounting", "pp8–9", "81% before the separate availability convention")
    available = case["hours_year"] / 8760
    add("source_availability", available, "fraction", "calendar interpretation", "pp6,9", "8000h is stated in case data, but an explicit equation fixing/bounding y to it is absent")
    add("annual_available_capture", gross * case["capture_fraction"] * available, "Mt/year", "conditional calendar accounting", "pp6,8–9", "Uses all source Qi as full-year potential; native time convention unverified")
    add("twenty_year_target", target * case["years"], "Mt", "printed accounting", "pp8–10", "A policy target, not a calibrated geological resource")
    add("twenty_year_gross", gross * case["years"], "Mt", "printed accounting", "p8 Table2; p10 Figure5", "Blue source labels are gross emissions, not captured arc flows")
    for s in sources:
        name = s["id"]
        add(f"{name}_salvage_percent", 100 * s["salvage_MUSD"] / s["capital_MUSD"], "%", "printed accounting", "p8 Table2", "5% source capital identity only")
        actual = math.fsum(x["cumulative_Mt"] for x in flows if x["origin"] == name)
        add(f"{name}_reported_capture", actual, "Mt", "rounded flow replay", "p10 Figure5", "Sum of labelled outgoing arcs; cumulative check only")
        add(f"{name}_available_capture_ceiling", s["emissions_Mt_year"] * case["capture_fraction"] * available * case["years"], "Mt", "conditional calendar accounting", "pp6,8–10", "Not a reconstructed annual operating profile")
    flow_total = math.fsum(x["cumulative_Mt"] for x in flows)
    sink_total = math.fsum(data["reported_baseline"]["sink_Mt"].values())
    add("reported_arc_total", flow_total, "Mt", "rounded flow replay", "p10 Figure5", "S5 ribbon is 78.9 Mt, confirmed by magnification")
    add("reported_sink_total", sink_total, "Mt", "rounded flow replay", "p10 Figure5", "491.43 plus 331.03 Mt")
    add("reported_node_flow_residual", flow_total - sink_total, "Mt", "rounded flow replay", "p10 Figure5", "Zero at displayed precision; no native model certification")
    add("stored_share_gross", 100 * sink_total / (gross * case["years"]), "%", "rounded flow replay", "pp8,10", "Stored/injected scenario quantity, not lifecycle avoidance or permanence")
    add("baseline_pipe_units", sum(x["pipes"] for x in flows), "parallel pipe units", "rounded flow replay", "p10 Figure5", "Six selected arcs carry nine units")
    add("baseline_pipe_km", math.fsum(x["pipes"] * distance[x["origin"], x["destination"]] for x in flows), "pipe-km", "rounded flow replay", "p9 Figure4; p10 Figure5", "911.44 agrees with approximately 911; not route-km or a solved optimum")
    differences = []
    for origin in ["H1", "S1", "S2", "S3", "S4", "S5"]:
        difference = distance[origin, "R1"] - distance[origin, "R2"]
        differences.append(difference)
        add(f"{origin}_R1_minus_R2_distance", difference, "km", "printed distance comparison", "p9 Figure4; p10",
            "R1 is farther in every displayed pair; the prose transport-distance advantage needs qualification, not a reversal of the reported allocation")
    add("all_R1_pairwise_distances_longer", int(all(x > 0 for x in differences)), "boolean", "printed distance comparison", "p9 Figure4; p10",
        "This does not prove an optimum is wrong: injectivity, costs and network interactions also matter")
    for sink in sinks:
        name = sink["id"]
        injection = math.fsum(x["cumulative_Mt"] for x in flows if x["destination"] == name)
        add(f"{name}_flow_residual", injection - data["reported_baseline"]["sink_Mt"][name], "Mt", "rounded flow replay", "p10 Figure5", "Displayed arc sum matches displayed sink total")
        wells = data["reported_baseline"]["wells"][name]
        add(f"{name}_twenty_year_nominal_well_capacity", wells * sink["injectivity_Mt_year_well"] * case["years"], "Mt", "constant-rate capacity accounting", "p9 Table3; p10 Figure5", "Upper bound from assumed per-well rate, not pressure-derived deliverability")
        add(f"{name}_fixed_opex_residual", sink["fixed_MUSD_year_well"] - .025 * sink["capital_MUSD_well"], "MUSD/year/well", "printed accounting", "p9 Table3", "R2 residual is consistent with six-decimal display rounding")
    add("pipe_fixed_opex_residual", data["pipeline"]["fixed_MUSD_km_year"] - .025 * data["pipeline"]["capital_MUSD_km"], "MUSD/km/year", "printed accounting", "p9", "Residual consistent with stated rounded annual coefficient")
    add("transport_analyst_length_omitted", .0475 * 1, "numeric dollars with unresolved missing km", "analyst unit example", "p6 Equation1; p9", "One tonne and a 100km arc: literal term lacks length if coefficient is per tonne-km")
    add("transport_analyst_length_included", .0475 * 1 * 100, "USD", "analyst dimensional comparison", "p6 Equation1; p9", "4.75USD requires an explicit length factor or a preaggregated coefficient; native code unverified")
    coal = next(s for s in sources if s["id"] == "S3")
    for hours in [8000, 8760]:
        estimate = 2000 * 1000 * hours * 2.31 * .45359237 / 1e9
        lo = estimate * 2.305 / 2.31
        hi = estimate * 2.315 / 2.31
        overlap = max(lo, coal["emissions_Mt_year"] - .0005) <= min(hi, coal["emissions_Mt_year"] + .0005)
        add(f"coal_emission_{hours}h", estimate, "Mt/year", "exact-unit conditional conversion", "p8 Tables1–2", "Uses international pound; annual potential versus operating-hour convention remains explicit")
        add(f"coal_rounding_compatible_{hours}h", int(overlap), "boolean", "conditional display-rounding check", "p8 Tables1–2", "2.31lb/kWh ±0.005 and 18.396Mt/year ±0.0005; no unrounded source factor is invented")
    prob = [.2] * 5
    fixture = [0, 1, 2, 3, 4]
    for alpha in [0, .5, .8, .95]:
        add(f"analyst_CVaR_{alpha}", discrete_cvar(fixture, prob, alpha), "analyst loss units", "disclosed analyst fixture", "p7 Equations15–16", "Independent tail integral; not native scenario losses")
        add(f"analyst_CVaR_LP_{alpha}", cvar_lp(fixture, prob, alpha), "analyst loss units", "independent analyst LP", "p7 Equations15–16", "Matches independent linear-program evaluation")
    add("minimum_scenario_probability", min(prob), "fraction", "printed scenario arithmetic", "p12", "20% per atom exceeds the selected 5% tail; CVaR95 equals maximum annual scenario loss")
    annual = [[10, 0], [0, 10]]
    separate = sum(discrete_cvar(loss, [.5, .5], .95) for loss in annual)
    horizon = discrete_cvar([sum(x) for x in zip(*annual)], [.5, .5], .95)
    add("crossing_annual_CVaR_sum", separate, "analyst loss units", "analyst two-year counterexample", "p7 Equation17", "Undiscounted fixture; separately assessed yearly tails need not be the same scenario")
    add("crossing_horizon_CVaR", horizon, "analyst loss units", "analyst two-year counterexample", "p7 Equation17", "10 versus 20 demonstrates distinction, not a numerical error in the unavailable native case")
    add("discount_factor_sum_20y", discounted_sum([1] * 20, .1), "PV years", "printed discount component", "pp6,9", "Discounted mass is not ordinary cumulative mass")
    add("discounted_85_credit_first12y", discounted_sum([85] * 12 + [0] * 8, .1), "USD per constant annual tonne", "stated time-profile component", "pp6,9", "Requires time-dependent revenue despite unindexed Rrev in Equation1")
    add("discounted_85_credit_all20y", discounted_sum([85] * 20, .1), "USD per constant annual tonne", "literal constant-revenue comparison", "pp6,9", "Not a corrected or reproduced author objective")
    add("high_lambda_mean_shortfall_share", 100 * 15 / target, "% of annual target", "approximate reported comparison", "pp12–13 Figure11", "Approximately 36.6%; not a probability or a measured failure frequency")
    for label, base, final, reported in data["reported_cost_comparisons"]:
        lo, hi = percent_interval(base, final, .05)
        add(f"{label}_central_percent", 100 * (final / base - 1), "%", "rounded endpoint comparison", "pp10,14,17", "Rounded endpoints do not give exact native objective values")
        add(f"{label}_reported_percent_rounding_compatible", int(lo <= reported <= hi), "boolean", "conditional rounding interval", "pp10,14,17", f"Reported {reported}% lies in [{lo:.6f},{hi:.6f}] if each endpoint is rounded to 0.1 billion USD")
    grid = []
    for gamma in np.linspace(0, 1, 11):
        factor = 1 - .4 * float(gamma)
        grid.append(dict(gamma=float(gamma),capacity_fraction=factor,
                         pipe_Mt_year=5 * factor,
                         R1_Mt_year_well=.3798 * factor,
                         R2_Mt_year_well=.3183 * factor,
                         minimum_wells_best_sink=math.ceil(target / (.3798 * factor)),
                         interpretation="Independent coefficient derates in every row; not a shared component-count budget or solved network"))
    return rows, grid


def main():
    rows, grid = calculate(load_inputs())
    OUT.mkdir(parents=True, exist_ok=True)
    for name, values in [("B2-09_checks.csv", rows), ("B2-09_capacity_grid.csv", grid)]:
        with (OUT / name).open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=values[0])
            writer.writeheader(); writer.writerows(values)
    report = dict(study_id="B2-09", checks=len(rows), capacity_grid_rows=len(grid),
                  author_model="not_reproduced", accepted_inputs_changed=False,
                  scope="Printed accounting and disclosed CVaR/unit fixtures only",
                  excluded_missing_inputs=load_inputs()["missing_inputs"])
    (OUT / "B2-09_reconciliation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
