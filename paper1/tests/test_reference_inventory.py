import unittest,csv,json,hashlib,sys,gzip
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
def rd(name):
 with (ROOT/name).open() as f:return list(csv.DictReader(f))
class ReferenceChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=sum([json.loads((ROOT/f'data/dataset{i}_manifest.json').read_text()) for i in [5,6]],[]);cls.M={x['batch_id']:x for x in cls.manifest}
  cls.inputs=rd('data/reference_inventory_inputs.csv');cls.P={x['value_id']:float(x['value']) for x in cls.inputs}
 def test_originals_unchanged_and_unavailable_files_not_claimed(self):
  self.assertEqual(len(self.manifest),104);self.assertEqual(sum('path'in x for x in self.manifest),100)
  for x in self.manifest:
   if x.get('path'):self.assertEqual(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest(),x['sha256'])
   else:self.assertIn('32 MiB',x['error'])
 def test_pdf_input_locators(self):
  for x in self.inputs:
   if x['locator'].startswith('physical PDF page '):
    p=int(x['locator'].split()[-1]);pages=json.loads((ROOT/self.M[x['document_id']]['page_text_path']).read_text());self.assertIn(x['source_token'],pages[p-1])
 def test_imo_unit_scaling_and_gwp(self):
  p=self.P;expected=p['imo_co2']+p['imo_ch4']*28+p['imo_n2o']*265+p['imo_wtt']*p['imo_lcv']
  actual=json.loads((ROOT/'outputs/imo_mdo_default_inventory.json').read_text())
  self.assertAlmostEqual(actual['wtt_kgco2e_per_kg'],.75579)
  self.assertAlmostEqual(expected,4.01089);self.assertAlmostEqual(actual['wtw_kgco2e_per_kg'],expected)
 def test_electric_heat_and_market_boundaries(self):
  self.assertEqual(self.P['NVE_physical_climate_2025'],9.4);self.assertEqual(self.P['NVE_market_disclosure_2025'],430.93)
  self.assertAlmostEqual(self.P['JP_R8_electric_fallback']*1000,.416);self.assertAlmostEqual(self.P['JP_R8_heat_fallback']*1000,53.2)
  cases=rd('data/netl_capture_reference_cases.csv')
  for x in cases:
   if x['route']=='electric_makeup':
    self.assertEqual(x['heat_gj_per_t'],'');self.assertAlmostEqual(float(x['electricity_kwh_per_t']),float(x['auxiliary_kwh_per_t'])+float(x['steam_opportunity_kwh_per_t']))
   else:self.assertEqual(x['steam_opportunity_kwh_per_t'],'');self.assertGreater(float(x['heat_gj_per_t']),2.7);self.assertLess(float(x['electricity_kwh_per_t']),120)
 def test_wave_snapshots_cannot_create_availability(self):
  cover=rd('data/wave_coverage.csv');self.assertEqual(len(cover),2)
  for x in cover:self.assertEqual(x['timestamps'],'1');self.assertEqual(x['latitudes'],'1');self.assertEqual(x['longitudes'],'1');self.assertEqual(x['calendar_usable'],'False')
 def test_partial_bag_and_recovered_norway_sales_export(self):
  summary=json.loads((ROOT/'outputs/reference_ingest_summary.json').read_text());self.assertEqual(summary['bag_payload_sha256_matches'],27);self.assertEqual(summary['bag_payload_sha256_expected'],31)
  meta=json.loads((ROOT/'evidence/reference_workbooks/D5-01_metadata.json').read_text());self.assertEqual(meta['numeric_cached_cells'],2);self.assertFalse(meta['macros_executed'])
  with gzip.open(ROOT/'evidence/reference_workbooks/D5-01_cells.jsonl.gz','rt') as f:cells={x['cell']:x['cached_value'] for x in map(json.loads,f)}
  self.assertEqual(cells['B4'],101.0025);self.assertEqual(cells['B5'],36.5945)
 def test_full_lca_remains_uncomputed_and_utility_uses_captured_mass(self):
  xs=rd('outputs/reference_inventory_comparisons.csv');self.assertEqual(len(xs),2980)
  scenario={x['utility_scenario']:float(x['capture_utility_kg_per_t_captured']) for x in rd('data/capture_utility_scenarios.csv')}
  for x in xs:
   self.assertEqual(x['complete_net_avoided_ghg_t'],'')
   self.assertAlmostEqual(float(x['additional_capture_utility_inventory_t']),float(x['additional_captured_t'])*scenario[x['utility_scenario']]/1000,places=5)
if __name__=='__main__':unittest.main()
