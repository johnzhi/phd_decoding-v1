import copy
import importlib.util
from pathlib import Path
import unittest
import numpy as np
from scipy.linalg import lstsq

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('rom',ROOT/'scripts/audit_reservoir_rom.py')
rom=importlib.util.module_from_spec(spec);spec.loader.exec_module(rom)


class ReservoirROMChecks(unittest.TestCase):
    def test_POD_reconstructs_rank_one_snapshots_and_is_sign_invariant(self):
        data,_=rom.load_inputs();case=data['toy'];phi=rom.pod_basis(case)
        snapshots=np.vstack((case['pressure_snapshots'],case['saturation_snapshots']))
        np.testing.assert_allclose(phi.T@phi,np.eye(2),atol=1e-14)
        np.testing.assert_allclose(phi@phi.T@snapshots,snapshots,atol=1e-14)
        original=rom.projected_step(case,phi)['reconstructed'];flipped=copy.deepcopy(case);sign=np.array([-1,1])
        for key in ('xi_previous','xi_next','xi_current'):flipped[key]=(np.array(case[key])*sign).tolist()
        np.testing.assert_allclose(rom.projected_step(flipped,phi*sign)['reconstructed'],original,atol=1e-14)

    def test_Petrov_Galerkin_matches_independent_least_squares_not_zero_full_residual(self):
        data,_=rom.load_inputs();case=data['toy'];r=rom.projected_step(case)
        rhs=-(np.array(case['A'])@r['phi']@(np.array(case['xi_current'])-case['xi_previous'])
              +np.array(case['B'])@(np.array(case['u_current'])-case['u_training']))
        independent=lstsq(np.array(case['J'])@r['phi'],rhs)[0]
        np.testing.assert_allclose(r['delta'],independent,atol=1e-14)
        self.assertGreater(np.linalg.norm(r['residual']),1e-4)
        self.assertLess(np.linalg.norm(r['projected_residual']),1e-14)
        with self.assertRaises(ValueError):rom.projected_step(dict(case,J=np.zeros((4,4)).tolist()))

    def test_bounded_selector_preserves_minimum_despite_output_objective(self):
        data,_=rom.load_inputs();case=data['toy'];eps=data['published']['epsilon']
        result=rom.selector_milp(case,eps)
        expected=rom.distances(18,[10,30,50],eps)
        self.assertEqual(result['selected'],int(np.argmin(expected)))
        self.assertAlmostEqual(result['minimum'],min(expected))
        self.assertAlmostEqual(result['output'],.8*2+.2*4+1)
        self.assertGreater(result['candidate_outputs'][2],result['output'])
        self.assertNotEqual(np.argmin(expected),np.argmin(rom.distances(18,[10,30,50],eps,False)))
        with self.assertRaises(ValueError):rom.distances(1,[0],0)

    def test_rate_amount_density_and_hydrostatic_units_remain_distinct(self):
        data,_=rom.load_inputs();values={r['item']:r['value'] for r in rom.calculate(data)}
        self.assertAlmostEqual(values['analyst_rate_mean_volume'],1.5/800)
        self.assertAlmostEqual(values['analyst_Eq29_if_inputs_are_interval_masses'],1.5/800)
        self.assertAlmostEqual(values['analyst_rate_mean_volume']/values['analyst_literal_Eq29_if_inputs_are_rates'],86400)
        self.assertEqual(values['analyst_b_from_rho_relation'],400)
        self.assertEqual(values['analyst_inverse_b_prose'],.0025)
        self.assertAlmostEqual(values['analyst_column_density_hydrostatic_comparison'],800*9.81*1500/1e5)

    def test_coarse_pressure_is_not_peak_and_plane_error_has_interaction_term(self):
        data,_=rom.load_inputs();p=data['toy']['pressure_case']
        limit=.9*p['fracture_pressure']
        self.assertLess(p['well_pressure']+np.mean(p['daily_rates'])/p['conductance'],limit)
        self.assertGreater(p['well_pressure']+max(p['daily_rates'])/p['conductance'],limit)
        case=data['toy']['pump_case']
        for row in rom.pump_corners(case):
            exact=(row['mass_rate_kgps']-case['reference_mass_rate_kgps'])*(row['delta_p_Pa']-case['reference_delta_p_Pa'])/(case['rho_kgpm3']*case['efficiency'])
            self.assertAlmostEqual(row['full_minus_plane_W'],exact)
        self.assertAlmostEqual(rom.pump_power(1,1e6,800,.8),1562.5)
        with self.assertRaises(ValueError):rom.pump_power(1,1,800,0)


if __name__=='__main__':unittest.main()
