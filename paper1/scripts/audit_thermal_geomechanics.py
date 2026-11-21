#!/usr/bin/env python3
"""B1-11 literal table/algebra checks with explicit missing field inputs.

Pressure-rule replays assume compatible pressure references and a linear stress
path; they do not validate those assumptions. Analyst elastic, friction and
uplift examples are not author cases or complete field-model reproduction.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B1-11.json').read_text())
    if hashlib.sha256((ROOT / data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale thermal-geomechanics source')
    return data


def check_elastic(nu, young):
    if not -1 < nu < .5 or young <= 0:
        raise ValueError('Example requires stable isotropic elastic constants')


def compliance(nu, young):
    check_elastic(nu, young)
    return (1 - nu - 2 * nu**2) / ((1 - nu) * young)


def horizontal_stress_change(alpha, nu, delta_p):
    check_elastic(nu, 1)
    return alpha * (1 - 2 * nu) / (1 - nu) * delta_p


def margin_rule(current_pressure, caprock_stress, safety_factor):
    if safety_factor <= 0:
        raise ValueError('Safety factor must be positive')
    return current_pressure + (caprock_stress - current_pressure) / safety_factor


def conditional_isothermal_intersection(row):
    beta = ((row['depleted_Sh_psi'] - row['original_Sh_psi']) /
            (row['initial_reservoir_psi'] - row['current_reservoir_psia']))
    critical = (row['depleted_Sh_psi'] + beta * row['current_reservoir_psia']) / (1 + beta)
    return beta, critical


def friction_coefficient_ratio(angle_deg, angle_multiplier):
    return math.tan(math.radians(angle_deg * angle_multiplier)) / math.tan(math.radians(angle_deg))


def bruno_literal(nu, radius, overburden, thickness, displacement):
    """Printed Eq5 with its stated DeltaH=displacement semantics, uncorrected.

    Rationalise the square-root difference to avoid subtractive cancellation.
    The resulting small-displacement response is quadratic, not assumed to be
    the original Bruno implementation or the authors' hidden implementation.
    """
    check_elastic(nu, 1)
    if radius <= 0 or overburden < 0 or thickness <= 0:
        raise ValueError('Positive radius/thickness and nonnegative overburden required')
    roots = math.hypot(radius, overburden + displacement) + math.hypot(radius, overburden)
    root_difference = displacement * (2 * overburden + displacement) / roots
    bracket = displacement - root_difference
    return 2 * (1 - nu) * bracket * displacement / thickness


def calculate(data):
    rows = []

    def add(item, value, unit, locator, interpretation, status='limited_arithmetic'):
        rows.append(dict(item=item, value=value, unit=unit, source_locator=locator,
                         calculation_status=status, interpretation=interpretation,
                         scope='not_full_native_thermal_fault_uplift_retention_or_accepted_GHG_model'))

    factor = data['reported_safety_factor']
    for row in data['seals']:
        seal = row['seal']
        iso, cool = row['isothermal_recommended_psi'], row['cooled_recommended_psi']
        add(seal + '_reported_pressure_pair_drop', iso - cool, 'psi DIFFERENCE', 'Tables2/first3 pp5–6',
            'Reported-pair arithmetic only; not annual mass loss, observed field response or a temperature derivative.')
        add(seal + '_reported_pressure_pair_drop_pct', 100 * (iso - cool) / iso, '% of reported isothermal recommendation', 'pp5–6',
            'Explicit denominator; field thermal derivation and pressure references remain unverified.')
        for case in ('isothermal', 'cooled'):
            replay = margin_rule(row['current_reservoir_psia'], row[case + '_final_Sh_psi'], factor)
            add(seal + '_' + case + '_conditional_margin_rule', replay, 'psi; compatible references ASSUMED', 'pp5–6',
                'Analyst rule Pcurrent+(Sh_after−Pcurrent)/1.5. Mixed psi/psia headers and source implementation unresolved.',
                'conditional_rule_not_native_field_reproduction')
            add(seal + '_' + case + '_printed_minus_margin_rule', row[case + '_recommended_psi'] - replay, 'psi DIFFERENCE', 'pp5–6',
                'SealA cooled residual is about75.33psi. Preserve source values; no replacement is adopted.',
                'conditional_rule_not_native_field_reproduction')
        beta, critical = conditional_isothermal_intersection(row)
        for name, value, unit in [('caprock_stress_path_beta', beta, 'dimensionless'),
                                  ('critical_pressure', critical, 'psi; compatible references ASSUMED'),
                                  ('critical_minus_printed_final_Sh', critical - row['isothermal_final_Sh_psi'], 'psi DIFFERENCE'),
                                  ('recommended_from_intersection', margin_rule(row['current_reservoir_psia'], critical, factor), 'psi')]:
            add(seal + '_conditional_' + name, value, unit, 'Table2 / Eq1 / analyst derivation D02',
                'Infer a linear caprock stress path from depletion, solve P=Sh(P), then apply delta safety factor. '
                'Near agreement is a conditional table-component check, not validation of stress transfer, datum or field physics.',
                'conditional_linear_stress_path_example')

    for method in ('Geertsma', 'Bruno'):
        for quantity in ('expansion', 'uplift'):
            before = data['deformation_tables']['without_degradation'][method][quantity]
            after = data['deformation_tables']['with_degradation'][method][quantity]
            for label, old, new in zip(data['compliance_table']['percentile_labels'], before, after):
                add(f'{method}_{quantity}_{label}_change', new - old, 'm DIFFERENCE', 'secondTable3/Table4 p8',
                    'Printed case labels retained. Other pressure/thickness/geometry changes and joint percentile construction are missing.')
                add(f'{method}_{quantity}_{label}_change_pct', 100 * (new - old) / old, '% of corresponding without-degradation value', 'p8',
                    'Some cases increase; approximately37% decrease is not a universal degradation factor.')
    maximum = max(max(data['deformation_tables']['without_degradation'][m]['uplift']) for m in ('Geertsma', 'Bruno'))
    add('table_maximum_uplift_minus_narrative', maximum - data['narrative_max_uplift_m'], 'm DIFFERENCE', 'p7 narrative / p8 table',
        'Table maximum0.19m differs from adopted0.18m prose; rounding/case identity needs original arrays.')

    example = data['analyst_examples']
    for nu in example['nu_values']:
        original = compliance(nu, example['E_MPa'])
        changed = compliance(nu * example['relative_nu_multiplier'], example['E_MPa'] * example['E_multiplier'])
        add(f'analyst_nu_{nu:g}_compliance_ratio', changed / original, 'ratio', 'Eq3 / stated26%E and10%nu sensitivity',
            'Analyst relative-nu examples at fixed pressure/thickness. E softening and nu increase have opposing effects; '
            'direction depends on base nu. Not native model inputs or an alternative field prediction.', 'analyst_elastic_example')
    delta_total = horizontal_stress_change(example['alpha'], .25, example['delta_p_MPa'])
    add('analyst_pressure_total_stress_change', delta_total, 'MPa', 'Eq1 p5',
        'Analyst alpha=1,nu=.25,DeltaP=10MPa under the printed constrained elastic relation.', 'analyst_sign_example')
    add('analyst_pressure_effective_stress_change', delta_total - example['alpha'] * example['delta_p_MPa'], 'MPa', 'p2 / analyst effective-stress identity',
        'Compression-positive sigmaPrime=sigma−alphaP. Not a reconstructed field stress state.', 'analyst_sign_example')
    add('analyst_fixed_pore_pressure_cooling_effective_change',
        example['cooling_total_stress_change_MPa'] - example['alpha'] * example['fixed_pore_pressure_change_MPa'], 'MPa', 'p2 thermal/effective stress statement',
        'At fixed pore pressure, a decrease in total stress also decreases effective stress in this convention. '
        'The paper’s increase wording needs coupled-pressure/sign clarification; no silent correction.', 'analyst_sign_example')
    for multiplier in data['fault_sensitivity']['friction_angle_multipliers']:
        add(f'analyst_angle_multiplier_{multiplier:g}_coefficient_ratio',
            friction_coefficient_ratio(example['friction_angle_deg'], multiplier), 'tan(angle) ratio', 'fault sensitivity pp6–7',
            'Reducing the angle by10/20% is not the same as reducing tan(angle) by10/20%. Actual fault angles are unavailable.',
            'analyst_friction_example')

    nu = .25
    radius, depth, thickness, disp = [example[k] for k in ('bruno_R_m', 'bruno_D_m', 'bruno_H_m', 'displacement_m')]
    literal = bruno_literal(nu, radius, depth, thickness, disp)
    upper = 2 * (1 - nu) * disp**2 / thickness
    for key, value, unit in [('literal_Bruno', literal, 'm'), ('literal_Bruno_upper_bound', upper, 'm'),
                              ('literal_double_displacement_ratio', bruno_literal(nu, radius, depth, thickness, 2 * disp) / literal, 'ratio')]:
        add('analyst_' + key, value, unit, 'Eq5 p7 / D03',
            'Printed DeltaH interpreted as stated displacement; analyst geometry only. Quadratic small-displacement scaling '
            'requires original notation/implementation verification, not a repaired author model.', 'analyst_literal_notation_example')
    add('analyst_Geertsma_signed_example', -2 * (1 - nu) * .5 * disp, 'm SIGNED', 'Eq4 p7',
        'Analyst integralA=.5 and displacement+.19m give negativeS; table reports positive magnitudes. '
        'Method sign definitions require reconciliation.', 'analyst_literal_notation_example')
    for key in ('sonic_DTS', 'pressure_data_asterisk', 'wellbore_images', 'daily_drilling_reports'):
        add('table1_available_' + key, sum(data['well_audit']['availability'][key]), 'wells WITH checkmark', 'Table1 p4',
            'Availability symbols are not measurements, quality scores or supplied native records. ECD is assumed and noXLOT supplied.')
    for key, value in data['missing_inputs'].items():
        add(key, value, 'MISSING', 'pp3–8',
            'Missing native inputs prevent full thermal/fault/deformation reproduction or regional service/retention calibration.',
            'not_computable_missing_author_inputs')
    return rows


def main():
    rows = calculate(load_inputs())
    target = ROOT / 'outputs/comprehensive_review/B1-11_diagnostics.csv'
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    print(f'{len(rows)} limited checks; full native thermal, fault and uplift cases remain unreproduced.')


if __name__ == '__main__':
    main()
