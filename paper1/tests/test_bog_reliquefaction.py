import csv
import importlib.util
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('bog', ROOT/'scripts/audit_bog_reliquefaction.py')
bog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bog)


class BOGChecks(unittest.TestCase):
    def test_fill_inverse_matches_independent_volume_construction(self):
        for gas_moles,liquid_moles,vg,vl in [(2,98,2,.02),(10,1,1,.01),(0,3,4,.1)]:
            fill = liquid_moles*vl/(gas_moles*vg+liquid_moles*vl)
            self.assertAlmostEqual(bog.vapor_mole_fraction(fill,vg/vl),gas_moles/(gas_moles+liquid_moles))
        for args in ((-1,100),(1.01,100),(.5,0),(.5,math.nan)):
            with self.assertRaises(ValueError):bog.vapor_mole_fraction(*args)

    def test_annuity_closes_discounted_cashflow_including_zero_interest(self):
        for interest in (0,.1,.03):
            factor = bog.capital_recovery_factor(interest,20)
            self.assertAlmostEqual(sum(factor/(1+interest)**year for year in range(1,21)),1)
        with self.assertRaises(ValueError):bog.capital_recovery_factor(.1,0)

    def test_energy_units_close_using_independent_kg_balance(self):
        data=bog.load_inputs();rows={r['item']:r for r in bog.calculate(data)}
        # 1MWh consumes197.5kg MGO and emits633.185kgCO2 under printed factors.
        self.assertAlmostEqual(rows['compression_MGO_CO2_per_kWh']['value']*1000*1000,197.5*3.206)
        for r in data['rows']:
            if r['figure6_power_kW'][0] is not None:
                independent_kg = r['figure6_power_kW'][2]*4000*.1975*3.206
                self.assertLess(abs(independent_kg/1000-r['laden_compression_CO2_t']),.18)
        self.assertIsNone(data['missing']['ballast_power_and_purge_split'])

    def test_percentages_preserve_complement_and_literal_bad_inputs(self):
        data=bog.load_inputs();checks={r['item']:r for r in bog.calculate(data)}
        for case in ('1-3','2-3'):
            for n in (.05,.1,.15):
                key=f'C{case}_N{n:g}_compression_vs_two_stage_single_'
                self.assertAlmostEqual(checks[key+'remaining_percent']['value']+checks[key+'reduction_percent']['value'],100)
        self.assertAlmostEqual(checks['C1-3_N0.05_compression_vs_two_stage_single_reduction_percent']['value'],20.7971981321)
        self.assertEqual(checks['laden_C1-3_N0.05_mixture_sum']['value'],105)
        conflict=data['pressure_conflicts'][0]
        self.assertEqual(conflict['table_A1_R5_bar'],conflict['table_A4_R6_bar'])
        with self.assertRaises(ValueError):bog.percentage(2,0)

    def test_rounding_checks_do_not_close_native_models_or_sources(self):
        data=bog.load_inputs();checks=bog.calculate(data)
        with (ROOT/'data/analysis_inputs.csv').open() as stream:
            existing={r['value_id']:r for r in csv.DictReader(stream)}
        for r in data['rows']:
            prefix=f"bog_{r['case']}_{round(r['N2_liquid_label_mol_percent']*100):03d}_"
            self.assertEqual(float(existing[prefix+'emissions']['value']),r['annual_CO2_t'])
            self.assertEqual(float(existing[prefix+'transport']['value']),r['transported_kt_per_year'])
        self.assertEqual(len(checks),324)
        overlaps=[r for r in checks if r['item'].endswith('CPT_rounding_intervals_overlap')]
        self.assertEqual(len(overlaps),18)
        self.assertTrue(all(r['value']==1 for r in overlaps))
        review=json.loads((ROOT/'evidence/comprehensive_review/B1-19.json').read_text())
        bibliography=json.loads((ROOT/'evidence/comprehensive_review_inputs/B1-19_bibliography.json').read_text())
        self.assertEqual(review['text_read_pages'],list(range(1,16)))
        self.assertEqual(review['visually_inspected_pages'],list(range(1,16)))
        self.assertEqual(len(review['visuals']),24)
        self.assertEqual(len(review['equations']),18)
        self.assertEqual(review['references'],bibliography['entries'])
        self.assertEqual(bibliography['printed_entries'],48)
        self.assertEqual(len(review['references']),55)
        self.assertTrue(all(r['verification_status']=='unverified' for r in review['references']))
        self.assertEqual(review['overall_status'],'incomplete')
        result=json.loads((ROOT/'outputs/comprehensive_review/B1-19_reconciliation.json').read_text())
        self.assertFalse(result['native_HYSYS_PR_flash_recycle_PSO_APEA_or_heat_transfer_model_reproduced'])
        self.assertFalse(result['accepted_inputs_changed'])


if __name__=='__main__':
    unittest.main()
