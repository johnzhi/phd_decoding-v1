import unittest,sys,csv,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import reproduce
class ResearchChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.inputs={x['value_id']:x for x in reproduce.read_csv('analysis_inputs.csv')};cls.rows=reproduce.calculate()
 def result(self,metric,case):return next(x for x in self.rows if x['metric']==metric and x['case']==case)['value']
 def test_source_files_and_locators(self):
  a=reproduce.validate_sources();self.assertEqual(a['unique_publications'],92);self.assertEqual(a['pdf_files'],93)
 def test_provenance_closure_and_hold_exclusion(self):
  used={k for x in self.rows for k in x['input_ids'].split(';')}
  self.assertEqual(used,set(self.inputs));self.assertFalse(any('density' in k for k in used))
  for x in self.inputs.values():self.assertEqual(x['status'],'ACCEPTED_FOR_STATED_CONTEXT')
 def test_threshold_cancels_score_difference(self):
  rlo=float(self.inputs['retention_SW_A']['value']);rhi=float(self.inputs['retention_MW_A']['value']);elo=float(self.inputs['gwp_NL07']['value'])
  crossing=next(x['value'] for x in self.rows if x['metric']=='score_crossing_high_path_reported_intensity')
  self.assertAlmostEqual(rhi*(1-crossing/1000),rlo*(1-elo/1000),places=10)
  # Reference-case equality should require no extra storage; sign changes across the published high/low burden scenarios.
  self.assertAlmostEqual(self.result('required_storage_uplift_for_score_equality','NL07'),0)
  self.assertGreater(self.result('difference_in_stored_mass_minus_reported_GWP_score','NL15'),0)
  self.assertLess(self.result('difference_in_stored_mass_minus_reported_GWP_score','SM07'),0)
 def test_bog_units_and_denominator(self):
  # Independent explicit tonne/kg scaling of source Table6/TableA6 first case.
  expected=2412.4*1000/320400
  self.assertAlmostEqual(self.result('partial_process_emissions_intensity','1-1; N2=0.05 mol%'),expected)
  self.assertAlmostEqual(self.result('buffer_as_percent_of_ship','99'),102.4)
  self.assertAlmostEqual(self.result('buffer_as_percent_of_ship','100'),117.8)
 def test_outputs_match_current_inputs(self):
  saved=json.loads((ROOT/'outputs/calculated_results.json').read_text());self.assertEqual(saved,self.rows)
  self.assertEqual(sum(x['group']=='fleet' for x in self.rows),75)
  self.assertEqual(sum(x['group']!='fleet' for x in self.rows),49)
  self.assertTrue(all(math.isfinite(x['value']) for x in self.rows))
 def test_source_loss_correction_is_disclosed(self):
  text=(ROOT/'manuscript/Paper_1_draft.template.md').read_text()
  self.assertIn('double-count',text);self.assertIn('\\Delta L_{\\mathrm{inc}}',text)
  self.assertIn('Complete lifecycle net avoided GHG is not computed',text)
if __name__=='__main__':unittest.main()
