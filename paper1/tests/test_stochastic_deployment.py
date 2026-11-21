import importlib.util
import math
from pathlib import Path
import unittest
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('deployment',ROOT/'scripts/audit_stochastic_deployment.py')
model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)


class StochasticDeploymentChecks(unittest.TestCase):
    def test_cost_sign_changes_optional_project_choice(self):
        data,_=model.load_inputs();case=data['analyst_cost_case']
        correct=model.objective_component(case);literal=model.objective_component(case,True)
        self.assertEqual((correct,literal),(-10,30))
        self.assertEqual(literal-correct,2*case['operating'])
        with self.assertRaises(ValueError):model.objective_component(dict(case,operating=math.nan))

    def test_set_update_omits_new_commitment_and_reservation_prevents_overbooking(self):
        data,_=model.load_inputs();case=data['analyst_stock_case']
        bad=model.stock_trace(case,True);comparison=model.stock_trace(case,False)
        self.assertEqual([r['built'] for r in bad],[1,1])
        self.assertEqual([r['built'] for r in comparison],[1,0])
        self.assertEqual(bad[-1]['lifetime_commitment_total'],10*(2+2))
        self.assertGreater(bad[-1]['lifetime_commitment_total'],case['initial_stock'])
        self.assertEqual(comparison[-1]['available_after_update'],case['initial_stock']-10*2)
        with self.assertRaises(ValueError):model.stock_trace(dict(case,lifetime=0),False)

    def test_independent_MILP_confirms_rolling_value_is_not_an_upper_bound(self):
        data,_=model.load_inputs();case=data['analyst_horizon_case']
        solved=milp(c=-np.array(case['rewards'],dtype=float),integrality=np.ones(2),bounds=Bounds(0,1),
                    constraints=LinearConstraint(np.array([case['commitments']]),-np.inf,case['capacity']))
        self.assertTrue(solved.success)
        result=model.horizon_solutions(case)
        self.assertEqual(result['full_objective'],-solved.fun)
        self.assertEqual(result['full_decisions'],[0,1]);self.assertEqual(result['rolling_decisions'],[1,0])
        self.assertLess(result['rolling_objective'],result['full_objective'])

    def test_finite_sample_values_need_not_be_confidence_bounds(self):
        data,_=model.load_inputs();values={r['item']:r['value'] for r in model.calculate(data)}
        truth=values['analyst_finite_sample_true_expected_single_policy']
        self.assertEqual(truth,(0+2)/2)
        self.assertLess(values['analyst_finite_sample_one_sample_low'],truth)
        self.assertGreater(values['analyst_finite_sample_one_sample_high'],truth)
        self.assertAlmostEqual(values['reported_deviation_reduction_recomputed'],96.97101147028154)
        self.assertEqual(round(values['reduction_from_reported_endpoints'],1),55.4)


if __name__=='__main__':unittest.main()
