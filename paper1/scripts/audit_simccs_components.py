#!/usr/bin/env python3
"""Reimplement printed functions and expose unit interfaces, not the original MILP.

All example geometry/flows are labelled analyst fixtures. No network or reservoir
inputs are inferred, no pressure formula is silently repaired, and accepted
Paper1 results/inputs are untouched. Uses only the retained publication.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/comprehensive_review'


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B3-44.json').read_text())
    if hashlib.sha256((ROOT / 'papers/B3-44.pdf').read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale SimCCS source')
    return data


def properties(data, temperature_K, pressure_MPa):
    dt = temperature_K-data['fit_origin']['T_K']
    dp = pressure_MPa-data['fit_origin']['P_MPa']
    def evaluate(terms):
        return sum(c*dt**i*dp**j for i,j,c in terms)
    return evaluate(data['eq19_density_kg_m3_terms']), evaluate(data['eq20_viscosity_mPa_s_terms'])


def pressure_drop_literal(data, mass_kg_s, density_kg_m3, length_km, diameter_m):
    # The printed factor8000 includes km→m; dimensional output is Pa.
    return data['published_constants']['friction_factor']*mass_kg_s**2/density_kg_m3*length_km/diameter_m**5*8000/math.pi**2


def radial_mass_kg_s(data, thickness_m, permeability_m2, density_kg_m3, viscosity_mPa_s, delta_pressure_MPa):
    # Footnote6 explicitly distinguishes mPa-s(Eq20) from MPa-s(Eq17).
    viscosity_MPa_s = viscosity_mPa_s*1e-9
    return 2*math.pi*thickness_m/data['published_constants']['log_radius_ratio']*permeability_m2*density_kg_m3/viscosity_MPa_s*delta_pressure_MPa


def diagnostics(data):
    example = data['analyst_unit_example']
    constants = data['published_constants']
    rho, mu = properties(data, 340, 25)
    friction_raw = pressure_drop_literal(data, example['mass_kg_s'], rho, example['pipe_length_km'], example['pipe_diameter_m'])
    head_raw = 1000*rho*constants['gravity_m_s2']*example['depth_km']
    rows = []
    def add(item, value, unit, interpretation, locator='B3-44 p8 Eqs15–23; constants p4; illustrative analyst fixture unless stated'):
        rows.append(dict(item=item, value=value, unit=unit, source_locator=locator, interpretation=interpretation,
                         scope='component_or_dimensional_diagnostic_not_original_California_model'))
    add('fit_origin_density', rho, 'kg/m3', 'Printed Eq19 at T340K/P25MPa; no independent EOS validation.')
    add('fit_origin_viscosity', mu, 'mPa.s', 'Printed Eq20; unit expressly differs from Eq17.')
    add('viscosity_for_Eq17', mu*1e-9, 'MPa.s', 'Explicit mPa→MPa conversion. Omitting it changes radial rate by nine orders of magnitude.')
    add('Eq16_literal_numeric_output', friction_raw, 'Pa by stated SI dimensions', 'Printed factor8000 yields Pa for Lkm/Dm/masskg-s/densitykg-m3, whereas the preceding DeltaP label is MPa.')
    add('Eq16_SI_pressure_expressed_MPa', friction_raw/1e6, 'MPa', 'Dimensional comparison only; not a replacement author input or proof of author-code error.')
    add('Eq18_literal_numeric_output', head_raw, 'Pa by stated SI dimensions', '1000*rho*g*depth_km gives Pa. Conversion is required at an MPa interface.')
    add('Eq18_SI_head_expressed_MPa', head_raw/1e6, 'MPa', 'Unit comparison, not a field measurement.')
    add('Eq15_pump_power_using_SI_pressure', example['mass_kg_s']*(friction_raw/1e6)/rho/constants['pump_efficiency'], 'MW', 'Eq15 with DeltaP in MPa produces MW; pressure-drop example is hypothetical.')
    add('Eq17_radial_fixture_rate', radial_mass_kg_s(data, example['formation_thickness_m'], example['permeability_m2'], rho, mu, example['injection_minus_farfield_MPa']), 'kg/s', 'Steady radial formula with explicit viscosity units; not calibrated injectivity or annual capacity.')
    for depth in (1,2,3):
        drilling = sum(c*depth**(4-i) for i,c in enumerate(data['eq21_drilling_USD_descending_powers']))
        equipping = data['eq22_equipping_USD']['constant']+data['eq22_equipping_USD']['depth_km_coefficient']*depth
        rig = depth*(data['eq23_rig_USD']['depth_km_oil_price_coefficient']*constants['oil_USD_bbl']+data['eq23_rig_USD']['depth_km_coefficient'])
        for label, value in [('drilling',drilling),('equipping',equipping),('rig',rig)]:
            add(f'Eq21_23_{label}_fixture_{depth}km', value, 'source USD basis', 'Analyst depth, printed cost function and stated60USD/bbl; source cost-year/basis not harmonised.')
    table = data['table1']
    total = table['source_count']*table['source_mean_kt_year']/1000
    add('Table1_mean_times_count_source', total, 'Mt/year', 'Rounded summary aggregation; differs from text roughly56Mt/year maximal case; exact input basis unresolved.', 'B3-44 Table1 p5; maximum p6')
    add('Table1_if_mean_were_gross_times_90percent', total*.9, 'Mt/year', 'Conditional alternative interpretation only; not an adopted capture correction.', 'B3-44 Table1 p5; capture90% p4; maximum p6')
    add('Table1_mean_times_count_reservoir', table['reservoir_count']*table['reservoir_mean_kt_stock']/1000, 'Mt stock', 'Lifetime stock, not annual service; retain 25-year distinction.', 'B3-44 Table1 p5; lifetime basis p4')
    return rows


def main():
    data = load_inputs()
    OUT.mkdir(parents=True, exist_ok=True)
    rows = diagnostics(data)
    with (OUT / 'B3-44_diagnostics.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    points = []
    for temperature in data['analyst_fit_evaluation_points']['T_K']:
        for pressure in data['analyst_fit_evaluation_points']['P_MPa']:
            rho, mu = properties(data, temperature, pressure)
            points.append(dict(T_K=temperature, P_MPa=pressure, printed_fit_density_kg_m3=rho,
                               printed_fit_viscosity_mPa_s=mu, scope='analyst_evaluation_not_author_domain_or_EOS_validation'))
    with (OUT / 'B3-44_printed_property_functions.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(points[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(points)
    print(f'Wrote {len(rows)} component/unit diagnostics and {len(points)} analyst fit evaluations; no original MILP reproduction.')


if __name__ == '__main__':
    main()
