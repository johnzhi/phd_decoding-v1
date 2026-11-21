#!/usr/bin/env python3
"""Limited B2-05 equation/accounting checks. No native Swiss model replay.

Printed values, conditional unit conversions and analyst examples remain
separate. Nothing from this script enters accepted operating/GHG inputs.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/comprehensive_review'


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B2-05.json').read_text())
    for source in [data['source'], *data['cited_sources']]:
        if hashlib.sha256((ROOT / source['path']).read_bytes()).hexdigest() != source['sha256']:
            raise ValueError(f"Source changed: {source['path']}")
    return data


def period_weights(periods, step):
    """Annual interval counts: final modeled year has weight one (Eq2)."""
    if periods < 1 or step < 1:
        raise ValueError('Positive integer periods/step required')
    return [step] * (periods - 1) + [1]


def discount_weights(periods, step, rate):
    """Eq2 with y a consecutive period index, not a calendar-year label."""
    if rate <= -1:
        raise ValueError('Invalid discount rate')
    return [sum((1 + rate) ** -(step * k + i) for i in range(n))
            for k, n in enumerate(period_weights(periods, step))]


def surviving_capacity(additions, period, life_years, step):
    """Literal Eq3 ceiling convention; not exact intra-period retirement."""
    if life_years <= 0 or step <= 0:
        raise ValueError('Positive lifetime and step required')
    start = max(0, period - math.ceil(life_years / step) + 1)
    return math.fsum(additions[start:period + 1])


def knowledge(additions, period, step, depreciation):
    """Eq9/12/14 for an already selected capacity/distance metric."""
    if not 0 <= depreciation <= 1:
        raise ValueError('Annual depreciation outside [0,1]')
    return math.fsum((1 - depreciation) ** (step * (period - k)) * additions[k]
                     for k in range(period))


def saturated_diffusion(periods, step, rate, pioneering, depreciation=0):
    """Saturate the source upper bound; no demand, construction or network."""
    if rate < 0 or pioneering < 0:
        raise ValueError('Nonnegative diffusion parameters required')
    growth = (1 + rate) ** step - 1
    additions, rows = [], []
    for k in range(periods):
        stock = knowledge(additions, k, step, depreciation)
        added = growth * stock + step * pioneering
        rows.append(dict(period_index=k, knowledge=stock, addition=added,
                         cumulative_metric=math.fsum(additions) + added))
        additions.append(added)
    return rows


def penalty_example(service_cost, penalty_cost):
    """Independent analyst LP: one feasible unit of service versus soft slack."""
    result = linprog([service_cost, penalty_cost], A_ub=[[-1, -1]], b_ub=[-1],
                     bounds=[(0, 1), (0, None)], method='highs')
    if not result.success:
        raise RuntimeError(result.message)
    return dict(service=float(result.x[0]), slack=float(result.x[1]), cost=float(result.fun))


def pipeline_capex(capacity_ktpy, distance_km, per_capacity, per_distance, built=1):
    """Eq7/Table1 literal units; raw CAPEX, not annualized or levelized cost."""
    if min(capacity_ktpy, distance_km, per_capacity, per_distance) < 0 or built not in (0, 1):
        raise ValueError('Invalid pipeline inputs')
    if not built and capacity_ktpy:
        raise ValueError('Analyst example enforces capacity/build linkage')
    return built * distance_km * per_distance + capacity_ktpy * per_capacity


def calculate(data):
    rows = []
    def add(item, value, unit, basis, locator, interpretation):
        rows.append(dict(item=item, value=value, unit=unit, basis=basis,
                         source_locator=locator, interpretation=interpretation))
    p = data['planning']; t = data['reported']; weights = period_weights(p['periods'], p['step_years'])
    add('planning_periods', len(weights), 'periods', 'printed arithmetic', 'p5 Section3.1', '2026,2029,...,2050')
    add('annual_interval_count', sum(weights), 'years', 'Eq2 index convention', 'p3 Eq2; p5', 'Eight three-year blocks and final one-year endpoint')
    dw = discount_weights(p['periods'], p['step_years'], p['discount_rate'])
    add('discounted_annual_weights', sum(dw), 'discounted annual weights', 'Eq2 reconstruction', 'p3 Eq2', 'Constant annual stream only; not the native time-varying objective')
    add('second_period_correct_calendar_exponent', p['step_years'], 'years', 'index clarification', 'p3 Eq2', 'y must be a consecutive index')
    add('second_period_calendar_labels_literal_exponent', p['step_years'] ** 2, 'years', 'analyst counter-interpretation', 'p3 Eq2', 'Substituting calendar-year differences would count the step twice; native code not checked')
    add('lifetime10_literal_blocks', math.ceil(10 / 3), 'periods', 'analyst Eq3 example', 'p3 Eq3', 'Four whole periods for a ten-year lifetime')
    add('lifetime10_block_retirement_year', 3 * math.ceil(10 / 3), 'years', 'analyst Eq3 example', 'p3 Eq3', 'Twelve-year block retirement; not an allegation about actual technology lifetimes')
    add('diffusion_three_year_growth', (1.12 ** 3 - 1), 'fraction', 'printed parameter component', 'p4 Eq13; p6 Table2', 'Not simply three times12%')
    add('first_metric_addition_bound', 3 * 160, 'MtCO2 km/year rated capacity', 'printed parameter component', 'p4 Eq13; p6 Table2', 'No prior knowledge; dy is the numerical year count. Pioneering temporal units need convention')
    add('implied_median_announced_project_metric', 160 / .4, 'MtCO2 km/year', 'conditional parameter arithmetic', 'p6 Table2 and prose', 'If the stated40% multiplier alone yields160; source project list not verified')
    zero = saturated_diffusion(9, 3, 0, 160)
    add('zero_growth_total_metric', zero[-1]['cumulative_metric'], 'MtCO2 km/year rated capacity', 'source recurrence without network', 'p4 Eq13/14', 'Pioneering still permits growth at zero theta; no native capacity forecast')
    toy = saturated_diffusion(9, 3, .12, 160)
    add('saturated_final_metric', toy[-1]['cumulative_metric'], 'MtCO2 km/year rated capacity', 'source recurrence without network', 'p4 Eq13/14', 'Exponential reinforcement has no intrinsic logistic saturation; actual demand and other limits can bind')
    add('pooled_history_new_edge_allowance', (1.12 ** 3 - 1) * 100, 'arbitrary metric units', 'analyst two-edge example', 'p4 Eq10', 'History100 on edgeA can support a new edgeB within the same cluster; no pioneering in this example')
    add('new_edge_own_history_allowance', 0, 'arbitrary metric units', 'analyst two-edge example', 'p3 Eq8 versus p4 Eq10', 'Separate edgeB with no history/pioneering cannot grow under the own-edge rule')
    add('retired_asset_knowledge', knowledge([100,0,0,0],3,3,0), 'arbitrary metric units', 'analyst Eq9 example', 'p4 Eq9; p6 Table2', 'Knowledge is not tied to surviving physical capacity when depreciation is zero')
    add('retired_asset_physical_capacity', surviving_capacity([100,0,0,0],3,3,3), 'arbitrary metric units', 'analyst Eq3 example', 'p3 Eq3', 'Three-year asset is retired; this is a distinction, not a source inconsistency')
    add('body_gap_fraction', 100 * t['body_gap_Mt'] / t['target_Mt'], '%', 'printed arithmetic', 'p7 Section4.2', '4.8/53 approximately9%; gap remains conflicting')
    add('caption_gap_fraction', 100 * t['caption_gap_Mt'] / t['target_Mt'], '%', 'printed arithmetic', 'p8 Figure3 caption', '1.7/53 approximately3.2%; do not substitute for body figure')
    add('gap_disagreement', t['body_gap_Mt'] - t['caption_gap_Mt'], 'MtCO2', 'printed arithmetic', 'p7 versus p8', 'Unresolved; no native annual arrays')
    possible = [.7, .85, .15]
    add('hypothetical_unweighted_gap', sum(possible), 'MtCO2/year rate sum', 'analyst weighting example', 'p8 Figure4 caption; p3 Eq2', 'Illustrates possibility only; not digitized or recovered author data')
    add('hypothetical_weighted_gap', sum(a*b for a,b in zip(possible,[3,3,1])), 'MtCO2', 'analyst weighting example', 'p8 Figure4 caption; p3 Eq2', 'Can equal4.8 when unweighted rate sum is1.7; does not establish the explanation')
    add('alternative_modes_emissions_vs_body_gap', 100 * .2 / 4.8, '%', 'printed arithmetic', 'p10 Section5', '200kt/4.8Mt below5%; not the complete incremental lifecycle balance')
    add('alternative_modes_emissions_vs_caption_gap', 100 * .2 / 1.7, '%', 'conditional conflicting-denominator check', 'p8 caption; p10', 'Exceeds5% if1.7 is used; neither conflict repaired')
    add('pipeline_lengths_total', 843 + 1700 + 945, 'km', 'printed arithmetic', 'p6 Section4.1', 'Different domestic/cross-border/offshore classes; not verified corridors')
    add('offshore_capacity_multiplier', 1710 / 1000, 'ratio', 'Table1 arithmetic', 'p6 Table1', '1.71 agrees with distance and variable-cost multipliers')
    add('offshore_distance_multiplier', 171000 / 100000, 'ratio', 'Table1 arithmetic', 'p6 Table1', 'No source or price-year validation')
    add('offshore_variable_multiplier', 13.68 / 8, 'ratio', 'Table1 arithmetic', 'p6 Table1', 'Adjustment source remains unverified')
    add('cost_ratio_using_rounded_percentages', 100 * (1.34 / 1.05 - 1), '%', 'printed rounded ratio check', 'p9 Section4.4', '27.62%; independently rounded34%,5%,27% can be compatible')
    add('rounded_ratio_lower', 100 * (1.335 / 1.055 - 1), '%', 'conditional nearest-integer-percent intervals', 'p9', 'Overlap with a rounded27% ratio exists; do not label a proven error')
    add('rounded_ratio_upper', 100 * (1.345 / 1.045 - 1), '%', 'conditional nearest-integer-percent intervals', 'p9', 'Exact costs required for tighter comparison')
    for cap in (1000,2000):
        cost = pipeline_capex(cap,100,1000,100000)
        add(f'pipeline_capex_{cap}ktpy_100km', cost, 'EUR raw CAPEX', 'analyst Eq7/Table1 case', 'p3 Eq7; p6 Table1', 'No annuity, utilities, construction or storage costs')
        add(f'pipeline_capex_per_tpy_{cap}', cost/(cap*1000), 'EUR/(tCO2/year rated)', 'analyst Eq7/Table1 case', 'p3 Eq7; p6 Table1', 'Fixed distance offset creates scale effects; not EUR/tCO2 actually stored')
    add('conditional_minimum_flow_1000ktpy', .6 * 1000, 'ktCO2/year', 'analyst60% convention', 'p6 Section3.2', 'Minimum active-flow and shutoff implementation delegated to code/SI')
    for name,x in [('cheap_slack',penalty_example(6,5)),('expensive_slack',penalty_example(6,7))]:
        add(f'{name}_service',x['service'],'units','analyst independent LP','p3 Eq1/6','Finite penalty can sacrifice a feasible target unless calibrated against marginal service cost')
        add(f'{name}_slack',x['slack'],'units','analyst independent LP','p3 Eq1/6','No claim about the native penalty value, which is missing from the main PDF')
    for capture in (.99,.9):
        add(f'feed_for_one_stored_capture{capture}', 1/capture, 'MtCO2/year source feed', 'analyst fixed-target no-loss case', 'p5 Section3.1', 'Lower capture increases required feed; fixed stored throughput remains1. Gathering topology may change')
    for mode in data['transport_costs']:
        add(f"{mode['mode']}_variable_per_t_km", mode['variable_EUR_per_kt_km']/1000,
            'EUR/(tCO2 km)', 'Table1 unit conversion', 'p6 Table1', 'Only the variable transport cost; no full utility inventory')
    add('raw_tonne_cost_example', 3.2e9/53e6,'EUR/tCO2','analyst denominator example','p9 Figure6','3.2billionEUR is an illustrative value, not extracted exact cost; figure denominator undisclosed')
    add('discounted_final_tonne_cost_example',3.2e9/(53e6*1.06**-24),'EUR/discounted tCO2','analyst denominator example','p3 Eq2; p9 Figure6','Same raw tonnes can give a different discounted denominator; no native levelized cost inferred')
    return rows, toy


def main():
    data = load_inputs(); checks, trajectory = calculate(data)
    OUT.mkdir(parents=True,exist_ok=True)
    for name,rows in [('B2-05_checks.csv',checks),('B2-05_diffusion_example.csv',trajectory)]:
        with (OUT/name).open('w',newline='',encoding='utf-8') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    result=dict(study_id='B2-05',checks=len(checks),synthetic_diffusion_rows=len(trajectory),
                native_Swiss_ZEN_garden_model_reproduced=False,public_code_and_SI_verified=False,
                pressure_constrained_storage_or_complete_utility_inventory=False,
                accepted_operating_GHG_inputs_changed=False,
                body_gap_Mt=4.8,caption_gap_Mt=1.7,
                resolution='unresolved; weighting explanation is hypothetical, not recovered data',
                source_sha256=data['source']['sha256'])
    (OUT/'B2-05_reconciliation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
