#!/usr/bin/env python3
"""B2-02 learning-curve components and unit diagnostics, not DAC/IAM forecasts.

No full author TEA, LCA, coupling algorithm, reservoir or cited model reproduced.
The Eq2 summation and literal expanded denominator are evaluated separately.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B2-02.json').read_text())
    if hashlib.sha256((ROOT / data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale prospective-assessment source')
    return data


def learning_exponent(rate):
    """Invert Eq1 on the explicitly selected nonnegative-learning domain."""
    if not math.isfinite(rate) or not 0 <= rate < 1:
        raise ValueError('Selected learning domain requires finite 0 <= LR < 1')
    return -math.log1p(-rate) / math.log(2)


def component_cost(initial_cost, initial_capacity, capacity, rate):
    if not all(math.isfinite(v) for v in (initial_cost, initial_capacity, capacity)):
        raise ValueError('Finite costs and capacities required')
    if initial_cost < 0 or initial_capacity <= 0 or capacity <= 0:
        raise ValueError('Nonnegative cost and positive capacities required')
    return initial_cost * (capacity / initial_capacity) ** (-learning_exponent(rate))


def costs(case, capacities):
    c0, x0, lr = (case[k] for k in ('initial_costs', 'initial_capacities', 'learning_rates'))
    if not len(c0) == len(x0) == len(lr) == len(capacities) or len(c0) != 2:
        raise ValueError('This literal-expansion diagnostic is a two-component example')
    intended = sum(component_cost(c, x, t, r) for c, x, t, r in zip(c0, x0, capacities, lr, strict=True))
    # Preserve the printed x01 in the second expanded term; do not silently fix it.
    expanded = sum(component_cost(c, x0[0], t, r) for c, t, r in zip(c0, capacities, lr, strict=True))
    return intended, expanded


def calculate(data):
    rows = []

    def add(item, value, unit, source, status, scope):
        rows.append(dict(item=item, value=value, unit=unit, source=source, status=status, scope=scope))

    for typ in data['typology_learning_rates']:
        rate = typ['mean']; name = f'type{typ["type"]}'
        add(name + '_exponent', learning_exponent(rate), 'dimensionless', 'Eq1 and typology p9',
            'printed_learning_component', 'No distribution, component assignment, deployment path or author forecast inferred.')
        for doublings in (1, 8):
            add(name + f'_factor_after_{doublings}_doublings', component_cost(1, 1, 2**doublings, rate),
                'cost ratio', 'Eq1–2 p9', 'printed_learning_component',
                'Conditional constant-rate mathematical component, not calendar-based technology cost.')
    case = data['analyst_case']
    for name, capacities in [('initial', case['initial_capacities']), ('future', case['future_capacities'])]:
        intended, expanded = costs(case, capacities)
        add('analyst_' + name + '_summation', intended, 'arbitrary consistent cost', 'Eq2 p9; disclosed synthetic case',
            'analyst_algebra_counterexample', case['scope'])
        add('analyst_' + name + '_literal_expansion', expanded, 'arbitrary consistent cost', 'Eq2 p9; second denominator x01',
            'HOLD_EXPANDED_DENOMINATOR', 'Literal expansion differs from summation for unequal initial capacities; no author software defect inferred.')
        add('analyst_' + name + '_expansion_minus_sum', expanded-intended, 'arbitrary consistent cost', 'Eq2 p9',
            'HOLD_EXPANDED_DENOMINATOR', case['scope'])
    for row in data['table1']:
        literal = row['xt_MtCO2_literal']
        if ',' in literal:
            continue  # Preserve ambiguous 1,4; neither a decimal nor two cases invented.
        add(row['id'] + '_same_unit_capacity_ratio', float(literal) * 1e6 / row['x0_tCO2'],
            'dimensionless', 'Table1 p10; x0 tCO2 versus xt MtCO2', 'conditional_header_unit_conversion',
            'Only if both columns denote the same cumulative-capacity basis. No calendar, annual rate, net-removal or projected-cost validation.')
    return rows


def curve(data):
    return [dict(technology_type=t['type'], source_mean_LR=t['mean'], capacity_doublings=k,
                 capacity_ratio=2**k, cost_factor=component_cost(1, 1, 2**k, t['mean']),
                 scope='dimensionless_learning_component_only_not_author_DAC_or_IAM_forecast')
            for t in data['typology_learning_rates'] for k in range(9)]


def write_csv(path, rows):
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def main():
    data = load_inputs(); rows = calculate(data); points = curve(data)
    out = ROOT / 'outputs/comprehensive_review'; out.mkdir(parents=True, exist_ok=True)
    write_csv(out / 'B2-02_checks.csv', rows)
    write_csv(out / 'B2-02_learning_components.csv', points)
    result = dict(study_id='B2-02', source_sha256=data['source_sha256'], checks=len(rows), component_rows=len(points),
                  reconstructed='Eq1 and Eq2 summation components; literal expanded-form counterexample',
                  native_DAC_cost_LCA_IAM_or_feedback_model_reproduced=False,
                  original_source_verification=False, supplement_availability_verified=False,
                  accepted_inputs_changed=False, missing=data['missing'])
    (out / 'B2-02_reconciliation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
