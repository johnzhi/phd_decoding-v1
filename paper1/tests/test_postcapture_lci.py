import importlib.util
from pathlib import Path
import unittest
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("postcapture_lci", ROOT / "scripts/audit_postcapture_lci.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class PostcaptureLCIChecks(unittest.TestCase):
    def test_geometry_matches_independent_closed_cylinder_and_pressure_relation(self):
        d, h, t = 13.96, 30, .045
        result = m.cylinder(d, h, t)
        self.assertAlmostEqual(result["volume_m3"], np.pi * (d / 2) ** 2 * h)
        self.assertAlmostEqual(result["area_m2"], 2 * np.pi * (d / 2) * (h + d / 2))
        # Using the printed Table3 pressure as design differential pressure,
        # round the independent hoop-stress diameter at displayed precision.
        self.assertEqual(round(2 * t * 108.6 / .7, 2), d)
        self.assertAlmostEqual(result["thin_shell_volume_m3"] / result["area_m2"], t)
        self.assertEqual(7861 / (7861 / 1000), 1000)

    def test_scalarization_MILP_matches_independent_enumeration(self):
        costs = np.array([0, 6, 10]); emissions = np.array([10, 6, 0])
        for weight in np.linspace(0, 1, 21):
            result = m.choose_plan(costs, emissions, weight=float(weight))
            objective = (1 - weight) * costs + weight * emissions
            self.assertAlmostEqual(objective[result["selected"]], min(objective))
            self.assertNotEqual(result["selected"], 1)
        # The middle point is nondominated, but an epsilon constraint finds it.
        result = m.choose_plan(costs, emissions, emission_limit=6)
        self.assertEqual(result["selected"], 1)
        for i in [0, 2]:
            self.assertFalse(costs[i] <= costs[1] and emissions[i] <= emissions[1])

    def test_unnormalised_mass_units_change_choice_at_same_weight(self):
        tonne = m.choose_plan([100, 120], [10, 1], weight=.5)
        kg = m.choose_plan([100, 120], [10000, 1000], weight=.5)
        self.assertEqual(tonne["selected"], 0)
        self.assertEqual(kg["selected"], 1)
        # Threshold follows the independent cost/emission-difference equation.
        self.assertGreater(20 / (20 + 9), .5)
        self.assertLess(20 / (20 + 9000), .5)

    def test_active_release_matches_hour_integration_and_exposes_increment_difference(self):
        factor = .00286
        result = m.active_and_increment_fugitives([1] * 5, [6] * 5, factor)
        self.assertAlmostEqual(result["active_state_t"], 30 * 8760 * factor)
        self.assertAlmostEqual(result["activation_increment_t"], 6 * 8760 * factor)
        self.assertAlmostEqual(result["active_state_t"], 5 * result["activation_increment_t"])
        retired = m.active_and_increment_fugitives([1, 1, 0], [6] * 3, factor)
        self.assertAlmostEqual(retired["active_state_t"], 12 * 8760 * factor)
        self.assertAlmostEqual(retired["activation_increment_t"], 0)

    def test_source_quotes_hold_and_conditional_grid_do_not_create_native_GWP(self):
        data = m.load_inputs(); checks, designs, _ = m.calculate(data)
        self.assertEqual(len(designs), 28)
        self.assertEqual(sum(x["mode"] == "lorry" for x in designs), 3)
        self.assertTrue(all(x["author_GWP_kg_t"] == "" for x in designs))
        for row in designs:
            self.assertLessEqual(row["analyst_integer_trips_year"] * row["analyst_roundtrip_with_loading_h"],
                                 data["operation"]["ship_hours_year"] if row["mode"] == "ship" else data["operation"]["lorry_hours_year"])
            self.assertAlmostEqual(row["analyst_98percent_cargo_t_year"], .98 * row["analyst_full_cargo_t_year"])
        held = next(x for x in data["best_reported"] if x["case"] == "combined15")
        self.assertEqual(held["GWP_kg_t"], 39.2)
        self.assertTrue(held["status"].startswith("HOLD"))
        self.assertIsNone(data["liquefaction"]["native_duty_kWh_t"])
        self.assertEqual(data["geometry"]["steel_density_printed_unit"], "t/m3")
        self.assertEqual(data["appendix"]["storage_50kt_GHG_t"], 12027)
        self.assertEqual(data["tanks"]["GHG_low_t"][-1], 12567)

    def test_invalid_domains_fail_before_scientific_comparison(self):
        with self.assertRaises(ValueError):
            m.cylinder(0, 1, .1)
        with self.assertRaises(ValueError):
            m.choose_plan([1], [2], weight=1.1)
        with self.assertRaises(ValueError):
            m.choose_plan([1, 2], [1], weight=.5)
        with self.assertRaises(ValueError):
            m.choose_plan([1], [1])
        with self.assertRaises(ValueError):
            m.active_and_increment_fugitives([1], [0], .1)
        with self.assertRaises(ValueError):
            m.active_and_increment_fugitives([1], [1], float("nan"))


if __name__ == "__main__":
    unittest.main()
