"""Unit/time/reference-flow checks for the scoped B2-13 reconstruction."""
import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location("transport_audit", Path(__file__).parents[1] / "scripts/audit_prospective_transport.py")
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


class ProspectiveTransportTests(unittest.TestCase):
    def test_heel_returns_and_mass_closes(self):
        r = m.tank_balance(9.2, 20.7, .04)
        self.assertAlmostEqual(r["full_t"] - r["returned_t"], r["delivered_t"])
        self.assertAlmostEqual(r["heel_t"] + r["delivered_t"], 20.7)
        self.assertAlmostEqual(r["delivered_t"], 19.872)
        self.assertAlmostEqual(r["circulated_CO2_per_delivered_t"], 1 / .96)

    def test_constant_rate_fractional_crossing_and_scale_invariance(self):
        t, rows = m.first_payback([8] * 5, [2] * 5, 13)
        self.assertAlmostEqual(t, 13 / 6)
        self.assertLess(rows[1]["net_saving_after_construction"], 0)
        self.assertGreater(rows[2]["net_saving_after_construction"], 0)
        scaled, _ = m.first_payback([80] * 5, [20] * 5, 130)
        self.assertAlmostEqual(t, scaled)

    def test_no_crossing_is_horizon_specific(self):
        self.assertIsNone(m.first_payback([2] * 4, [3] * 4, 1)[0])
        self.assertIsNone(m.first_payback([8] * 2, [2] * 2, 13)[0])
        self.assertAlmostEqual(m.first_payback([8] * 3, [2] * 3, 13)[0], 13 / 6)

    def test_first_crossing_does_not_guarantee_lasting_benefit(self):
        t, rows = m.first_payback([8, 0, 0], [0, 8, 8], 4)
        self.assertEqual(t, .5)
        self.assertLess(rows[-1]["net_saving_after_construction"], 0)
        self.assertEqual(m.first_payback([1], [1], 0)[0], 0)

    def test_annual_interpolation_and_hold_are_distinct_from_continuous_integral(self):
        old = m.annual_interpolation([2040, 2042], [10, 6], 2040, 2)
        self.assertEqual(old, [10, 8])
        t, _ = m.first_payback(old, [2, 2], 12)
        self.assertAlmostEqual(t, 1 + 4 / 6)
        # Continuous linear-rate integration gives a different crossing.
        self.assertNotAlmostEqual(t, (8 - (64 - 48) ** .5) / 2)

    def test_percent_budget_and_tkm_units(self):
        low = m.sector_allocation(70, 1800, .6)
        high = m.sector_allocation(70, 1800, 1.9)
        self.assertAlmostEqual(low, .0233333333333)
        self.assertAlmostEqual(high, .0738888888889)
        self.assertGreater(.075, high)
        # 4g/tkm x 100km = .4kg/t; 0.7Gt/y gives .28Mt/y.
        self.assertAlmostEqual((4 * 100 / 1000) * .7e9 / 1e9, .28)

    def test_source_graphics_corroborated_without_creating_native_impacts(self):
        data = m.load_inputs()
        checks, switches, ranks, annual = m.calculate(data)
        self.assertEqual(len(switches), 66)
        self.assertEqual(sum(r["finite"] for r in switches), 49)
        self.assertEqual(sum(not r["finite"] for r in switches), 17)
        self.assertEqual(len(ranks), 272)
        self.assertTrue(all(r["absolute_impact"] == "" for r in ranks))
        self.assertTrue(all(r["status"] == "analyst_example_not_author_case" for r in annual))
        values = {r["item"]: r["value"] for r in checks}
        self.assertEqual(values["offshore_dense10_first_categories"], 14)
        self.assertEqual(values["electric_truck_worse_than_hydrogen_truck"], 11)
        self.assertIsNone(data["missing_native"]["licensed_ecoinvent"])
        self.assertIsNone(data["missing_native"]["capture_heat_GJ_t"])

    def test_invalid_domains_reject_before_comparison(self):
        for fraction in [-.1, 1, float("nan")]:
            with self.assertRaises(ValueError):
                m.tank_balance(9.2, 20.7, fraction)
        for args in [([1], [1, 2], 1), ([float("nan")], [1], 1), ([1], [1], -1)]:
            with self.assertRaises(ValueError):
                m.first_payback(*args)
        with self.assertRaises(ValueError):
            m.annual_interpolation([2040, 2040], [1, 2], 2040, 1)
        with self.assertRaises(ValueError):
            m.annual_interpolation([2040, 2045], [1, 2], 2039, 2)
        with self.assertRaises(ValueError):
            m.sector_allocation(70, 0, 1.9)


if __name__ == "__main__":
    unittest.main()
