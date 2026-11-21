#!/usr/bin/env python3
"""B2-04 reduced-equation components and disclosed mathematical/unit examples.

Synthetic matrices are not MRST training data. No native reservoir, validation,
AdOpT-NET0 optimization, pump fit or physical safety/retention model reproduced.
"""
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
import numpy as np
from scipy.linalg import block_diag
from scipy.optimize import Bounds, LinearConstraint, milp

ROOT=Path(__file__).resolve().parents[1]


def load_inputs():
    data=json.loads((ROOT/'evidence/comprehensive_review_inputs/B2-04.json').read_text())
    edges=json.loads((ROOT/'evidence/comprehensive_review_inputs/B2-04_citation_checks.json').read_text())
    if hashlib.sha256((ROOT/data['source_path']).read_bytes()).hexdigest()!=data['source_sha256']:
        raise ValueError('Stale reservoir-ROM source')
    for e in edges:
        for path,sha in [('citing_path','citing_sha256'),('cited_path','cited_sha256')]:
            if hashlib.sha256((ROOT/e[path]).read_bytes()).hexdigest()!=e[sha]:
                raise ValueError('Stale ROM scoped citation original')
    return data,edges


def pod_basis(case):
    p=np.asarray(case['pressure_snapshots'],float);s=np.asarray(case['saturation_snapshots'],float)
    up=np.linalg.svd(p,full_matrices=False)[0][:,:1]
    us=np.linalg.svd(s,full_matrices=False)[0][:,:1]
    return block_diag(up,us)


def projected_step(case,phi=None):
    phi=pod_basis(case) if phi is None else np.asarray(phi,float)
    J,A,B=(np.asarray(case[k],float) for k in ('J','A','B'))
    previous,next_training,current=(np.asarray(case[k],float) for k in ('xi_previous','xi_next','xi_current'))
    du=np.asarray(case['u_current'])-np.asarray(case['u_training'])
    psi=J@phi;Jr=psi.T@J@phi;Ar=psi.T@A@phi;Br=psi.T@B
    if np.linalg.matrix_rank(Jr)<Jr.shape[0]:raise ValueError('Projected operator is rank deficient')
    delta=-np.linalg.solve(Jr,Ar@(current-previous)+Br@du)
    result=next_training+delta
    residual=J@phi@delta+A@phi@(current-previous)+B@du
    return dict(phi=phi,psi=psi,Jr=Jr,Ar=Ar,Br=Br,delta=delta,xi_next=result,
                reconstructed=phi@result,residual=residual,projected_residual=psi.T@residual)


def distances(current,training,epsilon,training_normalization=True):
    training=np.asarray(training,float)
    if not math.isfinite(current) or current<0 or not math.isfinite(epsilon) or epsilon<=0 or np.any(~np.isfinite(training)) or np.any(training<0):
        raise ValueError('Finite nonnegative volumes and positive epsilon required')
    denominator=training+epsilon if training_normalization else current+epsilon
    return np.abs(current-training)/denominator


def selector_milp(case,epsilon):
    """Bounded synthetic one-hot minimum plus indicator affine-map component.

    State/control are fixed in this isolated diagnostic. The valid big-M values
    follow from explicit output bounds; no native Bertoni bounds are assumed.
    """
    d=distances(case['current_cumulative_volume'],case['training_cumulative_volumes'],epsilon)
    values=(np.array(case['selector_affine_a'])*case['selector_state']
            +np.array(case['selector_affine_b'])*case['selector_control']+np.array(case['selector_affine_c']))
    n=len(d);lower_y,upper_y=-100.,100.
    rows=[];lo=[];hi=[]
    def add(row,lower,upper):rows.append(row);lo.append(lower);hi.append(upper)
    add([1.]*n+[0,0],1,1)
    for value in d:add([0.]*n+[1,0],-np.inf,float(value))
    add(list(-d)+[1,0],0,np.inf)
    for j,value in enumerate(values):
        M=max(abs(lower_y-value),abs(upper_y-value))
        row=np.zeros(n+2);row[j]=M;row[-1]=1;add(row,-np.inf,value+M)
        row=np.zeros(n+2);row[j]=-M;row[-1]=1;add(row,value-M,np.inf)
    objective=np.zeros(n+2);objective[-1]=-1 # Reward cannot override nearest-distance rule.
    solved=milp(c=objective,integrality=[1]*n+[0,0],
                bounds=Bounds([0]*n+[0,lower_y],[1]*n+[max(d),upper_y]),
                constraints=LinearConstraint(np.array(rows),np.array(lo),np.array(hi)))
    if not solved.success:raise RuntimeError(solved.message)
    return dict(selected=int(np.argmax(solved.x[:n])),q=solved.x[:n].tolist(),minimum=solved.x[-2],
                output=solved.x[-1],candidate_outputs=values.tolist(),distances=d.tolist(),
                scope='synthetic_bounded_selector_and_affine_map_not_native_ROM_MILP')


def pump_power(mass_rate,delta_p,rho,efficiency):
    if not all(math.isfinite(v) for v in (mass_rate,delta_p,rho,efficiency)) or mass_rate<0 or delta_p<0 or rho<=0 or not 0<efficiency<=1:
        raise ValueError('Nonnegative rate/head,positive density and0<efficiency<=1 required')
    return mass_rate*delta_p/(rho*efficiency)


def pump_corners(case):
    m0=case['reference_mass_rate_kgps'];p0=case['reference_delta_p_Pa'];rho=case['rho_kgpm3'];eta=case['efficiency']
    rows=[]
    for m,p in itertools.product(case['mass_rate_bounds'],case['delta_p_bounds_Pa']):
        full=pump_power(m,p,rho,eta)
        plane=pump_power(m0,p0,rho,eta)+(m-m0)*p0/(rho*eta)+(p-p0)*m0/(rho*eta)
        rows.append(dict(mass_rate_kgps=m,delta_p_Pa=p,full_W=full,analyst_tangent_plane_W=plane,
                         full_minus_plane_W=full-plane,scope='synthetic_plane_not_author_SI_fit'))
    return rows


def calculate(data):
    rows=[]
    def add(item,value,unit,source,status,scope):
        rows.append(dict(item=item,value=float(value),unit=unit,source=source,status=status,scope=scope))
    pub=data['published'];toy=data['toy'];full=pub['full_state_dimension'];reduced=pub['pressure_modes']+pub['saturation_modes']
    for name,value,unit in [('inferred_cells',full/2,'cells'),('reduced_states',reduced,'states'),
                            ('dimension_reduction_percent',100*(1-reduced/full),'percent'),
                            ('nominal_five_year_halfyear_intervals',pub['validation_years']*12/pub['reservoir_step_months'],'intervals'),
                            ('interior_search_candidates',2*pub['search_s']+1,'candidates')]:
        add(name,value,unit,'Methods/Results pp5–9','reported_dimension_arithmetic','Initial/final indexing,calendar and native grid not independently reconstructed.')
    for row in data['table2']:
        ratio=row['full_seconds']/row['linear_seconds']
        add(row['scenario']+'_reported_timing_ratio',ratio,'ratio','Table2 p9','reported_output_arithmetic',
            'Standalone selection/Eq14/reconstruction timing,not a native MILP or fresh hardware benchmark. Full-chain integration is reported to add order100x solve cost.')
    projected=projected_step(toy)
    for key in ('residual','projected_residual'):
        add('analyst_'+key+'_norm',np.linalg.norm(projected[key]),'dimensionless residual norm','Eq13–14 pp5–6','synthetic_projected_component',
            'Least-squares projection can have nonzero full residual; this is not a measured carbon mass loss or native ROM validation.')
    add('analyst_basis_orthogonality_error',np.linalg.norm(projected['phi'].T@projected['phi']-np.eye(2)),
        'dimensionless','Eq11–14 p5','synthetic_POD_component',toy['scope'])
    for norm in (False,True):
        d=distances(toy['current_cumulative_volume'],toy['training_cumulative_volumes'],pub['epsilon'],norm)
        add('analyst_selected_candidate_'+('training_normalized' if norm else 'current_normalized'),np.argmin(d),'zero-based index','Eq10/Section2.3 pp5–6',
            'analyst_metric_comparison','Denominator change deliberately changes metric; example current18,training10/30/50. Not native candidate/accuracy data.')
    selector=selector_milp(toy,pub['epsilon'])
    add('analyst_MILP_selected_candidate',selector['selected'],'zero-based index','Eq20–25 p6','synthetic_selector_component',selector['scope'])
    add('analyst_MILP_selected_output',selector['output'],'dimensionless state','Eq14 and one-hot selection','synthetic_selector_component',selector['scope'])
    weights=np.asarray(selector['q']);operators=np.array([1,4,9])
    add('analyst_fixed_i_operator_sum',sum(operators[0]*weights),'arbitrary coefficient','Eq26–28 p6','HOLD_SELECTION_INDEX',
        'Printed RHS retains i inside a sum over j;with one-hot sum1 a fixed-i coefficient is unchanged. No author code defect or silent correction inferred.')
    add('analyst_j_weighted_operator_comparison',operators@weights,'arbitrary coefficient','Eq26–28 p6','analyst_index_comparison','A separately disclosed j-dependent comparison;not a repaired native formulation.')
    average=toy['average_case'];mean_rate=np.mean(average['mass_rates_kgps']);rho=average['rho_kgpm3'];dt=average['step_seconds']
    for name,value,unit in [('rate_mean_volume',mean_rate/rho,'m3/s'),('literal_Eq29_if_inputs_are_rates',mean_rate/rho/dt,'m3/s2'),
                            ('Eq29_if_inputs_are_interval_masses',np.mean(np.array(average['mass_rates_kgps'])*dt)/rho/dt,'m3/s')]:
        add('analyst_'+name,value,unit,'Eq29 p7','HOLD_FLOW_AMOUNT_TIME_BASIS','Native variable/time units unknown; both interpretations retained. No source correction or rate input adopted.')
    p=toy['pressure_case'];mean_bhp=p['well_pressure']+np.mean(p['daily_rates'])/p['conductance'];peak=p['well_pressure']+max(p['daily_rates'])/p['conductance'];limit=pub['pressure_limit_factor']*p['fracture_pressure']
    for name,value in [('coarse_BHP',mean_bhp),('peak_BHP',peak),('model_safety_limit',limit)]:
        add('analyst_'+name,value,'arbitrary pressure unit','Eq30–31 p7','analyst_temporal_counterexample',p['scope'])
    density=toy['density_case'];b=density['reservoir_kgpm3']/density['surface_kgpm3']
    for name,value,unit in [('b_from_rho_relation',b,'dimensionless'),('inverse_b_prose',1/b,'dimensionless'),
                            ('BHP_increment_rho_relation',density['surface_rate_m3ps']/(density['mobility_WI_m3ps_per_Pa']*b),'Pa'),
                            ('BHP_increment_inverse_b',density['surface_rate_m3ps']/(density['mobility_WI_m3ps_per_Pa']/b),'Pa'),
                            ('surface_density_hydrostatic_drop',density['surface_kgpm3']*density['g_mps2']*density['depth_m']/1e5,'bar'),
                            ('column_density_hydrostatic_comparison',density['reservoir_kgpm3']*density['g_mps2']*density['depth_m']/1e5,'bar')]:
        add('analyst_'+name,value,unit,'rho=b*rho_surface p3;Eq30–32 p7','HOLD_DENSITY_REFERENCE',
            'Chosen densities2/800kg/m3 and depth1500m are hypothetical,not native reservoir or surface conditions. Actual datum/column/EOS remain open.')
    for i,row in enumerate(pump_corners(toy['pump_case']),1):
        add(f'analyst_pump_plane_corner{i}_full_minus_plane',row['full_minus_plane_W'],'W','Eq34 p7','analyst_plane_approximation',
            'Reference tangent plane chosen for synthetic data. Native fitting coefficients/domain/error absent;not author pump-case reproduction.')
    add('analyst_conditional_true_pressure_at_5percent_underprediction',.9/.95,'fraction of fracture-pressure reference','Accuracy/constraint pp7–11','analyst_error_margin_example',
        'Conditional true=(predicted/.95) with predicted=.9pmax. Test-case well-cell error is not a proven BHP bound; no robust margin adopted.')
    return rows


def write_csv(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
    data,edges=load_inputs();rows=calculate(data);out=ROOT/'outputs/comprehensive_review'
    write_csv(out/'B2-04_checks.csv',rows);write_csv(out/'B2-04_pump_plane_example.csv',pump_corners(data['toy']['pump_case']))
    projected={k:v.tolist() for k,v in projected_step(data['toy']).items()}
    result=dict(study_id='B2-04',source_sha256=data['source_sha256'],checks=len(rows),synthetic_projected_component=projected,
                synthetic_selector=selector_milp(data['toy'],data['published']['epsilon']),scoped_citation_checks=len(edges),
                native_MRST_training_validation_AdOpT_or_pump_fit_reproduced=False,physical_safety_or_retention_validated=False,
                accepted_inputs_changed=False,missing=data['missing'])
    (out/'B2-04_reconciliation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('synthetic_projected_component','synthetic_selector')},indent=2))


if __name__=='__main__':main()
