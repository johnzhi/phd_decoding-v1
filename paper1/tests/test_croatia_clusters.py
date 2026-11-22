"""Mass-boundary and source-driven counterexample checks for B3-04."""
import importlib.util
from pathlib import Path
import unittest

SPEC=importlib.util.spec_from_file_location('croatia',Path(__file__).parents[1]/'scripts/audit_croatia_clusters.py')
M=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(M)


class CroatiaClusterTests(unittest.TestCase):
    def test_recovery_conserves_fresh_mass_without_changing_unproduced_mass(self):
        for I,P in [(100,40),(8542,5291),(275,80)]:
            for recovery in [0,.5,1]:
                x=M.recycle_balance(I,P,recovery)
                self.assertAlmostEqual(x['fresh_CO2_kt_y']+x['recycled_kt_y'],I)
                self.assertAlmostEqual(x['fresh_CO2_kt_y'],x['conditional_retained_kt_y']+x['vented_CO2_kt_y'])
                self.assertAlmostEqual(x['conditional_retained_kt_y'],I-P)
            full=M.recycle_balance(I,P,1)
            self.assertEqual(full['vented_CO2_kt_y'],0);self.assertEqual(full['retained_over_fresh'],1)
        with self.assertRaises(ValueError):M.recycle_balance(100,101,1)

    def test_native_small_pair_refutes_universal_mean_intake_claim(self):
        d=M.load_inputs();rows=M.subset_screens(d['eor'],[3.36])
        pair=next(x for x in rows if x['fields']=='Lipovljani + Žutica' and x['basis']=='gross')
        self.assertAlmostEqual(pair['mean_Mt_y'],2.124);self.assertFalse(pair['meets_mean_target'])
        triple=next(x for x in rows if x['fields']=='Kloštar + Lipovljani + Žutica' and x['basis']=='net')
        self.assertAlmostEqual(triple['mean_Mt_y'],2.713);self.assertFalse(triple['meets_mean_target'])
        self.assertEqual(len(rows),112)

    def test_source_precision_and_ambiguous_value_stay_separate(self):
        d=M.load_inputs();checks,*_=M.calculate(d);values={x['item']:x['value'] for x in checks}
        self.assertAlmostEqual(values['Table2_DHF_total'],143.6)
        self.assertEqual(values['Figure11_integer_bar_total'],146)
        self.assertTrue(all(x['value'] for x in checks if x['item'].startswith('Figure11_rounding_')))
        self.assertIsNone(next(x for x in d['eor'] if x['name']=='Lipovljani')['emitted_min_kt_y'])
        self.assertFalse(any(x['item']=='range_Lipovljani_emitted' for x in checks))


if __name__=='__main__':unittest.main()
