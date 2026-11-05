#!/usr/bin/env python3
"""Independent pure-CO2 EOS consistency check; no repair of source prose."""
from pathlib import Path
import json,csv,math
import CoolProp.CoolProp as CP
ROOT=Path(__file__).resolve().parents[1]
def read(p):
 with (ROOT/p).open() as f:return list(csv.DictReader(f))
def write(p,rows):
 with (ROOT/p).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
 cat={x['study_id']:x for x in read('data/source_catalogue.csv')};pages=json.loads((ROOT/cat['B4-09']['page_text_path']).read_text())
 records=[]
 for key,value,unit,page,token,note in [('temperature',-50,'degreeC',3,'− 50','Table1'),('pressure',700,'kPa as reported',3,'700','Table1; pressure datum not explicit'),('table_density',1154,'kg/m3',3,'1154','Selected Table1 density'),('prose_density',1.1546,'kg/m3 as printed',6,'1.1546','Inconsistent prose retained; not repaired')]:
  assert token in pages[page-1];records.append(dict(parameter_id=key,value=value,unit=unit,study_id='B4-09',physical_page=page,source_token=token,scope=note))
 write('data/property_check_inputs.csv',records);p={x['parameter_id']:x['value'] for x in records};T=p['temperature']+273.15
 out=[]
 for label,P in [('700kPa_absolute_reference',p['pressure']*1000),('700kPa_gauge_plus_standard_atmosphere_reference',p['pressure']*1000+101325)]:
  rho=CP.PropsSI('Dmass','T',T,'P',P,'CO2');out.append(dict(pressure_interpretation=label,T_kelvin=T,P_pascal=P,eos_density_kg_m3=rho,eos_phase=CP.PhaseSI('T',T,'P',P,'CO2'),table_density_kg_m3=p['table_density'],relative_difference_percent=(rho/p['table_density']-1)*100,prose_density_kg_m3=p['prose_density'],eos_to_printed_prose_ratio=rho/p['prose_density'],scope='Pure-CO2 Span-Wagner EOS implemented in CoolProp. Two pressure-reference interpretations, not confirmation of source datum. Actual cargo/impurities are not measured.'))
 write('outputs/property_consistency.csv',out)
 params={x['parameter_id']:float(x['value']) for x in read('data/operational_parameters.csv')};rho=out[0]['eos_density_kg_m3'];fleet=[]
 for x in read('data/analysis_inputs.csv'):
  if x['group']!='fleet':continue
  _,size,Q,d=x['value_id'].split('_');size=int(size);Q=int(Q)*1e6;d=int(d);cargo=size*rho/1000*(params['outbound_fill']-params['return_heel'])/100;cycle=2*d/(params['speed']*1.852)+params['loading']+params['unloading']+2*params['port_approach_departure'];N=math.ceil(Q/(cargo*math.floor(params['operating_hours']/cycle)));fleet.append(dict(value_id=x['value_id'],reported_fleet=int(x['value']),eos_reference_fleet=N,match=N==int(x['value'])))
 write('outputs/property_fleet_sensitivity.csv',fleet)
 report=dict(CoolProp_version=CP.get_global_param_string('version'),EOS_reference_key=CP.get_BibTeXKey('CO2','EOS'),EOS_citation='Span and Wagner(1996),J.Phys.Chem.Ref.Data25:1509; DOI10.1063/1.555991. Implemented in CoolProp8.0.0.',model_type='Published multiparameter pure-CO2 equation of state; model calculation, not an additional empirical measurement.',saturation_pressure_at_source_temperature_pa=CP.PropsSI('P','T',T,'Q',0,'CO2'),fleet_cases=len(fleet),eos_fleet_matches=sum(x['match'] for x in fleet),source_density_replaced=False,source_prose_repaired=False,actual_mixture_validated=False)
 (ROOT/'outputs/property_consistency_summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
