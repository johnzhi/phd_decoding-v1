import gzip
import importlib.util
import json
import math
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('decatur_history',ROOT/'scripts/audit_decatur_history.py')
history=importlib.util.module_from_spec(spec);spec.loader.exec_module(history)


class DecaturHistoryChecks(unittest.TestCase):
    def test_reconstructed_geometry_closes_analytic_extent_and_volume(self):
        data,_=history.load_inputs();cells,radii,depths=history.reconstruct_geometry(data)
        self.assertEqual(len(cells),12194)
        self.assertEqual(len(radii)-1,67);self.assertEqual(len(depths)-1,182)
        self.assertEqual(radii[-1],100000)
        self.assertEqual(depths[0],1974);self.assertEqual(depths[-1],1420)
        self.assertEqual(depths[89],1885)
        self.assertTrue(all(b>a for a,b in zip(radii,radii[1:])))
        self.assertTrue(all(b<a for a,b in zip(depths,depths[1:])))
        geometric_sum=math.fsum(c['volume_per_radian_m3'] for c in cells)
        self.assertAlmostEqual(geometric_sum/(.5*100000**2*554),1,places=12)
        self.assertIsNone(data['mesh']['native_well_cell_indices'])
        self.assertIsNone(data['model']['outer_radial_boundary'])

    def test_skin_relation_matches_independent_radial_resistance_integral(self):
        data,_=history.load_inputs();s=data['skin'];ratio=history.skin_permeability_ratio(s['s'],s['rw_m'],s['rs_m'])
        def integral(a,b,k,n=4000):
            log_a,log_b=math.log(a),math.log(b);total=0
            for i in range(n):
                left=math.exp(log_a+(log_b-log_a)*i/n);right=math.exp(log_a+(log_b-log_a)*(i+1)/n)
                total+=(right-left)/(k*math.sqrt(left*right))
            return total
        far=100
        actual=integral(s['rw_m'],s['rs_m'],ratio)+integral(s['rs_m'],far,1)
        expected=math.log(far/s['rw_m'])+s['s']
        self.assertAlmostEqual(actual,expected,places=5)
        self.assertGreater(ratio,36);self.assertLess(ratio,37)
        self.assertEqual(history.skin_permeability_ratio(0,.12,.29),1)
        self.assertLess(math.log(far/.12)/expected,1.2)
        with self.assertRaises(ValueError):history.skin_permeability_ratio(-math.log(.29/.12),.12,.29)
        with self.assertRaises(ValueError):history.skin_permeability_ratio(s['s'],.12,.28)

    def test_Leverett_and_log_scaling_do_not_require_invented_absolute_curves(self):
        self.assertEqual(history.leverett_factor(1,1),1)
        self.assertEqual(history.leverett_factor(.25,1),2)
        self.assertAlmostEqual(history.leverett_factor(1,.5),math.sqrt(.5))
        self.assertAlmostEqual(history.minmax_normalize(10,.01,26.6),history.minmax_normalize(.10,.0001,.266))
        self.assertGreater(history.minmax_normalize(300,26,227),1)
        data,_=history.load_inputs()
        self.assertIsNone(data['model']['Berea_reference_curve'])
        self.assertIsNone(data['model']['Berea_reference_k_m2'])
        with self.assertRaises(ValueError):history.leverett_factor(0,1)

    def test_pressure_normalization_handles_reference_and_conditional_error_scope(self):
        self.assertEqual(history.normalized_gradient(114000,114000),1)
        self.assertGreater(history.normalized_gradient(115140,114000),1)
        low,high=history.gradient_example_bounds(115140,114000,1000)
        self.assertLess(low,1);self.assertGreater(high,1)
        with self.assertRaises(ValueError):history.normalized_buildup(.2,0)
        with self.assertRaises(ValueError):history.gradient_example_bounds(1000,1000,1000)
        self.assertEqual(history.normalized_buildup(.2,.05),4)
        data,_=history.load_inputs()
        self.assertTrue(data['analyst_examples']['source_resolution_is_not_error_bound'])
        self.assertIsNone(data['observation']['exact_drift_and_filter_method'])

    def test_datum_comparison_does_not_adopt_correction_or_citation_edge(self):
        data,edge=history.load_inputs();cross=history.depth_comparison(data,edge)
        zone4=next(r for r in cross if r['zone']==4)
        self.assertEqual(zone4['B1_18_below_ground_m'],2079.4)
        self.assertAlmostEqual(zone4['figure_minus_B1_18_below_ground_m'],4.8224)
        offsets=[r['figure_minus_B1_18_below_ground_m'] for r in cross]
        self.assertTrue(all(4.6<offset<4.9 for offset in offsets))
        self.assertIsNone(data['physical_geometry']['unknown_KB_or_other_datum_offset_m'])
        self.assertIn('NOT a direct citation',edge['relation'])
        self.assertEqual(data['model']['pure_H2O_viscosity_literal_Pa_s'],.56e-4)
        self.assertEqual(data['model']['brine_viscosity_literal_Pa_s'],.8e-4)
        self.assertEqual(data['model']['calibration_pressure_days'],40)
        self.assertIn('breakthrough',data['model']['arrival_calibration'])

    def test_source_coverage_and_components_leave_originals_and_native_case_open(self):
        review=json.loads((ROOT/'evidence/comprehensive_review/B1-18.json').read_text())
        self.assertEqual(review['text_read_pages'],list(range(1,13)))
        self.assertEqual(review['visually_inspected_pages'],list(range(1,13)))
        self.assertEqual(len(review['visuals']),9)
        self.assertEqual(sum(r['record_type']=='printed_bibliography' for r in review['references']),28)
        self.assertTrue(all(r['verification_status']=='unverified' for r in review['references']))
        self.assertEqual(review['overall_status'],'incomplete')
        result=json.loads((ROOT/'outputs/comprehensive_review/B1-18_reconciliation.json').read_text())
        self.assertFalse(result['native_history_match_or_prediction_reproduced'])
        self.assertFalse(result['native_TOUGH_mesh_connections_or_forward_case_reproduced'])
        self.assertFalse(result['accepted_inputs_changed'])
        with gzip.open(ROOT/'outputs/comprehensive_review/B1-18_geometry.csv.gz','rt') as stream:
            self.assertEqual(sum(1 for _ in stream)-1,12194)


if __name__=='__main__':unittest.main()
