"""Necessary economic/physical invariants for the B3-06 diagnostics."""
import importlib.util
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location('guangdong', Path(__file__).parents[1] / 'scripts/audit_guangdong_clusters.py')
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class GuangdongTests(unittest.TestCase):
    def test_discounted_cashflow_convention_and_literal_capital_are_distinct(self):
        rate, years = .12, 20
        closed = (1 - (1 + rate) ** -years) / rate
        self.assertAlmostEqual(M.annuity_factor(rate, years), closed)
        self.assertEqual(M.annuity_factor(0, 20), 20)
        self.assertEqual(M.annuity_factor(0, 20, True), 21)
        capital, opex, net = 100, 10, .8
        once = M.conventional_present_cost(capital, opex, rate, years) / (net * closed)
        repeated = (capital + opex) / net
        self.assertGreater(repeated, once)
        self.assertAlmostEqual(once - opex / net, capital / (net * closed))
        with self.assertRaises(ValueError):
            M.annuity_factor(-.1, 20)

    def test_avoided_mass_cannot_exceed_discounted_gross_capture(self):
        # Any nonnegative auxiliary-emission schedule reduces this zero-auxiliary upper bound.
        upper = M.gross_mass_bound(9, .12, 20)
        auxiliary = [0 if n % 2 else 1 for n in range(21)]
        actual = sum((9 - auxiliary[n]) / 1.12 ** n for n in range(21))
        self.assertLessEqual(actual, upper)
        self.assertLessEqual(upper, 21 * 9)
        # Both displayed values receive a liberal rounding interval; incompatibility persists.
        required_min = (173632.2 - .05) / (298.02 + .005)
        self.assertGreater(required_min, 21 * 9)
        self.assertGreater(required_min, upper)

    def test_reported_saving_variants_are_not_explained_by_display_rounding(self):
        _, _, rows, _ = M.calculate(M.load_inputs())
        incompatible = [r for r in rows if not r['table_rounding_compatible']]
        self.assertEqual([(r['scenario'], r['plant']) for r in incompatible], [('II', 'Honghaiwan')])
        row = incompatible[0]
        self.assertFalse(row['prose_rounding_compatible'])
        self.assertAlmostEqual(row['calculated_percent'], 11.01755643138661)

    def test_unique_network_length_and_source_path_accounting_are_different(self):
        _, _, _, rows = M.calculate(M.load_inputs())
        direct = sum(r['native_direct_km'] for r in rows)
        unique = sum(r['native_feeder_km'] for r in rows) + rows[0]['native_shared_trunk_km']
        paths = sum(r['naive_via_hub_path_km'] for r in rows)
        self.assertLess(unique, direct)
        self.assertGreater(paths, direct)
        self.assertAlmostEqual(paths - unique, 2 * 113.56)


if __name__ == '__main__':
    unittest.main()
