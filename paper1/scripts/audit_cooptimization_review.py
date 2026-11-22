#!/usr/bin/env python3
"""B2-07 bookkeeping and disclosed analyst schematic checks only.

This does not reproduce database selection, any cited author model, project
operation, trained controller or quantum benchmark. It changes no accepted
operating or GHG input.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/comprehensive_review'


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B2-07.json').read_text())
    for source in [data['source'], *data['cited_sources']]:
        if hashlib.sha256((ROOT / source['path']).read_bytes()).hexdigest() != source['sha256']:
            raise ValueError(f"Source changed: {source['path']}")
    return data


def schematic_milp(demand=None, sink_link=False):
    """Analyst S->H->K graph under only the static displayed constraint classes.

    Variables: capture binary, two build binaries, two arc flows, injection.
    Optional demand and sink-inflow equality are separately labelled variants;
    neither is attributed to the compact source display or unavailable code.
    """
    if demand is not None and demand < 0:
        raise ValueError('Nonnegative analyst demand required')
    matrix = [
        [0, 0, 0, 1, -1, 0],  # hub conservation
        [-5, 0, 0, 1, 0, 0],  # capture activation
        [0, -5, 0, 1, 0, 0],  # first arc capacity
        [0, 0, -5, 0, 1, 0],  # second arc capacity
    ]
    lower = [0, -np.inf, -np.inf, -np.inf]
    upper = [0, 0, 0, 0]
    if sink_link:
        matrix.append([0, 0, 0, 0, 1, -1])
        lower.append(0); upper.append(0)
    if demand is not None:
        matrix.append([0, 0, 0, 0, 0, 1])
        lower.append(demand); upper.append(np.inf)
    result = milp(
        [10, 5, 5, 1, 1, 1], integrality=[1, 1, 1, 0, 0, 0],
        bounds=Bounds(np.zeros(6), [1, 1, 1, np.inf, np.inf, 10]),
        constraints=LinearConstraint(matrix, lower, upper),
    )
    if not result.success:
        raise ValueError('Analyst schematic is infeasible: ' + result.message)
    return result


def cumulative_mass(rates, durations):
    if len(rates) != len(durations) or not rates or min(durations) <= 0 or min(rates) < 0:
        raise ValueError('Compatible nonnegative rates and positive durations required')
    return math.fsum(q * dt for q, dt in zip(rates, durations))


def present_value(capital, annual_cost, rate, years):
    if years < 1 or rate <= -1:
        raise ValueError('Positive years and discount rate above -1 required')
    return capital + annual_cost * math.fsum((1 + rate) ** -t for t in range(1, years + 1))


def robust_comparison(costs):
    """Finite static decisions versus a distinct perfect-information comparator."""
    costs = np.asarray(costs, dtype=float)
    if costs.ndim != 2 or not costs.size or not np.isfinite(costs).all():
        raise ValueError('Finite decision-by-scenario matrix required')
    return float(costs.max(axis=1).min()), float(costs.min(axis=0).max())


def calculate(data):
    rows = []

    def add(item, value, unit, basis, locator, interpretation):
        rows.append(dict(item=item, value=value, unit=unit, basis=basis,
                         source_locator=locator, interpretation=interpretation))

    s = data['screening']
    identities = {
        'identified': (s['WoS'] + s['Scopus'] + s['registers'], s['before_deduplication']),
        'deduplicated': (s['before_deduplication'] - s['duplicates'], s['screened']),
        'fulltext_sought': (s['screened'] - s['abstract_excluded'], s['reports_sought']),
        'fulltext_assessed': (s['reports_sought'] - s['not_retrieved'], s['assessed']),
        'fulltext_exclusion_reasons': (sum(s['reasons'].values()), s['fulltext_excluded']),
        'included': (s['assessed'] - s['fulltext_excluded'], s['included_reports']),
        'studies_reports': (s['included_reports'], s['included_studies']),
    }
    for name, (computed, reported) in identities.items():
        add(name + '_residual', computed - reported, 'count', 'reported bookkeeping',
            'pp3–6 Figure2', 'Zero verifies arithmetic only, not database selection or eligibility')
    for name, numerator, denominator in [
        ('duplicate_share', s['duplicates'], s['before_deduplication']),
        ('abstract_exclusion_share', s['abstract_excluded'], s['screened']),
        ('fulltext_inclusion_share', s['included_studies'], s['assessed']),
        ('screened_inclusion_share', s['included_studies'], s['screened']),
    ]:
        add(name, 100 * numerator / denominator, 'percent', 'reported count ratio',
            'pp3–6', 'Descriptive ratio, not sensitivity, precision or probability of completeness')
    add('reason_share_sum', sum(100 * v / s['fulltext_excluded'] for v in s['reasons'].values()),
        'percent', 'reported count ratio', 'p6', 'One primary reason per excluded report as stated')
    g = data['graph']; stock = sum(g['sink_stocks_Mt']); flow = sum(g['source_rates_Mtpy'])
    add('figure8_source_rate', flow, 'MtCO2/year', 'printed schematic sum', 'p15 Figure8', 'Illustration, not measured source or injection service')
    add('figure8_resource_stock', stock, 'MtCO2', 'printed schematic sum', 'p15 Figure8', 'Stock is not an annual injection bound')
    add('figure8_aggregate_stock_rate_ratio', stock / flow, 'years', 'conditional schematic ratio', 'p15 Figure8', 'No per-sink injectivity, allocation, availability or retention inferred')
    for diameter in g['diameters_inch']:
        add(f'diameter_{diameter}_inch', diameter * .0254, 'm', 'unit conversion', 'p15 Figure8', 'Diameter alone does not determine flow capacity or safe pressure')
    project = data['project_snapshot']
    add('Iowa_length_conversion', project['Summit_Iowa_miles'] * 1.609344, 'km', 'dated reported unit conversion', 'p13 Table4', 'Iowa proposed filing scope at source audit date, not current whole-project length')
    add('Porthos_nominal_stock_rate_ratio', project['Porthos_stock_Mt'] / project['Porthos_rate_Mtpy'], 'years', 'conditional dated ratio', 'p13 Table4', 'Not a verified operational life, yearly service or commercial allocation')
    add('Northern_Lights_expansion_ratio_lower', project['Northern_Lights_expansion_lower_Mtpy'] / project['Northern_Lights_phase1_Mtpy'], 'ratio', 'dated reported ratio', 'p13 Table4', 'Lower-bound nominal expansion ratio, not observed performance')
    add('Li_source_sink_pair_count', project['Li_sources'] * project['Li_sinks'], 'pairs', 'possible Cartesian size only', 'pp13,18', 'Not a recovered candidate-arc count or a complexity lower bound')
    c = data['compute']; cap = c['Bogs_cap_h'] * 3600
    add('Bogs_cap', cap, 'seconds', 'reported unit conversion', 'p18 Table6', 'Maximum reported runtime may be below a cap')
    add('Bogs_runtime_below_cap', cap - c['Bogs_runtime_s'][1], 'seconds', 'reported arithmetic', 'p18 Table6', '300 seconds below the cap is compatible, not a discrepancy')
    for i, (error, hours) in enumerate(zip(c['PWL_errors_percent'], c['PWL_runtime_h']), 1):
        add(f'PWL_runtime_segments_{i}', hours * 3600, 'seconds', 'reported unit conversion', 'p18 Table6 footnote', 'Different approximation and compute cases, not a controlled method ranking')
        add(f'PWL_error_reduction_segments_{i}', 100 * (1 - error / c['PWL_errors_percent'][0]), 'percent relative', 'reported arithmetic', 'p18 Table6 footnote', 'Approximation error change, not solver optimality gap or net climate gain')
    for label, demand, link in [('literal_classes', None, False), ('added_demand_only', 3, False), ('added_demand_and_sink_link', 3, True)]:
        result = schematic_milp(demand, link)
        add('toy_objective_' + label, float(result.fun), 'analyst cost units', 'analyst independent MILP', 'pp15–16 illustrative classes', 'Not the authors’ optimization or a corrected native solution')
        add('toy_arc_flow_' + label, float(result.x[3]), 'analyst flow units', 'analyst independent MILP', 'pp15–16', 'All added target/link assumptions are explicit in the variant label')
        add('toy_injection_' + label, float(result.x[5]), 'analyst flow units', 'analyst independent MILP', 'pp15–16', 'Unlinked injection shows an incomplete illustration, not a native-code defect')
    add('compact_allocation_without_arc_flow', int(1 <= 1 and 0 <= 0 and 1 == sum([1])), 'boolean', 'analyst compact-display fixture', 'p12', 'q=a=b=1, E=I=1, f=y=0 satisfies the displayed totals without a delivery link')
    mass = cumulative_mass([3, 3], [2, 2])
    add('toy_integrated_injection', mass, 'MtCO2', 'analyst rate-stock example', 'pp15–16', '3 Mt/year for four years gives 12 Mt, exceeding a hypothetical 10 Mt resource')
    add('toy_literal_rate_stock_test', int(3 <= 10), 'boolean', 'analyst literal numeric comparison', 'p16', 'A rate-stock number comparison passes despite the integrated mass excess')
    add('toy_resource_feasible_after_integration', int(mass <= 10), 'boolean', 'analyst mass comparison', 'p16', 'Separate dimensionally consistent check; no source value repaired')
    add('toy_lifetime_PV', present_value(100, 6, .08, 10), 'analyst currency units', 'analyst cost-time example', 'pp15–16', '100 capital and 6 annual cost at analyst 8% over ten years, not source costing')
    add('toy_capital_plus_one_year', 106, 'analyst currency units', 'analyst cost-time example', 'pp15–16', 'Needs a common time convention before comparison with lifetime PV')
    events = [1, 0, 0]; active = np.cumsum(events)
    add('toy_persistent_capacity_all_years', int(all(5 <= 5 * n for n in active)), 'boolean', 'analyst commissioned-stock comparison', 'p16', 'A separately supplied stock equation preserves an asset; delta-y alone is an event')
    add('toy_event_only_capacity_all_years', int(all(5 <= 5 * n for n in events)), 'boolean', 'analyst event-only comparison', 'p16', 'Different capacity linkage rejects later service; neither is asserted native code')
    static, perfect = robust_comparison([[0, 10], [10, 0]])
    add('toy_static_robust_cost', static, 'analyst cost units', 'analyst finite enumeration', 'p16', 'One decision before uncertainty; no probabilities or CCUS calibration')
    add('toy_perfect_information_cost', perfect, 'analyst cost units', 'analyst distinct comparator', 'p16', 'Decision after complete information, not automatically implementable recourse')
    return rows


def main():
    data = load_inputs(); rows = calculate(data); OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / 'B2-07_checks.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    result = dict(study_id='B2-07', source_sha256=data['source']['sha256'], checks=len(rows),
                  database_search_and_selection_reproduced=False,
                  native_cited_optimizer_physics_or_learning_model_reproduced=False,
                  complete_utility_or_pressure_constrained_service=False,
                  accepted_operating_GHG_inputs_changed=False,
                  scope='Reported arithmetic and explicitly disclosed analyst examples only')
    (OUT / 'B2-07_reconciliation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
