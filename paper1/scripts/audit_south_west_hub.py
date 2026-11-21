#!/usr/bin/env python3
"""B1-12 literal unit, equation and table checks; no native field reproduction.

Rounded formation means need not reproduce means of nonlinear correlations.
The symmetric stress formula is an explicitly labelled analyst comparison,
never a replacement for the source's printed Eq13 or its unavailable code.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PSI_PA = 6894.757293168
LBM_KG = .45359237
FT_M = .3048
G0 = 9.80665


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B1-12.json').read_text())
    if hashlib.sha256((ROOT / data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale South-West Hub source')
    return data


def sonic_km_s(transit_us_ft):
    if transit_us_ft <= 0:
        raise ValueError('Positive transit time required')
    return 304.8 / transit_us_ft


def wave_elastic(rho_g_cm3, vp_km_s, vs_km_s):
    """Isotropic wave relations in the explicit g/cm3, km/s, GPa convention."""
    if min(rho_g_cm3, vp_km_s, vs_km_s) <= 0 or vp_km_s**2 <= 4 * vs_km_s**2 / 3:
        raise ValueError('Positive isotropic bulk and shear moduli required')
    p2, s2 = vp_km_s**2, vs_km_s**2
    return dict(E_GPa=rho_g_cm3 * s2 * (3 * p2 - 4 * s2) / (p2 - s2),
                nu=(p2 - 2 * s2) / (2 * (p2 - s2)),
                G_shear_GPa=rho_g_cm3 * s2,
                K_bulk_GPa=rho_g_cm3 * (p2 - 4 * s2 / 3))


def ucs_from_cohesion(cohesion, friction_deg):
    if cohesion < 0 or not 0 <= friction_deg < 90:
        raise ValueError('Nonnegative cohesion and friction in [0,90) required')
    angle = math.radians(friction_deg)
    return 2 * cohesion * math.cos(angle) / (1 - math.sin(angle))


def stress_pair(young, nu, alpha, sv, pore, epsilon_x, epsilon_y, *, convention='printed'):
    if young <= 0 or not -1 < nu < .5:
        raise ValueError('Stable isotropic elastic parameters required')
    if convention not in ('printed', 'analyst_symmetric_comparison'):
        raise ValueError('Unknown stress convention')
    base = nu / (1 - nu) * sv - nu / (1 - nu) * alpha * pore + alpha * pore
    factor = young / (1 - nu**2)
    sh = base + factor * (epsilon_x + nu * epsilon_y)
    # Eq13 visibly prints E on epsilon_x; do not insert a missing nu silently.
    x_coefficient = 1 if convention == 'printed' else nu
    big_sh = base + factor * (x_coefficient * epsilon_x + epsilon_y)
    return sh, big_sh


def overburden_psi(rho_lbm_ft3, depth_ft, gravity_m_s2=G0):
    """Explicit SI conversion avoids multiplying lbm into a psi result."""
    if rho_lbm_ft3 <= 0 or depth_ft < 0 or gravity_m_s2 <= 0:
        raise ValueError('Positive density/gravity and nonnegative depth required')
    density_si = rho_lbm_ft3 * LBM_KG / FT_M**3
    return density_si * gravity_m_s2 * depth_ft * FT_M / PSI_PA


def calculate(data):
    rows = []

    def add(item, value, unit, locator, interpretation, status='limited_arithmetic'):
        rows.append(dict(item=item, value=value, unit=unit, source_locator=locator,
                         calculation_status=status, interpretation=interpretation,
                         scope='not_native_Visage_flow_THM_fault_retention_or_accepted_operating_GHG_model'))

    ex = data['analyst_examples']
    corr = data['correlations']
    speed = sonic_km_s(ex['sonic_us_ft'])
    add('analyst_sonic_conversion', speed, 'km/s', 'Eq1 p7',
        '100 microsecond/ft analyst example; source coefficient gives km/s, whereas later prose says m/s.', 'analyst_unit_example')
    add('analyst_sonic_conversion_SI', speed * 1000, 'm/s', 'Eq1 p7',
        'Equivalent explicit SI velocity, not a Harvey log point.', 'analyst_unit_example')
    add('Gardner_same_coefficient_m_s_unit_factor', 1000**corr['rho_exponent'], 'density ratio', 'Eq3 pp7–8',
        'Changing numeric Vp from km/s to m/s without changing the coefficient scales density by this factor. Not evidence of native code behavior.', 'unit_scaling_identity')
    add('UCS_same_coefficient_m_s_unit_factor', 1000**corr['UCS_exponent'], 'UCS ratio', 'Eq7 p8',
        'The fit explicitly requires km/s. A unit error is amplified by the exponent; no such native error is asserted.', 'unit_scaling_identity')
    add('conditional_static_modulus_positive_threshold', -corr['E_static_intercept'] / corr['E_static_slope'],
        'same modulus unit as intercept; GPa only if assumed', 'Eq6 p8',
        'Below this Edynamic, the literal fit gives nonpositive Estatic. Original calibration/domain and intercept unit remain unknown.', 'conditional_correlation_domain')

    for row in data['formation_averages']:
        label = row['formation']
        vp, vs, rho = [row[k] for k in ('Vp_km_s', 'Vs_km_s', 'rho_g_cm3')]
        result = wave_elastic(rho, vp, vs)
        for key, value in result.items():
            add(label + '_wave_at_reported_means_' + key, value, 'dimensionless' if key == 'nu' else 'GPa',
                'Eqs4–5 pp7–8 / averages p12',
                'Transform of reported rounded means, not mean of transformed native logs. Dynamic/static and spatial weighting unresolved.',
                'conditional_transform_of_means_not_native_reproduction')
        comparisons = dict(
            synthetic_Vs_at_mean_Vp_km_s=corr['Vs_slope'] * vp + corr['Vs_intercept'],
            density_at_mean_Vp_g_cm3=corr['rho_coefficient'] * vp**corr['rho_exponent'],
            UCS_at_mean_Vp_MPa=corr['UCS_coefficient'] * vp**corr['UCS_exponent'],
            phi_at_mean_Vp_deg_assumed=corr['phi_coefficient'] * vp**corr['phi_exponent'],
            static_E_at_wave_means_GPa_assumed=corr['E_static_slope'] * result['E_GPa'] + corr['E_static_intercept'],
            E_if_G_token_is_same_basis_shear_GPa=2 * row['G_token_GPa'] * (1 + row['nu']),
            E_if_G_token_is_same_basis_bulk_GPa=3 * row['G_token_GPa'] * (1 - 2 * row['nu']))
        units = ['km/s', 'g/cm3', 'MPa', 'degrees ASSUMED', 'GPa ASSUMED', 'GPa', 'GPa']
        for (key, value), unit in zip(comparisons.items(), units):
            add(label + '_' + key, value, unit, 'Eqs2–8 / pp12–14',
                'Conditional means/basis comparison. G is undefined in prose while Figure8 says bulk modulus. Nonlinear averaging, rounding and static/dynamic distinctions prevent declaring a hidden code error.',
                'conditional_transform_or_material_basis_not_native_reproduction')

    for row in data['material_table']['rows']:
        prefix = 'Table1_' + row['material'].replace(' ', '_')
        replay = ucs_from_cohesion(row['cohesion_MPa'], row['friction_deg'])
        add(prefix + '_MC_uniaxial_UCS', replay, 'MPa', 'Eq9 p8 / Table1 p15',
            'Inverse printed cohesion relation with degree-to-radian conversion; not a reproduced rock test or native constitutive model.')
        add(prefix + '_printed_UCS_minus_MC', row['UCS_MPa'] - replay, 'MPa DIFFERENCE', 'Table1 p15',
            'Printed values retained. Small display-level residual is an internal arithmetic comparison, not independent measurement validation.')
        add(prefix + '_tensile_over_cohesion', row['tensile_MPa'] / row['cohesion_MPa'], 'ratio', 'Table1 p15',
            'All rows prescribe tensile strength as one-half cohesion; independent tensile measurements not established.')

    for row in data['strain_cases']:
        add(f'Table3_case{row["case"]}_implied_epsilon_y', row['epsilon_x'] * row['K_y_over_x'],
            'source strain numeric scale UNKNOWN', 'Table3 p18',
            'K=epsilon_y/epsilon_x only. Neither percent nor millistrain nor literal dimensionless scaling is selected.')
    for scale in ex['strain_scale_scenarios']:
        fit = data['best_fit_strains']
        args = (ex['E_MPa'], ex['nu'], ex['alpha'], ex['Sv_MPa'], ex['Pp_MPa'], fit['epsilon_x'] * scale, fit['epsilon_y'] * scale)
        for convention in ('printed', 'analyst_symmetric_comparison'):
            small, big = stress_pair(*args, convention=convention)
            add(f'analyst_{convention}_bestfit_scale_{scale:g}_SH_minus_Sh', big - small, 'MPa', 'Eqs12–13 p9 / strain numbers p17',
                'Analyst E=5000MPa,nu=.22 with three hypothetical strain scales. These are counterexamples, not inferred native stresses, a corrected equation or a chosen scale.',
                'analyst_literal_versus_symmetric_example')
    eps = ex['equal_strain']
    for convention in ('printed', 'analyst_symmetric_comparison'):
        small, big = stress_pair(ex['E_MPa'], ex['nu'], ex['alpha'], ex['Sv_MPa'], ex['Pp_MPa'], eps, eps, convention=convention)
        add('analyst_equal_strains_' + convention + '_SH_minus_Sh', big - small, 'MPa', 'Eqs12–13 p9',
            'Equal prescribed strains expose the printed coefficient asymmetry. The symmetric comparison has zero horizontal difference; actual implementation remains unavailable.',
            'analyst_symmetry_counterexample')
    add('analyst_fixed_inputs_total_horizontal_pressure_derivative', ex['alpha'] * (1 - 2 * ex['nu']) / (1 - ex['nu']),
        'MPa/MPa', 'Eqs12–13 p9', 'Fixed elastic constants, vertical stress and tectonic strains only; no thermal or flow feedback.', 'analyst_elastic_derivative')
    add('analyst_fixed_inputs_effective_horizontal_pressure_derivative', -ex['alpha'] * ex['nu'] / (1 - ex['nu']),
        'MPa/MPa', 'Eqs12–13 / analyst compression-positive effective stress',
        'Subtract alpha*P from total stress. Not a temporal field forecast or failure probability.', 'analyst_elastic_derivative')
    add('analyst_overburden_explicit_SI_conversion', overburden_psi(ex['density_lbm_ft3'], ex['depth_ft']), 'psi', 'Eq11 p9',
        'Analyst150lbm/ft3 and5000ft at standard gravity; explicit density, depth, force and area units. No Harvey density column reconstructed.', 'analyst_unit_example')

    for number, row in enumerate(data['lot_tests'], 1):
        if row['pump_pressure_psi'] is not None:
            pump = row['pump_pressure_psi'] * PSI_PA / 1e6
            add(f'Table2_row{number}_pump_converted', pump, 'MPa; reference unresolved', 'Table2 p18',
                'Unit conversion only. Pump pressure and reported LOT are distinct quantities; hydrostatic mud head and datum are not supplied.')
            add(f'Table2_row{number}_LOT_minus_pump', row['LOT_MPa'] - pump, 'MPa DIFFERENCE; reference compatibility ASSUMED', 'Table2 p18',
                'Not an inferred pressure error or measured mud head. FIT29.4MPa is not fracture equality.', 'conditional_reference_comparison')
    # Candidate pairings expose source depth differences, without asserting identity.
    for label, case, test in [('7_4MPa', 1, 0), ('about26MPa', 2, 4)]:
        add('candidate_' + label + '_Table3_minus_Table2_depth', data['strain_cases'][case]['depth_m'] - data['lot_tests'][test]['depth_m'],
            'm DIFFERENCE', 'Tables2–3 p18', 'Similar stress numbers do not prove the same observation or depth datum. Pairing is unresolved.', 'unconfirmed_candidate_pairing')
    point = data['stress_at_depth']
    ratio = point['SH_MPa'] / point['Sh_MPa']
    add('reported_pair_SH_over_Sh', ratio, 'ratio', 'p18', '37/32 is1.15625; the paper reports about1.125. Neither stress is changed.')
    add('reported_pair_ratio_minus_quoted_ratio', ratio - point['reported_ratio'], 'ratio DIFFERENCE', 'p18', 'Preserve both source numbers and the reported ratio; obtain native unrounded case.')
    for label in ('Sh_MPa', 'SH_MPa'):
        add('analyst_depth_average_' + label, point[label] * 1000 / point['depth_m'], 'kPa/m depth-average ratio', 'p18',
            'Stress/depth arithmetic, not a local gradient, formation fit or correction of the source .18MPa gradient lacking a length denominator.')
    plan = data['reference_plan']
    add('nominal_plan_total', plan['nominal_total_t_year'] * plan['years'] / 1e6, 'Mt nominal target', 'p18',
        '800000t/year times30years is24Mt, not maximum annual mass, achieved injection or permanent retention.')
    add('analyst_equal_well_share', plan['nominal_total_t_year'] / plan['wells'], 't/well/year equal-share EXAMPLE', 'p18',
        'Nine wells do not imply actual equal allocation. No per-well rate schedule is supplied.', 'analyst_allocation_example')
    increment = plan['multiplier'] * plan['increment_base_bar']
    add('conditional_control_increment', increment, 'bar DIFFERENCE', 'p18', 'Literal .9*69. No independent fracture margin, pressure reference or thermal condition established.', 'conditional_control_algebra')
    add('conditional_implied_reference_pore_pressure', plan['bhp_bar'] - increment, 'bar; pressure basis UNKNOWN', 'p18',
        '360=Pp+.9*69 only if quantities share a compatible reference; not measured initial pressure.', 'conditional_control_algebra')
    fig = data['figure10']
    add('Figure10_left_legend_minus_caption_maximum', fig['left_legend_max_psi'] - fig['left_caption_max_psi'], 'psi displayed maximum DIFFERENCE', 'Figure10 p14',
        '800psi legend versus500psi caption. Does not establish absolute pressure, a reservoir increment or safe service.')
    return rows


def main():
    data = load_inputs()
    rows = calculate(data)
    output = ROOT / 'outputs/comprehensive_review'
    with (output / 'B1-12_checks.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    result = dict(study_id='B1-12', source_sha256=data['source_sha256'], check_count=len(rows),
                  material_parameter_cells=90, material_porosity_numeric_cells=8, material_porosity_HRP_tokens=2,
                  source_equations=13, figures=17, tables=3,
                  native_models_reproduced=False, accepted_inputs_changed=False,
                  unresolved_strain_scale=data['strain_scale'], unresolved_gradient_denominator=data['reported_Sh_gradient']['denominator'],
                  original_model_status='not_reproduced; literal equations, units and table arithmetic only',
                  interpretation='No calibrated annual maximum injection, observed operation, field-wide zero failure, caprock/thermal integrity,1000y retained mass or GHG benefit established.')
    (output / 'B1-12_reconciliation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
