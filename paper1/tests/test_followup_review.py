import csv,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):
 with (ROOT/p).open(encoding='utf-8') as f:return list(csv.DictReader(f))

class FollowupEvidenceChecks(unittest.TestCase):
 def test_review_coverage_requires_manual_beyond_abstract_cards(self):
  cards=json.loads((ROOT/'data/deep_review_cards.json').read_text())
  cat={x['study_id']:x for x in read('data/source_catalogue.csv')}
  expected={x['study_id'] for x in json.loads((ROOT/'evidence/deep_review/selection.json').read_text())}
  self.assertEqual(len(cards),44);self.assertEqual({x['study_id'] for x in cards},expected)
  unique=[x for x in cat.values() if not x['duplicate_of']]
  self.assertEqual(len(unique),92);self.assertTrue(all('Targeted' in x['reading_stage'] for x in unique))
  for x in cards:
   self.assertTrue(x['methods'] and x['findings'] and x['transfer_limits'])
   self.assertTrue(any(p>1 for p in x['reviewed_physical_pages']))
   self.assertTrue(all(1<=p<=int(cat[x['study_id']]['pages']) for p in x['reviewed_physical_pages']))
 def test_located_values_and_hold_exclusion(self):
  rows=read('data/deep_review_values.csv');self.assertEqual(len(rows),140)
  cat={x['study_id']:x for x in read('data/source_catalogue.csv')};pages={}
  for x in rows:
   sid=x['study_id']
   if sid not in pages:pages[sid]=json.loads((ROOT/cat[sid]['page_text_path']).read_text())
   self.assertIn(x['source_token'],pages[sid][int(x['physical_page'])-1])
  accepted=read('data/limitation_benchmark_inputs.csv');self.assertEqual(len(accepted),18)
  self.assertTrue(all(x['status'].startswith('ACCEPTED_') for x in accepted))
  self.assertFalse(any(x['study_id']=='B2-05' for x in accepted))
  conflicts=[x for x in rows if x['value_id'] in ['deep_B205_body_shortfall','deep_B205_caption_shortfall']]
  self.assertEqual({x['value'] for x in conflicts},{'4.8','1.7'})
  self.assertTrue(all(x['status']=='HOLD_CONFLICT' for x in conflicts))
 def test_property_check_keeps_datum_and_prose_uncertainty(self):
  rows=read('outputs/property_consistency.csv');self.assertEqual(len(rows),2)
  self.assertEqual({float(x['P_pascal']) for x in rows},{700000,801325})
  for x in rows:
   self.assertEqual(x['eos_phase'],'liquid');self.assertAlmostEqual(float(x['T_kelvin']),223.15)
   self.assertLess(abs(float(x['relative_difference_percent'])),.1)
   self.assertGreater(float(x['eos_to_printed_prose_ratio']),999)
  meta=json.loads((ROOT/'outputs/property_consistency_summary.json').read_text())
  self.assertEqual(meta['EOS_reference_key'],'Span-JPCRD-1996')
  for key in ['source_density_replaced','source_prose_repaired','actual_mixture_validated']:self.assertFalse(meta[key])
  fleets=read('outputs/property_fleet_sensitivity.csv');self.assertEqual(len(fleets),75);self.assertTrue(all(x['match']=='True' for x in fleets))
 def test_MEA_utility_charges_captured_mass_and_replaces_reference(self):
  case=read('data/deep_capture_reference_case.csv')[0]
  self.assertEqual(float(case['heat_gj_per_t_captured']),3.6)
  self.assertEqual(float(case['electricity_kwh_per_t_captured']),100)
  self.assertAlmostEqual(float(case['utility_inventory_kg_per_t_captured']),233.12)
  for x in read('outputs/MEA_reference_comparisons.csv'):
   C=float(x['additional_captured_t']);I=float(x['additional_injected_t']);G=float(x['additional_MEA_reference_utility_t'])
   self.assertAlmostEqual(G,C*.23312,places=5)
   storage=float(x['additional_storage_reference_t']) if x['storage_reference_applied']=='True' else 0
   self.assertAlmostEqual(float(x['remaining_allowance_t']),I-G-float(x['additional_marine_wtw_t'])-storage,places=4)
   self.assertEqual(x['complete_net_avoided_ghg_t'],'')
 def test_within_source_benchmarks_preserve_boundaries(self):
  rows={x['result_id']:x for x in read('outputs/limitation_benchmark_results.csv')}
  self.assertEqual(len(rows),8)
  for i in range(1,6):
   x=rows[f'Cihan_rate_shortfall_{i}'];self.assertIn('fault pressure increase',x['scope']);self.assertGreaterEqual(float(x['value']),35.4);self.assertLessEqual(float(x['value']),60.7)
  self.assertAlmostEqual(float(rows['Chong_compensated_power_intensity']['value']),.33444444444444443)
  self.assertGreater(float(rows['Musayev_proxy_gain']['value']),float(rows['Musayev_full_physics_gain']['value']))
  self.assertIn('Volumetric reference cancels',rows['Musayev_full_physics_gain']['scope'])
 def test_primary_manuscript_does_not_use_cross_study_score_as_main_result(self):
  text=(ROOT/'manuscript/Paper_1_draft.template.md').read_text()
  main,appendix=text.split('# Appendix A.',1)
  self.assertNotIn('{{PROXY_TABLE}}',main);self.assertIn('{{PROXY_TABLE}}',appendix)
  self.assertIn('not a completed regional lifecycle assessment',main)
  self.assertIn('do not optimise detailed dispatch globally',main)

if __name__=='__main__':unittest.main()
