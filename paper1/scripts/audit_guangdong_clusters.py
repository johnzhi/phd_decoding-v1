#!/usr/bin/env python3
"""B3-06 printed cost, mass-bound and route accounting diagnostics.

This does not reproduce the author's native Guangdong cash flows, GIS, capture
process or LF-2A reservoir. Conflicting source units/numbers remain unchanged.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/comprehensive_review'


def annuity_factor(rate, years, include_start=False):
    """Fixed end-year payments; optional additional n=0 payment."""
    if not math.isfinite(rate) or rate < 0 or not isinstance(years, int) or years < 1:
        raise ValueError('A finite nonnegative rate and positive integer years are required')
    return math.fsum((1 + rate) ** -n for n in range(0 if include_start else 1, years + 1))


def conventional_present_cost(capital, annual_opex, rate, years):
    """Disclosed diagnostic convention: capital once at0, OPEX at1..years."""
    if any(not math.isfinite(x) or x < 0 for x in (capital, annual_opex)):
        raise ValueError('Finite nonnegative costs are required')
    return capital + annual_opex * annuity_factor(rate, years)


def saving_interval(standalone, cluster, halfstep=.005):
    """Extremal percentage savings from independently rounded positive costs."""
    if not all(math.isfinite(x) for x in (standalone, cluster, halfstep)):
        raise ValueError('Finite values are required')
    if halfstep < 0 or standalone <= halfstep or cluster < halfstep:
        raise ValueError('Positive cost denominators and nonnegative rounding step required')
    return (100 * (1 - (cluster + halfstep) / (standalone - halfstep)),
            100 * (1 - (cluster - halfstep) / (standalone + halfstep)))


def intervals_overlap(bounds, reported, halfstep=.005):
    return bounds[0] <= reported + halfstep and reported - halfstep <= bounds[1]


def gross_mass_bound(gross_Mt_y, rate, years, include_start=True):
    """Liberal discounted avoided-mass upper bound for nonnegative auxiliary CO2.

    Includes full gross capture at n=0 when requested; does not certify that the
    plant operates then or that captured CO2 equals avoided/stored/retained CO2.
    """
    if not math.isfinite(gross_Mt_y) or gross_Mt_y < 0:
        raise ValueError('Finite nonnegative gross capture required')
    return gross_Mt_y * annuity_factor(rate, years, include_start)


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B3-06.json').read_text())
    if hashlib.sha256((ROOT / data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale B3-06 source')
    return data


def calculate(data):
    checks, money, percentages, route_rows = [], [], [], []
    rate, years = data['discount_rate'], data['lifetime_y']
    factor = annuity_factor(rate, years)
    factor0 = annuity_factor(rate, years, True)

    def add(item, value, unit, scope):
        checks.append(dict(item=item, value=value, unit=unit, scope=scope))

    add('annuity_end_year_1_to_20', factor, 'years', 'Explicit diagnostic timing, not a verified native convention')
    add('discounted_year_0_to_20_factor', factor0, 'years', 'Conservative Eq1 gross-mass bound includes n=0')
    add('literal_time_indices_count', years + 1, 'count', 'n=0..20 has21 observations; not21 completed operating years')
    add('abstract_to_body_larger_plant_rate_ratio', data['abstract_plant_capture_Mt_y_as_printed'] / data['body_plant_capture_Mt_y'][1], 'ratio', 'Native300 versus3Mt/y preserved; no corrected abstract value inserted')
    for scenario, cluster in [('I', 475.81), ('II', 298.02)]:
        individual = [r for r in data['cases'] if r['scenario'] == scenario and r['item'] != 'Cluster']
        mean = math.fsum(r['cost_CNY_t_avoided'] for r in individual) / len(individual)
        add(scenario + '_standalone_mean', mean, 'CNY/t avoided', 'Equal-weight mean of printed unit costs, not captured-mass weighted system cost')
        add(scenario + '_mean_absolute_unit_saving', mean - cluster, 'CNY/t avoided', 'No conversion to absolute cash savings without matched avoided-mass denominators')
        add(scenario + '_mean_relative_unit_saving', 100 * (1 - cluster / mean), 'percent', 'Cost comparison only, not a GHG benefit')
        for row in individual:
            bounds = saving_interval(row['cost_CNY_t_avoided'], cluster)
            percentages.append(dict(scenario=scenario, plant=row['item'], calculated_percent=100 * (1 - cluster / row['cost_CNY_t_avoided']),
                                    lower_cost_rounding_percent=bounds[0], upper_cost_rounding_percent=bounds[1],
                                    table_percent=row['saving_table_percent'], prose_percent=row['saving_prose_percent'],
                                    table_rounding_compatible=intervals_overlap(bounds, row['saving_table_percent']),
                                    prose_rounding_compatible=intervals_overlap(bounds, row['saving_prose_percent']),
                                    scope='Independent +/-0.005 CNY/t cost rounding and +/-0.005 percentage-point display rounding; not statistical uncertainty'))
    add('cluster_scale_unit_cost_reduction', 100 * (1 - 298.02 / 475.81), 'percent', 'Unit costs fall; relative clustering advantage falls19.94 to15.92% across cases')
    for row in data['cases']:
        capital = math.fsum(row[k] for k in ['capture_capital_million_CNY', 'transport_capital_million_CNY', 'storage_capital_million_CNY'])
        annual = math.fsum(row[k] for k in ['capture_OM_million_CNY', 'transport_OM_million_CNY', 'storage_OM_million_CNY'])
        pv = conventional_present_cost(capital, annual, rate, years)
        # Table5 prints CNY, whereas Table6 explicitly prints million CNY.
        # The million interpretation for Table5 is conditional, not relabelling.
        required = row['reported_NPV_number'] / row['cost_CNY_t_avoided']
        implied = required / factor
        bound = gross_mass_bound(row['gross_capture_Mt_y'], rate, years)
        money.append(dict(scenario=row['scenario'], item=row['item'], physical_page=row['physical_page'],
                          native_NPV_number=row['reported_NPV_number'], native_NPV_header=row['NPV_native_header'],
                          NPV_scale_for_this_diagnostic='million CNY; conditional for Table5, explicit for Table6',
                          cost_CNY_t_avoided=row['cost_CNY_t_avoided'], capital_sum_million_CNY=capital,
                          annual_OM_sum_million_CNY=annual, once_at0_cost_million_CNY=pv,
                          diagnostic_minus_native_NPV_number=pv - row['reported_NPV_number'],
                          required_discounted_avoided_mass_Mt=required,
                          conditional_implied_constant_net_Mt_y=implied,
                          conditional_implied_auxiliary_Mt_y=row['gross_capture_Mt_y'] - implied,
                          gross_capture_Mt_y=row['gross_capture_Mt_y'], conservative_gross_PV_bound_Mt=bound,
                          compatible_with_gross_bound=required <= bound,
                          scope='Conditional timing/scale diagnostics, assuming reported NPV is Eq1 discounted cost numerator. Implied auxiliary mass is not verified native An. No guessed repair of 1548, storage billions or 173632.2.'))
    large = next(r for r in money if r['scenario'] == 'II' and r['item'] == 'Cluster')
    add('II_cluster_required_discounted_avoided_mass', large['required_discounted_avoided_mass_Mt'], 'Mt', 'Explicit Table6 million CNY divided by CNY/t; no native value corrected')
    add('II_cluster_liberal_discounted_gross_mass_bound', large['conservative_gross_PV_bound_Mt'], 'Mt', 'All9Mt/y at every n=0..20, zero auxiliary emissions; already overgenerous')
    add('II_cluster_required_to_gross_PV_bound_ratio', large['required_discounted_avoided_mass_Mt'] / large['conservative_gross_PV_bound_Mt'], 'ratio', 'Greater than1 rules out reconciliation within the stated positive-discount and nonnegative-auxiliary bounds')
    add('II_cluster_even_undiscounted_gross_bound', 9 * (years + 1), 'Mt', 'Conservative21 observations, still below required582.619Mt; not a native21-year case')
    required_min = (173632.2 - .05) / (298.02 + .005)
    add('II_cluster_required_mass_minimum_under_display_rounding', required_min, 'Mt', 'Allow native NPV +/-0.05M and cost +/-0.005; lower bound still exceeds liberal gross mass')
    add('I_cluster_4percent_capture_capital_reference', .04 * 3870, 'million CNY/y', '154.8 versus native1548; does not establish a decimal correction')
    add('II_individual_literal_storage_unit_OM', 120 * 3, 'million CNY/y', 'Literal120CNY/t at3Mt/y implies360M, versus native120M; units/case boundary unresolved')
    add('storage_capital_billion_to_table_million_ratio', 1000, 'ratio', 'Native Table4billion versus Table5/6million; no selection or repair')
    add('II_cluster_capture_capital_over_individual_total', 3870 / (3 * 2580), 'ratio', 'Undocumented scale treatment; not an established sharing benefit')
    add('II_over_I_cluster_reported_capture_OM_ratio', 1548 / 1548, 'ratio', 'Native same capture OPEX despite tripled capture; no inferred scaling law')
    add('II_over_I_cluster_reported_transport_OM_ratio', 171 / 171, 'ratio', 'Native same transport OPEX; flow allocation and route basis unknown')
    add('II_over_I_cluster_reported_storage_OM_ratio', 240 / 120, 'ratio', 'Only this cluster OPEX column doubles')
    hub = data['hub_sink_km']
    for plant in data['plants']:
        via = plant['hub_km'] + hub
        route_rows.append(dict(plant=plant['name'], native_direct_km=plant['direct_sink_km'], native_feeder_km=plant['hub_km'], native_shared_trunk_km=hub,
                               naive_via_hub_path_km=via, via_minus_direct_km=via - plant['direct_sink_km'],
                               scope='Path accounting under disclosed disjoint-edge assumption; not native routed GIS or length/cost optimization'))
    direct = math.fsum(r['native_direct_km'] for r in route_rows)
    feeder = math.fsum(r['native_feeder_km'] for r in route_rows)
    shared = feeder + hub
    path = math.fsum(r['naive_via_hub_path_km'] for r in route_rows)
    for item, value in [('direct_disjoint_sum', direct), ('feeder_disjoint_sum', feeder), ('shared_disjoint_physical_sum', shared),
                        ('sum_source_via_hub_paths', path), ('shared_disjoint_minus_table', shared - 228.23),
                        ('omit_Honghaiwan_feeder_minus_table', shared - 5.05 - 228.23)]:
        add(item, value, 'km', 'Conditional length accounting only; no actual route overlap, cost or permission inferred')
    add('conditional_disjoint_physical_length_reduction', 100 * (1 - shared / direct), 'percent', 'Unique physical length under analyst assumption; not per-source travel-distance reduction')
    add('conditional_equal_source_path_increase', 100 * (path / direct - 1), 'percent', 'Equal-source path sum increases although conditional unique network length falls')
    add('plants_total_installed_capacity', 2 * 1000 + 2 * 1000 + 4 * 600, 'MW', 'Installed capacity not capacity factor, capture operation or dispatch')
    a = data['analyst_conventions']['literal_cashflow_comparison']
    net = a['gross_Mt_y'] - a['auxiliary_Mt_y']
    conventional = conventional_present_cost(a['capital_million_CNY'], a['annual_opex_million_CNY'], rate, years) / (net * factor)
    literal = (a['capital_million_CNY'] + a['annual_opex_million_CNY']) / net
    add('analyst_conventional_once_capital_unit_cost', conventional, 'CNY/t avoided', 'Explicit100MCNY capital/10M annual OPEX/1Mt gross/.2Mt auxiliary, not a native case')
    add('analyst_literal_repeated_capital_unit_cost', literal, 'CNY/t avoided', 'Same analyst numbers, literal capital repeated n=0..20; finite discount factors cancel for constant inputs')
    return checks, money, percentages, route_rows


def main():
    data = load_inputs()
    checks, money, percentages, routes = calculate(data)
    OUT.mkdir(parents=True, exist_ok=True)
    for suffix, rows in [('checks', checks), ('financial_diagnostics', money), ('savings_rounding', percentages), ('route_accounting', routes)]:
        with (OUT / f'B3-06_{suffix}.csv').open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
    summary = dict(study_id='B3-06', source_sha256=data['source_sha256'], limited_checks=len(checks), financial_rows=len(money),
                   savings_rounding_rows=len(percentages), route_rows=len(routes), rounding_compatible_savings=sum(r['table_rounding_compatible'] for r in percentages),
                   direct_bibliography_entries=33, scoped_primary_citation_edges=0, native_cashflow_GIS_reservoir_or_capture_model_reproduced=False,
                   separate_supplement_inspected=False,
                   limits='Printed arithmetic, conditional financial timing/scale and route examples only. Necessary gross-mass bound assumes reported NPV is Eq1 discounted cost numerator; native definition remains unresolved. Raw 300, 1548, storage 431/862 billion, 173632.2, percentage variants and Table5 CNY header preserved. No native correction or accepted operating/GHG input.')
    (OUT / 'B3-06_reproduction_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
