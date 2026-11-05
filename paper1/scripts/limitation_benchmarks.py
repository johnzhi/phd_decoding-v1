#!/usr/bin/env python3
"""Within-source checks and a replacement MEA utility reference.

These calculations do not reconstruct the original optimisations or constitute
regional lifecycle mitigation. All empirical values have primary PDF locators.
"""
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[1]
def read(p):
 with (ROOT/p).open() as f:return list(csv.DictReader(f))
def write(p,rows):
 with (ROOT/p).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
 inp=[x for x in read('data/deep_review_values.csv') if x['status'].startswith('ACCEPTED_')];write('data/limitation_benchmark_inputs.csv',inp);p={x['value_id']:float(x['value']) for x in inp};out=[]
 def add(key,value,unit,ids,equation,scope):out.append(dict(result_id=key,value=value,unit=unit,input_ids=';'.join(ids),equation=equation,scope=scope))
 for i in range(1,6):add(f'Cihan_rate_shortfall_{i}',100*(1-p[f'deep_B316_rate{i}']/p['deep_B316_target_rate']),'percent',[f'deep_B316_rate{i}','deep_B316_target_rate'],'100*(1-optimal_no_brine_rate/target_rate)','Within-source reservoir-model comparison under1MPa fault pressure increase; not a measured Japanese shortfall or pressure-rate calibration.')
 add('Chong_compensated_power_intensity',p['deep_B309_residual']/p['deep_B309_output'],'tCO2/MWh',['deep_B309_residual','deep_B309_output'],'residual_tCO2_per_hour/net_MW','Within-source matched-power arithmetic, not a full lifecycle industrial inventory.')
 for label,a,b in [('proxy','deep_B323_offline_initial','deep_B323_offline_optimal'),('full_physics','deep_B323_physics_initial','deep_B323_physics_optimal')]:add('Musayev_'+label+'_gain',100*(p[b]/p[a]-1),'percent',[a,b],'100*(optimal/initial-1)','Within-source model-to-model well-placement comparison. Volumetric reference cancels; no unsupported volume-to-mass conversion or field validation.')
 heat=p['deep_B211_heat'];electric=p['deep_B211_electric']*1000
 ef={x['value_id']:float(x['value']) for x in read('data/reference_inventory_inputs.csv')};kg_per_t=heat*ef['JP_R8_heat_fallback']*1000+electric*ef['JP_R8_electric_fallback']*1000
 case=dict(case_id='MEA_Swedish_CHP_reference_90pct_no_DH_credit',technology='MEA',heat_gj_per_t_captured=heat,electricity_kwh_per_t_captured=electric,utility_inventory_kg_per_t_captured=kg_per_t,source_heat_id='deep_B211_heat',source_electric_id='deep_B211_electric',heat_factor_id='JP_R8_heat_fallback',electric_factor_id='JP_R8_electric_fallback',scope='Replacement utility-accounting reference, not added to NETL. Electricity includes capture/compression/liquefaction; no additional liquefaction or DH output credit.120C/3bar steam conditions; actual district-heat/steam compatibility and complete LCA unverified.')
 write('data/deep_capture_reference_case.csv',[case]);comparisons=[];storage={x['result_id']:float(x['value']) for x in read('outputs/case_evidence_calculations.csv')}['NL_selected_storage_reference_intensity']
 for x in read('outputs/reference_inventory_comparisons.csv'):
  if x['model_case']!='99pct_design_control' or x['utility_scenario']!='NGCC_CANSOLV_90__NO_2025_climate':continue
  capture=float(x['additional_captured_t'])*kg_per_t/1000
  for with_storage in [False,True]:
   additional_storage=float(x['additional_injected_t'])*storage/1000 if with_storage else ''
   remaining=float(x['additional_injected_t'])-float(x['additional_marine_default_wtw_tco2e'])-capture-(additional_storage if with_storage else 0)
   comparisons.append(dict(higher_distance_km=x['higher_distance_km'],utility_case=case['case_id'],additional_injected_t=x['additional_injected_t'],additional_captured_t=x['additional_captured_t'],additional_marine_wtw_t=x['additional_marine_default_wtw_tco2e'],additional_MEA_reference_utility_t=capture,storage_reference_applied=with_storage,additional_storage_reference_t=additional_storage,remaining_allowance_t=remaining,complete_net_avoided_ghg_t='',scope=case['scope']+' Missing other inventory and retention terms remain unquantified.'))
 write('outputs/limitation_benchmark_results.csv',out);write('outputs/MEA_reference_comparisons.csv',comparisons)
 (ROOT/'outputs/limitation_benchmarks_summary.json').write_text(json.dumps(dict(located_benchmark_inputs=len(inp),within_source_calculations=len(out),MEA_reference_sensitivities=len(comparisons),MEA_heat_gj_per_t=heat,MEA_electricity_kwh_per_t=electric,MEA_JP_reporting_inventory_kg_per_t=kg_per_t,complete_lca=False),indent=2)+'\n');print(json.dumps(case,indent=2))
if __name__=='__main__':main()
