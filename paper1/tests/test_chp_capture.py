import importlib.util
import json
from pathlib import Path
import unittest

from CoolProp.CoolProp import PhaseSI, PropsSI

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("chp_capture", ROOT / "scripts/audit_chp_capture.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class CHPCaptureChecks(unittest.TestCase):
    def test_annuity_repays_independently_discounted_capital(self):
        for rate, years in [(0, 25), (.075, 23), (.075, 25), (.1, 10)]:
            annual = 280000 * m.crf(rate, years)
            present = sum(annual / (1 + rate) ** t for t in range(1, years + 1))
            self.assertAlmostEqual(present, 280000, places=6)
        self.assertGreater(m.crf(.075, 23), m.crf(.075, 25))

    def test_kg_s_calibration_and_scale_economy(self):
        data = m.load_inputs()
        cost = m.capture_capex_EUR(3.6, data["capture_capex"])
        self.assertAlmostEqual(cost, 15520000)
        larger = m.capture_capex_EUR(36, data["capture_capex"])
        self.assertGreater(larger, cost)
        self.assertLess(larger / 36, cost / 3.6)

    def test_truck_volume_and_time_conservation(self):
        data = m.load_inputs()
        for distance in data["analyst"]["distances_km"]:
            row = m.truck_component(distance, 1000, .5, data["truck"], data["analyst"])
            # Total driving/loading hours for all continuous trips equal fleet*24h.
            hours = row["continuous_trips_per_day"] * (2 * distance / 50 + 1)
            self.assertAlmostEqual(hours, row["continuous_fleet"] * 24)
            self.assertAlmostEqual(row["continuous_trips_per_day"] * 33, 1000)
            self.assertAlmostEqual(row["volume_per_truck_day_m3"] * row["continuous_fleet"], 1000)
            self.assertGreaterEqual(row["ceil_fleet"] * row["volume_per_truck_day_m3"], 1000)
            self.assertLess((row["ceil_fleet"] - 1) * row["volume_per_truck_day_m3"], 1000)
            self.assertGreaterEqual(row["ceil_fleet_cost_EUR_m3"], row["continuous_cost_EUR_m3"])
            self.assertEqual(row["cost_EUR_t"], "")

    def test_utilization_affects_fixed_cost_without_changing_scaled_variable_rate(self):
        data = m.load_inputs()
        args = (50, 1000)
        full = m.truck_component(*args, 1, data["truck"], data["analyst"])
        half = m.truck_component(*args, .5, data["truck"], data["analyst"])
        quarter = m.truck_component(*args, .25, data["truck"], data["analyst"])
        self.assertAlmostEqual(quarter["continuous_cost_EUR_m3"] - half["continuous_cost_EUR_m3"],
                               2 * (half["continuous_cost_EUR_m3"] - full["continuous_cost_EUR_m3"]))
        self.assertEqual(full["continuous_fleet"], half["continuous_fleet"])

    def test_conditional_CO2_phase_bracket_does_not_supply_a_native_density(self):
        T = 248.15
        saturation = PropsSI("P", "T", T, "Q", 0, "HEOS::CO2")
        self.assertGreater(saturation, 16e5)
        self.assertLess(saturation, 17e5)
        self.assertEqual(PhaseSI("T", T, "P", 15e5, "HEOS::CO2"), "gas")
        self.assertEqual(PhaseSI("T", T, "P", 17e5, "HEOS::CO2"), "liquid")
        data = m.load_inputs()
        self.assertIsNone(data["truck"]["density_t_per_m3"])
        self.assertIsNone(data["utilities"]["cooling_quantity"])
        self.assertIsNone(data["utilities"]["MEA_quantity"])

    def test_invalid_finance_flow_and_truck_domains(self):
        data = m.load_inputs()
        for rate, years in [(-.1, 10), (float("nan"), 10), (.1, 0)]:
            with self.assertRaises(ValueError):
                m.crf(rate, years)
        for flow in [0, -1, float("inf")]:
            with self.assertRaises(ValueError):
                m.capture_capex_EUR(flow, data["capture_capex"])
        for distance, volume, cf in [(-1, 1, 1), (1, 0, 1), (1, 1, 0), (1, 1, 1.1)]:
            with self.assertRaises(ValueError):
                m.truck_component(distance, volume, cf, data["truck"], data["analyst"])

    def test_citation_asset_status_and_native_missing_inputs_remain_explicit(self):
        record = json.loads((ROOT / "evidence/comprehensive_review/B2-11.json").read_text())
        bibliography = json.loads((ROOT / "evidence/comprehensive_review_inputs/B2-11_bibliography.json").read_text())
        self.assertEqual(len(bibliography["entries"]), 48)
        self.assertEqual(bibliography["entries"][20]["pages"], [13, 14])
        self.assertEqual(record["references"][:48], [{k: v for k, v in entry.items() if k not in ["native_lines", "line_bboxes"]} for entry in bibliography["entries"]])
        self.assertEqual(record["overall_status"], "incomplete")
        self.assertEqual(sum(ref["verification_status"].startswith("primary_text_checked") for ref in record["references"]), 1)
        self.assertIn("not_reproduced", record["original_model_status"])


if __name__ == "__main__":
    unittest.main()
