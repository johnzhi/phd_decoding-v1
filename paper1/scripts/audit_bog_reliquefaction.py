#!/usr/bin/env python3
"""B1-19 rounded accounting and printed-parameter diagnostics, without HYSYS.

Reconstructs algebra/accounting components only. No VLE, solid boundary, heat
exchanger, recycle, PSO optimum, APEA equipment case or full lifecycle reproduced.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_inputs():
    data = json.loads((ROOT/'evidence/comprehensive_review_inputs/B1-19.json').read_text())
    if hashlib.sha256((ROOT/data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale BOG source')
    return data


def vapor_mole_fraction(fill_fraction, vapor_to_liquid_molar_volume_ratio):
    """Analytical inversion of Eq1, not a flash or N2 composition model."""
    if not math.isfinite(fill_fraction) or not 0 <= fill_fraction <= 1:
        raise ValueError('Liquid volume fraction must be in[0,1]')
    r = vapor_to_liquid_molar_volume_ratio
    if not math.isfinite(r) or r <= 0:
        raise ValueError('Positive finite molar-volume ratio required')
    return (1-fill_fraction)/((1-fill_fraction)+fill_fraction*r)


def capital_recovery_factor(interest, years):
    if not math.isfinite(interest) or interest < 0 or not math.isfinite(years) or years <= 0:
        raise ValueError('Nonnegative finite interest and positive life required')
    if interest == 0:
        return 1/years
    growth = math.expm1(years*math.log1p(interest))
    return interest*(growth+1)/growth


def percentage(new, baseline):
    if not all(math.isfinite(x) and x >= 0 for x in (new, baseline)) or baseline == 0:
        raise ValueError('Nonnegative values and positive baseline required')
    return dict(remaining_percent=100*new/baseline, reduction_percent=100*(1-new/baseline))


def calculate(data):
    a = data['assumptions']; results = []
    def add(item, value, unit, locator, status, interpretation):
        results.append(dict(item=item, value=value, unit=unit, source_locator=locator,
                            status=status, interpretation=interpretation,
                            scope='no_native_process_or_accepted_operating_GHG_input'))
    sfoc = a['SFOC_g_per_kWh']/1e6  # g/kWh -> metric t/kWh
    ef = sfoc*a['MGO_CO2_t_per_t_fuel']
    crf = capital_recovery_factor(a['interest_rate'], a['life_years'])
    add('compression_MGO_CO2_per_kWh', ef, 'tCO2/kWh', 'Eq5–6 p4; nomenclature p11', 'accounting_component',
        '0.1975kg fuel/kWh times3.206kgCO2/kg fuel. Combustion only, not full lifecycle or actual load-dependent generation.')
    add('capital_recovery_factor', crf, '1/year', 'Eq7 p4', 'accounting_component', '20years/10% source assumptions, no independent APEA equipment cost.')
    add('assumed_annual_unused_calendar_hours', 8760-a['hours_laden']-a['hours_ballast'], 'h/nonleap year', 'pp4,6 / analyst calendar', 'conditional_calendar',
        '760h left under the source8000h assumption. No actual loading, maintenance, idle, weather or route timetable supplied.')
    add('conditional_hours_per_laden_leg', a['hours_laden']/a['voyages_per_year'], 'h/leg if6 annual cycles', 'pp4,6', 'conditional_calendar',
        'Algebraic implication only; no observed voyage length/speed or calendar.')
    baseline = {(r['case'],r['N2_liquid_label_mol_percent']):r for r in data['rows']}
    for r in data['rows']:
        key = f"C{r['case']}_N{r['N2_liquid_label_mol_percent']:g}"
        laden,ballast,total = (r[k] for k in ('laden_CO2_t','ballast_CO2_t','annual_CO2_t'))
        power,purge = r['laden_compression_CO2_t'],r['laden_purge_CO2_t']
        add(key+'_annual_sum_residual', laden+ballast-total, 'tCO2/year', 'Table6 p7', 'rounded_source_arithmetic', 'Three0.1t displayed values; no native annual simulation.')
        add(key+'_laden_partition_residual', power+purge-laden, 'tCO2/year', 'Figure5/Table6 p7', 'rounded_source_arithmetic',
            'Differences within rounding remain visible. Figure labels, not clipped bar heights, are used.')
        add(key+'_ballast_over_laden_percent',100*ballast/laden,'percent','Table6 p7','rounded_source_arithmetic',
            'Ratio to laden emissions, not to annual total or transported cargo.')
        power_kw = power/(ef*a['hours_laden'])
        add(key+'_implied_laden_power', power_kw, 'kW', 'Figure5 + Eq5–6 pp4,7', 'accounting_component',
            'Inverts the displayed combustion partition under source SFOC/hours, not independent compressor or thermodynamic reproduction.')
        if r['figure6_power_kW'][0] is not None:
            co2_kw,ref_kw,total_kw = r['figure6_power_kW']
            add(key+'_power_stack_residual',co2_kw+ref_kw-total_kw,'kW','Figure6 p8','rounded_source_arithmetic','Both gas and refrigerant compression are included.')
            add(key+'_power_to_emission_residual',total_kw*a['hours_laden']*ef-power,'tCO2/year','Figures5–6 pp7–8','accounting_component',
                'Independent unit conversion; four-thousand laden hours and fixed MGO factor, with0.1kW/t rounding.')
        for name in ('tank','other'):
            value = r[name+'_CAPEX_MUSD']*crf-r[name+'_annualized_MUSD']
            add(key+'_'+name+'_annualization_residual',value,'MUSD/year','TableA6 p13; Eq7 p4','accounting_component','Retains source0.01MUSD rounding, not cost re-estimation.')
        add(key+'_TAC_display_residual',r['annualized_CAPEX_MUSD']+r['OPEX_MUSD']-r['TAC_MUSD'],'MUSD/year','Eq9/TableA6 pp6,13','rounded_source_arithmetic','Rounded component sum, no corrected TAC adopted.')
        add(key+'_tax_display_residual',a['carbon_price_USD_per_t']*total/1e6-r['tax_MUSD'],'MUSD/year','Eq11/TableA6 pp6,13','accounting_component','Tax is a scenario, not verified applicable legislation.')
        q = r['transported_kt_per_year']*1000
        cpt = (r['TAC_MUSD']*1e6+a['carbon_price_USD_per_t']*total)/q
        add(key+'_CPT_display_residual',cpt-r['CPT_USD_per_t'],'USD/t transported','Eq13/TableA6 pp6,13','rounded_source_arithmetic','Uses printed TAC and transport denominator; no native cargo-density/heel calculation reproduced.')
        # Interval overlap propagates printed precision instead of requiring rounded sums to match exactly.
        low = ((r['TAC_MUSD']-.005)*1e6+a['carbon_price_USD_per_t']*(total-.05))/(q+50)
        high = ((r['TAC_MUSD']+.005)*1e6+a['carbon_price_USD_per_t']*(total+.05))/(q-50)
        compatible = low <= r['CPT_USD_per_t']+.005 and high >= r['CPT_USD_per_t']-.005
        add(key+'_CPT_rounding_intervals_overlap',int(compatible),'boolean','Eq13/TableA6','rounded_input_interval_check',
            '±0.005MUSD TAC,±0.05t emissions,±50t transport,±0.005USD/t CPT are rounding intervals, not measurement uncertainty.')
        # Ballast emissions partition is unavailable; retain a bound rather than inventing power/purge.
        fuel_cost_laden = power/a['MGO_CO2_t_per_t_fuel']*a['MGO_price_USD_per_t']
        fuel_cost_upper = (power+ballast)/a['MGO_CO2_t_per_t_fuel']*a['MGO_price_USD_per_t']
        add(key+'_conditional_OPEX_lower',fuel_cost_laden/1e6,'MUSD/year','Eq8; Figures5/Table6','nonnegative_ballast_partition_bound','Laden combustion fixes laden fuel. Assumes missing ballast power/purge contributions are nonnegative.')
        add(key+'_conditional_OPEX_upper',fuel_cost_upper/1e6,'MUSD/year','Eq8; Figures5/Table6','nonnegative_ballast_partition_bound','Treats all ballast CO2 as combustion only to bound cost; not an actual ballast allocation.')
        if r['case'][-1] != '1':
            base = baseline[(r['case'][0]+'-1',r['N2_liquid_label_mol_percent'])]
            for metric in ('annual_CO2_t','laden_purge_CO2_t'):
                for name,value in percentage(r[metric],base[metric]).items():
                    add(key+'_'+metric+'_'+name,value,'percent','Table6/Figure5 p7; prose pp8–10','percentage_claim_check','Remaining fraction and reduction are explicitly separate; not a full-chain GHG reduction.')
            if r['case'][-1] == '3':
                base2 = baseline[(r['case'][0]+'-2',r['N2_liquid_label_mol_percent'])]
                for name,value in percentage(power,base2['laden_compression_CO2_t']).items():
                    add(key+'_compression_vs_two_stage_single_'+name,value,'percent','Figure5/prose pp7–8','percentage_claim_check','Printed79.2–84.6%/89.8–95.6% describe remaining power emissions, not percentage reductions.')
    for voyage,groups in data['literal_mixtures_mol_percent'].items():
        for case,mixtures in groups.items():
            for n,components in zip((.05,.10,.15),mixtures,strict=True):
                add(f'{voyage}_C{case}_N{n:g}_mixture_sum',sum(components),'mol%','TablesA1–A2 p12','literal_parameter_diagnostic',
                    'Do not normalize an inconsistent row. Laden1-3,N0.05 sums105%; other rows have displayed rounding.')
    for i,c in enumerate(data['pressure_conflicts'],1):
        add(f'pressure_conflict_{i}_R5_difference',c['table_A1_R5_bar']-c.get('table_A4_R5_bar',c.get('table_A5_R5_bar')),'bar','TablesA1,A4,A5 pp12–13','HOLD_SOURCE_LABEL_CONFLICT',
            'Printed pressure rows disagree/apparently exchange R5/R6. Both retained; no corrected process input adopted.')
    for f in (a['fill_laden'],a['fill_ballast']):
        for ratio in data['analyst_examples']['vapor_to_liquid_molar_volume_ratios']:
            x=vapor_mole_fraction(f,ratio)
            add(f'analyst_fill{f:g}_molar_volume_ratio{ratio:g}_x',x,'vapor mole fraction EXAMPLE','Eq1 p3 / analyst volume ratios','analyst_algebra_example',
                'Mole and volume fractions differ. No actual PR flash, N2 partition or tank state reproduced.')
    return results


def main():
    data=load_inputs();rows=calculate(data);out=ROOT/'outputs/comprehensive_review'
    with (out/'B1-19_checks.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    result=dict(study_id='B1-19',source_sha256=data['source_sha256'],diagnostic_count=len(rows),case_rows=18,
                components_reconstructed=['Eq1 filling-fraction algebra','Eq2 displayed annual sum and Eq5–6 laden combustion conversion','Eq7 capital recovery','Eq9–11 and Eq13 rounded cost/tax/index accounting using reported annual outputs'],
                Eq8_status='literal_power_times_SFOC_price_is_hourly_cost_without_time_factor; annualOPEX_only_bounded_from_available_partitions',
                Eq12_status='reported_transport_totals_used; native_gross_cargo_density_heel_and_purge_calculation_not_reproduced',
                native_HYSYS_PR_flash_recycle_PSO_APEA_or_heat_transfer_model_reproduced=False,accepted_inputs_changed=False,
                missing=data['missing'])
    (out/'B1-19_reconciliation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
