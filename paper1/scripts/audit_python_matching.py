#!/usr/bin/env python3
"""B3-05 printed arithmetic and disclosed algorithm/unit diagnostics.

No native CCS-NetOptmizer, Kazakhstan MILP, routing, SI or Monte Carlo replay.
Synthetic geometries and process inputs remain outside accepted Paper1 data.
"""
from __future__ import annotations
import csv
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs/comprehensive_review'


def energy_emissions(power_MW,hours_y,kg_per_kWh):
    if any(not math.isfinite(x) or x<0 for x in (power_MW,hours_y,kg_per_kWh)):
        raise ValueError('Finite nonnegative power,hours and intensity required')
    energy=power_MW*1000*hours_y
    return energy,energy*kg_per_kWh/1000


def dbscan_min2(points,eps):
    """Synthetic Euclidean min_samples=2, counting each point itself.

    Non-singleton connected components of the epsilon-neighbor graph are clusters.
    This is not an implementation/metric verification of the author repository.
    """
    p=np.asarray(points,dtype=float)
    if p.ndim!=2 or not len(p) or not np.isfinite(p).all() or not math.isfinite(eps) or eps<=0:
        raise ValueError('Finite coordinates and positive epsilon required')
    dist=np.linalg.norm(p[:,None,:]-p[None,:,:],axis=2);labels=np.full(len(p),-1,dtype=int);visited=set();label=0
    for start in range(len(p)):
        if start in visited:continue
        group=[];todo=[start];visited.add(start)
        while todo:
            v=todo.pop();group.append(v)
            for neighbor in np.flatnonzero(dist[v]<=eps):
                if int(neighbor) not in visited:visited.add(int(neighbor));todo.append(int(neighbor))
        if len(group)>1:
            labels[group]=label;label+=1
    return labels,dist


def tree_metrics(points,edges,flows):
    """Root0 tree distance and linear flow-distance proxy, not pipeline USD."""
    p=np.asarray(points,dtype=float);n=len(p)
    if len(edges)!=n-1 or len(flows)!=n or any(x<0 for x in flows):raise ValueError('Nonnegative flows and tree edges required')
    graph=[[] for _ in range(n)];length=0
    for a,b in edges:
        d=float(np.linalg.norm(p[a]-p[b]));length+=d;graph[a].append((b,d));graph[b].append((a,d))
    rootdistance={0:0.};todo=[0]
    while todo:
        a=todo.pop()
        for b,d in graph[a]:
            if b not in rootdistance:rootdistance[b]=rootdistance[a]+d;todo.append(b)
    if len(rootdistance)!=n:raise ValueError('Connected tree required')
    return length,math.fsum(flows[j]*rootdistance[j] for j in range(n))


def pipeline_literal(L,d):
    return math.fsum([1294*L**.90*d**1.59,30690*L**.82*d**.94,8913*L**1.05*d**.40,24547*L**.78*d**.79])


def load_inputs():
    d=json.loads((ROOT/'evidence/comprehensive_review_inputs/B3-05.json').read_text())
    if hashlib.sha256((ROOT/d['source_path']).read_bytes()).hexdigest()!=d['source_sha256']:
        raise ValueError('Stale source')
    return d


def calculate(d):
    checks=[];a=d['analyst'];f=d['native_factors'];cost=d['native_costs']
    def add(item,value,unit,scope):checks.append(dict(item=item,value=value,unit=unit,scope=scope))
    add('sector_source_count',sum(x['sources'] for x in d['native_sectors']),'count','Six sector counts total88; included source IDs per radius remain unknown')
    add('sector_emission_total',math.fsum(x['emissions_Mt_y'] for x in d['native_sectors']),'Mt/y','Native selected inventory148.53,not necessarily every plotted scenario baseline')
    add('selected_inventory_power_share',100*math.fsum(x['emissions_Mt_y'] for x in d['native_sectors'][:2])/148.53,'percent','Selected-source denominator differs from national80% statement')
    add('selected_sites_capacity_Gt',f['storage_capacity_Mt']/1000,'Gt','Static5784Mt selected sites,not annual injection service')
    add('selected_over_national_resource_percent',100*f['storage_capacity_Mt']/1000/f['national_storage_Gt'],'percent','Different resource levels; not an availability probability')
    for strategy in ['full','partial']:
        total=cost[f'100{strategy}_total_billion_USD'];unit=cost[f'100{strategy}_unit_USD_t']
        add('100_'+strategy+'_implied_cost_denominator',total*1000/unit,'Mt','Conditional BUSD/USD-per-t quotient; stored versus abated and annual/lifetime basis unresolved')
        add('100_'+strategy+'_transport_cost_share',100*cost[f'100{strategy}_transport_USD_t']/unit,'percent','Common cost denominator assumed; no native optimizer replay')
    add('100_partial_total_premium',100*(cost['100partial_total_billion_USD']/cost['100full_total_billion_USD']-1),'percent','Reported deterministic totals,not MC ranking probability')
    add('100_partial_unit_premium',100*(cost['100partial_unit_USD_t']/cost['100full_unit_USD_t']-1),'percent','Reported unit-cost arithmetic only')
    add('100_partial_transport_premium',100*(cost['100partial_transport_USD_t']/cost['100full_transport_USD_t']-1),'percent','Not evidence of stochastic equivalence')
    for radius in [100,180]:add(str(radius)+'_unassigned_cost_share',100-cost[f'{radius}capture_percent']-cost[f'{radius}transport_percent'],'percent','Residual percentage only,not a verified storage-cost decomposition')
    for radius in [100,400]:
        before,after=cost[f'{radius}existing_compare_amounts']
        add(str(radius)+'_reported_reuse_saving',100*(before-after)/before,'percent','Scale-free arithmetic; MUSD prose versus BUSD axis remains unresolved')
    add('100_prose_MC_relative_halfwidth',100*(13-9)/2/11,'percent','About18.18% from illustrative9–13around11; not confidence in a population median')
    leak=f['fugitive_t_per_km_y']*a['leak_length_km']
    add('length_consistent_fugitive_example',leak,'t/y','100km analyst length with quoted1.4t/km/y; no actual leak calibration verified')
    add('unconverted_m_length_numeric_example',f['fugitive_t_per_km_y']*a['leak_length_km']*1000,'inconsistent raw product','Deliberately mismatched m and per-km inputs,not a valid emission estimate or demonstrated code behavior')
    add('m_km_numeric_ratio',1000,'ratio','Unit conflict magnitude only; no guessed repair of author implementation')
    energy,emission=energy_emissions(a['power_MW'],a['hours_y'],f['grid_kgCO2e_per_kWh'])
    add('analyst_MW_to_annual_energy',energy,'kWh/y','1MW and8760h are analyst assumptions,not native station load or operating schedule')
    add('analyst_energy_to_tonnes',emission,'tCO2e/y','Quoted grid intensity; includes explicit kg-to-t conversion,not native grid verification')
    source=a['capture_example_source_t_y'];fraction=a['capture_fraction']
    add('analyst_capture_Eq2',fraction*a['unit_capture_USD_t']*source,'USD/y','Dimensionally annual cost,not USD stock; all example source/rate/unit cost analyst choices')
    add('analyst_capture_Eq11_residual',(1-fraction)*source,'t/y','Uncaptured fraction; no heat,electricity,upstream or utility suppliers represented')
    comp=a['compression_example'];raw=comp['k']/(comp['k']-1)*comp['R_J_mol_K']*comp['T_K']/comp['efficiency']*((comp['Pout_Pa']/comp['Pin_Pa'])**((comp['k']-1)/comp['k'])-1)*comp['mass_kg_s']
    add('analyst_Eq5_universalR_raw_product',raw,'unresolved mol/kg basis','Literal numeric product with analyst inputs; cannot interpret directly as native MW')
    add('analyst_dimensioned_ideal_gas_compression',raw/comp['molar_mass_kg_mol']/1e6,'MW','Analyst R/M and W/MW conversion,not a correction/reproduction of native code or validated dense-CO2 compression')
    v=a['volume_example'];mass=v['E']*v['A_m2']*v['h_m']*v['phi']*v['rho_kg_m3']
    add('analyst_Eq16_volume_component',mass/1e9,'Mt','All geometry/properties/efficiency analyst choices; static mass only,no annual pressure limit')
    for row in a['pipeline_examples']:
        add('analyst_Eq3_L'+str(row['length_km']),pipeline_literal(row['length_km'],row['diameter_m']),'source coefficient numeric output','Literal units km/m assumed; coefficient currency/vintage/original scale unverified,not accepted pipeline cost')
    graph,dist=dbscan_min2(a['graph_coordinates_km'],a['graph_eps_km']);cluster=np.flatnonzero(graph==0);coords=np.asarray(a['graph_coordinates_km'])
    add('synthetic_DBSCAN_cluster_size',len(cluster),'count','Four chain points neighbor-connected at eps100,min_samples2; isolated fifth is noise')
    add('synthetic_DBSCAN_cluster_diameter',float(dist[np.ix_(cluster,cluster)].max()),'km','270km diameter does not violate100km neighbor epsilon')
    add('synthetic_DBSCAN_max_centroid_distance',float(np.linalg.norm(coords[cluster]-coords[cluster].mean(axis=0),axis=1).max()),'km','135km from centroid; epsilon is not guaranteed hub-distance bound')
    add('synthetic_DBSCAN_MST_length',float(minimum_spanning_tree(dist[np.ix_(cluster,cluster)]).sum()),'km','Synthetic Euclidean component,not native Kazakhstan GIS/routing')
    graphrows=[dict(point=j,x_km=x[0],y_km=x[1],cluster=int(graph[j]),scope='Analyst Euclidean min_samples2 example,not the authors geodetic metric or native source data') for j,x in enumerate(a['graph_coordinates_km'])]
    trees=[]
    for name,edges in [('distance_MST',[(0,1),(1,2)]),('direct_star',[(0,1),(0,2)]),('other_tree',[(0,2),(1,2)])]:
        length,proxy=tree_metrics(a['MST_counterexample_coordinates_km'],edges,a['MST_counterexample_source_flows'])
        trees.append(dict(tree=name,total_length_km=length,flow_distance_proxy=proxy,scope='Analyst root0 andflows0/1/100; linear flow-distance proxy,not actual pipeline USD or proof of native suboptimality'))
    weights=[]
    for unit,scale in [('USD',1),('BUSD',1e-9)]:
        for name,residual,c in [('zero_residual',0,1e9),('one_residual',1,0)]:weights.append(dict(cost_unit=unit,design=name,residual=residual,cost=c*scale,EI_weight=100,weighted_numeric_score=100*residual+c*scale,scope='Explicit analyst finite weight/scaling counterexample; no native weights or preference inferred'))
    horizon=[dict(annual_Mt_y=1,capacity_Mt=10,horizon_y=h,raw_rate_number_le_capacity_number=True,required_mass_Mt=h,within_stock=h<=10,scope='Analyst rate1,stock10 andhorizon1/30; no claim about native implementation horizon') for h in [1,30]]
    return checks,graphrows,trees,weights,horizon


def main():
    d=load_inputs();checks,graph,trees,weights,horizon=calculate(d);OUT.mkdir(parents=True,exist_ok=True)
    for suffix,rows in [('checks',checks),('DBSCAN_example',graph),('MST_examples',trees),('weight_examples',weights),('horizon_examples',horizon),('reported_cost_labels',d['native_figure4_total_labels'])]:
        with (OUT/f'B3-05_{suffix}.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    summary=dict(study_id='B3-05',source_sha256=d['source_sha256'],limited_checks=len(checks),synthetic_graph_points=len(graph),synthetic_tree_cases=len(trees),synthetic_weight_cases=len(weights),synthetic_horizon_cases=len(horizon),reported_cost_labels=14,native_code_MILP_MC_or_Kazakhstan_case_reproduced=False,SI_inspected=False,scoped_citation_edges=2,
        limits='Unit/arithmetic/synthetic component checks only. Essential SI and native code/version/data unverified. No correction of printed indices,coefficient scale,money horizon,kg/t,m/km,power/energy or residual/abatement naming silently applied. No accepted operating/GHG inputs changed.')
    (OUT/'B3-05_reproduction_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
