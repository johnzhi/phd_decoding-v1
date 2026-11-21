import importlib.util
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('prospective', ROOT / 'scripts/audit_prospective_assessment.py')
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)


class ProspectiveAssessmentChecks(unittest.TestCase):
    def test_learning_matches_repeated_direct_percentage_reductions(self):
        # Independent experience-curve identity: k doublings multiply by (1-LR)^k.
        for rate in (0, .05, .13, .22, .5):
            expected = 100.
            for k in range(9):
                self.assertAlmostEqual(model.component_cost(100, 3, 3 * 2**k, rate), expected)
                expected *= 1-rate

    def test_component_baselines_and_capacity_units(self):
        case = model.load_inputs()['analyst_case']
        self.assertEqual(model.costs(case, case['initial_capacities'])[0], 300)
        self.assertAlmostEqual(model.costs(case, case['future_capacities'])[0], 100*.8+200*.9)
        scaled = dict(case, initial_capacities=[v/1e6 for v in case['initial_capacities']])
        self.assertAlmostEqual(model.costs(scaled, [v/1e6 for v in case['future_capacities']])[0], 260)
        self.assertAlmostEqual(model.component_cost(100, 10, 20, .2) * 1.5,
                               model.component_cost(150, 10, 20, .2))

    def test_literal_second_denominator_fails_its_own_baseline(self):
        case = model.load_inputs()['analyst_case']
        intended, literal = model.costs(case, case['initial_capacities'])
        self.assertGreater(intended-literal, 50)
        equal = dict(case, initial_capacities=[10,10])
        a, b = model.costs(equal, [20,20]); self.assertEqual(a,b)
        no_learning = dict(case, learning_rates=[.2,0])
        a, b = model.costs(no_learning, case['future_capacities']); self.assertEqual(a,b)

    def test_domains_and_ambiguous_table_capacity_stay_explicit(self):
        for rate in (-.1, 1, math.nan, math.inf):
            with self.assertRaises(ValueError): model.learning_exponent(rate)
        for x0, x in ((0,1),(1,0),(-1,2),(1,math.inf)):
            with self.assertRaises(ValueError): model.component_cost(100,x0,x,.1)
        data = model.load_inputs(); values = {r['item']:r for r in model.calculate(data)}
        self.assertNotIn('T1R04_same_unit_capacity_ratio', values)
        self.assertEqual(data['table1'][3]['xt_MtCO2_literal'], '1,4')
        self.assertEqual(values['T1R01_same_unit_capacity_ratio']['value'], 15357/3)
        self.assertEqual(sum(r['storage_boundary_explicitly_unclear'] for r in data['table1']), 2)


if __name__ == '__main__':
    unittest.main()
