import importlib.util
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('audit_decatur_monitoring', ROOT / 'scripts/audit_decatur_monitoring.py')
decatur = importlib.util.module_from_spec(spec)
spec.loader.exec_module(decatur)


class DecaturMonitoringChecks(unittest.TestCase):
    def test_analyst_nrms_is_scale_invariant_and_does_not_assign_CO2_mass(self):
        a = [1, -1, 2, -2]
        b = [1.1, -.9, 2.2, -1.8]
        self.assertAlmostEqual(decatur.conventional_nrms_percent(a, b), decatur.conventional_nrms_percent([7*x for x in a], [7*x for x in b]))
        self.assertEqual(decatur.conventional_nrms_percent(a, a), 0)
        self.assertEqual(decatur.conventional_nrms_percent(a, [-x for x in a]), 200)
        for percent in (15, 20):
            gain = decatur.gain_for_nrms_example(percent)
            self.assertAlmostEqual(decatur.conventional_nrms_percent(a, [gain*x for x in a]), percent)
        for x, y in [([], []), ([0], [0]), ([1], [1, 2]), ([1], [math.nan])]:
            with self.assertRaises(ValueError):
                decatur.conventional_nrms_percent(x, y)
        self.assertIsNone(decatur.load_inputs()['VSP']['exact_NRMS_formula_and_processing'])

    def test_cumulative_milestones_are_differenced_and_goal_is_not_service(self):
        rows = {row['item']: row for row in decatur.calculate(decatur.load_inputs())}
        self.assertEqual(rows['VSP_monitor_1_to_2_mass_increment']['value'], 359000)
        self.assertEqual(rows['VSP_monitor_2_to_3_mass_increment']['value'], 297000)
        self.assertAlmostEqual(rows['reported_injected_fraction_of_goal']['value'], .9253)
        self.assertEqual(rows['goal_minus_reported_injection']['value'], 74700)
        self.assertIn('TARGET', rows['nominal_goal_rate']['unit'])
        self.assertIsNone(decatur.load_inputs()['injection']['exact_start_day'])
        self.assertIsNone(decatur.load_inputs()['missing']['maximum_annual_service_and_retained_fraction'])

    def test_literal_port_and_array_conflicts_are_not_replaced_by_candidates(self):
        data = decatur.load_inputs()
        zone4 = data['pressures'][3]
        self.assertEqual(zone4['prose_depth_m'], 2128)
        self.assertEqual(zone4['figure4_depth_ft'], 6838)
        rows = {row['item']: row['value'] for row in decatur.calculate(data)}
        self.assertLess(rows['zone4_figure_candidate_minus_prose'], -40)
        self.assertEqual(rows['zone4_prose_minus_figure_depth_ft'], 144)
        self.assertIsNone(data['pressure_plot']['gauge_or_absolute'])
        self.assertIsNone(data['pressure_plot']['rate_plot_axis_or_transform'])
        self.assertIsNone(data['microseismic']['verified_array_configuration'])
        self.assertNotEqual(data['microseismic']['initial_arrays'], data['microseismic']['results_arrays_as_printed'])

    def test_monitoring_reading_does_not_verify_originals_or_native_models(self):
        review = json.loads((ROOT / 'evidence/comprehensive_review/B1-16.json').read_text())
        self.assertEqual(review['overall_status'], 'incomplete')
        self.assertEqual(review['text_read_pages'], list(range(1, 13)))
        self.assertEqual(review['visually_inspected_pages'], list(range(1, 13)))
        self.assertEqual(len(review['visuals']), 7)
        self.assertTrue(all(equation['id'].startswith('A') for equation in review['equations']))
        self.assertEqual(sum(ref['record_type'] == 'printed_bibliography' for ref in review['references']), 6)
        self.assertTrue(all(ref['verification_status'] == 'unverified' for ref in review['references']))
        self.assertTrue(all(value is None for value in decatur.load_inputs()['missing'].values()))


if __name__ == '__main__':
    unittest.main()
