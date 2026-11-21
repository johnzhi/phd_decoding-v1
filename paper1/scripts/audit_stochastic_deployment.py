#!/usr/bin/env python3
"""B2-03 arithmetic, literal bookkeeping and mathematical counterexamples.

No native Illinois/Gurobi/SAA/CDF model or geological service is reproduced.
Synthetic examples are separately disclosed and never become operating inputs.
"""
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_inputs():
    data = json.loads((ROOT/'evidence/comprehensive_review_inputs/B2-03.json').read_text())
    edges = json.loads((ROOT/'evidence/comprehensive_review_inputs/B2-03_citation_checks.json').read_text())
    if hashlib.sha256((ROOT/data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale deployment source')
    for edge in edges:
        for path, sha in [('citing_path','citing_sha256'),('cited_path','cited_sha256')]:
            if hashlib.sha256((ROOT/edge[path]).read_bytes()).hexdigest() != edge[sha]:
                raise ValueError('Stale scoped citation original')
    return data, edges


def objective_component(case, literal_stochastic_sign=False):
    if not all(math.isfinite(v) and v >= 0 for k,v in case.items() if k != 'scope'):
        raise ValueError('Nonnegative finite monetary terms required')
    operating_sign = -1 if literal_stochastic_sign else 1
    return (case['benefit'] - case['investment'] - operating_sign*case['operating']
            - case['pipeline'] - case['storage'] + case['revenue'])


def stock_trace(case, remove_before_sum):
    stock, life, flows = (case[k] for k in ('initial_stock','lifetime','annual_flows'))
    if not all(math.isfinite(x) for x in [stock,life,*flows]) or stock < 0 or life <= 0 or any(f<0 for f in flows):
        raise ValueError('Finite nonnegative stock/flows and positive lifetime required')
    available = set(range(len(flows))); remaining = stock; committed = 0; rows = []
    for i, flow in enumerate(flows):
        build = life*flow <= remaining
        current_flows = {j: flow if j == i and build else 0 for j in available}
        if build:
            available.remove(i)
            committed += life*flow
        # Published Algorithms1/2 sum the already-updated I_A, omitting the new source.
        deduction = life*sum(current_flows[j] for j in (available if remove_before_sum else current_flows))
        remaining -= deduction
        rows.append(dict(period=i+1,proposed_annual_flow=flow,built=int(build),available_after_update=remaining,
                         lifetime_commitment_total=committed,commitment_minus_original_stock=committed-stock,
                         scope='synthetic_literal_set_update' if remove_before_sum else 'synthetic_reservation_comparison'))
    return rows


def horizon_solutions(case):
    capacity = case['capacity']; q = case['commitments']; values = case['rewards']
    if not len(q) == len(values) or not q or capacity < 0 or any(x < 0 for x in q):
        raise ValueError('Compatible nonnegative capacity/commitments required')
    feasible = [(sum(v*x for v,x in zip(values,bits,strict=True)),bits)
                for bits in itertools.product((0,1),repeat=len(q))
                if sum(c*x for c,x in zip(q,bits,strict=True)) <= capacity]
    full = max(feasible)
    remaining = capacity; chosen = []; reward = 0
    for consumption,value in zip(q,values,strict=True):
        take = int(value > 0 and consumption <= remaining)
        chosen.append(take); remaining -= take*consumption; reward += take*value
    return dict(full_objective=full[0],full_decisions=list(full[1]),rolling_objective=reward,
                rolling_decisions=chosen,scope=case['scope'])


def calculate(data):
    rows=[]
    def add(item,value,unit,source,status,scope):
        rows.append(dict(item=item,value=value,unit=unit,source=source,status=status,scope=scope))
    c=data['case'];years=c['planning_years'][1]-c['planning_years'][0]+1
    for name,value,unit in [
        ('inclusive_planning_periods',years,'years'),
        ('sink_count',c['sequestration_sites']+c['utilization_sites'],'sites'),
        ('construction_scenario_draws',c['batches']*c['scenarios_per_batch'],'scenario realizations'),
        ('rolling_candidate_solves_if_every_batch_runs_all_periods',c['batches']*years,'MILP calls'),
        ('reported_annual_emissions_difference',c['source_emissions_ktpa']-c['reported_final_emissions_ktpa'],'kt/year'),
        ('reported_new_capacity_endpoint_difference',c['first_new_capture_ktpa']-c['last_new_capture_ktpa'],'kt/year')]:
        add(name,value,unit,'Results p7','reported_case_arithmetic','Not native deployment, sampling, performance or physical-service reproduction.')
    reduction=100*(c['source_emissions_ktpa']-c['reported_final_emissions_ktpa'])/c['source_emissions_ktpa']
    add('reduction_from_reported_endpoints',reduction,'percent','Results p7 / Figures6,8','HOLD_REDUCTION_ROUNDING',
        '55.36624% rounds to55.4 at one decimal; source55.3 may use truncation/different underlying values. Preserve both, no repaired native output.')
    add('endpoint_reduction_minus_reported',reduction-c['reported_base_reduction_percent'],'percentage points','Results p7','HOLD_REDUCTION_ROUNDING','No full GHG boundary or true model output inferred.')
    deviation=100*(c['deterministic_lifetime_deviation_kt']-c['stochastic_lifetime_deviation_kt'])/c['deterministic_lifetime_deviation_kt']
    add('reported_deviation_reduction_recomputed',deviation,'percent','Results p7','reported_output_arithmetic',
        'Agrees with96.97% rounding; lifetime scenario-mean deviation is not a probability, annual outage or leakage fraction.')
    for b in data['budget_cases']:
        add(f'budget_fraction_{b["fraction"]:g}',c['annual_base_budget_billion_dollars']*b['fraction'],'billion dollars per allocation period','Results p7 / Figure8','reported_budget_arithmetic',
            'Allocation funds lifetime NPV commitments at commissioning, not an independently reconstructed annual cash ledger.')
    add('analyst_one_kt_one_year_SCC',1000*c['social_cost_dollars_per_t'],'dollars','Results p7 / symbols p10','analyst_unit_example',
        'One hypothetical1kt emission at42 dollars/t; not source lifetime/discount coefficient or a full project benefit.')
    for literal in (False,True):
        value=objective_component(data['analyst_cost_case'],literal)
        label='literal_Eq7_13' if literal else 'Eq1_19_25_plus_cost'
        add('analyst_objective_'+label,value,'arbitrary monetary units','Eqs1,7,13,19,25 pp3–6','HOLD_OPERATING_COST_SIGN','Synthetic component only; no native implementation defect inferred.')
        add('analyst_optional_build_'+label,int(value>0),'binary decision','Eqs1,7,13,19,25','analyst_objective_counterexample','No-build has objective0; all hypothetical project costs fit budget100.')
    for literal in (False,True):
        trace=stock_trace(data['analyst_stock_case'],literal);tail=trace[-1]
        label='literal_after_removal' if literal else 'reservation_comparison'
        for key in ('available_after_update','lifetime_commitment_total','commitment_minus_original_stock'):
            add('analyst_'+label+'_'+key,tail[key],'arbitrary stock units','Algorithm1 line12 / Algorithm2 line13 pp5–6','HOLD_SET_UPDATE_ORDER',
                'Synthetic bookkeeping; conventional nonnegative flow. Not Illinois source/sink geometry, actual author code or calibrated injectivity.')
    horizon=horizon_solutions(data['analyst_horizon_case'])
    for key in ('full_objective','rolling_objective'):
        add('analyst_'+key,horizon[key],'arbitrary objective units','Rolling scope p5 / Eq31 p6','analyst_bound_counterexample',horizon['scope'])
    add('analyst_Eq31_heuristic_minus_global',horizon['rolling_objective']-horizon['full_objective'],'arbitrary objective units','Eq31–33 p6','HOLD_HEURISTIC_UPPER_BOUND',
        'Deterministic distribution is a special stochastic case. A feasible rolling reward5 is below optimum10; feasibility alone cannot establish the asserted>= inequality.')
    for name,value in [('true_expected_single_policy',1),('one_sample_low',0),('one_sample_high',2)]:
        add('analyst_finite_sample_'+name,value,'arbitrary objective units','Eq33/35 p6','analyst_statistical_counterexample',
            'Only policy has equiprobable reward0/2. Finite sample means can fall either side of true optimum1; no confidence guarantee without statistical treatment.')
    return rows


def write_csv(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
    data,edges=load_inputs();rows=calculate(data);out=ROOT/'outputs/comprehensive_review'
    write_csv(out/'B2-03_checks.csv',rows)
    traces=stock_trace(data['analyst_stock_case'],False)+stock_trace(data['analyst_stock_case'],True)
    write_csv(out/'B2-03_stock_counterexample.csv',traces)
    result=dict(study_id='B2-03',source_sha256=data['source_sha256'],checks=len(rows),horizon_counterexample=horizon_solutions(data['analyst_horizon_case']),
                scoped_citation_checks=len(edges),native_Illinois_Gurobi_SAA_CDF_model_reproduced=False,
                statistical_bound_or_physical_service_validated=False,accepted_inputs_changed=False,missing=data['missing'])
    (out/'B2-03_reconciliation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
