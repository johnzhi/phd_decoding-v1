import csv
import hashlib
import json
from decimal import Decimal
from pathlib import Path
import sys
import unittest
from zipfile import ZipFile

import fitz

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import public_evidence_followup as public


class PublicEvidenceChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = public.verify_sources()
        cls.history = public.read_csv('data/public_reservoir_history.csv')
        cls.capture = public.read_csv('data/public_capture_values.csv')
        cls.inventory = public.read_csv('data/public_capture_inventory.csv')
        cls.audit = json.loads((ROOT/'outputs/public_reservoir_audit.json').read_text())

    def test_complete_native_input_closure_and_retained_bytes(self):
        source = next(x for x in self.manifest['files'] if x['source_id']=='PUB-BJARMELAND')
        with ZipFile(ROOT/source['path']) as z:
            for name in self.audit['includes_resolved']:
                self.assertIn('Bjarmeland/'+name, z.namelist())
            self.assertEqual(len(z.namelist()), 9)
            data = z.read('Bjarmeland/CO2_BJ_C07B9.DATA').decode('latin1').splitlines()
            for p in public.read_csv('data/public_reservoir_parameters.csv'):
                self.assertIn(p['source_token'], data[int(p['line_1based'])-1])
            # Source completion warning and solver warnings must remain visible.
            self.assertEqual(len(self.audit['warnings']), 7)
            self.assertIn('Completion ignored', self.audit['warnings'][0]['text'])

    def test_pressure_limited_history_is_paired_and_keeps_standard_volume(self):
        h=self.history
        self.assertEqual(len(h),4951)
        self.assertEqual(h[0]['time_days'],'1.000000')
        self.assertEqual(h[-1]['time_days'],'18263.00')
        self.assertEqual(h[0]['WGIR_GI'],'902592.4')
        self.assertEqual(h[0]['WBHP_GI'],'225.0000')
        self.assertEqual(h[-1]['WGIT_GI'],'2.74E+10')
        self.assertEqual(self.audit['records_at_pressure_ceiling'],6)
        self.assertEqual(self.audit['records_above_pressure_ceiling'],0)
        self.assertEqual(self.audit['rate_unit'],'SM3/DAY')
        for a,b in zip(h,h[1:]):
            self.assertLess(Decimal(a['time_days']),Decimal(b['time_days']))
            self.assertLessEqual(Decimal(a['WGIT_GI']),Decimal(b['WGIT_GI']))
        for x in h:
            self.assertEqual(x['FGIR'],x['WGIR_GI'])
            self.assertEqual(x['FGIT'],x['WGIT_GI'])
            self.assertLessEqual(Decimal(x['WBHP_GI']),225)
        self.assertFalse(self.audit['independently_rerun'])
        self.assertFalse(self.audit['mass_conversion_performed'])
        self.assertFalse(self.audit['maximum_service_curve_generated'])

    def test_table_cells_remain_located_and_cases_are_not_cross_paired(self):
        self.assertEqual(len(self.capture),42)
        source=next(x for x in self.manifest['files'] if x['source_id']=='PUB-CEMCAP')
        with fitz.open(ROOT/source['path']) as pdf:
            for x in self.capture:
                page=pdf[int(x['physical_page'])-1]
                cell=fitz.Rect(json.loads(x['cell_bbox']))
                # Bounding-box extraction is independent of the table reader.
                self.assertIn(x['source_token'],page.get_textbox(cell))
                self.assertEqual(x['use_as_regional_calibrated_input'],'False')
        design=next(x for x in self.inventory if 'typical_air' in x['case_id'])
        self.assertEqual(design['heat_gj_per_t_captured'],'3.832')
        self.assertEqual(design['cooling_gj_per_t_captured'],'4.909')
        self.assertEqual(design['steam_pressure_bara'],'2.45')
        self.assertAlmostEqual(float(design['electricity_kwh_per_t_captured']),126.69444444444444)
        for x in self.inventory:
            self.assertAlmostEqual(float(x['capture_aux_kwh_per_t_captured'])+float(x['compression_kwh_per_t_captured']),float(x['electricity_kwh_per_t_captured']))
            self.assertEqual(x['heat_electricity_pair_complete_as_reported'],'True')
            self.assertEqual(x['full_lifecycle'],'False')
            self.assertEqual(x['eligible_for_regional_lca'],'False')

    def test_reporting_factor_calculation_has_no_cooling_or_capture_double_charge(self):
        factors={x['value_id']:float(x['value']) for x in public.read_csv('data/reference_inventory_inputs.csv')}
        for x in self.inventory:
            expected=float(x['heat_gj_per_t_captured'])*factors['JP_R8_heat_fallback']*1000+float(x['electricity_kwh_per_t_captured'])*factors['JP_R8_electric_fallback']*1000
            self.assertAlmostEqual(float(x['jp_reporting_utility_kgco2_per_t']),expected)
        summary=json.loads((ROOT/'outputs/public_evidence_summary.json').read_text())
        self.assertFalse(summary['complete_lca_generated'])
        self.assertFalse(summary['existing_operational_results_changed'])


if __name__=='__main__':
    unittest.main()
