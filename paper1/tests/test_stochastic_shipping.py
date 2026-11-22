import importlib.util
from pathlib import Path
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('stochastic_shipping', ROOT / 'scripts/audit_stochastic_shipping.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)


class StochasticShippingChecks(unittest.TestCase):
    def test_minimum_direction_is_distinct_from_penalty_incentive(self):
        self.assertAlmostEqual(m.minimum_service_example(.99, True).x[0], 0)
        self.assertAlmostEqual(m.minimum_service_example(.99).x[0], .99)
        self.assertAlmostEqual(m.minimum_service_example(.99, True, 20).x[0], .99)

    def test_receiving_sign_difference_and_free_cyclic_complement(self):
        physical = m.tank_path(0, [2, 0], [0, 2])
        np.testing.assert_allclose(physical, [2, 0])
        self.assertLess(m.tank_path(0, [2, 0], [0, 2], True).min(), 0)
        np.testing.assert_allclose(m.tank_path(2, [2, 0], [0, 2], True), 2 - physical)
        self.assertEqual(physical[-1], 0)

    def test_conditional_speed_units_and_head_wave_component(self):
        self.assertAlmostEqual(m.speed_component(2000, 16, 95, 0), 12)
        self.assertAlmostEqual(m.speed_component(2e6, 16, 95, 0), 12)
        literal = m.speed_component(2000, 16, 95, 4)
        conditional = m.speed_component(2e6, 16, 95, 4)
        self.assertLess(literal, .1)
        self.assertGreater(conditional, 9)
        self.assertLess(conditional, 12)
        with self.assertRaises(ValueError):
            m.speed_component(0, 16, 95, 4)

    def test_annuity_and_two_explicit_scaling_exponents(self):
        self.assertAlmostEqual(m.pv_factor(.08, 25), (1 - 1.08 ** -25) / .08)
        self.assertAlmostEqual(m.pv_factor(0, 25), 25)
        for exponent in [.8, .85]:
            self.assertAlmostEqual(m.scaled_capital(3, exponent=exponent), 7.9)
        self.assertGreater(m.scaled_capital(.4, exponent=.8), m.scaled_capital(.4, exponent=.85))

    def test_reported_ratios_and_rounding_do_not_silently_harmonize(self):
        rows, speeds = m.calculate(m.load_inputs()); r = {x['item']: x['value'] for x in rows}
        self.assertEqual(r['representative_days'], 442)
        self.assertAlmostEqual(r['rate99_t_percent_ship'], 102.4)
        self.assertAlmostEqual(r['rate100_t_percent_ship'], 117.8)
        self.assertAlmostEqual(r['fuel_case_3_label_residual'], -.4)
        self.assertEqual(r['unit99_rounding_overlap_standard'], 1)
        self.assertEqual(r['unit99_rounding_overlap_printed'], 0)
        self.assertEqual(r['energy_rounding_overlap'], 1)
        self.assertEqual(r['last_percent_rounding_overlap'], 1)
        self.assertEqual(len(speeds), 78)

    def test_three_hour_port_mass_requires_duration_conversion(self):
        rate = 5000 / 12
        self.assertAlmostEqual(rate * 4 * 3, 5000)
        self.assertAlmostEqual(rate * 4, 5000 / 3)
        data = m.load_inputs()
        self.assertIsNone(data['missing']['scenario_probabilities_season_weights_and_slots'])


if __name__ == '__main__':
    unittest.main()
