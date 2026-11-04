#!/usr/bin/env python3
"""Index retained reference packages; never execute XLSM macros or external links.

Native workbook dumps distinguish cached values, formulas, Excel errors and
styles. They are a searchable raw archive, not an approved parameter table.
"""
from pathlib import Path,PurePosixPath
import csv,json,gzip,hashlib,re,zipfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def write(name,rows):
 with (ROOT/name).open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def manifests():return sum([json.loads((ROOT/f'data/dataset{i}_manifest.json').read_text()) for i in [5,6]],[])
def dump_workbook(path,sid):
 base=ROOT/'evidence/reference_workbooks';base.mkdir(exist_ok=True);n=0;numeric=0;forms=0;metadata=[]
 with zipfile.ZipFile(path) as z,gzip.open(base/f'{sid}_cells.jsonl.gz','wt',encoding='utf-8') as out:
  shared=[]
  if 'xl/sharedStrings.xml' in z.namelist():
   for si in ET.fromstring(z.read('xl/sharedStrings.xml')):shared.append(''.join(si.itertext()))
  rels={x.attrib['Id']:x.attrib['Target'] for x in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
  wb=ET.fromstring(z.read('xl/workbook.xml'))
  for sheet in wb.find('m:sheets',NS):
   target=rels[sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']];target=target.lstrip('/') if target.startswith('/') else 'xl/'+target
   doc=ET.fromstring(z.read(target));count=0
   from openpyxl.utils.cell import get_column_letter,column_index_from_string
   for row_index,row in enumerate(doc.findall('.//m:sheetData/m:row',NS),1):
    row_number=int(row.get('r',row_index));next_col=1
    for c in row.findall('m:c',NS):
     ref=c.get('r',f'{get_column_letter(next_col)}{row_number}');next_col=column_index_from_string(re.match(r'[A-Z]+',ref).group())+1
     typ=c.get('t','n');v=c.find('m:v',NS);v=v.text if v is not None else None;formula=c.find('m:f',NS)
     if typ=='s' and v is not None:v=shared[int(v)]
     elif typ=='inlineStr':v=''.join(c.find('m:is',NS).itertext())
     elif typ=='n' and v is not None:
      try:v=float(v);numeric+=1
      except ValueError:pass
     if v is None and formula is None:continue
     rec=dict(document_id=sid,sheet=sheet.attrib['name'],cell=ref,cached_value=v,value_type=typ,style_id=c.get('s'),formula=formula.text if formula is not None else None,formula_attributes=formula.attrib if formula is not None else None)
     out.write(json.dumps(rec,ensure_ascii=False)+'\n');n+=1;count+=1;forms+=formula is not None
   dim=doc.find('m:dimension',NS);metadata.append(dict(sheet=sheet.attrib['name'],dimension=dim.get('ref') if dim is not None else '',nonempty_or_formula_cells=count))
  meta=dict(document_id=sid,source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),cells=n,numeric_cached_cells=numeric,formula_cells=forms,sheets=metadata,macros_executed=False,external_links_refreshed=False)
  (base/f'{sid}_metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
 return meta

def extract_japan():
 import openpyxl
 M={x['batch_id']:x for x in manifests() if x.get('path')};rows=[]
 for sid,kind,fcol,mcol in [('D5-38','electricity',4,3),('D5-16','heat',5,4),('D5-45','gas',5,4)]:
  w=openpyxl.load_workbook(ROOT/M[sid]['path'],read_only=True,data_only=True,keep_links=False);s=w.worksheets[0];company=registration=region=''
  for row in s:
   vals=[c.value for c in row]
   if len(vals)<fcol+1:continue
   if row[1].value and str(row[1].value).startswith('代替値'):
    for c in row:
     if isinstance(c.value,(int,float)):
      rows.append(dict(document_id=sid,kind=kind,sheet=s.title,cell=c.coordinate,supplier='OFFICIAL_FALLBACK',registration='',region='',menu='代替値',coefficient_type='fallback',raw_value=str(c.value),reported_value=c.value,unit={'electricity':'tCO2/kWh','heat':'tCO2/GJ','gas':'tCO2/1000m3'}[kind],scope='Japanese reporting coefficient; not supplier matching or complete LCA.'))
    continue
   # Require a number or footnoted number in the factor columns, not arbitrary numeric rows.
   raw=[row[fcol-1].value,row[fcol].value]
   def number(v):
    if isinstance(v,(int,float)):return float(v)
    if isinstance(v,str) and re.fullmatch(r'\s*[0-9]+(?:\.[0-9]+)?(?:[※＊*].*)?\s*',v):return float(re.match(r'\s*([0-9.]+)',v).group(1))
    return None
   nums=list(map(number,raw))
   if not any(v is not None for v in nums):continue
   if row[1].value:
    company=str(row[1].value);registration=str(row[0].value or '');region=''
   if kind!='electricity' and row[2].value:region=str(row[2].value)
   for j,v in enumerate(nums):
    if v is not None:rows.append(dict(document_id=sid,kind=kind,sheet=s.title,cell=row[fcol-1+j].coordinate,supplier=company,registration=registration,region=region,menu=str(row[mcol-1].value or ''),coefficient_type='base' if j==0 else 'adjusted',raw_value=str(raw[j]),reported_value=v,unit={'electricity':'tCO2/kWh','heat':'tCO2/GJ','gas':'tCO2/1000m3'}[kind],scope='Menu/base/adjusted reporting factor retained; zero values do not establish zero lifecycle GHG.'))
 write('data/japan_current_factors.csv',rows)
 return len(rows)

def waves():
 import xarray as xr
 M={x['batch_id']:x for x in manifests() if x.get('path')};cover=[];values=[]
 for sid in ['D5-53','D5-55']:
  with xr.open_dataset(ROOT/M[sid]['path']) as d:
   cover.append(dict(document_id=sid,timestamps=d.sizes['time'],latitudes=d.sizes['latitude'],longitudes=d.sizes['longitude'],time_start=str(d.time.values.min()),time_end=str(d.time.values.max()),latitude=float(d.latitude.values[0]),longitude=float(d.longitude.values[0]),calendar_usable=False,reason='One timestamp and one grid point; no historical availability distribution or route coverage can be estimated.'))
   for k,v in d.data_vars.items():values.append(dict(document_id=sid,variable=k,time=str(d.time.values[0]),latitude=float(d.latitude.values[0]),longitude=float(d.longitude.values[0]),value=float(v.values.flat[0]),unit=v.attrs.get('units',''),standard_name=v.attrs.get('standard_name','')))
 write('data/wave_coverage.csv',cover);write('data/wave_snapshot_values.csv',values);return cover

def bag_audit():
 M={x['batch_id']:x for x in manifests() if x.get('path')};candidates={}
 for x in M.values():candidates.setdefault(Path(x['path']).name,[]).append(x)
 result=[]
 for sid,algorithm,part in [('D6-01','sha256','payload'),('D6-05','sha512','payload'),('D6-04','sha256','tags'),('D6-06','sha512','tags')]:
  for line in (ROOT/M[sid]['path']).read_text().splitlines():
   digest,rel=line.split(None,1);name=PurePosixPath(rel).name;found=candidates.get(name,[]);match=next((x for x in found if hashlib.new(algorithm,(ROOT/x['path']).read_bytes()).hexdigest()==digest),None)
   result.append(dict(manifest_id=sid,part=part,algorithm=algorithm,declared_path=rel,expected_hash=digest,matching_document=match['batch_id'] if match else '',status='MATCHED' if match else 'NOT_AVAILABLE_OR_MISMATCH',note='Four report files exceeded the32MiB transfer limit; this is partial validation, not a complete BagIt validation.' if not match else 'Matched original uploaded bytes.'))
 write('data/ibdp_bag_checksum_audit.csv',result);return result

def main():
 rows=manifests();catalog=[];books=[]
 for x in rows:
  sid=x['batch_id'];p=ROOT/x['path'] if x.get('path') else None
  if p and p.suffix.lower() in ['.xlsx','.xlsm']:books.append(dump_workbook(p,sid))
  stage='Archived and indexed; targeted model-use review only'
  if sid in ['D5-02','D5-16','D5-38','D5-45','D5-48','D5-49','D5-50','D5-51','D5-53','D5-54','D5-55','D6-07','D6-20','D6-22','D6-23']:stage='Targeted boundary, unit or dataset inspection'
  catalog.append(dict(document_id=sid,original_filename=p.name if p else x.get('original_filename','untransferred report'),path=x.get('path',''),sha256=x.get('sha256',''),size_bytes=p.stat().st_size if p else '',pages=x.get('pages',''),duplicate_of=x.get('duplicate_of',''),reading_stage=stage,transfer_status='AVAILABLE' if p else x.get('error','UNAVAILABLE')))
 write('data/reference_dataset_catalogue.csv',catalog);j=extract_japan();wave=waves();bag=bag_audit()
 summary=dict(uploaded_references=len(rows),available=sum(bool(x.get('path')) for x in rows),unavailable=[x['batch_id'] for x in rows if not x.get('path')],native_workbooks=len(books),archived_workbook_cells=sum(x['cells'] for x in books),japan_current_factor_records=j,wave_coverage=wave,bag_payload_sha256_matches=sum(x['part']=='payload' and x['algorithm']=='sha256' and x['status']=='MATCHED' for x in bag),bag_payload_sha256_expected=sum(x['part']=='payload' and x['algorithm']=='sha256' for x in bag),all_workbooks_cached_not_recalculated=True)
 (ROOT/'outputs/reference_ingest_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
