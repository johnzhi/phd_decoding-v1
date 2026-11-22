import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("matching_review", Path(__file__).parents[1] / "scripts/audit_matching_review.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class MatchingReviewChecks(unittest.TestCase):
    def test_oil_material_water_balance_and_mass_scaling(self):
        a = m.oil_material_mass(1000, 600, .4, .25, 10, 20)
        self.assertEqual(a, 186000)
        self.assertEqual(m.oil_material_mass(1000, 600, .4, .25, 20, 20), a - 6000)
        self.assertEqual(m.oil_material_mass(2000, 600, .4, .25, 20, 40), a * 2)

    def test_dissolved_mass_uses_density_weighted_fractions(self):
        self.assertEqual(m.dissolved_mass(1000, 1050, .02, 1000, .001), 20000)
        self.assertEqual(m.dissolved_mass(1000, 1000, .01, 1000, .01), 0)
        self.assertEqual(m.dissolved_mass(1000, 1000, .001, 1050, .02), -20000)

    def test_coal_mass_and_volume_units_close(self):
        a = m.coal_material_mass(1000, 2, 1000, .02, .1, .1)
        self.assertEqual(a, 32000)
        self.assertEqual(m.coal_material_mass(2000, 2, 1000, .02, .1, .1), 2 * a)
        self.assertEqual(m.pore_volume(1e6, 40, .15), 6e6)

    def test_entire_Shen_bracket_is_multiplied_by_density(self):
        zero = m.shen_literal_mass(1000, 600, .25, .4, 10, 20, 0, 0)
        water = m.shen_literal_mass(1000, 600, .25, .4, 10, 20, .02, 0)
        oil = m.shen_literal_mass(1000, 600, .25, .4, 10, 20, 0, .1)
        self.assertEqual(zero, 456000)
        self.assertAlmostEqual(water - zero, 600 * .02 * 240)
        self.assertAlmostEqual(oil - zero, 600 * .1 * .6 * 750)

    def test_molar_mass_unit_conversion_is_explicit_not_a_source_correction(self):
        self.assertAlmostEqual(m.molal_mass_kg(1000, .5, 44.01), 22.005)
        self.assertAlmostEqual(m.molal_mass_kg(2000, .5, 44.01), 44.01)

    def test_depth_pressure_alone_does_not_guarantee_pure_supercritical_state(self):
        cold = m.hydrostatic_screen(801, 10, 25)
        warm = m.hydrostatic_screen(801, 15, 25)
        self.assertGreater(cold["pressure_MPa_absolute"], 7.8)
        self.assertFalse(cold["pure_critical_pair_passes"])
        self.assertTrue(warm["pure_critical_pair_passes"])
        self.assertEqual(cold["pressure_MPa_absolute"], warm["pressure_MPa_absolute"])

    def test_interval_midpoint_is_not_identified_as_a_probability_median(self):
        self.assertEqual(m.weighted_median([121, 267, 413], [.8, .1, .1]), 121)
        self.assertEqual(m.weighted_median([121, 267, 413], [.1, .1, .8]), 413)
        self.assertEqual((121 + 413) / 2, 267)
        d = m.load_inputs(); checks, intervals, phases = m.calculate(d)
        values = {r["item"]: r["value"] for r in checks}
        self.assertEqual(values["cement_low_table_over_body"], 10)
        self.assertEqual(values["cement_high_table_over_body"], 10)
        self.assertGreater(values["Fig3_country_share_sum"], 100)
        self.assertTrue(all(abs(r["midpoint_minus_Fig10"]) <= .5 for r in intervals))
        self.assertEqual(len(phases), 6)

    def test_invalid_domains_and_negative_phase_volumes_are_rejected(self):
        with self.assertRaises(ValueError): m.pore_volume(1e6, 40, 15)
        with self.assertRaises(ValueError): m.oil_material_mass(1000, 600, .1, .5, 1000, 0)
        with self.assertRaises(ValueError): m.coal_material_mass(1000, 2, 1000, .02, .8, .3)
        with self.assertRaises(ValueError): m.shen_literal_mass(1000, 600, .25, .4, 1000, 0, .02, .1)
        with self.assertRaises(ValueError): m.weighted_median([1, 2], [0, 0])


if __name__ == "__main__":
    unittest.main()
