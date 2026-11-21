import importlib.util
import math
from pathlib import Path
import unittest

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pipeline_diffusion',ROOT/'scripts/audit_pipeline_diffusion.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class PipelineDiffusionChecks(unittest.TestCase):
    def test_discount_blocks_match_independent_annual_cash_stream(self):
        blocks=m.discount_weights(9,3,.06)
        annual=math.fsum(1.06**-year for year in range(25))
        self.assertAlmostEqual(sum(blocks),annual)
        self.assertEqual(sum(m.period_weights(9,3)),25)
        self.assertAlmostEqual(blocks[-1],1.06**-24)
        self.assertAlmostEqual(m.discount_weights(9,3,0)[0],3)

    def test_saturated_history_matches_independent_linear_system(self):
        # Solve all Eq9/13 equalities simultaneously, independently of the
        # production recurrence. This does not reconstruct a network optimum.
        for depreciation in (0,.1):
            rows=m.saturated_diffusion(9,3,.12,160,depreciation)
            a=np.eye(9);growth=1.12**3-1
            for i in range(9):
                for j in range(i):a[i,j]=-growth*(1-depreciation)**(3*(i-j))
            expected=np.linalg.solve(a,np.full(9,480.))
            np.testing.assert_allclose([r['addition'] for r in rows],expected,rtol=1e-12)
        no_growth=m.saturated_diffusion(9,3,0,160)
        self.assertEqual([r['addition'] for r in no_growth],[480]*9)
        increments=np.diff([r['addition'] for r in rows])
        self.assertTrue(np.all(increments>0))

    def test_knowledge_pooling_and_lifetime_are_distinct_constraints(self):
        self.assertEqual(m.knowledge([100,0,0,0],3,3,0),100)
        self.assertEqual(m.surviving_capacity([100,0,0,0],3,3,3),0)
        self.assertEqual(m.surviving_capacity([100,0,0,0,0],3,10,3),100)
        self.assertEqual(m.surviving_capacity([100,0,0,0,0],4,10,3),0)
        with self.assertRaises(ValueError):m.knowledge([100],1,3,1.1)

    def test_finite_penalty_can_miss_a_feasible_target(self):
        cheap=m.penalty_example(6,5);expensive=m.penalty_example(6,7)
        self.assertEqual(cheap['service'],0);self.assertEqual(cheap['slack'],1)
        self.assertEqual(expensive['service'],1);self.assertEqual(expensive['slack'],0)
        self.assertLess(cheap['cost'],6)  # feasible hard-target alternative

    def test_accounting_conflicts_are_not_silently_resolved(self):
        data=m.load_inputs();checks,_=m.calculate(data);r={x['item']:x['value'] for x in checks}
        self.assertAlmostEqual(r['body_gap_fraction'],100*4.8/53)
        self.assertAlmostEqual(r['caption_gap_fraction'],100*1.7/53)
        self.assertAlmostEqual(r['hypothetical_unweighted_gap'],1.7)
        self.assertAlmostEqual(r['hypothetical_weighted_gap'],4.8)
        self.assertGreater(r['alternative_modes_emissions_vs_caption_gap'],5)
        # Reported rounded percentages can coexist, e.g.5.49%,33.51%,26.56%.
        ratio=100*(1.3351/1.0549-1)
        self.assertEqual(round(ratio),27)
        self.assertEqual(m.pipeline_capex(1000,100,1000,100000),11_000_000)
        self.assertLess(r['pipeline_capex_per_tpy_2000'],r['pipeline_capex_per_tpy_1000'])
        self.assertEqual(r['ship_variable_per_t_km'],.06)
        self.assertIsNone(data['missing']['native_penalty_EUR_per_tCO2'])


if __name__=='__main__':unittest.main()
