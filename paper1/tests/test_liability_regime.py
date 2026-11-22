import importlib.util
import itertools
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('liability_regime',Path(__file__).parents[1]/'scripts/audit_liability_regime.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class LiabilityRegimeChecks(unittest.TestCase):
    def test_enumeration_matches_analytic_mean_covariance_and_probability_mass(self):
        for p,c,L in itertools.product([0,.1,.5,1],[0,.5,1],[0,100]):
            atoms,s=m.two_site_pool(p,L,100,c)
            self.assertAlmostEqual(sum(x['probability'] for x in atoms),1)
            self.assertTrue(all(x['probability']>=0 for x in atoms))
            self.assertAlmostEqual(sum(x['probability']*x['site1_event'] for x in atoms),p)
            self.assertAlmostEqual(sum(x['probability']*x['site2_event'] for x in atoms),p)
            self.assertAlmostEqual(s['mean_loss_units'],2*p*L)
            self.assertAlmostEqual(s['variance_loss_units2'],2*L**2*p*(1-p)*(1+c))

    def test_correlation_increases_unfunded_tail_without_reducing_mean_physical_loss(self):
        vals=[m.two_site_pool(.1,100,100,c)[1] for c in [0,.5,1]]
        for s in vals:self.assertAlmostEqual(s['mean_loss_units'],20)
        for s,short in zip(vals,[1,5.5,10]):self.assertAlmostEqual(s['mean_unfunded_units'],short)
        self.assertAlmostEqual(vals[0]['loss_above_fund_probability'],.01)
        self.assertAlmostEqual(vals[-1]['loss_above_fund_probability'],.1)
        self.assertAlmostEqual(vals[-1]['variance_loss_units2'],2*vals[0]['variance_loss_units2'])

    def test_fund_payments_and_shortfalls_conserve_every_claim_amount(self):
        for fund in [0,50,100,150,200,1000]:
            atoms,s=m.two_site_pool(.1,100,fund,.5)
            for row in atoms:self.assertEqual(row['pool_paid_units']+row['unfunded_units'],row['loss_units'])
            self.assertAlmostEqual(s['mean_pool_paid_units']+s['mean_unfunded_units'],s['mean_loss_units'])
            self.assertAlmostEqual(s['mean_loss_units'],20)
        self.assertEqual(m.two_site_pool(.1,100,200,.5)[1]['mean_unfunded_units'],0)

    def test_annuity_requirement_matches_closed_form_and_yearly_cash_balance(self):
        masses=[1e6,2e6,3e6];annual=1e6
        for years,r in itertools.product([15,30,50],[0,.02]):
            s=m.monitoring_fund(masses,2,annual,years,r)
            expected=annual*years if r==0 else annual*(1-(1+r)**(-years))/r
            self.assertAlmostEqual(s['monitoring_PV_at_injection_end_currency'],expected,places=6)
            # A separately iterated cash balance using the computed exact charge
            # must end at zero after the stated monitoring payments.
            balance=0
            for mass in masses:balance=balance*(1+r)+s['conditional_required_fee_currency_per_t']*mass
            for _ in range(years):balance=balance*(1+r)-annual
            self.assertAlmostEqual(balance,0,places=5)
        zero=m.monitoring_fund(masses,2,annual,30,0)
        self.assertEqual(zero['injection_end_fund_currency'],12e6)
        self.assertEqual(zero['funding_gap_currency'],18e6)
        self.assertEqual(zero['conditional_required_fee_currency_per_t'],5)

    def test_charge_units_and_mass_cost_scaling_are_explicit(self):
        a=m.monitoring_fund([1e6,2e6,3e6],2,1e6,30,.02)
        b=m.monitoring_fund([2e6,4e6,6e6],2,1e6,30,.02)
        c=m.monitoring_fund([1e6,2e6,3e6],2,2e6,30,.02)
        self.assertAlmostEqual(b['conditional_required_fee_currency_per_t'],a['conditional_required_fee_currency_per_t']/2)
        self.assertAlmostEqual(c['conditional_required_fee_currency_per_t'],2*a['conditional_required_fee_currency_per_t'])
        self.assertAlmostEqual(b['injection_end_fund_currency'],2*a['injection_end_fund_currency'])
        d=m.monitoring_fund([1e6,2e6,3e6],2,0,30,.02)
        self.assertEqual(d['conditional_required_fee_currency_per_t'],0)

    def test_invalid_probabilities_money_and_years_are_rejected(self):
        for args in [(-.1,100,100,0),(.1,-1,100,0),(.1,100,-1,0),(.1,100,100,2),(float('nan'),100,100,0)]:
            with self.assertRaises(ValueError):m.two_site_pool(*args)
        with self.assertRaises(ValueError):m.monitoring_fund([],2,1e6,30,.02)
        with self.assertRaises(ValueError):m.monitoring_fund([0],2,1e6,30,.02)
        with self.assertRaises(ValueError):m.monitoring_fund([1e6],-1,1e6,30,.02)
        with self.assertRaises(ValueError):m.monitoring_fund([1e6],2,1e6,True,.02)
        with self.assertRaises(ValueError):m.monitoring_fund([1e6],2,1e6,30,-.01)

if __name__=='__main__':unittest.main()
