import csv,json,unittest,sys,math
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
def read(p):
 with (ROOT/p).open() as f:return list(csv.DictReader(f))
class MixedChecks(unittest.TestCase):
 def test_mixed_coarse_objective_contains_exclusive_feasible_modes(self):
  groups=defaultdict(dict)
  for x in read('outputs/mixed_solver_audit.csv'):groups[x['higher_distance_km'],x['partition']][x['mode']]=float(x['planned_partial_component_score_t'])
  self.assertEqual(len(groups),4)
  for modes in groups.values():self.assertGreaterEqual(modes['mixed']+.01,max(modes['short'],modes['long']))
 def test_milp_optimality_is_separate_from_detailed_optimality(self):
  a=json.loads((ROOT/'outputs/mixed_validation.json').read_text());self.assertEqual(a['annual_milp_cases'],12);self.assertEqual(a['optimal_solver_cases'],12);self.assertEqual(a['operational_reevaluations'],72);self.assertFalse(a['global_detailed_optimum']);self.assertFalse(a['complete_lca']);self.assertFalse(a['independent_storage_calibration'])
 def test_disjoint_groups_and_one_source_not_two_copies(self):
  rr=read('outputs/mixed_reservoir_plans.csv');groups=defaultdict(dict);annual=defaultdict(float);resource=defaultdict(float)
  for x in rr:
   k=x['case_id'];r=x['reservoir'];self.assertEqual(groups[k].setdefault(r,x['route']),x['route']);annual[k,x['year']]+=float(x['allocated_t']);resource[k,r]+=float(x['allocated_t'])
   self.assertLessEqual(float(x['allocated_t']),float(x['exogenous_envelope_t'])+.02)
   if int(x['year'])<int(x['readiness']):self.assertAlmostEqual(float(x['allocated_t']),0)
  self.assertTrue(all(len(x)==8 for x in groups.values()));self.assertTrue(all(x<=1e6+.02 for x in annual.values()))
  caps={x['reservoir']:float(x['capacity_mt'])*1e6 for x in read('data/supplement_reservoirs.csv')}
  self.assertTrue(all(m<=caps[r]+.02 for (k,r),m in resource.items()))
 def test_integer_voyage_flow_and_fuel_plan(self):
  plans=read('outputs/mixed_trip_plans.csv');totals=defaultdict(lambda:[0,0.])
  for x in plans:
   n=float(x['planned_trips']);self.assertEqual(n,int(n));self.assertLessEqual(n,float(x['annual_trip_limit']));self.assertLessEqual(float(x['planned_flow_t']),n*float(x['cargo_per_trip_t'])+.03);totals[x['case_id']][0]+=int(n);totals[x['case_id']][1]+=n*float(x['fuel_per_trip_kg'])
  for x in read('outputs/mixed_solver_audit.csv'):
   self.assertEqual(totals[x['case_id']][0],int(x['planned_trip_count']));self.assertAlmostEqual(totals[x['case_id']][1],float(x['planned_fuel_kg']),places=3)
 def test_reevaluation_conserves_common_source_and_uncredited_stock(self):
  for x in read('outputs/mixed_operational_comparisons.csv'):
   c=float(x['captured_t']);r=float(x['injected_t']);stock=float(x['final_inventory_t']);self.assertAlmostEqual(c-r-stock,0,places=3);self.assertLessEqual(c,float(x['planned_injection_t'])+.02);self.assertLessEqual(c,30e6+.02);self.assertEqual(x['complete_net_avoided_ghg_t'],'');self.assertLessEqual(float(x['maximum_short_active_hours']),8000+.001);self.assertLessEqual(float(x['maximum_long_active_hours']),8000+.001)
  for x in read('outputs/mixed_operational_annual.csv'):
   self.assertLessEqual(float(x['captured_t']),float(x['source_allocated_plan_t'])+.02);self.assertLessEqual(float(x['source_allocated_plan_t']),1e6+.02);self.assertAlmostEqual(float(x['captured_t'])+float(x['uncaptured_t']),1e6,places=4)
 def test_variable_source_schedule_does_not_create_capture_in_zero_year(self):
  from operational_model import Shuttle
  rr,meta=Shuttle([200000]*3,1000,source_tpa=[0,100000,0],fixed_fleet=1).run();self.assertEqual(rr[0]['captured_t'],0);self.assertEqual(rr[2]['captured_t'],0);self.assertLessEqual(sum(x['captured_t'] for x in rr),100000+.001);self.assertLess(meta['max_mass_balance_residual_t'],.001)
 def test_dispatch_comparison_preserves_default_and_hours(self):
  rows=read('outputs/dispatch_policy_controls.csv');self.assertEqual(len(rows),18);self.assertEqual({x['dispatch_policy'] for x in rows},{'index','earliest_window_end','least_active_hours'})
  for x in rows:
   self.assertLessEqual(float(x['max_active_hours']),8000+.001);self.assertLess(float(x['mass_residual_t']),.001)
   if x['dispatch_policy']=='index':self.assertAlmostEqual(float(x['injected_t']),float(x['default_injected_t']),places=3)
if __name__=='__main__':unittest.main()
