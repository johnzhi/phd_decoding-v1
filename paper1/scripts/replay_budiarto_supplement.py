#!/usr/bin/env python3
"""Replay rounded published allocations; this is not a new CCS optimisation.

Blanks remain blanks in the input. Totals sum printed cells only, treating blanks
as no reported allocation for reconstruction, not as measured physical zeros.
Rounding envelopes assume conventional rounding to the printed precision; they
are deterministic display-resolution checks, not confidence intervals.
"""
from pathlib import Path
from decimal import Decimal as D
import csv,json,hashlib,os,itertools
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR','/tmp/paper1-matplotlib')
os.environ.setdefault('XDG_CACHE_HOME','/tmp/paper1-cache')
def rd(name):
 with (ROOT/name).open(encoding='utf-8') as f:return list(csv.DictReader(f))
def wr(name,rows):
 with (ROOT/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def validate():
 from docx import Document
 from PIL import Image
 import numpy as np,matplotlib
 doc=rd('data/supplement_documents.csv')[0];path=ROOT/doc['path']
 assert hashlib.sha256(path.read_bytes()).hexdigest()==doc['sha256'],'Supplement SHA256 mismatch'
 source=Document(path);tables=[[[c.text for c in row.cells] for row in t.rows] for t in source.tables]
 assert len(tables)==3
 assert tables==json.loads((ROOT/'evidence/supplements/B4-06-S1/native_tables.json').read_text())['tables']
 for x in rd('data/supplement_sources.csv'):
  row=tables[0][int(x['docx_row'])-1];assert row==[x['source'],x['industry_type'],x['co2_rate_mtpa'],x['capture_cost_usd_per_t']]
 for x in rd('data/supplement_reservoirs.csv'):
  row=tables[1][int(x['docx_row'])-1];assert row==[x['reservoir'],x['reservoir_type'],x['capacity_mt'],x['estimated_start_year'],x['storage_cost_reported']]
 for x in rd('data/supplement_distances.csv'):
  row=tables[2][int(x['docx_row'])-1];src=row[2 if x['hub']=='h1' else 3]
  assert x['distance_km']==('' if src=='-' else src)
 media=json.loads((ROOT/'evidence/supplements/B4-06-S1/media_manifest.json').read_text())
 for x in media:assert hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256']
 annual=rd('data/supplement_annual_injection.csv');keys={(x['scenario'],x['reservoir'],int(x['year'])) for x in annual}
 expected=set(itertools.product(['SW-A','MW-A','MW-D'],[f'r{i}' for i in range(1,9)],range(2027,2057)))
 assert len(annual)==len(keys)==720 and keys==expected
 # Independent auxiliary occupancy/colour check supports the visually reviewed annotation transcription.
 palette=np.array([matplotlib.colormaps['viridis_r'](i/255)[:3] for i in range(256)])*255;ims={};diffs=[]
 for x in annual:
  if x['source_image'] not in ims:ims[x['source_image']]=Image.open(ROOT/x['source_image']).convert('RGB')
  box=[int(v) for v in x['cell_bbox'].split(',')];a=np.array(ims[x['source_image']].crop((box[0]+4,box[1]+4,box[2]-4,box[3]-4)))
  colored=np.mean(a.min(axis=2)<220)>.4;printed=bool(x['reported_value_mtpa']);assert bool(colored)==printed,x['value_id']
  if printed:
   assert x['cell_status']=='PRINTED_ONE_DECIMAL_REVIEWED' and len(x['reported_value_mtpa'].split('.')[-1])==1
   rgb=np.median(a.reshape(-1,3),axis=0);idx=np.argmin(((palette-rgb)**2).sum(axis=1));diff=abs(idx/255*5-float(x['reported_value_mtpa']));diffs.append(diff)
   assert diff<.09,f"Heatmap colour/annotation check failed: {x['value_id']}"
  else:assert x['cell_status']=='BLANK_NOT_NUMERIC_ZERO'
 return dict(supplement_sha256=doc['sha256'],source_tables=3,embedded_figures=len(media),annual_grid_cells=len(annual),printed_numeric_cells=len(diffs),blank_cells=len(annual)-len(diffs),max_auxiliary_colour_difference=max(diffs),interpretation='Native tables match DOCX; annotations visually transcribed and independently checked for cell occupancy and approximate source colour. Colour precision is not used in calculations.')
def numeric_ledger():
 values=rd('data/supplement_table_values.csv')
 for x in rd('data/supplement_annual_injection.csv'):
  if x['reported_value_mtpa']:
   values.append(dict(value_id=x['value_id'],study_id=x['document_id'],parameter='Annual reservoir CO2 injection allocation',value=x['reported_value_mtpa'],unit='MtCO2/year',pdf_page='',locator=f"Figure {x['source_figure']}, reservoir {x['reservoir']}, year {x['year']}; {x['source_image']}; bbox {x['cell_bbox']}",scenario=x['scenario'],evidence_type='Published MILP allocation output, rounded figure annotation',boundary='South Sumatra original optimisation case, not Japanese or independent injection-capacity input',status=x['cell_status'],transferability_note='One decimal only; no hidden precision invented. Allocation result is not a physical maximum service profile. Blank grid cells are preserved separately.'))
 wr('data/supplement_values.csv',values)
 old=[x for x in rd('data/all_extracted_values.csv') if x['Study ID']!='B4-06-S1'];fields=list(old[0])
 for n,x in enumerate(values,len(old)+1):old.append(dict(zip(fields,[f'E{n:04d}',x['study_id'],x['parameter'],x['value'],x['unit'],'',x['locator'],x['evidence_type'],x['scenario'],x['status'],x['transferability_note'],'','',''])))
 wr('data/all_extracted_values.csv',old)
 return len(values),len(old)
def calculate():
 sources=rd('data/supplement_sources.csv');reservoirs={x['reservoir']:x for x in rd('data/supplement_reservoirs.csv')};cells=rd('data/supplement_annual_injection.csv');inputs={x['value_id']:x for x in rd('data/analysis_inputs.csv')}
 source=sum(D(x['co2_rate_mtpa']) for x in sources);source_half=sum(D(10)**(-len(x['co2_rate_mtpa'].split('.')[-1]))/2 for x in sources)
 annual=[];summary=[];by_res=[]
 for scenario in ['SW-A','MW-A','MW-D']:
  data=[x for x in cells if x['scenario']==scenario];years=sorted({int(x['year']) for x in data});cumulative=D(0);half=D(0);prestart=[]
  for year in years:
   yr=[x for x in data if int(x['year'])==year and x['reported_value_mtpa']];total=sum((D(x['reported_value_mtpa']) for x in yr),D(0));display_half=D('.05')*len(yr);cumulative+=total;half+=display_half
   for x in yr:
    if year<int(reservoirs[x['reservoir']]['estimated_start_year']):prestart.append(x['value_id'])
   annual.append(dict(scenario=scenario,year=year,reported_cells=len(yr),sum_printed_allocations_mt=float(total),conditional_rounding_lower_mt=float(total-display_half),conditional_rounding_upper_mt=float(total+display_half),cumulative_sum_printed_mt=float(cumulative),nominal_source_rate_mtpa=float(source),nominal_source_minus_printed_sum_mt=float(source-total),source_rate_inside_conditional_rounding_envelope=bool(total-display_half<=source<=total+display_half),basis='Sum of printed cells; blanks have no reported allocation. Negative nominal gap can be rounding, not physical excess.'))
  assert not prestart,f'Printed allocation before reservoir readiness: {prestart}'
  reported=D(inputs['retention_SW_A' if scenario=='SW-A' else 'retention_MW_A']['value'])
  summary.append(dict(scenario=scenario,first_year=years[0],last_year=years[-1],annual_bins=len(years),printed_numeric_cells=sum(bool(x['reported_value_mtpa']) for x in data),sum_printed_allocations_mt=float(cumulative),main_paper_cumulative_mt=float(reported),printed_minus_main_mt=float(cumulative-reported),conditional_rounding_lower_mt=float(cumulative-half),conditional_rounding_upper_mt=float(cumulative+half),main_total_inside_conditional_rounding_envelope=bool(cumulative-half<=reported<=cumulative+half),nominal_source_over_horizon_mt=float(source*len(years)),source_rate_precision_halfwidth_mtpa=float(source_half),allocated_before_estimated_start_count=len(prestart),interpretation='Rounded allocation replay; not independently reproduced MILP or calibrated whole-chain mitigation. MW-D reported total shares the same main-paper value as MW-A.'))
  for rid,r in reservoirs.items():
   vals=[D(x['reported_value_mtpa']) for x in data if x['reservoir']==rid and x['reported_value_mtpa']];s=sum(vals,D(0));h=D('.05')*len(vals);cap=D(r['capacity_mt'])
   by_res.append(dict(scenario=scenario,reservoir=rid,capacity_mt=float(cap),sum_printed_allocations_mt=float(s),display_rounding_lower_mt=float(s-h),display_rounding_upper_mt=float(s+h),rounded_sum_minus_capacity_mt=float(s-cap),interpretation='Comparative audit only; source capacity and printed allocations are rounded, and no exact capacity violation is inferred from a nominal excess.'))
 wr('outputs/supplement_annual_replay.csv',annual);wr('outputs/supplement_scenario_summary.csv',summary);wr('outputs/supplement_reservoir_audit.csv',by_res)
 out=dict(source_count=len(sources),reservoir_count=len(reservoirs),nominal_annual_source_mtpa=float(source),nominal_source_30_bins_mt=float(source*len(years)),sum_candidate_reservoir_capacity_mt=float(sum(D(r['capacity_mt']) for r in reservoirs.values())),hub_distance_values=sum(x['cell_status']=='REPORTED_VALUE' for x in rd('data/supplement_distances.csv')),summary=summary)
 (ROOT/'outputs/supplement_replay.json').write_text(json.dumps(out,indent=2));return out

def figures():
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'font.size':10,'figure.dpi':160,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
 data=rd('outputs/supplement_annual_replay.csv');fig,axs=plt.subplots(2,1,figsize=(7.4,6.5),sharex=True)
 for scenario in ['SW-A','MW-A','MW-D']:
  ds=[x for x in data if x['scenario']==scenario];xx=[int(x['year']) for x in ds]
  axs[0].plot(xx,[float(x['sum_printed_allocations_mt']) for x in ds],marker='.',label=scenario)
  axs[1].plot(xx,[float(x['cumulative_sum_printed_mt']) for x in ds],label=scenario)
 axs[0].axhline(float(data[0]['nominal_source_rate_mtpa']),linestyle='--',color='grey',label='Table S1 source-rate sum')
 axs[0].set_ylabel('Sum of printed allocations (Mt/year)');axs[1].set_ylabel('Cumulative printed allocations (Mt)');axs[1].set_xlabel('Calendar year');axs[0].legend(frameon=False,ncol=2);fig.tight_layout()
 for ext in ['png','pdf']:fig.savefig(ROOT/f'outputs/figures/supplement_annual_replay.{ext}',bbox_inches='tight')
 plt.close(fig)
if __name__=='__main__':
 audit=validate();n,total=numeric_ledger();result=calculate();figures();audit.update(supplement_numeric_records=n,all_extracted_records=total,physical_optimisation_reproduced=False,net_mitigation_model_completed=False)
 (ROOT/'outputs/supplement_validation_report.json').write_text(json.dumps(audit,indent=2));print(json.dumps(dict(validation=audit,replay=result),indent=2))
