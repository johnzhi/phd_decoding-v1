import importlib.util
from pathlib import Path
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('cooptimization_review', ROOT / 'scripts/audit_cooptimization_review.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class CooptimizationReviewChecks(unittest.TestCase):
    def test_screening_conservation_does_not_claim_selection_reproduction(self):
        data = m.load_inputs(); rows = m.calculate(data)
        residuals = [r['value'] for r in rows if r['item'].endswith('_residual')]
        self.assertEqual(len(residuals), 7)
        self.assertEqual(residuals, [0] * 7)
        self.assertIsNone(data['missing']['publisher_SI_queries_exclusion_matrix'])

    def test_independent_milp_separates_target_and_delivery_link(self):
        empty = m.schematic_milp()
        self.assertAlmostEqual(empty.fun, 0)
        unlinked = m.schematic_milp(3)
        self.assertAlmostEqual(unlinked.fun, 3)
        self.assertAlmostEqual(unlinked.x[3], 0)
        delivered = m.schematic_milp(3, True)
        # Independent enumeration: all three assets are required for positive
        # delivered flow; fixed costs20 plus three throughput costs of3.
        self.assertAlmostEqual(delivered.fun, 10 + 5 + 5 + 3 * 3)
        np.testing.assert_allclose(delivered.x, [1, 1, 1, 3, 3, 3])
        with self.assertRaises(ValueError):
            m.schematic_milp(6, True)

    def test_mass_is_invariant_under_equivalent_time_partition(self):
        self.assertAlmostEqual(m.cumulative_mass([3, 3], [2, 2]), m.cumulative_mass([3] * 4, [1] * 4))
        self.assertGreater(m.cumulative_mass([3] * 4, [1] * 4), 10)
        with self.assertRaises(ValueError):
            m.cumulative_mass([3], [0])

    def test_cost_time_basis_uses_discounted_cash_flows(self):
        expected = 100 + 6 * (1 - 1.08 ** -10) / .08
        self.assertAlmostEqual(m.present_value(100, 6, .08, 10), expected)
        self.assertAlmostEqual(m.present_value(100, 6, 0, 10), 160)
        with self.assertRaises(ValueError):
            m.present_value(100, 6, -1, 10)

    def test_information_comparator_is_not_static_robust_policy(self):
        self.assertEqual(m.robust_comparison([[0, 10], [10, 0]]), (10, 0))
        self.assertEqual(m.robust_comparison([[4, 4], [6, 6]]), (4, 4))
        with self.assertRaises(ValueError):
            m.robust_comparison([])

    def test_units_and_below_cap_runtime_are_not_false_conflicts(self):
        rows = {r['item']: r for r in m.calculate(m.load_inputs())}
        self.assertAlmostEqual(rows['figure8_aggregate_stock_rate_ratio']['value'], 48.75)
        self.assertAlmostEqual(rows['Iowa_length_conversion']['value'], 1107.228672)
        self.assertEqual(rows['Bogs_runtime_below_cap']['value'], 300)
        self.assertEqual(rows['toy_persistent_capacity_all_years']['value'], 1)
        self.assertEqual(rows['toy_event_only_capacity_all_years']['value'], 0)


if __name__ == '__main__':
    unittest.main()
