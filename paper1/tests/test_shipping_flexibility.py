import importlib.util
from pathlib import Path
import unittest
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("shipping_flexibility", ROOT / "scripts/audit_shipping_flexibility.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ShippingFlexibilityChecks(unittest.TestCase):
    def test_optional_plan_lowers_objective_but_can_raise_another_metric(self):
        restricted = m.choose_plan([[100, 0], [0, 101]], [1, 1], .1, [False, True])
        expanded = m.choose_plan([[100, 0], [0, 101]], [1, 1], .1, [True, True])
        self.assertAlmostEqual(restricted["total"], 101)
        self.assertAlmostEqual(expanded["total"], 100)
        self.assertGreater(expanded["pv_cost"], restricted["pv_cost"])
        self.assertGreater(expanded["levelized"], restricted["levelized"])
        np.testing.assert_allclose(restricted["weights"], [0, 1])
        np.testing.assert_allclose(expanded["weights"], [1, 0])

    def test_buffer_lp_matches_independent_gap_mass_bound(self):
        for capacity, steps, demand in [(20, 10, 2), (20, 12, 2), (24, 12, 2), (0, 3, 1)]:
            result = m.gap_shortfall(capacity, [0] * steps, [demand] * steps)
            self.assertAlmostEqual(result["unmet"], max(0, steps * demand - capacity))
            self.assertGreaterEqual(min(result["inventory"]), -1e-10)
            self.assertLessEqual(max(result["inventory"]), capacity + 1e-10)

    def test_finance_units_and_invalid_domains(self):
        self.assertAlmostEqual(m.pv([1] * 30, .1), (1 - 1.1 ** -30) / .1)
        self.assertAlmostEqual(m.pv([1, 2, 3], 0), 6)
        with self.assertRaises(ValueError):
            m.pv([], .1)
        with self.assertRaises(ValueError):
            m.gap_shortfall(-1, [0], [1])
        with self.assertRaises(ValueError):
            m.choose_plan([[1, 2]], [1, 1], .1, [False])
        rows = {x["item"]: x for x in m.calculate(m.load_inputs())}
        self.assertEqual(rows["missing_Table1_label"]["value"], "z")
        self.assertEqual(rows["what_if_alternatives"]["value"], 12)
        self.assertEqual(rows["labelled_designs_total"]["value"], 15)


if __name__ == "__main__":
    unittest.main()
