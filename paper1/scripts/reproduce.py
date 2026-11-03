#!/usr/bin/env python3
"""Reproduce literature calculations; no fitted regional CCS simulation.

All physical inputs are looked up by ID in data/analysis_inputs.csv.
100, 1000 and 1 below are unit/percentage/algebraic constants, not assumed data.
"""
from pathlib import Path
import csv,json,hashlib,math,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/paper1-matplotlib')
os.environ.setdefault('XDG_CACHE_HOME','/tmp/paper1-cache')
ROOT=Path(__file__).resolve().parents[1]

def read_csv(name):
 with (ROOT/'data'/name).open(encoding='utf-8') as f:return list(csv.DictReader(f))

def validate_sources():
 cat=read_csv('source_catalogue.csv');lookup={x['study_id']:x for x in cat}
 for x in cat:
  p=ROOT/x['pdf_path']
  if hashlib.sha256(p.read_bytes()).hexdigest()!=x['sha256']:raise ValueError(f'PDF hash mismatch: {p}')
  pages=json.loads((ROOT/x['page_text_path']).read_text())
  if len(pages)!=int(x['pages']):raise ValueError(f'Page count mismatch: {p}')
 for x in read_csv('curated_values.csv'):
  pages=json.loads((ROOT/lookup[x['study_id']]['page_text_path']).read_text())
  page=pages[int(x['pdf_page'])-1]
  if not x['source_token'] or x['source_token'] not in page:raise ValueError(f"Source token absent: {x['value_id']}")
 # Reject corrupted or context-only parameters in the calculation input file.
 curated={x['value_id']:x for x in read_csv('curated_values.csv')}
 inputs=read_csv('analysis_inputs.csv')
 if len({x['value_id'] for x in inputs})!=len(inputs):raise ValueError('Duplicate analysis input IDs')
 for x in inputs:
  if x!=curated[x['value_id']]:raise ValueError(f"Analysis row differs from curated row: {x['value_id']}")
  if x['status']!='ACCEPTED_FOR_STATED_CONTEXT' or x['group']=='context':raise ValueError(f"Ineligible analysis input: {x['value_id']}")
 return {'pdf_files':len(cat),'unique_publications':sum(not x['duplicate_of'] for x in cat),'unique_pdf_pages':sum(int(x['pages']) for x in cat if not x['duplicate_of']),'extracted_records':len(read_csv('all_extracted_values.csv')),'curated_records':len(curated),'analysis_inputs':len(inputs),'source_checks':'All PDF SHA256 hashes, page counts and curated source tokens pass. Token checks locate text; table mapping and interpretation require human review.'}

def calculate():
 raw={x['value_id']:x for x in read_csv('analysis_inputs.csv')};used=set();out=[]
 def v(key):
  x=raw[key]
  if x['status']!='ACCEPTED_FOR_STATED_CONTEXT':raise ValueError(key)
  used.add(key);return float(x['value'])
 def emit(group,case,metric,value,unit,ids,equation,boundary):
  out.append(dict(result_id=f'R{len(out)+1:03d}',group=group,case=case,metric=metric,value=value,unit=unit,input_ids=';'.join(ids),equation=equation,boundary=boundary))
 for s in 'ABCD':
  ids=[f'thermal_{s}_isothermal',f'thermal_{s}_cooled'];a,b=map(v,ids)
  emit('thermal',s,'pressure_ceiling_drop',a-b,'psi',ids,'P_isothermal - P_cooled','Same published seal; not injectivity or stored-mass reduction')
  emit('thermal',s,'pressure_ceiling_drop_percent',100*(a-b)/a,'%',ids,'100*(P_isothermal-P_cooled)/P_isothermal','Percent of isothermal pressure ceiling as printed, not allowable pressure headroom')
 for feed in ['pure','inland']:
  ids=[f'liq_{feed}_7',f'liq_{feed}_15'];a,b=map(v,ids)
  emit('liquefaction',feed,'electricity_7_minus_15_barg',a-b,'kWh/tCO2',ids,'e7 - e15','Within-feed comparison only; no shipping or grid factors')
  emit('liquefaction',feed,'electricity_reduction_percent',100*(a-b)/a,'%',ids,'100*(e7-e15)/e7','Within-feed comparison only')
 for pressure in [7,15]:
  ids=[f'liq_pure_{pressure}',f'liq_inland_{pressure}'];a,b=map(v,ids)
  emit('liquefaction',str(pressure),'pure_to_inland_electricity_ratio',a/b,'ratio',ids,'e_pure/e_inland','Different feed pressures; not causal effect of destination')
 for case in ['99','100']:
  ids=[f'buffer_{case}','buffer_ship'];a,b=map(v,ids)
  emit('buffer',case,'buffer_as_percent_of_ship',100*a/b,'%',ids,'100*buffer/ship','Transport-completion case in Bjerketvedt; excludes alternative cycle-mass denominator')
 for case in ['1-1','1-2','1-3','2-1','2-2','2-3']:
  for n in ['005','010','015']:
   ids=[f'bog_{case}_{n}_emissions',f'bog_{case}_{n}_transport'];a,b=map(v,ids)
   emit('bog',f'{case}; N2={int(n)/100:g} mol%','partial_process_emissions_intensity',a/b,'kgCO2/tCO2 transported',ids,'emissions[t/year]*1000 / (transport[1000 t/year]*1000)','Purge plus auxiliary generation; excludes full propulsion and upstream lifecycle effects')
 base=v('gwp_NL07');lo=v('retention_SW_A');hi=v('retention_MW_A');ids=['retention_SW_A','retention_MW_A']
 emit('retention','MW_A vs SW_A','additional_gross_storage',hi-lo,'MtCO2',ids,'R_high - R_low','Published South Sumatra optimisation; not net avoided GHG')
 emit('retention','MW_A vs SW_A','gross_storage_increase',100*(hi-lo)/lo,'%',ids,'100*(R_high-R_low)/R_low','Same published source–sink system; additional well GHG not included')
 crit=1000*(1-lo/hi*(1-base/1000))
 emit('hybrid','South Sumatra retention + NL07 reference','score_crossing_high_path_reported_intensity',crit,'kgCO2e/tCO2 stored',ids+['gwp_NL07'],'1000*[1-(R_low/R_high)*(1-e_low/1000)]','Diagnostic cross-study score only; reported GWP includes fugitives. Loss accounting and omitted burdens must be reconciled before avoided-emissions interpretation')
 for name in ['NL07','NL15','SM07','SM15','combined07','combined15']:
  key='gwp_'+name;e=v(key)
  emit('intensity_threshold',name,'required_storage_uplift_for_score_equality',100*((1-base/1000)/(1-e/1000)-1),'%', ['gwp_NL07',key], '100*[(1-e_low/1000)/(1-e_high/1000)-1]','Reported-GWP score equality only; requires loss reconciliation and equal omitted burdens for mitigation interpretation. Portfolio configurations, not isolated pressure effects')
  balhi=hi*(1-e/1000);ballo=lo*(1-base/1000)
  emit('hybrid',name,'difference_in_stored_mass_minus_reported_GWP_score',balhi-ballo,'MtCO2e',ids+['gwp_NL07',key],'R_high*(1-e_high/1000)-R_low*(1-e_low/1000)','Cross-study score only; fugitive/source-loss double counting and extra capture/well burdens require reconciliation; not avoided emissions')
 for key,x in raw.items():
  if x['group']=='fleet':
   emit('fleet',x['scenario'],'published_ship_count',v(key),'ships',[key],'Direct transcription, no reconstruction','Original Table 7 outputs; density conflict prevents independent cargo/fleet reconstruction')
 if used!=set(raw):raise ValueError(f'Unused registered analysis input IDs: {set(raw)-used}')
 return out

def save_results(rows):
 out=ROOT/'outputs';out.mkdir(exist_ok=True)
 with (out/'calculated_results.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (out/'calculated_results.json').write_text(json.dumps(rows,indent=2))
 groups={}
 for x in rows:groups.setdefault(x['group'],[]).append(x)
 (out/'result_tables.md').write_text('\n\n'.join('### '+g+'\n\n| Case | Metric | Value | Unit |\n|---|---|---:|---|\n'+'\n'.join(f"| {x['case']} | {x['metric']} | {x['value']:.6g} | {x['unit']} |" for x in rs) for g,rs in groups.items()))

def figures(rows):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'font.size':10,'figure.dpi':160,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
 out=ROOT/'outputs/figures';out.mkdir(exist_ok=True)
 raw={x['value_id']:float(x['value']) for x in read_csv('analysis_inputs.csv')}
 def save(fig,name):
  fig.savefig(out/(name+'.png'),bbox_inches='tight');fig.savefig(out/(name+'.pdf'),bbox_inches='tight');plt.close(fig)
 fig,ax=plt.subplots(figsize=(6.5,3.6));xx=list(range(4));ax.bar([i-.18 for i in xx],[raw[f'thermal_{s}_isothermal'] for s in 'ABCD'],.36,label='Isothermal');ax.bar([i+.18 for i in xx],[raw[f'thermal_{s}_cooled'] for s in 'ABCD'],.36,label='Estimated 50°C cooling');ax.set_xticks(xx,list('ABCD'));ax.set_xlabel('Seal');ax.set_ylabel('Published pressure ceiling (psi)');ax.legend(frameon=False);save(fig,'thermal_pressure')
 fig,ax=plt.subplots(figsize=(6.5,3.6));xx=[0,1];ax.bar([i-.18 for i in xx],[raw['liq_pure_7'],raw['liq_inland_7']],.36,label='7 barg');ax.bar([i+.18 for i in xx],[raw['liq_pure_15'],raw['liq_inland_15']],.36,label='15 barg');ax.set_xticks(xx,['Pure feed','Pressurised inland feed']);ax.set_ylabel('Conditioning electricity (kWh/tCO₂)');ax.legend(frameon=False);save(fig,'liquefaction_feed_pressure')
 fig,ax=plt.subplots(figsize=(7,3.8))
 for case in ['1-1','1-2','1-3','2-1','2-2','2-3']:
  ys=[next(x['value'] for x in rows if x['group']=='bog' and x['case']==f'{case}; N2={int(n)/100:g} mol%') for n in ['005','010','015']]
  ax.plot([.05,.1,.15],ys,'o-',label='Case '+case)
 ax.set_xlabel('N₂ impurity (mol%)');ax.set_ylabel('Partial process CO₂ (kg/t transported)');ax.set_xticks([.05,.1,.15]);ax.legend(ncol=2,frameon=False);save(fig,'bog_partial_emissions')
 rr=[x for x in rows if x['group']=='intensity_threshold'];fig,ax=plt.subplots(figsize=(7,3.8));ax.bar(['NL\n0.7 MPa','NL\n1.5 MPa','SM\n0.7 MPa','SM\n1.5 MPa','Combined\n0.7 MPa','Combined\n1.5 MPa'],[x['value'] for x in rr]);uplift=next(x['value'] for x in rows if x['metric']=='gross_storage_increase');ax.axhline(uplift,color='firebrick',linestyle='--',label=f'Derived storage uplift: {uplift:.2f}%');ax.set_ylabel('Storage uplift for reported-score equality (%)');ax.set_xlabel('Published post-capture intensity scenario');ax.legend(frameon=False);save(fig,'proxy_thresholds')

if __name__=='__main__':
 audit=validate_sources();results=calculate();save_results(results);figures(results)
 audit['calculated_results']=len(results);(ROOT/'outputs/validation_report.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2))
