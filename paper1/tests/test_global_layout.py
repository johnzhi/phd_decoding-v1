import importlib.util
import math
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("global_layout", Path(__file__).parents[1] / "scripts/audit_global_layout.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class GlobalLayoutChecks(unittest.TestCase):
    def test_deployment_endpoints_and_rising_segment(self):
        for u in [0, 1, 2, 3]:
            self.assertAlmostEqual(m.deployment(2020, 2020, u, .8), .8 * math.exp(-u * u))
            self.assertAlmostEqual(m.deployment(2050, 2020, u, .8), .8)
            values = [m.deployment(t, 2020, u, .8) for t in range(2020, 2051)]
            self.assertTrue(all(0 <= x <= .8 for x in values))
            self.assertEqual(values, sorted(values))

    def test_learning_doubling_and_capacity_units(self):
        for rate in [0, .1, .25, .5]:
            self.assertAlmostEqual(m.learning_cost(200, 100, 80, rate), 80 * (1 - rate))
            self.assertAlmostEqual(m.learning_cost(.2, .1, 80, rate), 80 * (1 - rate))
            self.assertAlmostEqual(m.learning_cost(400, 100, 80, rate), 80 * (1 - rate) ** 2)

    def test_lcoe_learning_identity_preserves_capacity_factor(self):
        case = m.load_inputs()["analyst_examples"]["lcoe"]
        result = m.lcoe_learning_example(case)
        self.assertAlmostEqual(result["learning_direct"], result["learning_Eq24"])
        equal_cf = dict(case, CF_doubled=case["CF_initial"])
        a = m.lcoe_learning_example(equal_cf)
        self.assertLess(result["doubled_USD_MWh"], a["doubled_USD_MWh"])
        self.assertAlmostEqual(result["doubled_USD_MWh"] * case["CF_doubled"], a["doubled_USD_MWh"] * case["CF_initial"])

    def test_avoided_and_captured_denominators_are_distinct(self):
        self.assertAlmostEqual(m.avoided_unit_cost(50, 90, .8, .1), 400 / 7)
        self.assertNotAlmostEqual(m.avoided_unit_cost(50, 90, .8, .1), 40 / .8)
        self.assertAlmostEqual(m.avoided_unit_cost(50, 90, .8, .1) * .7, 40)

    def test_lower_bound_lp_can_overcapture_with_negative_marginal_costs(self):
        case = m.load_inputs()["analyst_examples"]["lp"]
        expected = {0: 7, 55: 9, 95: 10}
        for oil, total in expected.items():
            lower = m.aggregate_lp(case, oil)
            exact = m.aggregate_lp(case, oil, exact_targets=True)
            self.assertAlmostEqual(lower["total_Mt"], total)
            self.assertAlmostEqual(exact["total_Mt"], 7)
            self.assertLessEqual(lower["objective_million_USD"], exact["objective_million_USD"] + 1e-8)
            self.assertGreaterEqual(lower["power_EOR_Mt"] + lower["power_saline_Mt"], 5)
            self.assertGreaterEqual(lower["nonpower_EOR_Mt"] + lower["nonpower_saline_Mt"], 2)
            self.assertLessEqual(lower["EOR_Mt"], 10)

    def test_source_accounting_and_conflicts_preserve_boundaries(self):
        data = m.load_inputs(); checks, curves, cases = m.calculate(data)
        v = {r["item"]: r["value"] for r in checks}
        self.assertEqual(v["target_from_IEA"], 92)
        self.assertEqual(v["sink_flow_sum"], 92)
        self.assertEqual(v["cluster_threshold_ratio"], 10)
        self.assertLess(v["eight_country_emission_share_rounding_upper"], 83.5)
        self.assertAlmostEqual(v["base_conditional_fixed_flow_benefit"], .4591125)
        self.assertAlmostEqual(v["capture_share_of_gross"], 4.45 / 8.2 * 100)
        self.assertAlmostEqual(v["saline_synthetic_mass"], 177500)
        self.assertEqual(len(curves), 21); self.assertEqual(len(cases), 6)
        self.assertIsNone(data["missing_native"]["annual_pressure_limited_service"])

    def test_infeasible_lp_is_not_misreported_as_a_layout(self):
        data = m.load_inputs()["analyst_examples"]["lp"]
        with self.assertRaises(ValueError):
            m.aggregate_lp(dict(data, source_limits_Mt=[1, 1]), 55)

    def test_invalid_domains_do_not_create_results(self):
        for args in [(2051, 2020, 1, .8), (2020, 2050, 1, .8), (2020, 2020, -1, .8), (2020, 2020, 1, 1.1)]:
            with self.assertRaises(ValueError): m.deployment(*args)
        for args in [(0, 100, 80, .2), (100, 100, 80, 1), (100, 100, 80, float("nan"))]:
            with self.assertRaises(ValueError): m.learning_cost(*args)
        with self.assertRaises(ValueError): m.avoided_unit_cost(50, 90, .1, .1)


if __name__ == "__main__":
    unittest.main()
