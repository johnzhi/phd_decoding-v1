#!/usr/bin/env python3
"""Scoped B2-13 components and graphic checks; no native LCA reproduction."""
from __future__ import annotations

import bisect
import csv
import hashlib
import json
import math
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "evidence/comprehensive_review_inputs/B2-13.json"
OUT = ROOT / "outputs/comprehensive_review"


def finite_values(values, *, positive=False):
    if not values or any(not math.isfinite(x) or (x <= 0 if positive else x < 0) for x in values):
        raise ValueError("Finite nonnegative values required (strictly positive where specified)")


def tank_balance(tare, fill, remaining_fraction):
    finite_values([tare, fill], positive=True)
    if not math.isfinite(remaining_fraction) or not 0 <= remaining_fraction < 1:
        raise ValueError("Remaining fraction must lie in [0,1)")
    heel = fill * remaining_fraction
    return dict(full_t=tare + fill, heel_t=heel, returned_t=tare + heel,
                delivered_t=fill - heel, circulated_CO2_per_delivered_t=fill / (fill - heel))


def first_payback(old_annual_rates, new_annual_rates, construction):
    """First crossing of Eq1 under annual constant rates, including fractional year.

    Rates are impact/year, capital is impact; both paths must provide identical
    service. None means no crossing within the supplied horizon, not never.
    A later reversal is possible; first crossing does not assert permanent benefit.
    """
    if len(old_annual_rates) != len(new_annual_rates):
        raise ValueError("Matched horizons required")
    finite_values(old_annual_rates)
    finite_values(new_annual_rates)
    finite_values([construction])
    cumulative = 0.0
    crossing = 0.0 if construction == 0 else None
    rows = []
    for year, (old, new) in enumerate(zip(old_annual_rates, new_annual_rates)):
        saving = old - new
        if crossing is None and saving > 0 and cumulative + saving >= construction:
            crossing = year + (construction - cumulative) / saving
        cumulative += saving
        rows.append(dict(elapsed_year_end=year + 1, old_rate=old, new_rate=new,
                         cumulative_operating_saving=cumulative,
                         net_saving_after_construction=cumulative - construction))
    return crossing, rows


def annual_interpolation(knot_years, rates, start_year, horizon_years):
    """Linear interpolation at each integer year start, then annual hold."""
    if len(knot_years) != len(rates) or len(knot_years) < 2:
        raise ValueError("At least two matched knots required")
    finite_values(knot_years)
    finite_values(rates)
    if any(b <= a for a, b in zip(knot_years, knot_years[1:])):
        raise ValueError("Strictly increasing years required")
    if not isinstance(horizon_years, int) or horizon_years < 1:
        raise ValueError("Positive integer horizon required")
    if not math.isfinite(start_year) or start_year != int(start_year):
        raise ValueError("Integer start year required")
    if start_year < knot_years[0] or start_year + horizon_years - 1 > knot_years[-1]:
        raise ValueError("Extrapolation is not permitted")
    result = []
    for year in range(int(start_year), int(start_year) + horizon_years):
        k = min(bisect.bisect_right(knot_years, year) - 1, len(knot_years) - 2)
        fraction = (year - knot_years[k]) / (knot_years[k + 1] - knot_years[k])
        result.append(rates[k] + fraction * (rates[k + 1] - rates[k]))
    return result


def sector_allocation(demand_Gtkm, baseline_Gtkm, GVA_percent):
    finite_values([demand_Gtkm, baseline_Gtkm, GVA_percent], positive=True)
    return demand_Gtkm / baseline_Gtkm * GVA_percent


def native_rank_lines(pdf):
    """Corroborate manually inspected ordinal lines using native vector geometry.

    Frames/colors are manually identified from Figure5 and its rank labels.
    This checks discrete ordinal transcriptions, never bubble impact magnitudes.
    """
    colors = {
        "onshore": {
            (0.329, 0.510, 0.208): "dense10", (0.663, 0.820, 0.557): "dense03",
            (0., 0., 0.): "supercritical", (0.349, 0.349, 0.349): "gas10",
            (0.647, 0.647, 0.647): "gas03", (1., 0.753, 0.): "electric_train",
            (0.929, 0.490, 0.192): "electric_truck", (0.518, 0.235, 0.047): "hydrogen_truck",
            (0.149, 0.267, 0.471): "diesel_barge", (0.357, 0.608, 0.835): "diesel_truck",
        },
        "offshore": {
            (0.329, 0.510, 0.208): "dense10", (0.663, 0.820, 0.557): "dense03",
            (0., 0.690, 0.941): "ammonia_ship", (0.267, 0.447, 0.769): "methanol_ship",
            (0.349, 0.349, 0.349): "gas10", (0.647, 0.647, 0.647): "gas03",
            (0.600, 0.400, 1.): "hfo_ship",
        },
    }
    frames = {"onshore": (228.52, 419.80, 82.29, (214.03 - 82.29) / 9),
              "offshore": (228.88, 420.23, 254.10, (364.41 - 254.10) / 6)}
    result = {area: {} for area in frames}
    with fitz.open(pdf) as doc:
        drawings = doc[8].get_drawings()
    for area, (x0, x1, y1, spacing) in frames.items():
        for path in drawings:
            color = path.get("color")
            if color is None:
                continue
            mode = colors[area].get(tuple(round(v, 3) for v in color))
            rect = path["rect"]
            if mode is None or abs(rect.x0 - x0) > .1 or abs(rect.x1 - x1) > .1:
                continue
            if not (y1 - .1 <= rect.y0 <= rect.y1 <= y1 + (len(colors[area]) - 1) * spacing + .1):
                continue
            lines = [item for item in path["items"] if item[0] == "l"]
            if not lines:
                continue
            ranks = []
            for i in range(16):
                x = rect.x0 + i * rect.width / 15
                ys = [a.y + (b.y - a.y) * (x - a.x) / (b.x - a.x)
                      for _, a, b in lines if abs(b.x - a.x) > 1
                      and min(a.x, b.x) - .06 <= x <= max(a.x, b.x) + .06]
                if not ys:
                    raise ValueError("Missing vector intersection")
                geometric_rank = 1 + (sum(ys) / len(ys) - y1) / spacing
                if abs(geometric_rank - round(geometric_rank)) > .01:
                    raise ValueError("Rank geometry exceeds stated tolerance")
                ranks.append(round(geometric_rank))
            if mode in result[area]:
                raise ValueError("Ambiguous rank path")
            result[area][mode] = ranks
        if set(result[area]) != set(colors[area].values()):
            raise ValueError("Missing ordinal path")
    return result


def load_inputs():
    data = json.loads(INPUT.read_text())
    if hashlib.sha256((ROOT / data["source_path"]).read_bytes()).hexdigest() != data["source_sha256"]:
        raise ValueError("Stale source")
    return data


def calculate(data):
    checks = []

    def add(item, value, unit, basis):
        checks.append(dict(item=item, value=value, unit=unit, basis=basis))

    c = data["containers"]
    tank = tank_balance(c["tare_t"], c["capacity_CO2_t"], c["remaining_fraction"])
    for key, value in tank.items():
        add("conditional_ISO_" + key, value, "ratio" if "per_delivered" in key else "t",
            "Conditional fill/heel mass balance; not native freight denominator or atmospheric loss")
    add("remaining_44t_allowance", c["gross_truck_t_approx"] - tank["full_t"], "t",
        "Approximate gross less full container, not actual tractor/trailer/battery weights or legal validation")
    allocation = data["planetary_allocation"]
    demand = allocation["annual_CO2_Gt"] * allocation["average_distance_km"]
    add("annual_transport_demand", demand, "Gtkm/y", "Reported scenario product, not field capacity")
    budgets = [sector_allocation(demand, allocation["EU27_road_freight_Gtkm"], v)
               for v in allocation["road_GVA_percent_range"]]
    for label, budget in zip(["low", "high"], budgets):
        add("GVA_sector_allocation_" + label, budget, "% of Europe safe operating space",
            "Conditional linear GVA allocation; EU27 freight and population/EUR boundaries need alignment")
        add("pipeline_quoted_upper_over_" + label + "_allocation", .075 / budget, "ratio",
            "Quoted upper bound divided by conditional budget; not proof actual case exceeds budget")
    for label, share in zip(["low", "high"], allocation["batch_onshore_highest_percent_range"]):
        add("batch_" + label + "_over_high_allocation", share / budgets[1], "ratio",
            "Reported impact endpoint versus optimistic sector budget, T only; not complete-chain burden")
    add("Europe_to_global_upper_share", .075 * allocation["European_population_fraction"], "% global",
        "Allocation arithmetic only; not a new planetary boundary")
    f2 = data["figures"]["F2"]
    specific = f2["specific_2020_pipeline_gCO2e_tkm_quote"]
    add("selected_4g_intensity_at_100km", specific * 100 / 1000, "kgCO2e/t transported",
        "Transport-only unit conversion of selected quoted intensity, not all pipelines or whole-chain avoidance")
    add("selected_4g_at_70Gtkm", specific * demand / 1000, "MtCO2e/y",
        "Conditional intensity times demand, not reproduced European network LCA")
    add("annual_snapshot_time_points", len(data["background"]["years"]), "count",
        "Source time grid, not annual inventory arrays")

    switches = data["figures"]["F4"]["switches"]
    for area, modes in [("onshore", 10), ("offshore", 7)]:
        rows = [r for r in switches if r["area"] == area]
        add(area + "_displayed_switches", len(rows), "count", "All Figure4 upper-triangle cells")
        add(area + "_finite_displayed_switches", sum(r["finite"] for r in rows), "count",
            "Source classifications, not recomputed paybacks")
        add(area + "_all_directed_pairs", modes * (modes - 1), "count",
            "Combinatorial comparison; missing reverse directions were not assessed in figure")
    add("finite_displayed_switches", sum(r["finite"] for r in switches), "count", "Includes parenthesized beyond-lifetime16")
    add("source_X_switches", sum(not r["finite"] for r in switches), "count", "Native X, no inferred infinite-horizon model")
    add("beyond_lifetime_switches", sum(r["beyond_lifetime"] for r in switches), "count", "H2 truck to electric truck, printed(16)")
    add("source_zero_labels", sum(r["quoted"] == 0 for r in switches), "count", "Rounded/displayed zero is not an instantaneous payoff")
    f3 = data["figures"]["F3"]
    add("F3_2040_train_dense03", f3["quoted_payback_years"][3], "y", "Native Figure3 quote, Figure4 rounds to7")
    add("F3_2040_excess_over_3y", f3["quoted_payback_years"][3] - 3, "y", "Counterexample to an unqualified under3 claim")
    add("F3_negative_adjacent_changes", sum(b < a for a, b in zip(f3["quoted_payback_years"], f3["quoted_payback_years"][1:])),
        "count", "Source sequence is not monotonically increasing")

    ranks = data["figures"]["F5"]
    geometry = native_rank_lines(ROOT / data["source_path"])
    rank_rows = []
    for area in ["onshore", "offshore"]:
        native = ranks[area + "_ranks"]
        if geometry[area] != native:
            raise ValueError("Manual ranks differ from native vector paths")
        for i, category in enumerate(ranks["category_order"]):
            if sorted(v[i] for v in native.values()) != list(range(1, len(native) + 1)):
                raise ValueError("Invalid per-category rank ordering")
            for mode, values in native.items():
                rank_rows.append(dict(area=area, category=category, mode=mode, rank=values[i],
                                      source_page=9, scenario="SSP2-NDC", year=2070, system_boundary="T",
                                      absolute_impact="", provenance="Manual tracing corroborated by native vector paths; ordinal only"))
        add(area + "_dense10_first_categories", sum(r == 1 for r in native["dense10"]), "count",
            "Native Figure5 discrete rank, not cardinal environmental benefit")
    on = ranks["onshore_ranks"]
    for alternative in ["hydrogen_truck", "diesel_truck"]:
        add("electric_truck_worse_than_" + alternative,
            sum(a > b for a, b in zip(on["electric_truck"], on[alternative])), "categories",
            "Source ordinal comparison corroborates11/16 and4/16, respectively")
    off = ranks["offshore_ranks"]
    for alternative in ["ammonia_ship", "methanol_ship"]:
        add("HFO_better_than_" + alternative + "_nonclimate",
            sum(a < b for a, b in zip(off["hfo_ship"][1:], off[alternative][1:])), "categories",
            "Pairwise ordinal comparison, no weighting or aggregate sustainability score")

    examples = data["analyst_examples"]
    constant = examples["constant"]
    payback, _ = first_payback([constant["old_rate_g_y"]] * 40,
                              [constant["new_rate_g_y"]] * 40, constant["construction_g"])
    add("analyst_constant_payback", payback, "y", "Synthetic Eq1 example; no author inputs")
    declining = examples["declining"]
    old = annual_interpolation(declining["knot_years"], declining["old_rate_g_y"],
                               declining["start_year"], declining["horizon_years"])
    new = annual_interpolation(declining["knot_years"], declining["new_rate_g_y"],
                               declining["start_year"], declining["horizon_years"])
    payback, annual = first_payback(old, new, declining["construction_g"])
    add("analyst_declining_payback", payback, "y", "Synthetic interpolated annual rates, source discretization, no author LCA")
    for row in annual:
        row.update(calendar_year=declining["start_year"] + row["elapsed_year_end"] - 1,
                   unit="gCO2e and gCO2e/y", status="analyst_example_not_author_case")
    return checks, switches, rank_rows, annual


def write_csv(name, rows):
    with (OUT / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    data = load_inputs()
    checks, switches, ranks, annual = calculate(data)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, rows in [("checks", checks), ("source_switches", switches),
                       ("source_ranks", ranks), ("analyst_payback", annual)]:
        write_csv("B2-13_" + name + ".csv", rows)
    summary = dict(study_id="B2-13", source_sha256=data["source_sha256"],
                   limited_checks=len(checks), source_switch_cells=len(switches),
                   source_ordinal_ranks=len(ranks), analyst_annual_rows=len(annual),
                   native_LCA_model_reproduced=False, native_payback_cases_reproduced=False,
                   native_absolute_impacts_reconstructed=False, accepted_Paper1_inputs_added=0,
                   scope="Printed arithmetic, ordinal transcription and Eq1 component with synthetic inputs only",
                   missing_native=data["missing_native"])
    (OUT / "B2-13_reproduction_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
