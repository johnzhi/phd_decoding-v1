#!/usr/bin/env python3
from pathlib import Path
import csv
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment
ROOT=Path(__file__).resolve().parents[1]
def count(name):
 with (ROOT/name).open(encoding='utf-8') as f:return sum(1 for _ in csv.DictReader(f))
w=Workbook();s=w.active;s.title='Read me'
for row in [ ['Paper 1 source-driven evidence workbook'],['Current draft', 'manuscript/Paper_1_draft.md and .docx'],['Coverage','93 PDFs / 92 unique publications; 48 targeted, 44 abstract-screened; extraction is selective.'],['Extraction records',count('data/all_extracted_values.csv')],['Curated PDF records',count('data/curated_values.csv')],['Supplement numeric records',count('data/supplement_values.csv')],['Original benchmark input rows',134],['Supplement annual grid','720 cells; 250 printed values and 470 blanks; rounded allocation replay'],['Operational inputs',count('data/operational_parameters.csv')],['Operational comparisons','144 comparisons,36 contrasts; partial active fuel boundary, not complete LCA'],['Outputs','49 calculations plus 75 directly transcribed fleet outputs.'],['Scientific scope','Cross-study reported-burden score is NOT net avoided emissions; reconcile fugitive/source losses and omitted burdens first.'],['Status','HOLD records are excluded from analysis. Broad extraction records are not harmonised regional inputs.'],['Reproduce','python paper1/scripts/reproduce.py; python -m unittest discover -s paper1/tests -v'],['Metadata','Read data dictionary, proxy register and evidence digest for full limits.'] ]:s.append(row)
files=[('Source catalogue','data/source_catalogue.csv'),('All extracted values','data/all_extracted_values.csv'),('Curated values','data/curated_values.csv'),('Analysis inputs','data/analysis_inputs.csv'),('New paper values','data/new_batch_values.csv'),('Calculated results','outputs/calculated_results.csv'),('Source issues','data/issues.csv'),('Proposal audit','data/proposal_claim_audit.csv'),('Supplement documents','data/supplement_documents.csv'),('Supplement values','data/supplement_values.csv'),('Supplement sources','data/supplement_sources.csv'),('Supplement reservoirs','data/supplement_reservoirs.csv'),('Supplement distances','data/supplement_distances.csv'),('Annual allocation grid','data/supplement_annual_injection.csv'),('Annual replay','outputs/supplement_annual_replay.csv'),('Replay summary','outputs/supplement_scenario_summary.csv'),('Operating inputs','data/operational_parameters.csv'),('Operating comparisons','outputs/operational_comparisons.csv'),('Operating contrasts','outputs/operational_contrasts.csv'),('Operating controls','outputs/operational_controls.csv'),('Fleet adequacy','outputs/operational_design_adequacy.csv'),('Selected fleet comparison','outputs/operational_design_comparisons.csv'),('Operating data gaps','data/operational_data_gaps.csv')]
for title,p in files:
 s=w.create_sheet(title)
 with (ROOT/p).open(encoding='utf-8') as f:
  for row in csv.reader(f):s.append(["'"+x if x.startswith('=') else x for x in row])
 s.freeze_panes='A2';s.auto_filter.ref=s.dimensions
for s in w:
 for cell in s[1]:cell.font=Font(bold=True,color='FFFFFF');cell.fill=PatternFill('solid',fgColor='24475B')
 for row in s.iter_rows(min_row=2):
  for cell in row:cell.alignment=Alignment(wrap_text=True,vertical='top')
 for col in s.columns:
  length=max(len(str(c.value or '')) for c in list(col)[:30]);s.column_dimensions[col[0].column_letter].width=min(55,max(15,length*.7))
w.save(ROOT/'data/Paper_1_evidence.xlsx');print('Saved evidence workbook')
