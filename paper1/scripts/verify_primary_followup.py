#!/usr/bin/env python3
"""Verify three retained primary PDFs, preserving unresolved labels and dates.

Run after ingest_partial_evidence.py. The supplied ZIP is an audit memo, never
an authority to mark other URLs verified or execute attachment instructions.
"""
from pathlib import Path
from decimal import Decimal
import csv,json,hashlib,re,unicodedata,sys
import fitz
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
M={x['batch_id']:x for x in json.loads((ROOT/'data/dataset9_manifest.json').read_text())}
PRIMARY='PRIMARY_VALUE_VERIFIED_CONTEXT_ONLY_NOT_CALIBRATED_INPUT'
DERIVED='DERIVED_FROM_VERIFIED_PRIMARY_INPUTS_NOT_CORRECTED_OBSERVATION'
PENDING='SUPPLIED_TRANSCRIPTION_PRIMARY_PENDING_NOT_MODEL_INPUT'
URLS={'D9-02':'https://www.classnk.or.jp/hp/pdf/research/rd/2026/12_e05.pdf','D9-03':'https://www.jccs-tomakomai-monitoring.com/JCCS/wp-content/uploads/2019/07/201907_ENG.pdf','D9-04':'https://www.jccs-tomakomai-monitoring.com/JCCS/wp-content/uploads/2019/06/201906_ENG.pdf'}
def read(path):
 with (ROOT/path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(path,rows):
 with (ROOT/path).open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def D(x):return Decimal(str(x).replace(',','').replace('−','-'))
def norm(s):return unicodedata.normalize('NFKC',s)
def number(s):return re.search(r'[-+−]?\d[\d,]*(?:\.\d+)?',s).group()

def main():
 for x in M.values():assert hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256']
 docs={sid:fitz.open(ROOT/M[sid]['path']) for sid in URLS}
 values=[];byid={}
 def add(key,sid,page,token,unit,meaning,case,bbox=None,value=None,mode='NATIVE_TEXT_OR_TABLE',note=''):
  p=docs[sid][page-1];text=p.get_text()
  if mode!='VISUALLY_CHECKED_RASTER_TABLE':assert token in text,(key,token)
  if bbox is None:
   rects=p.search_for(token);assert rects,(key,token);bbox=rects[0]
  x=dict(value_id=key,document_id=sid,physical_page=page,source_token=token,value=str(D(token) if value is None else D(value)),unit=unit,meaning=meaning,case=case,source_bbox=json.dumps(list(bbox)),source_mode=mode,visual_page_checked=True,primary_sha256=M[sid]['sha256'],source_url=URLS[sid],status=PRIMARY,use_as_calibrated_input=False,note=note)
  values.append(x);byid[key]=x;return x
 def v(key):return D(byid[key]['value'])
 # Native Table3 cells were visually checked against the retained page image.
 table=docs['D9-02'][4].find_tables().tables[0];raw=table.extract();assert len(raw)==8 and raw[0][5]=='Pressure\n(MPaG)'
 trials=[];direct={}
 for j,row in enumerate(raw[1:],1):
  ids={};month,description,method,mass,temp,pressure=row
  for col,token,unit,key in [(3,mass,'tCO2 after loading','loaded_mass'),(4,temp,'degreeC','cargo_temperature'),(5,pressure,'MPaG','cargo_pressure')]:
   keyid=f'P_EXCOOL_{j}_{key}';add(keyid,'D9-02',5,token,unit,key,f'Table3 row{j};{month}',table.rows[j].cells[col],note='Table footnote: quantity, temperature and pressure values are after loading. No annual throughput or fuel duty.');ids[key]=keyid;direct[f'EXCOOL_TRIAL_{j}_{key}']=keyid
  trials.append(dict(trial_id=f'EXCOOL_{j:02d}',date_as_printed=month,test_item=description.replace('\n',' '),loading_method=method,loaded_co2_raw=mass,loaded_co2_t=str(D(mass)),temperature_raw=temp,temperature_c=str(D(temp)),pressure_raw=pressure,pressure_mpag=str(D(pressure)),document_id='D9-02',physical_page=5,table='Table3',source_table_row=j,values_after_loading=True,mass_value_id=ids['loaded_mass'],temperature_value_id=ids['cargo_temperature'],pressure_value_id=ids['cargo_pressure'],status=PRIMARY,scope='Distinct loading tests, not annual voyages, net delivered mass, fuel duty, transfer duration or an availability calendar.'))
 write('data/excool_verified_loading_tests.csv',trials)
 add('P_EXCOOL_tank_count','D9-02',3,'two','tanks','Cargo holds, one tank per hold','Design prose',value=2,note='Prose spans pp3–4: two cargo holds and one tank per hold.')
 add('P_EXCOOL_each_tank_volume','D9-02',4,'725','m3','Volume per cargo tank','Design prose')
 add('P_EXCOOL_max_load','D9-02',4,'850','tCO2','Stated maximum CO2 load','Design prose',note='Vessel specification, not a realised annual service or international-carrier parameter.')
 add('P_EXCOOL_port_limit','D9-02',5,'750','tCO2','Upper limit due to port restrictions in described tests','Trial prose')
 direct['EXCOOL_README_technical_maximum']='P_EXCOOL_max_load';direct['EXCOOL_README_port_restricted_trial']='P_EXCOOL_port_limit'
 # Table2 is raster in this PDF. The retained rendered page was visually read;
 # never represent these cells as mechanically text-verified tokens.
 visual=[('length','72','m','Length overall',[298,528,479,546]),('breadth','12.5','m','Breadth overall',[298,528,479,546]),('draught','4.5','m','Draught',[298,528,479,546]),('gross_tonnage','997','tons as printed','Gross tonnage',[298,545,479,563]),('deadweight','1,261','tons as printed','Deadweight',[298,545,479,563]),('tank_volume','1,450','m3','Total cargo tank capacity',[298,580,479,597]),('design_Tmin','-50','degreeC','Minimum design temperature',[298,596,479,614]),('design_Tmax','+45','degreeC','Maximum design temperature',[298,596,479,614]),('design_pressure','1.9','MPaG','Design pressure',[298,596,479,614])]
 for key,token,unit,meaning,bbox in visual:add('P_EXCOOL_'+key,'D9-02',4,token,unit,meaning,'Table2',bbox,mode='VISUALLY_CHECKED_RASTER_TABLE',note='Visual transcription; retain edition differences from MHI2024 particulars, not silent replacements.')
 # Section3.3 provides a voyage case, not a future fleet/availability calendar.
 voyage_inputs=[('roundtrip_miles','1 900','miles as printed','Approximate round-trip distance',1900),('roundtrip_km','3 500','km','Approximate round-trip distance',3500),('cargo_mass','496','tons as printed','Reported unchanged cargo weight, rounded prose',496),('out_hours','90','hours','Outbound elapsed time including offshore anchorage',90),('moored_hours','50','hours','Moored duration; no cargo handling',50),('return_hours','73','hours','Return voyage duration',73),('out_T0','–47.8','degreeC','Outbound departure temperature',-47.8),('out_P0','0.64','MPaG','Outbound departure pressure',.64),('out_T1','–44.9','degreeC','Outbound arrival temperature',-44.9),('out_P1','0.74','MPaG','Outbound arrival pressure',.74),('return_T0','–43.5','degreeC','Return departure temperature',-43.5),('return_P0','0.79','MPaG','Return departure pressure',.79),('return_T1','–41.1','degreeC','Return arrival temperature',-41.1),('return_P1','0.86','MPaG','Return arrival pressure',.86),('out_T_rate','0.032','degreeC/hour','Reported outbound temperature rise rate',.032),('out_P_rate','0.0011','MPaG/hour','Reported outbound pressure rise rate',.0011),('return_T_rate','0.033','degreeC/hour','Reported return temperature rise rate',.033),('return_P_rate','0.0010','MPaG/hour','Reported return pressure rise rate',.0010),('moored_T_rate','0.028','degreeC/hour','Reported moored temperature rise rate',.028),('moored_P_rate','0.0010','MPaG/hour','Reported moored pressure rise rate',.0010)]
 for key,token,unit,meaning,val in voyage_inputs:
  bbox=docs['D9-02'][5].search_for(token)[-1] if key=='moored_P_rate' else None
  add('P_VOYAGE_'+key,'D9-02',6,token,unit,meaning,'July2025 Maizuru–Hirara–Maizuru test',bbox=bbox,value=val,note='Durations/distances are approximate; unchanged496tons is rounded prose, not a measured0.8t difference from496.8t Table3. No venting/no onboard reliquefier are source-reported for this test, not universal parameters.')
 injection=[];headers=[];observations=[]
 for sid,month,planmonth,headerdate,headertotal,headeramount in [('D9-04','2019-05','2019-06','2019-06-29','261,729.8','0.0'),('D9-03','2019-06','2019-07','2019-07-30','264,193.1','397.0')]:
  p=docs[sid][11];t=p.find_tables().tables[0];rows=t.extract();assert month[-2:] in ['05','06']
  assert ('May 2019' if month.endswith('05') else 'June 2019') in rows[0][1]
  for j,formation in [(1,'Moebetsu'),(2,'Takinoue')]:
   assert formation in rows[j][0];ids={}
   for col,key,unit in [(1,'monthly','tCO2/month'),(2,'planned','tCO2/month, future plan'),(3,'cumulative','tCO2 as labelled')]:
    token=number(rows[j][col]);keyid=f'P_TOMA_{month}_{formation}_{key}';add(keyid,sid,12,token,unit,key,month+' '+formation,t.rows[j].cells[col],note='Table date/formation label preserved; future plan is not actual injection.');ids[key]=keyid
   injection.append(dict(month=month,formation=formation,monthly_actual_t=byid[ids['monthly']]['value'],planned_month=planmonth,planned_t=byid[ids['planned']]['value'],cumulative_as_labelled_t=byid[ids['cumulative']]['value'],document_id=sid,physical_page=12,monthly_value_id=ids['monthly'],planned_value_id=ids['planned'],cumulative_value_id=ids['cumulative'],status=PRIMARY,scope='Formation labels copied without correcting May cumulative classification. The header has a different current date.'))
   if formation=='Moebetsu':
    direct[f'TOMA_PARTIAL_{month}_actual_injected_t_month']=ids['monthly'];direct[f'TOMA_PARTIAL_{month}_published_cumulative_Moebetsu_t']=ids['cumulative']
  for key,token,meaning in [('header_total',headertotal,'Overall cumulative amount in dated header'),('header_amount',headeramount,'Injection-rate header value, unit tonnes as printed')]:
   bb=next(r for r in p.search_for(token) if r.x0<500)
   add(f'P_TOMA_{month}_{key}',sid,12,token,'tonnes as printed',meaning,headerdate,bb,note='Current header date, not the table month. Header rate caption does not supply a native daily rate series.')
  headers.append(dict(report_issue='201906' if sid=='D9-04' else '201907',table_month=month,header_as_of=headerdate,overall_cumulative_t=str(D(headertotal)),header_injection_amount_t_as_printed=str(D(headeramount)),document_id=sid,physical_page=12,total_value_id=f'P_TOMA_{month}_header_total',amount_value_id=f'P_TOMA_{month}_header_amount',scope='Header date must not be conflated with end-of-table-month. Rate caption retains original tonnes unit.'))
  prefixes={'Moe_OB2':'Moebetsu Fm. Observation Well OB-2','Taki_OB3':'Takinoue Fm. Observation Well OB-3','Taki_OB1':'Takinoue Fm. Observation Well OB-1','Taki_injector':'Takinoue Fm. Injection Well','Moe_injector':'Moebetsu Fm. Injection Well'}
  for well,prefix in prefixes.items():
   ids={};depths=[]
   for page,key,unit in [(17,'pressure','MPa; gauge/absolute unspecified'),(18,'temperature','degreeC')]:
    lines=[(''.join(s['text'] for s in line['spans']),line['bbox']) for b in docs[sid][page-1].get_text('dict')['blocks'] for line in b.get('lines',[])]
    text,bbox=next((s,b) for s,b in lines if ''.join(norm(s).split()).startswith(''.join(prefix.split())))
    match=re.search(r'Average:\s*([\d.]+).*?Depth\s*(\d+)m',norm(text));assert match,(well,text);token,depth=match.groups();depths.append(depth)
    kid=f'P_TOMA_{month}_{well}_{key}';add(kid,sid,page,token,unit,key,month+' '+prefix,bbox,note='Average and reported depth, not maximum pressure or a calibrated limit.');ids[key]=kid
    if key=='pressure':
     depid=f'P_TOMA_{month}_{well}_depth';add(depid,sid,page,depth,'m; reference unspecified','Reported monitoring depth',month+' '+prefix,bbox,note='Depth datum not identified; do not substitute for the2024 sensor921mTVDSS or completion973mTVDSS.')
   assert depths[0]==depths[1]
   observations.append(dict(month=month,well_id=well,well_label=prefix,average_pressure_mpa=byid[ids['pressure']]['value'],average_temperature_c=byid[ids['temperature']]['value'],reported_depth_m=depths[0],depth_reference='UNSPECIFIED_AS_PRINTED',pressure_reference='MPa; gauge/absolute unspecified',document_id=sid,pressure_page=17,temperature_page=18,pressure_value_id=ids['pressure'],temperature_value_id=ids['temperature'],depth_value_id=depid,status=PRIMARY,scope='Monthly means; not native telemetry, maximum injectivity or a cross-depth pressure-cap comparison.'))
   if well=='Moe_injector':
    direct[f'TOMA_PARTIAL_{month}_avg_bhp_MPa_basis_unverified']=ids['pressure'];direct[f'TOMA_PARTIAL_{month}_avg_bottomhole_temp_C']=ids['temperature']
 direct['PARTIAL_SUPPLIED_QA_2']='P_TOMA_2019-06_Moebetsu_monthly';direct['PARTIAL_SUPPLIED_QA_4']='P_TOMA_2019-06_Takinoue_cumulative'
 write('data/primary_followup_values.csv',values);write('data/tomakomai_primary_injection_tables.csv',injection);write('data/tomakomai_primary_header_totals.csv',headers);write('data/tomakomai_primary_well_means.csv',observations)
 calculations=[]
 def calc(key,value,unit,ids,equation,scope):calculations.append(dict(result_id=key,value=str(value),unit=unit,input_ids=';'.join(ids),equation=equation,scope=scope))
 may='P_TOMA_2019-05_Moebetsu_cumulative';june='P_TOMA_2019-06_Moebetsu_cumulative';mass='P_TOMA_2019-06_Moebetsu_monthly';taki='P_TOMA_2019-06_Takinoue_cumulative';header='P_TOMA_2019-05_header_total'
 calc('formation_labelled_delta',v(june)-v(may),'tCO2',[june,may],'June labelled Moebetsu cumulative - May labelled Moebetsu cumulative','Labels preserved; not a corrected formation history.')
 calc('formation_labelled_discrepancy',v(mass)-(v(june)-v(may)),'tCO2',[mass,june,may],'June monthly - formation-labelled cumulative delta','98.1t discrepancy remains; no authoritative formation-label correction.')
 calc('June29_header_minus_May_label',v(header)-v(may),'tCO2',[header,may],'June29 overall header - May Moebetsu-labelled cumulative','Exact numerical match to June monthly is consistent with a mixed-classification hypothesis. May overall classification and June29/end-June identity are not independently confirmed.')
 calc('June_formation_sum_minus_June29_header',v(june)+v(taki)-v(header),'tCO2',[june,taki,header],'End-June formation sum - June29 overall header','0.1t difference retains printed precision and different dates; do not silently force equality.')
 maytaki='P_TOMA_2019-05_Takinoue_cumulative'
 calc('hypothetical_May_Moebetsu',v(may)-v(maytaki),'tCO2',[may,maytaki],'May labelled quantity - May Takinoue cumulative','HYPOTHESIS_ONLY_NOT_OBSERVED: conditional on May quantity actually being overall. Never replaces the source value.')
 for key,unit in [('pressure','MPa, unverified common pressure basis'),('temperature','degreeC')]:
  a=f'P_TOMA_2019-05_Moe_injector_{key}';b=f'P_TOMA_2019-06_Moe_injector_{key}';calc('June_minus_May_Moebetsu_'+key,v(b)-v(a),unit,[b,a],'June monthly mean - May monthly mean','Descriptive same-report-well means, not a rate-response fit, absolute/gauge verification or maximum service.')
 voyage=[]
 for phase,T0,T1,P0,P1,h in [('outbound','out_T0','out_T1','out_P0','out_P1','out_hours'),('moored','out_T1','return_T0','out_P1','return_P0','moored_hours'),('return','return_T0','return_T1','return_P0','return_P1','return_hours')]:
  prefix='out' if phase=='outbound' else phase
  ids={key:'P_VOYAGE_'+key for key in [T0,T1,P0,P1,h]}
  temp=(v(ids[T1])-v(ids[T0]))/v(ids[h]);press=(v(ids[P1])-v(ids[P0]))/v(ids[h]);tr='P_VOYAGE_'+prefix+'_T_rate';pr='P_VOYAGE_'+prefix+'_P_rate'
  for kind,value,unit,a,b,reported in [('temperature',temp,'degreeC/hour',T0,T1,tr),('pressure',press,'MPaG/hour',P0,P1,pr)]:
   calc('EXCOOL_'+phase+'_'+kind+'_rise_rate',value,unit,[ids[b],ids[a],ids[h],reported],'(end-start)/approximate_elapsed_hours','Within-source endpoint reconstruction; reported rate is a comparison. Not a constant heat-leak/BOG law, future shutdown threshold or large-carrier parameter.')
  voyage.append(dict(phase=phase,approximate_hours=str(v(ids[h])),start_temperature_c=str(v(ids[T0])),end_temperature_c=str(v(ids[T1])),start_pressure_mpag=str(v(ids[P0])),end_pressure_mpag=str(v(ids[P1])),reported_temperature_rise_c_per_hour=str(v(tr)),reconstructed_temperature_rise_c_per_hour=str(temp),reported_pressure_rise_mpag_per_hour=str(v(pr)),reconstructed_pressure_rise_mpag_per_hour=str(press),document_id='D9-02',physical_page=6,reported_BOG_fate='No venting reported during this test; no onboard reliquefier',cargo_handling_during_moored_phase='None reported',scope='July2025 single voyage; outbound includes anchorage. Moored endpoints are outbound arrival and return departure. No fuel/maintenance calendar, constant future BOG law or geometric storage retention implied.'))
 hours=['P_VOYAGE_out_hours','P_VOYAGE_moored_hours','P_VOYAGE_return_hours']
 calc('EXCOOL_reported_phase_hours_sum',sum(v(i) for i in hours),'hours',hours,'90+50+73','Sum of approximate reported intervals; not annual availability, active engine hours or terminal turnaround.')
 write('data/excool_reported_voyage_reference.csv',voyage)
 write('outputs/primary_followup_calculations.csv',calculations)
 # Update the existing current register, retaining the original compilation state.
 derived={'PARTIAL_SUPPLIED_QA_1':'formation_labelled_delta','PARTIAL_SUPPLIED_QA_3':'formation_labelled_discrepancy'}
 cc={x['result_id']:x for x in calculations};claims=read('data/partial_compilation_values.csv')
 for x in claims:
  x['original_compilation_status']=x.get('original_compilation_status',PENDING)
  x.update(primary_document_id='',primary_physical_page='',primary_value_id='',primary_source_bbox='')
  if x['value_id'] in direct:
   pv=byid[direct[x['value_id']]];assert D(x['value'])==D(pv['value']);x.update(status=PRIMARY,primary_pdf_retained=True,primary_page_verified=True,primary_document_id=pv['document_id'],primary_physical_page=pv['physical_page'],primary_value_id=pv['value_id'],primary_source_bbox=pv['source_bbox'])
  elif x['value_id'] in derived:
   c=cc[derived[x['value_id']]];assert D(x['value'])==D(c['value']);x.update(status=DERIVED,primary_pdf_retained=True,primary_page_verified=False,primary_document_id='D9-03;D9-04',primary_physical_page='12;12',primary_value_id=c['input_ids'])
 write('data/partial_compilation_values.csv',claims)
 pairs=read('data/tomakomai_paired_partial.csv')
 for x in pairs:
  x.update(primary_document_id='',primary_pages='',reported_sensor_depth_m='',depth_reference='Unverified or unspecified')
  if x['month'] in ['2019-05','2019-06']:
   sid='D9-04' if x['month']=='2019-05' else 'D9-03';x.update(status=PRIMARY,primary_document_id=sid,primary_pages='12;17;18',reported_sensor_depth_m='930',depth_reference='Depth930m as printed; vertical/reference datum unspecified')
 write('data/tomakomai_paired_partial.csv',pairs)
 leads=read('data/excool_loading_trial_leads.csv')
 for x in leads:x.update(status=PRIMARY,primary_document_id='D9-02',primary_physical_page=5,primary_table='Table3',after_loading=True)
 write('data/excool_loading_trial_leads.csv',leads)
 urls={URLS[s]:s for s in URLS};sources=read('data/partial_primary_source_leads.csv')
 for x in sources:
  sid=urls.get(x['url']);x.update(primary_document_id=sid or '',sha256=M[sid]['sha256'] if sid else '',targeted_physical_pages='3;4;5;6;7' if sid=='D9-02' else '12;17;18' if sid else '')
  if sid:x.update(status='PRIMARY_PDF_RETAINED_TARGETED_TEXT_AND_VISUAL_VERIFIED',handling='Original uploaded PDF retained; selected native tables/text and page renders checked. No native telemetry or model calibration inferred.')
 write('data/partial_primary_source_leads.csv',sources)
 gaps=read('data/partial_supplied_gap_map.csv')
 for x in gaps:
  if x['component']=='Physical service':x['current_project_interpretation']='May/June monthly mass and P/T values primary-checked; formation cumulative classification and pressure/depth reference remain unresolved. No native telemetry or independent physical upper bounds.'
  if x['component']=='Cargo/process':x['current_project_interpretation']='Seven EXCOOL Table3 states and one reported voyage P/T/elapsed-time/no-venting case primary-verified. No fuel, complete BOG duty, loading duration or independent operating envelope.'
  if x['component']=='Operating calendar':x['current_project_interpretation']='One voyage reports approximately90h outbound including anchorage,50h moored without cargo handling,73h return. These do not supply annual availability or a cargo-transfer turnaround distribution.'
 write('data/partial_supplied_gap_map.csv',gaps)
 # Third-party claims of online inspection in the ZIP are not our local checks.
 package=read('evidence/dataset9/verification_package/primary_source_status_R22.csv');audit=[]
 for x in package:
  sid=urls.get(x['publisher_pdf_url']);audit.append(dict(**x,local_primary_document=sid or '',local_status='PRIMARY_RETAINED_TARGETED_VERIFIED' if sid else 'NOT_LOCALLY_VERIFIED',handling='ZIP status/memo retained as secondary assertions; only the three separately supplied primary PDFs support local status upgrades.'))
 write('data/verification_package_status_audit.csv',audit)
 # Source precision is now visible: conditional nearest displayed-unit rounding.
 import CoolProp.CoolProp as CP
 eos=read('outputs/excool_trial_property_checks.csv')
 for x,t in zip(eos,trials):
  assert x['trial_id']==t['trial_id'];T=float(D(t['temperature_raw']))+273.15;P=float(D(t['pressure_raw']))*1e6+101325
  dT=float(Decimal('.5')*Decimal(10)**D(t['temperature_raw']).as_tuple().exponent);dP=float(Decimal('.5')*Decimal(10)**D(t['pressure_raw']).as_tuple().exponent)*1e6
  low=(P-dP-CP.PropsSI('P','T',T+dT,'Q',0,'CO2'))/1000;high=(P+dP-CP.PropsSI('P','T',T-dT,'Q',0,'CO2'))/1000
  classification='STRADDLES_SATURATION' if low<=0<=high else 'ENTIRELY_BELOW_SATURATION' if high<0 else 'ENTIRELY_ABOVE_SATURATION'
  x.update(primary_document_id='D9-02',primary_physical_page=5,pressure_basis_verified_as='MPaG',conditional_temperature_halfstep_c=dT,conditional_pressure_halfstep_pa=dP,conditional_min_pressure_minus_saturation_kpa=low,conditional_max_pressure_minus_saturation_kpa=high,conditional_display_rounding_class=classification,scope='Table3 P/T and MPaG are primary-verified; all values after loading. Pure fluid plus standard atmosphere, not measured ambient. Nearest0.1C/0.01MPaG display rounding is a conditional sensitivity, not measurement uncertainty or proof of actual phase. Source sensor location/timing/composition remain unspecified; a nominal gas result does not establish actual vapour cargo. No cargo density/fill/fuel/limit is derived.')
 write('outputs/excool_trial_property_checks.csv',eos)
 old=json.loads((ROOT/'outputs/partial_evidence_summary.json').read_text());old.update(primary_pdfs_verified=3,primary_value_claims_verified=sum(x['status']==PRIMARY for x in claims),derived_claims_reproduced_from_primary=sum(x['status']==DERIVED for x in claims),claims_still_primary_pending=sum(x['status']==PENDING for x in claims),monthly_complete_pairs_primary_verified=2,maximum_rate_array_received=False,pressure_datum_verified=False)
 (ROOT/'outputs/partial_evidence_summary.json').write_text(json.dumps(old,indent=2)+'\n')
 summary=dict(uploaded_files=4,retained_primary_pdfs=3,indexed_primary_pages=sum(len(d) for d in docs.values()),targeted_primary_value_records=len(values),verified_loading_tests=len(trials),reported_voyage_phase_records=len(voyage),verified_well_month_pairs=len(observations),verified_Moebetsu_monthly_pairs=2,reproduced_calculations=len(calculations),current_compilation_primary_verified=old['primary_value_claims_verified'],current_compilation_derived_from_primary=old['derived_claims_reproduced_from_primary'],current_compilation_pending=old['claims_still_primary_pending'],nominal_EOS_gas_reference_cases=sum(x['nominal_pure_fluid_phase']=='gas' for x in eos),conditional_rounding_straddles=sum(x['conditional_display_rounding_class']=='STRADDLES_SATURATION' for x in eos),conditional_rounding_entirely_below=sum(x['conditional_display_rounding_class']=='ENTIRELY_BELOW_SATURATION' for x in eos),formation_label_issue_resolved=False,monthly_pressure_reference_verified=False,native_telemetry_received=False,model_inputs_or_optimisation_results_changed=False,complete_lca=False)
 (ROOT/'outputs/primary_followup_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 from ingest_partial_evidence import plot
 plot(pairs)
 for d in docs.values():d.close()
 print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
