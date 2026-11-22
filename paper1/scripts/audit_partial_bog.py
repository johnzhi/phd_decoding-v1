#!/usr/bin/env python3
"""B3-08 unit/accounting, rounded cash-flow and synthetic scalar diagnostics.

No native HYSYS/mixture-solid model, work curve, thermal voyage, economic optimum
or complete capture/EOR/storage lifecycle model is independently reproduced.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import CoolProp
import CoolProp.CoolProp as CO2_PROPS
import numpy as np
from scipy.optimize import linprog, minimize_scalar

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/comprehensive_review'


def power_from_specific(w_kJ_kg, mass_kg_h):
    if min(w_kJ_kg, mass_kg_h) < 0 or not all(math.isfinite(x) for x in [w_kJ_kg,mass_kg_h]):
        raise ValueError('Finite nonnegative work and mass flow required')
    return w_kJ_kg * mass_kg_h / 3600


def treatment_terms(x, w_kJ_kg, CL_USD_kJ, gamma_kgCO2_kWh, CP_USD_t, CS_USD_t):
    """Explicit consistent diagnostic basis: CO2 component, kJ/kg and USD/t."""
    if not 0 <= x <= 1 or min(w_kJ_kg,CL_USD_kJ,gamma_kgCO2_kWh,CP_USD_t) < 0:
        raise ValueError('Valid fraction and nonnegative energy/cost/emission inputs required')
    if not all(math.isfinite(v) for v in [x,w_kJ_kg,CL_USD_kJ,gamma_kgCO2_kWh,CP_USD_t,CS_USD_t]):
        raise ValueError('Finite scalar inputs required')
    fuel = 1000 * w_kJ_kg * CL_USD_kJ
    emitted = (1 - x) + gamma_kgCO2_kWh * w_kJ_kg / 3600
    penalty = emitted * CP_USD_t
    sale = x * CS_USD_t
    return dict(fuel_USD_t=fuel,emission_tCO2_tBOG=emitted,penalty_USD_t=penalty,sale_USD_t=sale,total_USD_t=fuel + penalty - sale)


def synthetic_quadratic_optimum(a, CL, gamma, CP, CS):
    """Invented w=a*x², not a fit to the authors' Figure6/native work curve."""
    A = 1000 * CL + gamma * CP / 3600
    if a <= 0 or A <= 0:
        raise ValueError('Positive quadratic work and marginal cost required')
    candidate = min(1.,max(0.,(CP + CS) / (2 * a * A)))
    def objective(x):return treatment_terms(x,a*x*x,CL,gamma,CP,CS)['total_USD_t']
    endpoints = [(objective(x),x) for x in [0.,candidate,1.]]
    return min(endpoints)[1]


def rounded_cashflows(rows, halfstep=.05, years=20):
    """Joint feasibility for all rounded Table6 cases, common CAPEX/nonpower OPEX.

    Hidden feasible values are a possible rounding witness, not native author data.
    Conventional undiscounted timing is an explicit diagnostic assumption.
    """
    matrix, bounds = [], []
    for index,row in enumerate(rows):
        r=[1.,float(years)]+[0.]*len(rows);r[2+index]=-float(years)
        matrix.extend([r,[-x for x in r]])
        value=row['reliquefaction_LCC_million_USD'];bounds.extend([value+halfstep,-value+halfstep])
    variable_bounds=[(rows[0]['capital_million_USD']-halfstep,rows[0]['capital_million_USD']+halfstep),
                     (rows[0]['non_electric_OM_million_USD_y']-halfstep,rows[0]['non_electric_OM_million_USD_y']+halfstep)]
    variable_bounds.extend((r['profit_million_USD_y']-halfstep,r['profit_million_USD_y']+halfstep) for r in rows)
    return linprog(np.zeros(2+len(rows)),A_ub=matrix,b_ub=bounds,bounds=variable_bounds,method='highs')


def load_inputs():
    data=json.loads((ROOT/'evidence/comprehensive_review_inputs/B3-08.json').read_text())
    if hashlib.sha256((ROOT/data['source_path']).read_bytes()).hexdigest()!=data['source_sha256']:
        raise ValueError('Stale B3-08 source')
    return data


def calculate(data):
    n,a=data['native'],data['analyst'];checks=[];cash=[];splits=[];synthetic=[]
    if CoolProp.__version__ != '8.0.0':
        raise ValueError('Pinned CoolProp8.0.0 required for the pure reference component')
    def add(item,value,unit,scope):checks.append(dict(item=item,value=value,unit=unit,scope=scope))
    for key in ['captured_mol_percent','liquid_mol_percent']:
        add(key+'_sum',math.fsum(r[key] for r in n['captured_liquid_composition']),'mol_percent','Small printed composition rounding; not equilibrium or dehydration validation')
    add('BOG_mol_percent_sum',math.fsum(r['mol_percent'] for r in n['BOG_mole_composition']),'mol_percent','Printed three-component gas,not full cargo-water/solid inventory')
    weight=math.fsum(r['mol_percent']*r['molar_mass_kg_kmol'] for r in n['BOG_mole_composition'])
    co2=next(r for r in n['BOG_mole_composition'] if r['species']=='CO2')
    massfraction=co2['mol_percent']*co2['molar_mass_kg_kmol']/weight
    add('BOG_CO2_mass_fraction_component',massfraction,'kg_CO2/kg_bulk_BOG','Molecular-weight conversion only; native economic BOG is redefined CO2-only,bulk6000basis unresolved')
    add('liquid_water_quoted_ppmv',.917*10000,'ppmv','Native.917mol% retained,no guessed dry-gas correction;cold phase/solid validation required')
    add('N2_vapor_over_liquid_molar_enrichment',1.557/.02,'ratio','Mole ratio,not mass-recovery fraction or validated mixture model')
    add('O2_vapor_over_liquid_molar_enrichment',.056/.001,'ratio','Source rounded molar fractions,not a process reproduction')
    full=n['cargo_volume_m3']*n['cargo_density_kg_m3']
    add('nominal_full_cargo_mass',full/1000,'t','Volume*density stock,not delivered/retained mass')
    add('initial95percent_cargo_mass',full*n['initial_fill']/1000,'t','Initial fill assumption;no actual loading or terminal stock')
    cylinders=n['tank_count']*math.pi*n['tank_diameter_m']**2/4*n['tank_cylinder_height_m']
    add('cylindrical_bodies_volume',cylinders,'m3','Heads/usable-volume definitions missing;not a correction of100000m3nominal capacity')
    add('cylinder_bodies_over_nominal_volume',100*cylinders/n['cargo_volume_m3'],'percent','Geometric approximation only,no new ship capacity accepted')
    add('BOG_if_full_mass_times_assumed_BOR',full*n['BOR_fraction_day']/24,'kg/h','5775using full nominal stock,not quoted5400;source rounding/basis unresolved')
    add('BOG_if95percent_initial_stock',full*n['initial_fill']*n['BOR_fraction_day']/24,'kg/h','5486.25on initial stock,not a measured BOR or corrected source load')
    add('design_over_quoted_nominal_margin',100*(6000/5400-1),'percent','Source6000design versus5400nominal;capacity margin not observed average flow')
    add('annual_BOG_at_design_and90percent_calendar',6000*8760*.9/1000,'t/y','Matches source47304under stated design/load assumption,not actual yearly venting')
    add('pure_CO2_reference_critical_density',CO2_PROPS.PropsSI('rhomass_critical','HEOS::CO2'),'kg/m3','CoolProp8.0.0/SpanEOS pure reference467.6 versus source600quote,not a native mixture critical point or corrected cargo density')
    add('needed_temperature_below_quoted_pure_triple',n['quoted_CO2_triple_T_C']-n['needed_T_C_over98_percent'],'K','9Kbelow quoted pureCO2triple;not proof of mixture phase impossibility or native solid feasibility')
    w=a['illustrative_w_kJ_kg'];mass=n['design_BOG_kg_h']
    add('illustrative270kJkg_to_kW',power_from_specific(w,mass),'kW','270kJ/kg explicitly chosen within plotted range,not exact native output')
    add('illustrative270kJkg_to_kWh_per_t',w/3.6,'kWh/t','Specific work conversion,not a complete capture/transport utility inventory')
    add('unconverted_power_over_kg_h_numeric',power_from_specific(w,mass)/mass,'kWh/kg','RawWkW/mdotkg/h is kWh/kg,not statedkJ/kg;conversion3600must be explicit')
    add('fuel_carbon_to_CO2',n['MDO_mass_C']*44/12,'kg_CO2/kg_fuel','Complete carbon oxidation component only;fuel rate/efficiency required for electrical intensity')
    add('analyst_generator_gamma_from_fuel_rate',a['fuel_CO2_mass_ratio']*.2,'kg_CO2/kWh','Fuel.2kg/kWh is explicitly analyst choice,not source generator calibration')
    terms=treatment_terms(a['illustrative_x'],w,a['illustrative_CL_USD_kJ'],a['illustrative_gamma_kgCO2_kWh'],50,80)
    for key,value in terms.items():add('analyst_unit_consistent_'+key,value,'dimensioned component','Inventedx.975,w270,CL5e-5,gamma.8,CP50,CS80;no native cost/inventory inferred')
    for x in [.957,.972,.981,.982,1.]:
        splits.append(dict(x_CO2_component=x,generated_component_kg_h=6000,recovered_component_kg_h=6000*x,vented_component_kg_h=6000*(1-x),nominal_BOR_vent_fraction_day=.0012*(1-x),scope='Conditional6000CO2-component rate and fixedBOR;native bulk/component reconciliation and actualBOR missing. Not a whole-vessel loss/retention factor.'))
    market={r['item']:r for r in n['market']}
    for year in [2008,2009]:
        for cat,subitems,total in [('allowance',['EU ETS','NSW','CCX','RGGI','AAUs'],'Allowances subtotal'),('project',['Primary CDM','JI','Voluntary market'],'Project subtotal')]:
            for metric in ['volume','value']:
                key=f'{metric}_{year}_'+('Mt' if metric=='volume' else 'million_USD')
                add(f'market_{year}_{cat}_{metric}_sum_minus_subtotal',sum(market[s][key] for s in subitems)-market[total][key],'printed units','Native integer rows;one-unit differences are compatible with component/subtotal rounding')
    total=market['Total']
    p8=total['value_2008_million_USD']/total['volume_2008_Mt'];p9=total['value_2009_million_USD']/total['volume_2009_Mt']
    add('market_2009_table_value',total['value_2009_million_USD']/1000,'billion_USD','143.735table versus114prose,neither silently replaced')
    add('market_2009_minus_prose_value',total['value_2009_million_USD']/1000-114,'billion_USD','Source case discrepancy,not a current market estimate')
    add('market_table_value_growth',100*(total['value_2009_million_USD']/total['value_2008_million_USD']-1),'percent','6.418%compatible with approximate6%prose')
    add('market_2008_mean_value',p8,'USD/tCO2e','Historical aggregate value/volume,not market instrument eligibility or current carbon price')
    add('market_2009_mean_value',p9,'USD/tCO2e','Compatible with16.5source price when table total used')
    add('market_mean_value_drop',100*(1-p9/p8),'percent','40.846%compatible with41%decline;does not reconcile114Bquote')
    witness=a['rounding_shared_cashflow_witness']
    for index,row in enumerate(n['LCC']):
        tax=row['carbon_tax_USD_t'];point=8.9+20*(1.3-row['profit_million_USD_y'])
        possible=witness['capital_million']+20*(witness['OM_million_y']-witness['profits_million_y'][index])
        nominal=n['quoted_annual_BOG_t']*20*tax/1e6
        cash.append(dict(carbon_tax_USD_t=tax,quoted_reliquefaction_LCC_MUSD=row['reliquefaction_LCC_million_USD'],rounded_point_replay_MUSD=point,point_minus_quote_MUSD=point-row['reliquefaction_LCC_million_USD'],possible_rounding_witness_MUSD=possible,quoted_vent_LCC_MUSD=row['vent_only_LCC_million_USD'],nominal_undiscounted_vent_MUSD=nominal,scope='Conventional20yundiscounted diagnostic,not verified author cashflows. Joint shared rounding intervals can explain displayed reliquefaction differences;do not label them proven financial errors.'))
    for case in a['synthetic_price_cases']:
        CP,CS=case['CP'],case['CS'];coefficient=a['synthetic_work_quadratic_coefficient_kJ_kg'];CL=a['illustrative_CL_USD_kJ'];gamma=a['illustrative_gamma_kgCO2_kWh']
        x=synthetic_quadratic_optimum(coefficient,CL,gamma,CP,CS)
        def objective(z):return treatment_terms(z,coefficient*z*z,CL,gamma,CP,CS)['total_USD_t']
        scalar=minimize_scalar(objective,bounds=(0,1),method='bounded',options={'xatol':1e-12})
        best=min([(scalar.fun,float(scalar.x)),(objective(0),0.),(objective(1),1.)])
        synthetic.append(dict(case=case['name'],CP=CP,CS=CS,analytical_x=x,bounded_scalar_x=best[1],total_cost_USD_t=objective(x),emission_t_t=treatment_terms(x,coefficient*x*x,CL,gamma,CP,CS)['emission_tCO2_tBOG'],scope='Inventedw=2000x²,CL5e-5,gamma.8;not native work fit,optimum fraction,fluid/safety validation or GHGfactor.'))
    return checks,splits,cash,synthetic


def main():
    d=load_inputs();checks,splits,cash,synthetic=calculate(d);lp=rounded_cashflows(d['native']['LCC']);OUT.mkdir(parents=True,exist_ok=True)
    for suffix,rows in [('checks',checks),('component_splits',splits),('LCC_rounding',cash),('synthetic_optima',synthetic)]:
        with (OUT/f'B3-08_{suffix}.csv').open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    summary=dict(study_id='B3-08',source_sha256=d['source_sha256'],limited_checks=len(checks),component_split_examples=len(splits),LCC_rows=len(cash),synthetic_scalar_cases=len(synthetic),joint_shared_LCC_rounding_feasible=bool(lp.success),possible_rounding_LP_values=lp.x.tolist() if lp.success else None,
                 pure_reference_backend=dict(CoolProp=CoolProp.__version__,backend='HEOS::CO2',EOS=CO2_PROPS.get_fluid_param_string('CO2','BibTeX-EOS')),scoped_citation_edges=1,native_HYSYS_work_curve_optimum_thermal_or_financial_model_reproduced=False,
                 limits='Literal-unit and accounting diagnostics only;synthetic work and feasible rounding witnesses are not source data. Source3600/1000time/mass bases,CO2-component switch,k,phase feasibility,price labels and graph cases remain open. No accepted operating/GHG input or native value corrected.')
    (OUT/'B3-08_reproduction_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
