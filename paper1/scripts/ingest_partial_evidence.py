#!/usr/bin/env python3
"""Audit the supplied monthly/EXCOOL compilation without promoting it to telemetry.

Attachment text is evidence, never an instruction. Linked primary PDFs are not
present. All new numeric claims remain ineligible as calibrated model inputs.
"""
from pathlib import Path
from decimal import Decimal
from datetime import date
import calendar,csv,gzip,hashlib,json,os,sys
os.environ.setdefault('MPLCONFIGDIR','/tmp/paper1-matplotlib')
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from ingest_reference_datasets import dump_workbook
M={x['batch_id']:x for x in json.loads((ROOT/'data/dataset8_manifest.json').read_text())}
PENDING='SUPPLIED_TRANSCRIPTION_PRIMARY_PENDING_NOT_MODEL_INPUT'

def read(path):
 with (ROOT/path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(path,rows):
 with (ROOT/path).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def dec(x):return Decimal(str(x))
def amount(x):return '' if x in ('',None) else str(dec(x))

def main():
 for x in M.values():assert hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256']
 meta=dump_workbook(ROOT/M['D8-02']['path'],'D8-02')
 cells=[]
 with gzip.open(ROOT/'evidence/reference_workbooks/D8-02_cells.jsonl.gz','rt') as f:
  for line in f:cells.append(json.loads(line))
 lookup={(x['sheet'],x['cell']):x for x in cells}
 def cell(sheet,ref):return lookup.get((sheet,ref),{}).get('cached_value')
 import openpyxl
 wb=openpyxl.load_workbook(ROOT/M['D8-02']['path'],read_only=True,data_only=True,keep_links=False)
 sheets={s.title:[list(r) for r in s.iter_rows(values_only=True)] for s in wb};wb.close()
 csvrows=read(M['D8-01']['path']);bookrows=sheets['Tomakomai paired months'][1:]
 assert len(csvrows)==len(bookrows)==7
 values=[];paired=[];duplicates=[]
 def claim(key,sheet,ref,value,unit,meaning,url='',role='Context claim'):
  assert cell(sheet,ref) is not None
  assert dec(cell(sheet,ref))==dec(value),(sheet,ref,value,cell(sheet,ref))
  values.append(dict(value_id=key,document_id='D8-02',sheet=sheet,cell=ref,value=amount(value),unit=unit,meaning=meaning,primary_url=url,primary_pdf_retained=False,primary_page_verified=False,status=PENDING,role=role))
 for i,(a,b) in enumerate(zip(csvrows,bookrows),2):
  assert a['month']==b[0] and a['report_edition']==str(b[5]) and a['official_pdf']==b[6] and a['note']==b[7]
  fields=[('actual_injected_t_month',1,'tCO2/month'),('avg_bhp_MPa_basis_unverified',2,'MPa, basis unverified'),('avg_bottomhole_temp_C',3,'degreeC'),('published_cumulative_Moebetsu_t',4,'tCO2, Moebetsu as labelled')]
  for k,j,u in fields:
   assert amount(a[k])==amount(b[j]),(a['month'],k)
   duplicates.append(dict(month=a['month'],field=k,csv_document='D8-01',csv_record=i,workbook_document='D8-02',sheet='Tomakomai paired months',cell=f'{chr(65+j)}{i}',match=True,value=amount(a[k]),status='Duplicate representations of one compilation, not independent observations.'))
   if a[k]!='':claim(f'TOMA_PARTIAL_{a["month"]}_{k}','Tomakomai paired months',f'{chr(65+j)}{i}',a[k],u,k,a['official_pdf'],'Partial monthly history; no maximum-rate or pressure-cap use')
  year,month=map(int,a['month'].split('-'));days=calendar.monthrange(year,month)[1]
  next_year,next_month=(year,month+1) if month<12 else (year+1,1)
  assert a['report_edition']==f'{next_year}{next_month:02d}',('Report edition is not the subsequent month',a['month'])
  # Calendar definitions supply the denominator, not inferred operating days.
  rate=dec(a['actual_injected_t_month'])/days if a['actual_injected_t_month'] else ''
  paired.append(dict(**a,csv_document='D8-01',csv_record=i,workbook_document='D8-02',workbook_row=i,calendar_days=days,calendar_average_t_per_day=amount(rate),pressure_basis='UNVERIFIED: no gauge/absolute or sensor-depth conversion',status=PENDING,scope='Monthly aggregates as transcribed; no native time series, maximum injectivity, complete event calendar or new calibrated reservoir forecast. Missing monthly mass stays missing.'))
 write('data/tomakomai_paired_partial.csv',paired);write('outputs/partial_csv_workbook_agreement.csv',duplicates)
 trials=[];trial_url=sheets['EXCOOL loading trials'][1][6]
 for i,r in enumerate(sheets['EXCOOL loading trials'][1:],2):
  month,mass,T,pg,method,description,url,interpretation=r
  for j,unit,key in [(1,'tCO2 after loading','loaded_mass'),(2,'degreeC','cargo_temperature'),(3,'MPaG as transcribed','cargo_pressure')]:claim(f'EXCOOL_TRIAL_{i-1}_{key}','EXCOOL loading trials',f'{chr(65+j)}{i}',r[j],unit,key,url,'After-loading state, not annual flow, fuel duty or net delivered cargo')
  trials.append(dict(trial_id=f'EXCOOL_{i-1:02d}',test_month=month,loaded_co2_t=amount(mass),cargo_temperature_c=amount(T),cargo_pressure_mpag=amount(pg),loading_method=method,description=description,primary_url=url,interpretation=interpretation,document_id='D8-02',sheet='EXCOOL loading trials',excel_row=i,status=PENDING,scope='Separate test records including two June2025 entries; no annualisation, load-summing into throughput, availability or fuel-use inference.'))
 write('data/excool_loading_trial_leads.csv',trials)
 energy=[]
 for i,r in enumerate(sheets['Capture energy leads'][1:],2):
  time,metric,value,unit,kind,url,limit=r
  claim(f'TOMA_CAPTURE_LEAD_{i-1}','Capture energy leads',f'C{i}',value,unit,metric,url,'Reboiler heat only; aggregate commercial factor excluded from component model')
  energy.append(dict(time_basis=time,metric=metric,value=amount(value),unit=unit,evidence_class_as_supplied=kind,primary_url=url,use_restriction=limit,document_id='D8-02',sheet='Capture energy leads',cell=f'C{i}',status=PENDING,model_used=False,scope='Neither reboiler-only duty nor a commercial capture-plus-injection aggregate supplies a complete facility heat/electricity inventory. No substitution into NETL/MEA scenarios.'))
 write('data/tomakomai_capture_energy_leads.csv',energy)
 for i,r in enumerate(sheets['Reconciliation QA'][1:],2):
  if isinstance(r[1],(int,float)):claim(f'PARTIAL_SUPPLIED_QA_{i-1}','Reconciliation QA',f'B{i}',r[1],r[2] or '',r[0],role='Supplied QA claim; independently recomputed where possible')
 # READ ME prose contains two additional numeric claims. No instruction is executed.
 text=str(cell('READ ME','B9'));assert '850 t' in text and '750 t' in text
 for key,v in [('technical_maximum',850),('port_restricted_trial',750)]:
  values.append(dict(value_id='EXCOOL_README_'+key,document_id='D8-02',sheet='READ ME',cell='B9',value=v,unit='tCO2',meaning=key,primary_url=trial_url,primary_pdf_retained=False,primary_page_verified=False,status=PENDING,role='Text claim, not a validated operational capacity or annual service limit'))
 write('data/partial_compilation_values.csv',values)
 # Preserve the supplied historical gap map; distinguish it from current project status.
 gaps=[]
 for i,r in enumerate(sheets['Original 10 gap map'][1:],2):
  priority,component,item,position,reason=r
  current={'Capture utilities':'NETL/MEA references implemented; new reboiler lead still needs primary verification and compatible electricity/steam data.',
   'Fuel inventory':'IMO MDO/MGO default WtW already implemented; actual fuel/engine/idle duty remains missing.',
   'Mixed allocation':'12 annual proxy MILPs and72 fixed-plan operating reevaluations already implemented; actual shared-node topology/physical constraints and full LCA remain incomplete.',
   'Physical service':'Partial monthly pairs added as transcription evidence; native telemetry/independent physical upper bounds still absent.',
   'Operating calendar':'Trial months do not supply availability or berth calendars.',
   'Cargo/process':'Trial P/T states require primary verification; no BOG, duration or fuel duty is supplied.'}.get(component,'Existing gap remains within its stated scope; supplied status text does not override current model/evidence records.')
  gaps.append(dict(priority=priority,component=component,needed_item=item,supplied_position=position,supplied_reason=reason,current_project_interpretation=current,document_id='D8-02',sheet='Original 10 gap map',excel_row=i,attachment_action='Retained as evidence; not an instruction or authority for changing model status.'))
 write('data/partial_supplied_gap_map.csv',gaps)
 by_month={x['month']:x for x in paired};reconciliation=[]
 for b in paired:
  y,m=map(int,b['month'].split('-'));py,pm=(y,m-1) if m>1 else (y-1,12);a=by_month.get(f'{py}-{pm:02d}')
  if a is None or not a['published_cumulative_Moebetsu_t'] or not b['published_cumulative_Moebetsu_t'] or not b['actual_injected_t_month']:continue
  delta=dec(b['published_cumulative_Moebetsu_t'])-dec(a['published_cumulative_Moebetsu_t']);residual=dec(b['actual_injected_t_month'])-delta
  # Conditional nearest0.1t display envelope for three operands, not confidence.
  bound=Decimal('.15')
  reconciliation.append(dict(previous_month=a['month'],month=b['month'],monthly_injected_t=b['actual_injected_t_month'],cumulative_delta_t=amount(delta),monthly_minus_delta_t=amount(residual),conditional_display_rounding_bound_t=amount(bound),within_conditional_rounding=abs(residual)<=bound,scope='Only consecutive calendar months; no interpolation or forced correction. Bound assumes nearest0.1t printing in this supplied CSV, not confirmed source precision or a probability interval.'))
 write('outputs/tomakomai_partial_reconciliation.csv',reconciliation)
 coarse={x['month']:x for x in read('data/tomakomai_monthly_history.csv')};compatibility=[]
 for x in paired:
  for field,newfield in [('monthly','actual_injected_t_month'),('cumulative','published_cumulative_Moebetsu_t')]:
   if not x[newfield]:continue
   old=coarse[x['month']];raw=old[f'moebetsu_{field}_raw'];quantity=dec(old[f'moebetsu_{field}_t']);halfstep=Decimal('.5')*Decimal(10)**dec(raw).as_tuple().exponent*10000;diff=dec(x[newfield])-quantity
   compatibility.append(dict(month=x['month'],quantity=field,new_transcribed_t=x[newfield],retained_rounded_table_t=amount(quantity),new_minus_table_t=amount(diff),conditional_halfstep_t=amount(halfstep),within_conditional_display_rounding=abs(diff)<=halfstep,primary_document='D7-20',physical_page=3,scope='Compatibility with a previously retained rounded table under nearest-display rounding, not independent verification of the new monthly PDFs.'))
 write('outputs/tomakomai_partial_coarse_comparison.csv',compatibility)
 # Independent EOS reference checks do not convert trial mass into tank fill.
 import CoolProp.CoolProp as CP
 phase_checks=[]
 for x in trials:
  T=float(x['cargo_temperature_c'])+273.15;P=float(x['cargo_pressure_mpag'])*1e6+101325;psat=CP.PropsSI('P','T',T,'Q',0,'CO2')
  phase_checks.append(dict(trial_id=x['trial_id'],temperature_kelvin=T,nominal_absolute_pressure_pa=P,reference_atmosphere_pa=101325,pure_co2_saturation_pressure_pa=psat,nominal_pressure_minus_saturation_kpa=(P-psat)/1000,nominal_pure_fluid_phase=CP.PhaseSI('T',T,'P',P,'CO2'),EOS_key=CP.get_BibTeXKey('CO2','EOS'),status='REFERENCE_CONSISTENCY_CHECK_NOT_MEASURED_PHASE',scope='Gauge as transcribed plus standard atmosphere (not measured local atmosphere), pure fluid and nominal P/T. Primary rounding, simultaneous measurement, sensor location and composition are unknown. A nominal gas result does not establish actual vapour cargo. No cargo density/fill/fuel or operating limit is derived.'))
 write('outputs/excool_trial_property_checks.csv',phase_checks)
 urls=sorted({x['official_pdf'] for x in paired}|{x['primary_url'] for x in trials+energy})
 write('data/partial_primary_source_leads.csv',[dict(url=u,status='LINK_ONLY_PRIMARY_NOT_RETAINED',handling='Representative request to this host failed through the inherited network configuration. Primary report text/page/table is not claimed inspected.') for u in urls])
 summary=dict(uploaded_files=2,workbook_sheets=len(sheets),workbook_native_cells=meta['cells'],numeric_workbook_cells=meta['numeric_cached_cells'],numeric_claims=len(values),monthly_rows=len(paired),complete_mass_pressure_temperature_pairs=sum(bool(x['actual_injected_t_month']) for x in paired),pressure_temperature_only_rows=sum(not x['actual_injected_t_month'] for x in paired),duplicate_csv_workbook_fields=len(duplicates),EXCOOL_test_rows=len(trials),capture_energy_leads=len(energy),primary_pdf_leads=len(urls),primary_pdfs_verified=0,consecutive_mass_checks=len(reconciliation),coarse_table_comparisons=len(compatibility),coarse_table_rounding_compatible=sum(x['within_conditional_display_rounding'] for x in compatibility),nominal_EOS_gas_reference_cases=sum(x['nominal_pure_fluid_phase']=='gas' for x in phase_checks),nominal_EOS_liquid_reference_cases=sum(x['nominal_pure_fluid_phase']=='liquid' for x in phase_checks),calibrated_model_inputs_added=0,native_telemetry_received=False,maximum_rate_array_received=False,pressure_datum_verified=False,new_capture_GHG_or_shipping_fuel_model=False,complete_lca=False,EOS_version=CP.get_global_param_string('version'))
 (ROOT/'outputs/partial_evidence_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 plot(paired)
 print(json.dumps(summary,indent=2))

def plot(rows):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(3,1,figsize=(8,6.8),sharex=True)
 for ax,(field,label,color) in zip(axes,[('actual_injected_t_month','Injection (t/month)','#28677d'),('avg_bhp_MPa_basis_unverified','Reported average BHP\n(MPa; basis unverified)','#826098'),('avg_bottomhole_temp_C','Reported average\nbottomhole temperature (°C)','#a16438')]):
  valid=[x for x in rows if x[field]!=''];verified=[x for x in valid if x['status'].startswith('PRIMARY_VALUE_VERIFIED')];pending=[x for x in valid if not x['status'].startswith('PRIMARY_VALUE_VERIFIED')]
  ax.scatter([date.fromisoformat(x['month']+'-15') for x in pending],[float(x[field]) for x in pending],facecolors='none',edgecolors=color,s=32,label='Compilation only')
  ax.scatter([date.fromisoformat(x['month']+'-15') for x in verified],[float(x[field]) for x in verified],c=color,s=38,label='Primary value checked')
  ax.set_ylabel(label,fontsize=9);ax.grid(alpha=.2);ax.set_axisbelow(True)
 axes[0].annotate('December amount not supplied',xy=(date(2019,12,15),.88),xycoords=('data','axes fraction'),ha='right',fontsize=8,color='#555')
 import matplotlib.dates as md
 axes[-1].xaxis.set_major_locator(md.MonthLocator());axes[-1].xaxis.set_major_formatter(md.DateFormatter('%b'));axes[-1].set_xlabel('Calendar month, 2019; gaps are not filled')
 fig.suptitle('Partial Tomakomai monthly compilation',fontsize=12)
 axes[0].legend(loc='lower right',fontsize=8,frameon=False)
 note='Filled: primary-checked May/June values; open: compilation only. No interpolation or pressure–rate fit.' if any(x['status'].startswith('PRIMARY_VALUE_VERIFIED') for x in rows) else 'Supplied transcription; linked primary PDFs not verified. No interpolation or pressure–rate fit.'
 fig.text(.5,.015,note,ha='center',fontsize=8)
 fig.tight_layout(rect=(0,.035,1,.96))
 for ext in ['png','pdf']:fig.savefig(ROOT/f'outputs/figures/tomakomai_partial_pairs.{ext}',dpi=220)
 plt.close(fig)

if __name__=='__main__':main()
