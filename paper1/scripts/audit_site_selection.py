#!/usr/bin/env python3
"""B1-10 unit/geometry checks and explicitly analyst-selected counterexamples.

This does not reproduce the anonymised case, EOS, diameter optimisation, annual
dispatch, global MILP or PSO. Plot estimates and arithmetic are not accepted
annual service, monetary savings or GHG inputs.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B1-10.json').read_text())
    if hashlib.sha256((ROOT / data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale site-selection source')
    return data


def friction_factor(reynolds, roughness_m, diameter_m):
    """Literal Eq2. Calling this is not a check of its validity for a real case."""
    if reynolds <= 0 or diameter_m <= 0 or roughness_m < 0:
        raise ValueError('Nonpositive Reynolds/diameter or negative roughness')
    return .25 / math.log10(roughness_m / (3.7 * diameter_m) + 5.74 / reynolds**.9)**2


def pipeline_example(example):
    area = math.pi * example['diameter_m']**2 / 4
    velocity = example['mass_kg_s'] / (example['density_kg_m3'] * area)
    reynolds = example['density_kg_m3'] * velocity * example['diameter_m'] / example['viscosity_Pa_s']
    factor = friction_factor(reynolds, example['roughness_m'], example['diameter_m'])
    pressure_loss = factor * example['length_m'] / example['diameter_m'] * example['density_kg_m3'] * velocity**2 / 2
    return dict(area=area, velocity=velocity, reynolds=reynolds, friction_factor=factor, pressure_loss=pressure_loss)


def radial_delta_p_squared(example, axisymmetric=False):
    """Printed Eq5 versus an independent SI constant-mu/z/T radial derivation.

    Integrating m = 2*pi*r*h*k/ mu * (M*p/(z*R*T)) * dp/dr
    supplies pi in the pressure-squared coefficient. The same -0.75 shape
    correction is held fixed for this coefficient comparison only. The book
    cited by the source is not verified; no hidden implementation is inferred.
    """
    shape = math.log(example['re_m'] / example['rw_m']) - .75
    numerator = (example['mass_kg_s'] * example['viscosity_Pa_s'] * example['z_constant'] *
                 example['R_J_mol_K'] * example['temperature_K'] * shape)
    denominator = example['molar_mass_kg_mol'] * example['permeability_m2'] * example['thickness_m']
    return numerator / denominator / (math.pi if axisymmetric else 1)


def pumping_power_W(mass_kg_s, density_kg_m3, delta_pressure_Pa, efficiency):
    return mass_kg_s / density_kg_m3 * delta_pressure_Pa / efficiency


def electricity_cost_from_W(power_W, hours, tariff_USD_kWh):
    return power_W / 1000 * hours * tariff_USD_kWh


def raw_capex(diameter_number, length_number, coefficient=1.2):
    """Raw printed Eq9. Money/length conventions are deliberately unassigned."""
    return coefficient * diameter_number**1.3 * length_number


def available_start_does_not_limit_end(start, limit, increment):
    return dict(start_available=start < limit, end_pressure=start + increment,
                end_within_limit=start + increment <= limit)


def calculate(data):
    rows = []

    def add(item, value, unit, locator, interpretation, status='limited_arithmetic'):
        rows.append(dict(item=item, value=value, unit=unit, source_locator=locator,
                         calculation_status=status, interpretation=interpretation,
                         scope='not_author_EOS_case_dispatch_MILP_PSO_or_accepted_service_GHG_input'))

    old = data['reported_cumulative_cost_USD_million']['baseline_text_p11']
    far = data['reported_cumulative_cost_USD_million']['far_only_text_p11']
    add('quoted_cost_difference', old - far, 'million USD quoted-text arithmetic', 'p11',
        '230 minus148 only; Figure6 endpoint conflicts and fixed-asset/equivalent-service cases remain unresolved.')
    add('quoted_cost_reduction', 100 * (old - far) / old, '% of quoted230 baseline', 'p11',
        'Not a verified saving, NPV, global optimum, GHG benefit or transfer factor.')
    low, high = data['graphic_estimate_Figure6_endpoint_USD_million_range']
    for name, value in [('low', low), ('high', high)]:
        add('graphic_endpoint_minus_quote_' + name, value - old, 'million USD; graphic estimate interval', 'Figure6 p9 / p11',
            'Approximate275–290 visual range, not native data or a corrected author total.',
            'approximate_graphic_comparison_not_corrected_source')

    diameter_ratio = data['reported_max_diameter_m']['far_only'] / data['reported_max_diameter_m']['baseline']
    for name, value, unit in [('reported_max_diameter_ratio', diameter_ratio, 'ratio'),
                              ('reported_max_area_ratio', diameter_ratio**2, 'ratio'),
                              ('constant_friction_loss_ratio', diameter_ratio**-5, 'ratio'),
                              ('Eq9_same_length_CAPEX_ratio', diameter_ratio**data['reported_diameter_exponent'], 'ratio')]:
        add(name, value, unit, 'p11 / Eq9 p6',
            '0.50→0.55m only. Constant-f loss comparison assumes equal flow, density, length and friction; '
            'CAPEX ratio assumes the same dimensional coefficient. Neither is full network cost.')
    initial, final = data['analyst_initial_final_diameter_example_m']
    add('illustrative_initial_to_final_asset_CAPEX_ratio', (final / initial)**1.3, 'ratio', 'Figures9–10 / Eq9',
        'Analyst0.30→0.55m fixed-size illustration, not an authorised replacement design or corrected case cost.',
        'analyst_asset_example_not_author_reproduction')

    example = data['analyst_SI_example']
    pipe = pipeline_example(example)
    units = dict(area='m2', velocity='m/s', reynolds='dimensionless', friction_factor='dimensionless', pressure_loss='Pa')
    for key, value in pipe.items():
        add('analyst_pipeline_' + key, value, units[key], 'Eqs1–2 p5 / unnumbered identities',
            'All example states/geometry are analyst supplied. Positive pressure loss magnitude, '
            'not signed downstream dP/dx, a phase check or author-case reproduction.', 'analyst_SI_unit_example')

    literal = radial_delta_p_squared(example)
    reference = radial_delta_p_squared(example, axisymmetric=True)
    for label, value in [('literal', literal), ('axisymmetric_SI', reference)]:
        add('analyst_radial_deltaP2_' + label, value, 'Pa2', 'Eq5 p6 / independent derivation D01',
            'Constant mu/z/T single-gas radial geometry example with identical log-minus0.75 term. '
            'No dense-phase real-EOS validation or correction of the unpublished author code.', 'analyst_geometry_example')
        add('analyst_radial_BHP_' + label, math.sqrt(example['reservoir_pressure_Pa']**2 + value), 'Pa', 'Eq5 p6',
            'Illustrative absolute-pressure square root only; actual author pressure basis and cases unavailable.',
            'analyst_geometry_example')
    add('literal_to_axisymmetric_pressure_squared_increment_ratio', literal / reference, 'ratio', 'Eq5 p6 / D01',
        'Pi coefficient distinction under explicitly SI axisymmetric assumptions; the Dake passage and author implementation remain unverified.')
    add('analyst_average_pressure_passes', example['reservoir_pressure_Pa'] <= example['frac_pressure_Pa'],
        'boolean', 'Eq4 versus Eq5 pp6/12', 'Illustrative average-pressure test; not the author case.', 'analyst_constraint_counterexample')
    add('analyst_literal_BHP_passes', math.sqrt(example['reservoir_pressure_Pa']**2 + literal) <= example['frac_pressure_Pa'],
        'boolean', 'Eq4 versus Eq5 pp6/12', 'Average can pass while BHP fails. No guarantee follows from average pressure alone.',
        'analyst_constraint_counterexample')

    power = pumping_power_W(example['mass_kg_s'], example['density_kg_m3'], example['pump_delta_Pa'], example['efficiency'])
    add('analyst_pumping_power', power, 'W', 'Eq7 p6',
        'Constant-density pumping approximation. Not a complete near-atmospheric gas-compression work integral.', 'analyst_SI_unit_example')
    add('analyst_electricity_cost', electricity_cost_from_W(power, data['reported_hours_per_year'], example['electricity_USD_kWh']),
        'USD/year at illustrativeUSD/kWh tariff', 'Eq8 p6',
        'SI watts converted to kW before multiplying hours andUSD/kWh. Source power/tariff units are unspecified.', 'analyst_SI_unit_example')
    add('W_to_kW_numeric_factor', 1000, 'ratio', 'Eq8 p6',
        'If W is numerically watts and tariffUSD/kWh, an explicit/implicit1000conversion is needed. '
        'Not proof of an error in unpublished code using kW or another tariff unit.')
    for unit, length in [('km_number', example['length_m'] / 1000), ('m_number', example['length_m'])]:
        add('Eq9_raw_' + unit, raw_capex(example['diameter_m'], length, data['reported_k_capex']),
            'UNASSIGNED monetary unit', 'Eq9 pp6–7',
            'Raw output changes1000fold with length convention. Missing dimensional coefficient/currency year must be resolved.',
            'unit_convention_example_not_author_cost')

    toy = data['analyst_closure_counterexample']
    closure = available_start_does_not_limit_end(toy['start_pressure'], toy['limit'], toy['increment'])
    for key, value in closure.items():
        add('analyst_closure_' + key, value, 'dimensionless toy units', 'Eqs3–4/11–13 pp5–7',
            'Start-only availability can overshoot a within-year limit. This does not establish what the author code does; '
            'native qmax, time indexing, clipping/rescaling and mass conservation remain open.', 'analyst_constraint_counterexample')
    for key, value in data['missing_inputs'].items():
        add(key, value, 'MISSING', 'pp5–13',
            'Missing native inputs/code cannot be filled from plot estimates or analyst examples.', 'not_computable_missing_author_inputs')
    return rows


def main():
    rows = calculate(load_inputs())
    target = ROOT / 'outputs/comprehensive_review/B1-10_diagnostics.csv'
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    print(f'{len(rows)} limited checks; author case/global optimisation/annual service remain unreproduced.')


if __name__ == '__main__':
    main()
