#!/usr/bin/env python3
"""B2-11 printed utility/cost components and conditional pure-fluid checks.

No native Ebsilon/Aspen/spreadsheet or110-plant result is reproduced. EOS
pressure/composition assumptions and truck calendar/volume are analyst inputs.
Missing cooling, MEA, density and LCI values remain missing; no accepted input
or operating/GHG output is changed.
"""
from __future__ import annotations
import csv
import hashlib
import json
import math
from pathlib import Path

import CoolProp
from CoolProp.CoolProp import PhaseSI, PropsSI

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs/comprehensive_review"


def load_inputs():
    data = json.loads((ROOT / "evidence/comprehensive_review_inputs/B2-11.json").read_text())
    for source in [data["source"], *data["cited_sources"]]:
        if hashlib.sha256((ROOT / source["path"]).read_bytes()).hexdigest() != source["sha256"]:
            raise ValueError(f"Changed source: {source['path']}")
    return data


def crf(rate, years):
    if not math.isfinite(rate) or rate < 0 or not isinstance(years, int) or years <= 0:
        raise ValueError("Nonnegative finite rate and positive integer years required")
    return 1 / years if rate == 0 else rate / (1 - (1 + rate) ** -years)


def capture_capex_EUR(flow_t_h, parameters):
    if not math.isfinite(flow_t_h) or flow_t_h <= 0:
        raise ValueError("Positive finite captured flow in tonnes/hour required")
    return 1000 * parameters["coefficient_kEUR"] * (flow_t_h / 3.6) ** parameters["exponent"]


def truck_component(distance_km, daily_volume_m3, capacity_factor, truck, analyst):
    """Printed continuous Eq3–6, plus a separately labelled integer fleet bound.

    Calendar365days/year and1000m3/day demonstration volume are analyst choices;
    no truck density, payload, travel queue or staff-season policy is inferred.
    """
    if (not all(math.isfinite(x) for x in [distance_km, daily_volume_m3, capacity_factor])
            or distance_km < 0 or daily_volume_m3 <= 0 or not 0 < capacity_factor <= 1):
        raise ValueError("Nonnegative distance, positive volume and capacity factor in(0,1] required")
    trip_h = 2 * distance_km / truck["speed_kmh"] + truck["loading_h"]
    volume_per_truck_day = truck["shift_h"] / trip_h * truck["shifts_per_day"] * truck["capacity_m3"]
    fleet = daily_volume_m3 / volume_per_truck_day
    trips = daily_volume_m3 / truck["capacity_m3"]
    annual_volume = daily_volume_m3 * analyst["days_per_year"] * capacity_factor
    fixed_per_truck = truck["capex_EUR"] * (crf(truck["discount_rate"], truck["lifetime_years"]) + truck["maintenance_fraction"])
    # Wage and fuel multiply CF as stated in the paper. This is an economic
    # component, not proof that fractional wages/fleets are operable.
    annual_fuel = trips * 2 * distance_km * truck["fuel_EUR_per_km"] * analyst["days_per_year"] * capacity_factor
    wage_per_truck = truck["drivers_per_truck"] * truck["wage_EUR_per_driver_year"] * capacity_factor
    annual_continuous = fleet * (fixed_per_truck + wage_per_truck) + annual_fuel
    integer_fleet = math.ceil(fleet)
    annual_integer = integer_fleet * (fixed_per_truck + wage_per_truck) + annual_fuel
    return dict(distance_km=distance_km, capacity_factor=capacity_factor,
                analyst_daily_volume_m3=daily_volume_m3, trip_h=trip_h,
                volume_per_truck_day_m3=volume_per_truck_day,
                continuous_fleet=fleet, ceil_fleet=integer_fleet,
                continuous_trips_per_day=trips, annual_volume_m3=annual_volume,
                continuous_cost_EUR_m3=annual_continuous / annual_volume,
                ceil_fleet_cost_EUR_m3=annual_integer / annual_volume,
                cost_EUR_t="", density_t_m3="",
                basis="Printed continuous component; analyst365-day calendar/volume. Ceil alternative only; no full integer dispatch, tonne cost or native case.")


def calculate(data):
    rows = []
    def add(item, value, unit, basis, locator, interpretation):
        rows.append(dict(item=item, value=value, unit=unit, basis=basis,
                         source_locator=locator, interpretation=interpretation))
    u = data["utilities"]; c = data["case"]; cap = data["capture_capex"]
    heat = u["reboiler_MJ_per_kg"] / 3.6
    add("reboiler_heat", heat, "MWh/tcaptured", "exact unit conversion", "p3", "Positive process heat; recovered DH is not a negative reboiler input")
    add("base_bundled_electricity", u["base_electricity_MWh_per_t"] * 1000, "kWh/tcaptured", "exact unit conversion", "pp4,7", "Capture+compression+liquefaction; do not append duplicate conditioning work")
    add("HP_case_direct_electricity", u["base_electricity_MWh_per_t"] + u["HP_extra_MWh_per_t"], "MWh/tcaptured", "source component sum", "p4", "Lost turbine generation remains a separate opportunity cost")
    add("base_direct_electricity_cost", u["base_electricity_MWh_per_t"] * data["prices"]["electricity_EUR_per_MWh"], "EUR/tcaptured", "printed component arithmetic", "pp4,7", "4EUR/t is not total lost-electricity cost or total OPEX")
    add("HP_direct_electricity_cost", (u["base_electricity_MWh_per_t"] + u["HP_extra_MWh_per_t"]) * data["prices"]["electricity_EUR_per_MWh"], "EUR/tcaptured", "printed component arithmetic", "pp4,7", "10.8EUR/t direct electricity only")
    add("conditional_HP_heat", u["COP"] * u["HP_extra_MWh_per_t"], "MWh/tcaptured", "common-basis assumption", "p4", "COP heat includes HP work; not a substitute for the native stream enthalpy ledger")
    recovered = .64 * heat + u["COP"] * u["HP_extra_MWh_per_t"]
    add("conditional_recovery_fraction", recovered / heat, "fraction", "exact shared reboiler-basis diagnostic", "p4", "1.15 only if every quantity uses the same exact1MWh/t basis; not a demonstrated error in118%")
    add("conditional_118_recovery_residual", 1.18 * heat - recovered, "MWh/tcaptured", "exact shared reboiler-basis diagnostic", "p4", "0.03 residual; extracted-steam energy, rounding and per-plant cases unresolved")
    add("conditional_HP_work_for_118", (1.18 - .64) * heat / u["COP"], "MWh/tcaptured", "exact shared reboiler-basis diagnostic", "p4", "0.18 is conditional comparison, never a corrected native0.17")
    add("new_FGC_count", c["plants"] - c["existing_FGC"], "plants", "source arithmetic", "p4", "Assumed retrofit at25 plants; feasibility/capital inputs missing")
    add("Table1_case_count", len(data["plants"]), "plants", "manual table reconciliation", "p5", "14 cases do not supply the110-plant database")
    for fuel in ["biomass", "waste"]:
        add("Table1_" + fuel, sum(x["fuel"] == fuel for x in data["plants"]), "plants", "manual table reconciliation", "p5", "Count of transcribed representative cases only")
    for kind in ["turbine", "primary steam", "hot water(b)"]:
        add("Table1_supply_" + kind, sum(x["reboiler_supply"] == kind for x in data["plants"]), "plants", "manual table reconciliation", "p5", "Footnote b is hot water; do not call these failed steam states")
    for fuel, values in data["fuel_composition_wt_percent"].items():
        add(fuel + "_composition_sum", sum(values), "wt%", "printed composition sum", "p6 Table2", "100.1wt% for waste is compatible with one-decimal rounding; no renormalization")
        oxidized = values[0] / 100 * 44 / 12
        add(fuel + "_conditional_full_oxidation_CO2", oxidized, "kgCO2/kgfuel", "conditional complete carbon oxidation", "p6 Table2", "No native LHV or oxidation analysis; not kgCO2/MWh or verified biogenic fraction")
        add(fuel + "_conditional90pct_capture", oxidized * u["capture_fraction"], "kgCO2/kgfuel", "conditional complete carbon oxidation", "p6 Table2", "Gross capture only; not avoided/retained carbon")
    for category in ["CHP", "industry"]:
        add("Table5_" + category + "_sum", sum(x[category + "_kt_y"] for x in data["hubs"]), "ktCO2/year", "seven-hub source sum", "p7 Table5", "CHP64% case; industrial totals are a separate source portfolio")
    add("Table5_combined_sum", sum(x["CHP_kt_y"] + x["industry_kt_y"] for x in data["hubs"]), "ktCO2/year", "separate-portfolios arithmetic", "p7 Table5", "25.065Mt is not110-CHP capture potential")
    add("truck_unrounded_staff_coverage", 7 * data["truck"]["shifts_per_day"] / data["truck"]["workdays_per_week"], "drivers/truck", "weekly coverage arithmetic", "p7", "4.2FTE rounds up to5; leave/fatigue/calendar not modeled")
    for years in [cap["economic_years"], cap["operating_years"]]:
        factor = crf(cap["discount_rate"], years)
        add(f"capture_CRF_{years}years", factor, "1/year", "alternative finance convention", "p6", "25-year economic versus23 operating years; actual construction cash-flow timing not reconstructed")
        for flow in data["analyst"]["capex_flows_t_h"]:
            total = capture_capex_EUR(flow, cap)
            add(f"capture_CAPEX_{flow}t_h_{years}year", total * factor / (flow * data["analyst"]["hours_per_year"]), "EUR/tcaptured", "printed power function with analyst8760full-load hours", "p6 Eq1", "Not an author plant point; no HP/FGC investment or truck/variable cost")
    for flow in data["analyst"]["capex_flows_t_h"]:
        add(f"capture_upfront_{flow}t_h", capture_capex_EUR(flow, cap), "EUR", "Eq1 kg/s input conversion", "p6 Eq1", "t/h divided by3.6 before applying power fit; price-year unknown")
    # Product check is conditional on pureCO2 and each disclosed pressure interpretation.
    backend = data["analyst"]["CO2_backend"]
    T = u["product_T_C"] + 273.15
    psat = PropsSI("P", "T", T, "Q", 0, backend)
    add("conditional_product_Psat", psat / 1e5, "barabsolute", "pureCO2 HEOS", "p7", "Not native mixture specification; no product state silently corrected")
    for label, P in [("15bara", u["product_P_bar"] * 1e5), ("15barg_plus_1atm", u["product_P_bar"] * 1e5 + data["analyst"]["atmospheric_Pa"])]:
        add(label + "_phase", PhaseSI("P", P, "T", T, backend), "phase", "conditional pureCO2 pressure interpretation", "p7", "Gas under these assumptions; authors' pressure basis/purity/composition unverified")
        add(label + "_saturation_pressure_margin", (P - psat) / 1e5, "bar", "conditional pureCO2 pressure interpretation", "p7", "Negative margin is a state-compatibility question, not a native flash validation")
        add(label + "_Tsat", PropsSI("T", "P", P, "Q", 0, backend) - 273.15, "degC", "conditional pureCO2 pressure interpretation", "p7", "Comparison only; do not replace reported−25°C")
    add("conditional3bara_water_Tsat", PropsSI("T", "P", u["steam_supply_bar"] * 1e5, "Q", 0, data["analyst"]["water_backend"]) - 273.15, "degC", "purewater absolute-pressure diagnostic", "p3", "Saturation above120°C plausible; does not prove steam-flow/part-load feasibility")
    for plant in data["plants"]:
        if plant["reboiler_supply"] == "hot water(b)":
            add(plant["plant"] + "_conditional_primary_phase", PhaseSI("P", plant["primary_P_bar"] * 1e5, "T", plant["primary_T_C"] + 273.15, data["analyst"]["water_backend"]), "phase", "purewater absolute-pressure interpretation", "p5 footnote b", "Liquid agrees with hot-water footnote; not a steam-model failure")
    r = data["reported"]
    for denominator in [r["national_2019_fossil_Mt"], r["national_intro_CO2_Mt"], r["national_intro_GHG_Mt"]]:
        for mass in [*r["biogenic_capture_rounded_Mt_y"], r["total_capture_Mt_y"][1]]:
            add(f"gross_{mass}Mt_over_{denominator}Mt", 100 * mass / denominator, "%", "conditional numerator/denominator comparison", "pp1,10,13", "Keep year/fossil/biogenic/CO2/GHG scope distinct; not net climate mitigation")
    for i in [0, 1]:
        add(f"predicted_total_cost_endpoint_{i}", r["most_capture_truck_EUR_t"][i] + r["ship_storage_prediction_EUR_t"][i], "EUR/tcaptured", "reported range endpoint arithmetic", "p13", "75–180 forecast range; not a matched same-case whole-chain inventory/cost")
    add("analyst_first_waste_plant_below_min_gap", max(0, .7 * 10 - 5), "MWheat", "disclosed10MW plant5MW demand example", "p6 rules1,5", "2MW gap if online minimum7MW; off+peak/spill/edge handling missing, not proof of native sheet defect")
    trucks = [truck_component(L, data["analyst"]["truck_daily_volume_m3"], cf, data["truck"], data["analyst"]) for L in data["analyst"]["distances_km"] for cf in data["analyst"]["annual_capacity_factors"]]
    return rows, trucks


def main():
    data = load_inputs(); rows, trucks = calculate(data)
    OUT.mkdir(parents=True, exist_ok=True)
    for filename, values in [("B2-11_checks.csv", rows), ("B2-11_truck_volume_grid.csv", trucks), ("B2-11_representative_plants.csv", data["plants"])]:
        with (OUT / filename).open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=values[0], lineterminator="\n")
            writer.writeheader(); writer.writerows(values)
    report = dict(study_id="B2-11", checks=len(rows), truck_component_rows=len(trucks),
                  representative_plants=len(data["plants"]), author_model="not_reproduced",
                  EOS_version=CoolProp.__version__, EOS_assumptions="HEOS pureCO2/water; absolute/gauge interpretations explicitly conditional",
                  missing_cooling_MEA_density_LCI_preserved=True, accepted_inputs_changed=False,
                  excluded_missing_inputs=data["missing_inputs"])
    (OUT / "B2-11_reconciliation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
