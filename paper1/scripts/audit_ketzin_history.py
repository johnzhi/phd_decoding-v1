#!/usr/bin/env python3
"""Evaluate B1-15's printed constitutive components and limited diagnostics.

No native ECLIPSE, DuMux or iTOUGH2 model is reproduced. Literal expressions
are preserved; no clipping rule, pressure-gradient correction, raw history,
posterior, safe annual service or retention factor is invented.
"""
import csv
from datetime import date, timedelta
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B1-15.json').read_text())
    if hashlib.sha256((ROOT / data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale Class2015 source')
    return data


def phase_kr(sw, setup, nw=None, ng=None):
    """Literal Eq1 on the common physical real domain; never silently clip."""
    swr, snr = setup['Swr'], setup['Snr']
    nw = setup['nw'] if nw is None else nw
    ng = setup['nCO2'] if ng is None else ng
    if not (0 <= swr < 1 and 0 <= snr < 1 and swr + snr < 1):
        raise ValueError('Residual saturations must define a nonempty interval')
    if not all(math.isfinite(x) for x in (sw, nw, ng)) or min(nw, ng) <= 0:
        raise ValueError('Finite saturation and positive finite exponents required')
    if not swr <= sw <= 1 - snr:
        raise ValueError('Outside shared real physical domain; native clipping is unknown')
    water = setup['krw_eq'] * ((sw - swr) / (1 - swr))**nw
    gas = setup['krn_eq'] * ((1 - sw - snr) / (1 - snr - swr))**ng
    return water, gas


def kozeny_ratio(multiplier, reference_phi):
    if not 0 < reference_phi < 1 or not 0 < multiplier * reference_phi < 1:
        raise ValueError('Reference and scaled porosity must be inside (0,1)')
    return multiplier**3 * (1 - reference_phi)**2 / (1 - multiplier * reference_phi)**2


def kozeny_log_sensitivity(multiplier, reference_phi):
    kozeny_ratio(multiplier, reference_phi)  # same physical domain
    phi = multiplier * reference_phi
    return 3 + 2 * phi / (1 - phi)


def calculate(data):
    rows = []

    def add(item, value, unit, locator, interpretation, status='limited_source_arithmetic'):
        rows.append(dict(item=item, value=value, unit=unit, source_locator=locator,
                         calculation_status=status, interpretation=interpretation,
                         scope='not_native_forward_inverse_or_accepted_service_retention_GHG_model'))

    setup, examples = data['setup'], data['analyst_examples']
    add('literal_gradient_implied_hydrostatic_density', setup['pressure_gradient_literal_Pa_m'] / examples['gravity_m_s2'],
        'kg/m3 under dp/dz=rho*g', 'Table1 p4 / analyst identity',
        'Literal 1.14 Pa/m is on HOLD. This flags a unit/implementation question; no replacement brine density or gradient is inferred.', 'literal_value_dimensional_diagnostic')
    add('literal_gradient_pressure_difference_over_20m', setup['pressure_gradient_literal_Pa_m'] * examples['gradient_test_depth_m'] / 1e5,
        'bar conditional on literal gradient', 'Table1 p4', 'Not an accepted hydrostatic correction or boundary condition.', 'literal_value_dimensional_diagnostic')
    add('temperature_difference_over_20m', setup['temperature_gradient_C_m'] * examples['gradient_test_depth_m'],
        'K', 'Table1 p4', 'Linear gradient difference only, not a cold-injection thermal simulation.')
    add('entry_pressure_bar', setup['entry_pressure_Pa'] / 1e5, 'bar', 'Table1 p4', 'Capillary entry pressure is not an injection BHP ceiling.')
    add('salt_per_water_mass_ratio', setup['salt_mass_fraction_per_brine'] / (1 - setup['salt_mass_fraction_per_brine']),
        'kg salt/kg water', 'Table1 p4', 'Brine-mass versus water-mass denominator. Salt composition and density are not inferred.')
    add('pore_compressibility_times_example_deltaP', setup['pore_compressibility_per_Pa'] * examples['compressibility_delta_pressure_Pa'],
        'dimensionless linearised example', 'Table1 p4 / analyst example', 'Not a full constitutive deformation or retained-carbon calculation.', 'analyst_linearised_example')

    geometry = data['geometry']
    add('described_zone_thickness_sum', sum(geometry['geological_zone_thickness_m']), 'm', 'Section2 p2', '72 m of described zones versus 74 m formation statement; no forced geometry repair.')
    add('formation_minus_zone_thickness_sum', geometry['formation_thickness_m'] - sum(geometry['geological_zone_thickness_m']),
        'm DIFFERENCE', 'Sections1–2 pp1–2', 'Mapping, datum and active interval need the native model.')
    add('conditional_geological_vertical_interval_count', sum(h / dz for h, dz in zip(geometry['geological_zone_thickness_m'], geometry['geological_vertical_steps_m'])),
        'intervals if layer thicknesses divide exactly', 'Section2 p2', 'Not the dynamic mesh cell count; lateral extent, inactive cells and mapping remain unknown.', 'conditional_geometry')

    curve_rows = []
    phase_cases = [dict(case='Table1', nw=setup['nw'], nCO2=setup['nCO2'])] + data['approachII_cases']
    lo, hi = examples['common_Sw']
    count = examples['Sw_grid_count']
    for case in phase_cases:
        label = str(case['case'])
        curve = []
        for i in range(count):
            sw = hi if i == count - 1 else lo + (hi - lo) * i / (count - 1)
            kw, kg = phase_kr(sw, setup, case['nw'], case['nCO2'])
            curve.append((sw, kw, kg))
            curve_rows.append(dict(case=label, Sw=sw, krw=kw, krn=kg,
                                   source_locator='Eq1 p4; Table1 p4; Table4 p6',
                                   status='printed_expression_evaluation_not_native_case_or_clipping_validation'))
        for suffix, value, unit in [('water_at_Swr', curve[0][1], 'dimensionless kr'),
                                    ('gas_at_Swr', curve[0][2], 'dimensionless kr'),
                                    ('water_at_1_minus_Snr', curve[-1][1], 'dimensionless kr'),
                                    ('gas_at_1_minus_Snr', curve[-1][2], 'dimensionless kr'),
                                    ('water_monotone_on_evaluation_grid', int(all(a[1] <= b[1] for a,b in zip(curve, curve[1:]))), 'boolean0/1'),
                                    ('gas_monotone_on_evaluation_grid', int(all(a[2] >= b[2] for a,b in zip(curve, curve[1:]))), 'boolean0/1')]:
            add('phase_' + label + '_' + suffix, value, unit, 'Eq1 / Tables1,4',
                'Literal asymmetric denominators retained on shared Sw domain. Endpoint treatment, capillary law and native phase implementation remain unverified.', 'printed_constitutive_component_evaluated')
    kc = data['Kozeny_Carman']
    case3 = next(case for case in data['approachII_cases'] if case['case'] == 3)
    computed = kozeny_ratio(case3['Mphi'], kc['reference_phi'])
    for item, value, unit in [('case3_reference_scaled_phi', case3['Mphi'] * kc['reference_phi'], 'reference porosity fraction'),
                              ('case3_Kozeny_MK', computed, 'dimensionless multiplier'),
                              ('case3_Kozeny_MK_minus_printed', computed - case3['MK'], 'multiplier DIFFERENCE'),
                              ('case3_Kozeny_MK_matches_display', int(round(computed, 4) == case3['MK']), 'boolean0/1'),
                              ('case3_local_Kozeny_log_sensitivity', kozeny_log_sensitivity(case3['Mphi'], kc['reference_phi']), 'dlnMK/dlnMphi')]:
        add(item, value, unit, 'Section4.2 inline formula / Table4 p6',
            'Printed reference-porosity component only; not field-wide porosity, a recovered inverse solution or statistical variance.', 'printed_constitutive_component_evaluated')

    for entry in data['approachI_arrivals']:
        if entry['observed_days'] is None:
            continue  # printed dashes are missing, never zero
        for eos in ('Span_Wagner', 'Peneloux'):
            error = entry[eos + '_days'] - entry['observed_days']
            percent = abs(error) / entry['observed_days'] * 100
            for suffix, value, unit in [('signed_arrival_error', error, 'days'),
                                        ('absolute_relative_arrival_error', percent, '% of observed detection time'),
                                        ('absolute_error_minus_printed', percent - entry['Span_deviation_percent' if eos == 'Span_Wagner' else 'Peneloux_deviation_percent'], 'percentage points')]:
                add(entry['well'] + '_' + eos + '_' + suffix, value, unit, 'Table3 p5',
                    'Rounded source times; small residuals to printed percentages retained. GMS detection is delayed and these observations are shared across papers.')
    observations = {'200': 21.7, '202': 271}
    for case in data['approachII_cases'] + data['farfield_cases']:
        for well, observed in observations.items():
            error = case['arrival' + well + '_days'] - observed
            add('case_' + str(case['case']) + '_Ktzi' + well + '_signed_error', error, 'days', 'Table4 p6 / Section4.2 p7',
                'Recomputed difference of reported outputs, not independent forward model or holdout data.')
            add('case_' + str(case['case']) + '_Ktzi' + well + '_absolute_relative_error', abs(error) / observed * 100,
                '% of observed detection time', 'Table4 p6 / Section4.2 p7', 'No sensor uncertainty distribution or independent prediction inferred.')
    base, barrier1, changed_region_barrier2 = data['farfield_cases']
    add('same_region_b1_Ktzi202_delay', barrier1['arrival202_days'] - base['arrival202_days'], 'days', 'Section4.2 p7',
        'Same reported nearfield plus inserted barrier; native mask/permeability remain unavailable.')
    add('changed_region_b2_Ktzi202_delay_vs_base', changed_region_barrier2['arrival202_days'] - base['arrival202_days'], 'days', 'Section4.2 p7',
        'Region and barrier geometry change together. Do not attribute the difference solely to one extra metre of thickness.')
    add('case2_arrived_at_Fig4_day255', int(data['approachII_cases'][1]['arrival202_days'] < 255), 'boolean0/1', 'Table4 / Figure4', 'Reported time/figure consistency only.')
    add('case2b_b2_not_arrived_at_Fig4_day255', int(changed_region_barrier2['arrival202_days'] > 255), 'boolean0/1', 'Section4.2 / Figure4', 'Reported time/figure consistency only.')

    for direction, new, old in zip('ijk', data['EOS_multipliers']['near_Span_Wagner'], data['EOS_multipliers']['near_Peneloux']):
        add('near_' + direction + '_EOS_modifier_relative_change', 100 * (new / old - 1), '% of old multiplier', 'Table2 p5',
            'Calibration retuning is not a proportional density-error rule. Baseline tensors/PVT remain missing.')
    add('near_Span_modifier_k_over_i', data['EOS_multipliers']['near_Span_Wagner'][2] / data['EOS_multipliers']['near_Span_Wagner'][0],
        'modifier ratio, not absolute Kv/Kh', 'Table2 p5', 'Actual anisotropy requires the baseline tensor and coordinate orientation.')

    near = data['nearfield']
    lx, ly = near['base_dimensions_m']
    d = near['enlargement_each_direction_m']
    for item, value, unit in [('nearfield_base_area', lx * ly, 'm2'),
                              ('nearfield_expanded_area_if_bounds_each_move_100m', (lx + 2*d) * (ly + 2*d), 'm2'),
                              ('nearfield_area_ratio_if_bounds_each_move_100m', (lx + 2*d) * (ly + 2*d) / (lx * ly), 'ratio'),
                              ('barrier_b1_geometric_volume', near['barrier_length_m'] * near['barrier_width_m'] * barrier1['barrier_thickness_m'], 'm3 geometric'),
                              ('barrier_b2_geometric_volume', near['barrier_length_m'] * near['barrier_width_m'] * changed_region_barrier2['barrier_thickness_m'], 'm3 geometric')]:
        add(item, value, unit, 'Section4.2 pp7–8', 'Explicit rectangle interpretation; not pore volume, storage capacity or verified native case geometry.', 'conditional_geometry')

    cal = data['calibration']
    add('pressure_sigma_in_bar', cal['pressure_sigma_Pa'] / 1e5, 'bar', 'Section4.2 p6', 'Pressure sigma is dimensional; binary arrival-step sigma is not in days.')
    add('conditional_arrival_inverse_variance_weight_case3_over_case12', (cal['arrival_step_sigma_cases12'] / cal['arrival_step_sigma_case3'])**2,
        'ratio under unchanged least-squares residual scaling', 'Section4.2 p6', '0.16 is conditional on inverse-variance weighting, not verified native objective/covariance.', 'analyst_weight_example')
    for name, sensitivity in cal['case3_sensitivities'].items():
        add('case3_' + name + '_relative_to_nw_sensitivity', sensitivity / cal['case3_sensitivities']['nw'], 'coefficient ratio', 'Section4.2 p6',
            'Parameterisation and weighting matter; these are not posterior probabilities or explained variance.')

    calendar = data['calendar']
    start = date.fromisoformat(calendar['start'])
    cal_end = date.fromisoformat(calendar['calibration_end'])
    final = date.fromisoformat(calendar['forecast_end_as_printed'])
    for item, value, unit in [('calendar_elapsed_to_calibration_end', (cal_end - start).days, 'elapsed days'),
                              ('calendar_inclusive_to_calibration_end', (cal_end - start).days + 1, 'inclusive date count'),
                              ('calendar_elapsed_to_printed_forecast_end', (final - start).days, 'elapsed days'),
                              ('reported_final_day_minus_calendar_elapsed', calendar['reported_final_day'] - (final - start).days, 'days DIFFERENCE'),
                              ('elapsed_between_printed_calibration_and_forecast_dates', (final - cal_end).days, 'elapsed days'),
                              ('reported_additional_forecast_minus_calendar_interval', calendar['reported_additional_forecast_days'] - (final - cal_end).days, 'days DIFFERENCE'),
                              ('reported_calibration_plus_forecast_minus_final_day', calendar['reported_calibration_days'] + calendar['reported_additional_forecast_days'] - calendar['reported_final_day'], 'days DIFFERENCE'),
                              ('date_at_zero_based_reported_day2193', (start + timedelta(days=calendar['reported_final_day'])).isoformat(), 'calendar date; diagnostic only'),
                              ('first_shutdown_elapsed', calendar['shutdown_days'][1] - calendar['shutdown_days'][0], 'days'),
                              ('second_shutdown_elapsed', calendar['second_shutdown_days'][1] - calendar['second_shutdown_days'][0], 'days')]:
        add(item, value, unit, 'Sections3.1,4.1 / Figure5 pp3,5–6,8',
            'Preserve printed dates, day labels and six/seven-month descriptions. No corrected source calendar or annual availability factor inferred.', 'explicit_calendar_diagnostic')
    return rows, curve_rows


def main():
    data = load_inputs()
    rows, curve_rows = calculate(data)
    output = ROOT / 'outputs/comprehensive_review'
    for name, table in [('B1-15_checks.csv', rows), ('B1-15_printed_phase_curves.csv', curve_rows)]:
        with (output / name).open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(table[0]), lineterminator='\n')
            writer.writeheader()
            writer.writerows(table)
    result = dict(study_id='B1-15', source_sha256=data['source_sha256'], check_count=len(rows), phase_curve_rows=len(curve_rows),
                  figures=6, tables=4, numbered_equation_groups=1, phase_functions=2,
                  components_evaluated=['literal Eq1 phase relative permeabilities on common real domain', 'inline Kozeny-Carman multiplier'],
                  native_models_reproduced=False, underlying_originals_verified=0,
                  accepted_inputs_changed=False, missing=data['missing'],
                  interpretation='Constitutive evaluation and limited arithmetic only; no native ECLIPSE/DuMux/iTOUGH2 fit, predictive validation, uncertainty posterior, safe annual service, retention or GHG factor.')
    (output / 'B1-15_reconciliation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
