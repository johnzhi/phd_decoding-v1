#!/usr/bin/env python3
"""B1-20 printed HTX components and output-accounting checks, without COSSMOS.

No native tank/SRK/transfer/compressor/controller model or validation reproduced.
Spray and hydraulic examples are conditional, not invented native states.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def load_inputs():
    data=json.loads((ROOT/'evidence/comprehensive_review_inputs/B1-20.json').read_text())
    if hashlib.sha256((ROOT/data['source_path']).read_bytes()).hexdigest()!=data['source_sha256']:
        raise ValueError('Stale interface source')
    return data


def lmtd(a,b):
    if not all(math.isfinite(x) and x>0 for x in (a,b)):
        raise ValueError('Positive finite terminal temperature differences required')
    if a==b:return a
    if abs(a-b)<.1*b:
        r=(a-b)/b
        return b*r/math.log1p(r)
    return (a-b)/(math.log(a)-math.log(b))


def heater_area(duty_W,U_W_per_m2_K,temperature_difference_K):
    if not all(math.isfinite(x) and x>0 for x in (duty_W,U_W_per_m2_K,temperature_difference_K)):
        raise ValueError('Positive finite duty,U and LMTD required')
    return duty_W/(U_W_per_m2_K*temperature_difference_K)


def heater_cost(area_m2,pressure_bar,a=12003,b=.603,c=1.011187):
    if not all(math.isfinite(x) for x in (area_m2,pressure_bar,a,b,c)) or area_m2<=0 or pressure_bar<0 or a<=0 or c<=0:
        raise ValueError('Positive area/cost factors and nonnegative pressure required')
    return a*area_m2**b*c**pressure_bar


def spray_for_fixed_outlet(outlet_mass,hot_h,target_h,liquid_h):
    if not all(math.isfinite(x) for x in (outlet_mass,hot_h,target_h,liquid_h)) or outlet_mass<=0 or not liquid_h<target_h<hot_h:
        raise ValueError('Positive final flow and liquid_h<target_h<hot_h required')
    return outlet_mass*(target_h-hot_h)/(liquid_h-hot_h)


def calculate(data):
    rows=[];a=data['assumptions']
    def add(item,value,unit,locator,status,note):
        rows.append(dict(item=item,value=value,unit=unit,source_locator=locator,status=status,interpretation=note,
                         scope='not_native_COSSMOS_or_accepted_physical_operating_GHG_input'))
    net_volume=a['ship_tank_count']*a['reference_tank_volume_m3']*(a['initial_fill']-a['heel_fraction'])
    add('conditional_net_liquid_volume',net_volume,'m3','Table1 / Section2.3 p3','conditional_geometry','Three tanks,96-to4% volume; assumes referencegeometry and no density/state change.')
    add('conditional_total_discharge_rate',net_volume/a['duration_h'],'m3/h','Table1 p3','conditional_geometry','Equals reported1679m3/h as a whole-vessel rate; per-tank requirement is a third. Native control/state mapping still needed.')
    add('conditional_per_tank_discharge_rate',net_volume/a['duration_h']/a['ship_tank_count'],'m3/h/tank','Table1/Table2','conditional_geometry','Compare with600m3/h per-tank nameplate; not a verified pump curve or available vessel.')
    for i,lp in enumerate((7,8.5,10)):
        mass=net_volume*a['ship_liquid_density_kg_per_m3'][i]/1000
        add(f'LP{lp:g}_conditional_net_mass',mass,'t','Table1 p3','conditional_geometry','Uses rounded fixed source density; not a corrected Table5 mass or constant24700t case.')
        add(f'LP{lp:g}_Table5_minus_conditional_mass',data['table5_discharged_t'][i]-mass,'t','Tables1,5 pp3,11','mass_basis_diagnostic','Source state/control and transported/gross/net/heel definitions remain unresolved.')
        piston=net_volume*a['ship_vapor_density_kg_per_m3'][i]/1000
        add(f'LP{lp:g}_conditional_piston_minus_VR',piston-data['figure7_VR_t'][i],'t','Table1/Figure7','conditional_geometry','Rounded-density piston estimate only; actual superheat/phase/flow histories are not reproduced.')
        volumetric_rate=net_volume/a['duration_h']/a['ship_tank_count']/3600
        kw=a['ship_liquid_density_kg_per_m3'][i]*9.80665*volumetric_rate*a['pump_head_m']/a['pump_efficiency']/1000
        add(f'LP{lp:g}_conditional_140m_head_pump',kw,'kW/tank','Table2 / analyst hydraulic identity','analyst_hydraulic_example','Assumed full140m head at constant density and selected netflow; not native shaft/motor/system operating point.')
        add(f'LP{lp:g}_ship_cost_residual',data['figure15_ship_kWh_per_t'][i]*a['electric_price_EUR_per_kWh']-data['table5_ship_EUR_per_t'][i],'EUR/t','Figures15–16/Table5','rounded_output_accounting','Electricity-only scenario. No generator fuel or lifecycle intensity inferred.')
        add(f'LP{lp:g}_shore_cost_residual',data['figure16_shore_kWh_per_t'][i]*a['electric_price_EUR_per_kWh']-data['table5_shore_EUR_per_t'][i],'EUR/t','Figures15–16/Table5','rounded_output_accounting','Rounded cost labels; no actual regional supplier or tariff calibration.')
    for i,r in enumerate(data['rows']):
        ilp,imp=divmod(i,3);lp,mp=r['LP_bara'],r['MP_bara'];key=f'LP{lp:g}_MP{mp:g}'
        t=r['table4'];area=heater_area(t['Q_MW']*1e6,a['U_W_per_m2_K'],t['LMTD_K'])
        add(key+'_area_residual',area-t['area_m2'],'m2','Eq2/Table4 pp9–10','printed_component_reconstructed','Q in MW converted to W; not an independently simulated thermal duty.')
        lo=heater_area((t['Q_MW']-.05)*1e6,a['U_W_per_m2_K'],t['LMTD_K']+.05)
        hi=heater_area((t['Q_MW']+.05)*1e6,a['U_W_per_m2_K'],t['LMTD_K']-.05)
        add(key+'_area_rounding_overlap',int(lo<=t['area_m2']+.5 and hi>=t['area_m2']-.5),'boolean','Eq2/Table4','printed_component_rounding','±.05MW,±.05K,±.5m2 are display intervals, not physical uncertainty.')
        cost=heater_cost(t['area_m2'],mp,a['cost_a'],a['cost_b'],a['cost_c'])
        add(key+'_CAPEX_residual',cost-t['cost_EUR'],'EUR','Eq4/Table4','printed_component_reconstructed','Uses numerical terminal pressure in bar and source coefficient units; not a new cost estimate or validated vendor quote.')
        clo=heater_cost(t['area_m2']-.5,mp);chi=heater_cost(t['area_m2']+.5,mp)
        add(key+'_CAPEX_area_rounding_overlap',int(clo<=t['cost_EUR']+.5 and chi>=t['cost_EUR']-.5),'boolean','Eq4/Table4','printed_component_rounding','Rounded-area propagation only; base year,full installation and source cost authority remain unverified.')
        source_heat=data['figure6_heat_kWh_per_t_LP_major'][ilp][imp]
        reconstructed_heat=data['figure14_heater_kWh_per_t_LP_major'][ilp][imp]+data['figure14_vaporizer_kWh_per_t'][ilp]
        add(key+'_Figure14_minus_Figure6_heat',reconstructed_heat-source_heat,'kWh/t','Figures6,14 pp6,10','HOLD_GRAPHIC_SCOPE','Retains4.4 versus10.5 atLP8.5/MP16; other displayed sums agree within rounding. Do not silently replace either graphic.')
        add(key+'_Figure17_minus_Table6_vapor',data['figure17_vapor_t_LP_major'][ilp][imp]-r['table6']['vapor_t'],'t','Figure17/Table6 pp12–13','HOLD_VAPOR_CASE_IDENTITY','Both called displaced vapor; total/excess/gross/net or case mapping not supplied, no resolved correction.')
        for name,table,prefixes in [('no_subcooling',r['table6'],['','with_reliq_']),('subcooling',r['table7'],[''])]:
            base=key+'_'+name
            if name=='no_subcooling':
                add(base+'_power_partition_residual',table['compressor_kW']+table['cooler_kW']-table['total_kW'],'kW','Table6 p13','rounded_output_accounting','Rounded component totals retained without repair.')
                add(base+'_reliq_partition_residual',table['total_kW']+table['reliquefaction_kW']-table['total_with_reliq_kW'],'kW','Table6 p13','rounded_output_accounting','Includes only the stated excess-VR treatment, not all ship/terminal utilities.')
            else:
                total=sum(table[k] for k in ('compressor_kW','cooler_kW','reliquefaction_kW','subcooler_label_kW'))
                add(base+'_signed_partition_residual',total-table['total_kW'],'kW','Table7 p14','HOLD_SIGNED_COOLING_BOUNDARY','Literal sums include−47/−18kW cooler entries. A negative demand is not proven electrical generation; do not clamp or credit as accepted input.')
            for prefix in prefixes:
                power=table['total_with_reliq_kW'] if prefix else table['total_kW']
                specific=power*a['duration_h']/table['liquid_t']
                sfield='specific_with_reliq_label_kWel_per_t' if prefix else 'specific_label_kWel_per_t'
                cfield='cost_with_reliq_EUR' if prefix else 'cost_EUR'
                pfield='cost_with_reliq_per_t_EUR' if prefix else 'cost_per_t_EUR'
                cost=power*a['duration_h']*a['electric_price_EUR_per_kWh']
                add(base+'_'+prefix+'specific_residual',specific-table[sfield],'kWh/t','Tables6–7 pp13–14','HOLD_PRINTED_UNIT','Numerical specific values follow12h energy/mass, although source labels kWel/ton. No changed source label or observedload assumed.')
                add(base+'_'+prefix+'cost_residual',cost-table[cfield],'EUR/operation','Tables6–7','rounded_output_accounting','12h timeskW times0.11EUR/kWh; not annual OPEX or full transfer cost.')
                add(base+'_'+prefix+'specific_cost_residual',cost/table['liquid_t']-table[pfield],'EUR/t','Tables6–7','rounded_output_accounting','Own-case reported liquid mass used, not an assumed common transported service.')
        with_reliq=r['table6'];sub=r['table7']
        exact_no=with_reliq['total_with_reliq_kW']*a['duration_h']*.11/with_reliq['liquid_t']
        exact_sub=sub['total_kW']*a['duration_h']*.11/sub['liquid_t']
        add(key+'_subcooling_minus_reliq_cost_per_t',exact_sub-exact_no,'EUR/t','Tables6–7','case_boundary_comparison','Conditional ranking using different own-case masses. Totalpower,totalcost and cost-per-ton comparisons can differ; not global optimization.')
    add('spray_percent_of_reference_mass',data['spray_report']['liquid_t']/a['reference_mass_t']*100,'percent','Section3.2.3 p8','mass_basis_diagnostic','5.7t is0.0231%of24700t; reported0.025% implies another/rounded net mass basis. Actual spray enthalpies missing.')
    add('spray_report_implied_denominator',data['spray_report']['liquid_t']/(data['spray_report']['reported_percent']/100),'t','Section3.2.3 p8','mass_basis_diagnostic','Implied22800t,near netdischarged quantities; not an adopted correction or independently reproduced5.7t.')
    sample=dict(outlet_mass=10,hot_h=430000,target_h=410000,liquid_h=200000)
    liquid=spray_for_fixed_outlet(**sample)
    add('analyst_fixed_outlet_spray_mass',liquid,'kg/s EXAMPLE','Eq1 / analyst enthalpies','analyst_mixing_component','Synthetic final10kg/s; actual source enthalpies and inlet/outlet mapping missing.')
    add('analyst_fixed_inlet_spray_mass',10*(sample['hot_h']-sample['target_h'])/(sample['target_h']-sample['liquid_h']),'kg/s EXAMPLE','Eq1 / analyst derivation','analyst_mixing_component','Same10kg/s defined as hot INLET instead gives another result; mass reference matters.')
    return rows


def main():
    data=load_inputs();rows=calculate(data);out=ROOT/'outputs/comprehensive_review'
    with (out/'B1-20_checks.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    result=dict(study_id='B1-20',source_sha256=data['source_sha256'],diagnostic_count=len(rows),
                components_reconstructed=['Eq2 area from reported Q/U/LMTD','Eq4 empirical cost using reported area and terminal pressure in bar','12h rounded electricity/cost accounting'],
                other_scope='Eq1 and Eq3 analytically implemented with synthetic inputs; actual spray duty and native HTX temperatures/transfer dynamics missing',
                native_COSSMOS_SRK_tank_transfer_control_compression_or_optimization_reproduced=False,accepted_inputs_changed=False,missing=data['missing'])
    (out/'B1-20_reconciliation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
