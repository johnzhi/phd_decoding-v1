#!/usr/bin/env python3
"""B1-13 source-table arithmetic, conditional bases and control checks.

No native Petrel/GEM or geomechanical case is reproduced. Display-resolution
intervals below are conditional rounding checks, not measurement uncertainty.
No standard-volume quantity is converted to CO2 mass.
"""
import csv
import hashlib
import json
from datetime import date
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FT_M = .3048
BBL_M3 = .158987294928


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B1-13.json').read_text())
    if hashlib.sha256((ROOT / data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale pressure-sink source')
    return data


def pressure_margin(initial, critical, factor):
    if factor <= 0:
        raise ValueError('Positive safety factor required')
    return initial + (critical - initial) / factor


def rounding_product_overlap(left, left_step, right, right_step, reported, reported_step):
    """Positive displayed operands, each rounded to nearest supplied step."""
    if min(left, right, left_step, right_step, reported_step) <= 0:
        raise ValueError('Positive inputs and display steps required')
    low = (left - left_step / 2) * (right - right_step / 2)
    high = (left + left_step / 2) * (right + right_step / 2)
    return max(low, reported - reported_step / 2) <= min(high, reported + reported_step / 2)


def full_pore_capacity_Bscf(pore_m3, bg_reservoir_m3_per_standard_m3):
    """Conditional Bg convention, not the undefined source Bg basis."""
    if pore_m3 < 0 or bg_reservoir_m3_per_standard_m3 <= 0:
        raise ValueError('Nonnegative volume and positive Bg required')
    return pore_m3 / bg_reservoir_m3_per_standard_m3 / FT_M**3 / 1e9


def poroelastic_increment(alpha, nu, delta_pressure):
    if not -1 < nu < .5:
        raise ValueError('Stable isotropic Poisson ratio required')
    return alpha * (1 - 2 * nu) / (1 - nu) * delta_pressure


def calculate(data):
    output = []

    def add(item, value, unit, locator, interpretation, status='limited_source_arithmetic'):
        output.append(dict(item=item, value=value, unit=unit, source_locator=locator,
                           calculation_status=status, interpretation=interpretation,
                           scope='not_native_Petrel_GEM_failure_retention_or_accepted_operating_GHG_model'))

    grid = data['structural_grid']
    for key, dimensions, source in [('cells', grid['cells'], grid['reported_cells']),
                                     ('nodes', grid['nodes'], grid['reported_nodes']),
                                     ('2D_cells', grid['cells'][:2], grid['reported_2D_cells']),
                                     ('2D_nodes', grid['nodes'][:2], grid['reported_2D_nodes'])]:
        result = 1
        for dim in dimensions:
            result *= dim
        add('grid_' + key + '_product_minus_printed', result - source, 'count DIFFERENCE', 'Figure1 p4',
            'Metadata count identity only; not active-cell/region volume, mesh convergence or model validation.')

    for column in ('bulk_Mm3', 'net_Mm3', 'pore_Mm3'):
        total = sum(row[column] for row in data['zones'])
        add('Table4_' + column + '_row_sum', total, 'million m3', 'Table4 p5', 'Sum of printed rows; no geological or fluid model reproduced.')
        add('Table4_' + column + '_row_sum_minus_total', total - data['table4_totals'][column], 'million m3 DIFFERENCE',
            'Table4 p5', 'Exact printed arithmetic only; volume definitions still require native masks/properties.')
    capacities = [Decimal(str(row['theoretical_Bscf'])) for row in data['zones']]
    fine_sum = sum(capacities)
    coarse_sum = sum(Decimal(str(row['table4_capacity_Tscf'])) for row in data['zones'])
    add('Table7_capacity_row_sum', float(fine_sum), 'Bscf', 'Table7 p7', '157.02Bscf printed-row sum versus157.03Bscf total; no source value corrected.')
    add('Table7_capacity_row_sum_minus_total', float(fine_sum - Decimal(str(data['table7_totals']['capacity_Bscf']))),
        'Bscf DIFFERENCE', 'Table7 p7', '0.01Bscf difference is compatible with two-decimal row display; not inferred leakage.')
    add('Table4_coarse_capacity_row_sum', float(coarse_sum), 'Tscf', 'Table4 p5',
        'Individually rounded rows sum.15Tscf, while the finer aggregate rounds.16Tscf. Coarse aggregation need not commute with rounding.')
    add('finer_row_sum_rounded_Tscf', float((fine_sum / 1000).quantize(Decimal('.01'))), 'Tscf', 'Tables4/7',
        'Rounding the157.02Bscf row sum to.01Tscf yields.16. This explains coarse aggregation without establishing capacity physics.')

    for row in data['zones']:
        prefix = row['table4_label']
        net_replay = row['bulk_Mm3'] * row['NTG']
        pore_replay = row['net_Mm3'] * row['phi']
        common = 'Conditional same-region, compatible volume/property basis. Rounded inputs are preserved; no native mask or definition inferred.'
        for label, value, unit in [
            ('bulk_NTG_net_replay', net_replay, 'million m3'),
            ('printed_net_minus_replay', row['net_Mm3'] - net_replay, 'million m3 DIFFERENCE'),
            ('net_NTG_rounding_overlap', int(rounding_product_overlap(row['bulk_Mm3'], 1, row['NTG'], .01, row['net_Mm3'], 1)), 'boolean0/1'),
            ('net_phi_pore_replay', pore_replay, 'million m3'),
            ('printed_pore_minus_replay', row['pore_Mm3'] - pore_replay, 'million m3 DIFFERENCE'),
            ('pore_phi_rounding_overlap', int(rounding_product_overlap(row['net_Mm3'], 1, row['phi'], .01, row['pore_Mm3'], 1)), 'boolean0/1')]:
            add(prefix + '_' + label, value, unit, 'Tables4/7 pp5/7', common +
                ' Overlap uses nearest displayed integer volume and.01 fraction rounding only, not measurement uncertainty.', 'conditional_common_region_rounding_check')
        capacity = full_pore_capacity_Bscf(row['pore_Mm3'] * 1e6, row['Bg_numeric'])
        add(prefix + '_conditional_full_pore_Bg_capacity', capacity, 'Bscf; Bg m3/m3 ASSUMED', 'Table7 p7',
            'Source Bg unit, standard state, Swirr/efficiency and occupied-region bases unknown. Not a reproduced resource or accepted input.', 'conditional_Bg_basis_example')
        add(prefix + '_conditional_implied_occupied_factor', row['theoretical_Bscf'] / capacity, 'ratio', 'Table7 p7',
            'Ratio required under the assumed Bg convention; not measured Swirr, saturation or efficiency.', 'conditional_Bg_basis_example')
        replay = pressure_margin(row['initial_pressure_numeric_psi'], row['critical_caprock_Sh_after_psi'], data['pressure_safety_factor'])
        add(prefix + '_delta_safety_pressure_replay', replay, 'psi; compatible references ASSUMED', 'Table6 p6',
            'Initial+(critical−initial)/1.5, not critical/1.5. Critical caprock response, initialpsia versus otherpsi and datums remain unverified.', 'conditional_delta_pressure_rule')
        add(prefix + '_printed_recommended_minus_replay', row['recommended_pressure_psi'] - replay, 'psi DIFFERENCE', 'Table6 p6',
            'All six residuals within.4psi. Rounded-rule agreement is not geomechanical calibration or validation.', 'conditional_delta_pressure_rule')
        add(prefix + '_uniform_BHP_minus_layer_limit', data['controls']['max_injector_BHP_numeric_psi'] - row['recommended_pressure_psi'],
            'psi DIFFERENCE; reference compatibility NOT established', 'Tables6/7 / p8 controls',
            'Conditional raw number comparison only. Well BHP, layer depth and caprock limit references must be mapped before declaring compliance or violation.',
            'unresolved_depth_reference_comparison')
        at_contact = data['water_gradient_psi_ft'] * abs(row['contact_m']) / FT_M
        add(prefix + '_gradient_at_contact_minus_initial', at_contact - row['initial_pressure_numeric_psi'], 'psi DIFFERENCE', 'Table7 / pp7–8',
            'Contact magnitudes match listed pressures within display precision if used as gradient depth. Text says mid-depth; no origin,MD/TVDSS mapping or pressure datum inferred.',
            'conditional_gradient_depth_comparison')
        add(prefix + '_reference_MD_minus_contact_magnitude', row['reference_depth_mMD'] - abs(row['contact_m']), 'm DIFFERENCE', 'Tables6/7',
            'Different depth quantities are retained. Not a derived derrick/seabed offset or trajectory correction.', 'unresolved_depth_reference_comparison')
        beta = (row['original_caprock_Sh_psi'] - row['critical_caprock_Sh_after_psi']) / (row['critical_caprock_Sh_after_psi'] - row['initial_pressure_numeric_psi'])
        add(prefix + '_conditional_implied_caprock_relaxation_slope', beta, 'stress/pressure increment ratio', 'Table6 / Eq1 / p6 transfer statement',
            'Assume linear caprock weakening between the printed states. This inferred slope is not the stated maximum.33 vertical-transfer factor, alpha, nu or a calibrated native stress path.',
            'conditional_linear_stress_path_identity')
        rounded = (Decimal(str(row['theoretical_Bscf'])) / 1000).quantize(Decimal('.01'))
        add(prefix + '_fine_capacity_rounding_matches_Table4', int(rounded == Decimal(str(row['table4_capacity_Tscf']))), 'boolean0/1', 'Tables4/7',
            'Two-decimal Tscf display only. Compatible rounding does not reproduce volume-to-gas physics.')

    results, controls = data['results'], data['controls']
    names = ('no_producer', 'one_injector_one_producer', 'two_injectors_one_producer')
    # Source says January2025 to2050, without an exact endpoint. These dates
    # define an explicit analyst25-year calendar, not the native run schedule.
    days = (date.fromisoformat(data['analyst_examples']['constant_rate_calendar_end']) -
            date.fromisoformat(data['analyst_examples']['constant_rate_calendar_start'])).days
    add('analyst_calendar_days', days, 'days', 'p1 January2025 /2050 /25years',
        'Conditional Jan1,2025→Jan1,2050, not an asserted native endpoint, annual array or operating availability.', 'analyst_calendar_example')
    for label, percent in zip(names, results['reported_percentages']):
        volume = results[label + '_Bscf']
        ratio = 100 * volume / results['theoretical_Bscf']
        add(label + '_effective_over_theoretical_percent', ratio, '% of157.03Bscf', 'Table8 p13 / source case text',
            'Reported cumulative injection divided by reported resource. Not a retained fraction or annual rate.', 'source_ratio_arithmetic')
        add(label + '_ratio_minus_rounded_percent', ratio - percent, 'percentage points', 'Table8 p13',
            'Whole-percent source rounding retained, not a calibrated uncertainty distribution.', 'source_ratio_arithmetic')
        add(label + '_analyst_calendar_average_rate', volume * 1000 / days, 'MMscf/day scenario average', 'Table8 / analyst calendar',
            'Uniform-time average of a cumulative output only; not a constant actual rate or maximum annual service.', 'analyst_calendar_example')
    no, one, two = [results[name + '_Bscf'] for name in names]
    for name, value, unit in [('one_vs_no_ratio', one / no, 'ratio'), ('two_vs_no_ratio', two / no, 'ratio'),
                               ('two_minus_one', two - one, 'Bscf'), ('two_over_one_increment_percent', 100 * (two - one) / one, '% of one-injector result')]:
        add(name, value, unit, 'Table8 p13', 'Different modeled configurations/controls. No transferable multiplier, independent flow reproduction or economic/GHG inference.', 'source_scenario_comparison')
    add('no_producer_average_until_shutdown', no * 1000 / results['no_producer_shutdown_days'], 'MMscf/day', 'p8',
        '4.9Bscf over reported200days gives24.5MMscf/day, distinct from the60MMscf/day upper target.')
    add('no_producer_constant_target200days', controls['max_gas_MMscf_day'] * results['no_producer_shutdown_days'] / 1000, 'Bscf target example', 'p8',
        'Constant60MMscf/day for200days would be12Bscf; achieved pressure-limited cumulative is4.9Bscf. No constant-rate assumption adopted.')
    for factor in (1, 2):
        add(f'analyst_calendar_target_{factor}x60MMscf_day', factor * controls['max_gas_MMscf_day'] * days / 1000, 'Bscf target ceiling EXAMPLE', 'pp8/11 / analyst calendar',
            'One total60 target versus two per-well60 targets are alternative unresolved interpretations, not achieved capacities or selected control semantics.', 'analyst_target_basis_example')

    water = results['optimized_water_Mbbl'] * 1e6
    peak = results['optimized_peak_water_kbbl_numeric'] * 1000
    for name, value, unit in [('volume_m3', water * BBL_M3, 'surface m3'), ('calendar_average_bbl_day', water / days, 'bbl/day'),
                               ('peak_over_target', peak / controls['max_water_bbl_day'], 'ratio'),
                               ('volume_over_peak', water / peak, 'equivalent peak-rate days'),
                               ('water_over_injected_standard_gas', water / (two * 1000), 'bbl/MMscf injected')]:
        add('optimized_reported_water_' + name, value, unit, 'p12/Figure14 / Table8',
            'Approximately40million surfacebbl and21000bbl/day peak in this scenario. No reservoir-volume equivalence, actual active duration, brine mass, pumping duty, producedCO2 fate or general inventory factor.',
            'approximate_reported_water_scenario_arithmetic')
    ex = data['analyst_examples']
    delta = poroelastic_increment(ex['alpha'], ex['nu'], ex['delta_P_psi'])
    add('analyst_Eq1_total_horizontal_increment', delta, 'psi', 'Eq1 p6',
        'Analyst alpha1,nu.25,DeltaP100psi only; no native log or field stress reconstructed.', 'analyst_poroelastic_example')
    add('analyst_effective_horizontal_increment', delta - ex['alpha'] * ex['delta_P_psi'], 'psi', 'Eq1 / analyst compression-positive identity',
        'Effective stress subtracts alphaP. Reservoir total-stress increase is not the caprock transfer path or a fracture criterion.', 'analyst_poroelastic_example')
    for colour in ('green', 'yellow', 'red'):
        add('screening_' + colour + '_cell_count', sum(row['colours'].count(colour) for row in data['screening_matrix']), 'qualitative colour cells', 'Table2 p3',
            'Literal27-cell raster transcription only. Shifted legend rows are not repaired; colours are not probabilities.')
    return output


def main():
    data = load_inputs()
    rows = calculate(data)
    out = ROOT / 'outputs/comprehensive_review'
    with (out / 'B1-13_checks.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    source = {row['item']: row for row in rows}
    reconciliation = dict(study_id='B1-13', source_sha256=data['source_sha256'], check_count=len(rows),
                          source_figures=15, source_tables=8, numbered_equations=1,
                          pressure_rule_max_abs_residual_psi=max(abs(source[row['table4_label'] + '_printed_recommended_minus_replay']['value']) for row in data['zones']),
                          conditional_net_rounding_compatible_rows=sum(source[row['table4_label'] + '_net_NTG_rounding_overlap']['value'] for row in data['zones']),
                          conditional_pore_rounding_compatible_rows=sum(source[row['table4_label'] + '_pore_phi_rounding_overlap']['value'] for row in data['zones']),
                          native_models_reproduced=False, accepted_inputs_changed=False,
                          missing=data['missing'], standard_temperature=None, standard_pressure=None, Bg_units=None,
                          pressure_reference_and_control_depth=None,
                          interpretation='Internal pressure/volume/rounding/ratio checks only. Common-region and Bg assumptions are conditional; no correction, mass conversion, maximum annual service, retained-carbon, economic or GHG conclusion.')
    (out / 'B1-13_reconciliation.json').write_text(json.dumps(reconciliation, indent=2) + '\n')
    print(json.dumps(reconciliation, indent=2))


if __name__ == '__main__':
    main()
