#!/usr/bin/env python3
"""Check printed cost conventions, integration bounds and a CDF inference.

The analytical CDF example uses analyst distributions, not the author's data.
No absent supplementary input, raw KPI, weight or utility balance is invented.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/comprehensive_review'


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B1-01.json').read_text())
    if hashlib.sha256((ROOT / 'papers/B1-01.pdf').read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale OCCS source')
    return data


def annuity_factors(rate, years):
    present = (1-(1+rate)**(-years))/rate
    return present, 1/present


def annual_electricity_co2_t(power_kW, hours, kg_per_kWh):
    return power_kW*hours*kg_per_kWh/1000


def uniform_cdf(x, low, high):
    return min(1, max(0, (x-low)/(high-low)))


def counterexample_inversion_probability(data):
    a0,a1 = data['CDF_counterexample']['A_uniform_support']
    b0,b1 = data['CDF_counterexample']['B_uniform_support']
    # These declared supports overlap with a0 <= b0 < a1 <= b1.
    if not a0 <= b0 < a1 <= b1:
        raise ValueError('This analytical integral requires ordered overlapping supports')
    return (a1-b0)**2/(2*(a1-a0)*(b1-b0))


def calculate(data):
    rows = []
    def add(item, value, unit, locator, interpretation):
        rows.append(dict(item=item, value=value, unit=unit, source_locator=locator,
                         interpretation=interpretation,
                         scope='component_or_method_diagnostic_not_original_Aspen_hazard_or_MC_model'))
    present, recovery = annuity_factors(data['discount_fraction'], data['economic_life_years'])
    capex = (1+data['TIPC_to_TDPC'])*data['TDPC_to_TEC']/data['capex_to_FCI_divisor']
    add('annuity_present_value_factor', present, 'years', 'Eqs2/8 p4; Table2', 'Ordinary annual cash-flow factor using the printed8%/25years.')
    add('capital_recovery_factor', recovery, 'year^-1', 'Eq8 p4', 'Reciprocal of the Eq2 present-value factor.')
    add('CAPEX_divided_by_TEC', capex, 'ratio', 'Eqs3–7 p4', 'Printed cost multipliers; equipment costs and VOPEX absent.')
    fraction = data['FOPEX_to_annualised_CAPEX']*recovery
    add('annual_FOPEX_divided_by_CAPEX', fraction, 'year^-1', 'Eq8 p4', 'Literal0.03×annualisedCAPEX, not an assumed0.03×CAPEX annual cost.')
    add('PV_FOPEX_divided_by_CAPEX', fraction*present, 'ratio', 'Eqs2/8 p4', 'Exactly0.03 algebraically; unusual convention preserved without an author-code correction.')
    add('NPC_without_VOPEX_divided_by_CAPEX', 1+fraction*present, 'ratio', 'Eqs2/8 p4', 'Only the printed fixed-cost component; not either full process NPC.')
    add('one_kW_annual_direct_CO2', annual_electricity_co2_t(1,data['annual_operating_hours'],data['onboard_electricity_kg_CO2_per_kWh']), 't/year per kW', 'Eq11/Table3 p4; schedule p6', 'Explicit kW×h×kg/kWh→t/year interface. Raw EF×kW alone iskg/hour.')
    add('nominal_voyage_equivalents', data['annual_operating_hours']/(data['voyage_days']*24), 'equivalents/year', 'Case p6', 'Accounting ratio, not observed annual availability or a discrete voyage schedule.')
    for row in data['table8']:
        add(row['concept']+'_cold_duty_to_available', row['cold_MW']/data['LNG_cold_available_MW'], 'ratio', 'Table8 p9; p7 LNG duty', 'Necessary total-duty test only. Passing does not reproduce a heat-exchanger pinch profile.')
    for row in data['table7']:
        if row['electric_MJ_per_kg_avoided'] is not None:
            add(row['concept']+'_electric_kWh_per_t_avoided', row['electric_MJ_per_kg_avoided']*1000/3.6, 'kWh/t AVOIDED', 'Table7 p8', 'Unit conversion only. Never relabelled per captured tonne or transferred into accepted inventory.')
    add('Table9_IN_AS_to_A3C_ratio', data['table9_OSI']['AS'][0]/data['table9_OSI']['A3C'][0], 'ratio', 'Table9 p10', 'Reconstructs reported2.5×individualist OSI; does not reproduce missing weighting inputs.')
    add('analyst_CDF_counterexample_P_A_exceeds_B', counterexample_inversion_probability(data), 'probability in analyst example ONLY', 'Method inference discussed p12; analyst U[0,.8]/U[.2,1]', 'Noncrossing marginalCDFs permit positive paired inversion. Not an estimated author-case probability; raw paired SF traces needed.')
    return rows


def main():
    data = load_inputs()
    rows = calculate(data)
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / 'B1-01_diagnostics.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    print(f'Wrote {len(rows)} OCCS diagnostics; complete author models remain unreproduced.')


if __name__ == '__main__':
    main()
