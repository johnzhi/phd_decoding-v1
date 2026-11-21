import importlib.util
import json
import math
from pathlib import Path
import unittest

from scipy.integrate import quad

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('interface',ROOT/'scripts/audit_pressure_interface.py')
interface=importlib.util.module_from_spec(spec)
spec.loader.exec_module(interface)


class PressureInterfaceChecks(unittest.TestCase):
    def test_lmtd_matches_integral_and_rejects_temperature_crossing(self):
        for a,b in ((10,20),(50,3),(12,12),(10+1e-10,10)):
            resistance=quad(lambda x:1/(b+(a-b)*x),0,1)[0]
            self.assertAlmostEqual(interface.lmtd(a,b),1/resistance,places=9)
            self.assertAlmostEqual(interface.lmtd(a,b),interface.lmtd(b,a),places=9)
        for a,b in ((0,10),(-2,10),(math.nan,1)):
            with self.assertRaises(ValueError):interface.lmtd(a,b)

    def test_spray_equation_closes_only_its_stated_mass_boundary(self):
        total,hot,target,liquid=10,430000,410000,200000
        spray=interface.spray_for_fixed_outlet(total,hot,target,liquid)
        hot_inlet=total-spray
        self.assertAlmostEqual(hot_inlet*hot+spray*liquid,total*target)
        fixed_inlet_spray=total*(hot-target)/(target-liquid)
        self.assertNotAlmostEqual(spray,fixed_inlet_spray)
        self.assertAlmostEqual(total*hot+fixed_inlet_spray*liquid,(total+fixed_inlet_spray)*target)
        with self.assertRaises(ValueError):interface.spray_for_fixed_outlet(10,400,450,200)

    def test_printed_heater_components_close_with_display_precision(self):
        data=interface.load_inputs();checks=interface.calculate(data)
        overlap=[r for r in checks if r['item'].endswith('_rounding_overlap')]
        self.assertEqual(len(overlap),18)
        self.assertTrue(all(r['value']==1 for r in overlap))
        self.assertAlmostEqual(interface.heater_area(15.9e6,2000,63.1),125.9904912837)
        self.assertAlmostEqual(interface.heater_cost(126,20)/interface.heater_cost(126,12),1.011187**8)
        with self.assertRaises(ValueError):interface.heater_area(1,0,20)

    def test_accounting_keeps_conflicts_and_signed_cooling_visible(self):
        data=interface.load_inputs();checks={r['item']:r for r in interface.calculate(data)}
        self.assertEqual(len(checks),196)
        self.assertEqual(checks['conditional_total_discharge_rate']['value'],1679)
        self.assertAlmostEqual(checks['LP8.5_MP16_Figure14_minus_Figure6_heat']['value'],6.1)
        self.assertEqual(data['rows'][4]['table7']['cooler_kW'],-47)
        self.assertEqual(data['rows'][5]['table7']['cooler_kW'],-18)
        self.assertLess(max(r['table4']['area_m2'] for r in data['rows']),data['assumptions']['heater_area_range_m2'][0])
        for r in data['rows']:
            t=r['table6']
            self.assertLess(abs(t['total_kW']*12*.11-t['cost_EUR']),1)
            self.assertLess(abs(t['total_kW']*12/t['liquid_t']-t['specific_label_kWel_per_t']),.05)
        cheaper=[r for k,r in checks.items() if k.endswith('_subcooling_minus_reliq_cost_per_t') and r['value']<0]
        self.assertEqual(len(cheaper),2)

    def test_reading_does_not_close_originals_or_native_model(self):
        review=json.loads((ROOT/'evidence/comprehensive_review/B1-20.json').read_text())
        bibliography=json.loads((ROOT/'evidence/comprehensive_review_inputs/B1-20_bibliography.json').read_text())
        self.assertEqual(review['text_read_pages'],list(range(1,16)))
        self.assertEqual(review['visually_inspected_pages'],list(range(1,16)))
        self.assertEqual(len(review['visuals']),29)
        self.assertEqual(len(review['equations']),12)
        self.assertEqual(review['references'],bibliography['entries'])
        self.assertEqual(bibliography['printed_entries'],19)
        self.assertEqual(len(review['references']),26)
        self.assertTrue(all(r['verification_status']=='unverified' for r in review['references']))
        self.assertEqual(review['overall_status'],'incomplete')
        result=json.loads((ROOT/'outputs/comprehensive_review/B1-20_reconciliation.json').read_text())
        self.assertFalse(result['native_COSSMOS_SRK_tank_transfer_control_compression_or_optimization_reproduced'])
        self.assertFalse(result['accepted_inputs_changed'])


if __name__=='__main__':unittest.main()
