"""Scientific and accounting boundary tests for B3-08 diagnostics."""
import importlib.util
from pathlib import Path
import unittest

SPEC=importlib.util.spec_from_file_location('partial',Path(__file__).parents[1]/'scripts/audit_partial_bog.py')
M=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(M)


class PartialBOGTests(unittest.TestCase):
    def test_power_and_specific_cost_require_explicit_bases(self):
        self.assertAlmostEqual(M.power_from_specific(270,6000),450)
        terms=M.treatment_terms(.975,270,5e-5,.8,50,80)
        self.assertAlmostEqual(terms['fuel_USD_t'],13.5)
        self.assertAlmostEqual(terms['emission_tCO2_tBOG'],.025+.8*75/1000)
        self.assertAlmostEqual(terms['total_USD_t'],terms['fuel_USD_t']+terms['penalty_USD_t']-terms['sale_USD_t'])

    def test_generated_recovered_and_vented_component_mass_are_distinct(self):
        _,rows,_,_=M.calculate(M.load_inputs())
        for row in rows:
            self.assertAlmostEqual(row['recovered_component_kg_h']+row['vented_component_kg_h'],6000)
        self.assertAlmostEqual(rows[-1]['vented_component_kg_h'],0)
        self.assertNotEqual(rows[1]['nominal_BOR_vent_fraction_day'],.0012)

    def test_shared_cashflow_rounding_can_reconcile_all_three_cases(self):
        d=M.load_inputs();result=M.rounded_cashflows(d['native']['LCC'])
        self.assertTrue(result.success)
        witness=d['analyst']['rounding_shared_cashflow_witness']
        for row,profit in zip(d['native']['LCC'],witness['profits_million_y']):
            self.assertLess(abs(profit-row['profit_million_USD_y']),.05)
            self.assertAlmostEqual(witness['capital_million']+20*(witness['OM_million_y']-profit),row['reliquefaction_LCC_million_USD'])
        cap,om,*profits=result.x
        self.assertTrue(8.85-1e-10<=cap<=8.95+1e-10 and 1.25-1e-10<=om<=1.35+1e-10)
        for row,profit in zip(d['native']['LCC'],profits):
            self.assertLessEqual(abs(cap+20*(om-profit)-row['reliquefaction_LCC_million_USD']),.05000001)

    def test_stationary_scalar_component_matches_independent_bounded_solver(self):
        *_,rows=M.calculate(M.load_inputs())
        for row in rows:self.assertAlmostEqual(row['analytical_x'],row['bounded_scalar_x'],places=6)
        by={r['case']:r for r in rows}
        self.assertEqual(by['zero_value']['analytical_x'],0)
        self.assertEqual(by['upper_boundary']['analytical_x'],1)
        self.assertEqual(by['negative_sale_value']['analytical_x'],0)
        self.assertTrue(0<by['interior']['analytical_x']<1)

    def test_higher_carbon_price_cannot_lower_fixed_or_optimized_cost(self):
        d=M.load_inputs();a=d['analyst'];coef=2000;CL=5e-5;gamma=.8
        values=[]
        for CP in [0,20,50,100]:
            x=M.synthetic_quadratic_optimum(coef,CL,gamma,CP,80)
            values.append(M.treatment_terms(x,coef*x*x,CL,gamma,CP,80)['total_USD_t'])
        self.assertEqual(values,sorted(values))
        lo=M.treatment_terms(.7,980,CL,gamma,20,80)
        hi=M.treatment_terms(.7,980,CL,gamma,100,80)
        self.assertAlmostEqual(hi['total_USD_t']-lo['total_USD_t'],80*lo['emission_tCO2_tBOG'])

    def test_economic_optimum_does_not_minimize_emission_proxy(self):
        x=M.synthetic_quadratic_optimum(2000,5e-5,.8,50,80)
        economic=M.treatment_terms(x,2000*x*x,5e-5,.8,50,80)
        full=M.treatment_terms(1,2000,5e-5,.8,50,80)
        self.assertLess(economic['total_USD_t'],full['total_USD_t'])
        self.assertGreater(economic['emission_tCO2_tBOG'],full['emission_tCO2_tBOG'])


if __name__=='__main__':unittest.main()
