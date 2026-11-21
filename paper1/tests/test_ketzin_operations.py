import csv
import gzip
import importlib.util
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('operations', ROOT / 'scripts/audit_ketzin_operations.py')
operations = importlib.util.module_from_spec(spec)
spec.loader.exec_module(operations)


class KetzinOperationsChecks(unittest.TestCase):
    def test_upward_SI_march_matches_closed_form_with_partial_final_step(self):
        site = dict(site='analytical constant-density example', depth_m=2.5, temperature_C=30, pressure_bar=100)
        rows, status = operations.integrate_column(site, lambda p,t: (1000, 'liquid'), step_m=.3)
        expected = 100 - 1000 * 9.80665 * 2.5 / 1e5
        self.assertAlmostEqual(status['surface_pressure_bar'], expected)
        self.assertEqual(rows[-1]['depth_m'], 0)
        self.assertEqual(rows[-1]['temperature_C'], 8)
        self.assertAlmostEqual(operations.hydrostatic_upward_step(1e7, 1000, 80), 1e7 - 1000*9.80665*80)
        with self.assertRaises(ValueError):
            operations.hydrostatic_upward_step(1e4, 1000, 80)

    def test_phase_crossing_and_backend_ambiguity_cannot_be_marked_complete(self):
        site = dict(site='phase-closure example', depth_m=2.5, temperature_C=30, pressure_bar=50)
        rows, status = operations.integrate_column(site, lambda p,t: (1000, 'liquid' if p>=49.9e5 else 'gas'), step_m=.1)
        self.assertEqual(status['status'], 'blocked_unspecified_two_phase_closure')
        self.assertIsNone(status['surface_pressure_bar'])
        self.assertGreater(rows[-1]['depth_m'], 0)
        def ambiguous(p,t):
            raise ValueError('unknown mixture density')
        rows, status = operations.integrate_column(site, ambiguous)
        self.assertEqual(rows, [])
        self.assertEqual(status['status'], 'blocked_EOS_state')
        self.assertIsNone(status['surface_pressure_bar'])

    def test_reference_and_test_schedule_checks_preserve_missing_inputs(self):
        data = operations.load_inputs()
        checks = {row['item']:row for row in operations.source_checks(data)}
        self.assertEqual(operations.gauge_to_absolute(61), 62)
        self.assertEqual(data['measurement']['paper_approximate_BHP_increment_bar'], 2)
        self.assertEqual(checks['sensor_to_injection_reference_interval']['value'], 80)
        self.assertAlmostEqual(checks['isochronal_four_stage_injection_mass']['value'], 32.4)
        self.assertEqual(checks['four_cycle_duration']['value'], 56)
        self.assertEqual(checks['four_cycle_date_elapsed']['value'], 55)
        self.assertEqual(checks['5min_to_example5s_interval_ratio']['value'], 60)
        self.assertIsNone(data['logging_table'][0]['Ktzi201'])
        self.assertIsNone(data['plant']['actual_heat_and_power'])
        self.assertIsNone(data['tests']['native_fit_inputs'])
        self.assertIsNone(data['P300']['leakage_detection_limit'])

    def test_saved_columns_are_limited_and_numerically_refined_without_filling_Sleipner(self):
        result = json.loads((ROOT/'outputs/comprehensive_review/B1-17_reconciliation.json').read_text())
        self.assertFalse(result['full_native_models_reproduced'])
        self.assertFalse(result['accepted_inputs_changed'])
        self.assertEqual(result['software']['CoolProp'], '8.0.0')
        self.assertEqual(result['software']['EOS_BibTeX'], 'Span-JPCRD-1996')
        columns = {row['site']: row for row in result['columns']}
        self.assertEqual(columns['Sleipner']['status'], 'blocked_unspecified_two_phase_closure')
        self.assertIsNone(columns['Sleipner']['surface_pressure_bar'])
        for name in ('In Salah','Weyburn','Snovhit'):
            self.assertIn('completed', columns[name]['status'])
            self.assertGreater(columns[name]['surface_density_kg_m3'], columns[name]['bottom_density_kg_m3'])
            refinements = [r for r in result['refinement_checks'] if r['site']==name]
            self.assertTrue(all(abs(r['surface_difference_from_0_1m_bar'])<.002 for r in refinements))
        self.assertEqual(len(result['graphic_endpoint_checks']), 3)
        self.assertTrue(all(r['within_analyst_graphic_tolerance'] for r in result['graphic_endpoint_checks']))
        self.assertTrue(all(7.9<r['temperature_C']<8.3 for r in result['graphic_endpoint_checks']))
        with gzip.open(ROOT/'outputs/comprehensive_review/B1-17_columns.csv.gz','rt') as stream:
            profiles=list(csv.DictReader(stream))
        self.assertEqual(len(profiles), result['profile_rows'])
        last = {row['site']: row for row in profiles}
        self.assertGreater(float(last['Sleipner']['depth_m']), 0)
        self.assertTrue(all(float(last[name]['depth_m'])==0 for name in ('In Salah','Weyburn','Snovhit')))

    def test_source_reading_and_new_citation_support_do_not_close_underlying_chain(self):
        review=json.loads((ROOT/'evidence/comprehensive_review/B1-17.json').read_text())
        self.assertEqual(review['overall_status'], 'incomplete')
        self.assertEqual(review['text_read_pages'], list(range(1,12)))
        self.assertEqual(review['visually_inspected_pages'], list(range(1,12)))
        self.assertEqual(len(review['visuals']),10)
        self.assertEqual(sum(r['record_type']=='printed_bibliography' for r in review['references']),28)
        self.assertTrue(all(r['verification_status']=='unverified' for r in review['references']))
        edge=json.loads((ROOT/'evidence/comprehensive_review_inputs/B1-14_Liebscher2013_citation_check.json').read_text())
        self.assertEqual(edge['cited_study'],'B1-17')
        self.assertEqual(edge['targeted_pages'],[3,5])
        self.assertIn('not_disproved',edge['checks'][2]['result'])
        parent=json.loads((ROOT/'evidence/comprehensive_review/B1-14.json').read_text())
        reference=next(r for r in parent['references'] if r['id']=='R22')
        self.assertTrue(reference['verification_status'].startswith('primary_text_checked_partial_support'))
        self.assertEqual(parent['overall_status'],'incomplete')


if __name__ == '__main__':
    unittest.main()
