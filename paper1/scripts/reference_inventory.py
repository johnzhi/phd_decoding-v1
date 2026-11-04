#!/usr/bin/env python3
"""Add explicitly scoped NETL utility and IMO default fuel-inventory scenarios.

No macros are run; six reference cases use retained workbook cached parameters.
Heat+auxiliary and electrical-makeup routes are mutually exclusive. Regulatory,
physical-disclosure and market-disclosure factors remain distinct scenarios.
"""
from pathlib import Path
import csv,json,math,os
os.environ.setdefault("MPLCONFIGDIR","/tmp/paper1-matplotlib")
os.environ.setdefault("XDG_CACHE_HOME","/tmp/paper1-cache")
import openpyxl
ROOT=Path(__file__).resolve().parents[1]
def read(name):return list(csv.DictReader((ROOT/name).open(encoding='utf-8')))
def write(name,rows):
 with (ROOT/name).open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def build_inputs():
 M={x['batch_id']:x for x in json.loads((ROOT/'data/dataset5_manifest.json').read_text())};inputs=[];cases=[]
 def cell(key,sid,sheet,ref,unit,note):
  w=books.setdefault(sid,openpyxl.load_workbook(ROOT/M[sid]['path'],read_only=False,data_only=True,keep_links=False)) if sid not in books else books[sid]
  value=w[sheet][ref].value;assert isinstance(value,(int,float)),(sid,ref,value)
  inputs.append(dict(value_id=key,document_id=sid,value=value,unit=unit,locator=f'{sheet}!{ref}',source_token=str(value),interpretation=note));return value
 def pdf(key,sid,page,value,unit,token,note):
  ps=json.loads((ROOT/M[sid]['page_text_path']).read_text());assert token in ps[page-1],(key,token)
  inputs.append(dict(value_id=key,document_id=sid,value=value,unit=unit,locator=f'physical PDF page {page}',source_token=token,interpretation=note));return value
 books={}
 for sid,host,rate_row,flow_row,derate_row,aux_row in [('D5-48','NGCC',34,35,49,50),('D5-50','PC',43,44,58,59)]:
  for col in ['B','C','D']:
   key=f'{host}_{col}';rate=cell(key+'_rate',sid,'Cost Parameters',f'{col}{rate_row}','fraction','CANSOLV capture design rate; not an additional multiplier on already captured source mass.')
   flow_lb=cell(key+'_flow',sid,'Cost Parameters',f'{col}{flow_row}','lbCO2/hour as reported','Published reference CO2 flow; caches read without recalculating macros.')
   derate=cell(key+'_derate',sid,'Cost Parameters',f'{col}{derate_row}','MW','Steam-turbine electric opportunity loss, not thermal GJ demand.')
   aux=cell(key+'_aux',sid,'Cost Parameters',f'{col}{aux_row}','MW','Total additional electrical auxiliary load, including capture/compression; do not add a separate duplicate compression load.')
   tph=flow_lb*.45359237/1000
   cases.append(dict(case_id=f'{host}_CANSOLV_{round(rate*100)}',route='electric_makeup',capture_fraction=rate,heat_gj_per_t='',electricity_kwh_per_t=(derate+aux)*1000/tph,auxiliary_kwh_per_t=aux*1000/tph,steam_opportunity_kwh_per_t=derate*1000/tph,source_id=sid,scope='Reference power-output replacement accounting; electricity replaces derate+auxiliary losses. Never add thermal heat emissions to this route. Uniform proxy, not14 calibrated industrial processes.'))
 # Physically paired steam/condensate streams in the same report case, not a latent-heat assumption.
 for rate,p1,p2,flow,steam,cond,recl,dryer,cap_kw,comp_kw,bop_kw in [(90,43,44,474979,499356,457357,5585,250,14700,38030,40250),(95,46,47,501431,527172,482834,5586,264,15500,40150,40350)]:
  base=f'PC_REPORT_{rate}';sid='D5-49'
  for suffix,val,unit,p,token in [('product',flow,'kg/hour',p2,f'{flow:,}'),('reboiler_in',steam,'kg/hour',p1,f'{steam:,}'),('reboiler_return',cond,'kg/hour',p1,f'{cond:,}'),('reclaimer',recl,'kg/hour',p1,f'{recl:,}'),('dryer',dryer,'kg/hour',p2,str(dryer)),('h_reboiler_in',2994.07,'kJ/kg',p1,'2,994.07'),('h_reboiler_return',439.34,'kJ/kg',p1,'439.34'),('h_reclaimer_in',3098.44,'kJ/kg',p1,'3,098.44'),('h_reclaimer_return',913.81,'kJ/kg',p1,'913.81'),('h_dryer_in',3408.95,'kJ/kg',p2,'3,408.95'),('h_dryer_return',863.65,'kJ/kg',p2,'863.65')]:
   pdf(base+'_'+suffix,sid,p,val,unit,token,'Exhibits3-2/3-3/3-4: reboiler24/25, reclaimer27/28, dryer33/32, product34/35. Net reported utility enthalpy import, not a verbatim reboiler-duty measurement.')
  page=48 if rate==90 else 49
  for name,v in [('capture_aux',cap_kw),('compression',comp_kw),('bop_new',bop_kw),('bop_base',37520)]:pdf(base+'_'+name,sid,page,v,'kW',f'{v:,}','Paired report additional electrical load; turbine derate is excluded from this heat+aux route.')
  q=(steam*2994.07-cond*439.34+recl*(3098.44-913.81)+dryer*(3408.95-863.65))/(flow*1000)
  e=(cap_kw+comp_kw+bop_kw-37520)/(flow/1000)
  cases.append(dict(case_id=f'PC_REPORT_CANSOLV_{rate}',route='heat_plus_aux',capture_fraction=rate/100,heat_gj_per_t=q,electricity_kwh_per_t=e,auxiliary_kwh_per_t=e,steam_opportunity_kwh_per_t='',source_id=sid,scope='Derived net reported steam-utility enthalpy plus incremental auxiliaries. External-utility accounting sensitivity, not isolated reboiler duty or verified district-steam compatibility; no turbine-derate addition.'))
 for key,p,value,unit,token,note in [('imo_wtt',51,17.7,'gCO2e/MJ','17.7','Appendix2 row5 fossil MDO/MGO ULSFO default upstream intensity.'),('imo_lcv',51,.0427,'MJ/g fuel','0.0427','Same pathway LCV.'),('imo_co2',51,3.206,'gCO2/g fuel','3.206','Same MDO/MGO pathway, all ICEs.'),('imo_ch4',51,.00005,'gCH4/g fuel','0.00005','Fuel-default methane coefficient, not LNG engine slip.'),('imo_n2o',51,.00018,'gN2O/g fuel','0.00018','Fuel-default nitrous oxide coefficient.'),('gwp_ch4',5,28,'gCO2e/gCH4','CH4 28','Guideline GWP100.'),('gwp_n2o',5,265,'gCO2e/gN2O','N2O 265','Guideline GWP100.')]:pdf(key,'D5-54',p,value,unit,token,note)
 # Exact named sheet/cells preserve accounting scope and year.
 for year,row in [(2019,2),(2020,3),(2021,4),(2022,5),(2023,6),(2024,7),(2025,8)]:
  for sheet,tag in [('Klimadeklarasjon','physical_climate'),('Varedeklarasjon','market_disclosure')]:cell(f'NVE_{tag}_{year}','D5-02',sheet,f'C{row}','gCO2e/kWh' if tag=='physical_climate' else 'gCO2/kWh','As-reported NVE disclosure series; physical climate and market declaration are not interchangeable.')
 el_sheet=books['D5-38'].sheetnames[0] if 'D5-38'in books else openpyxl.load_workbook(ROOT/M['D5-38']['path'],read_only=True).sheetnames[0]
 heat_sheet=openpyxl.load_workbook(ROOT/M['D5-16']['path'],read_only=True).sheetnames[0]
 cell('JP_R8_electric_fallback','D5-38',el_sheet,'C1499','tCO2/kWh','Official fallback reporting coefficient; R6 supply data with header-specific menus, for R7 emissions/R8 reporting. Not an actual supplier or forecast.')
 cell('JP_R8_heat_fallback','D5-16',heat_sheet,'D47','tCO2/GJ','Official heat fallback reporting coefficient; heat quality/steam compatibility and full LCA remain unestablished.')
 write('data/reference_inventory_inputs.csv',inputs);write('data/netl_capture_reference_cases.csv',cases)
 return {x['value_id']:float(x['value']) for x in inputs},cases

def run():
 p,cases=build_inputs();wtw=p['imo_co2']+p['imo_ch4']*p['gwp_ch4']+p['imo_n2o']*p['gwp_n2o']+p['imo_wtt']*p['imo_lcv']
 # Units: g/g equals kg/kg; (gCO2e/MJ)*(MJ/g fuel) also equals g/g.
 gas=dict(fuel_pathway='MDO/MGO(ULSFO)_f_SR_gm',ttw_co2_kg_per_kg=p['imo_co2'],ttw_ch4_n2o_kgco2e_per_kg=p['imo_ch4']*p['gwp_ch4']+p['imo_n2o']*p['gwp_n2o'],wtt_kgco2e_per_kg=p['imo_wtt']*p['imo_lcv'],wtw_kgco2e_per_kg=wtw,gwp_horizon=100,scope='2024 guideline default fuel pathway, not certified actual bunker fuel. Additional idle/process duties remain separate.')
 (ROOT/'outputs/imo_mdo_default_inventory.json').write_text(json.dumps(gas,indent=2))
 scenarios=[]
 for c in cases:
  for grid,ef,mode in [('NO_2025_climate',p['NVE_physical_climate_2025']/1000,'physical-disclosure reference'),('JP_R8_fallback',p['JP_R8_electric_fallback']*1000,'Japanese reporting-factor sensitivity'),('NO_2025_market',p['NVE_market_disclosure_2025']/1000,'MARKET_ACCOUNTING_ONLY')]:
   if c['route']=='heat_plus_aux' and grid!='JP_R8_fallback':continue
   heat=float(c['heat_gj_per_t']) if c['heat_gj_per_t']!='' else 0
   intensity=float(c['electricity_kwh_per_t'])*ef+heat*p['JP_R8_heat_fallback']*1000
   scenarios.append(dict(utility_scenario=c['case_id']+'__'+grid,capture_case=c['case_id'],grid_scenario=grid,accounting_mode=mode,capture_utility_kg_per_t_captured=intensity,route=c['route'],source_note=c['scope'],full_lifecycle=False))
 write('data/capture_utility_scenarios.csv',scenarios)
 original=read('outputs/operational_comparisons.csv');out=[]
 def evaluate(label,x,scenario):
  Cf,Cd=float(x['higher_captured_t']),float(x['lower_captured_t']);Rf,Rd=float(x['higher_injected_t']),float(x['lower_injected_t'])
  deltafuel=(float(x['higher_ship_combustion_co2_t'])-float(x['lower_ship_combustion_co2_t']))/p['imo_co2'] # tonnes of fuel
  marine=deltafuel*wtw;utility=(Cf-Cd)*scenario['capture_utility_kg_per_t_captured']/1000
  return dict(model_case=label,size_m3=x['size_m3'],higher_distance_km=x['higher_distance_km'],variant=x['variant'],static_policy=x['static_policy'],calendar=x['availability_calendar'],rounding=x['rounding_case'],utility_scenario=scenario['utility_scenario'],accounting_mode=scenario['accounting_mode'],additional_injected_t=Rf-Rd,additional_captured_t=Cf-Cd,additional_marine_default_wtw_tco2e=marine,additional_capture_utility_inventory_t=utility,remaining_uninventoried_allowance_t=(Rf-Rd)-marine-utility,complete_net_avoided_ghg_t='',scope='Uniform NETL reference transfer, IMO default fuel and historical utility disclosure/reporting scenario. Other processes/assets/retention remain missing; no destination preference or full LCA.')
 for x in original:
  for s in scenarios:out.append(evaluate('reference_fleet_grid',x,s))
 # Recompute selected fleet capture quantities; preserve injected results instead of substituting injected tonnes for captured tonnes.
 import operational_model as model
 selected=read('outputs/operational_design_adequacy.csv');actual=[]
 for x in selected:
  _,_,I=model.service(x['storage_proxy']);rr,meta=model.Shuttle(I,int(x['one_way_distance_km']),fleet_margin=int(x['extra_vessels'])).run()
  actual.append(dict(proxy=x['storage_proxy'],distance=int(x['one_way_distance_km']),captured=sum(a['captured_t'] for a in rr),injected=sum(a['injected_t'] for a in rr),shipco2=sum(a['combustion_co2_t'] for a in rr)))
  assert abs(actual[-1]['injected']-float(x['selected_injected_t']))<.001
 low=actual[0]
 for high in actual[1:]:
  x=dict(size_m3=40000,higher_distance_km=high['distance'],variant='B3',static_policy='design_control',availability_calendar='staggered',rounding_case='printed',higher_captured_t=high['captured'],lower_captured_t=low['captured'],higher_injected_t=high['injected'],lower_injected_t=low['injected'],higher_ship_combustion_co2_t=high['shipco2'],lower_ship_combustion_co2_t=low['shipco2'])
  for s in scenarios:out.append(evaluate('99pct_design_control',x,s))
 write('outputs/reference_inventory_comparisons.csv',out)
 (ROOT/'outputs/reference_inventory_summary.json').write_text(json.dumps(dict(capture_cases=len(cases),utility_scenarios=len(scenarios),comparison_rows=len(out),imo_default=gas,complete_lca_generated=False,site_specific_calibration=False),indent=2));print(json.dumps(dict(capture_cases=cases,marine=gas,utility_scenarios=len(scenarios),comparison_rows=len(out)),indent=2))
def plot_results():
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'font.size':10,'figure.dpi':160,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
 rows=read('outputs/reference_inventory_comparisons.csv');names=[('NGCC_CANSOLV_90__NO_2025_climate','NGCC replacement\nNO climate factor'),('NGCC_CANSOLV_90__JP_R8_fallback','NGCC replacement\nJP fallback factor'),('PC_REPORT_CANSOLV_90__JP_R8_fallback','PC heat + auxiliaries\nJP fallback factors')]
 fig,axs=plt.subplots(1,2,figsize=(10,4.2))
 for ax,d in zip(axs,['5000','10000']):
  vals=[float(next(x['remaining_uninventoried_allowance_t'] for x in rows if x['model_case']=='99pct_design_control' and x['higher_distance_km']==d and x['utility_scenario']==name))/1e6 for name,label in names]
  ax.bar(range(3),vals,color=['#247BA0','#F2994A','#4D9078']);ax.axhline(0,color='grey',lw=1);ax.set_xticks(range(3),[label for name,label in names],fontsize=8);ax.set_title(d+' km higher-service proxy')
  for i,v in enumerate(vals):ax.annotate(f'{v:+.3f}',(i,v),ha='center',va='bottom' if v>=0 else 'top',fontsize=9)
  ax.margins(y=.2)
 axs[0].set_ylabel('Remaining uninventoried allowance (Mt)\nConditional component inventory; not full LCA');fig.tight_layout()
 for ext in ['png','pdf']:fig.savefig(ROOT/f'outputs/figures/reference_inventory_allowance.{ext}',bbox_inches='tight')
 plt.close(fig)
if __name__=='__main__':run();plot_results()
