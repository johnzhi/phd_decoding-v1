import importlib.util
import itertools
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('prudent_storage',Path(__file__).parents[1]/'scripts/audit_prudent_storage.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class PrudentStorageChecks(unittest.TestCase):
    def test_bulk_coefficient_dimensions_and_linear_scaling(self):
        self.assertAlmostEqual(m.stock_from_bulk(1.5,.037)*1e9,55500)
        self.assertAlmostEqual(m.stock_from_bulk(1000,.037),.037)
        self.assertAlmostEqual(.037*1e12/1e12,.037)  # kg/m3 bulk, not fluid density
        self.assertEqual(m.stock_from_bulk(0,.037),0)

    def test_temperature_stock_competition_and_response_corners(self):
        self.assertAlmostEqual(m.temperature_potential(1460,.45),.657)
        self.assertAlmostEqual(m.temperature_potential(1290,.27),.3483)
        self.assertAlmostEqual(m.temperature_potential(2710,.45),1.2195)
        self.assertEqual(m.temperature_potential(1460,.45,0),0)
        self.assertAlmostEqual(m.temperature_potential(1460,.45,.3),.657*.3)

    def test_mask_union_matches_exhaustive_cell_set_calculation(self):
        # All pairs of masks on a four-cell domain, both orders, independent
        # set-union calculation: marginal attribution varies, union does not.
        weights=[6,3,1,2];subsets=[{i for i in range(4) if bits&(1<<i)} for bits in range(16)]
        for a,b in itertools.product(subsets,repeat=2):
            expect=sum(weights[i] for i in set(range(4))-(a|b))
            for order in [('A','B'),('B','A')]:
                rows=m.mask_sequence(weights,{'A':a,'B':b},order)
                self.assertEqual(rows[-1]['remaining'],expect)
                self.assertEqual(sum(r['removed'] for r in rows)+expect,sum(weights))
        self.assertNotEqual(m.mask_sequence(weights,{'A':{0,1},'B':{1,2}},('A','B'))[0]['removed'],
                            m.mask_sequence(weights,{'A':{0,1},'B':{1,2}},('B','A'))[1]['removed'])

    def test_first_negative_and_exact_zero_are_distinct_conventions(self):
        self.assertEqual(m.first_negative_year([2030,2040,2050],[10,0,-10]),2041)
        self.assertIsNone(m.first_negative_year([2030,2040,2050],[10,0,0]))
        self.assertIsNone(m.first_negative_year([2030,2040],[-1,-2]))
        self.assertEqual(m.first_negative_year([2030,2040],[10,-10]),2036)

    def test_annual_extrapolated_sum_matches_closed_form_and_threshold_bracket(self):
        rows,cross=m.extrapolate([2090,2100],[8,12],1000,100)
        self.assertEqual(cross,2144)
        for n,r in enumerate(rows,1):
            self.assertAlmostEqual(r['rate_Gt_y'],12+.4*n)
            self.assertAlmostEqual(r['cumulative_Gt'],100+12*n+.4*n*(n+1)/2)
        self.assertLess(rows[42]['cumulative_Gt'],1000)
        self.assertGreaterEqual(rows[43]['cumulative_Gt'],1000)
        self.assertEqual(m.remaining_years(1000,100,12),75)
        self.assertNotEqual(2100+75,cross)

    def test_decreasing_extrapolation_requires_explicit_policy(self):
        rows,cross=m.extrapolate([2090,2100],[16,12],1000,100)
        self.assertIsNone(cross)
        self.assertAlmostEqual(rows[-1]['rate_Gt_y'],-68)
        self.assertAlmostEqual(rows[-1]['cumulative_Gt'],-5540)
        self.assertAlmostEqual(100+sum(max(0,r['rate_Gt_y']) for r in rows),274)
        self.assertTrue(any(r['cumulative_Gt']<0 for r in rows))
        # This is the analyst raw extrapolator, not an assertion about author code.

    def test_source_panel_labels_and_rounding_ambiguity_are_preserved(self):
        d=m.load_inputs();checks,rings,temp,seq,scenarios,states=m.calculate(d)
        self.assertEqual([r['sum_Gt'] for r in rings],[5701,994,5517,452])
        self.assertEqual([r['native_label'] for r in rings],['Offshore','Offshore','Onshore','Onshore'])
        self.assertTrue(all(not r['rounding_compatible'] for r in rings))
        val={r['item']:r['value'] for r in checks}
        self.assertLess(val['historical_scale_rounding_low'],175)
        self.assertGreater(val['historical_scale_rounding_high'],175)
        self.assertEqual(len(temp),6);self.assertEqual(len(scenarios),400)
        # Rho ratio = inverse volume ratio only for equal mass; surface state matters.
        self.assertEqual(len(states),6)
        for r in states:
            self.assertAlmostEqual(r['density_kg_m3']/r['surface_density_kg_m3'],r['equal_mass_volume_reduction'])
        self.assertGreater(states[0]['equal_mass_volume_reduction'],states[1]['equal_mass_volume_reduction'])

    def test_invalid_domains_are_rejected(self):
        for args in [(-1,.037),(1,float('nan'))]:
            with self.assertRaises(ValueError):m.stock_from_bulk(*args)
        with self.assertRaises(ValueError):m.temperature_potential(1460,.45,50)
        with self.assertRaises(ValueError):m.remaining_years(1000,1001,1)
        with self.assertRaises(ValueError):m.remaining_years(1000,100,0)
        with self.assertRaises(ValueError):m.mask_sequence([1,2],{'A':[3]},['A'])
        with self.assertRaises(ValueError):m.first_negative_year([2040,2030],[1,-1])
        with self.assertRaises(ValueError):m.extrapolate([2090,2100],[8,-1],1000,100)
        with self.assertRaises(ValueError):m.conditional_state(800,0,15,25,1000,9.80665)

if __name__=='__main__':unittest.main()
