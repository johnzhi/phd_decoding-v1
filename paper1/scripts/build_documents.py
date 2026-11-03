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
 text=(ROOT/'manuscript/Paper_1_draft.template.md').read_text();ids=sorted(set(re.findall(r'B[1-4]-\d\d',text)),key=lambda s:tuple(map(int,s[1:].split('-'))))
 refs=[]
 for sid in ids:
  x=cat[sid];ident=x['doi'];link=('https://doi.org/'+ident) if ident.startswith('10.') else '../'+x['pdf_path']
  refs.append(f"- **[{sid}]** {x['author_year']+'. ' if x['author_year'] else ''}{x['title']}. [{ident}]({link}). [Retained PDF](../{x['pdf_path']}).")
 for key,val in {'THERMAL_TABLE':thermal,'BOG_TABLE':bog,'PROXY_TABLE':proxy,'REFERENCES':'\n\n'.join(refs)}.items():text=text.replace('{{'+key+'}}',val)
 if re.search(r'\{\{[A-Z_]+\}\}',text):raise ValueError('Unfilled manuscript token')
 out=ROOT/'manuscript/Paper_1_draft.md';out.write_text(text)
 subprocess.run(['pandoc',str(out),'--from=markdown','--standalone','--resource-path='+str(out.parent),'-o',str(out.with_suffix('.docx'))],check=True)
 # A digest copy lets the researcher review citations and coverage in an editable document.
 digest=ROOT/'docs/evidence_digest.md'
 subprocess.run(['pandoc',str(digest),'--from=markdown','--standalone','-o',str(ROOT/'docs/evidence_digest.docx')],check=True)
 print(f'Rendered manuscript and digest DOCX; {len(ids)} cited sources; {len(text.split())} manuscript words including tables/references.')
if __name__=='__main__':render()
