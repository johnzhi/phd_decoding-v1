import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("zonal", Path(__file__).parents[1] / "scripts/audit_zonal_pairing.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ZonalPairingChecks(unittest.TestCase):
    def test_angular_cells_have_latitude_dependent_area(self):
        equator = m.spherical_cell(0, .01)
        northern = m.spherical_cell(50, .01)
        self.assertGreater(equator["area_km2"], 1)
        self.assertLess(northern["area_km2"], 1)
        self.assertAlmostEqual(equator["height_km"], northern["height_km"])
        self.assertAlmostEqual(m.spherical_cell(-50, .01)["area_km2"], northern["area_km2"])
        self.assertAlmostEqual(m.spherical_cell(0, .02)["area_km2"] / equator["area_km2"], 4, places=6)

    def test_interpolation_does_not_identify_unobserved_field(self):
        for spacing in [20, 50]:
            rows = m.unresolved_field(spacing)
            self.assertEqual(rows[0]["alternative_field"], rows[0]["linear_interpolant"])
            self.assertAlmostEqual(rows[-1]["alternative_field"], rows[-1]["linear_interpolant"])
            self.assertEqual(rows[spacing // 2]["alternative_field"], 2)
            self.assertTrue(all(r["linear_interpolant"] == 1 for r in rows))

    def test_candidate_coverage_is_distinct_from_shared_service(self):
        result = m.shared_sink([1, 1], [1, 2], 1)
        self.assertEqual(result["geographically_eligible_percent"], 100)
        self.assertEqual(result["served_percent"], 50)
        self.assertAlmostEqual(result["disclosed_cost"], 1)
        self.assertEqual(result["flows"], [1, 0])
        self.assertEqual(m.shared_sink([1, 1], [1, 2], 0)["served_percent"], 0)
        self.assertEqual(m.shared_sink([1, 1], [1, 2], 2)["served_percent"], 100)

    def test_flow_and_cost_scale_without_changing_service_fraction(self):
        small = m.shared_sink([1, 1], [1, 2], 1)
        large = m.shared_sink([1000, 1000], [1, 2], 1000)
        self.assertEqual(small["served_percent"], large["served_percent"])
        self.assertAlmostEqual(large["disclosed_cost"], 1000 * small["disclosed_cost"])

    def test_source_rounding_and_denominators_stay_explicit(self):
        data = m.load_inputs(); checks, _, _, _ = m.calculate(data)
        values = {r["item"]: r["value"] for r in checks}
        self.assertAlmostEqual(values["Table2_sum_minus_total"], .1)
        self.assertTrue(values["Table2_conditional_rounding_overlap"])
        self.assertGreater(values["rounding_upper_below_59_lower"], 2)
        self.assertAlmostEqual(values["conditional_capture_difference"], 272)
        self.assertAlmostEqual(values["conditional_capture_after_removing_captive"], 7304.985)
        self.assertAlmostEqual(values["Table3_theoretical_sum_residual"], 0)
        self.assertGreater(values["matched_300km_captured_percent"], values["matched_300km_gross_emission_percent"])
        self.assertIsNone(data["capacities_table"]["annual_pressure_constrained_field_service"])
        self.assertIsNone(data["missing_native"]["SM1"])

    def test_invalid_inputs_fail_before_comparison(self):
        with self.assertRaises(ValueError): m.fraction_percent(1, 0)
        with self.assertRaises(ValueError): m.spherical_cell(90, .01)
        with self.assertRaises(ValueError): m.spherical_cell(30, -1)
        with self.assertRaises(ValueError): m.unresolved_field(0)
        with self.assertRaises(ValueError): m.shared_sink([1, 1], [1], 1)
        with self.assertRaises(ValueError): m.shared_sink([1], [1], -1)
        with self.assertRaises(ValueError): m.shared_sink([float("nan")], [1], 1)


if __name__ == "__main__":
    unittest.main()
