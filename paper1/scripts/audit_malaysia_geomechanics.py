#!/usr/bin/env python3
"""B1-09 printed correlations, unit checks and explicit missing inputs.

Numeric Phi examples are analyst counterexamples to an undisclosed convention,
not reconstructed author cases. No constitutive, coupled finite-element,
fault/fracture, annual-service or retention model is reproduced.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PSI_TO_MPA = 0.006894757293168
FT_TO_M = 0.3048


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B1-09.json').read_text())
    if hashlib.sha256((ROOT / data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale Malaysian geomechanics source')
    return data


def table1(numeric_phi):
    """Literal printed functions; no automatic percent/fraction conversion."""
    ucs = 10598 * math.exp(-4.5206 * numeric_phi)
    fang = 33.861 - 3.816 * numeric_phi
    return dict(RHOB=2.6658 - 1.315 * numeric_phi,
                YME=3.478 * math.exp(-3.281 * numeric_phi),
                PR=0.33905 - 0.3861 * numeric_phi,
                UCS=ucs, FANG=fang, TSTR=ucs / 10, DANG=fang / 2)


def table2(numeric_phi):
    """The printed logarithm requires a positive numeric argument."""
    if numeric_phi <= 0:
        raise ValueError('Phi must be positive for the printed logarithm')
    return dict(Pc_exp=1.8354e4 * math.exp(-5.541e-2 * numeric_phi),
                H_exp=1.8613e7 * math.exp(-1.578e-1 * numeric_phi),
                Rat0=-0.861 * math.log(numeric_phi) + 2.8971,
                BRat0=0.0072 * math.exp(0.0323 * numeric_phi))


def axis_separation_degrees(first, second):
    """Horizontal stress axes are unoriented, modulo 180 degrees."""
    difference = abs(first - second) % 180
    return min(difference, 180 - difference)


def calculate(data):
    rows = []

    def add(item, value, unit, locator, interpretation, status='limited_arithmetic'):
        rows.append(dict(item=item, value=value, unit=unit, source_locator=locator,
                         calculation_status=status, interpretation=interpretation,
                         scope='not_constitutive_FE_fault_fracture_service_retention_or_accepted_GHG_input'))

    for phi in data['analyst_porosity_examples']:
        for table, calculated, definitions in (
                ('Table1', table1(phi), data['table1_correlations']),
                ('Table2', table2(phi), data['table2_correlations'])):
            for item in definitions:
                add(f'{table}_numeric_Phi_{phi:g}_{item["symbol"]}', calculated[item['symbol']],
                    item['unit'], table + ' p5',
                    'Analyst numeric argument, not an author sample. Phi scale/range and creep time '
                    'are unresolved; unphysical results are retained as convention counterexamples.',
                    'analyst_convention_example_not_author_model')

    stress = data['stress_boundary']
    add('horizontal_axis_separation', axis_separation_degrees(stress['Sh_azimuth_deg'], stress['SH_azimuth_deg']),
        'degrees', 'Table3 p6 / text pp4,6',
        'Orthogonal if both azimuths use the same convention; full stress/datum model remains missing.')
    for key in ('Sh_gradient_psi_ft', 'seawater_gradient_psi_ft'):
        add(key + '_SI', stress[key] * PSI_TO_MPA * 1000 / FT_TO_M, 'kPa/m', 'Table3 p6',
            'Gradient unit conversion, not actual CO2 density, BHP or an annual injection limit.')
    add('horizontal_anisotropy_above_Sh', 100 * (stress['SH_over_Sh'] - 1), '% of Sh', 'Table3 p6',
        'The stated SH/Sh ratio implies 4% above Sh; it does not determine Sv or a complete stress regime.')

    ceiling = data['maximum_injection_reservoir_pressure_psi']
    for label, value in [('recommended_reservoir_pressure', ceiling),
                         ('reported_Shmin_low', data['Shmin_range_psi'][0]),
                         ('reported_Shmin_high', data['Shmin_range_psi'][1])]:
        add(label + '_SI', value * PSI_TO_MPA, 'MPa; reference unspecified', 'p13 Figure15/conclusions',
            'Unit conversion only; no gauge-to-absolute conversion or flowing BHP interpretation.')
    for label, stress_value in zip(('low', 'high'), data['Shmin_range_psi']):
        add('displayed_stress_minus_ceiling_' + label, stress_value - ceiling, 'psi DIFFERENCE', 'p13',
            '600 psi applies to the lower reported stress, not every cell or uncertainty bound.')
    margin = data['Shmin_range_psi'][0] - ceiling
    add('lower_margin_relative_to_Shmin', 100 * margin / data['Shmin_range_psi'][0], '% of lower Shmin', 'p13',
        'Explicit denominator: 600/4600, distinct from 600/4000.')
    add('lower_margin_relative_to_ceiling', 100 * margin / ceiling, '% of recommendation', 'p13',
        'Explicit denominator: 600/4000; not an author safety probability or universal margin.')

    # These values are printed prose magnitudes, not digitised time-series points.
    subsidence = data['subsidence_ft']
    for name, feet in [('subsidence_2003', subsidence['depletion_2003']),
                       ('subsidence_prediction_2013', subsidence['predicted_2013']),
                       ('GPS_subsidence_2014', subsidence['GPS_2014']),
                       ('reported_uplift', subsidence['reported_uplift_approx']),
                       ('subsidence_end', subsidence['end_injection_2040']),
                       ('reservoir_compaction_end', data['reservoir_compaction_2040_ft'])]:
        add(name + '_metres', feet * FT_TO_M, 'm magnitude', 'p7 / p13 conclusions',
            'Different years, spatial scopes and reference frames are not interchangeable or matched residuals.')
    add('asynchronous_subsidence_difference',
        (subsidence['GPS_2014'] - subsidence['predicted_2013']) * FT_TO_M, 'm magnitude', 'p7',
        '2014 GPS minus 2013 prediction; not an aligned residual, RMSE, holdout or uncertainty statistic.')

    fault = data['fault_properties_adopted']
    for key in ('normal_stiffness_psi_ft', 'shear_stiffness_psi_ft'):
        add('adopted_' + key + '_SI', fault[key] * PSI_TO_MPA / FT_TO_M, 'MPa/m', 'Table4 p9',
            'Imported SF30 clastic contact stiffness: stress per displacement, not an elastic modulus.')
    add('adopted_cohesion_SI', fault['cohesion_psi'] * PSI_TO_MPA, 'MPa', 'Table4 p9',
        'Imported analogue cohesion; not a measured Field X parameter.')
    add('adopted_tangent_friction', math.tan(math.radians(fault['friction_deg'])), 'dimensionless', 'Table4 p9',
        'Analyst tangent conversion only; not a reproduced contact law or field calibration.')
    slips = data['reported_slip_cm']
    add('reported_max_fault_slip', slips['FieldX'] * 10, 'mm', 'pp10–11 / Table5',
        'Unit conversion of model deformation, not a leakage flux or probability.')
    for field in ('Ekofisk', 'SF30'):
        add(field + '_printed_slip_ratio_to_FieldX', slips[field] / slips['FieldX'], 'ratio', 'Table5 p11',
            'Different field/material/contact/loading cases; ratio is not a risk-reduction factor.')
    add('conclusion_fault_count_minus_displayed',
        data['conclusion_fault_count'] - len(data['displayed_fault_ids']), 'fault count', 'pp10/13',
        'Conclusion says five; Figure12/text identify four. No fifth fault is inferred.')
    add('reported_max_plastic_strain_fraction', data['maximum_local_plastic_strain_pct'] / 100,
        'dimensionless', 'p12 Figure14',
        'Local maximum scalar, not foreign-field average or incremental volumetric compaction strain.')
    for key, value in data['missing_inputs'].items():
        add(key, value, 'MISSING', 'pp3–13',
            'Not computed from pressure, plotted displacement, selected step count or foreign-field thresholds.',
            'not_computable_missing_author_inputs')
    return rows


def main():
    rows = calculate(load_inputs())
    target = ROOT / 'outputs/comprehensive_review/B1-09_diagnostics.csv'
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    print(f'{len(rows)} limited geomechanics checks; full models and annual service remain uncomputed.')


if __name__ == '__main__':
    main()
