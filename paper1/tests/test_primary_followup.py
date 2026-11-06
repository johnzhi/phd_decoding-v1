import csv,json,hashlib,unittest
from pathlib import Path
from decimal import Decimal
import fitz
ROOT=Path(__file__).resolve().parents[1]
def read(p):
 with (ROOT/p).open(encoding='utf-8-sig') as f:return list(csv.DictReader(f))

class PrimaryFollowupChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.M={x['batch_id']:x for x in json.loads((ROOT/'data/dataset9_manifest.json').read_text())}
  cls.V={x['value_id']:x for x in read('data/primary_followup_values.csv')}
 def test_primary_originals_and_zip_members_preserved(self):
  self.assertEqual(len(self.M),4);self.assertEqual(sum(x.get('pages',0) for x in self.M.values()),46)
  for x in self.M.values():
   self.assertEqual(hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest(),x['sha256'])
   for m in x.get('members',[]):self.assertEqual(hashlib.sha256((ROOT/m['path']).read_bytes()).hexdigest(),m['sha256'])
 def test_hundred_located_records_distinguish_native_and_visual_cells(self):
  self.assertEqual(len(self.V),100);visual=[]
  for sid in ['D9-02','D9-03','D9-04']:
   with fitz.open(ROOT/self.M[sid]['path']) as d:
    for x in [v for v in self.V.values() if v['document_id']==sid]:
     p=d[int(x['physical_page'])-1];bbox=fitz.Rect(json.loads(x['source_bbox']))
     self.assertTrue(p.rect.contains(bbox));self.assertEqual(x['visual_page_checked'],'True');self.assertEqual(x['use_as_calibrated_input'],'False')
     if x['source_mode']=='VISUALLY_CHECKED_RASTER_TABLE':visual.append(x['value_id'])
     else:self.assertIn(x['source_token'],p.get_text())
  self.assertEqual(len(visual),9)
 def test_seven_after_loading_trials_match_the_actual_table_cells(self):
  with fitz.open(ROOT/self.M['D9-02']['path']) as d:rows=d[4].find_tables().tables[0].extract()
  rr=read('data/excool_verified_loading_tests.csv');self.assertEqual(len(rr),7)
  for a,b in zip(rr,rows[1:]):
   self.assertEqual(a['date_as_printed'],b[0]);self.assertEqual(a['loaded_co2_raw'],b[3]);self.assertEqual(a['temperature_raw'],b[4]);self.assertEqual(a['pressure_raw'],b[5]);self.assertEqual(a['values_after_loading'],'True')
  self.assertEqual(rr[2]['pressure_raw'],'0.60')
 def test_header_dates_are_distinct_from_reported_table_month(self):
  h={x['report_issue']:x for x in read('data/tomakomai_primary_header_totals.csv')}
  self.assertEqual(h['201906']['header_as_of'],'2019-06-29');self.assertEqual(h['201906']['table_month'],'2019-05');self.assertEqual(h['201906']['overall_cumulative_t'],'261729.8');self.assertEqual(h['201906']['document_id'],'D9-04')
  self.assertEqual(h['201907']['header_as_of'],'2019-07-30');self.assertEqual(h['201907']['overall_cumulative_t'],'264193.1')
  with fitz.open(ROOT/self.M['D9-03']['path']) as d:self.assertNotIn('261,729.8',d[11].get_text())
 def test_formation_arithmetic_is_not_a_corrected_observation(self):
  c={x['result_id']:x for x in read('outputs/primary_followup_calculations.csv')}
  self.assertEqual(c['formation_labelled_delta']['value'],'1217.3');self.assertEqual(c['formation_labelled_discrepancy']['value'],'98.1');self.assertEqual(c['June29_header_minus_May_label']['value'],'1315.4');self.assertEqual(c['June_formation_sum_minus_June29_header']['value'],'0.1')
  self.assertEqual(c['hypothetical_May_Moebetsu']['value'],'260316.2');self.assertIn('HYPOTHESIS_ONLY_NOT_OBSERVED',c['hypothetical_May_Moebetsu']['scope'])
  for x in c.values():self.assertTrue(set(x['input_ids'].split(';'))<=set(self.V))
  obs=read('data/tomakomai_primary_injection_tables.csv');may=next(x for x in obs if x['month']=='2019-05' and x['formation']=='Moebetsu');self.assertEqual(may['cumulative_as_labelled_t'],'260414.4')
 def test_monthly_means_retain_depth_and_unverified_pressure_reference(self):
  rows=read('data/tomakomai_primary_well_means.csv');self.assertEqual(len(rows),10)
  moe={x['month']:x for x in rows if x['well_id']=='Moe_injector'}
  self.assertEqual(moe['2019-06']['average_pressure_mpa'],'9.64');self.assertEqual(moe['2019-06']['average_temperature_c'],'41.3');self.assertEqual(moe['2019-05']['average_temperature_c'],'43.9')
  self.assertTrue(all(x['reported_depth_m']=='930' for x in moe.values()));self.assertTrue(all(x['depth_reference']=='UNSPECIFIED_AS_PRINTED' for x in rows));self.assertTrue(all('unspecified' in x['pressure_reference'] for x in rows))
 def test_only_retained_primary_sources_upgrade_the_compilation(self):
  rows=read('data/partial_compilation_values.csv')
  self.assertEqual(sum(x['status'].startswith('PRIMARY_VALUE_VERIFIED') for x in rows),33);self.assertEqual(sum(x['status'].startswith('DERIVED_FROM_VERIFIED') for x in rows),2);self.assertEqual(sum(x['status'].startswith('SUPPLIED_TRANSCRIPTION') for x in rows),25)
  audit=read('data/verification_package_status_audit.csv');self.assertEqual(len(audit),9);self.assertEqual(sum(x['local_status']=='NOT_LOCALLY_VERIFIED' for x in audit),6)
  energy=read('data/tomakomai_capture_energy_leads.csv');self.assertTrue(all(x['status'].startswith('SUPPLIED_TRANSCRIPTION') and x['model_used']=='False' for x in energy))
  s=json.loads((ROOT/'outputs/primary_followup_summary.json').read_text())
  for k in ['formation_label_issue_resolved','monthly_pressure_reference_verified','native_telemetry_received','model_inputs_or_optimisation_results_changed','complete_lca']:self.assertFalse(s[k])
 def test_source_precision_rounding_narrows_but_does_not_validate_phase(self):
  rows=read('outputs/excool_trial_property_checks.csv');self.assertEqual(sum(x['conditional_display_rounding_class']=='STRADDLES_SATURATION' for x in rows),3)
  below=[x for x in rows if x['conditional_display_rounding_class']=='ENTIRELY_BELOW_SATURATION'];self.assertEqual(len(below),1);self.assertEqual(below[0]['trial_id'],'EXCOOL_04')
  for x in rows:
   self.assertEqual(float(x['conditional_temperature_halfstep_c']),.05);self.assertEqual(float(x['conditional_pressure_halfstep_pa']),5000);self.assertEqual(x['pressure_basis_verified_as'],'MPaG');self.assertEqual(x['status'],'REFERENCE_CONSISTENCY_CHECK_NOT_MEASURED_PHASE')
 def test_voyage_endpoint_rates_reproduce_report_without_creating_fuel_or_vent_factors(self):
  rows=read('data/excool_reported_voyage_reference.csv');self.assertEqual(len(rows),3)
  self.assertEqual([x['approximate_hours'] for x in rows],['90','50','73'])
  for x in rows:
   self.assertLessEqual(abs(Decimal(x['reported_temperature_rise_c_per_hour'])-Decimal(x['reconstructed_temperature_rise_c_per_hour'])),Decimal('.0005'))
   self.assertLessEqual(abs(Decimal(x['reported_pressure_rise_mpag_per_hour'])-Decimal(x['reconstructed_pressure_rise_mpag_per_hour'])),Decimal('.00005'))
   self.assertEqual(x['reported_BOG_fate'],'No venting reported during this test; no onboard reliquefier');self.assertNotIn('fuel_kg',x);self.assertNotIn('annual_availability',x)
  c={x['result_id']:x for x in read('outputs/primary_followup_calculations.csv')};self.assertEqual(c['EXCOOL_reported_phase_hours_sum']['value'],'213');self.assertEqual(len(c),14)

if __name__=='__main__':unittest.main()
