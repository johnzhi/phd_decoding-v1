#!/usr/bin/env python3
"""Regenerate plain page text separately from retained layout-preserving extraction."""
from pathlib import Path
import csv,json
import fitz
ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
 out=ROOT/'outputs/regenerated_page_text';out.mkdir(exist_ok=True)
 for x in csv.DictReader((ROOT/'data/source_catalogue.csv').open()):
  with fitz.open(ROOT/x['pdf_path']) as d:
   (out/(x['study_id']+'.json')).write_text(json.dumps([p.get_text() for p in d],ensure_ascii=False,indent=1))
 print('Wrote regenerated plain text; retained evidence/pages was not overwritten.')
