#!/usr/bin/env python3
"""B1-07 topology, calendar and relative-index checks; no reservoir replay.

No absolute tonnes, pressure limits, annual profiles, selected-realisation
probabilities or relief-water inventories are inferred from unscaled plots.
"""
import csv
from datetime import date
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/comprehensive_review'


def load_inputs():
    data=json.loads((ROOT/'evidence/comprehensive_review_inputs/B1-07.json').read_text())
    if hashlib.sha256((ROOT/data['source_path']).read_bytes()).hexdigest()!=data['source_sha256']:
        raise ValueError('Stale Higashi-Niigata source')
    return data


def elapsed_days(start,end):
    return (date.fromisoformat(end)-date.fromisoformat(start)).days


def relative_total_bounds(baseline,uplift_pct):
    if baseline is None:
        return None,None
    return tuple(baseline*(1+p/100) for p in uplift_pct)


def calculate(data):
    rows=[]
    def add(item,value,unit,locator,interpretation,status='limited_diagnostic'):
        rows.append(dict(item=item,value=value,unit=unit,source_locator=locator,
                         calculation_status=status,interpretation=interpretation,
                         scope='not_original_reservoir_forecast_or_accepted_rate_pressure_GHG_input'))
    cells=math.prod(data['grid_dimensions'])
    add('total_grid_topology_cells',cells,'cells','Table3 p4',
        'Grid topology product only; not pore volume or a uniform cell-geometry assumption.')
    add('inactive_topology_cells',cells-data['active_grid_cells'],'cells','Table3 p4',
        'Arithmetic count difference, not a physical inactive-volume estimate.')
    add('active_cell_count_fraction',data['active_grid_cells']/cells,'count fraction','Table3 p4',
        'Not net-to-gross, porosity, storage efficiency or a volume-weighted fraction.')
    extent=data['model_extent']
    add('model_bounding_box_volume',extent['length_km']*extent['width_km']*extent['height_m']/1000,
        'km3 GROSS bounding box','Table3 p4',
        'No active/pore/storage volume follows without cell dimensions, masks and rock/fluid properties.')
    add('selected_realisation_count_fraction',data['realizations_selected']/data['realizations_generated'],
        'count fraction','p4/p5',
        'Selection frequency only. Not model accuracy, confidence level, probability mass or a calibrated uncertainty bound.')
    for label,start,end in [('injection',data['simulation_start'],data['injection_end']),
                            ('post_injection',data['injection_end'],data['simulation_end']),
                            ('full_simulation',data['simulation_start'],data['simulation_end']),
                            ('history_to_injection',data['history_match_end'],data['simulation_start'])]:
        add(label+'_calendar_days',elapsed_days(start,end),'calendar days','p5/Table8 p6',
            'Date difference only. No observed availability, production schedule or pressure-controlled service inferred.')
    for case in ('A','B'):
        row=data['case_'+case]
        add(case+'_listed_scenario_wells',row['injectors']+row['relief_wells'],'listed injection/relief wells',
            'Table8 p6',
            'Does not count every legacy well or validate actual operations/assets.')
    add('additional_relief_wells_B_minus_A',data['case_B']['relief_wells']-data['case_A']['relief_wells'],
        'listed wells','Table8 p6',
        'Water handling, assets, energy, treatment and costs are not supplied by this count.')
    bounds=relative_total_bounds(1,data['reported_uplift_pct'])
    for name,value in zip(('low','high'),bounds):
        add('B_to_A_normalised_total_'+name,value,'relative index; A=1 ONLY','p8/ Figure17 p9',
            'Analyst-normalised expression of reported25–30% cumulative uplift. Not absolute mass or an annual multiplier.')
    missing_bounds=relative_total_bounds(data['absolute_case_A_total'],data['reported_uplift_pct'])
    for name,value in zip(('low','high'),missing_bounds):
        add('B_absolute_total_'+name,value,'source CO2_ton SCALE UNAVAILABLE','Figures11/17',
            'No numerical vertical scale or absolute baseline; unknown stays missing, not zero or a guessed Mt case.',
            'not_computable_missing_absolute_baseline')
    add('initial_pressure_limit',data['initial_reservoir_pressure_MPa'],'MPa REFERENCE UNRESOLVED','Table8/Figure19',
        'Initial pressure numerical value, datum/reference date and well/field control implementation are unavailable.',
        'not_computable_missing_pressure_definition')
    add('annual_injection_profile',data['annual_injection_profile'],'NOT AVAILABLE','Figures11/17',
        'Cumulative relative uplift does not establish annual flow or zero injection after the approximate2040 constraint time.',
        'not_computable_missing_annual_outputs')
    add('pressure_relief_water_inventory',data['relief_water_inventory'],'NOT AVAILABLE','p8',
        'No production volume, salinity, gas content, treatment or pumping inventory for the pressure-relief comparison.',
        'not_computable_missing_process_outputs')
    return rows


def main():
    rows=calculate(load_inputs())
    OUT.mkdir(parents=True,exist_ok=True)
    with (OUT/'B1-07_diagnostics.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader();writer.writerows(rows)
    print(f'{len(rows)} Higashi-Niigata checks including explicit missing quantities; author reservoir cases remain unreproduced.')


if __name__=='__main__':
    main()
