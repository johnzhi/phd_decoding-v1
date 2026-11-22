import importlib.util
from pathlib import Path
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("risk_network", ROOT / "scripts/audit_risk_network.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class RiskNetworkChecks(unittest.TestCase):
    def test_five_atom_tail_equals_maximum_not_resolved_failure_frequency(self):
        p = [.2] * 5
        for losses in [[0, 1, 2, 3, 4], [10, 3, 7, 7, 1], [2] * 5]:
            self.assertAlmostEqual(m.discrete_cvar(losses, p, .95), max(losses))
            self.assertAlmostEqual(m.cvar_lp(losses, p, .95), max(losses))
        self.assertAlmostEqual(m.discrete_cvar([0, 1, 2, 3, 4], p, .5), 3.2)
        self.assertAlmostEqual(m.discrete_cvar([0, 1, 2, 3, 4], p, 0), 2)

    def test_tail_integral_matches_independent_linear_program(self):
        rng = np.random.default_rng(117200)
        for _ in range(12):
            losses = rng.uniform(-2, 20, 7)
            probabilities = rng.uniform(.01, 1, 7)
            probabilities /= probabilities.sum()
            for alpha in [0, .37, .8, .95]:
                self.assertAlmostEqual(m.discrete_cvar(losses, probabilities, alpha),
                                       m.cvar_lp(losses, probabilities, alpha), places=7)

    def test_invalid_domains_and_zero_probability_atoms(self):
        for losses, p, alpha in [([], [], .95), ([1], [.2], .95),
                                  ([1, 2], [-.1, 1.1], .5),
                                  ([float("nan")], [1], .5), ([1], [1], 1)]:
            with self.assertRaises(ValueError):
                m.discrete_cvar(losses, p, alpha)
        self.assertAlmostEqual(m.discrete_cvar([100, 7], [0, 1], 1 - 1e-15), 7)

    def test_annual_tail_sum_is_not_generally_horizon_tail(self):
        annual = [[10, 0], [0, 10]]
        separate = sum(m.discrete_cvar(loss, [.5, .5], .95) for loss in annual)
        totals = [sum(x) for x in zip(*annual)]
        self.assertAlmostEqual(separate, 20)
        self.assertAlmostEqual(m.cvar_lp(totals, [.5, .5], .95), 10)

    def test_printed_flow_replay_and_fractional_capacity_grid(self):
        rows, grid = m.calculate(m.load_inputs())
        r = {x["item"]: x["value"] for x in rows}
        self.assertAlmostEqual(r["reported_node_flow_residual"], 0)
        self.assertAlmostEqual(r["reported_arc_total"], 822.46)
        self.assertAlmostEqual(r["baseline_pipe_km"], 911.44)
        self.assertEqual(r["baseline_pipe_units"], 9)
        self.assertEqual(r["all_R1_pairwise_distances_longer"], 1)
        self.assertAlmostEqual(r["annual_target"], 40.95036)
        self.assertEqual(grid[0]["minimum_wells_best_sink"], 108)
        self.assertEqual(grid[-1]["minimum_wells_best_sink"], 180)
        self.assertAlmostEqual(grid[-1]["capacity_fraction"], .6)
        self.assertIsNone(m.load_inputs()["missing_inputs"]["pressure_and_resource_model"])

    def test_rounding_time_and_discounted_mass_boundaries(self):
        rows, _ = m.calculate(m.load_inputs())
        r = {x["item"]: x["value"] for x in rows}
        for label in ["pipe", "injectivity", "joint", "injectivity_vs_pipe"]:
            self.assertEqual(r[f"{label}_reported_percent_rounding_compatible"], 1)
        self.assertEqual(r["coal_rounding_compatible_8760h"], 1)
        self.assertEqual(r["coal_rounding_compatible_8000h"], 0)
        self.assertAlmostEqual(m.discounted_sum([1] * 20, .1), (1 - 1.1 ** -20) / .1)
        self.assertGreater(r["discounted_85_credit_all20y"], r["discounted_85_credit_first12y"])
        self.assertLess(r["discount_factor_sum_20y"], 20)


if __name__ == "__main__":
    unittest.main()
