#!/usr/bin/env python3
"""Extract the supplied DOCX's native tables; figures remain separately audited.

No figure OCR output is accepted as input automatically. The retained annual-cell
CSV is a reviewed transcription of printed figure annotations, not raw MILP data.
"""
from pathlib import Path
import csv,json,hashlib,zipfile
from decimal import Decimal
from docx import Document
ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/'original/supplements/43979_2025_135_MOESM1_ESM.docx'
SID='B4-06-S1'
def write(p,rows):
 with p.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def extract():
 d=Document(DOC);base=ROOT/'evidence/supplements'/SID;base.mkdir(parents=True,exist_ok=True)
 paragraphs=[dict(paragraph=i,text=p.text) for i,p in enumerate(d.paragraphs,1) if p.text.strip()]
 tables=[[[c.text for c in row.cells] for row in t.rows] for t in d.tables]
 (base/'native_tables.json').write_text(json.dumps(dict(paragraphs=paragraphs,tables=tables),ensure_ascii=False,indent=2))
 media=[]
 with zipfile.ZipFile(DOC) as z:
  for p in z.namelist():
   if p.startswith('word/media/'):
    b=z.read(p);target=base/Path(p).name;target.write_bytes(b);media.append(dict(path=str(target.relative_to(ROOT)),sha256=hashlib.sha256(b).hexdigest()))
 sources=[]
 for rid,row in enumerate(tables[0][1:],2):
  sid,industry,rate,cost=row
  sources.append(dict(source=sid,industry_type=industry,co2_rate_mtpa=rate,capture_cost_usd_per_t=cost,source_table='S1',docx_row=rid))
 reservoirs=[]
 for rid,row in enumerate(tables[1][1:],2):
  sid,typ,cap,start,cost=row;parts=cost.split(' to ')
  reservoirs.append(dict(reservoir=sid,reservoir_type=typ,capacity_mt=cap,estimated_start_year=start,storage_cost_reported=cost,storage_cost_low_usd_per_t=parts[0],storage_cost_high_usd_per_t=parts[-1],source_table='S2',docx_row=rid))
 distances=[]
 for rid,row in enumerate(tables[2][2:],3):
  typ,node,h1,h2=row
  for hub,value in [('h1',h1),('h2',h2)]:
   distances.append(dict(node_type=typ,node=node,hub=hub,distance_km='' if value=='-' else value,cell_status='DASH_NOT_A_DISTANCE' if value=='-' else 'REPORTED_VALUE',source_table='S3',docx_row=rid))
 write(ROOT/'data/supplement_sources.csv',sources);write(ROOT/'data/supplement_reservoirs.csv',reservoirs);write(ROOT/'data/supplement_distances.csv',distances)
 values=[]
 def add(key,param,value,unit,table,row,case,note):
  values.append(dict(value_id=key,study_id=SID,parameter=param,value=value,unit=unit,pdf_page='',locator=f'Table {table}, DOCX table row {row}',scenario=case,evidence_type='Published model input',boundary='South Sumatra industrial-cluster CCS model',status='EXTRACTED_NATIVE_DOCX_TABLE',transferability_note=note))
 for x in sources:
  for col,param,unit in [('co2_rate_mtpa','Source CO2 rate','MtCO2/year'),('capture_cost_usd_per_t','Capture cost','USD/tCO2')]:
   add(f"sup_{x['source']}_{col}",param,x[col],unit,'S1',x['docx_row'],x['industry_type'],'The main paper defines ms,t as captured mass; do not apply the capture fraction again without checking its boundary. No source energy/GHG inventory is supplied by this cost.')
 for x in reservoirs:
  sid=x['reservoir'];add(f'sup_{sid}_capacity','Candidate reservoir storage capacity',x['capacity_mt'],'MtCO2','S2',x['docx_row'],x['reservoir_type'],'Published model candidate capacity referencing Zhang & Lau; not annual deliverability, measured permanence or commercial allocation.')
  add(f'sup_{sid}_start','Estimated injection start year',x['estimated_start_year'],'calendar year','S2',x['docx_row'],x['reservoir_type'],'Depletion/readiness estimate in the paper, not confirmed commissioning.')
  parts=x['storage_cost_reported'].split(' to ')
  for n,v in enumerate(parts):add(f'sup_{sid}_cost_{n+1}','Storage cost'+(' lower bound' if len(parts)>1 and n==0 else ' upper bound' if len(parts)>1 else ''),v,'USD/tCO2','S2',x['docx_row'],x['reservoir_type'],'Retains supplied value/range; main-paper economic base year is 2023. Not a GHG factor.')
 for x in distances:
  if x['cell_status']=='REPORTED_VALUE':add(f"sup_distance_{x['node']}_{x['hub']}",'Distance to hub',x['distance_km'],'km','S3',x['docx_row'],x['node']+' to '+x['hub'],'Published network model distance; no Japanese route or shipping distance is implied. Dash entries remain missing, not zero.')
 write(ROOT/'data/supplement_table_values.csv',values)
 write(ROOT/'data/supplement_documents.csv',[dict(document_id=SID,parent_study_id='B4-06',title='Budiarto et al. (2025) supplementary materials',path=str(DOC.relative_to(ROOT)),sha256=hashlib.sha256(DOC.read_bytes()).hexdigest(),native_tables=3,figures=10,locator_convention='DOCX table and physical row; figure/cell for heatmaps; no stable PDF page number')])
 (base/'media_manifest.json').write_text(json.dumps(media,indent=2))
 return values
if __name__=='__main__':print(f'Extracted {len(extract())} numeric table records; three native tables and ten source figures preserved.')
