import importlib.util
import itertools
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('ccs_liability',Path(__file__).parents[1]/'scripts/audit_ccs_liability.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class CCSLiabilityChecks(unittest.TestCase):
    def test_historical_taxonomy_recovers_all_six_native_cases(self):
        d=m.load_inputs();seen=set()
        for row in d['native_classification']:
            got=m.historical_case(row['capture_annex_I'],row['storage_annex_I'],row['same_country'])
            self.assertEqual(got,{k:row[k] for k in got});seen.add(got['case'])
        self.assertEqual(seen,set(range(1,7)))
        self.assertEqual(m.historical_case(True,False,False)['mechanism'],'Annex_I_mitigation')
        self.assertEqual(m.historical_case(False,True,False)['proposed_liability'],'storing_country')

    def test_capacity_endpoints_close_without_identifying_a_best_estimate(self):
        checks,cells,classes,reported,finite,growth=m.calculate(m.load_inputs())
        val={x['item']:x['value'] for x in checks}
        for k,v in val.items():
            if k.endswith('_closure'):self.assertAlmostEqual(v,0)
        self.assertEqual(val['total_low_Gt_sum'],476)
        self.assertEqual(val['total_high_Gt_sum'],5880)
        self.assertEqual(val['range_midpoint'],3178)
        self.assertNotEqual(val['range_midpoint'],1660)
        self.assertLess(val['analyst_independent_interval_non_Annex_share_low'],50)
        self.assertEqual(len(cells),30)
        self.assertEqual(val['historical_energy_renewable_max'],21)
        self.assertEqual(val['historical_forestry_renewable_max'],60)

    def test_mass_ledger_conserves_source_carbon_and_separates_utility_carbon(self):
        a=m.mass_ledger(100,90,15,2,0,1)
        self.assertEqual(a['physical_balance_residual_t'],0)
        self.assertEqual((a['retained_t'],a['avoided_t'],a['emitted_t']),(87,72,28))
        b=m.mass_ledger(200,180,30,4,0,2)
        self.assertEqual(b['retained_t'],a['retained_t']*2)
        self.assertEqual(b['avoided_t'],a['avoided_t']*2)
        self.assertEqual(2*a['captured_t']/a['avoided_t'],2.5)
        self.assertLess(m.mass_ledger(100,90,100,2,0,1)['avoided_t'],0)

    def test_finite_replacement_pv_agrees_with_explicit_cash_flow_sum(self):
        for lam,r,g,T in itertools.product([0,.0001,.01,.2,1],[0,.01,.1],[-.02,0,.05],[1,21,60]):
            got=m.cohort_value(lam,r,expiry=T,growth=g)
            releases=sum(lam*(1-lam)**(t-1)*((1+g)/(1+r))**t for t in range(1,T+1))
            terminal=(1-lam)**T*((1+g)/(1+r))**T
            self.assertAlmostEqual(got['replacement_fraction'],releases+terminal,places=9)
            self.assertAlmostEqual(got['value_fraction']+got['replacement_fraction'],1)
            self.assertAlmostEqual(got['physical_retention'],(1-lam)**T)
        # Equal geometric ratio case tests the removable denominator singularity.
        self.assertAlmostEqual(m.cohort_value(.5,0,expiry=3,growth=1)['replacement_fraction'],4)

    def test_unrestricted_constant_price_value_and_long_horizon_limit(self):
        for lam,r in itertools.product([.0001,.001,.01],[.01,.05,.1]):
            value=m.cohort_value(lam,r)
            self.assertAlmostEqual(value['value_fraction'],r/(r+lam))
            self.assertAlmostEqual(value['replacement_fraction'],lam/(r+lam))
            self.assertAlmostEqual(m.cohort_value(lam,r,expiry=10000)['value_fraction'],value['value_fraction'])
        self.assertEqual(m.cohort_value(0,.05)['value_fraction'],1)
        self.assertAlmostEqual(m.cohort_value(.01,0)['value_fraction'],0)

    def test_credit_expiry_is_not_physical_release(self):
        short=m.cohort_value(0,.01,expiry=21)
        long=m.cohort_value(0,.01,expiry=60)
        self.assertEqual(short['physical_retention'],1)
        self.assertEqual(long['physical_retention'],1)
        self.assertAlmostEqual(short['value_fraction'],1-1.01**-21)
        self.assertLess(short['value_fraction'],long['value_fraction'])
        self.assertLess(long['value_fraction'],1)

    def test_rising_prices_require_a_convergent_present_value(self):
        base=m.cohort_value(.01,.1,growth=0)
        rising=m.cohort_value(.01,.1,growth=.05)
        self.assertLess(rising['value_fraction'],base['value_fraction'])
        with self.assertRaises(ValueError):m.cohort_value(.01,.1,growth=.12)
        # A finite model remains computable even when the infinite PV diverges.
        self.assertTrue(m.cohort_value(.01,.1,expiry=60,growth=.12)['value_fraction']<1)
        self.assertEqual(m.cohort_value(0,.1,growth=.12)['replacement_fraction'],0)

    def test_native_credit_table_is_preserved_without_claiming_reproduction(self):
        d=m.load_inputs();_,_,_,rows,finite,_=m.calculate(d)
        self.assertEqual(len(rows),12);self.assertEqual(len(finite),24)
        for row in rows:
            if row['release_percent']==0:self.assertEqual(row['reported_value_percent'],100)
            else:self.assertFalse(row['year_end_within_nearest_tenth'])
        worst=next(x for x in rows if x['release_percent']==1 and x['discount_percent']==1)
        self.assertEqual(worst['reported_value_percent'],48.5)
        self.assertAlmostEqual(worst['analyst_year_end_percent'],50)
        self.assertAlmostEqual(worst['analyst_year_start_percent'],49.5)

    def test_invalid_domains_and_case_inputs_are_rejected(self):
        for args in [(-.01,.1),(.01,-1),(10,.1),(.01,float('nan'))]:
            with self.assertRaises(ValueError):m.cohort_value(*args)
        with self.assertRaises(ValueError):m.cohort_value(.01,.1,expiry=0)
        with self.assertRaises(ValueError):m.cohort_value(.01,.1,expiry=True)
        with self.assertRaises(ValueError):m.historical_case(True,False,True)
        with self.assertRaises(ValueError):m.historical_case(1,False,False)
        with self.assertRaises(ValueError):m.mass_ledger(100,101,0,0,0,0)
        with self.assertRaises(ValueError):m.mass_ledger(100,90,0,50,50,0)

if __name__=='__main__':unittest.main()
