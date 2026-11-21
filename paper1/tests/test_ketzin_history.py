"""Scientific boundaries of the Class2015 constitutive-component audit."""
import importlib.util
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('history', ROOT / 'scripts/audit_ketzin_history.py')
history = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(history)


class KetzinHistoryChecks(unittest.TestCase):
    def test_phase_law_keeps_printed_denominators_and_rejects_unreported_clipping(self):
        setup = history.load_inputs()['setup']
        wet, gas = history.phase_kr(.95, setup)
        self.assertAlmostEqual(wet, .71645816602122)
        self.assertLess(wet, setup['krw_eq'])
        self.assertAlmostEqual(gas, 0)
        wet, gas = history.phase_kr(.15, setup)
        self.assertEqual(wet, 0)
        self.assertAlmostEqual(gas, .85)
        for sw in (.149, .951, 1.0, float('nan')):
            with self.assertRaises(ValueError):
                history.phase_kr(sw, setup)

    def test_Kozeny_ratio_matches_dimensional_law_and_log_derivative(self):
        # Independent ratio of the conventional dimensional porosity factor.
        phi0, multiplier = .2, .5555
        factor = lambda phi: phi**3 / (1 - phi)**2
        expected = factor(phi0 * multiplier) / factor(phi0)
        self.assertAlmostEqual(history.kozeny_ratio(multiplier, phi0), expected)
        self.assertEqual(round(expected, 4), .1388)
        self.assertEqual(history.kozeny_ratio(1, phi0), 1)
        eps = 1e-5
        derivative = (math.log(history.kozeny_ratio(multiplier * math.exp(eps), phi0)) -
                      math.log(history.kozeny_ratio(multiplier * math.exp(-eps), phi0))) / (2 * eps)
        rows, _ = history.calculate(history.load_inputs())
        reported = {row['item']: row['value'] for row in rows}
        self.assertAlmostEqual(derivative, reported['case3_local_Kozeny_log_sensitivity'], places=8)
        for mult, phi in [(0, .2), (5, .2), (1, 0), (1, 1)]:
            with self.assertRaises(ValueError):
                history.kozeny_ratio(mult, phi)

    def test_literal_gradient_calendar_and_missing_observations_stay_unrepaired(self):
        data = history.load_inputs()
        rows, curve = history.calculate(data)
        values = {row['item']: row['value'] for row in rows}
        self.assertEqual(data['setup']['pressure_gradient_literal_Pa_m'], 1.14)
        self.assertIsNone(data['setup']['corrected_pressure_gradient'])
        self.assertLess(values['literal_gradient_implied_hydrostatic_density'], 1)
        self.assertEqual(values['calendar_elapsed_to_calibration_end'], 1285)
        self.assertEqual(values['calendar_inclusive_to_calibration_end'], 1286)
        self.assertEqual(values['reported_final_day_minus_calendar_elapsed'], 31)
        self.assertEqual(data['calendar']['forecast_end_as_printed'], '2014-05-26')
        self.assertEqual(values['date_at_zero_based_reported_day2193'], '2014-06-26')
        self.assertAlmostEqual(values['conditional_arrival_inverse_variance_weight_case3_over_case12'], .16)
        self.assertFalse(any('dissolved' in row['item'] for row in rows))
        self.assertTrue(all(entry['observed_days'] is None for entry in data['approachI_arrivals'] if entry['phase'] == 'dissolved'))
        self.assertEqual(len(curve), 324)

    def test_reading_and_constitutive_evaluation_do_not_close_native_models_or_sources(self):
        review = json.loads((ROOT / 'evidence/comprehensive_review/B1-15.json').read_text())
        self.assertEqual(review['overall_status'], 'incomplete')
        self.assertEqual(review['text_read_pages'], list(range(1, 11)))
        self.assertEqual(review['visually_inspected_pages'], list(range(1, 11)))
        self.assertEqual(len(review['visuals']), 10)
        printed = [ref for ref in review['references'] if ref['record_type'] == 'printed_bibliography']
        dependencies = [ref for ref in review['references'] if ref['record_type'] != 'printed_bibliography']
        self.assertEqual(len(printed), 27)
        self.assertEqual(len(dependencies), 8)
        self.assertTrue(all(ref['verification_status'] == 'unverified' for ref in review['references']))
        self.assertTrue(all(value is None for value in history.load_inputs()['missing'].values()))
        self.assertIsNone(history.load_inputs()['nearfield']['barrier_permeability'])
        self.assertEqual(history.load_inputs()['nearfield']['barrier_well_pair'], ['Ktzi201', 'Ktzi202'])


if __name__ == '__main__':
    unittest.main()
