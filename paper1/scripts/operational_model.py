#!/usr/bin/env python3
"""Source-driven forward model with explicitly exogenous storage-service proxies.

This model does not solve reservoir physics or estimate complete lifecycle GHG.
It simulates closed, lossless cargo inventories and capture curtailment. Source
CO2 left in tanks/ships is not credited as injected. One berth per terminal,
constant annual proxy injection rate, greedy dispatch and deterministic windows
are declared modelling conventions, not measured geographic conditions.
"""
from pathlib import Path
from dataclasses import dataclass
import csv,json,math,os
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR','/tmp/paper1-matplotlib');os.environ.setdefault('XDG_CACHE_HOME','/tmp/paper1-cache')
TOL=1e-7

def read(name):
 with (ROOT/name).open(encoding='utf-8') as f:return list(csv.DictReader(f))
def write(name,rows):
 with (ROOT/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

def parameters():return {x['parameter_id']:float(x['value']) for x in read('data/operational_parameters.csv')}

def service(scenario,static='aggregate_mean',rounding='printed'):
 """Return nominal annual envelopes constructed from published allocation output.

 Printed allocations are NOT treated as independently calibrated physical limits.
 The rounding alternatives are conditional display-resolution stress tests.
 """
 cells=read('data/supplement_annual_injection.csv');reservoirs={x['reservoir']:x for x in read('data/supplement_reservoirs.csv')}
 selected=[x for x in cells if x['scenario']==scenario];years=sorted({int(x['year']) for x in selected});delta={'printed':0,'lower':-.05,'upper':.05}[rounding]
 by_r={r:{y:0.0 for y in years} for r in reservoirs}
 for x in selected:
  if x['reported_value_mtpa']:by_r[x['reservoir']][int(x['year'])]=max(0,float(x['reported_value_mtpa'])+delta)*1e6
 dynamic=[sum(by_r[r][y] for r in reservoirs) for y in years]
 if static=='aggregate_mean':fixed=[sum(dynamic)/len(years)]*len(years)
 elif static=='ready_mean':
  fixed=[0.0]*len(years)
  for r,data in by_r.items():
   active=[i for i,y in enumerate(years) if y>=int(reservoirs[r]['estimated_start_year'])]
   for i in active:fixed[i]+=sum(data.values())/len(active)
 else:raise ValueError(static)
 return years,fixed,dynamic

@dataclass
class Ship:
 phase:str='AVAILABLE'
 end:float=math.inf
 payload:float=0.0
 heel:float=0.0
 active_year:float=0.0
 waiting_year:float=0.0
 trips_year:int=0

class Shuttle:
 def __init__(self,annual_service,distance,size=40000,calendar='staggered',source_tpa=None,fleet_margin=0,target_injected_t=None):
  p=parameters();self.p=p;self.size=size;self.distance=distance;self.calendar=calendar;self.H=p['year_hours'];self.W=p['operating_hours'];self.Hend=len(annual_service)*self.H;self.I=list(annual_service)
  self.source=float(source_tpa) if source_tpa is not None else sum(float(x['co2_rate_mtpa']) for x in read('data/supplement_sources.csv'))*1e6
  self.q=self.source/self.H;self.rho=p['density_table1']/1000;self.net=size*self.rho*(p['outbound_fill']-p['return_heel'])/100;self.heel=size*self.rho*p['return_heel']/100
  self.leg=distance/(p['speed']*1.852);self.out=p['port_approach_departure']+self.leg;self.back=self.out;self.cycle=p['loading']+self.out+p['unloading']+self.back
  self.target=target_injected_t;self.fleet_margin=fleet_margin;self.nar=math.floor(self.W/self.cycle)
  if self.nar<1:raise ValueError('No full source-model trip within annual operating budget')
  self.N=max(1,math.ceil(self.source/(self.net*self.nar)))+fleet_margin;self.ships=[Ship() for _ in range(self.N)];self.buffer=size*self.rho*p['buffer_volume_percent']/100
  self.fuel_rate=p[f'fuel_rate_{size}']*size/1000;self.factor=p['distillate_combustion_factor'];self.now=0.;self.export=0.;self.imported=0.;self.C=0.;self.R=0.;self.fuel=0.;self.max_balance=0.;self.event_count=0
  self.annual=[];self.capture_y=0.;self.inject_y=0.;self.fuel_y=0.;self.delivered_y=0.;self.inventory_open=0.;self.origin_busy=False;self.destination_busy=False;self.max_export=0.;self.max_import=0.
 def window(self,index):
  offset=index*self.H/self.N if self.calendar=='staggered' else 0.
  local=(self.now-offset)%self.H
  if abs(local-self.H)<TOL:local=0.
  open_=local<self.W-TOL
  return open_, self.now+(self.W-local if open_ else self.H-local)
 def can_run(self,index,duration):
  opened,bound=self.window(index);return opened and self.now+duration<=bound+TOL
 def next_payload(self):
  if self.target is None:return self.net
  return max(0.,min(self.net,self.target-self.R-self.imported-sum(s.payload for s in self.ships)))
 def inventory(self):return self.export+self.imported+sum(s.payload+s.heel for s in self.ships)
 def balance(self):
  self.max_export=max(self.max_export,self.export);self.max_import=max(self.max_import,self.imported)
  residual=self.C-self.R-self.inventory();self.max_balance=max(self.max_balance,abs(residual))
  if abs(residual)>1e-3:raise ArithmeticError(f'Mass imbalance {residual}')
  if min(self.export,self.imported)<-1e-5 or max(self.export,self.imported)>self.buffer+1e-4:raise ArithmeticError('Buffer constraint violation')
 def complete_events(self):
  for s in self.ships:
   if s.end>self.now+TOL:continue
   old=s.phase;s.end=math.inf
   if old=='LOADING':self.origin_busy=False;s.phase='READY_OUTBOUND'
   elif old=='OUTBOUND':s.phase='WAIT_DESTINATION'
   elif old=='UNLOADING':
    self.destination_busy=False;self.imported+=s.payload;self.delivered_y+=s.payload;s.payload=0.;s.phase='READY_RETURN'
   elif old=='INBOUND':s.phase='AVAILABLE'
   else:raise RuntimeError(old)
 def dispatch(self):
  changed=True
  while changed:
   changed=False
   for i,s in enumerate(self.ships):
    if s.phase=='AVAILABLE' and not self.origin_busy and self.can_run(i,self.cycle):
     heel_add=self.heel if s.heel==0 else 0.;payload=self.next_payload();need=payload+heel_add
     if payload<=TOL:continue
     if self.export+TOL>=need:
      self.export-=need;s.heel+=heel_add;s.payload=payload;s.phase='LOADING';s.end=self.now+self.p['loading'];s.trips_year+=1;self.origin_busy=True;changed=True
    elif s.phase=='READY_OUTBOUND' and self.can_run(i,self.out):s.phase='OUTBOUND';s.end=self.now+self.out;changed=True
    elif s.phase=='WAIT_DESTINATION' and not self.destination_busy and self.can_run(i,self.p['unloading']):
     if self.imported+s.payload<=self.buffer+TOL:s.phase='UNLOADING';s.end=self.now+self.p['unloading'];self.destination_busy=True;changed=True
    elif s.phase=='READY_RETURN' and self.can_run(i,self.back):s.phase='INBOUND';s.end=self.now+self.back;changed=True
 def run(self):
  active={'LOADING','OUTBOUND','UNLOADING','INBOUND'}
  while self.now<self.Hend-TOL:
   self.event_count+=1
   if self.event_count>300000:raise RuntimeError('Event loop did not converge')
   y=min(int((self.now+TOL)/self.H),len(self.I)-1);inj=self.I[y]/self.H
   self.complete_events();self.dispatch();self.balance()
   q_capture=self.q if self.next_payload()>TOL else 0.
   year_end=min((y+1)*self.H,self.Hend);candidates=[year_end]
   for i,s in enumerate(self.ships):
    if s.end>self.now+TOL:candidates.append(s.end)
    opened,bound=self.window(i)
    if bound>self.now+TOL:candidates.append(bound)
    if s.phase=='AVAILABLE' and not self.origin_busy and self.can_run(i,self.cycle):
     need=self.next_payload()+(self.heel if s.heel==0 else 0.)
     if q_capture>0 and self.export<need-TOL:candidates.append(self.now+(need-self.export)/q_capture)
    if s.phase=='WAIT_DESTINATION' and not self.destination_busy and self.can_run(i,self.p['unloading']) and inj>0:
     excess=self.imported+s.payload-self.buffer
     if excess>TOL:candidates.append(self.now+excess/inj)
   if self.target is not None and inj>0 and self.R<self.target-TOL:candidates.append(self.now+(self.target-self.R)/inj)
   nxt=min(t for t in candidates if t>self.now+TOL);dt=nxt-self.now
   captured=min(q_capture*dt,max(0.,self.buffer-self.export));injected=min(inj*dt,self.imported,max(0.,self.target-self.R) if self.target is not None else math.inf)
   self.export+=captured;self.imported-=injected;self.C+=captured;self.R+=injected;self.capture_y+=captured;self.inject_y+=injected
   active_count=0
   for s in self.ships:
    if s.phase in active:s.active_year+=dt;active_count+=1
    else:s.waiting_year+=dt
   fuel=active_count*self.fuel_rate*dt;self.fuel+=fuel;self.fuel_y+=fuel
   self.now=nxt;self.max_export=max(self.max_export,self.export);self.max_import=max(self.max_import,self.imported);self.balance()
   if abs(self.now-year_end)<1e-5:
    self.complete_events();self.balance();stock=self.inventory();max_hours=max(s.active_year for s in self.ships)
    if max_hours>self.W+1e-4:raise ArithmeticError(f'Annual active-hour bound exceeded: {max_hours}')
    self.annual.append(dict(year=2027+y,captured_t=self.capture_y,injected_t=self.inject_y,uncaptured_t=self.source-self.capture_y,inventory_open_t=self.inventory_open,inventory_close_t=stock,export_close_t=self.export,import_close_t=self.imported,marine_close_t=sum(s.payload+s.heel for s in self.ships),cargo_delivered_t=self.delivered_y,fuel_kg=self.fuel_y,combustion_co2_t=self.fuel_y/1000*self.factor,modelled_balance_t=self.inject_y-self.fuel_y/1000*self.factor,started_trips=sum(s.trips_year for s in self.ships),active_vessel_hours=sum(s.active_year for s in self.ships),max_active_hours_one_ship=max_hours,active_utilisation=sum(s.active_year for s in self.ships)/(self.N*self.W),waiting_or_unavailable_vessel_hours=sum(s.waiting_year for s in self.ships)))
    self.inventory_open=stock;self.capture_y=self.inject_y=self.fuel_y=self.delivered_y=0.
    for s in self.ships:s.active_year=s.waiting_year=0.;s.trips_year=0
  self.balance()
  return self.annual,dict(fleet=self.N,fleet_margin=self.fleet_margin,target_injected_t=self.target,cargo_per_delivery_t=self.net,roundtrip_hours=self.cycle,source_model_roundtrips_per_ship=self.nar,max_mass_balance_residual_t=self.max_balance,final_inventory_t=self.inventory(),final_heel_t=sum(s.heel for s in self.ships),max_export_inventory_t=self.max_export,max_import_inventory_t=self.max_import,buffer_capacity_t=self.buffer,event_count=self.event_count)

def continuous(annual_service,distance,size=40000,source_tpa=None):
 p=parameters();Q=source_tpa if source_tpa is not None else sum(float(x['co2_rate_mtpa']) for x in read('data/supplement_sources.csv'))*1e6
 cargo=size*p['density_table1']/1000*(p['outbound_fill']-p['return_heel'])/100;cycle=2*distance/(p['speed']*1.852)+p['loading']+p['unloading']+2*p['port_approach_departure'];fuel_rate=p[f'fuel_rate_{size}']*size/1000
 # Full-flow reference includes an integer last voyage; no source/ship startup inventory in this simplified variant.
 fixed_fuel_per_t=math.ceil(Q/cargo)*cycle*fuel_rate/Q if Q else None
 rows=[]
 for i,I in enumerate(annual_service):
  m=min(Q,I);fuel=m*fixed_fuel_per_t if Q else 0.;ghg=fuel/1000*p['distillate_combustion_factor']
  rows.append(dict(year=2027+i,captured_t=m,injected_t=m,uncaptured_t=Q-m,inventory_open_t=0.,inventory_close_t=0.,export_close_t=0.,import_close_t=0.,marine_close_t=0.,cargo_delivered_t=m,fuel_kg=fuel,combustion_co2_t=ghg,modelled_balance_t=m-ghg,started_trips='',active_vessel_hours='',max_active_hours_one_ship='',active_utilisation='',waiting_or_unavailable_vessel_hours=''))
 return rows,dict(fixed_fuel_kg_per_t=fixed_fuel_per_t,reference_source_tpa=Q)

def validate_fleet():
 p=parameters();out=[]
 for x in read('data/analysis_inputs.csv'):
  if x['group']!='fleet':continue
  _,size,Q,d=x['value_id'].split('_');size=int(size);Q=int(Q)*1e6;d=int(d)
  cargo=size*p['density_table1']/1000*(p['outbound_fill']-p['return_heel'])/100;cycle=2*d/(p['speed']*1.852)+p['loading']+p['unloading']+2*p['port_approach_departure'];count=math.ceil(Q/(cargo*math.floor(p['operating_hours']/cycle)))
  out.append(dict(source_value_id=x['value_id'],reported_ships=int(x['value']),reconstructed_ships=count,match=count==int(x['value']),density_basis='Explicit Table1 1154 kg/m3; conflicting prose not repaired.'))
 if not all(x['match'] for x in out):raise ArithmeticError('Published fleet validation mismatch')
 return out

def run_grid():
 cache={};annual=[];results=[];diagnostics=[]
 cases=[(size,d,static,'staggered','printed','primary') for size in [40000,80000,120000] for d in [1000,5000,10000,15000,20000] for static in ['aggregate_mean','ready_mean']]
 cases +=[(40000,d,'aggregate_mean',cal,rnd,'structural_sensitivity') for d in [5000,10000] for cal,rnd in [('synchronised','printed'),('staggered','lower'),('staggered','upper')]]
 for size,d,static,calendar,rounding,group in cases:
  for variant in ['B0','B1','B2','B3']:
   path_results={}
   for path,scenario,dist in [('lower_service','SW-A',1000),('higher_service','MW-A',d)]:
    _,fixed,dynamic=service(scenario,static,rounding);I=dynamic if variant in ['B1','B3'] else fixed;ops=variant in ['B2','B3']
    key=(scenario,dist,size,static if not(variant in ['B1','B3']) else 'dynamic',calendar if ops else 'fixed',rounding)
    if key not in cache:
     rr,meta=Shuttle(I,dist,size,calendar).run() if ops else continuous(I,dist,size)
     cache[key]=(rr,meta);diagnostics.append(dict(case_key='|'.join(map(str,key)),**meta))
    rr,meta=cache[key];C=sum(x['captured_t'] for x in rr);R=sum(x['injected_t'] for x in rr);G=sum(x['combustion_co2_t'] for x in rr);path_results[path]=(C,R,G)
    for x in rr:annual.append(dict(group=group,size_m3=size,higher_distance_km=d,static_policy=static,availability_calendar=calendar,rounding_case=rounding,variant=variant,path=path,**x))
   Cd,Rd,Gd=path_results['lower_service'];Cf,Rf,Gf=path_results['higher_service'];deltaR=Rf-Rd;deltaG=Gf-Gd;headroom=deltaR-deltaG
   results.append(dict(group=group,size_m3=size,higher_distance_km=d,lower_distance_km=1000,static_policy=static,availability_calendar=calendar,rounding_case=rounding,variant=variant,lower_captured_t=Cd,higher_captured_t=Cf,lower_injected_t=Rd,higher_injected_t=Rf,lower_ship_combustion_co2_t=Gd,higher_ship_combustion_co2_t=Gf,additional_injected_t=deltaR,additional_ship_combustion_co2_t=deltaG,differential_uninventoried_burden_allowance_tco2e=headroom,allowance_kgco2e_per_extra_injected_t=headroom/deltaR*1000 if deltaR>0 else '',net_avoided_ghg_t='',interpretation='Conditional injected-mass minus inventoried ship-combustion balance. Full lifecycle GHG, leakage and end-stock permanence are not established.'))
 # Distinguish the full representation contrast from the two-factor interaction.
 contrasts=[]
 grouped={}
 for x in results:
  k=tuple(x[a] for a in ['group','size_m3','higher_distance_km','static_policy','availability_calendar','rounding_case']);grouped.setdefault(k,{})[x['variant']]=x
 for k,xx in grouped.items():
  v=[xx[f'B{i}']['differential_uninventoried_burden_allowance_tco2e'] for i in range(4)]
  contrasts.append(dict(zip(['group','size_m3','higher_distance_km','static_policy','availability_calendar','rounding_case'],k),full_B3_minus_B0_t=v[3]-v[0],deliverability_B1_minus_B0_t=v[1]-v[0],operations_B2_minus_B0_t=v[2]-v[0],two_factor_interaction_t=v[3]-v[2]-v[1]+v[0]))
 write('outputs/operational_annual.csv',annual);write('outputs/operational_comparisons.csv',results);write('outputs/operational_contrasts.csv',contrasts)
 (ROOT/'outputs/operational_diagnostics.json').write_text(json.dumps(diagnostics,indent=2));return results,contrasts,diagnostics

def figures(results):
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'font.size':10,'figure.dpi':160,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
 fig,ax=plt.subplots(figsize=(7.5,4.2))
 for variant in ['B0','B1','B2','B3']:
  data=[x for x in results if x['size_m3']==40000 and x['static_policy']=='aggregate_mean' and x['group']=='primary' and x['variant']==variant]
  ax.plot([x['higher_distance_km'] for x in data],[x['differential_uninventoried_burden_allowance_tco2e']/1e6 for x in data],'o-',label=variant)
 ax.axhline(0,color='grey',lw=1);ax.set_xlabel('Higher-service route scenario (km, one way)');ax.set_ylabel('Uninventoried differential burden allowance\n(Mt CO₂e; conditional, not net mitigation)');ax.legend(frameon=False,ncol=4);fig.tight_layout()
 for ext in ['png','pdf']:fig.savefig(ROOT/f'outputs/figures/operational_allowance.{ext}',bbox_inches='tight')
 plt.close(fig)
def control_cases():
 records=[];cache={}
 for distance in [5000,10000]:
  base={}
  for path,scenario,dist in [('lower_service','SW-A',1000),('higher_service','MW-A',distance)]:
   _,_,I=service(scenario)
   for margin in [0,1]:
    rr,meta=Shuttle(I,dist,fleet_margin=margin).run();key=(path,margin);cache[(distance,path,margin)]=(rr,meta)
    base[key]=dict(injected_t=sum(x['injected_t'] for x in rr),combustion_t=sum(x['combustion_co2_t'] for x in rr),captured_t=sum(x['captured_t'] for x in rr),fleet=meta['fleet'])
  for margin in [0,1]:
   a,b=base[('lower_service',margin)],base[('higher_service',margin)]
   records.append(dict(control='B3 one-vessel structural control',higher_distance_km=distance,fleet_margin_each_route=margin,lower_fleet=a['fleet'],higher_fleet=b['fleet'],lower_injected_t=a['injected_t'],higher_injected_t=b['injected_t'],additional_injected_t=b['injected_t']-a['injected_t'],additional_ship_co2_t=b['combustion_t']-a['combustion_t'],uninventoried_allowance_t=b['injected_t']-a['injected_t']-b['combustion_t']+a['combustion_t'],target_reached='',interpretation='One extra vessel is a controlled design perturbation, not an empirical parameter. Capital/idle effects remain missing; no optimum is claimed.'))
  target=min(base[('lower_service',0)]['injected_t'],base[('higher_service',0)]['injected_t']);equal={}
  for path,scenario,dist in [('lower_service','SW-A',1000),('higher_service','MW-A',distance)]:
   _,_,I=service(scenario);rr,meta=Shuttle(I,dist,target_injected_t=target).run();equal[path]=(sum(x['injected_t'] for x in rr),sum(x['combustion_co2_t'] for x in rr),meta)
  a,b=equal['lower_service'],equal['higher_service'];ok=abs(a[0]-target)<.001 and abs(b[0]-target)<.001
  records.append(dict(control='B3 equal-injection control',higher_distance_km=distance,fleet_margin_each_route=0,lower_fleet=a[2]['fleet'],higher_fleet=b[2]['fleet'],lower_injected_t=a[0],higher_injected_t=b[0],additional_injected_t=b[0]-a[0],additional_ship_co2_t=b[1]-a[1],uninventoried_allowance_t=b[0]-a[0]-b[1]+a[1],target_reached=ok,interpretation='Both simulations stop additional dispatch/capture when the common injected target is supplied. The target is the smaller primary B3 injected output. Remaining inventory is uncredited; no whole-chain mitigation or optimal shutdown is inferred.'))
 write('outputs/operational_controls.csv',records);return records

def design_adequacy_control():
 p=parameters();fraction=p['completion_design_percent']/100;records=[]
 for scenario,d in [('SW-A',1000)]+[('MW-A',v) for v in [1000,5000,10000,15000,20000]]:
  _,_,I=service(scenario);ideal,_=continuous(I,d);ceiling=sum(x['injected_t'] for x in ideal);target=fraction*ceiling
  initial=Shuttle(I,d);N0=initial.N;maximum_fleet=math.ceil(initial.source/initial.net);chosen=None;history=[]
  for margin in range(maximum_fleet-N0+1):
   sim=initial if margin==0 else Shuttle(I,d,fleet_margin=margin);rr,meta=sim.run();R=sum(x['injected_t'] for x in rr);G=sum(x['combustion_co2_t'] for x in rr);history.append(dict(fleet=meta['fleet'],injected_t=R,completion_of_continuous_envelope=R/ceiling))
   if R>=target-TOL:chosen=(R,G,meta);break
  R,G,meta=chosen if chosen else (R,G,meta)
  records.append(dict(storage_proxy=scenario,one_way_distance_km=d,source_reference_fleet=N0,selected_fleet=meta['fleet'],extra_vessels=meta['fleet']-N0,completion_design_fraction=fraction,continuous_envelope_t=ceiling,required_injected_t=target,selected_injected_t=R,selected_combustion_co2_t=G,design_target_met=bool(chosen),initial_injected_t=history[0]['injected_t'],initial_completion_fraction=history[0]['completion_of_continuous_envelope'],candidate_history=json.dumps(history),interpretation='Minimum added fleet beyond the source-model reference meeting a transferred99%-of-continuous-envelope design criterion under staggered windows. No cost/capital optimum or physical storage calibration is claimed.'))
 write('outputs/operational_design_adequacy.csv',records)
 low=records[0];comparisons=[]
 for high in records[1:]:
  comparisons.append(dict(higher_distance_km=high['one_way_distance_km'],lower_selected_fleet=low['selected_fleet'],higher_selected_fleet=high['selected_fleet'],additional_injected_t=high['selected_injected_t']-low['selected_injected_t'],additional_ship_co2_t=high['selected_combustion_co2_t']-low['selected_combustion_co2_t'],uninventoried_allowance_t=high['selected_injected_t']-low['selected_injected_t']-high['selected_combustion_co2_t']+low['selected_combustion_co2_t'],both_design_targets_met=low['design_target_met'] and high['design_target_met']))
 write('outputs/operational_design_comparisons.csv',comparisons);return records

def reliquefaction_envelope(results):
 p=parameters();Q=sum(float(x['co2_rate_mtpa']) for x in read('data/supplement_sources.csv'))*1e6;out=[]
 for x in results:
  size=x['size_m3'];power=p[f'reliq_compressor_{size}_1']+p[f'reliq_compressor_{size}_2'];kgph=power*p['generator_sfoc']/1000
  years=len(service('SW-A')[0]);charges=[]
  for path,dist,key in [('lower_service',1000,'lower_injected_t'),('higher_service',x['higher_distance_km'],'higher_injected_t')]:
   cycle=2*dist/(p['speed']*1.852)+p['loading']+p['unloading']+2*p['port_approach_departure'];cargo=size*p['density_table1']/1000*(p['outbound_fill']-p['return_heel'])/100;N=math.ceil(Q/(cargo*math.floor(p['operating_hours']/cycle)))
   full=N*p['operating_hours']*years*kgph/1000*p['distillate_combustion_factor']
   # Compare fixed throughput coefficient versus fixed assigned-fleet costing-duty treatment, explicitly as an envelope.
   charge=full*x[key]/(Q*years) if x['variant'] in ['B0','B1'] else full;charges.append(charge)
  extra=charges[1]-charges[0]
  out.append(dict(size_m3=size,higher_distance_km=x['higher_distance_km'],static_policy=x['static_policy'],availability_calendar=x['availability_calendar'],rounding_case=x['rounding_case'],variant=x['variant'],additional_generator_co2_full_load_scenario_t=extra,allowance_after_full_load_generator_scenario_t=x['differential_uninventoried_burden_allowance_tco2e']-extra,whole_chain_ghg_t='',interpretation='Optional nameplate compressor ×8000h/year × published MGO SFOC scenario; not a measured BOG duty. Source0.084kg/kWh LHV-labelled value is not used. Other components remain missing.'))
 write('outputs/operational_reliquefaction_envelope.csv',out);return out

def control_figure():
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 raw=read('outputs/operational_controls.csv');cal=read('outputs/operational_comparisons.csv');fig,axs=plt.subplots(1,2,figsize=(10,3.8),sharey=True)
 for j,margin in enumerate(['0','1']):
  data=[x for x in raw if x['control']=='B3 one-vessel structural control' and x['fleet_margin_each_route']==margin]
  axs[0].bar([i+(j-.5)*.34 for i in range(2)],[float(x['uninventoried_allowance_t'])/1e6 for x in data],.34,label='Reference fleet' if margin=='0' else 'One added vessel per route')
 for j,calendar in enumerate(['staggered','synchronised']):
  data=[x for x in cal if x['size_m3']=='40000' and x['static_policy']=='aggregate_mean' and x['variant']=='B3' and x['rounding_case']=='printed' and x['availability_calendar']==calendar and x['higher_distance_km'] in ['5000','10000']]
  axs[1].bar([i+(j-.5)*.34 for i in range(2)],[float(x['differential_uninventoried_burden_allowance_tco2e'])/1e6 for x in data],.34,label=calendar.capitalize())
 for ax in axs:ax.axhline(0,color='grey',lw=1);ax.set_xticks([0,1],['5000 km','10000 km']);ax.legend(frameon=False,fontsize=8);ax.set_xlabel('Higher-service route scenario')
 axs[0].set_ylabel('Conditional uninventoried allowance (Mt CO₂e)');axs[0].set_title('Added-vessel control');axs[1].set_title('Availability-calendar sensitivity');fig.tight_layout()
 for ext in ['png','pdf']:fig.savefig(ROOT/f'outputs/figures/operational_controls.{ext}',bbox_inches='tight')
 plt.close(fig)

if __name__=='__main__':
 fleet=validate_fleet();write('outputs/operational_fleet_validation.csv',fleet);rr,cc,diag=run_grid();figures(rr);controls=control_cases();envelope=reliquefaction_envelope(rr);design=design_adequacy_control();control_figure()
 report=dict(published_fleet_cases=len(fleet),published_fleet_matches=sum(x['match'] for x in fleet),comparison_rows=len(rr),contrast_rows=len(cc),unique_model_runs=len(diag),control_cases=len(controls),design_adequacy_cases=len(design),optional_generator_scenarios=len(envelope),full_lifecycle_results_generated=False,storage_physics_calibrated=False,climate_metric='Uninventoried differential burden allowance; conditional fossil-source one-for-one and injected-as-retained interpretation only. Missing lifecycle/leakage terms are not assigned zero.')
 (ROOT/'outputs/operational_validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
