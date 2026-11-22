#!/usr/bin/env python3
"""B3-01 historical accounting and disclosed finance diagnostics; no current law.

Source arithmetic is distinguished from an analyst isolated-cohort cash-flow model.
The author's native Table4 calculation and physical storage models are not reproduced.
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


def domain(release, discount, growth=0):
    if not all(math.isfinite(x) for x in (release,discount,growth)) or not 0<=release<=1 or discount<0 or growth<=-1:
        raise ValueError('Fractional release in [0,1], nonnegative discount and growth > -1 required')


def cohort_value(release, discount, expiry=None, growth=0):
    """P0-normalized value: end-year releases and surviving credit expiry.

    Expiring credits are replaced at T even while carbon stays physically stored.
    The future permanent price grows by (1+growth)^t. The native calculation's
    release basis, renewals, timing and horizon remain unknown.
    """
    domain(release,discount,growth)
    if expiry is not None and (isinstance(expiry,bool) or not isinstance(expiry,int) or expiry<1):
        raise ValueError('Expiry must be a positive integer number of years')
    h=(1+growth)/(1+discount);a=(1-release)*h
    if expiry is None:
        if release==0:return dict(value_fraction=1.,replacement_fraction=0.,physical_retention=1.)
        if a>=1:raise ValueError('Unrestricted replacement PV diverges under these analyst assumptions')
        rc=release*h/(1-a)
        return dict(value_fraction=1-rc,replacement_fraction=rc,physical_retention=0.)
    series=expiry if abs(a-1)<1e-14 else -math.expm1(expiry*math.log(a))/(1-a) if a>0 else 1.
    rc=release*h*series+a**expiry
    return dict(value_fraction=1-rc,replacement_fraction=rc,physical_retention=(1-release)**expiry)


def historical_case(capture_annex,storage_annex,same_country):
    """Mechanical reconstruction of Tables2/3, not a determination of current law."""
    if any(type(x) is not bool for x in (capture_annex,storage_annex,same_country)):
        raise ValueError('Boolean historical group flags required')
    if same_country and capture_annex!=storage_annex:
        raise ValueError('One country cannot be both historical groups in this table')
    if capture_annex and storage_annex:case=1 if same_country else 2
    elif not capture_annex and storage_annex:case=3
    elif capture_annex:case=4
    else:case=5 if same_country else 6
    mechanism='Annex_I_mitigation' if capture_annex else 'CDM'
    liability='storing_country' if storage_annex else 'capturing_country' if capture_annex else 'temporary_credit_buyer'
    return dict(case=case,mechanism=mechanism,proposed_liability=liability)


def mass_ledger(gross_source_t,captured_t,utility_emissions_t,transport_fugitive_t,injection_fugitive_t,storage_release_t):
    values=[gross_source_t,captured_t,utility_emissions_t,transport_fugitive_t,injection_fugitive_t,storage_release_t]
    if any(not math.isfinite(x) or x<0 for x in values) or gross_source_t<=0 or captured_t>gross_source_t:
        raise ValueError('Nonnegative finite masses and capture <= positive gross source required')
    physical_loss=transport_fugitive_t+injection_fugitive_t+storage_release_t
    if physical_loss>captured_t:raise ValueError('Downstream release exceeds captured mass')
    retained=captured_t-physical_loss
    uncaptured=gross_source_t-captured_t
    emitted=uncaptured+utility_emissions_t+physical_loss
    return dict(captured_t=captured_t,retained_t=retained,emitted_t=emitted,avoided_t=gross_source_t-emitted,
                physical_balance_residual_t=gross_source_t-(uncaptured+physical_loss+retained))


def load_inputs():
    d=json.loads((ROOT/'evidence/comprehensive_review_inputs/B3-01.json').read_text())
    if hashlib.sha256((ROOT/d['source_path']).read_bytes()).hexdigest()!=d['source_sha256']:
        raise ValueError('Stale source')
    return d


def calculate(d):
    checks=[]
    def add(item,value,unit,scope):checks.append(dict(item=item,value=value,unit=unit,scope=scope))
    caps={(r['zone'],r['group']):r for r in d['capacity_rows']};cells=[]
    for r in d['capacity_rows']:
        for col,lo,hi in zip(d['capacity_columns'],r['low_Gt'],r['high_Gt']):
            cells.append(dict(zone=r['zone'],group=r['group'],category=col,low_Gt=lo,high_Gt=hi,
                              scope='Native Table1 interval; no probability distribution or annual pressure limit'))
    for zone,col,bound in itertools.product(['onshore','offshore'],range(5),['low_Gt','high_Gt']):
        a=caps[(zone,'Annex_I')][bound][col];b=caps[(zone,'non_Annex_I')][bound][col];t=caps[(zone,'total')][bound][col]
        add(zone+'_'+d['capacity_columns'][col]+'_'+bound+'_closure',a+b-t,'Gt','Printed group endpoint sums, not correlated uncertainty scenarios')
    aggregate={}
    for group,bound in itertools.product(['Annex_I','non_Annex_I','total'],['low_Gt','high_Gt']):
        val=sum(sum(caps[(z,group)][bound]) for z in ['onshore','offshore']);aggregate[(group,bound)]=val
        add(group+'_'+bound+'_sum',val,'Gt','Five listed media columns; saline aquifers have no explicit Table1 column')
    add('range_midpoint',sum(d['native_total_resource_Gt'])/2,'Gt','3178 is only an interval midpoint, not the reported1660 best estimate or an identified statistical mean')
    for bound in ['low_Gt','high_Gt']:
        add('non_Annex_share_'+bound,aggregate[('non_Annex_I',bound)]/aggregate[('total',bound)]*100,'%', 'Paired endpoint totals only; not guaranteed dominance under every joint allocation')
    add('analyst_independent_interval_non_Annex_share_low',aggregate[('non_Annex_I','low_Gt')]/(aggregate[('non_Annex_I','low_Gt')]+aggregate[('Annex_I','high_Gt')])*100,'%', 'Counterexample under independent bounds; native correlation/region allocation unknown')
    rules=d['historical_credit_rules']
    add('historical_energy_renewable_max',rules['energy_renewable_years']*(1+rules['max_renewals']),'years','2006 historical7years plus two renewals; not a physical retention period or current eligibility rule')
    add('historical_forestry_renewable_max',rules['forestry_renewable_years']*(1+rules['max_renewals']),'years','2006 historical20years plus two renewals; not release at expiry')
    classifications=[]
    for row in d['native_classification']:
        got=historical_case(row['capture_annex_I'],row['storage_annex_I'],row['same_country'])
        assert all(got[k]==row[k] for k in got)
        classifications.append(dict(**row,scope='Conditional2006 author classification/proposed liability; current legal applicability unverified'))
    comparisons=[]
    for i,discount_pct in enumerate(d['discount_percent']):
        for j,release_pct in enumerate(d['release_percent']):
            lam,r=release_pct/100,discount_pct/100
            c=cohort_value(lam,r);year_end=c['value_fraction']*100
            year_start=(1-(1+r)*c['replacement_fraction'])*100
            reported=d['table4_value_percent'][i][j]
            comparisons.append(dict(release_percent=release_pct,discount_percent=discount_pct,reported_value_percent=reported,
                analyst_year_end_percent=year_end,analyst_year_start_percent=year_start,
                year_end_minus_reported_pp=year_end-reported,year_start_minus_reported_pp=year_start-reported,
                year_end_within_nearest_tenth=abs(year_end-reported)<=.05+1e-10,
                year_start_within_nearest_tenth=abs(year_start-reported)<=.05+1e-10,
                scope='Disclosed isolated-cohort proportional release models, not native Table4 reproduction or proof of author error'))
    finite=[]
    for release_pct,discount_pct,t in itertools.product(d['release_percent'],d['discount_percent'],d['analyst']['credit_expiry_years']):
        v=cohort_value(release_pct/100,discount_pct/100,expiry=t)
        finite.append(dict(release_percent=release_pct,discount_percent=discount_pct,credit_expiry_year=t,**v,
            scope='Analyst finite-credit cash flows; credit replacement at T does not physically release retained carbon'))
    ledger=mass_ledger(**d['analyst']['ledger'])
    for k,v in ledger.items():add('analyst_ledger_'+k,v,'t','Synthetic gross100/captured90/utility15/transportloss2/storageloss1, not an observed facility inventory')
    rate=d['analyst']['transport_cost_per_t_transported']
    add('analyst_transport_cost_per_t_avoided',rate*ledger['captured_t']/ledger['avoided_t'],'currency/t avoided','2 per captured tonne ×90/72=2.5; not a new native transport cost')
    add('analyst_loss_of_financial_value_without_leakage',cohort_value(0,.01,expiry=21)['value_fraction']*100,'%', 'Zero physical leakage retains100% mass while finite21-year credit value is below100%; no retention factor inferred')
    growth=[]
    for g in d['analyst']['price_growth_examples']:
        try:
            val=cohort_value(d['analyst']['growth_release_fraction'],d['analyst']['growth_discount_fraction'],growth=g)
            growth.append(dict(price_growth_fraction=g,status='convergent',**val))
        except ValueError:
            growth.append(dict(price_growth_fraction=g,status='divergent_PV',value_fraction=None,replacement_fraction=None,physical_retention=None))
    return checks,cells,classifications,comparisons,finite,growth


def main():
    d=load_inputs();checks,cells,classes,comparisons,finite,growth=calculate(d);OUT.mkdir(parents=True,exist_ok=True)
    for label,rows in [('checks',checks),('capacity_cells',cells),('classification',classes),('temporary_values',comparisons),('finite_credit_examples',finite),('price_growth_examples',growth)]:
        with (OUT/f'B3-01_{label}.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    summary=dict(study_id='B3-01',source_sha256=d['source_sha256'],limited_checks=len(checks),capacity_cells=len(cells),classification_cases=len(classes),reported_table4_cells=len(comparisons),finite_credit_examples=len(finite),price_growth_examples=len(growth),
        nonzero_release_cells_not_reconciled_under_analyst_year_end=sum(not x['year_end_within_nearest_tenth'] for x in comparisons if x['release_percent']>0),
        native_Table4_reproduced=False,native_physical_model_reproduced=False,current_legal_status_verified=False,
        limits='Native Table4 timing/release/crediting calculation and original citations remain unverified. Disclosed cash flows, not physical retention or author model reproduction. Historical accounting proposals, not current legal determinations. No accepted operating/GHG input changes.')
    (OUT/'B3-01_reproduction_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
