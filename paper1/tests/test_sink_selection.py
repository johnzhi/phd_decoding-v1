import csv
import importlib.util
import json
import math
from pathlib import Path
import unittest

from scipy.stats import entropy as independent_entropy

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('selection',ROOT/'scripts/audit_sink_selection.py')
selection=importlib.util.module_from_spec(spec)
spec.loader.exec_module(selection)


class SinkSelectionChecks(unittest.TestCase):
    def test_scenario1_all_leaves_and_equality_operators(self):
        data,_=selection.load_inputs();tree=data['trees']['scenario1']
        samples=[(2.25,.1,5,'F6_L1','SINK1'),(2.24,.25,5,'F6_L2','SINK1'),
                 (2.24,.24,3.5,'F6_L3','SINK2'),(2.24,.24,3.49,'F6_L4','SINK1')]
        for length,injectivity,W,leaf,outcome in samples:
            result=selection.predict(tree,dict(L2_over_L1=length,I1_over_I2=injectivity,W=W))
            self.assertEqual((result['leaf_id'],result['outcome']),(leaf,outcome))

    def test_scenario2_every_leaf_and_source_example(self):
        data,_=selection.load_inputs();tree=data['trees']['scenario2']
        samples=[(7.5,1,.8,5,1,'BOTH'),(7.5,1,.79,5,2,'SWITCH'),
                 (3,.6,.4,5,3,'BOTH'),(3,.6,.2,5,4,'SWITCH'),(3,.6,.199,5,5,'BOTH'),
                 (3,.15,.5,3.5,6,'BOTH'),(3,.14,.5,6.5,7,'LARGE'),
                 (3,.14,.5,6.49,8,'BOTH'),(3,.14,.5,3.49,9,'BOTH'),
                 (.6,3,.8,3.5,10,'BOTH'),(.6,3,.8,3.49,11,'LARGE'),
                 (.6,3,.79,5,12,'LARGE'),(.59,3,.8,5,13,'LARGE'),(2,2.99,.8,5,14,'LARGE')]
        for length,injectivity,R,W,leaf,outcome in samples:
            result=selection.predict(tree,dict(L2_over_L1=length,I1_over_I2=injectivity,R=R,W=W))
            self.assertEqual((result['leaf_id'],result['outcome']),(f'F8_L{leaf}',outcome))
        c=data['case2']
        result=selection.predict(tree,{k:c[k] for k in ('L2_over_L1','I1_over_I2','R','W')})
        self.assertEqual(result['outcome'],'BOTH')
        with self.assertRaises(ValueError):selection.predict(tree,dict(R=1,L2_over_L1=3,I1_over_I2=1,W=5))

    def test_geometry_matches_independent_coordinates_outside_dual_acos_domain(self):
        for ratio in (.1,.2,1,1.5,3,6,10):
            threshold=selection.geometry_threshold(100,100*ratio)
            for offset,expected in ((-1e-4,False),(1e-4,True)):
                theta=threshold+offset
                distance=math.hypot(100*ratio*math.cos(theta)-100,100*ratio*math.sin(theta))
                self.assertEqual(distance>max(100,100*ratio),expected)
        with self.assertRaises(ValueError):math.acos(6/2)  # literal second argument is not real
        with self.assertRaises(ValueError):selection.geometry_threshold(0,100)

    def test_entropy_uses_class_proportions_and_zero_limit(self):
        for counts in ([4,0],[2,2],[1,1,1],[1,3,9]):
            self.assertAlmostEqual(selection.entropy(counts),independent_entropy(counts,base=2))
        with self.assertRaises(ValueError):selection.entropy([0,0])
        self.assertAlmostEqual(selection.entropy([1,1,1]),math.log2(3))

    def test_units_and_common_pipeline_multiplier_do_not_fake_physical_service(self):
        data,_=selection.load_inputs();checks={r['item']:r for r in selection.calculate(data)}
        self.assertEqual(checks['case2_dimensionally_converted_R']['value'],.5)
        self.assertEqual(checks['R0.5_earliest_fullflow_fill']['value'],12.5)
        self.assertEqual(selection.well_capital(15,.3,2),100)
        self.assertGreater(checks['analyst_common_multiplier1_cost_difference']['value'],0)
        self.assertLess(checks['analyst_common_multiplier2_cost_difference']['value'],0)
        self.assertLess(checks['Figure4_ratio0.2_conditional_inverse_I_label_residual']['value'],-.9)
        self.assertEqual(len(checks),49)
        self.assertIsNone(data['missing']['physical_pressure_transient_well_interference_and_retention'])

    def test_grid_provenance_and_partial_citation_do_not_close_native_models(self):
        data,edge=selection.load_inputs();grid=selection.inference_grid(data)
        self.assertEqual(len(grid),402)
        self.assertTrue(all(r['native_optimal_label']=='' for r in grid))
        self.assertEqual(len({r['leaf_id'] for r in grid}),18)
        review=json.loads((ROOT/'evidence/comprehensive_review/B2-01.json').read_text())
        bibliography=json.loads((ROOT/'evidence/comprehensive_review_inputs/B2-01_bibliography.json').read_text())
        self.assertEqual(review['text_read_pages'],list(range(1,12)))
        self.assertEqual(review['visually_inspected_pages'],list(range(1,12)))
        self.assertEqual(len(review['visuals']),14)
        self.assertEqual(len(review['equations']),14)
        self.assertEqual(review['references'],bibliography['entries'])
        self.assertEqual(len(review['references']),51)
        self.assertEqual(sum(r['verification_status'].startswith('primary_text_checked') for r in review['references']),1)
        self.assertEqual(edge['cited_study'],'B3-13')
        self.assertEqual(edge['targeted_pages'],[1,2,3])
        self.assertEqual(review['overall_status'],'incomplete')
        result=json.loads((ROOT/'outputs/comprehensive_review/B2-01_reconciliation.json').read_text())
        self.assertFalse(result['native_ICCSEM_optimization_or_tree_training_accuracy_reproduced'])
        self.assertFalse(result['accepted_inputs_changed'])


if __name__=='__main__':unittest.main()
