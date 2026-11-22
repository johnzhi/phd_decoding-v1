#!/usr/bin/env python3
"""B3-03 limited freight arithmetic and conditional buffer/boundary examples.

No legal classifier, current-law verification, QRA or author process model.
No phase/density/scheduling assumptions enter the accepted Paper1 inputs.
"""
from __future__ import annotations
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/comprehensive_review'


def percentage_interval(numerator, denominator, halfwidth, decline=False):
    """Bounds from two independently rounded positive native quantities.

    This is a rounding envelope, not a statistical confidence interval.
    """
    if not all(math.isfinite(x) for x in (numerator, denominator, halfwidth)) or halfwidth < 0 or numerator < halfwidth or denominator <= halfwidth:
        raise ValueError('Finite nonnegative numerator and positive denominator bounds required')
    lower = 100 * (numerator-halfwidth)/(denominator+halfwidth)
    upper = 100 * (numerator+halfwidth)/(denominator-halfwidth)
    return (100-upper, 100-lower) if decline else (lower, upper)


def buffer_example(ship_m3, multiplier, density_kg_m3, annual_mass_t, days_year):
    """Analyst constant-density, uniform-throughput equivalent capacity days.

    Neither actual residence time nor an operationally sufficient buffer.
    """
    if any(not math.isfinite(x) or x <= 0 for x in (ship_m3, multiplier, density_kg_m3, annual_mass_t, days_year)):
        raise ValueError('All example inputs must be finite and positive')
    volume = ship_m3 * multiplier
    mass = volume * density_kg_m3 / 1000
    return dict(ship_m3=ship_m3, buffer_ship_multiplier=multiplier,
                analyst_density_kg_m3=density_kg_m3, buffer_m3=volume,
                conditional_buffer_t=mass,
                equivalent_uniform_throughput_days=mass/(annual_mass_t/days_year),
                scope='Analyst constant density and full volume; no filling fraction, reserve, weather, port dwell, schedule or native density verified')


def handling_example(domestic_mass, imports_mass, domestic_UK_events):
    """Conditional UK handling-event count, not verified DfT statistics rules.

    Illustrates a boundary distinction only. One event for each imported tonne.
    """
    if min(domestic_mass, imports_mass) < 0 or domestic_UK_events not in (1, 2):
        raise ValueError('Nonnegative flows and one/two domestic handling events required')
    return dict(domestic_UK_events_per_tonne=domestic_UK_events,
                physical_CO2_Mt_per_y=domestic_mass+imports_mass,
                conditional_UK_handling_Mt_per_y=domestic_mass*domestic_UK_events+imports_mass,
                scope='If each UK load/unload is counted separately; illustrative direct-offshore versus domestic port-to-port boundary, not an established freight convention or forecast')


def load_inputs():
    d = json.loads((ROOT/'evidence/comprehensive_review_inputs/B3-03.json').read_text())
    if hashlib.sha256((ROOT/d['source_path']).read_bytes()).hexdigest() != d['source_sha256']:
        raise ValueError('Stale source')
    return d


def calculate(d):
    f=d['native_freight_Mt'];s=d['native_scenarios'];a=d['analyst'];rep=d['reported_percentages']
    definitions=[
        ('Southampton_total_share','Southampton_total_2023','UK_total_2023',False,1),
        ('Southampton_liquid_bulk_share','Southampton_liquid_bulk_2023','UK_liquid_bulk_2023',False,1),
        ('UK_liquid_bulk_decline_2022_2023','UK_liquid_bulk_2023','UK_liquid_bulk_2022',True,2),
        ('Southampton_liquid_bulk_decline_2022_2023','Southampton_liquid_bulk_2023','Southampton_liquid_bulk_2022',True,2),
        ('UK_liquid_gas_share_of_liquid_bulk','UK_liquid_gas_2023','UK_liquid_bulk_2023',False,2),
        ('Southampton_liquid_gas_share_of_UK_liquid_gas','Southampton_liquid_gas_2023','UK_liquid_gas_2023',False,2)]
    percentages=[]
    for name,n,den,decline,precision in definitions:
        central=100*(1-f[n]/f[den]) if decline else 100*f[n]/f[den]
        lo,hi=percentage_interval(f[n],f[den],a['report_rounding_halfwidth_Mt'],decline)
        half=.5*10**(-precision)
        percentages.append(dict(item=name,numerator_Mt=f[n],denominator_Mt=f[den],decline=decline,
            calculated_percent=central,reported_percent=rep[name],rounding_lower_percent=lo,
            rounding_upper_percent=hi,rounding_compatible=lo<=rep[name]+half and hi>=rep[name]-half,
            scope='Printed arithmetic/rounding only; original freight series and commodity definitions unverified'))
    checks=[
        dict(item='2035_scenario_components',value=s['UK_2035_domestic_capture_Mt_per_y']+s['UK_2035_imports_Mt_per_y'],unit='Mt/y',scope='15 domestic +20 import =35 physical CO2 scenario, not observed freight or annual injection service'),
        dict(item='scenario35_over2023_all_liquid_gases',value=s['UK_2035_total_Mt_per_y']/f['UK_liquid_gas_2023'],unit='ratio',scope='Different dates/commodities and scenario basis; neither forecast probability nor proof of a specific freight increase'),
        dict(item='Solent_constant_daily_analyst_rate',value=s['Solent_source_case_Mt_per_y']*1e6/a['days_per_year'],unit='t/day',scope='Uniform 365-day analyst schedule from cited5.9Mt/y case; not a timestamped terminal operating series')]
    buffers=[buffer_example(v,k,a['density_kg_per_m3'],s['Solent_source_case_Mt_per_y']*1e6,a['days_per_year']) for v,k in itertools.product(s['source_case_ship_volume_m3'],s['source_case_buffer_ship_multipliers'])]
    handling=[handling_example(s['UK_2035_domestic_capture_Mt_per_y'],s['UK_2035_imports_Mt_per_y'],n) for n in (1,2)]
    return percentages,checks,buffers,handling


def main():
    d=load_inputs();percentages,checks,buffers,handling=calculate(d);OUT.mkdir(parents=True,exist_ok=True)
    for suffix,rows in [('freight_percentages',percentages),('checks',checks),('buffer_examples',buffers),('handling_examples',handling)]:
        with (OUT/f'B3-03_{suffix}.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    result=dict(study_id='B3-03',source_sha256=d['source_sha256'],limited_percentage_checks=len(percentages),rounding_compatible=sum(x['rounding_compatible'] for x in percentages),additional_arithmetic_checks=len(checks),conditional_buffer_examples=len(buffers),conditional_handling_examples=len(handling),native_quantitative_model_reported=False,current_legal_status_verified=False,original_sources_verified=0,
        limits='Qualitative legal synthesis and recommendations, not a QRA or current permission. Freight checks do not verify underlying series; density, throughput and handling-event assumptions are illustrative. Generic unpaired pressure/temperature ranges,24h notice and other-gas thresholds are not operational constraints. No native model or cited source chain reproduced; no accepted operating/GHG input changes.')
    (OUT/'B3-03_reproduction_summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
