import unittest,csv,json,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import replay_budiarto_supplement as replay
class SupplementChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.audit=replay.validate();cls.annual=replay.rd('outputs/supplement_annual_replay.csv');cls.summary=replay.rd('outputs/supplement_scenario_summary.csv')
 def test_docx_tables_media_and_annotated_cells(self):
  self.assertEqual(self.audit['source_tables'],3);self.assertEqual(self.audit['embedded_figures'],10)
  self.assertEqual(self.audit['annual_grid_cells'],720);self.assertEqual(self.audit['printed_numeric_cells'],250);self.assertEqual(self.audit['blank_cells'],470)
 def test_source_horizon_matches_published_full_storage(self):
  # Independent sum of the native Table S1 values, using decimal arithmetic.
  source=sum(D(x['co2_rate_mtpa']) for x in replay.rd('data/supplement_sources.csv'))
  self.assertEqual(source,D('5.327'));self.assertEqual(source*D(30),D('159.81'))
  reservoirs=replay.rd('data/supplement_reservoirs.csv')
  self.assertEqual(sum(D(x['capacity_mt']) for x in reservoirs),D('537.4'))
 def test_rounding_preserved_instead_of_forced_mass_match(self):
  expected={'SW-A':D('152.8'),'MW-A':D('159.4'),'MW-D':D('159.5')}
  for x in self.summary:
   self.assertEqual(D(x['sum_printed_allocations_mt']),expected[x['scenario']])
   self.assertNotEqual(D(x['sum_printed_allocations_mt']),D(x['main_paper_cumulative_mt']))
   self.assertEqual(x['main_total_inside_conditional_rounding_envelope'],'True');self.assertEqual(x['allocated_before_estimated_start_count'],'0')
  first=next(x for x in self.annual if x['scenario']=='MW-A' and x['year']=='2027')
  self.assertEqual(D(first['sum_printed_allocations_mt']),D('5.4'))
  self.assertGreater(D(first['sum_printed_allocations_mt']),D(first['nominal_source_rate_mtpa']))
  grid=replay.rd('data/supplement_annual_injection.csv')
  self.assertTrue(all(x['reported_value_mtpa']=='' for x in grid if x['cell_status']=='BLANK_NOT_NUMERIC_ZERO'))
 def test_ledger_closure_and_capacity_output_distinction(self):
  new=replay.rd('data/supplement_values.csv');ledger=replay.rd('data/all_extracted_values.csv')
  self.assertEqual(len(new),352);self.assertEqual(len([x for x in ledger if x['Study ID']=='B4-06-S1']),352)
  self.assertEqual(len(ledger),1642)
  text=(ROOT/'manuscript/Paper_1_draft.template.md').read_text()
  self.assertIn('whereas the main paper\'s kr,t denotes the physical annual injection upper bound',text)
  self.assertIn('does not reproduce the original MILP',text)
if __name__=='__main__':unittest.main()
