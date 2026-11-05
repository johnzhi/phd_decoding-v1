#!/usr/bin/env python3
"""Shared-source annual MILP benchmark and detailed fixed-plan reevaluation.

The optimisation uses declared, disjoint groups of published MW-A allocations
as EXOGENOUS envelopes, not independent physical capacity curves. It does not
reproduce the original optimisation or provide a complete climate optimum.
"""
from pathlib import Path
import csv,json,math,sys,os
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from operational_model import Shuttle,parameters,read,write,service
os.environ.setdefault('MPLCONFIGDIR','/tmp/paper1-matplotlib')
POLICIES=['index','earliest_window_end','least_active_hours']
SOURCE_TPA=1_000_000 # Published B4-09 p6 Table7 nominal flow class1M; not a measured Japanese capture stream.
P=parameters();YEARS=list(range(2027,2057));RES=read('data/supplement_reservoirs.csv');RN=[x['reservoir'] for x in RES]
CAP={x['reservoir']:float(x['capacity_mt']) for x in RES};READY={x['reservoir']:int(x['estimated_start_year']) for x in RES}
ENV={(r,y):0. for r in RN for y in YEARS}
for x in read('data/supplement_annual_injection.csv'):
 if x['scenario']=='MW-A' and x['reported_value_mtpa']:
  r=x['reservoir'];y=int(x['year']);assert y>=READY[r];ENV[r,y]=float(x['reported_value_mtpa'])
IMO=json.loads((ROOT/'outputs/imo_mdo_default_inventory.json').read_text())['wtw_kgco2e_per_kg']
UTILITY=float(next(x['capture_utility_kg_per_t_captured'] for x in read('data/capture_utility_scenarios.csv') if x['utility_scenario']=='NGCC_CANSOLV_90__NO_2025_climate'))

def route_meta(distance):
 s=Shuttle([SOURCE_TPA]*len(YEARS),distance,source_tpa=SOURCE_TPA)
 return dict(distance=distance,fleet=s.N,annual_trips=s.N*s.nar,cargo_mt=s.net/1e6,trip_fuel_kg=s.cycle*s.fuel_rate)

def solve_plan(distance,partition,mode):
 groups={'short':RN[:4] if partition=='first_four_short' else RN[4:],'long':RN[4:] if partition=='first_four_short' else RN[:4]};membership={r:k for k,rs in groups.items() for r in rs};meta={'short':route_meta(1000),'long':route_meta(distance)}
 assert set(groups['short']).isdisjoint(groups['long']) and set(groups['short']+groups['long'])==set(RN)
 flows=[(r,y) for r in RN for y in YEARS];trips=[(g,y) for g in ['short','long'] for y in YEARS];fi={v:i for i,v in enumerate(flows)};ti={v:len(flows)+i for i,v in enumerate(trips)};n=len(flows)+len(trips)
 c=np.zeros(n);ub=np.zeros(n);integrality=np.zeros(n)
 for r,y in flows:
  allowed=mode=='mixed' or membership[r]==mode
  ub[fi[r,y]]=ENV[r,y] if allowed else 0.;c[fi[r,y]]=-(1-UTILITY/1000)
 for g,y in trips:
  allowed=mode=='mixed' or g==mode
  ub[ti[g,y]]=meta[g]['annual_trips'] if allowed else 0.;integrality[ti[g,y]]=1;c[ti[g,y]]=meta[g]['trip_fuel_kg']*IMO/1e9
 nrows=len(YEARS)+len(RN)+len(trips);A=lil_matrix((nrows,n));limits=[];i=0
 for y in YEARS:
  for r in RN:A[i,fi[r,y]]=1
  limits.append(SOURCE_TPA/1e6);i+=1
 for r in RN:
  for y in YEARS:A[i,fi[r,y]]=1
  limits.append(CAP[r]);i+=1
 for g,y in trips:
  for r in groups[g]:A[i,fi[r,y]]=1
  A[i,ti[g,y]]=-meta[g]['cargo_mt'];limits.append(0.);i+=1
 result=milp(c,integrality=integrality,bounds=Bounds(np.zeros(n),ub),constraints=LinearConstraint(A.tocsr(),np.full(nrows,-np.inf),np.array(limits)),options={'mip_rel_gap':0.,'time_limit':120.})
 if not result.success:raise RuntimeError(f'MILP not optimal: {result.message}')
 x=result.x;max_violation=max(0.,float(np.max(A.tocsr()@x-np.array(limits))),float(np.max(x-ub)),float(-np.min(x)))
 if max_violation>1e-7:raise ArithmeticError('MILP constraint violation')
 plan=[];schedule={g:[] for g in groups}
 for y in YEARS:
  for g in groups:
   m=sum(x[fi[r,y]] for r in groups[g])*1e6;schedule[g].append(max(0.,m))
  for r in RN:plan.append(dict(reservoir=r,year=y,route=membership[r],allocated_t=max(0.,x[fi[r,y]]*1e6),exogenous_envelope_t=ENV[r,y]*1e6,candidate_resource_t=CAP[r]*1e6,readiness=READY[r],source_schedule='MW-A allocation-output proxy; not independently calibrated physical rate.'))
 integer_trips=sum(round(x[ti[v]]) for v in trips);planned=sum(sum(a) for a in schedule.values());fuel=sum(round(x[ti[g,y]])*meta[g]['trip_fuel_kg'] for g,y in trips);score=planned-planned*UTILITY/1000-fuel*IMO/1000
 trip_plan=[dict(year=y,route=g,planned_trips=int(round(x[ti[g,y]])),assigned_fleet=meta[g]['fleet'],annual_trip_limit=meta[g]['annual_trips'],cargo_per_trip_t=meta[g]['cargo_mt']*1e6,planned_flow_t=schedule[g][YEARS.index(y)],fuel_per_trip_kg=meta[g]['trip_fuel_kg']) for g,y in trips]
 return plan,schedule,meta,dict(solver_status=result.message,mip_gap=float(result.mip_gap),max_constraint_violation_mt=max_violation,planned_injection_t=planned,planned_trip_count=integer_trips,planned_fuel_kg=fuel,planned_partial_component_score_t=score,source_potential_t=SOURCE_TPA*len(YEARS)),trip_plan

def evaluate(schedule,meta,policy,margin):
 routes={};diag={}
 for g in ['short','long']:
  rr,d=Shuttle(schedule[g],meta[g]['distance'],source_tpa=schedule[g],dispatch_policy=policy,fixed_fleet=meta[g]['fleet']+margin).run();routes[g]=rr;diag[g]=d
 annual=[]
 for j,y in enumerate(YEARS):
  a,b=routes['short'][j],routes['long'][j];planned=sum(schedule[g][j] for g in schedule);C=a['captured_t']+b['captured_t'];R=a['injected_t']+b['injected_t'];stock=a['inventory_close_t']+b['inventory_close_t'];fuel=a['fuel_kg']+b['fuel_kg'];G=fuel*IMO/1000+C*UTILITY/1000
  if planned>SOURCE_TPA+.01 or C>planned+.01 or R>planned+.01:raise ArithmeticError('Shared-source/plan envelope violation')
  annual.append(dict(year=y,source_potential_t=SOURCE_TPA,source_allocated_plan_t=planned,captured_t=C,injected_t=R,uncaptured_t=SOURCE_TPA-C,inventory_close_t=stock,fuel_kg=fuel,marine_default_wtw_tco2e=fuel*IMO/1000,capture_utility_reference_t=C*UTILITY/1000,partial_component_score_t=R-G,short_injected_t=a['injected_t'],long_injected_t=b['injected_t'],short_inventory_t=a['inventory_close_t'],long_inventory_t=b['inventory_close_t'],short_active_hours=a['active_vessel_hours'],long_active_hours=b['active_vessel_hours']))
 C=sum(x['captured_t'] for x in annual);R=sum(x['injected_t'] for x in annual);stock=annual[-1]['inventory_close_t'];residual=C-R-stock
 if abs(residual)>.002:raise ArithmeticError(f'Combined mass balance {residual}')
 return annual,dict(captured_t=C,injected_t=R,final_inventory_t=stock,source_potential_t=SOURCE_TPA*len(YEARS),uncaptured_t=SOURCE_TPA*len(YEARS)-C,fuel_kg=sum(x['fuel_kg'] for x in annual),partial_component_score_t=sum(x['partial_component_score_t'] for x in annual),mass_balance_residual_t=residual,maximum_route_mass_residual_t=max(v['max_mass_balance_residual_t'] for v in diag.values()),short_fleet=diag['short']['fleet'],long_fleet=diag['long']['fleet'],maximum_short_active_hours=max(x['max_active_hours_one_ship'] for x in routes['short']),maximum_long_active_hours=max(x['max_active_hours_one_ship'] for x in routes['long']),complete_net_avoided_ghg_t='',scope='Shared source, disjoint reservoir groups and separate route-specific tanks/loading berths. Fixed annual allocation/source-share plan reevaluated operationally; no adaptive cross-route recourse, actual regional topology, complete LCA or global detailed optimum.')

def dispatch_controls():
 design=read('outputs/operational_design_adequacy.csv');out=[]
 for x in design:
  _,_,I=service(x['storage_proxy'])
  for policy in POLICIES:
   rr,d=Shuttle(I,int(x['one_way_distance_km']),fleet_margin=int(x['extra_vessels']),dispatch_policy=policy).run();R=sum(v['injected_t'] for v in rr)
   if policy=='index' and abs(R-float(x['selected_injected_t']))>.001:raise ArithmeticError('Default-policy regression')
   out.append(dict(storage_proxy=x['storage_proxy'],distance_km=x['one_way_distance_km'],fleet=d['fleet'],dispatch_policy=policy,injected_t=R,captured_t=sum(v['captured_t'] for v in rr),ship_fuel_kg=sum(v['fuel_kg'] for v in rr),mass_residual_t=d['max_mass_balance_residual_t'],max_active_hours=max(v['max_active_hours_one_ship'] for v in rr),default_injected_t=x['selected_injected_t'],difference_from_default_t=R-float(x['selected_injected_t']),scope='Alternative feasible priority rules under identical assigned fleet/service/calendar. Algorithm robustness, not independent observation/operator validation or optimal dispatch.'))
 write('outputs/dispatch_policy_controls.csv',out);return out

def plot_reevaluation(results):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(2,2,figsize=(10,7),sharey=True)
 for i,distance in enumerate([5000,10000]):
  for j,partition in enumerate(['first_four_short','last_four_short']):
   ax=axes[i,j]
   rr=[next(x for x in results if x['higher_distance_km']==distance and x['partition']==partition and x['mode']==mode and x['dispatch_policy']=='index' and x['added_vessels_per_route']==1) for mode in ['short','long','mixed']]
   xs=np.arange(3)
   ax.bar(xs-.18,[x['planned_injection_t']/1e6 for x in rr],.36,color='#bdc7cf',label='Annual allocation plan')
   ax.bar(xs+.18,[x['injected_t']/1e6 for x in rr],.36,color='#256478',label='Operating reevaluation')
   ax.set_xticks(xs,['Short only','Long only','Mixed']);ax.set_ylim(0,32)
   group='r1–r4' if partition=='first_four_short' else 'r5–r8'
   ax.set_title(f'Long route {distance:,} km; short group {group}',fontsize=10)
   ax.axhline(30,color='#555',ls=':',lw=.9);ax.set_axisbelow(True);ax.grid(axis='y',alpha=.2)
   if j==0:ax.set_ylabel('Cumulative injection (Mt)')
 axes[0,0].legend(frameon=False,fontsize=8,loc='lower left')
 fig.suptitle('One common 30 Mt source potential; disjoint service proxies',fontsize=12)
 fig.text(.5,.015,'Index dispatch; one added vessel per assigned route; no claim of regional calibration or a detailed optimum.',ha='center',fontsize=8)
 fig.tight_layout(rect=(0,.035,1,.95))
 for ext in ['png','pdf']:fig.savefig(ROOT/f'outputs/figures/mixed_allocation_reevaluation.{ext}',dpi=220)
 plt.close(fig)

def main():
 plans=[];solver=[];results=[];annual=[];trip_plans=[]
 for distance in [5000,10000]:
  for partition in ['first_four_short','last_four_short']:
   for mode in ['short','long','mixed']:
    key=f'{distance}_{partition}_{mode}';plan,schedule,meta,sol,tt=solve_plan(distance,partition,mode)
    plans.extend(dict(case_id=key,**x) for x in plan);trip_plans.extend(dict(case_id=key,**x) for x in tt);solver.append(dict(case_id=key,higher_distance_km=distance,partition=partition,mode=mode,**sol))
    for policy in POLICIES:
     for margin in [0,1]:
      aa,summary=evaluate(schedule,meta,policy,margin);keys=dict(case_id=key,higher_distance_km=distance,partition=partition,mode=mode,dispatch_policy=policy,added_vessels_per_route=margin)
      annual.extend(dict(**keys,**a) for a in aa);results.append({**keys,**sol,**summary})
    print('Solved and reevaluated',key,flush=True)
 write('outputs/mixed_reservoir_plans.csv',plans);write('outputs/mixed_trip_plans.csv',trip_plans);write('outputs/mixed_solver_audit.csv',solver);write('outputs/mixed_operational_annual.csv',annual);write('outputs/mixed_operational_comparisons.csv',results)
 controls=dispatch_controls()
 plot_reevaluation(results)
 (ROOT/'data/mixed_model_conventions.json').write_text(json.dumps(dict(source_tpa=SOURCE_TPA,source_evidence='B4-09 physical p6 Table7:1M nominal annual transport flow class; hypothetical already-captured source, not measured facility flow.',horizon=YEARS,service_evidence='B4-06-S1 FiguresS9 MW-A allocations and TableS2 resource/readiness.',groups='r1-r4 vsr5-r8 disjoint; swapped route assignment is a structural control, not geography.',distances_km=[1000,5000,10000],distance_evidence='B4-09 published shipping distance scenarios, not measured source-sink distances.',vessel_evidence='Existing operational_parameters.csv;40,000m3 conditional Table1 design.',partial_objective='Injection minus IMO-default active-cycle WtW and uniform NETL-NGCC90/NVE2025-climate capture utility reference. Other terms are missing, not zero.',objective_utility_kg_per_t=UTILITY,optimisation='Annual MILP with integer voyages; all source and resource groups coupled. Detailed fixed-plan reevaluation is not reoptimisation.',source_topology='Common capture stream split between two dedicated route export tanks/loading berths. Separate receiving terminals. Sum scheduled capture rates never exceeds common potential; unused share is not adaptively reassigned.',dispatch_policies=POLICIES,fleet_controls='Published annual fleet reference and one added vessel per assigned route; capital/idle penalties remain missing.',blank_semantics='Blank allocation annotations mean no reported allocation; assigning no exogenous service in this proxy does not establish geological zero capacity.',regional_calibration=False,complete_lca=False),indent=2)+'\n')
 (ROOT/'outputs/mixed_validation.json').write_text(json.dumps(dict(annual_milp_cases=len(solver),optimal_solver_cases=sum(x['mip_gap']<1e-8 for x in solver),operational_reevaluations=len(results),annual_operating_rows=len(annual),dispatch_control_cases=len(controls),source_shared=True,reservoir_groups_disjoint=True,maximum_combined_mass_residual_t=max(abs(x['mass_balance_residual_t']) for x in results),complete_lca=False,independent_storage_calibration=False,global_detailed_optimum=False),indent=2)+'\n')
 print('Mixed benchmark complete',len(results),flush=True)
if __name__=='__main__':main()
