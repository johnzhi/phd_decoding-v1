#!/usr/bin/env python3
"""B1-14 limited objective/unit/arrival checks and analyst physical identities.

Neither the native forward models nor the double-regularised inversion is
reproduced. Archie examples refer to homogeneous true bulk resistivity, never
the measured nonlocal apparent-resistivity ratios. Radial skin examples are
conditional Darcy counterexamples, not inferred field controls or annual rates.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B1-14.json').read_text())
    if hashlib.sha256((ROOT / data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale Ketzin source')
    edge = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B1-14_citation_checks.json').read_text())
    if hashlib.sha256((ROOT / edge['cited_path']).read_bytes()).hexdigest() != edge['cited_sha256']:
        raise ValueError('Stale Class2015 primary check')
    return data


def cost_reduction(initial, inverted):
    if initial <= 0 or inverted < 0:
        raise ValueError('Positive initial and nonnegative inverted cost required')
    return 100 * (1 - inverted / initial)


def cost_root_indicator(cost, restore_factor=1):
    if cost < 0 or restore_factor <= 0:
        raise ValueError('Nonnegative cost and positive scaling required')
    return math.sqrt(cost * restore_factor)


def archie_index(brine_saturation, exponent):
    if not 0 < brine_saturation <= 1 or exponent <= 0:
        raise ValueError('Homogeneous two-phase identity requires Sw in(0,1] and n>0')
    return brine_saturation**(-exponent)


def archie_gas_from_true_index(resistivity_index, exponent):
    if resistivity_index < 1 or exponent <= 0:
        raise ValueError('True homogeneous index must be>=1; do not discard apparent data<1')
    return 1 - resistivity_index**(-1 / exponent)


def radial_skin(clean_k, zone_k, zone_radius, well_radius):
    if min(clean_k, zone_k, zone_radius, well_radius) <= 0 or zone_radius <= well_radius:
        raise ValueError('Positive permeabilities and rs>rw required')
    return (clean_k / zone_k - 1) * math.log(zone_radius / well_radius)


def radial_pressure_factor(log_term, skin):
    if log_term <= 0 or log_term + skin <= 0:
        raise ValueError('Positive radial resistance required')
    return (log_term + skin) / log_term


def calculate(data):
    rows = []

    def add(item, value, unit, locator, interpretation, status='limited_source_arithmetic'):
        rows.append(dict(item=item, value=value, unit=unit, source_locator=locator,
                         calculation_status=status, interpretation=interpretation,
                         scope='not_native_hydraulic_multiphase_ERT_inverse_or_accepted_service_retention_GHG_model'))

    for group in data['objective_groups']:
        name = group['group']
        reduction = cost_reduction(group['initial'], group['inverted'])
        add(name + '_objective_reduction', reduction, '% of initial observation cost', 'Table1 p5',
            'Weighted, normalised objective change; not raw measurement error, explained variance, capacity or safety improvement.')
        add(name + '_reduction_minus_printed', reduction - group['reported_reduction_percent'], 'percentage points', 'Table1 p5',
            'Printed whole-percent reductions remain unchanged. Source objective entries have coarse display precision.')
        add(name + '_table_cost_root', cost_root_indicator(group['inverted']), 'normalised cost-root indicator', 'Table1 / Section4.2 p5',
            'Do not label this a raw relative pressure/resistivity error without PartI normalisation and weights.', 'conditional_objective_normalisation')
    ert = next(group for group in data['objective_groups'] if group['group'] == 'geoelectrical')
    for phase in ('initial', 'inverted'):
        restored = ert[phase] * ert['objective_restore_factor']
        add('ERT_' + phase + '_restored_objective', restored, 'objective after source factor10 restoration', 'Section4.2 / Table1',
            'Prose explicitly instructs multiplying objective by10 for comparison. Not changing accepted data or refitting the inversion.', 'conditional_objective_normalisation')
        add('ERT_' + phase + '_restored_cost_root', cost_root_indicator(ert[phase], ert['objective_restore_factor']),
            'normalised cost-root indicator; not raw percent error', 'Section4.2 / Table1',
            'Root scales sqrt10, not10. Actual physical error distribution remains unknown.', 'conditional_objective_normalisation')
    add('ERT_root_indicator_restore_ratio', math.sqrt(ert['objective_restore_factor']), 'ratio', 'Section4.2 p5',
        'Objective-scale versus residual-scale distinction; no inferred raw ERT uncertainty.', 'conditional_objective_normalisation')
    total = data['objective_total']
    for phase in ('initial', 'inverted'):
        group_sum = sum(group[phase] for group in data['objective_groups'])
        half_width = sum(group[phase + '_display_step'] / 2 for group in data['objective_groups'])
        reported_half = total[phase + '_display_step'] / 2
        overlap = max(group_sum - half_width, total[phase] - reported_half) <= min(group_sum + half_width, total[phase] + reported_half)
        for suffix, value, unit in [('group_sum', group_sum, 'observation objective'),
                                    ('group_sum_minus_reported', group_sum - total[phase], 'objective DIFFERENCE'),
                                    ('conditional_rounding_overlap', int(overlap), 'boolean0/1')]:
            add(phase + '_' + suffix, value, unit, 'Table1 p5',
                'Nearest displayed precision only, not measurement uncertainty. Inverted sum.0954 versus reported.094 is rounding-compatible; no correction adopted.',
                'conditional_display_rounding_check')
    add('reported_total_observation_cost_reduction', cost_reduction(total['initial'], total['inverted']), '% of initial reported cost', 'Table1',
        'Observation cost only; full regularisation and native loss are not reproduced.')
    add('printed_component_observation_cost_reduction', cost_reduction(sum(g['initial'] for g in data['objective_groups']), sum(g['inverted'] for g in data['objective_groups'])),
        '% of initial component sum', 'Table1', 'A different rounded aggregate; both round about80%. Not a physical performance metric.')

    relative_errors = []
    for entry in data['arrivals']:
        difference = entry['modelled_days'] - entry['observed_days']
        percent = difference / entry['observed_days'] * 100
        relative_errors.append(percent / 100)
        for suffix, value, unit in [('day_error', difference, 'days'), ('relative_error', percent, '% of observed detection time'),
                                    ('relative_error_minus_printed', percent - entry['reported_deviation_percent'], 'percentage points')]:
            add(entry['well'] + '_' + suffix, value, unit, 'Table2 p6',
                'Sensor detection includes well/completion delays; displayed rounding is not observational uncertainty or validation of the3% model threshold.')
    add('analyst_unweighted_RMS_relative_arrival_error', math.sqrt(sum(x*x for x in relative_errors) / len(relative_errors)),
        'dimensionless unweighted relative RMS', 'Table2 / analyst metric',
        'Not the reported arrival objective: PartI residual scales/covariance and weights are unavailable.', 'analyst_metric_not_author_objective')

    monitoring = data['monitoring']
    product = monitoring['retained_configurations'] * monitoring['days_per_series']
    for item, value, unit in [('ERT_processed_ratio_count', product, 'processed ratios'),
                              ('ERT_count_minus_printed', product - monitoring['total_ERT_ratios'], 'count DIFFERENCE'),
                              ('ERT_retained_configuration_fraction', monitoring['retained_configurations'] / monitoring['candidate_configurations'], 'fraction of candidate configurations'),
                              ('ERT_removed_configurations', monitoring['candidate_configurations'] - monitoring['retained_configurations'], 'configurations'),
                              ('hydraulic_nominal_pair_count', monitoring['hydraulic_wells'] * monitoring['hydraulic_tests'], 'well-test pairs'),
                              ('hydraulic_retained_pair_count', len(monitoring['retained_pairs']), 'pairs'),
                              ('hydraulic_excluded_pair_count', len(monitoring['excluded_pairs']), 'pairs'),
                              ('pressure_static_correction_depth_interval', monitoring['pressure_reference_depth_m'] - monitoring['pressure_sensor_depth_m'], 'm'),
                              ('nominal_display_to_raw_CO2_interval_ratio', monitoring['display_CO2_pressure_interval_min'] * 60 / monitoring['raw_CO2_acquisition_s'], 'time-interval ratio')]:
        add(item, value, unit, 'Sections2.1–2.3 / Figures5–7',
            'Counts and units only. Not independent samples, verified logger failures, exact resampling operation or a computed gas-column pressure correction.')
    core = data['core']
    height_cm, radius_cm = core['height_mm'] / 10, core['radius_mm'] / 10
    for item, value, unit in [('core_prose_height', height_cm, 'cm'), ('core_prose_radius', radius_cm, 'cm'),
                              ('core_prose_bulk_cylinder_volume', math.pi * radius_cm**2 * height_cm, 'cm3 bulk cylinder')]:
        add(item, value, unit, 'Section2.3.3 / Figure1 p3',
            'Prose geometry conversion only, not pore volume, lab saturation, a corrected graphic scale or a native FEM reproduction.')
    add('calibrated_n_position_within_source_bounds', (core['calibrated_n'] - core['calibration_n_bounds'][0]) / (core['calibration_n_bounds'][1] - core['calibration_n_bounds'][0]),
        'normalised bound position', 'Section4.1.2 p4',
        'Exactly at lower bound; not independent measurement or posterior certainty.')
    for exponent in core['calibration_n_bounds']:
        for sw in data['analyst_examples']['Archie_brine_saturations']:
            add(f'analyst_Archie_n{exponent:g}_Sw{sw:g}_true_index', archie_index(sw, exponent), 'true homogeneous bulk resistivity index',
                'Section2.3.3 / analyst Archie identity',
                'Two-phase, constant conductivity/surface/P/T assumptions. Not an inversion of nonlocal field apparent resistivity.', 'analyst_homogeneous_Archie_example')
        for index in data['analyst_examples']['Archie_resistivity_ratios']:
            add(f'analyst_Archie_n{exponent:g}_R{index:g}_gas_saturation', archie_gas_from_true_index(index, exponent), 'gas fraction in homogeneous EXAMPLE',
                'Figure2 / analyst identity', 'Different exponents imply different saturations even at the same true ratio. No field saturation or image-derived gas volume inferred.',
                'analyst_homogeneous_Archie_example')
    skin = data['skin']
    clean_k = skin['nearwell_permeability_mD'] * skin['reduction_factor_approx']
    add('conditional_implied_clean_comparison_permeability', clean_k, 'mD if approximate source factor treated exactly', 'Section4.1.2 p4',
        '15 times8 only; not a measured field-wide intrinsic permeability or accepted flow-model input.', 'conditional_source_equivalence_algebra')
    implied_rw = skin['zone_radius_m'] * math.exp(-skin['calibrated'] / (skin['reduction_factor_approx'] - 1))
    add('analyst_two_zone_implied_well_radius', implied_rw, 'm conditional example', 'source1m/15mD/factor8/skin10.1 / analyst radial identity',
        'Solve an ideal two-zone steady Darcy identity. Actual rw is missing and remains null; no geometric repair or native gas model reproduced.', 'analyst_radial_geometry_example')
    add('analyst_log_term_for_doubled_pressure', skin['calibrated'], 'dimensionless radial log term', 'analyst fixed-state radial comparison',
        'Exactly2× requires L=s under this ideal identity; no actual far boundary/transient radius inferred.', 'analyst_radial_geometry_example')
    for log_term in data['analyst_examples']['radial_log_terms']:
        pressure_factor = radial_pressure_factor(log_term, skin['calibrated'])
        add(f'analyst_L{log_term:g}_fixed_rate_pressure_factor', pressure_factor, 'pressure ratio', 'analyst radial Darcy identity',
            'Same local permeability contrast/skin yields different pressure ratios as geometry changes. Not actual pressure, phase mobility, capacity or annual service.', 'analyst_radial_counterexample')
        add(f'analyst_L{log_term:g}_fixed_margin_rate_factor', 1 / pressure_factor, 'rate ratio under fixed-state pressure-margin EXAMPLE', 'analyst radial Darcy identity',
            'Conditional single-state steady flow only. Factor8 local permeability loss does not equal8fold annual-rate loss; no operating/GHG factor adopted.', 'analyst_radial_counterexample')
    return rows


def main():
    data = load_inputs()
    rows = calculate(data)
    output = ROOT / 'outputs/comprehensive_review'
    with (output / 'B1-14_checks.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    result = dict(study_id='B1-14', source_sha256=data['source_sha256'], check_count=len(rows), figures=8, tables=2,
                  numbered_source_equations=0, scoped_primary_citation_edges=1, native_models_reproduced=False,
                  accepted_inputs_changed=False, missing=data['missing'],
                  source_skin_geometry=dict(well_radius_m=data['skin']['well_radius_m'], far_radius_m=data['skin']['far_radius_m']),
                  interpretation='Limited objective/arrival/unit checks and analyst Archie/radial identities only. No native joint inversion, corrected field saturation, universal rate penalty, annual maximum service, safety probability or retained-carbon/GHG result.')
    (output / 'B1-14_reconciliation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
