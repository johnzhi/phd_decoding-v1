#!/usr/bin/env python3
"""Limited B1-06 pressure-unit, interval and Figure2 algebra checks.

No failure probability, rate penalty, actual BHP, mobile mass or proprietary
THM model is inferred. US gallons and standard gravity are explicit analyst
unit conventions. Depth intervals remain approximate measured-depth spans.
"""
import csv
from datetime import date
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'outputs/comprehensive_review'
LB_KG = .45359237
US_GALLON_M3 = .003785411784
GRAVITY_M_S2 = 9.80665
PSI_PA = 6894.757293168
FOOT_M = .3048


def load_inputs():
    data=json.loads((ROOT/'evidence/comprehensive_review_inputs/B1-06.json').read_text())
    if hashlib.sha256((ROOT/data['source_path']).read_bytes()).hexdigest()!=data['source_sha256']:
        raise ValueError('Stale openhole source')
    return data


def ppg_to_pa_per_m(ppg):
    return ppg*LB_KG/US_GALLON_M3*GRAVITY_M_S2


def ppg_to_psi_per_ft(ppg):
    return ppg_to_pa_per_m(ppg)*FOOT_M/PSI_PA


def hoop_extrema(SHmax,SHmin,Pw,P0):
    """Literal Figure2 expressions, all pressures on the same basis.

    This does not add thermal/poroelastic terms, a stress rotation, material
    strengths or any failure criterion omitted from the source sketch.
    """
    return 3*SHmin-SHmax-Pw-P0, 3*SHmax-SHmin-Pw-P0


def interval_lengths(intervals):
    pairs=sorted((row['from_ftMD'],row['to_ftMD']) for row in intervals)
    if any(low>high for low,high in pairs):
        raise ValueError('Reversed depth interval')
    summed=sum(high-low for low,high in pairs)
    merged=[]
    for low,high in pairs:
        if merged and low<=merged[-1][1]:
            merged[-1][1]=max(merged[-1][1],high)
        else:
            merged.append([low,high])
    union=sum(high-low for low,high in merged)
    return summed,union,summed-union


def calculate(data):
    rows=[]
    def add(item,value,unit,locator,interpretation):
        rows.append(dict(item=item,value=value,unit=unit,source_locator=locator,
                         interpretation=interpretation,
                         scope='diagnostic_not_THM_failure_prediction_or_accepted_rate_GHG_input'))
    add('one_ppg_exact_USgal_gradient',ppg_to_psi_per_ft(1),'psi/ft perppg','analyst unit derivation',
        'Explicit pound/USgal and standard-gravity convention, not CO2 fluid density or a source-stated pressure datum.')
    for case in data['cases']:
        name=case['id'];g=case['gradient_ppg'];locator=f"Figure{case['figure']} p{case['page']}"
        add(name+'_pressure_gradient_SI',ppg_to_pa_per_m(g)/1000,'kPa/m',locator,
            'Conditional USgal equivalent-gradient conversion. Not an actual fluid density, BHP or fracture-pressure headroom.')
        add(name+'_pressure_gradient_US',ppg_to_psi_per_ft(g),'psi/ft',locator,
            'MD must not substitute for TVD; a depth/datum convention is needed before actual pressure can be inferred.')
        add(name+'_industry_rounded_gradient',.052*g,'psi/ft',locator,
            'Comparison using the familiar rounded0.052 coefficient, not a corrected author value.')
        if case['failure_intervals']:
            summed,union,overlap=interval_lengths(case['failure_intervals'])
            for label,value in [('sum_mode_spans',summed),('union_spans',union),('overlap_spans',overlap)]:
                add(name+'_'+label,value,'approximate ftMD SPAN',locator,
                    'Caption endpoint arithmetic only; not damaged rock volume, fracture height, leakage, outage or a mass/rate fraction.')
    cases={case['id']:case for case in data['cases']}
    for year in (2025,2030,2048):
        injection=cases[f'{year}_inject']['gradient_ppg'];stop=cases[f'{year}_stop']['gradient_ppg']
        difference=injection-stop
        add(f'{year}_gradient_support_change',difference,'ppg equivalent difference','Figures5–10 pp3–5',
            'Wellbore injection versus source-labelled stopped pore-pressure gradient. Variable/pressure-support distinction preserved.')
        add(f'{year}_gradient_relative_difference',100*difference/injection,'% of injection-gradient equivalent','Figures5–10 pp3–5',
            'Descriptive gradient ratio only. Never an outage probability, injectivity loss or annual service reduction.')
    for year,delta_F in data['cooling_reduction_degF'].items():
        add(f'{year}_cooling_difference_K',delta_F*5/9,'K DIFFERENCE','p5 discussion',
            'Temperature reduction converts by5/9 without subtracting32. Absolute injection/reservoir temperatures not reconstructed.')
    initial=date.fromisoformat(data['figure1']['export_dates'][0])
    for stamp in data['figure1']['export_dates'][1:]:
        add(stamp+'_days_after_first_export',(date.fromisoformat(stamp)-initial).days,'calendar days between exports','Figure1 p2',
            'Export timestamps, not a verified injection-start calendar. Nominal year offsets are not silently treated as exact elapsed service.')
    add('Figure2_hoop_anisotropy_multiplier',4,'dimensionless coefficient','Figure2 p3',
        'Literal max-minus-min equals4(SHmax−SHmin). No field stresses or strength thresholds inferred.')
    add('Figure2_fixed_stress_dhoop_dPw',-1,'dimensionless sensitivity','Figure2 p3',
        'For both printed extrema with SHmax,SHmin,P0 held fixed. Actual coupled stress changes are not held fixed in the author model.')
    add('Figure2_fixed_stress_dhoop_dP0',-1,'dimensionless sensitivity','Figure2 p3',
        'Provisional pore-pressure meaning ofP0; source original and complete poroelastic convention unverified.')
    return rows


def main():
    rows=calculate(load_inputs())
    OUT.mkdir(parents=True,exist_ok=True)
    with (OUT/'B1-06_diagnostics.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader();writer.writerows(rows)
    print(f'{len(rows)} openhole diagnostics; original thermal/geomechanical/failure and liner models remain unreproduced.')


if __name__=='__main__':
    main()
