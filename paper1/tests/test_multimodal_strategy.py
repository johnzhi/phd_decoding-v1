import importlib.util
import math
from pathlib import Path
import unittest

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('multimodal_strategy',ROOT/'scripts/audit_multimodal_strategy.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class MultimodalStrategyChecks(unittest.TestCase):
    def test_ramp_integral_matches_closed_form_for_all_partitions(self):
        for n in [1,2,4,5,10,20]:
            values=m.annual_targets(57.6,20,n)
            self.assertEqual(len(values),20)
            self.assertAlmostEqual(sum(values),20*57.6*(n+1)/(2*n))
            self.assertAlmostEqual(values[-1],57.6)
        with self.assertRaises(ValueError):m.annual_targets(57.6,20,3)

    def test_binary_product_LP_is_exact_at_both_modes(self):
        for mode in (0,1):
            for flow in [0,.2,.7,1]:
                lower,upper=m.product_range(flow,mode,1)
                self.assertAlmostEqual(lower,flow*mode)
                self.assertAlmostEqual(upper,flow*mode)
        with self.assertRaises(ValueError):m.product_range(1.1,1,1)

    def test_literal_capacity_index_and_inventory_do_not_get_silently_repaired(self):
        self.assertTrue(m.capacity_index_example())
        self.assertFalse(m.capacity_index_example(True))
        literal=m.inventory(.1,[.2,.2],[2,2],True)
        integral=m.inventory(.1,[.2,.2],[2,2])
        self.assertAlmostEqual(literal,.5);self.assertAlmostEqual(integral,.9)
        # Independently count each annual stock increment in the four-year case.
        self.assertAlmostEqual(integral,.1+sum([.2]*4))

    def test_integer_trip_conservation_counts_empty_return(self):
        trips=m.round_trip_milp(.059,.01)
        np.testing.assert_allclose(trips,[6,6],atol=1e-12)
        self.assertEqual(math.ceil(.059/.01),6)
        self.assertEqual(math.ceil(.457/.01),46)
        self.assertEqual(math.ceil(.779/.04),20)

    def test_annual_buffer_and_fleet_bounds_do_not_prove_daily_feasibility(self):
        reserve=m.buffer_rule(1)
        # Independent hourly material balance for a uniform24hdelivery.
        hourly=.04/24-1/8760
        peak=sum([hourly]*24)
        self.assertAlmostEqual(peak,m.peak_after_delivery(.04,24,1))
        self.assertGreater(peak,reserve)
        self.assertEqual(math.ceil(6/(8760*.8)),1)
        self.assertEqual(math.ceil(6/3),2)  # shared3hwindow requires2vehicles

    def test_reported_arithmetic_preserves_scope_and_rounding(self):
        data=m.load_inputs();checks,annual=m.calculate(data);r={x['item']:x['value'] for x in checks}
        self.assertEqual(len(annual),120);self.assertEqual(len(data['performance_table']),30)
        for n in [1,2,4,5,10]:self.assertEqual(r[f'rounding_overlap_N{n}'],1)
        self.assertAlmostEqual(r['end_year_storage_sum'],57.6)
        self.assertGreater(r['parallel_offshore_capacity'],49.4)
        self.assertAlmostEqual(r['pie_display_sum'],100.1)
        self.assertAlmostEqual(r['five_period_1h_time_saving'],55)
        self.assertIsNone(data['missing']['native_case_inputs_and_code'])


if __name__=='__main__':unittest.main()
