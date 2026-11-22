import importlib.util
import math
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("pressure_global", Path(__file__).parents[1] / "scripts/audit_pressure_limited_global.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class PressureLimitedGlobalChecks(unittest.TestCase):
    def test_both_lambert_branches_solve_the_stated_dimensionless_relation(self):
        roots = [m.dimensionless_lambert_rate(1, 2, branch=b) for b in [0, -1]]
        self.assertNotAlmostEqual(roots[0]["scaled_rate"], roots[1]["scaled_rate"])
        self.assertTrue(all(abs(r["implicit_residual"]) < 1e-12 for r in roots))
        self.assertFalse(roots[0]["increasing_pressure_branch"])
        self.assertTrue(roots[1]["increasing_pressure_branch"])

    def test_reference_identity_requires_branch_context(self):
        self.assertAlmostEqual(m.dimensionless_lambert_rate(2, 2, branch=-1)["scaled_rate"], 1)
        self.assertNotAlmostEqual(m.dimensionless_lambert_rate(2, 2, branch=0)["scaled_rate"], 1)
        self.assertAlmostEqual(m.dimensionless_lambert_rate(.5, .5, branch=0)["scaled_rate"], 1)
        for branch in [0, -1]:
            self.assertAlmostEqual(m.dimensionless_lambert_rate(1, 1, branch=branch)["scaled_rate"], 1)

    def test_reference_rate_scales_without_creating_pressure_units(self):
        a = m.dimensionless_lambert_rate(1, 2, reference_rate=1)
        b = m.dimensionless_lambert_rate(1, 2, reference_rate=1000)
        self.assertAlmostEqual(b["rate"], 1000 * a["rate"])
        self.assertAlmostEqual(a["scaled_rate"], b["scaled_rate"])

    def test_conventional_cohesion_definition_is_distinct_from_undefined_source_factor(self):
        zero = m.pressure_example(50, 20, .6, 30, 0, 2)
        with_c = m.pressure_example(50, 20, .6, 30, 1, 2)
        self.assertAlmostEqual(zero["literal_shear_MPa"], zero["conventional_shear_MPa"])
        self.assertAlmostEqual(with_c["conventional_shear_MPa"] - zero["conventional_shear_MPa"], 1 / math.tan(math.pi / 6))
        self.assertAlmostEqual(with_c["literal_shear_MPa"] - zero["literal_shear_MPa"], math.cos(math.pi / 6) * math.sin(math.pi / 6))
        self.assertAlmostEqual(with_c["tensile_headroom_MPa"], 20)

    def test_mass_geometry_closes_and_retains_duration(self):
        a = m.cumulative_cylinder_diameter(125, 30, 25, .2, 50, 600)
        b = m.cumulative_cylinder_diameter(125, 80, 25, .2, 50, 600)
        mass = 25 * math.pi * (a["diameter_m"] / 2) ** 2 * .2 * 50 * 600
        self.assertAlmostEqual(mass / a["cumulative_mass_kg"], 1)
        self.assertAlmostEqual(b["diameter_m"] / a["diameter_m"], math.sqrt(80 / 30))
        split = m.cumulative_cylinder_diameter(125, 30, 100, .2, 50, 600)
        self.assertAlmostEqual(split["diameter_m"], a["diameter_m"] / 2)

    def test_source_designs_are_ceilings_without_native_pressure_rates(self):
        data = m.load_inputs(); checks, designs, roots, cylinders = m.calculate(data)
        self.assertEqual(len(designs), 12)
        self.assertTrue(all(r["native_pressure_limited_rate"] == "" for r in designs))
        self.assertEqual(designs[-1]["nominal_cell_footprint_km2"], 360000)
        self.assertEqual(designs[-1]["centre_hull_km2"], 324900)
        self.assertTrue(data["figure1"]["negative_injectivity_prefactor_present"])
        self.assertFalse(data["figure1"]["analyst_raw_MPa_application_permitted"])
        self.assertFalse(data["missing_native"]["commercial_data_redistribution_permission"])

    def test_reported_rate_and_site_well_arithmetic_retains_scenario_scope(self):
        data = m.load_inputs(); checks, _, _, _ = m.calculate(data)
        values = {r["item"]: r["value"] for r in checks}
        self.assertEqual(values["scenario123_implied_basins"], 248)
        self.assertEqual(values["M_projects_four_sites"], 18377)
        self.assertEqual(values["M_wells_nine_per_site"], 661572)
        self.assertLess(abs(values["unrestricted_M_80y_minus_quoted_rate"]), .5)
        self.assertGreater(values["M_well_analogue_share_of_petroleum"], 2 / 3 * 100)
        self.assertIsNone(data["well_analogues"]["scenarioM_site_count_horizon"])

    def test_invalid_domains_do_not_generate_basin_predictions(self):
        for args in [(4, 2), (-1, 2), (1, float("nan"))]:
            with self.assertRaises(ValueError): m.dimensionless_lambert_rate(*args)
        with self.assertRaises(ValueError): m.dimensionless_lambert_rate(1, 2, branch=1)
        with self.assertRaises(ValueError): m.pressure_example(20, 50, .6, 30, 1, 2)
        with self.assertRaises(ValueError): m.pressure_example(50, 20, .6, 90, 1, 2)
        with self.assertRaises(ValueError): m.cumulative_cylinder_diameter(125, 30, 0, .2, 50, 600)
        with self.assertRaises(ValueError): m.cumulative_cylinder_diameter(125, 30, 25, 1.1, 50, 600)


if __name__ == "__main__":
    unittest.main()
