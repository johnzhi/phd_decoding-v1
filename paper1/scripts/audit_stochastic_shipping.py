#!/usr/bin/env python3
"""B2-08 printed components and explicitly disclosed analyst examples only.

No native Pyomo/Gurobi case, MET archive, scenario reduction, HYSYS process,
operating policy or fault model is reproduced. No accepted input is changed.
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
OUT = ROOT / 'outputs/comprehensive_review'


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B2-08.json').read_text())
    for source in [data['source'], *data['cited_sources']]:
        if hashlib.sha256((ROOT / source['path']).read_bytes()).hexdigest() != source['sha256']:
            raise ValueError(f"Source changed: {source['path']}")
    return data


def pv_factor(rate, years):
    if rate <= -1 or years < 1:
        raise ValueError('Invalid discount horizon')
    return math.fsum((1 + rate) ** -t for t in range(1, years + 1))


def tank_path(initial, unloaded, reconditioned, literal=False):
    if len(unloaded) != len(reconditioned):
        raise ValueError('Matching flow series required')
    net = np.asarray(unloaded, dtype=float) - np.asarray(reconditioned, dtype=float)
    return initial + np.cumsum(-net if literal else net)


def minimum_service_example(alpha, literal=False, unit_transport_cost=150):
    """Analyst one-unit LP with a100 emission penalty and an explicit direction."""
    if not 0 <= alpha <= 1:
        raise ValueError('Fractional requirement required')
    sign = 1 if literal else -1
    result = linprog([unit_transport_cost, 100], A_eq=[[1, 1]], b_eq=[1],
                     A_ub=[[sign, 0]], b_ub=[sign * alpha], bounds=[(0, 1)] * 2,
                     method='highs')
    if not result.success:
        raise RuntimeError(result.message)
    return result


def speed_component(power_W, width_m, length_m, wave_m,
                    mass_density=1025, gravity=9.80665, design_knots=12):
    """Conditional Eq22: analyst Rf=P/Vdesign and SI mass density, not relative density."""
    if min(power_W, width_m, length_m, mass_density, gravity, design_knots) <= 0 or wave_m < 0:
        raise ValueError('Positive physical fixture required')
    design_mps = design_knots * 1852 / 3600
    resistance = power_W / design_mps
    wave_resistance = mass_density * gravity * wave_m ** 2 * width_m * math.sqrt(width_m / length_m) / 16
    return power_W / (resistance + wave_resistance) * 3600 / 1852


def scaled_capital(capacity, reference=3, cost=7.9, exponent=.8):
    if min(capacity, reference) <= 0:
        raise ValueError('Positive capacities required')
    return cost * (capacity / reference) ** exponent


def intervals_overlap(a, b):
    return max(a[0], b[0]) <= min(a[1], b[1]) + 1e-12


def calculate(data):
    rows = []; speed_rows = []
    c = data['case']; b = data['buffers']; k = data['cost']

    def add(item, value, unit, basis, locator, interpretation):
        rows.append(dict(item=item, value=value, unit=unit, basis=basis,
                         source_locator=locator, interpretation=interpretation))

    add('hours_per_season', c['steps_per_season'] * c['step_hours'], 'hours', 'printed arithmetic', 'pp3–4', 'Representative season, not a continuous operating year')
    add('representative_days', c['steps_per_season'] * c['step_hours'] / 24 * c['seasons'] * c['scenarios'], 'days', 'printed arithmetic', 'pp3–4', '442 representative days, not independent monitoring coverage')
    annual_hourly = c['annual_t'] / 8760
    add('nonleap_calendar_average', annual_hourly, 't/hour', 'conditional calendar conversion', 'pp2,7', '365-day basis is disclosed, not a recovered native time weight')
    add('calm_water_time', c['distance_km'] / (12 * 1.852), 'hours', 'conditional exact-unit arithmetic', 'p7', '32.17 versus reported32.5 may involve route/discretization/rounding; not a forced correction')
    add('source_buffer_hours', b['rate99_t'] / annual_hourly, 'hours', 'conditional calendar conversion', 'p7', 'Approximately four days16hours, not actual availability')
    add('reported_95h_cycle_mass', annual_hourly * 95, 'tonnes', 'conditional calendar conversion', 'pp7–8', 'Not a recovered native mean cycle; 4330 is an approximate comparison basis')
    for name in ['rate99_t', 'rate100_t', 'breakdown_t']:
        add(name + '_percent_ship', 100 * b[name] / c['ship_t'], 'percent', 'printed ratio', 'pp7–10', 'Do not merge99%,100% and ideal breakdown cases')
        add(name + '_percent_reference_cycle', 100 * b[name] / c['reference_cycle_t'], 'percent', 'conditional cycle ratio', 'pp7–10', 'Approximate4330t cycle denominator differs from5000t ship')
    add('printed_breakdown_extra_difference', b['breakdown_t'] - b['rate100_t'] - b['printed_extra_breakdown_t'], 'tonnes', 'printed arithmetic', 'p9', '10t difference may depend on endpoint rounding/version; no silent correction')
    add('double_reference_cycle', 2 * c['reference_cycle_t'], 'tonnes', 'printed arithmetic', 'p9', 'Ideal one-cycle fault example only')
    for i, capacity in enumerate(b['fuel_sensitivity_t']):
        percent = 100 * capacity / c['ship_t']
        add(f'fuel_case_{i}_ship_percent', percent, 'percent', 'printed ratio', 'p9 Table4', 'Fixed5000t ship denominator')
        add(f'fuel_case_{i}_label_residual', percent - b['printed_ship_percent'][i], 'percentage points', 'printed ratio comparison', 'p9 Table4', 'Last109.6 versus110.0 remains unresolved; no alternate denominator invented')
        add(f'fuel_case_{i}_fuel_price', k['base_fuel_price'] * (1 + .5 * i), '2017EUR/tfuel', 'printed sensitivity arithmetic', 'p9', 'Sensitivity price, not a calibrated stochastic probability')
    a = pv_factor(c['discount'], c['years'])
    add('standard_endyear_PV_factor', a, 'years of annual cost', 'analyst standard financial identity', 'pp3,6,13', 'Not replacement of printed10.56 or inferred construction convention')
    add('printed_annuity_difference', c['printed_annuity'] - a, 'factor', 'printed versus conditional identity', 'p6 Table1', 'Requires cashflow-base and construction mapping')
    transported = c['annual_t'] * .99
    for label, factor in [('standard', a), ('printed', c['printed_annuity'])]:
        add('unit99_from_PV_' + label, k['lifetime99_MEUR'] * 1e6 / (transported * factor), 'EUR/t', 'conditional reported arithmetic', 'p7', 'Not a native objective or complete cost reconstruction')
        interval = ((k['lifetime99_MEUR'] - .5) * 1e6 / (transported * factor),
                    (k['lifetime99_MEUR'] + .5) * 1e6 / (transported * factor))
        add('unit99_rounding_overlap_' + label, int(intervals_overlap(interval, (33.75, 33.85))), 'boolean', 'conditional displayed rounding', 'p7', 'Assumes143roundedto1MEUR and33.8to.1EUR/t; not uncertainty calibration')
    add('last_percent_cost_from_rounded_delta', k['additional100_MEUR'] * 1e6 / (c['annual_t'] * .01 * a), 'EUR/t incremental', 'conditional reported arithmetic', 'p8', 'Rounded1.8MEUR may support41.9; actual cashflows unverified')
    add('last_percent_rounding_overlap', int(intervals_overlap(((1.8 - .05) * 1e6 / (4000 * a), (1.8 + .05) * 1e6 / (4000 * a)), (41.85, 41.95))), 'boolean', 'conditional displayed rounding', 'p8', 'No corrected marginal cost supplied')
    add('last_percent_premium', 100 * (k['last_one_percent'] / k['unit99'] - 1), 'percent', 'reported arithmetic', 'p8', 'Approximately24%; transport is not capture or lifecycle abatement')
    add('body_component_sum', sum(k[x] for x in ['conditioning', 'shipping', 'buffers', 'reconditioning']), 'EUR/t', 'reported arithmetic', 'p7', '33.8 component sum, not a new physical inventory')
    add('energy_component_point_sum', k['conditioning_electricity'] + k['ship_fuel'], 'EUR/t', 'reported arithmetic', 'p7', '11.9 point sum versus11.8 reported total; rounding intervals can overlap')
    add('energy_rounding_overlap', int(intervals_overlap((7.75 + 4.05, 7.85 + 4.15), (11.75, 11.85))), 'boolean', 'conditional displayed rounding', 'p7', 'Do not assert a proven contradiction from rounded components')
    add('VSS_percent_of_reported143', 100 * k['VSS_MEUR'] / k['lifetime99_MEUR'], 'percent', 'reported arithmetic', 'p8', '4.5% rounded comparison; native common service/objective still needed')
    add('one_point_nine_percent', 100 * k['reported_unit_increment'] / k['unit99'], 'percent', 'reported arithmetic', 'p8', '5.6% uses a different denominator from lifetime VSS percentage')
    add('one_percent_annual_vent', .01 * c['annual_t'], 'tonnes/year', 'reported arithmetic', 'p8', '4000sourceCO2, not complete lifecycle fuel or retention')
    add('conditional_different_throughput_cost_increment', ((143 + 1.8 + 6.4) * 1e6 / (396000 * a) - (143 + 1.8) * 1e6 / (400000 * a)), 'EUR/t', 'analyst possible denominator reconciliation', 'p8', 'Approximately1.86 can explain1.9 with distinct transported masses; not verified native basis')
    add('conditional_slowing_benefit', 1e6 / (transported * a), 'EUR/t', 'conditional reported arithmetic', 'pp7–8', 'Approximately.24, not an independently reproduced power policy')
    add('winter_vent_penalty', 3250 * c['emission_penalty'] / 1e6, 'MEUR/year', 'reported arithmetic', 'p8', '.325 approximates.33; no full native seasonal schedule')
    add('twenty_percent_winter_cycle_mass', c['ship_t'] + 445, 'tonnes/cycle', 'reported arithmetic', 'p8', 'Not annual injectivity or a general seasonal model')
    add('wrong_price_loss_ratio', 2.1 / .73, 'ratio', 'reported arithmetic', 'p9', 'Reported asymmetric example, not a universal theorem')
    for label, capital, om in [('conditioning', 50.5, 2.78), ('reconditioning', 9, .41), ('buffer', 982, 54)]:
        add(label + '_OM_at_5point5_percent', .055 * capital, 'EUR/(capacity tonne*year)', 'printed factor identity', 'pp6,12', 'Capacity time basis still unresolved')
        add(label + '_OM_residual', om - .055 * capital, 'EUR/(capacity tonne*year)', 'printed factor comparison', 'pp6,12', 'Reconditioning requires coefficient/version reconciliation')
    add('implied_buffer_mass_density', 1130 / 982, 'tonnes/m3', 'conditional cost-unit conversion', 'pp6,12', 'Implied density only, not independently verified EOS')
    add('conditional_conditioning_electricity', 7.8 / 65.2 * 1000, 'kWh/t', 'conditional reported cost/price', 'pp7,12', 'Rounded electricity-cost claim only; not accepted complete utility inventory')
    for exponent in [.8, .85]:
        add(f'harbor_scaling_exponent_{exponent}', scaled_capital(.4, exponent=exponent), 'MEUR per facility', 'two literal source conventions', 'pp12–13', 'No preferred exponent or source correction chosen')
    add('ship_capital_Table2_minus_Table6', 23.9 - 23.7, 'MEUR', 'printed comparison', 'pp6,12', '5000t ship cost versions unresolved')
    add('ship_capital_Table6_minus_Table1', 23.7 - 22.31, 'MEUR', 'printed comparison', 'pp6,12', 'Cost scope/date not harmonized by guessing')
    add('ship_fixedOM_Table6_minus_Table1', 1.61 - 1.49, 'MEUR/year', 'printed comparison', 'pp6,12', 'Fixed-cost version unresolved')
    add('literal_mass_loaded_four_3h_slots', c['ship_t'] / c['port_hours'] * 4, 'tonnes', 'analyst literal time-unit comparison', 'p5 Eq11/12', 'Rate without3h factor loads one-third cargo over12h')
    add('duration_scaled_mass_loaded_four_3h_slots', c['ship_t'] / c['port_hours'] * c['step_hours'] * 4, 'tonnes', 'analyst separate duration comparison', 'p5 Eq11/12', 'No native slot/time implementation inferred')
    for literal in [True, False]:
        result = minimum_service_example(.99, literal)
        add('toy_service_' + ('literal_upper' if literal else 'minimum_lower'), float(result.x[0]), 'fraction', 'analyst independent LP', 'p5 Eq21', 'Analysttransportcost150 andpenalty100; not native shipping cost')
    add('toy_cheap_service_literal_upper', float(minimum_service_example(.99, True, 20).x[0]), 'fraction', 'analyst independent LP', 'p5 Eq21', 'Cheaptransportcanreachupperbound; that doesnotturnupperboundintominimum')
    proper = tank_path(0, [2, 0], [0, 2]); literal_fixed = tank_path(0, [2, 0], [0, 2], True)
    literal_free = tank_path(2, [2, 0], [0, 2], True)
    add('toy_physical_tank_min', float(proper.min()), 'tonnes', 'analyst fixed-initial tank', 'p5 Eq17/18', 'Initialzero;arrival2thenwithdrawal2')
    add('toy_literal_tank_min', float(literal_fixed.min()), 'tonnes', 'analyst fixed-initial tank', 'p5 Eq17/18', 'Literalreceivingsigngivesnegativeinventory withthe sameinitialcondition')
    add('toy_free_cyclic_complement_error', float(np.abs(literal_free - (2 - proper)).max()), 'tonnes', 'analyst free-cyclic comparison', 'p5 Eq17/18', 'Zero proves complement for this fixture; sign issue need not change free-cyclic capacity objective')
    add('toy_unweighted_two_scenario_service', .5, 'fraction', 'analyst equal-mass fixture', 'p5 Eq21', 'Flows[1,0]and[0,1]have same raw pooled fraction')
    add('toy_weighted_highprobability_service', .99, 'fraction', 'analyst probabilities[.99,.01]', 'p5 Eq21', 'Unknown native probabilities are not supplied by this example')
    add('toy_weighted_lowprobability_service', .01, 'fraction', 'analyst probabilities[.99,.01]', 'p5 Eq21', 'Raw pooled fraction alone doesnotdefineexpectedservice')
    for ship in data['ships']:
        for scale, label in [(1, 'literal_W'), (1000, 'conditional_kW')]:
            for wave in range(13):
                speed_rows.append(dict(cargo_t=ship['cargo_t'], wave_m=wave,
                                       power_interpretation=label,
                                       speed_knots=speed_component(ship['power_literal_W'] * scale, ship['width_m'], ship['length_m'], wave),
                                       scope='Analystrho1025/g9.80665/Rf=P/Vdesign12kn;notnativeSTAwavevalidation'))
        add(f"hourly_fuel_increase_{ship['cargo_t']}", 100 * (ship['fuel_full_tph'] / ship['fuel_constant_tph'] - 1), 'percent', 'printed hourly fuel ratio', 'p6 Table2', 'Not comparable to route-total40%withouttime/wavecontrols')
    return rows, speed_rows


def main():
    data = load_inputs(); rows, speeds = calculate(data); OUT.mkdir(parents=True, exist_ok=True)
    for name, values in [('B2-08_checks.csv', rows), ('B2-08_speed.csv', speeds)]:
        with (OUT / name).open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(values[0]), lineterminator='\n')
            writer.writeheader(); writer.writerows(values)
    result = dict(study_id='B2-08', source_sha256=data['source']['sha256'], checks=len(rows), conditional_speed_rows=len(speeds),
                  native_stochastic_optimizer_or_policy_reproduced=False, weather_scenario_process_or_fault_model_reproduced=False,
                  pressure_constrained_service_or_complete_utility_inventory=False, accepted_operating_GHG_inputs_changed=False,
                  scope='Printed arithmetic and disclosed analyst examples; no silent notation/unit correction or native-code defect claim')
    (OUT / 'B2-08_reconciliation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
