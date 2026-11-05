#!/usr/bin/env python3
"""Validate manually written reading cards and publish follow-up review records.

No automatic page selection is counted as a completed scientific review. Only
manual cards with located methods/results notes and source-checked values update
coverage. Numerical extraction remains selective and context-qualified.
"""
from pathlib import Path
import csv,json,re
ROOT=Path(__file__).resolve().parents[1]
def read(p):
 with (ROOT/p).open(encoding='utf-8') as f:return list(csv.DictReader(f))
def write(p,rows):
 with (ROOT/p).open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
 cards=json.loads((ROOT/'data/deep_review_cards.json').read_text());selection=json.loads((ROOT/'evidence/deep_review/selection.json').read_text());expected={x['study_id'] for x in selection};assert {x['study_id'] for x in cards}==expected
 catalog=read('data/source_catalogue.csv');cat={x['study_id']:x for x in catalog};values=[]
 for c in cards:
  sid=c['study_id'];ps=json.loads((ROOT/cat[sid]['page_text_path']).read_text());assert c['methods'] and c['findings'] and c['transfer_limits'];assert any(p>1 for p in c['reviewed_physical_pages'])
  for x in c['numeric_records']:
   page=ps[x['physical_page']-1];token=x['source_token'];assert token in page,(sid,x['value_id'],x['physical_page'],token)
   loc=page.find(token);values.append(dict(study_id=sid,**x,source_excerpt=page[max(0,loc-100):loc+len(token)+140].replace('\n',' '),review_scope=c['review_scope']))
  cat[sid]['reading_stage']='Targeted methods/results extraction (follow-up full-text review)'
  cat[sid]['checked_sections']='Selected full-text passages; physical PDF pages '+','.join(map(str,c['reviewed_physical_pages']))
  cat[sid]['digest']=c['methods']+' '+c['findings'];cat[sid]['transferability_limits']=c['transfer_limits']
 assert len({x['value_id'] for x in values})==len(values)
 unique=[x for x in catalog if not x['duplicate_of']]
 assert len(unique)==92 and all('Targeted' in x['reading_stage'] or 'targeted' in x['reading_stage'] for x in unique)
 write('data/deep_review_values.csv',values);write('data/source_catalogue.csv',catalog)
 # Replace only the publication blocks covered by the manual follow-up; prior48 digests are retained.
 digest=ROOT/'docs/evidence_digest.md';text=digest.read_text()
 for c in cards:
  x=cat[c['study_id']];head='### '+c['study_id']+' — '+x['title'];block=head+'\n\n'+x['author_year']+'. Identifier: '+x['doi']+'. [PDF](../'+x['pdf_path']+').\n\nReading stage: '+x['reading_stage']+'. Checked sections: '+x['checked_sections']+'.\n\n'+c['methods']+'\n\n'+c['findings']+'\n\nTransfer limits: '+c['transfer_limits']+'\n\n'
  pattern=r'(?m)^### '+re.escape(c['study_id'])+r' —[^\n]*\n[\s\S]*?(?=^### |\Z)';assert re.search(pattern,text),c['study_id'];text=re.sub(pattern,lambda _:block,text,count=1)
 digest.write_text(text)
 md=['# Follow-up methods/results review — 5 November2026','',f'{len(cards)} manually reviewed full-text cards deepen the original abstract-only group. Reading covers selected methods/results passages, not every numerical statement, source reference or supplement. Together with the earlier48 targeted papers, all92 unique publications now have targeted full-text review. Automated packets are navigation aids and are not counted as review.','',f'The separate numerical register contains{len(values)} located records. Hold/context statuses prevent treating them as harmonised regional inputs. Two MEA quantities are accepted for the named utility reference, and sixteen other quantities for within-source arithmetic/pressure-limit benchmarks. These roles do not validate actual regional inputs.','']
 for c in cards:
  md += ['## '+c['study_id']+' — '+cat[c['study_id']]['title'],'','Physical pages: '+','.join(map(str,c['reviewed_physical_pages']))+'.','',c['methods'],'',c['findings'],'','Transfer limits: '+c['transfer_limits'],'']
 (ROOT/'docs/deep_review_report.md').write_text('\n'.join(md))
 summary=dict(followup_publications=len(cards),previous_targeted_publications=48,total_unique_targeted_fulltext_publications=92,abstract_only_unique_publications=0,located_new_numeric_records=len(values),context_or_hold_records=sum(not x['status'].startswith('ACCEPTED_') for x in values),accepted_for_source_benchmark=sum(x['status']=='ACCEPTED_FOR_STATED_BENCHMARK' for x in values),accepted_for_named_reference=sum(x['status']=='ACCEPTED_FOR_STATED_REFERENCE' for x in values),exhaustive_all_numbers_extraction=False,all_supplements_supplied=False,original_optimisations_reproduced=False)
 (ROOT/'outputs/deep_review_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
