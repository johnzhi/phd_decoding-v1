#!/usr/bin/env python3
"""Prepare auditable full-text page selections; selection alone is not review."""
from pathlib import Path
import csv,json,re
ROOT=Path(__file__).resolve().parents[1]
with (ROOT/'data/source_catalogue.csv').open() as f:catalog=list(csv.DictReader(f))
previous=ROOT/'evidence/deep_review/selection.json';base=previous.parent;base.mkdir(exist_ok=True)
if previous.exists():ids=[x['study_id'] for x in json.loads(previous.read_text())]
else:ids=[x['study_id'] for x in catalog if 'Abstract' in x['reading_stage'] and not x['duplicate_of']]
records=[]
for sid in ids:
 x=next(a for a in catalog if a['study_id']==sid);ps=json.loads((ROOT/x['page_text_path']).read_text())
 ref_start=next((i for i,t in enumerate(ps) if re.search(r'^\s*(?:\d+\.?\s+)?(?:References|Bibliography)\s*$',t,re.M|re.I)),len(ps))
 usable=[i for i in range(1,ref_start) if len(ps[i])>700]
 # Actual page choices are retained for the human/assistant to inspect and amend.
 method=next((i for i in usable if re.search(r'(?:\b2\.?\s+(?:Method|Model|Materials)|\bModel formulation|\bMathematical formulation|\bMethodology)',ps[i],re.I)),usable[0])
 result_candidates=[i for i in usable if i>method and i<int(.88*len(ps))] or usable
 def score(i):return 3*len(re.findall(r'\bTable\s+[1-9]',ps[i],re.I))+len(re.findall(r'\b(?:kg|GJ|kWh|MPa|Mt|tonnes|tCO2|MWe|MW|million|percent|capacity|cost)\b',ps[i],re.I))+.2*len(re.findall(r'\d+\.\d+',ps[i]))
 result=max(result_candidates,key=score)
 conclusion=next((i for i in reversed(usable) if re.search(r'^\s*(?:\d+(?:\.\d+)?\.?\s+)?(?:Conclusions?|Concluding remarks|Discussion and conclusions)(?:\s+and[^\n]*)?\s*$',ps[i],re.I|re.M) and i>method),usable[-1])
 selected=sorted(set([method,result,conclusion]));record=dict(study_id=sid,title=x['title'],page_count=len(ps),selected_physical_pages=[i+1 for i in selected],selection_status='Prepared for targeted scientific reading; not evidence of completed review');records.append(record)
 (base/f'{sid}_packet.txt').write_text(x['title']+'\n\n'+'\n\n'.join(f'PHYSICAL_PAGE {i+1}\n{ps[i]}' for i in selected))
previous.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');print('Prepared',len(records),'targeted review packets')
if __name__=='__main__':pass
