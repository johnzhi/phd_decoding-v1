#!/usr/bin/env python3
"""B3-04 source accounting, rounded stocks and conditional EOR recycling.

No native Eclipse model, pressure constraint, process utility balance, optimized
network, current legal eligibility or consequential climate benefit reproduced.
"""
from __future__ import annotations
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/comprehensive_review'


def recycle_balance(injected,produced,recovery_fraction):
    """Mean-flow bookkeeping, with unchanged gross injection/produced CO2.

    Recovered produced CO2 substitutes for fresh supply one-for-one. No process
    losses, recovery duty, inventory transients or oil lifecycle represented.
    """
    if not all(math.isfinite(x) for x in (injected,produced,recovery_fraction)) or not 0<=produced<=injected or not 0<=recovery_fraction<=1:
        raise ValueError('Finite mean flows, 0<=produced<=injected and recovery in [0,1] required')
    recycled=recovery_fraction*produced;fresh=injected-recycled;vent=(1-recovery_fraction)*produced;retained=injected-produced
    return dict(gross_injected_kt_y=injected,produced_kt_y=produced,recovery_fraction=recovery_fraction,
        recycled_kt_y=recycled,fresh_CO2_kt_y=fresh,vented_CO2_kt_y=vent,
        conditional_retained_kt_y=retained,retained_over_fresh=retained/fresh if fresh else None)


def subset_screens(fields,targets):
    """Exhaustive two/three-field mean-rate screens; not schedulable service.

    Targets assume all stated emissions captured. Gross intake and unproduced
    mass are distinct; average rates do not certify annual maxima or reliability.
    """
    rows=[]
    for n in (2,3):
        for group in itertools.combinations(fields,n):
            gross=math.fsum(f['injected_mean_kt_y'] for f in group)/1000
            net=math.fsum(f['injected_mean_kt_y']-f['emitted_mean_kt_y'] for f in group)/1000
            for target,basis in itertools.product(targets,['gross','net']):
                actual=gross if basis=='gross' else net
                rows.append(dict(fields=' + '.join(f['name'] for f in group),count=n,basis=basis,
                    mean_Mt_y=actual,target_Mt_y=target,meets_mean_target=actual>=target,
                    scope='Native mean-rate comparison under full-capture target; not pressure-limited service, paired annual availability or a net climate benefit'))
    return rows


def load_inputs():
    d=json.loads((ROOT/'evidence/comprehensive_review_inputs/B3-04.json').read_text())
    if hashlib.sha256((ROOT/d['source_path']).read_bytes()).hexdigest()!=d['source_sha256']:
        raise ValueError('Stale source')
    return d


def calculate(d):
    checks=[];s=d['native_summary'];a=d['analyst'];fields=d['fields'];eor=d['eor']
    def add(item,value,unit,scope):checks.append(dict(item=item,value=value,unit=unit,scope=scope))
    for name,v in d['native_figure4_percent'].items():add('Figure4_'+name+'_share_sum',sum(v),'percent','Printed slice accounting only; original facilities and category counts unverified')
    sector=math.fsum(d['native_sector_Mt_y'].values())
    add('Figure8_sector_total',sector,'Mt/y','Printed sector labels; mixed precision, source bodies report 5.53/5.5')
    add('Figure8_minus_body_emissions',sector-s['source_emissions_Mt_y'],'Mt/y','0.01 difference is within displayed component rounding, not a corrected total')
    add('power_refinery_share',100*(d['native_sector_Mt_y']['power']+d['native_sector_Mt_y']['refineries'])/sector,'percent','Rounded source values support about 67%; no primary inventory verified')
    add('assets_14DHF_plus5DSA',s['DHF']+s['DSA'],'count','Regional 19-asset count, not 19 qualified injection sites')
    for name,names in [('Sava',['Poljana','Okoli','Iva']),('Drava_Osijek',['Drava','Osijek']),('all',None)]:
        value=math.fsum(x['capacity_Mt'] for x in d['dsas'] if names is None or x['name'] in names)
        add('Table1_DSA_'+name,value,'Mt','Highly theoretical cumulative resource; traps, pressure, efficiency and annual injectivity unresolved')
    total=math.fsum(x['capacity_Mt'] for x in fields);bars=sum(d['native_figure11_capacity_Mt'].values())
    add('Table2_DHF_total',total,'Mt','Sum of fourteen one-decimal source capacities; not a corrected author field model')
    add('Figure11_integer_bar_total',bars,'Mt','Native rounded labels sum 146, matching prose but exceeding Table 2 sum 143.6')
    add('round_before_sum_minus_Table2_total',bars-total,'Mt','Premature individual rounding can explain aggregate difference; preserve both native bases')
    east=math.fsum(x['capacity_Mt'] for x in fields if x['name'] in ['Beničanci','Bokšić'])
    add('Eastern_two_fields_Table2',east,'Mt','Table 2 8.8+13.6=22.4; prose 23 matches 9+14 rounded Figure 11 labels')
    add('Eastern_two_fields_Figure11',sum(d['native_figure11_capacity_Mt'][x] for x in ['Beničanci','Bokšić']),'Mt','No silent substitution between source precision bases')
    add('Molve_plus_Kalinovac_Table2',math.fsum(x['capacity_Mt'] for x in fields if x['name'] in ['Molve','Kalinovac']),'Mt','74.4 agrees with approximate74; no annual service implied')
    add('regional113_plus31',s['DHF_eastern_Mt']+s['DHF_central_Mt'],'Mt','About144 is near143.6,not146; exact field membership not supplied')
    add('Central_Eastern_emissions',s['Central_Mt_y']+s['Eastern_Mt_y'],'Mt/y','2.5+0.86=3.36; full capture is not established')
    for f in fields:
        add('Figure11_rounding_'+f['name'],abs(d['native_figure11_capacity_Mt'][f['name']]-f['capacity_Mt'])<=.5,'bool','Every integer bar is compatible with individual Table2 rounding; sums use different precision')
    for f in eor:
        for metric in ['injected','emitted','oil']:
            lo,hi,mean=[f[f'{metric}_{key}_kt_y'] for key in ['min','max','mean']]
            if lo is None:continue
            add('range_'+f['name']+'_'+metric,lo<=mean<=hi,'bool','Marginal min/mean/max order only; extrema years are not paired')
    derived=[];recycling=[];stock=[]
    for f in eor:
        inj=f['injected_mean_kt_y'];produced=f['emitted_mean_kt_y'];net=inj-produced
        derived.append(dict(field=f['name'],gross_injected_kt_y=inj,produced_vented_kt_y=produced,
            conditional_unproduced_kt_y=net,produced_over_injected=produced/inj,
            unproduced_over_injected=net/inj,unproduced_t_per_oil_t=net/f['oil_mean_kt_y'],
            scope='Shared averaging window/weights assumed; not lifecycle avoidance,physical permanence or pressure-limited annual service'))
        for frac in a['recycle_fractions']:
            recycling.append(dict(field=f['name'],**recycle_balance(inj,produced,frac),scope='Analyst recovery fraction; gross rates held fixed, no process duty/dynamics/pressure or fossil-oil counterfactual'))
        cap=next(x['capacity_Mt'] for x in fields if x['name']==f['name'])
        stock.append(dict(field=f['name'],Table2_capacity_Mt=cap,
            analyst_duration_years=a['diagnostic_year_difference'],conditional_mean_net_times_duration_Mt=net*a['diagnostic_year_difference']/1000,
            ratio_to_Table2_capacity=net*a['diagnostic_year_difference']/1000/cap,
            scope='15=2040−2025 analyst screen,not native integration; static hydrocarbon replacement and dynamic EOR inventories differ and require reconciliation,not proof of a physical violation'))
    I=math.fsum(f['injected_mean_kt_y'] for f in eor);P=math.fsum(f['emitted_mean_kt_y'] for f in eor)
    add('sum_native_mean_gross',I/1000,'Mt/y','Seven unconstrained mean scenarios together,not a sized supply-matched network')
    add('sum_native_mean_produced_vented',P/1000,'Mt/y','Native baseline produced CO2 is vented; recovery is a separate conditional scenario')
    add('sum_native_mean_unproduced',(I-P)/1000,'Mt/y','Linearity requires common averaging periods/weights; no full lifecycle carbon ledger')
    add('aggregate_unproduced_fraction',100*(I-P)/I,'percent','About42% is compatible with source around40%; not a generic CCS retention/avoidance factor')
    add('unweighted_mean_produced_fraction',100*math.fsum(f['emitted_mean_kt_y']/f['injected_mean_kt_y'] for f in eor)/len(eor),'percent','Generic40–60% description need not bound every field; Lipovljani is about29%')
    ratios=[dict(item='Eastern_Table2_stock_over_emission',quotient_years=east/s['Eastern_Mt_y'],scope='Stock/rate quotient only,no service,pressure,availability or reliability validation'),dict(item='Eastern_prose_stock_over_emission',quotient_years=s['Eastern_Benicanci_Boksic_Mt']/s['Eastern_Mt_y'],scope='Different rounded source basis, no prediction of operating life')]
    combos=subset_screens(eor,a['allocation_targets_Mt_y'])
    return checks,derived,recycling,stock,ratios,combos


def main():
    d=load_inputs();checks,derived,recycling,stock,ratios,combos=calculate(d);OUT.mkdir(parents=True,exist_ok=True)
    for suffix,rows in [('checks',checks),('eor_means',derived),('recycle_examples',recycling),('stock_screens',stock),('stock_rate_quotients',ratios),('subset_screens',combos)]:
        with (OUT/f'B3-04_{suffix}.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    result=dict(study_id='B3-04',source_sha256=d['source_sha256'],limited_checks=len(checks),mean_EOR_rows=len(derived),conditional_recycle_rows=len(recycling),conditional_stock_screens=len(stock),stock_rate_quotients=len(ratios),subset_mean_screens=len(combos),
        ambiguous_Lipovljani_emitted_min='Native0 23 retained; numeric value excluded',
        universal_subset_claim_verified=False,native_Eclipse_or_optimized_network_reproduced=False,
        original_sources_verified=0,pressure_constrained_annual_service_established=False,
        limits='Arithmetic and analyst bookkeeping only. Confidential static/well/PVT/native cases and time-resolved controls unavailable. Gross injection,produced/vented mass,unproduced stock and lifecycle avoidance differ. No numeric interpretation for0 23,no minimum/maximum net flow from unpaired extrema,no automatic current field availability,no new accepted operating/GHG input.')
    (OUT/'B3-04_reproduction_summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
