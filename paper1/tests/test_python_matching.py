"""Scientific boundary checks for B3-05's disclosed analyst diagnostics."""
import importlib.util
from pathlib import Path
import unittest

SPEC=importlib.util.spec_from_file_location('matching',Path(__file__).parents[1]/'scripts/audit_python_matching.py')
M=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(M)


class PythonMatchingTests(unittest.TestCase):
    def test_power_energy_and_mass_units(self):
        kWh,tonnes=M.energy_emissions(1,8760,.882)
        self.assertEqual(kWh,8760000);self.assertAlmostEqual(tonnes,7726.32)
        self.assertEqual(M.energy_emissions(1,0,.882),(0,0))
        with self.assertRaises(ValueError):M.energy_emissions(1,-1,.882)

    def test_epsilon_neighbors_do_not_limit_cluster_diameter_or_centroid_radius(self):
        labels,dist=M.dbscan_min2([[0,0],[90,0],[180,0],[270,0],[1000,0]],100)
        self.assertEqual(labels.tolist(),[0,0,0,0,-1]);self.assertEqual(dist[:4,:4].max(),270)
        points=M.np.array([[0,0],[90,0],[180,0],[270,0]])
        self.assertGreater(float(M.np.linalg.norm(points-points.mean(axis=0),axis=1).max()),100)

    def test_distance_tree_is_not_flow_distance_optimum(self):
        d=M.load_inputs();_,_,trees,_,_=M.calculate(d);t={x['tree']:x for x in trees}
        self.assertLess(t['distance_MST']['total_length_km'],t['direct_star']['total_length_km'])
        self.assertGreater(t['distance_MST']['flow_distance_proxy'],t['direct_star']['flow_distance_proxy'])
        self.assertAlmostEqual(t['distance_MST']['flow_distance_proxy'],201)

    def test_finite_priority_weight_depends_on_undisclosed_cost_scale(self):
        *_,weights,horizon=M.calculate(M.load_inputs())
        best={unit:min([x for x in weights if x['cost_unit']==unit],key=lambda x:x['weighted_numeric_score'])['design'] for unit in ['USD','BUSD']}
        self.assertEqual(best,{'USD':'one_residual','BUSD':'zero_residual'})
        self.assertTrue(horizon[0]['within_stock']);self.assertFalse(horizon[1]['within_stock'])


if __name__=='__main__':unittest.main()
