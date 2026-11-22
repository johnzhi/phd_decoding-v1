#!/usr/bin/env python3
"""Limited B2-06 checks: printed components and disclosed analyst examples.

No Canadian GAMS/CPLEX scenario, native warm-start procedure, reservoir,
process utility inventory or detailed operating schedule is reproduced.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/comprehensive_review'


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B2-06.json').read_text())
    for source in [data['source'], *data['cited_sources']]:
        if hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest() != source['sha256']:
            raise ValueError(f"Source changed: {source['path']}")
    return data


def annual_targets(maximum, years, periods):
    if years < 1 or periods < 1 or years % periods:
        raise ValueError('This reconstruction requires equal integer-year periods')
    duration = years // periods
    return [maximum * (year // duration + 1) / periods for year in range(years)]


def inventory(initial, net_annual_flows, period_years, literal=False):
    """Literal Eq8/22 versus a separately labeled physical time integral."""
    if len(net_annual_flows) != len(period_years) or min(period_years) <= 0:
        raise ValueError('Compatible positive period durations required')
    return initial + math.fsum(flow * (1 if literal else years)
                               for flow, years in zip(net_annual_flows, period_years))


def product_range(flow, mode, upper):
    """Independent LP min/max under printed Eq34–36 and z>=0."""
    if mode not in (0, 1) or not 0 <= flow <= upper:
        raise ValueError('Binary mode and valid finite flow bound required')
    # z<=M*y, z<=x, z>=x-M*(1-y)
    rhs = [upper*mode, flow, upper*(1-mode)-flow]
    values=[]
    for sign in (1, -1):
        result=linprog([sign],A_ub=[[1],[1],[-1]],b_ub=rhs,bounds=[(0,None)],method='highs')
        if not result.success:raise RuntimeError(result.message)
        values.append(float(result.x[0]))
    return values


def round_trip_milp(mass, cargo):
    """Eq52–54 on the printed two-node Figure3 example only."""
    if mass < 0 or cargo <= 0:raise ValueError('Invalid mass/cargo')
    result=milp(np.ones(2),integrality=np.ones(2),
                bounds=Bounds([mass/cargo,0],[np.inf,np.inf]),
                constraints=LinearConstraint([[1,-1]],[0],[0]))
    if not result.success:raise RuntimeError(result.message)
    return result.x


def capacity_index_example(process_specific=False):
    """A fixed analyst case: q1=1,q2=0,x2>=.5. No native code claim."""
    bound = 0 if process_specific else 1
    result=linprog([1],A_ub=[[1],[-1]],b_ub=[bound,-.5],bounds=[(0,None)],method='highs')
    return bool(result.success)


def buffer_rule(flow_Mtpy, days=2, margin=1.2):
    return flow_Mtpy*days/365*margin


def peak_after_delivery(cargo_Mt, delivery_hours, constant_outflow_Mtpy):
    """Analyst initially empty tank; uniform delivery and outflow during it."""
    if min(cargo_Mt,delivery_hours,constant_outflow_Mtpy)<0:raise ValueError('Nonnegative inputs required')
    return max(0,cargo_Mt-constant_outflow_Mtpy*delivery_hours/8760)


def calculate(data):
    rows=[];annual=[]
    def add(item,value,unit,basis,locator,meaning):
        rows.append(dict(item=item,value=value,unit=unit,basis=basis,source_locator=locator,interpretation=meaning))
    a=data['case']['emissions_Mtpy'];years=data['case']['years']
    baseline=math.fsum(annual_targets(a,years,20))
    for n in data['case']['partitions']:
        targets=annual_targets(a,years,n);total=math.fsum(targets)
        annual += [dict(partitions=n,year_index=k+1,calendar_year=2025+k,
                        period_index=k//(years//n)+1,target_Mtpy=v,
                        scope='reconstructed stipulated ramp, not optimized achieved injection') for k,v in enumerate(targets)]
        add(f'target_mass_N{n}',total,'MtCO2','printed ramp reconstruction','p15 Figure6; p16','Authors explicitly acknowledge that cumulative service changes with partition')
        add(f'target_mass_ratio_N{n}',total/baseline,'ratio','printed ramp reconstruction','p16 Section6.2.2','Not a controlled comparison with identical service')
        if n!=20:
            raw=data['cost_differences'][str(n)]['total_percent'];per=data['cost_differences'][str(n)]['per_tonne_percent']
            implied=100*((1+raw/100)/(total/baseline)-1)
            lo=100*((1+(raw-.5)/100)/(total/baseline)-1)
            hi=100*((1+(raw+.5)/100)/(total/baseline)-1)
            per_half=.05 if n==10 else .5
            add(f'per_tonne_from_rounded_total_N{n}',implied,'percent','reported rounded arithmetic','p16','Point values need not reproduce independently rounded percentages')
            add(f'rounding_overlap_N{n}',int(max(lo,per-per_half)<=min(hi,per+per_half)),'boolean','conditional displayed-precision check','p16','Nearest displayed-unit intervals only; not measured uncertainty or a corrected result')
    add('figure3_loads',.059/.01,'loads/year','printed component','pp10–11 Figure3/Eq52','5.9 cargo loads is not5.9 integer trips or six vehicles')
    trips=round_trip_milp(.059,.01)
    add('figure3_outbound_trips',float(trips[0]),'trips/year','independent two-arc MILP','pp10–11 Eq52–54','Six outbound trips')
    add('figure3_empty_return_trips',float(trips[1]),'trips/year','independent two-arc MILP','pp10–11 Eq52–54','Six return trips despite zero return cargo; source does model these trips')
    add('train_single_capacity',100*80/1e6,'MtCO2/train','printed arithmetic','p14 Section6.1','100railcars of80tonnes; no train utilization/calendar inferred')
    add('transload_full_train_equivalents',5/.008,'full train loads/year','conditional printed arithmetic','p19','5Mt/year per direction; partial loads can require more actual trips')
    add('transload_calendar_daily_average',5/.008/365,'full train loads/day','conditional calendar example','p19','1.71average under365days, not a strict daily maximum; source four/day needs its handling/calendar convention')
    add('transload_both_directions_average',10/.008/365,'full train handlings/day','conditional combined-direction example','p19','3.42if5Mtloading and5Mtunloading; not proof of the published interpretation')
    add('injection_ship_loads',.457/.01,'loads/year','printed arithmetic','p19','Conditional46loaded trips; native sailing/unloading schedule not available')
    add('injection_ship_integer_loaded_trips',math.ceil(.457/.01),'trips/year','printed arithmetic','p19','Matches reported46 under10ktcapacity')
    add('transport_ship_loads',.779/.04,'loads/year','printed arithmetic','p19','19.475; at least20loaded trips if one cargo capacity applies')
    add('transport_ship_integer_loaded_trips',math.ceil(.779/.04),'trips/year','conditional printed arithmetic','p19','No native trips inferred beyond this conditional lower bound')
    add('end_year_storage_sum',49.4+8.2,'MtCO2/year','printed arithmetic','p18','Equals57.6; this is achieved model flow, not maximum physical service')
    add('parallel_offshore_capacity',29.3+20.2,'MtCO2/year rated','printed arithmetic','p19','49.5rated can exceed49.4flow; no contradiction')
    add('approximate_pipeline_lengths_sum',400+130+446+2*140,'km','rounded source arithmetic','p19','1256from explicitly approximate components versus1253reported total; not a proven inconsistency')
    add('average_train_additions',126/20,'trains/year','printed arithmetic','p19','6.3arithmetic, not independent confirmation of2.4standard deviation')
    add('pie_display_sum',sum(data['pie_percent'].values()),'percent','printed graphic arithmetic','p20 Figure13','100.1is compatible with component display rounding; no forced normalization')
    add('pipeline_pie_minus_body',data['pie_percent']['pipelines']-19.1,'percentage points','printed graphic/text comparison','p19 versus p20','19.2graphic versus19.1body remains a minor presentation discrepancy')
    add('offshore_share_of_total_if_body',.85*.191*100,'percent','conditional source arithmetic','p19','85%ofpipelinecost is not85%ofwhole-chaincost')
    add('heuristic_612s_vs_2days',100*612/(2*86400),'percent','reported timing arithmetic','pp20,25–26','About.354%versus statedabout.4%; not an independent runtime benchmark')
    add('five_period_10min_time_saving',100*(1-349/600),'percent','reported timing arithmetic','p25 TableD.1','41.83%at reportedcommon.8%gap')
    add('five_period_1h_time_saving',100*(1-1620/3600),'percent','reported timing arithmetic','p25 TableD.1','55%at reportedcommon.5%gap')
    add('twenty_period_cost_advantage_10min_vs_2days',100*(1-1.05/1.151),'percent','conditional common-positive-LB comparison','pp25–26','8.78%usingrounded5/15.1gaps; not10%improvement over a proved optimum')
    add('twenty_period_cost_advantage_64min_vs_2days',100*(1-1.0351/1.151),'percent','conditional common-positive-LB comparison','p26','About10.07%usingdifferent runtime comparison; exact native logs unavailable')
    add('gap_after_point06percent_cost_reduction',100*(1.0199*(1-.0006)-1),'percent gap','conditional common-positive-LB example','p26','Cost reduction.06%is not automatically.06percentage-point gap reduction')
    for row in data['performance_table']:
        add(f"normalized_objective_N{row['periods']}_{row['method']}",1+row['gap_to_bkb_percent']/100,
            'objective/common positive LB','printed table normalization','p25 TableD.1','Not an observed absolutecost or native optimizer reproduction')
    for k,mode in enumerate([0,1]):
        for flow in [0,.2,.7,1]:
            bounds=product_range(flow,mode,1)
            add(f'product_width_y{mode}_x{flow}',bounds[1]-bounds[0],'flow units','analyst independent LP','p9 Eq34–36','Exact binary product when0<=x<=M and all required domains/links hold')
    add('literal_two_year_inventory',inventory(.1,[.2,.2],[2,2],True),'MtCO2','analyst literal Eq8/22 example','pp7–8','NoOhfactor as printed; not native source inventory')
    add('integrated_two_year_inventory',inventory(.1,[.2,.2],[2,2]),'MtCO2','analyst time integral','pp7–8; p24 AppA','Separate conditional stock-flow comparison; do not silently repair native code')
    add('literal_q1_index_toy_feasible',int(capacity_index_example(False)),'boolean','analyst LP','p7 Eq10','q1=1,q2=0,x2>=.5 allowed by printedq1bound')
    add('process_specific_q2_toy_feasible',int(capacity_index_example(True)),'boolean','analyst alternative LP','p7 Eq10; p24 AppA','Same toy not feasible under separately labeledq2bound; native implementation unknown')
    reserve=buffer_rule(1)
    add('two_day_rule_buffer',reserve*1000,'ktCO2','analyst1Mt/year example','p10 Eq43–46; p23 beta','6.575kt; not native case size')
    add('one_day_40kt_delivery_peak',peak_after_delivery(.04,24,1)*1000,'ktCO2','analyst dynamic balance','p10 strategic scope','About37.26ktpeak withinitialemptytank; not a native failed schedule')
    add('annual_activity_count_for_overlapping_jobs',math.ceil(6/(8760*.8)),'vehicles','analyst aggregation example','p11 Eq57','Two3hjobs both required in same3hwindow need2vehicles despite annual aggregate1')
    add('overlapping_window_required_vehicles',2,'vehicles','analyst concurrent-window example','p11 strategic scope','An explicit missing scheduling restriction, not a claimed native failure')
    add('loaded_leg_fuel_proxy',100/2,'litres','analyst full outbound/empty return','p12 Eq69','100kmperleg,2km/L,loaded-mass coefficientcountsonelegonly')
    add('trip_based_roundtrip_fuel',2*100/2,'litres','analyst per-trip accounting','p12 FCtrip alternative','Source allowsper-tripfuelcost thatcountsbothemptyandloadedlegs')
    add('positive_used_fleet_cost_argmin',min(range(1,4),key=lambda n:n),'vehicles','analyst signed-cost domain','p12 Eq68','Minimumceil fleet1ifpositivecoefficient')
    add('negative_used_fleet_cost_argmin',min(range(1,4),key=lambda n:-n),'vehicles','analyst signed-cost domain','p12 Eq68','Nonzeroaloneis insufficient;this is not an asserted native negativecost')
    add('minimum_buffer_additions_after_three_open_periods',3*.1,'MtCO2','analyst positive-minimum rule','p10 Eq41/42','Ifminimumaddition.1,eachopenperiodforces.1;notjustone-timebuild')
    add('late_child_per_period_implication',int(all(c<=h for c,h in zip([0,1],[1,0]))),'boolean','analyst opening-event example','p13 Eq76; pp24–25 AppendixB','Hubopensfirst,childsecond; per-periodopeningimplicationrejectsthis')
    add('late_child_cumulative_availability',int(all(sum([0,1][:k+1])<=sum([1,0][:k+1]) for k in range(2))),'boolean','analyst separate availability comparison','p13 Eq76; pp24–25 AppendixB','Cumulativeavailabilitywouldpermitit; not a proposed silent replacement')
    return rows,annual


def main():
    data=load_inputs();checks,annual=calculate(data);OUT.mkdir(parents=True,exist_ok=True)
    for name,rows in [('B2-06_checks.csv',checks),('B2-06_ramp.csv',annual),('B2-06_performance.csv',data['performance_table'])]:
        with (OUT/name).open('w',newline='',encoding='utf-8') as stream:
            w=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    result=dict(study_id='B2-06',source_sha256=data['source']['sha256'],checks=len(checks),stipulated_ramp_rows=len(annual),reported_performance_rows=len(data['performance_table']),
                native_Canadian_GAMS_CPLEX_model_reproduced=False,native_heuristic_or_six_benchmarks_reproduced=False,
                pressure_constrained_reservoir_or_complete_utility_inventory=False,accepted_operating_GHG_inputs_changed=False,
                scope='Reported arithmetic and disclosed analyst component/counterexample checks only; unresolved printed notation is not proof of a native code defect')
    (OUT/'B2-06_reconciliation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
