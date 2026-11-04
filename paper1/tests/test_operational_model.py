import unittest,sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import operational_model as model
class OperationalChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  _,_,cls.I=model.service('SW-A');cls.p=model.parameters();cls.annual,cls.meta=model.Shuttle(cls.I,1000).run()
 def test_all_registered_parameters_have_primary_locators(self):
  for x in model.read('data/operational_parameters.csv'):
   pages=json.loads((ROOT/'evidence/pages'/f"{x['study_id']}.json").read_text())
   self.assertIn(x['source_token'],pages[int(x['pdf_page'])-1]);self.assertTrue(x['scope_note'])
 def test_source_fleet_table_reproduced_without_prose_unit_repair(self):
  x=model.validate_fleet();self.assertEqual(len(x),75);self.assertTrue(all(r['match'] for r in x))
 def test_closed_source_balance_and_inventory_credit(self):
  C=R=0.
  for i,x in enumerate(self.annual):
   C+=x['captured_t'];R+=x['injected_t']
   self.assertAlmostEqual(x['captured_t']-x['injected_t'],x['inventory_close_t']-x['inventory_open_t'],places=4)
   self.assertLessEqual(x['injected_t'],self.I[i]+1e-4);self.assertGreaterEqual(x['uncaptured_t'],-1e-4)
  self.assertAlmostEqual(C-R,self.meta['final_inventory_t'],places=4)
  self.assertGreater(self.meta['final_heel_t'],0);self.assertGreaterEqual(self.meta['final_inventory_t'],self.meta['final_heel_t'])
 def test_calendar_buffers_and_fuel_integral(self):
  self.assertLessEqual(self.meta['max_export_inventory_t'],self.meta['buffer_capacity_t']+1e-4);self.assertLessEqual(self.meta['max_import_inventory_t'],self.meta['buffer_capacity_t']+1e-4)
  F=self.p['fuel_rate_40000']*40000/1000
  for x in self.annual:
   self.assertLessEqual(x['max_active_hours_one_ship'],self.p['operating_hours']+1e-4)
   self.assertAlmostEqual(x['fuel_kg'],x['active_vessel_hours']*F,places=3)
 def test_all_saved_grid_rows_conserve_mass_and_respect_limits(self):
  service_cache={};Q=sum(float(x['co2_rate_mtpa']) for x in model.read('data/supplement_sources.csv'))*1e6
  for x in model.read('outputs/operational_annual.csv'):
   key=(x['path'],x['static_policy'],x['rounding_case'])
   if key not in service_cache:
    _,fixed,dynamic=model.service('SW-A' if x['path']=='lower_service' else 'MW-A',x['static_policy'],x['rounding_case']);service_cache[key]=(fixed,dynamic)
   I=service_cache[key][1 if x['variant'] in ['B1','B3'] else 0][int(x['year'])-2027]
   self.assertLessEqual(float(x['injected_t']),I+.001)
   self.assertLessEqual(float(x['captured_t']),Q+.001)
   self.assertAlmostEqual(float(x['captured_t'])-float(x['injected_t']),float(x['inventory_close_t'])-float(x['inventory_open_t']),places=3)
   if x['active_utilisation']:self.assertLessEqual(float(x['active_utilisation']),1+1e-8)
   if x['max_active_hours_one_ship']:self.assertLessEqual(float(x['max_active_hours_one_ship']),self.p['operating_hours']+1e-4)
 def test_zero_source_has_zero_flow_fuel_and_credit(self):
  a,_=model.Shuttle(self.I,1000,source_tpa=0).run();b,_=model.continuous(self.I,1000,source_tpa=0)
  for x in a+b:self.assertEqual(x['captured_t'],0);self.assertEqual(x['injected_t'],0);self.assertEqual(x['fuel_kg'],0)
 def test_static_proxies_preserve_nominal_profile_total(self):
  for s in ['SW-A','MW-A']:
   for policy in ['aggregate_mean','ready_mean']:
    _,fixed,dynamic=model.service(s,policy);self.assertAlmostEqual(sum(fixed),sum(dynamic),places=5)
 def test_equal_injection_control_and_uncomputed_ghg(self):
  controls=model.read('outputs/operational_controls.csv')
  equal=[x for x in controls if x['control']=='B3 equal-injection control'];self.assertEqual(len(equal),2)
  for x in equal:self.assertEqual(x['target_reached'],'True');self.assertAlmostEqual(float(x['additional_injected_t']),0,places=3)
  for x in model.read('outputs/operational_comparisons.csv'):
   self.assertEqual(x['net_avoided_ghg_t'],'')
   self.assertAlmostEqual(float(x['differential_uninventoried_burden_allowance_tco2e']),float(x['additional_injected_t'])-float(x['additional_ship_combustion_co2_t']),places=5)
 def test_extra_vessel_and_calendar_can_change_comparison_sign(self):
  # A regression guard against reporting an unsupported robust route preference.
  c=[x for x in model.read('outputs/operational_controls.csv') if x['control']=='B3 one-vessel structural control' and x['higher_distance_km']=='10000']
  self.assertGreater(float(next(x for x in c if x['fleet_margin_each_route']=='0')['uninventoried_allowance_t']),0)
  self.assertLess(float(next(x for x in c if x['fleet_margin_each_route']=='1')['uninventoried_allowance_t']),0)
 def test_design_adequacy_targets_and_interaction_identity(self):
  for x in model.read('outputs/operational_design_adequacy.csv'):self.assertEqual(x['design_target_met'],'True');self.assertGreaterEqual(float(x['selected_injected_t']),float(x['required_injected_t'])-1e-4)
  results=model.read('outputs/operational_comparisons.csv');contrasts=model.read('outputs/operational_contrasts.csv')
  fields=['group','size_m3','higher_distance_km','static_policy','availability_calendar','rounding_case']
  for row in contrasts:
   rr={x['variant']:float(x['differential_uninventoried_burden_allowance_tco2e']) for x in results if all(x[k]==row[k] for k in fields)}
   self.assertAlmostEqual(float(row['two_factor_interaction_t']),rr['B3']-rr['B2']-rr['B1']+rr['B0'],places=5)
if __name__=='__main__':unittest.main()
