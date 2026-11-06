import csv,gzip,hashlib,json,unittest
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]
def read(p):
 with (ROOT/p).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))

class PartialEvidenceChecks(unittest.TestCase):
 def test_original_identity_and_current_primary_boundary(self):
  m=json.loads((ROOT/'data/dataset8_manifest.json').read_text());self.assertEqual(len(m),2)
  for x in m:self.assertEqual(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest(),x['sha256'])
  s=json.loads((ROOT/'outputs/partial_evidence_summary.json').read_text())
  self.assertEqual(s['primary_pdfs_verified'],3);self.assertEqual(s['calibrated_model_inputs_added'],0)
  for k in ['native_telemetry_received','maximum_rate_array_received','pressure_datum_verified','new_capture_GHG_or_shipping_fuel_model','complete_lca']:self.assertFalse(s[k])
  leads=read('data/partial_primary_source_leads.csv');self.assertEqual(len(leads),9);self.assertEqual(sum(x['status']=='LINK_ONLY_PRIMARY_NOT_RETAINED' for x in leads),6)
 def test_every_numeric_workbook_cell_is_preserved_without_model_eligibility(self):
  with gzip.open(ROOT/'evidence/reference_workbooks/D8-02_cells.jsonl.gz','rt') as f:cells={(x['sheet'],x['cell']):x for x in map(json.loads,f)}
  rows=read('data/partial_compilation_values.csv');self.assertEqual(len(rows),60);self.assertEqual(len({x['value_id'] for x in rows}),60)
  numeric={key for key,x in cells.items() if x['value_type']=='n' and isinstance(x['cached_value'],(int,float))}
  represented=set()
  for x in rows:
   self.assertIn(x['status'],{'SUPPLIED_TRANSCRIPTION_PRIMARY_PENDING_NOT_MODEL_INPUT','PRIMARY_VALUE_VERIFIED_CONTEXT_ONLY_NOT_CALIBRATED_INPUT','DERIVED_FROM_VERIFIED_PRIMARY_INPUTS_NOT_CORRECTED_OBSERVATION'})
   self.assertEqual(x['original_compilation_status'],'SUPPLIED_TRANSCRIPTION_PRIMARY_PENDING_NOT_MODEL_INPUT')
   if x['status']=='SUPPLIED_TRANSCRIPTION_PRIMARY_PENDING_NOT_MODEL_INPUT':self.assertEqual(x['primary_pdf_retained'],'False');self.assertEqual(x['primary_page_verified'],'False')
   key=x['sheet'],x['cell'];c=cells[key]['cached_value']
   if key in numeric:self.assertEqual(Decimal(str(c)),Decimal(x['value']));represented.add(key)
   else:self.assertIn(str(x['value']),str(c))
  self.assertEqual(numeric,represented);self.assertEqual(len(numeric),58)
 def test_duplicate_representations_and_missing_december_are_not_new_observations(self):
  matches=read('outputs/partial_csv_workbook_agreement.csv');self.assertEqual(len(matches),28);self.assertTrue(all(x['match']=='True' for x in matches))
  rs=read('data/tomakomai_paired_partial.csv');self.assertEqual(len(rs),7)
  self.assertEqual(sum(x['actual_injected_t_month']!='' for x in rs),6)
  for x in rs:
   y,m=map(int,x['month'].split('-'));ey,em=(y,m+1) if m<12 else (y+1,1)
   self.assertEqual(x['report_edition'],f'{ey}{em:02d}')
  december=next(x for x in rs if x['month']=='2019-12')
  for k in ['actual_injected_t_month','published_cumulative_Moebetsu_t','calendar_average_t_per_day']:self.assertEqual(december[k],'')
  self.assertEqual(december['avg_bhp_MPa_basis_unverified'],'9.56')
  february=next(x for x in rs if x['month']=='2019-02');self.assertEqual(int(february['calendar_days']),28)
  self.assertAlmostEqual(float(february['calendar_average_t_per_day']),4031.7/28)
 def test_consecutive_month_reconciliation_does_not_interpolate_or_repair(self):
  rs=read('outputs/tomakomai_partial_reconciliation.csv');self.assertEqual(len(rs),3)
  r={x['month']:x for x in rs};self.assertEqual(r['2019-06']['cumulative_delta_t'],'1217.3');self.assertEqual(r['2019-06']['monthly_minus_delta_t'],'98.1')
  self.assertEqual(r['2019-06']['within_conditional_rounding'],'False');self.assertEqual(r['2019-10']['monthly_minus_delta_t'],'-0.1');self.assertEqual(r['2019-11']['monthly_minus_delta_t'],'0.0')
  original=next(x for x in read('data/tomakomai_paired_partial.csv') if x['month']=='2019-05');self.assertEqual(original['published_cumulative_Moebetsu_t'],'260414.4')
  coarse=read('outputs/tomakomai_partial_coarse_comparison.csv');self.assertEqual(len(coarse),12);self.assertTrue(all(x['within_conditional_display_rounding']=='True' for x in coarse))
 def test_trial_records_do_not_supply_a_fuel_or_operating_calendar(self):
  rs=read('data/excool_loading_trial_leads.csv');self.assertEqual(len(rs),7)
  june=[x for x in rs if x['test_month']=='2025-06'];self.assertEqual({Decimal(x['loaded_co2_t']) for x in june},{Decimal('750'),Decimal('743.2')})
  self.assertTrue(all('fuel' not in k for k in rs[0]))
  checks=read('outputs/excool_trial_property_checks.csv');self.assertEqual(len(checks),7)
  self.assertEqual(sum(x['nominal_pure_fluid_phase']=='gas' for x in checks),4)
  for x in checks:
   self.assertAlmostEqual((float(x['nominal_absolute_pressure_pa'])-float(x['pure_co2_saturation_pressure_pa']))/1000,float(x['nominal_pressure_minus_saturation_kpa']))
   self.assertEqual(x['status'],'REFERENCE_CONSISTENCY_CHECK_NOT_MEASURED_PHASE')
   self.assertNotIn('cargo_density_kg_m3',x);self.assertIn('does not establish actual vapour cargo',x['scope'])
 def test_capture_leads_and_supplied_gap_map_do_not_overwrite_current_model(self):
  energy=read('data/tomakomai_capture_energy_leads.csv');self.assertEqual(len(energy),4)
  self.assertTrue(all(x['model_used']=='False' for x in energy));self.assertEqual({x['value'] for x in energy},{'0.923','0.882','0.915','0.148'})
  gaps={x['component']:x for x in read('data/partial_supplied_gap_map.csv')}
  self.assertIn('already implemented',gaps['Mixed allocation']['current_project_interpretation']);self.assertIn('already implemented',gaps['Fuel inventory']['current_project_interpretation'])

if __name__=='__main__':unittest.main()
