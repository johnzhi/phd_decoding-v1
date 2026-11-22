"""Physical and accounting boundary checks for B3-07 component diagnostics."""
import importlib.util
from pathlib import Path
import math
import unittest

SPEC = importlib.util.spec_from_file_location('korea', Path(__file__).parents[1] / 'scripts/audit_korea_transport.py')
M = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)


class KoreaTransportTests(unittest.TestCase):
    def test_mass_calendar_and_compressor_ratio_rounding(self):
        self.assertTrue(math.isclose(M.mass_flow(1) * 365 * 86400, 1e9, rel_tol=1e-14, abs_tol=0))
        self.assertAlmostEqual(2800 / M.mass_flow(1), 88.3008)
        self.assertTrue(2.355 ** 5 < 73.8 < 2.365 ** 5)
        with self.assertRaises(ValueError):
            M.mass_flow(1, 0)

    def test_hydraulic_scaling_gravity_and_annular_mass(self):
        dp = M.pressure_drop(30, 100000, .3, 900, .02, 0)
        self.assertAlmostEqual(M.pressure_drop(60, 100000, .3, 900, .02, 0), 4 * dp)
        self.assertAlmostEqual(M.pressure_drop(30, 100000, .6, 900, .02, 0), dp / 32)
        self.assertLess(M.pressure_drop(0, 100000, .3, 900, 0, -150), 0)
        mass = M.pipe_mass(1000, 7850, .3, .01)
        annulus = math.pi * ((.3 + .02) ** 2 - .3 ** 2) / 4
        self.assertAlmostEqual(mass, annulus * 1000 * 7850)

    def test_train_scaling_is_conditional_and_power_is_kW(self):
        c10 = M.compressor_capital(10, 1, 73.8)
        c20 = M.compressor_capital(20, 1, 73.8)
        self.assertLess(c20, 2 * c10)
        self.assertAlmostEqual(M.compressor_capital(10, 2, 73.8), 2 * c10)
        self.assertAlmostEqual(M.pump_capital(1000), 1180000)
        self.assertAlmostEqual(M.pump_capital(1000, True), 8280000)

    def test_three_direct_delivery_windows_cannot_cover_long_cycle(self):
        # Necessary coverage bound if20h unloading is the only direct well-delivery window.
        cycle = M.roundtrip_hours(724, 15)
        self.assertGreater(cycle, 3 * 20)
        self.assertLess(3 * 20 / cycle, 1)
        # Five is a conditional mathematical minimum, not a recommended/native fleet design.
        self.assertEqual(math.ceil(cycle / 20), 5)
        self.assertGreater(5 * 20 / cycle, 1)

    def test_rounded_liquid_label_can_span_gas_and_liquid_states(self):
        rows = M.pure_state_rows(M.load_inputs())
        corners = [r for r in rows if r['kind'] == 'Figure4_rounding_corner']
        self.assertTrue(any(r['density_kg_m3'] < 100 for r in corners))
        self.assertTrue(any(r['density_kg_m3'] > 1000 for r in corners))
        # These are pure-fluid absolute-pressure diagnostics, not hydrate/solid validation.
        nominal = {r['label']:r for r in rows if r['kind'] == 'nominal_label'}
        self.assertGreater(nominal['main_ship_cargo']['density_kg_m3'], 1000)
        self.assertLess(nominal['compression_outlet']['density_kg_m3'], 500)


if __name__ == '__main__':
    unittest.main()
