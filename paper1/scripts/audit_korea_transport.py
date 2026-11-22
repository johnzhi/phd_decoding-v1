#!/usr/bin/env python3
"""B3-07 source arithmetic and explicitly conditional engineering diagnostics.

No native Korean GIS, 64-design optimization, ship schedule, HYSYS/cost model,
reservoir service, complete capture inventory or cited author model is reproduced.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import CoolProp
import CoolProp.CoolProp as CP

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/comprehensive_review'


def mass_flow(Mt_y, seconds_y=365 * 86400):
    if not math.isfinite(Mt_y) or Mt_y < 0 or not math.isfinite(seconds_y) or seconds_y <= 0:
        raise ValueError('Finite nonnegative annual mass and positive duration required')
    return Mt_y * 1e9 / seconds_y


def pressure_drop(flow, length, diameter, rho, friction, dz, gravity=9.80665):
    """Literal Eq1 with constant analyst rho/f and Darcy-style coefficient."""
    if any(not math.isfinite(x) for x in (flow, length, diameter, rho, friction, dz, gravity)):
        raise ValueError('Finite physical inputs required')
    if min(flow, length, friction) < 0 or min(diameter, rho, gravity) <= 0:
        raise ValueError('Positive geometry/properties and nonnegative flow/friction required')
    return 8 * friction * flow ** 2 * length / (rho * math.pi ** 2 * diameter ** 5) + rho * gravity * dz


def compressor_capital(train_flow, trains, pressure_ratio):
    if train_flow <= 0 or not isinstance(trains, int) or trains < 1 or pressure_ratio <= 1:
        raise ValueError('Positive train flow/count and compression ratio>1 required')
    return train_flow * trains * (.13e6 * train_flow ** -.71 + 1.40e6 * train_flow ** -.60 * math.log(pressure_ratio))


def pump_capital(power_kW, booster=False):
    if not math.isfinite(power_kW) or power_kW < 0:
        raise ValueError('Nonnegative finite kW required')
    slope, intercept = (7.82e6, .46e6) if booster else (1.11e6, .07e6)
    return slope * power_kW / 1000 + intercept


def pipe_mass(length_m, steel_rho, inner_m, wall_m):
    if min(length_m, steel_rho, inner_m, wall_m) <= 0:
        raise ValueError('Positive pipe geometry and density required')
    return math.pi * length_m * steel_rho * wall_m * (inner_m + wall_m)


def minimum_wall(P_Pa, outer_m, strength_Pa, F=.8, L_f=.9, J=1, T=1):
    if min(P_Pa, outer_m, strength_Pa, F, L_f, J, T) <= 0:
        raise ValueError('Positive design inputs required')
    return P_Pa * outer_m / (2 * strength_Pa * F * L_f * J * T)


def roundtrip_hours(distance_km, speed_knots, loading_h=20, unloading_h=20, entry_h=2, exit_h=2):
    """Idealized two-way voyage and four stated port/handling allowances.

    Additional stops, weather, maintenance and scheduling constraints are absent.
    """
    if distance_km < 0 or speed_knots <= 0 or min(loading_h, unloading_h, entry_h, exit_h) < 0:
        raise ValueError('Nonnegative distance/times and positive speed required')
    return 2 * distance_km / (speed_knots * 1.852) + loading_h + unloading_h + entry_h + exit_h


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B3-07.json').read_text())
    if hashlib.sha256((ROOT / data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale B3-07 source')
    return data


def calculate(data):
    n, a = data['native'], data['analyst']
    checks, steels, trains, fleet = [], [], [], []

    def add(item, value, unit, scope):
        checks.append(dict(item=item, value=value, unit=unit, scope=scope))

    kg_s = mass_flow(1, a['seconds_per_year'])
    add('one_Mt_y_constant_365day_flow', kg_s, 'kg/s', 'Calendar conversion only; native operating hours remain unknown')
    annual = n['injection_as_printed_kg_s'] * a['seconds_per_year'] / 1e9
    add('printed_2800kg_s_if_continuous', annual, 'Mt/y', 'Raw2800 preserved; does not equal1Mt/y under continuous365day operation')
    add('printed_over_calendar_flow_ratio', n['injection_as_printed_kg_s'] / kg_s, 'ratio', 'No alternative unit or corrected injection rate inferred')
    add('hours_for_one_Mt_at_printed_flow', 1e9 / n['injection_as_printed_kg_s'] / 3600, 'h', 'Could represent limited batch operation, not the stated continuous equivalence')
    add('pipeline_route_leg_sum', 280 + 190 + 60, 'km', 'Matches native530km pipeline route, not an optimal GIS reconstruction')
    add('scenario2_ship_table_leg_sum', 617 + 270, 'km', 'Native Table2 leg sum887; preserve prose877 separately')
    add('scenario2_table_sum_minus_prose', 617 + 270 - n['scenario2_ship_distance_prose_km'], 'km', 'Unresolved10km native source discrepancy')
    add('scenario2_table_extension', 100 * ((617 + 270) / 724 - 1), 'percent', '22.51% from table legs; route rounding/basis remains unknown')
    add('scenario2_prose_extension', 100 * (877 / 724 - 1), 'percent', '21.13% from prose877; printed22% is not silently replaced')
    add('Hadong_pipeline_fraction_of_total', 100 * 280 / 530, 'percent', 'Compatible with approximate53% claim')
    add('unequal_route_ship_over_pipe', 724 / 530, 'ratio', 'Technology cost comparison has unequal geographic routes, not a common-distance break-even threshold')
    add('scenario3_disjoint_shared_network', 470 + 250 + 60, 'km', 'Conditional unique-length accounting, not actual optimized GIS')
    add('scenario3_two_separate_source_paths', 470 + 60 + 250 + 60, 'km', 'Sum of source paths differs from unique shared length')
    add('scenario3_conditional_shared_length_reduction', 100 * (1 - 780 / 840), 'percent', 'Two source paths held fixed; no universal hub cost or GHG advantage')
    add('pipeline_pressure_band', (n['pipeline_max_bar'] - n['pipeline_min_bar']) / 10, 'MPa', '6.4MPa transport-design range, not reservoir fracture or maximum-injection calibration')
    add('five_reported_stage_ratios', n['stage_ratio'] ** n['compression_stages'], 'pressure ratio', '2.36^5 is compatible with rounding of the stated1-to73.8bar target')
    add('stage_ratio_required_for_target', 73.8 ** .2, 'ratio', '2.36380 rounds to2.36; no corrected native stage ratio inserted')
    crf = n['discount_rate'] / (1 - (1 + n['discount_rate']) ** -n['lifetime_y'])
    add('capital_recovery_exact_component', crf, '1/y', '5%discount and20years; native0.08 is rounded CRF, not8%discount')
    add('capital_recovery_rounding_relative_difference', 100 * (n['capital_recovery_printed'] / crf - 1), 'percent', 'Display-rounding component only, not full native annualization/cash flows')
    for mode in ['pipe', 'ship']:
        c = n[f'scenario1_{mode}_USD_t']
        add(mode + '_one_to_three_Mt_reported_unit_cost_reduction', 100 * (1 - c['3'] / c['1']), 'percent', 'Approximate native cost labels, not lifecycle or equal-route comparison')
    add('quoted_no_conditioning_B1_gap', 23 - 11, 'USD/t transported', 'Approximate pipeline23/ship11 component costs; conditioning premium can reverse rankings')
    add('quoted_seven_USD_if_all_electricity', 7 / n['price_electricity_USD_kWh'], 'kWh/t', 'Conditional conversion only: financial premium includes other costs, so100kWh/t is NOT native electricity duty')
    add('storage_material_share_at_280_total', (1 - .45) * 280, 'USD/m3', 'Manufacturing45%of total implies material55%, not45%markup on material')
    add('storage_manufacturing_share_at_280_total', .45 * 280, 'USD/m3', 'Source approximate tank cost, not native fabrication quote or rights verification')
    add('number_priced_steel_grades', sum(x['price_USD_per_ton'] is not None for x in data['steel']), 'count', 'Eight priced grades; ninthX90 explicitlyN/A')
    add('quoted_design_combinations', 8 * 8, 'count', 'Eight diameter choices times eight priced grades; standard schedules and native choices remain missing')
    add('analyst_horizontal_pressure_drop', pressure_drop(a['test_mass_kg_s'], a['test_length_m'], a['test_inner_diameter_m'], a['rho_CO2_kg_m3'], a['friction_factor'], 0), 'Pa', 'Analyst30kg/s,100km,0.3m,900kg/m3,f.02; no native hydraulics replay')
    add('analyst_offshore_gravity_component', a['rho_CO2_kg_m3'] * a['g_m_s2'] * -150, 'Pa', 'Analyst density with native minus150m elevation; seawater depth is not reservoir depth')
    wall = minimum_wall(15e6, a['test_outer_diameter_m'], a['test_grade_MPa'] * 1e6)
    add('analyst_Eq6_minimum_wall', wall, 'm', 'Analyst0.3m outer diameter and quotedX42strength; no schedule rounding or64-case replay')
    add('analyst_Eq5_pipe_mass', pipe_mass(a['test_pipe_length_m'], a['rho_steel_kg_m3'], a['test_inner_diameter_m'], a['test_wall_t_m']), 'kg', 'Explicit analyst1km,7850kg/m3,0.3m inner,0.01m wall; not native material procurement')
    add('analyst_Eq3_pump_at_1000kW', pump_capital(1000), 'USD', 'Literal coefficient component with analyst power, not actual equipment quote')
    add('analyst_Eq4_booster_at_1000kW', pump_capital(1000, True), 'USD', 'Literal coefficient component; native station powers/counts unverified')
    add('two_hour_buffer_for_one_Mt_calendar_flow', kg_s * 7200 / 1000, 't', 'Conditional flat1Mt/y basis; source actual buffer geometry and operation not reconstructed')
    weights = a['illustrative_cost_weighting']
    add('analyst_equal_mean_unit_cost', sum(r['unit_cost'] for r in weights) / len(weights), 'cost units/mass', 'Analyst10/30unit costs and1/3flows: simple mean20 is not total cost divided by total mass')
    add('analyst_mass_weighted_unit_cost', sum(r['unit_cost'] * r['flow'] for r in weights) / sum(r['flow'] for r in weights), 'cost units/mass', 'Analyst weighted25; paper equal1Mt source average does not generalize unchanged to unequal flows')
    for row in data['steel']:
        exact = row['psi'] * 6894.757293168 / 1e6
        steels.append(dict(**row,exact_psi_conversion_MPa=exact,quoted_minus_exact_MPa=row['quoted_MPa'] - exact,scope='Small native conversion/rounding variations preserved. USD/ton basis and2015internet quotes unverified; no corrected design strength.'))
    for mode, m, count in [('fixed_count', 10, 1), ('fixed_count', 20, 1), ('fixed_train_flow', 10, 1), ('fixed_train_flow', 10, 2)]:
        cap = compressor_capital(m, count, a['pressure_ratio'])
        trains.append(dict(analyst_mode=mode,train_flow_kg_s=m,trains=count,total_flow_kg_s=m * count,capital_USD=cap,capital_per_kg_s=cap / (m * count),scope='Analyst flow/count components. Fixed train flow yields proportional total capital; fixed count has sublinear flow powers. No native40MWtrain assignment inferred.'))
    for distance in [724, 877, 887]:
        cycle = roundtrip_hours(distance, n['ship_speed_knots'])
        fleet.append(dict(distance_km=distance,ideal_roundtrip_h=cycle,ships=3,assumed_direct_delivery_window_h=20,direct_delivery_coverage_upper_fraction=3 * 20 / cycle,conditional_minimum_ship_count=math.ceil(cycle / 20),scope='Conditional: each20h unloading window directly serves the well. No receiving buffer, weather or extra stops.724km isS1;877/887are alternative route-length illustrations, notS2schedule reproduction. A different injection duration/buffer/control could change the bound; native schedule unverified.'))
    return checks, steels, trains, fleet


def pure_state_rows(data):
    if CoolProp.__version__ != '8.0.0':
        raise ValueError('Pinned diagnostic backend CoolProp8.0.0 required')
    rows = []
    for kind, states in [('nominal_label', data['analyst']['pure_states']), ('Figure4_rounding_corner', data['analyst']['Figure4_rounding_corners'])]:
        for state in states:
            P, T = state['P_bar'] * 1e5, state['T_C'] + 273.15
            rho = CP.PropsSI('D', 'P', P, 'T', T, 'HEOS::CO2')
            rows.append(dict(kind=kind,label=state.get('label', 'rounding_corner'),P_bar_absolute_assumed=state['P_bar'],T_C=state['T_C'],density_kg_m3=rho,backend_phase=CP.PhaseSI('P', P, 'T', T, 'HEOS::CO2'),scope='Pure absolute-pressure HEOS component only. Native mixtures, rounded scheme correspondence, hydrates/solids, pumps and complete energy balances not validated.'))
    return rows


def main():
    data = load_inputs()
    checks, steels, trains, fleet = calculate(data)
    states = pure_state_rows(data)
    OUT.mkdir(parents=True, exist_ok=True)
    for suffix, rows in [('checks',checks),('steel_units',steels),('compressor_examples',trains),('fleet_timing_bounds',fleet),('pure_states',states)]:
        with (OUT / f'B3-07_{suffix}.csv').open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
            writer.writeheader(); writer.writerows(rows)
    summary = dict(study_id='B3-07',source_sha256=data['source_sha256'],limited_checks=len(checks),steel_rows=len(steels),compressor_example_rows=len(trains),conditional_fleet_rows=len(fleet),nominal_pure_states=7,rounding_state_corners=4,
                   pure_backend=dict(CoolProp=CoolProp.__version__,backend='HEOS::CO2',EOS=CP.get_fluid_param_string('CO2','BibTeX-EOS')),
                   scoped_citation_edges=2,native_design_optimization_HYSYS_GIS_ship_or_reservoir_reproduced=False,
                   limits='Printed arithmetic, literal formula components, analyst geometry/flows, conditional scheduling and pure states only. Preserve2800kg/s,877/887km,Fig3versusFig4states and native approximate costs. No unsupported corrections, capture inventory, annual pressure service, GHG/retention factor or accepted operating input.')
    (OUT / 'B3-07_reproduction_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
