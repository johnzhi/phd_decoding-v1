#!/usr/bin/env python3
"""B1-04 unit, heat-flow and reported-rate diagnostics; no GEM reconstruction.

No pressure datum, ton definition, lateral grid size, brine composition, well
hydraulics or unavailable simulator input is inferred. Phase comparisons use
the paper's own approximate thresholds, not a new EOS or density calculation.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/comprehensive_review'
PSI_PA = 6894.757293168
FOOT_M = .3048


def load_inputs():
    data = json.loads((ROOT/'evidence/comprehensive_review_inputs/B1-04.json').read_text())
    if hashlib.sha256((ROOT/data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale deepwater source')
    return data


def fahrenheit_to_celsius(value):
    return (value-32)*5/9


def gradient_K_per_km(value_F_per_100ft):
    # A temperature difference uses5/9, without subtracting32.
    return value_F_per_100ft*5/9/(100*FOOT_M)*1000


def heat_gradient_K_per_km(heat_mW_m2, conductivity_W_m_K):
    return heat_mW_m2/conductivity_W_m_K


def all_weather_risers(table):
    return [name for i,name in enumerate(table['riser_types'])
            if all(table[w][i] for w in ('calm','moderate','rough'))]


def calculate(data):
    rows = []
    def add(item,value,unit,locator,interpretation):
        rows.append(dict(item=item,value=value,unit=unit,source_locator=locator,
                         interpretation=interpretation,
                         scope='diagnostic_not_GEM_riser_model_or_accepted_service_GHG_input'))
    add('Cartesian_grid_cells',math.prod(data['grid_shape']),'cells','p10',
        'Topology only; lateral dimensions, block volumes and boundary conditions unavailable.')
    add('simulation_horizon',data['injection_years']+data['post_injection_years'],'years','p10',
        '250years since injection start; finite simulation is not an infinite-retention proof.')
    for g in (1,2,3,4,6,7,8):
        add(f'gradient_{g}F_per100ft',gradient_K_per_km(g),'K/km','p9/Table3',
            'Temperature-difference and length conversion only.')
    for q in data['heat_flow_mW_m2']:
        for c in data['sediment_conductivity_W_m_K']:
            add(f'Eq1_Q{q}_c{c}',heat_gradient_K_per_km(q,c),'K/km','Eq1 p9',
                'Conditional endpoint combination; conductivity need not be identical across sites. Not a measured site gradient.')
    for site,box in zip(data['sites'],data['figure7_red_near_injector_cell_boxes']):
        tag=f"site{site['site']}"
        rate=site['injection_rate_reported_tons_day']
        annual=rate*365
        add(tag+'_annual_imposed_mass',annual/1e6,'million REPORTED tons/year','Table3 p10',
            '365-day convention. Prescribed rate, not maximum pressure-constrained service; ton definition unconfirmed.')
        add(tag+'_25year_imposed_mass',annual*data['injection_years']/1e6,'million REPORTED tons','p10/Table3',
            'Input schedule arithmetic only. Not a mass-balance or retention output from GEM.')
        add(tag+'_water_depth_m',site['water_depth_ft']*FOOT_M,'m','Table3 p10',
            'Exact length conversion, not verified bathymetry at an operating well.')
        add(tag+'_seabed_pressure_MPa',site['seabed_pressure_psi']*PSI_PA/1e6,'MPa DATUM UNSPECIFIED','Table3 p10',
            'Pressure unit conversion preserves missing gauge/absolute basis. No fracture headroom inferred.')
        add(tag+'_pressure_gradient_psi_ft',site['seabed_pressure_psi']/site['water_depth_ft'],'psi/ft','Table3 p10',
            'Seabed-pressure/depth ratio only, not measured formation gradient or an allowable injection-pressure gradient.')
        temperature=site['seafloor_temperature_F']+site['gradient_F_per_100ft']*site['sediment_thickness_ft']/100
        add(tag+'_conditional_base_temperature_C',fahrenheit_to_celsius(temperature),'degC','Table3; p11',
            'Constant printed geothermal-gradient continuation to328ft. Exact cell temperatures not reproduced.')
        add(tag+'_permeability_range_ratio',site['permeability_mD'][1]/site['permeability_mD'][0],'ratio','Table3 p10',
            'Range endpoints only; not a pressure- or rate-capacity ratio.')
        add(tag+'_reported_red_box_cell_count',math.prod(box),'cells','p11/Figure7',
            'Approximate narrative box count; heterogeneous cell volumes and pore densities unknown. Not a mass or retained fraction.')
    casing=data['casing_conveyance_claim_reported_tons_day']
    add('3000perday_casing_claim_annual',casing*365/1e6,'million REPORTED tons/year','p6',
        'Conveyance estimate, not tested injectivity. Casing wall/ID/velocity/pressure limits absent.')
    base=data['sites'][0]['injection_rate_reported_tons_day']*365
    for mass in data['concept_annual_claim_lower_bounds_reported_tons']:
        add(f'concept_{mass/1e6:g}million_annual_to_single_case_rate',mass/base,'ratio','p5 versus Table3',
            'Scale comparison only; multiple wells/fleet could be intended. No single-well contradiction or validated fleet inferred.')
    add('500000ft3_ship_tank_scale',data['ship_tank_capacity_lower_bound_ft3']*FOOT_M**3,'m3','p5',
        'Volume conversion; cargo density, usable fill, fleet, cycle and reliability not supplied. No tonnes/capacity conversion.')
    deep=data['deep_case']
    linear_F=data['sites'][0]['seafloor_temperature_F']+data['sites'][0]['gradient_F_per_100ft']*deep['injection_depth_below_seafloor_ft']/100
    add('deep_case_constant_gradient_temperature_F',linear_F,'degF','Table3 versus p12',
        'Continuing6F/100ft gives215F versus reported200F. Gradient may vary; full temperature array is needed.')
    add('deep_case_temperature_difference_from_linear',deep['reported_temperature_F']-linear_F,'degF DIFFERENCE','p12 versus Table3',
        'Diagnostic difference, not an assumed corrected case temperature.')
    add('deep_case_depth_to_main_thickness',deep['injection_depth_below_seafloor_ft']/data['sites'][0]['sediment_thickness_ft'],'ratio','p10 versus p12/Figure8',
        'Additional3000ft case needs its own domain/vertical geometry; main328ft model cannot be silently reused.')
    for name,value in [('conclusion_bound',data['conclusion_phase_temperature_F']),('paper_critical_threshold',data['stated_supercritical_temperature_threshold_F']),('deep_case',deep['reported_temperature_F'])]:
        add(name+'_temperature_C',fahrenheit_to_celsius(value),'degC','p4/p12/p13',
            '80F is below the paper own88F approximate supercritical threshold. Neither phase label alone determines brine-relative density.')
    add('deep_case_pressure_MPa',deep['reported_pressure_psi']*PSI_PA/1e6,'MPa DATUM UNSPECIFIED','p12',
        'Unit conversion only; no bottom-hole pressure-control/fracture limit inferred.')
    add('Figure7_8_positive_colourbar_floor',min(data['figure7_and_8_colourbar_mole_fraction']),'global mole fraction','Figures7/8 pp12–13',
        'A positive log colourbar floor does not demonstrate exact zero outside a plume or immobilised mass.')
    for table in data['riser_tables']:
        for weather in ('calm','moderate','rough'):
            add(f'Table{table["table"]}_{weather}_passing_categories',sum(table[weather]),'categories','Tables1/2 p6',
                'Literal qualitative check marks only. Does not reproduce structural loads, stresses, fatigue or availability.')
    return rows


def main():
    rows=calculate(load_inputs())
    OUT.mkdir(parents=True,exist_ok=True)
    with (OUT/'B1-04_diagnostics.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader();writer.writerows(rows)
    print(f'{len(rows)} deepwater diagnostics; original GEM, geostatistical and riser models remain unreproduced.')


if __name__=='__main__':
    main()
