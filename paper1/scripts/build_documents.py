#!/usr/bin/env python3
"""Render manuscript tables and DOCX from the retained inputs/results."""
from pathlib import Path
import csv,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
def read(p):return list(csv.DictReader((ROOT/p).open(encoding='utf-8')))
def table(headers,rows):
 return '| '+' | '.join(headers)+' |\n|'+'|'.join('---' for _ in headers)+'|\n'+'\n'.join('| '+' | '.join(map(str,r))+' |' for r in rows)
def render():
 inp={x['value_id']:x for x in read('data/analysis_inputs.csv')};res=read('outputs/calculated_results.csv');cat={x['study_id']:x for x in read('data/source_catalogue.csv')}
 def value(k):return float(inp[k]['value'])
 def result(metric,case):return float(next(x['value'] for x in res if x['metric']==metric and x['case']==case))
 t=[]
 for s in 'ABCD':t.append([s,f"{value('thermal_'+s+'_isothermal'):,.0f}",f"{value('thermal_'+s+'_cooled'):,.0f}",f"{result('pressure_ceiling_drop',s):.0f}",f"{result('pressure_ceiling_drop_percent',s):.2f}"])
 thermal=table(['Seal','Isothermal ceiling (psi)','Cooled ceiling (psi)','Drop (psi)','Drop (%)'],t)
 t=[]
 for c in ['1-1','1-2','1-3','2-1','2-2','2-3']:
  t.append([c]+[f"{result('partial_process_emissions_intensity',f'{c}; N2={int(n)/100:g} mol%'):.3f}" for n in ['005','010','015']])
 bog=table(['Process case','N₂ 0.05 mol% (kg/t)','N₂ 0.10 mol% (kg/t)','N₂ 0.15 mol% (kg/t)'],t)
 t=[]
 for c in ['NL07','NL15','SM07','SM15','combined07','combined15']:
  names={'NL07':'Northern Lights, 0.7 MPa','NL15':'Northern Lights, 1.5 MPa','SM07':'Stella Maris, 0.7 MPa','SM15':'Stella Maris, 1.5 MPa','combined07':'Combined, 0.7 MPa','combined15':'Combined, 1.5 MPa'}
  t.append([names[c],f"{value('gwp_'+c):.1f}",f"{result('required_storage_uplift_for_score_equality',c):.2f}",f"{result('difference_in_stored_mass_minus_reported_GWP_score',c):+.3f}"])
 proxy=table(['High-storage burden scenario','Reported GWP (kgCO₂e/t stored)','Storage uplift for score equality (%)','Δ reported-burden score (MtCO₂e)'],t)
 sup=read('outputs/supplement_scenario_summary.csv');replay=__import__('json').loads((ROOT/'outputs/supplement_replay.json').read_text())
 parameter=table(['Quantity','Published-table aggregation','Locator'],[
  ['Sources',str(replay['source_count']),'Table S1'],
  ['Annual source-rate sum',f"{replay['nominal_annual_source_mtpa']:.3f} Mt/year",'Table S1'],
  ['Source CO2 over 30 calendar-year bins',f"{replay['nominal_source_30_bins_mt']:.2f} Mt",'Table S1; 2027–2056 horizon'],
  ['Candidate reservoirs',str(replay['reservoir_count']),'Table S2'],
  ['Summed candidate reservoir resource',f"{replay['sum_candidate_reservoir_capacity_mt']:.1f} Mt",'Table S2'],
  ['Numeric hub distances',str(replay['hub_distance_values']),'Table S3']])
 annual=table(['Scenario','Printed cells','Sum of printed allocations (Mt)','Main-paper total (Mt)','Printed minus main (Mt)'],[
  [x['scenario'],x['printed_numeric_cells'],f"{float(x['sum_printed_allocations_mt']):.1f}",f"{float(x['main_paper_cumulative_mt']):.2f}",f"{float(x['printed_minus_main_mt']):+.2f}"] for x in sup])
 op=read('outputs/operational_comparisons.csv');design=read('outputs/operational_design_adequacy.csv');ctrl=read('outputs/operational_controls.csv')
 operating=table(['Higher route (km)','Variant','Lower injected (Mt)','Higher injected (Mt)','Additional active ship CO₂ (Mt)','Uninventoried allowance (Mt)'],[
  [x['higher_distance_km'],x['variant'],f"{float(x['lower_injected_t'])/1e6:.3f}",f"{float(x['higher_injected_t'])/1e6:.3f}",f"{float(x['additional_ship_combustion_co2_t'])/1e6:.3f}",f"{float(x['differential_uninventoried_burden_allowance_tco2e'])/1e6:+.3f}"] for x in op if x['group']=='primary' and x['size_m3']=='40000' and x['static_policy']=='aggregate_mean' and x['higher_distance_km'] in ['5000','10000']])
 fleetdesign=table(['Service proxy','Route (km)','Reference fleet','Selected fleet','Initial/reference injection (%)','99% target met'],[
  [x['storage_proxy'],x['one_way_distance_km'],x['source_reference_fleet'],x['selected_fleet'],f"{float(x['initial_completion_fraction'])*100:.1f}",x['design_target_met']] for x in design])
 controls=table(['Control','Higher route (km)','Added vessels per route','Additional injection (Mt)','Additional active ship CO₂ (Mt)','Uninventoried allowance (Mt)'],[
  [x['control'].replace('B3 ',''),x['higher_distance_km'],x['fleet_margin_each_route'],f"{float(x['additional_injected_t'])/1e6:.3f}",f"{float(x['additional_ship_co2_t'])/1e6:.3f}",f"{float(x['uninventoried_allowance_t'])/1e6:+.3f}"] for x in ctrl])
 text=(ROOT/'manuscript/Paper_1_draft.template.md').read_text();ids=sorted(set(re.findall(r'B[1-4]-\d\d',text)),key=lambda s:tuple(map(int,s[1:].split('-'))))
 refs=[]
 for sid in ids:
  x=cat[sid]
  if x['duplicate_of']:continue  # One bibliography entry per publication; aliases remain in the catalogue.
  ident=x['doi'];link=('https://doi.org/'+ident) if ident.startswith('10.') else '../'+x['pdf_path']
  refs.append(f"- **[{sid}]** {x['author_year']+'. ' if x['author_year'] else ''}{x['title']}. [{ident}]({link}). [Retained PDF](../{x['pdf_path']}).")
 refs.append('- **[B4-06-S1]** Budiarto et al. (2025). Supplementary materials: Tables S1–S3 and Figures S1–S10. [Retained DOCX](../original/supplements/43979_2025_135_MOESM1_ESM.docx). Parent publication DOI 10.1007/s43979-025-00135-w.')
 for key,val in {'OPERATIONAL_COMPARISON_TABLE':operating,'OPERATIONAL_DESIGN_TABLE':fleetdesign,'OPERATIONAL_CONTROL_TABLE':controls,'SUPPLEMENT_PARAMETER_TABLE':parameter,'ANNUAL_REPLAY_TABLE':annual,'THERMAL_TABLE':thermal,'BOG_TABLE':bog,'PROXY_TABLE':proxy,'REFERENCES':'\n\n'.join(refs)}.items():text=text.replace('{{'+key+'}}',val)
 if re.search(r'\{\{[A-Z_]+\}\}',text):raise ValueError('Unfilled manuscript token')
 out=ROOT/'manuscript/Paper_1_draft.md';out.write_text(text)
 subprocess.run(['pandoc',str(out),'--from=markdown','--standalone','--resource-path='+str(out.parent),'-o',str(out.with_suffix('.docx'))],check=True)
 # A digest copy lets the researcher review citations and coverage in an editable document.
 digest=ROOT/'docs/evidence_digest.md'
 subprocess.run(['pandoc',str(digest),'--from=markdown','--standalone','-o',str(ROOT/'docs/evidence_digest.docx')],check=True)
 print(f'Rendered manuscript and digest DOCX; {len(refs)} unique bibliography entries; {len(text.split())} manuscript words including tables/references.')
if __name__=='__main__':render()
