"""Meaningful boundaries for conditional capacity/denominator diagnostics."""
import importlib.util
from pathlib import Path
import unittest

SPEC=importlib.util.spec_from_file_location('port_safety',Path(__file__).parents[1]/'scripts/audit_port_safety.py')
M=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(M)


class PortSafetyTests(unittest.TestCase):
    def test_rounding_interval_is_monotone_and_contains_central_ratio(self):
        lo,hi=M.percentage_interval(.31,17.95,.005)
        self.assertLess(lo,100*.31/17.95);self.assertGreater(hi,100*.31/17.95)
        dlo,dhi=M.percentage_interval(18.25,19.89,.005,decline=True)
        self.assertLess(dlo,100*(1-18.25/19.89));self.assertGreater(dhi,100*(1-18.25/19.89))
        with self.assertRaises(ValueError):M.percentage_interval(1,.005,.005)

    def test_buffer_dimensions_and_conditional_density_scaling(self):
        one=M.buffer_example(32000,2,1000,5.9e6,365)
        half=M.buffer_example(32000,2,500,5.9e6,365)
        self.assertEqual(one['buffer_m3'],64000);self.assertEqual(one['conditional_buffer_t'],64000)
        self.assertAlmostEqual(one['equivalent_uniform_throughput_days']*5.9e6/365,64000)
        self.assertEqual(half['equivalent_uniform_throughput_days']*2,one['equivalent_uniform_throughput_days'])
        with self.assertRaises(ValueError):M.buffer_example(32000,2,1000,0,365)

    def test_handling_boundary_changes_count_without_creating_physical_mass(self):
        a=M.handling_example(15,20,1);b=M.handling_example(15,20,2)
        self.assertEqual(a['physical_CO2_Mt_per_y'],35);self.assertEqual(b['physical_CO2_Mt_per_y'],35)
        self.assertEqual(a['conditional_UK_handling_Mt_per_y'],35);self.assertEqual(b['conditional_UK_handling_Mt_per_y'],50)
        with self.assertRaises(ValueError):M.handling_example(15,20,0)


if __name__=='__main__':unittest.main()
