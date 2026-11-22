#!/usr/bin/env python3
"""B3-02 historical money arithmetic and disclosed pool/funding examples.

No current law, actuarial calibration, transfer certificate or author model is
reproduced. The paper reports a qualitative legal synthesis and policy proposal.
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


def two_site_pool(probability,severity,funds,correlation_mixture):
    """Mixture of independent and common Bernoulli site events, positive dependence.

    Four exact atoms; synthetic dimensionless losses, not measured CCS hazards.
    Pool availability changes payment/shortfall, not the underlying loss.
    """
    if not all(math.isfinite(x) for x in (probability,severity,funds,correlation_mixture)) or not 0<=probability<=1 or min(severity,funds)<0 or not 0<=correlation_mixture<=1:
        raise ValueError('Probability/mixture in [0,1] and finite nonnegative money required')
    p,c=probability,correlation_mixture;atoms=[]
    for a,b in itertools.product([0,1],repeat=2):
        independent=(p if a else 1-p)*(p if b else 1-p)
        common=(p if a else 1-p) if a==b else 0
        weight=(1-c)*independent+c*common;loss=severity*(a+b)
        atoms.append(dict(site1_event=a,site2_event=b,probability=weight,loss_units=loss,
                          pool_paid_units=min(loss,funds),unfunded_units=max(0,loss-funds)))
    mean=math.fsum(x['probability']*x['loss_units'] for x in atoms)
    var=math.fsum(x['probability']*(x['loss_units']-mean)**2 for x in atoms)
    summary=dict(correlation_mixture=c,mean_loss_units=mean,variance_loss_units2=var,
        loss_above_fund_probability=math.fsum(x['probability'] for x in atoms if x['loss_units']>funds),
        mean_pool_paid_units=math.fsum(x['probability']*x['pool_paid_units'] for x in atoms),
        mean_unfunded_units=math.fsum(x['probability']*x['unfunded_units'] for x in atoms),
        scope='Two synthetic site hazards; not a calibrated CCS frequency, severity, premium, legal cap or prediction')
    return atoms,summary


def monitoring_fund(masses_t,fee_currency_per_t,annual_monitoring_currency,years,real_return):
    """End-year deposits during injection, then end-year monitoring withdrawals.

    No damage/remediation cash flows, inflation, fees, tax, insolvency or policy
    recourse. Required charge is conditional on these analyst inputs only.
    The monitoring horizon is not a legal or physical transfer trigger.
    """
    if not masses_t or any(not math.isfinite(x) or x<0 for x in masses_t) or sum(masses_t)<=0:
        raise ValueError('Positive total finite injection mass required')
    if any(not math.isfinite(x) or x<0 for x in (fee_currency_per_t,annual_monitoring_currency,real_return)):
        raise ValueError('Finite nonnegative costs and real return required')
    if type(years) is not int or years<=0:raise ValueError('Positive integer monitoring horizon required')
    n=len(masses_t)
    weighted_t=math.fsum(m*(1+real_return)**(n-t) for t,m in enumerate(masses_t,1))
    fund=fee_currency_per_t*weighted_t
    need=math.fsum(annual_monitoring_currency/(1+real_return)**t for t in range(1,years+1))
    return dict(monitoring_years=years,real_return=real_return,total_mass_t=sum(masses_t),
        injection_end_fund_currency=fund,monitoring_PV_at_injection_end_currency=need,
        funding_gap_currency=need-fund,conditional_required_fee_currency_per_t=need/weighted_t,
        scope='Synthetic 3-year deposits; monitoring starts at closure for illustration, without native phase allocation, damages or transfer. No actual toll or service.')


def load_inputs():
    d=json.loads((ROOT/'evidence/comprehensive_review_inputs/B3-02.json').read_text())
    if hashlib.sha256((ROOT/d['source_path']).read_bytes()).hexdigest()!=d['source_sha256']:
        raise ValueError('Stale source')
    return d


def calculate(d):
    a=d['analyst'];h=d['native_historical_numbers'];checks=[]
    def add(item,value,unit,scope):checks.append(dict(item=item,value=value,unit=unit,scope=scope))
    add('historic_initial_Superfund',h['Superfund_initial_billion_USD']*1000,'million USD','Native footnote8 historical fund, not a CCS reserve or current appropriation')
    add('historic_Superfund_arithmetic_period_average',h['Superfund_initial_billion_USD']*1000/h['Superfund_period_years'],'million USD/y','Five-year quotient only, not an observed annual spending profile')
    secondary=a['nuclear_example_contributors']*h['nuclear_secondary_per_company_million_USD']
    add('analyst100_nuclear_secondary_assessments',secondary,'million USD','100 explicitly analyst contributors, not an inferred company/reactor count or instant fund liquidity')
    add('analyst100_nuclear_primary_plus_secondary',secondary+h['nuclear_primary_insurance_million_USD'],'million USD','Historical analogy, conditional single300M primary layer plus100 contributions; not CCS compensation design')
    atoms=[];pools=[]
    for c in a['correlation_mixtures']:
        rows,s=two_site_pool(a['risk_event_probability'],a['loss_per_site_units'],a['pool_funds_units'],c)
        for row in rows:atoms.append(dict(correlation_mixture=c,**row,scope='All probabilities/severities/fund limits are analyst assumptions'))
        pools.append(s)
    funding=[monitoring_fund(a['injection_mass_t'],a['trial_fee_currency_per_t'],a['annual_postclosure_monitoring_currency'],t,r) for t,r in itertools.product(a['monitoring_years'],a['real_net_returns'])]
    return checks,atoms,pools,funding


def main():
    d=load_inputs();checks,atoms,pools,funding=calculate(d);OUT.mkdir(parents=True,exist_ok=True)
    for suffix,rows in [('checks',checks),('pool_atoms',atoms),('pool_examples',pools),('funding_examples',funding),('phases',d['phases'])]:
        with (OUT/f'B3-02_{suffix}.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    summary=dict(study_id='B3-02',source_sha256=d['source_sha256'],limited_arithmetic_checks=len(checks),synthetic_risk_atoms=len(atoms),synthetic_pool_cases=len(pools),synthetic_funding_cases=len(funding),conceptual_phases=len(d['phases']),
        native_quantitative_model_reported=False,author_legal_synthesis_and_proposal_independently_validated=False,
        original_sources_verified=0,current_legal_status_verified=False,
        limits='Historical legal synthesis and conceptual policy proposal; no native quantitative model identified. Exact source/case law and longer Emory version unverified. Analyst arithmetic/pooling/funding examples do not establish calibrated losses, current coverage, transfer conditions or actual contributions. No accepted operating/GHG input changes.')
    (OUT/'B3-02_reproduction_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
