#!/usr/bin/env python3
"""B1-08 displayed margins, relative bases and explicitly missing inputs.

No PVT/OLGA, corrosion kinetics, wall-temperature, annual-service or full
techno-economic model is reconstructed. Design fractions keep their own-well
denominator; nominal project capacity never supplies a missing well capacity.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/comprehensive_review'


def load_inputs():
    data=json.loads((ROOT/'evidence/comprehensive_review_inputs/B1-08.json').read_text())
    if hashlib.sha256((ROOT/data['source_path']).read_bytes()).hexdigest()!=data['source_sha256']:
        raise ValueError('Stale flow-assurance source')
    return data


def relative_index(change_pct):
    return 1+change_pct/100


def temperature_margin(value_C,minimum_C):
    return value_C-minimum_C


def absolute_well_limit(fraction,own_well_design_capacity):
    return None if own_well_design_capacity is None else fraction*own_well_design_capacity


def calculate(data):
    rows=[]
    def add(item,value,unit,locator,interpretation,status='limited_arithmetic'):
        rows.append(dict(item=item,value=value,unit=unit,source_locator=locator,
                         calculation_status=status,interpretation=interpretation,
                         scope='not_PVT_OLGA_corrosion_TEA_or_accepted_service_GHG_input'))
    for reservoir in data['reservoirs']:
        add(reservoir['name']+'_reported_pressure_span',reservoir['end_pressure_barg']-reservoir['start_pressure_barg'],
            'bar DIFFERENCE','Table1 p3',
            'Difference of approximate reported boundary states; not fracture headroom, maximum allowable pressure or annual injectivity.')
    add('upset_water_content',data['water_spec_ppmv']*data['upset_water_multiplier'],'ppmv','Table3 note p4',
        'Five times the40ppmv normal specification. Not ppm by mass or the full stream composition.')
    add('aqueous_condensate_volume_fraction',data['condensed_aqueous_vol_pct']/100,'volume fraction OF CONDENSATE','p4',
        '0.001vol% becomes1e-5. Not water mole fraction or the85wt%TEG composition of the liquid phase.')
    indices={name:relative_index(change) for name,change in data['corrosion_relative_changes_pct'].items()}
    for name,index in indices.items():
        add(name+'_corrosivity_index',index,'relative index; table baseline=1','Table3 p4',
            'Printed relative corrosion comparison, not an independently reproduced rate or85%inhibition factor.')
    add('upset_TEG_change_in_baseline_percentage_points',
        data['corrosion_relative_changes_pct']['upset_with_TEG']-data['corrosion_relative_changes_pct']['upset_no_TEG'],
        'percentage points of reference','Table3 p4',
        'The0.10point difference is distinct from a relative change against the upset case; comparison basis of the separate>85%claim unresolved.')
    add('upset_TEG_relative_change',100*(indices['upset_with_TEG']/indices['upset_no_TEG']-1),
        '% relative to noTEG upset','Table3 p4',
        'About0.0312%increase from displayed values. Does not independently verify any corrosion mechanism or correct the separate inhibition claim.')
    add('material_test_rate_upper_micrometre_year',data['material_test_corrosion_upper_mm_year']*1000,
        'micrometre/year UPPER BOUND','p4',
        'Unit conversion of reported<0.013mm/year. Test protocol, uncertainty and field extrapolation unavailable.')
    t=data['temperatures_C']
    add('SCSSV_reported_minimum_margin',temperature_margin(data['reported_SCSSV_low_C'],t['SCSSV_min']),
        'K temperature difference','p7',
        'Fluid temperature relative to SCSSV design minimum in the stated steady case, not annual failure probability.')
    add('startup_fluid_relative_to_piping_MDT',temperature_margin(data['startup_downstream_fluid_low_C'],t['piping_min']),
        'K FLUID-versus-design comparison','p11',
        'Fluid−64.6C versus−46C piping threshold. Transient wall temperature/exposure and ramp response are not reproduced; not proof of wall failure.')
    for row in data['figure5_labelled_BHT_points']:
        add('Figure5_'+row['case']+'_BHT_margin',temperature_margin(row['BHT_C'],t['BH_hydrate_min']),
            'K relative to10C criterion','Figure5 p8',
            'Reported labelled temperature point only. Smooth curve shape/optimum or original flow case not independently reproduced.')
    for reservoir,values in data['figure6_labelled_BHT_values'].items():
        for i,value in enumerate(values,1):
            add(f'Figure6_{reservoir}_point{i}_BHT_margin',temperature_margin(value,t['BH_hydrate_min']),
                'K relative to10C criterion','Figure6 p8',
                'Labelled temperature only; unlabelled intermediate xcoordinates not treated as exact operating data.')
    for row in data['figure7_labelled_pressure_points']:
        add(f"Figure7_{row['pressure_barg']}barg_BHT_margin",temperature_margin(row['BHT_C'],t['BH_hydrate_min']),
            'K relative to10C criterion','Figure7 p9',
            'One reported sensitivity curve, not a transferable pressure-to-rate or per-reservoir safety function.')
    for reservoir,fraction in data['early_life_well_capacity_fractions'].items():
        add(reservoir+'_retained_design_fraction',fraction,'fraction OF OWN WELL design capacity','p8',
            'Specific early-life pressure/temperature case. Not a fraction of the2MTPA project target or a constant lifetime/annual factor.')
        add(reservoir+'_design_fraction_reduction',100*(1-fraction),'% OF OWN WELL design capacity','p8',
            'Arithmetic complement, not observed outage, damage, leakage or annual lost storage.')
        add(reservoir+'_absolute_well_limit',absolute_well_limit(fraction,data['well_design_capacity_absolute']),
            'NOT COMPUTABLE','p8',
            'Individual well design capacity missing. Project target and three reservoir categories cannot replace it.',
            'not_computable_missing_own_well_capacity')
    for option in data['options']:
        for key in ('energy_pct','CAPEX_pct','OPEX_pct'):
            add(option['id']+'_'+key+'_index',relative_index(option[key]),'relative index; insulation=1','Table4 p10',
                'Relative displayed value, not absolute duty/cost. Gas option requires changed wells/tubing for equivalent early-life service.')
    add('electric_heater_temperature_lift',t['early_required_arrival']-t['minimum_seabed'],'K','p10 Option2',
        'Temperature lift only. No heat-capacity, enthalpy/flow or heaterMW inferred.')
    add('late_upstream_pressure_increment',data['late_upstream_choke_pressure_barg']-data['early_upstream_choke_pressure_barg'],
        'bar DIFFERENCE','p9',
        'Wellhead/platform boundary change, not a rate uplift or a downhole fracture limit.')
    for key in ('insulation_thickness_m','heater_duty_MW','baseline_energy_absolute','annual_injection_profile'):
        add(key,data[key],'MISSING','pp9–12',
            'U-value is not thickness; relative energy is not absolute duty; transient examples are not an annual schedule.',
            'not_computable_missing_author_inputs')
    gas=next(row for row in data['options'] if row['id']=='gas')
    add('gas_option_extra_GHG',gas['extra_CO2_t_year'],'MISSING; source says Similar','Table4 p10',
        'A qualitative Similar entry is not a numeric zero or a full lifecycle factor.',
        'not_computable_qualitative_GHG_entry')
    return rows


def main():
    rows=calculate(load_inputs())
    OUT.mkdir(parents=True,exist_ok=True)
    with (OUT/'B1-08_diagnostics.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader();writer.writerows(rows)
    print(f'{len(rows)} flow-assurance checks; PVT, corrosion, OLGA and full cost/GHG models remain unreproduced.')


if __name__=='__main__':
    main()
