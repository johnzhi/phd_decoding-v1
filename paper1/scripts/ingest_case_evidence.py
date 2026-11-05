#!/usr/bin/env python3
"""Review the third reference intake with explicit source/measurement boundaries.

No attachment is executed or treated as an instruction. Original bytes remain
unchanged. Published tables, derived checks and optional transfers stay separate.
"""
from pathlib import Path
from datetime import datetime
from decimal import Decimal
import csv,json,hashlib,re,sys,os
os.environ.setdefault('MPLCONFIGDIR','/tmp/paper1-matplotlib')
os.environ.setdefault('XDG_CACHE_HOME','/tmp/paper1-cache')
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from ingest_reference_datasets import dump_workbook
M={x['batch_id']:x for x in json.loads((ROOT/'data/dataset7_manifest.json').read_text())}
V=[]
def read(path):
 with (ROOT/path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(path,rows):
 with (ROOT/path).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def pages(sid):return json.loads((ROOT/M[sid]['page_text_path']).read_text())
def val(key,sid,p,value,unit,token,quantity,case='',kind='Published reference input',note='',bbox=''):
 assert token in pages(sid)[p-1],(sid,p,key,token)
 V.append(dict(value_id=key,document_id=sid,physical_page=p,source_token=token,value=value,unit=unit,quantity=quantity,case=case,evidence_type=kind,interpretation=note,source_bbox=bbox));return value

def native_tables():
 meta=[]
 for sid in ['D7-01','D7-02','D7-03','D7-04','D7-05','D7-06']:
  b=(ROOT/M[sid]['path']).read_bytes();text=b.decode('utf-8-sig')
  meta.append(dict(document_id=sid,encoding='UTF-8 with BOM' if b.startswith(b'\xef\xbb\xbf') else 'UTF-8',original_bytes=len(b),instruction_status='Attachment content is source data; no commands or instructions executed.'))
 write('data/japan_export_encoding.csv',meta)
 emissions=[]
 for i,r in enumerate(read(M['D7-03']['path']),2):
  category=r['温室効果ガスの種類']
  for field,raw in r.items():
   if field=='温室効果ガスの種類':continue
   year=int(re.search(r'\d{4}',field).group());num=float(raw) if re.fullmatch(r'\d+(?:\.\d+)?',raw) else ''
   emissions.append(dict(document_id='D7-03',csv_record=i,category=category,emissions_fiscal_year=year,raw_value=raw,value=num,unit='tCO2 (original header; gas rows are reporting CO2-equivalent quantities)',status='REPORTED' if num!='' else 'NO_REPORT',entity='Nippon Steel per separately supplied info.csv',scope='Company reporting aggregate; not one capture stream or matched no-CCS industrial inventory. Categories/adjusted totals must not be summed indiscriminately.'))
 write('data/japan_company_emissions.csv',emissions)
 facilities=[]
 for i,r in enumerate(read(M['D7-06']['path']),2):
  facilities.append(dict(document_id='D7-06',csv_record=i,report_year=r['報告年度'],facility_name=r['事業所名'],industry=r['事業所において行われる事業'],municipality=r['所在地'],reported_ghg_t=r['温室効果ガス算定排出量(tCO2)'],source_url=r['ページ'],scope='Reporting-year label preserved; not silently matched to emissions fiscal year. Similar site names are not merged. Total GHG is not capturable CO2 or available CO2 supply.'))
 write('data/japan_facility_candidates.csv',facilities)
 # All text remains available in the original export; do not attach ENEOS text to Nippon Steel.
 info=read(M['D7-04']['path'])[0];extra=(ROOT/M['D7-01']['path']).read_text(encoding='utf-8-sig')
 identity=dict(info_document='D7-04',metadata=info,additional_document='D7-01',additional_mentions_ENEOS='ENEOS' in extra,additional_mentions_Nippon_Steel='日本製鉄' in extra,status='ENTITY_MISMATCH_UNRESOLVED',handling='Do not merge additional-information statements or Scope1/2/3 values with the Nippon Steel company/facility inventory. Source identity requires export metadata.')
 (ROOT/'outputs/japan_export_identity_audit.json').write_text(json.dumps(identity,ensure_ascii=False,indent=2)+'\n')
 wb=dump_workbook(ROOT/M['D7-07']['path'],'D7-07')
 import openpyxl
 w=openpyxl.load_workbook(ROOT/M['D7-07']['path'],read_only=True,data_only=True,keep_links=False);s=w.active;it=iter(s.values);head=list(next(it))[:20];cppi=[]
 for i,row in enumerate(it,2):
  if row[0] is None:continue
  r={k:('' if v is None else v) for k,v in zip(head,row[:20])};r={'document_id':'D7-07','sheet':s.title,'excel_row':i,**r,'scope':'Container-port index/rank and berth share; not liquid-CO2 terminal turnaround hours. Zero index is retained, not treated as a zero-hour port call.'};cppi.append(r)
 w.close();write('data/cppi_port_reference.csv',cppi)
 return dict(company_emission_cells=len(emissions),reported_company_cells=sum(x['status']=='REPORTED' for x in emissions),facility_rows=len(facilities),cppi_ports=len(cppi),cppi_native_cells=wb['cells'])

def monthly_history():
 """Extract real rotated PDF text by month-column coordinates, not OCR guesses."""
 import fitz
 d=fitz.open(ROOT/M['D7-20']['path']);p=d[2];words=[];mat=fitz.Matrix(1,1).prerotate(90)
 for x0,y0,x1,y1,token,*_ in p.get_text('words'):
  b=fitz.Rect(x0,y0,x1,y1)*mat
  words.append(dict(x=(b.x0+b.x1)/2,y=(b.y0+b.y1)/2,token=token,bbox=[x0,y0,x1,y1]))
 def line(y):return sorted([x for x in words if abs(x['y']-y)<1 and re.fullmatch(r'\d+(?:\.\d+)?',x['token'])],key=lambda x:x['x'])
 columns=line(126);assert len(columns)==45
 fields=[('moebetsu_monthly',223.2),('moebetsu_cumulative',245.6),('both_monthly',409.1),('both_cumulative',437.2)]
 arrays={name:line(y) for name,y in fields};assert all(len(a)==45 for a in arrays.values())
 records=[]
 for j,col in enumerate(columns):
  year=2016+(j+3)//12;month=(j+3)%12+1;assert int(col['token'])==month
  r=dict(document_id='D7-20',physical_page=3,table='Table3-2',month=f'{year}-{month:02d}',fiscal_year=year if month>=4 else year-1)
  for name,_ in fields:
   a=arrays[name][j];assert abs(a['x']-col['x'])<1
   r[name+'_raw']=a['token'];r[name+'_t']=float(Decimal(a['token'])*10000)
   val(f'TOMA_{r["month"]}_{name}','D7-20',3,float(a['token']),'10^4 tCO2',a['token'],name,r['month'],'Reported historical quantity (rounded table)','Explicit numeric zero retains printed precision; monthly/cumulative and formation/combined rows remain distinct.',json.dumps(a['bbox']))
  r['scope']='Reported historical monthly totals, not independent maximum injection capacity or a reconstructed pressure series.';records.append(r)
 write('data/tomakomai_monthly_history.csv',records)
 fiscal=[]
 for i,(a,b) in enumerate(zip(line(466.2),line(494.4)),2016):
  fiscal.append(dict(fiscal_year=i,reported_annual_10kt=a['token'],reported_cumulative_10kt=b['token'],document_id='D7-20',physical_page=3))
  for tag,t in [('annual',a),('cumulative',b)]:val(f'TOMA_FY{i}_{tag}','D7-20',3,float(t['token']),'10^4 tCO2',t['token'],f'Fiscal-year {tag} reported mass',str(i),'Reported historical quantity (rounded table)',bbox=json.dumps(t['bbox']))
 write('data/tomakomai_fiscal_history.csv',fiscal)
 audit=[]
 for i in [2016,2017,2018,2019]:
  rs=[r for r in records if r['fiscal_year']==i];f=next(x for x in fiscal if x['fiscal_year']==i)
  for formation in ['moebetsu','both']:
   total=sum(Decimal(r[formation+'_monthly_raw'])*10000 for r in rs)
   audit.append(dict(fiscal_year=i,series=formation,reported_months=len(rs),sum_printed_monthly_t=str(total),reported_fiscal_t=str(Decimal(f['reported_annual_10kt'])*10000),difference_t=str(total-Decimal(f['reported_annual_10kt'])*10000),handling='Keep printed precision; do not force monthly/fiscal agreement or infer missing months. FY2019 table stops at December.'))
 write('outputs/tomakomai_history_audit.csv',audit)
 d.close();return records

def shutin_records():
 # Dates and causes are transcribed from Table5.2-1 (2024 report); times use the source local clock.
 spec=[
 (1,'2016-04-08 06:14','2016-04-08 17:01',11,58800,81,'External pressure rise'),
 (2,'2016-04-17 22:16','2016-05-07 15:15',473,109351,2558,'Compressor stopped'),
 (3,'2016-05-13 01:00','2016-05-14 14:19',37,139056,4330,'Safety-valve malfunction'),
 (4,'2016-05-24 09:00','2017-02-05 17:35',6177,71079,7163,'Planned shut-in'),
 (5,'2017-05-25 09:47','2017-07-13 16:15',1183,64861,61239,'Planned shut-in'),
 (6,'2017-08-01 10:00','2017-08-03 09:57',48,88474,65793,'Planned shut-in'),
 (7,'2017-08-15 09:00','2017-09-16 12:00',771,100124,69070,'Inspection/repair'),
 (8,'2017-11-30 09:27','2018-01-06 11:50',890,85159,109250,'Planned shut-in'),
 (9,'2018-05-25 09:20','2018-07-25 11:36',1466,87709,188136,'Planned shut-in'),
 (10,'2018-09-01 02:25','2018-12-27 13:28',2819,189602,207209,'Compressor stopped'),
 (11,'2019-02-08 08:33','2019-02-19 11:18',267,83620,217425,'Inspection/repair'),
 (12,'2019-03-26 10:37','2019-03-28 11:03',48,218008,233438,'Supply-side trouble'),
 (13,'2019-04-19 13:31','2019-05-08 11:28',454,108463,246354,'Supply-side trouble'),
 (14,'2019-06-04 08:49','2019-07-24 17:10',1208,78536,261632,'Planned shut-in'),
 (15,'2019-08-23 05:19','2019-09-10 11:48',438,137885,274342,'Supply-side trouble'),
 (16,'2019-10-09 18:20','2019-10-30 11:08',497,80592,288874,'Supply-side trouble'),
 (17,'2019-11-22 11:30','',None,216498,300012,'Planned final shut-in; measurement continuing')]
 rows=[]
 for i,start,end,h,q,c,cause in spec:
  p=10 if i<=14 else 11
  for k,v,unit,quantity in [('hours',h,'hours','Reported measurement duration'),('rate',q,'tCO2/year','Average rate immediately before shut-in, annualised'),('cumulative',c,'tCO2','Moebetsu cumulative injection at test')]:
   if v is not None:val(f'TOMA_FOA{i}_{k}','D7-22',p,v,unit,f'{v:,}',quantity,f'FOA{i}','Reported historical quantity','A pre-shut-in rate is not a maximum safe annual injection limit. Measurement duration and full elapsed window are separate fields.')
  elapsed=(datetime.fromisoformat(end)-datetime.fromisoformat(start)).total_seconds()/3600 if end else ''
  rows.append(dict(test=f'FOA{i}',start_local=start,end_local=end,reported_measurement_hours=h if h is not None else '',elapsed_window_hours=elapsed,average_pre_shutin_t_per_year=q,cumulative_moebetsu_t=c,cause=cause,document_id='D7-22',physical_page=p,scope='Selected test/measurement windows, not an exhaustive downtime calendar or failure probability. Final ongoing window is open, not zero duration.'))
 write('data/tomakomai_shutin_tests.csv',rows)
 # Published fall-off interpretation: effective properties inferred from tests, not directly measured reservoir constants.
 rows=[]
 spec=[(6,129623,88474,65793,3000,158),(7,146691,100124,69070,3078,162),(8,124766,85159,109250,3900,205),(9,128502,87709,188136,4950,261),(10,277785,189602,207209,6000,316),(11,122509,83618,217425,3600,190),(12,319403,218008,233438,6650,350),(14,115063,78536,261632,4940,260),(17,317189,216498,300012,6080,320)]
 for i,qv,qm,c,kh,k in spec:
  for name,n,unit in [('standard_volume_rate',qv,'m3/day as reported'),('mass_rate',qm,'tCO2/year'),('cumulative',c,'tCO2'),('kh',kh,'mD*m'),('k',k,'mD')]:val(f'TOMA_FOT{i}_{name}','D7-18',10,n,unit,f'{n:,}',name,f'FOT{i}','Published fall-off analysis input/output','Table5.1-3; FOT11 mass rate83,618 differs from83,620 in the overview and is preserved separately.')
  rows.append(dict(test=f'FOT{i}',standard_volume_rate_m3_day=qv,mass_rate_t_year=qm,cumulative_t=c,effective_kh_md_m=kh,effective_k_md=k,document_id='D7-18',physical_page=10,scope='Source-inferred effective properties; variations are not independent permeability measurements or an annual capacity series.'))
 write('data/tomakomai_falloff_reference.csv',rows)
 for key,value,unit,token,name in [('h',19,'m','19','Effective thickness'),('B',.0028,'reservoir m3/reference m3','0.0028','CO2 volume factor'),('mu',.0521,'cP','0.0521','CO2 viscosity'),('phi',.28,'fraction','0.28','Porosity'),('sco2',.8,'fraction','0.8','Assumed CO2 saturation'),('ct',7.28e-5,'1/kPa','7.28','Total compressibility'),('cw',4.29e-7,'1/kPa','4.29','Water compressibility'),('cco2',8.52e-5,'1/kPa','8.52','CO2 compressibility'),('cr',4.54e-6,'1/kPa','4.54','Rock compressibility'),('refP',9.82,'MPaG','9.82','Property-reference pressure'),('refT',37.8,'degreeC','37.8','Property-reference temperature')]:val('TOMA_FOT_'+key,'D7-18',10,value,unit,token,name,kind='Published fall-off model input')
 for key,p,v,u,t,name in [('sensor_depth',12,921,'mTVDSS','921','PT sensor depth'),('completion_depth',12,973,'mTVDSS','973','Completion-top depth'),('density_low',12,470,'kg/m3','470','Reported CO2 density low'),('density_high',12,670,'kg/m3','670','Reported CO2 density high'),('depth_gap',12,52,'m','52','Sensor/completion depth gap'),('approx_pressure_error',12,100,'kPa','100','Source approximate pressure-correction difference'),('history_match_difference',9,25,'kPa','25','Source model/observation difference less than this value')]:val('TOMA_'+key,'D7-22',p,v,u,t,name,kind='Reported monitoring/model-reference quantity',note='Depth/pressure basis is specific. The25kPa statement describes the source model, not validation of our model.')
 # Independent published prospective scenario, kept outside the operating model.
 for key,p,v,u,t,name in [('case2_rate',52,22,'10^4 tCO2/year','22','Counterfactual restart operating rate'),('case2_pressure_cap',52,12.93,'MPaG at IW2 completion top','12.93','Case2 pressure constraint'),('case2_monitoring',52,1000,'years','1,000','Post-injection screening horizon'),('case2_caprock',52,20,'m','20','Caprock thickness screening boundary'),('case2_depth',52,750,'m','750','Dissolved-plume depth screening boundary'),('case2_realisations',52,30,'count','30','Case2 geological realisations'),('case2_mean',53,470,'10^4 tCO2','470','Case2 mean simulated capacity'),('case2_sd',53,252,'10^4 tCO2','252','Case2 reported standard deviation'),('case2_P90',53,147,'10^4 tCO2','147','Case2 source-labelled P90 capacity'),('case2_P50',53,470,'10^4 tCO2','470','Case2 source-labelled P50 capacity'),('case2_P10',53,793,'10^4 tCO2','793','Case2 source-labelled P10 capacity')]:val('TOMA_'+key,'D7-18',p,v,u,t,name,kind='Published reservoir simulation input/output',note='Hypothetical2021 restart with June shut-in and pressure/plume constraints. Not an observed restart, contracted service, independent annual-rate array or a probability distribution adopted here.')


 # Alternative completions retain their own pressure/depth basis and capacity outputs.
 for tag,depth,fracture,cap in [('3-1',1030,14.63,13.17),('3-2',1145,16.28,14.65)]:
  for key,value,unit,token,name in [('depth',depth,'mTVDSS',f'{depth:,}','Completion-top depth'),('fracture',fracture,'MPaG',str(fracture),'Reference fracture pressure'),('cap',cap,'MPaG',str(cap),'Tabulated injection-pressure cap')]:val(f'TOMA_case{tag}_{key}','D7-18',74,value,unit,token,name,tag,'Published alternative-completion scenario','Table5.4-5; keep fracture and operating cap separate. Figure labels for Case3-2 elsewhere show16.28MPaG and require reconciliation; these values are not used to create annual rates.')
 alternatives=[('P90',200,300,500),('P90',100,1100,700),('P50',500,500,500),('P50',400,600,600),('P50',300,800,900),('P50',200,1200,800),('P50',100,1100,700),('P10',900,900,1000),('P10',800,900,1000),('P10',700,1200,1200),('P10',600,1100,1200),('P10',500,1100,1100),('P10',400,1000,1000),('P10',300,1000,900),('P10',200,900,800),('P10',100,900,700)]
 altrows=[]
 for percentile,switch,a,b in alternatives:
  for tag,value in [('switch',switch),('case3-1',a),('case3-2',b)]:val(f'TOMA_{percentile}_{switch}_{tag}','D7-18',74,value,'10^4 tCO2',f'{value:,}',tag,percentile,'Published alternative-completion simulation result','Table5.4-6; source-labelled geological scenarios, not an adopted probability distribution or annual service.')
  altrows.append(dict(source_label=percentile,switch_at_10kt=switch,case3_1_capacity_10kt=a,case3_2_capacity_10kt=b,document_id='D7-18',physical_page=74,scope='Published completion-policy scenarios; capacity totals are not annual rates or contracted service.'))
 write('data/tomakomai_completion_scenarios.csv',altrows)


def other_parameters():
 for key,p,v,u,t,name in [('lifetime_stored',7,127.8,'MtCO2','127.8','Reported lifetime stored mass'),('lifetime_ghg',7,3.32,'MtCO2e','3.32','Reported lifetime chain GHG'),('reported_intensity',7,.026,'tCO2e/t stored','0.026','Reported rounded footprint'),('shipping_share',7,91,'percent','91%','Shipping share of reported total GHG'),('fugitive_source_co2',11,96725,'tCO2','96,725','Reported captured-stream fugitive CO2'),('body_ship_fuel',11,2.15,'MtCO2e','2.15','Discussion ship-fuel GHG'),('phase1',3,1.5,'MtCO2/year','1.5','March2023 Phase1 design'),('phase2_total',3,3.5,'MtCO2/year','3.5','March2023 stated Phase2 total'),('injection_duration',3,25,'years','25','Reported expected injection activity'),('vessel_small',3,7500,'m3','7,500','Phase1/2 reference ship volume'),('vessel_large',3,12000,'m3','12,000','Phase2 reference ship volume'),('terminal_tanks',3,12,'count','12','Phase1 tank count'),('terminal_volume',3,7500,'m3','7,500','Phase1 total receiving tank volume'),('pipeline_diameter',3,12,'inch','12-','Pipeline diameter'),('pipeline_distance',3,100,'km','100','Offshore pipeline length')]:val('NL_'+key,'D7-15',p,v,u,t,name,kind='Prospective lifecycle study/design result',note='March2023 report; starts with customer-liquefied CO2 and excludes customer capture/liquefaction. LNG/MDO European shipping; not a Japan-route factor. Phase/horizon and GWP statements require reconciliation.')
 val('NL_2025_first_stored','D7-16',5,40000,'tCO2 approximately','40k','Rounded reported first-year stored mass',kind='2025 annual-report operational disclosure',note='Not annualised steady-state capacity or audited full-project lifetime performance.')
 for key,v,u,t,name in [('loa',71.99,'m','71.99','Length overall'),('breadth',12.5,'m','12.50','Breadth'),('depth',5.5,'m','5.50','Depth'),('draft',4.6,'m','4.60','Draft'),('gross_tonnage',996,'Japanese gross tonnage','996','Gross tonnage'),('crew',10,'persons','10','Complement'),('tank',1450,'m3 approximately','1,450','Total cargo tank volume'),('speed',12,'knots','12.0','Reference speed'),('engine',1471,'kW maximum','1,471','Maximum main-engine output')]:val('EXCOOL_'+key,'D7-10',1,v,u,t,name,kind='Published vessel specification',note='Domestic greater-coasting demonstration vessel; no fuel/duty curve or international operating availability inferred.')
 val('IMO_2026_ethanol_wtt','D7-08',3,20.8,'gCO2eq/MJ','20.8','Intermediate-crop corn/biomassCHP ethanol WtT default',note='MEPC.1/Circ.926 applies to specified ethanol pathway, not fossil MDO/MGO. Not substituted for the current MDO factor.')
 val('IMO_2026_ethanol_lcv','D7-08',3,.0268,'MJ/g','0.0268','Same ethanol pathway LCV')
 val('TOMA_takinoue_table_total','D7-20',3,98.2,'tCO2','98.2','Takinoue printed cumulative injection',kind='Historical cumulative table value',note='Table3-2 precision retained. Do not force agreement with a difference calculated from independently rounded Moebetsu/combined disclosures.')
 val('TOMA_latest_total_injected','D7-25',1,300110.3,'tCO2','300,110.3','Reported total historical injection, both formations',kind='Historical cumulative disclosure',note='Injection terminated22November2019; monitoring newsletters do not establish resumed injection.')


def northern_lights_components():
 # Visually checked labelled numeric rows; blank table cells are retained separately.
 spec={
 'transport':{
 'construction':[('Mobile vehicles',2682),('Grid electricity',22054),('Heat',17259),('Equipment/material',152946),('Other process emissions',9720),('Ship delivery',19781),('Wastewater treatment',.12),('Waste disposal',16088),('Chemicals/utilities',3409)],
 'operation':[('Grid electricity',5492),('Ship fuel consumption',2638032),('Other process emissions',124638)],
 'decommissioning':[('Waste disposal',16129)]},
 'storage':{
 'construction':[('Site preparation',4028),('Buildings/road',2416),('Equipment/material',64469),('Chemicals/utilities',978),('Use of vessels',75741)],
 'operation_injection':[('Chemicals/utilities',119),('Grid electricity',48329),('Other process emissions',14848),('Use of vessels',33065)],
 'operation_post_injection':[('Use of vessels',4406)],
 'decommissioning':[('Waste disposal',2162),('Use of vessels',32507)]}}
 rows=[]
 for area,stages in spec.items():
  p=12 if area=='transport' else 13
  for stage,items in stages.items():
   for item,value in items:
    token=f'{value:,}'.replace(',',' ') if isinstance(value,int) else str(value);key=f'NL_{area}_{stage}_{len(rows)+1:02d}'
    val(key,'D7-15',p,value,'tCO2e over reference lifetime',token,item,area+' / '+stage,'Published prospective lifecycle result','Appendix numeric cell; sum of printed entries is not forced to headline total. Blank rows are not assumed zero.')
    rows.append(dict(value_id=key,document_id='D7-15',physical_page=p,area=area,stage=stage,activity=item,reported_tco2e=value,source_token=token,cell_status='PRINTED_NUMERIC',scope='LNG/MDO Northern European project reference, customer capture/liquefaction excluded; no per-well/distance scaling inferred.'))
 # Explicitly retain all blank activity cells shown in the appendices rather than silently zero them.
 blanks={'transport':{'operation':['Heat','Equipment/material','Waste disposal'],'decommissioning':['Fuel in mobile vehicles','Grid electricity','Heat','Wastewater treatment']},'storage':{'construction':['Mobile vehicles','Other process emissions','Grid electricity','Heat','Stationary combustion','Wastewater treatment','Solid waste disposal'],'operation_injection':['Stationary combustion','Heat','Fuel in mobile vehicles','Equipment/material','Wastewater treatment','Solid waste disposal','Labour','Personal transport'],'operation_post_injection':['Grid electricity','Other process emissions'],'decommissioning':['Clearing onshore','Fuel in mobile vehicles','Wastewater treatment','Equipment/material','Grid electricity','Heat'],'post_closure':['Use of vessels']}}
 for area,stages in blanks.items():
  for stage,items in stages.items():
   for item in items:rows.append(dict(value_id='',document_id='D7-15',physical_page=12 if area=='transport' else 13,area=area,stage=stage,activity=item,reported_tco2e='',source_token='',cell_status='BLANK_NOT_IMPUTED',scope='Blank original cell, not an independently verified physical zero.'))
 write('data/northern_lights_components.csv',rows);return rows

def calculations(history,components):
 p={x['value_id']:float(x['value']) for x in V};out=[]
 def calc(key,value,unit,inputs,formula,scope):out.append(dict(result_id=key,value=value,unit=unit,input_ids=inputs,equation=formula,scope=scope))
 # Standard gravity is an explicit reference constant, not a fitted environmental parameter.
 gravity=9.80665;dz=p['TOMA_depth_gap'];drho=p['TOMA_density_high']-p['TOMA_density_low'];error=gravity*dz*drho/1000
 calc('TOMA_hydrostatic_correction_span',error,'kPa','TOMA_depth_gap;TOMA_density_low;TOMA_density_high','(rho_high-rho_low)*g0*dz/1000; g0=9.80665m/s2 standard gravity','Hydrostatic reference calculation using reported density range; not a calibrated pressure history.')
 calc('TOMA_correction_over_source_match_threshold',error/p['TOMA_history_match_difference'],'ratio','TOMA_depth_gap;TOMA_density_low;TOMA_density_high;TOMA_history_match_difference','hydrostatic_span/25kPa','Illustrates sensor/datum sensitivity relative to the source history-match statement; no validation of our reservoir model.')
 rs=[x for x in V if x['quantity']=='kh'];calc('TOMA_effective_kh_span_ratio',max(float(x['value']) for x in rs)/min(float(x['value']) for x in rs),'ratio',';'.join(x['value_id'] for x in rs),'max(published effective kh)/min(published effective kh)','Different fall-off interpretations/operating states; not a physical permeability change or probability distribution.')
 numeric=[x for x in components if x['cell_status']=='PRINTED_NUMERIC'];tot=sum(float(x['reported_tco2e']) for x in numeric);reported=p['NL_lifetime_ghg']*1e6;stored=p['NL_lifetime_stored']*1e6
 calc('NL_sum_printed_appendix',tot,'tCO2e',';'.join(x['value_id'] for x in numeric),'sum(printed numeric Appendix1/2 entries)','Blank cells remain unquantified; no forced reconciliation to3.32Mt.')
 calc('NL_appendix_minus_headline',tot-reported,'tCO2e','NL_lifetime_ghg;NL_sum_printed_appendix','appendix_sum-headline','Internal source difference; no guessed correction.')
 calc('NL_headline_intensity',reported/stored*1000,'kgCO2e/t stored','NL_lifetime_ghg;NL_lifetime_stored','reported total GHG/stored mass*1000','After customer liquefaction; not full CCS emissions or a transferable universal factor.')
 calc('NL_source_fugitive_intensity',p['NL_fugitive_source_co2']/stored*1000,'kgCO2/t stored','NL_fugitive_source_co2;NL_lifetime_stored','reported captured-source fugitives/stored mass*1000','Captured-source carbon loss requires mass reconciliation; do not charge it twice against retained mass.')
 selected=[x for x in numeric if x['area']=='storage' and x['activity']!='Other process emissions'];subtotal=sum(float(x['reported_tco2e']) for x in selected);intensity=subtotal/stored*1000
 calc('NL_selected_storage_reference_intensity',intensity,'kgCO2e/t reference stored','NL_lifetime_stored;'+';'.join(x['value_id'] for x in selected),'sum(selected printed storage rows excluding Other process emissions)/127.8Mt*1000','Optional average-burden transfer only. Excludes unresolved other-process/fugitive category; blanks remain unknown. Not marginal asset emissions, actual Japan inventory, or harmonised full LCA.')
 write('outputs/case_evidence_calculations.csv',out)
 comparison=[]
 for x in read('outputs/reference_inventory_comparisons.csv'):
  if x['model_case']!='99pct_design_control':continue
  extra=float(x['additional_injected_t'])*intensity/1000;remaining=float(x['remaining_uninventoried_allowance_t'])-extra
  comparison.append(dict(utility_scenario=x['utility_scenario'],higher_distance_km=x['higher_distance_km'],additional_injected_t=x['additional_injected_t'],previous_partial_allowance_t=x['remaining_uninventoried_allowance_t'],selected_storage_proxy_kgco2e_per_t=intensity,additional_selected_storage_proxy_tco2e=extra,remaining_allowance_after_proxy_t=remaining,complete_net_avoided_ghg_t='',scope='Optional Northern Lights2023 selected storage-row average transfer. Fixed lifecycle totals normalised by reference stored mass; not a design-specific marginal asset response. Original inventory scope/year/GWP differences and other missing terms remain.'))
 write('outputs/northern_lights_storage_proxy_comparisons.csv',comparison)
 return out,comparison

def plot(history,comparisons):
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'font.size':10,'figure.dpi':160,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
 fig,ax=plt.subplots(figsize=(9,4));ys=[x['both_monthly_t'] for x in history];ax.bar(range(len(ys)),[v/1000 for v in ys],color='#247BA0');ax.set_xticks(range(0,len(ys),6),[history[i]['month'] for i in range(0,len(ys),6)]);ax.set_ylabel('Reported monthly injection (kt CO2)');ax.set_xlabel('Historical months; printed table values retain original precision');ax2=ax.twinx();ax2.plot(range(len(ys)),[float(x['both_cumulative_t'])/1000 for x in history],color='#F2994A',lw=2);ax2.set_ylabel('Reported cumulative injection (kt CO2)');ax.set_title('Tomakomai observed injection table — not maximum capacity');fig.tight_layout()
 for ext in ['png','pdf']:fig.savefig(ROOT/f'outputs/figures/tomakomai_reported_history.{ext}',bbox_inches='tight')
 plt.close(fig)


def main():
 for x in M.values():
  if x.get('path'):assert hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'],x['batch_id']
 counts=native_tables();history=monthly_history();shutin_records();other_parameters();components=northern_lights_components();write('data/case_numeric_values.csv',V);calcs,comp=calculations(history,components);plot(history,comp)
 catalog=[]
 for sid,x in M.items():catalog.append(dict(document_id=sid,original_filename=x['original_filename'],path=x.get('path',''),sha256=x.get('sha256',''),pages=x.get('pages',''),transfer_status='AVAILABLE' if x.get('path') else x['error'],review_stage='Targeted source/boundary/table review' if sid in ['D7-01','D7-02','D7-03','D7-04','D7-06','D7-07','D7-08','D7-09','D7-10','D7-13','D7-15','D7-16','D7-18','D7-19','D7-20','D7-21','D7-22','D7-23','D7-24','D7-25'] else 'Archived/indexed; no exhaustive scientific review',instruction_status='Source data only'))
 write('data/dataset7_catalogue.csv',catalog)
 summary=dict(uploaded=26,available=sum(bool(x.get('path')) for x in M.values()),unavailable=[sid for sid,x in M.items() if not x.get('path')],indexed_pdf_files=sum('pages'in x for x in M.values()),indexed_pdf_pages=sum(x.get('pages',0) for x in M.values()),located_numeric_records=len(V),monthly_history_rows=len(history),shutin_tests=17,falloff_reference_tests=9,northern_lights_numeric_components=sum(x['cell_status']=='PRINTED_NUMERIC' for x in components),northern_lights_blank_components=sum(x['cell_status']=='BLANK_NOT_IMPUTED' for x in components),new_derived_checks=len(calcs),optional_storage_proxy_comparisons=len(comp),entity_mismatch_unresolved=True,independent_maximum_annual_injection_array=False,complete_lca=False,**counts)
 (ROOT/'outputs/case_evidence_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
