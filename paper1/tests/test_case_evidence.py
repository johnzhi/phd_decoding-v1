import csv,json,hashlib,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):
 with (ROOT/p).open(encoding='utf-8') as f:return list(csv.DictReader(f))
class CaseEvidenceChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.M={x['batch_id']:x for x in json.loads((ROOT/'data/dataset7_manifest.json').read_text())};cls.V=read('data/case_numeric_values.csv');cls.P={x['value_id']:float(x['value']) for x in cls.V}
 def test_originals_hashes_and_transfer_scope(self):
  self.assertEqual(len(self.M),26);self.assertEqual(sum(bool(x.get('path')) for x in self.M.values()),25)
  for sid,x in self.M.items():
   if x.get('path'):self.assertEqual(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest(),x['sha256'])
   else:self.assertEqual(sid,'D7-26');self.assertIn('32 MiB',x['error'])
 def test_every_numeric_value_has_source_text_and_unique_id(self):
  self.assertEqual(len({x['value_id'] for x in self.V}),len(self.V))
  for x in self.V:
   ps=json.loads((ROOT/self.M[x['document_id']]['page_text_path']).read_text());self.assertIn(x['source_token'],ps[int(x['physical_page'])-1])
 def test_rotated_table_cells_have_real_word_coordinates(self):
  import fitz
  d=fitz.open(ROOT/self.M['D7-20']['path']);ws=d[2].get_text('words')
  for x in self.V:
   if not x['source_bbox']:continue
   bbox=json.loads(x['source_bbox']);self.assertTrue(any(w[4]==x['source_token'] and all(abs(a-b)<1e-4 for a,b in zip(w[:4],bbox)) for w in ws))
  d.close()
 def test_historical_totals_are_not_normalised_or_capacity_limits(self):
  rs=read('data/tomakomai_monthly_history.csv');self.assertEqual(len(rs),45);self.assertEqual(rs[0]['month'],'2016-04');self.assertEqual(rs[-1]['month'],'2019-12')
  r=next(x for x in rs if x['month']=='2018-04');self.assertEqual(r['moebetsu_cumulative_raw'],'17.4');self.assertEqual(r['both_cumulative_raw'],'18.8')
  r=next(x for x in rs if x['month']=='2018-09');self.assertEqual(r['moebetsu_monthly_raw'],'0.01');self.assertEqual(r['both_monthly_raw'],'0.0')
  audit=read('outputs/tomakomai_history_audit.csv');self.assertTrue(any(float(x['difference_t'])!=0 for x in audit))
  summary=json.loads((ROOT/'outputs/case_evidence_summary.json').read_text());self.assertFalse(summary['independent_maximum_annual_injection_array'])
 def test_open_measurement_window_and_distinct_rate_versions(self):
  rs=read('data/tomakomai_shutin_tests.csv');self.assertEqual(len(rs),17);self.assertEqual(rs[-1]['end_local'],'');self.assertEqual(rs[-1]['reported_measurement_hours'],'');self.assertEqual(rs[-1]['elapsed_window_hours'],'')
  self.assertEqual(self.P['TOMA_FOA11_rate'],83620);self.assertEqual(self.P['TOMA_FOT11_mass_rate'],83618)
 def test_pressure_datum_calculation_and_published_capacity_scope(self):
  p=self.P;expected=(p['TOMA_density_high']-p['TOMA_density_low'])*9.80665*p['TOMA_depth_gap']/1000
  c={x['result_id']:float(x['value']) for x in read('outputs/case_evidence_calculations.csv')};self.assertAlmostEqual(c['TOMA_hydrostatic_correction_span'],expected);self.assertAlmostEqual(expected,101.98916)
  self.assertAlmostEqual(p['TOMA_case2_pressure_cap'],12.93);self.assertEqual(p['TOMA_case2_P90'],147);self.assertEqual(p['TOMA_case2_P50'],470);self.assertEqual(p['TOMA_case2_P10'],793)
 def test_entity_scope_missing_reports_and_port_units_remain_separate(self):
  a=json.loads((ROOT/'outputs/japan_export_identity_audit.json').read_text());self.assertEqual(a['status'],'ENTITY_MISMATCH_UNRESOLVED');self.assertTrue(a['additional_mentions_ENEOS']);self.assertEqual(a['metadata']['事業者名'],'日本製鉄株式会社')
  missing=[x for x in read('data/japan_company_emissions.csv') if x['status']=='NO_REPORT'];self.assertTrue(missing);self.assertTrue(all(x['value']=='' for x in missing))
  facilities=read('data/japan_facility_candidates.csv');self.assertEqual(len(facilities),78);self.assertTrue(all('report_year'in x for x in facilities));self.assertNotIn('emissions_fiscal_year',facilities[0])
  ports=read('data/cppi_port_reference.csv');self.assertEqual(len(ports),424);self.assertIn('Berth hours in % of port hours',ports[0]);self.assertNotIn('turnaround_hours',ports[0])
 def test_component_transfer_excludes_aggregate_shipping_and_unresolved_process_rows(self):
  components=read('data/northern_lights_components.csv');numeric=[x for x in components if x['cell_status']=='PRINTED_NUMERIC'];self.assertEqual(len(numeric),25)
  blank=[x for x in components if x['cell_status']=='BLANK_NOT_IMPUTED'];self.assertTrue(blank);self.assertTrue(all(x['reported_tco2e']=='' for x in blank))
  subtotal=sum(float(x['reported_tco2e']) for x in numeric if x['area']=='storage' and x['activity']!='Other process emissions');self.assertEqual(subtotal,268220)
  cases=read('outputs/northern_lights_storage_proxy_comparisons.csv');self.assertEqual(len(cases),100)
  for x in cases:
   self.assertEqual(x['complete_net_avoided_ghg_t'],'');self.assertAlmostEqual(float(x['additional_selected_storage_proxy_tco2e']),float(x['additional_injected_t'])*subtotal/(127.8e6),places=5)
  c={x['result_id']:float(x['value']) for x in read('outputs/case_evidence_calculations.csv')};self.assertAlmostEqual(c['NL_sum_printed_appendix'],3311298.12);self.assertAlmostEqual(c['NL_appendix_minus_headline'],-8701.88)
if __name__=='__main__':unittest.main()
