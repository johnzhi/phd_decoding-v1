import csv
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    with (ROOT / path).open(encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


spec = importlib.util.spec_from_file_location('audit_diagnostics', ROOT / 'scripts/audit_diagnostics.py')
diagnostics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagnostics)
ooi_spec = importlib.util.spec_from_file_location('reproduce_ooi_cascade', ROOT / 'scripts/reproduce_ooi_cascade.py')
ooi = importlib.util.module_from_spec(ooi_spec)
ooi_spec.loader.exec_module(ooi)
budiarto_spec = importlib.util.spec_from_file_location('audit_budiarto_fulltext', ROOT / 'scripts/audit_budiarto_fulltext.py')
budiarto = importlib.util.module_from_spec(budiarto_spec)
budiarto_spec.loader.exec_module(budiarto)


class ComprehensiveAuditChecks(unittest.TestCase):
    def test_retained_supplement_coverage_keeps_derivative_pages_and_blanks_separate(self):
        review = json.loads((ROOT / 'evidence/comprehensive_review/B4-06.json').read_text())
        self.assertEqual(review['text_read_pages'], list(range(1,21)))
        self.assertEqual(review['visually_inspected_pages'], list(range(1,21)))
        self.assertEqual(len(review['supplement_items']), 13)
        self.assertEqual(len({r['id'] for r in review['supplement_items']}), 13)
        asset = review['asset_reviews'][0]
        self.assertEqual(asset['derivative_pages'], 5)
        self.assertFalse(asset['derivative_pages_included_in_main_page_count'])
        cells = rows('data/supplement_annual_injection.csv')
        self.assertEqual(sum(bool(r['reported_value_mtpa']) for r in cells), 250)
        self.assertEqual(sum(r['cell_status'] == 'BLANK_NOT_NUMERIC_ZERO' for r in cells), 470)
        self.assertEqual(review['overall_status'], 'incomplete')

    def test_fixed_early_source_mass_exceeds_reported_service_without_an_escape_term(self):
        inputs = budiarto.load_inputs()
        result = {r['check']:r for r in budiarto.calculate(inputs)}
        self.assertAlmostEqual(float(result['source_rate_sum']['value']), 5.327)
        self.assertAlmostEqual(float(result['source_mass_30_bins']['value']), 159.81)
        self.assertGreater(float(result['source_rate_sum']['value']), inputs['early_SW_A_reported_injection_limit_Mt_per_year'])
        self.assertAlmostEqual(float(result['early_fixed_source_necessary_shortfall']['value']), 3.277)
        self.assertEqual({r['scope'] for r in result.values()}, {'diagnostic_not_independent_MILP_or_physical_service'})

    def test_published_cost_discrepancies_are_preserved_without_fabricated_corrections(self):
        result = {r['check']:r for r in budiarto.calculate(budiarto.load_inputs())}
        self.assertEqual([float(result[s+'_figure11_full_minus_components']['value']) for s in ['SW-A','MW-A','MW-D']], [1.92,3.54,3.9])
        self.assertAlmostEqual(float(result['source_weighted_capture_cost']['value']), 94.44293035479632)
        self.assertAlmostEqual(float(result['scenario_mean_transport_reduction']['value']), 34.06940063091483)
        self.assertAlmostEqual(float(result['SW-A_map_reservoir_total']['value']), 153.21)
        self.assertAlmostEqual(float(result['MW-A_map_reservoir_total']['value']), 159.81)
        self.assertAlmostEqual(float(result['MW-D_map_reservoir_total']['value']), 159.81)
        self.assertIsNone(budiarto.load_inputs()['figure9_MW_D_reservoir_totals_Mt']['r3'])

    def test_budiarto_citation_candidates_are_not_promoted_or_substituted(self):
        review = json.loads((ROOT / 'evidence/comprehensive_review/B4-06.json').read_text())
        self.assertEqual([r['id'] for r in review['references']], [f'R{i:02}' for i in range(1,59)])
        refs = {r['id']:r for r in review['references']}
        self.assertEqual(refs['R31']['retained_candidate'], 'B3-44')
        self.assertEqual(refs['R55']['retained_candidate'], 'B4-08')
        self.assertIn('different title/year/DOI', refs['R14']['related_but_not_substituted'])
        self.assertTrue(all(r['verification_status'] == 'unverified' for r in refs.values()))

    def test_page_inventory_closes_without_duplicate_or_automatic_review(self):
        sources = {r['study_id']: r for r in rows('data/source_catalogue.csv') if not r['duplicate_of']}
        papers = {r['study_id']: r for r in rows('outputs/comprehensive_review/papers.csv')}
        pages = rows('outputs/comprehensive_review/pages.csv')
        self.assertEqual(set(sources), set(papers))
        self.assertEqual(len(papers), 92)
        self.assertEqual(len(pages), 1301)
        self.assertEqual(len({(r['study_id'], r['physical_page']) for r in pages}), 1301)
        for sid, source in sources.items():
            subset = [r for r in pages if r['study_id'] == sid]
            self.assertEqual({int(r['physical_page']) for r in subset}, set(range(1, int(source['pages'])+1)))
            self.assertTrue(all(r['source_sha256'] == source['sha256'] for r in subset))
            if not papers[sid]['manual_record']:
                self.assertTrue(all(r['text_read'] == 'False' and r['visually_inspected'] == 'False' for r in subset))
        self.assertTrue(all(p['audit_status'] != 'complete' for p in papers.values()))

    def test_manual_records_do_not_certify_external_sources_or_models(self):
        summary = json.loads((ROOT / 'outputs/comprehensive_review/summary.json').read_text())
        self.assertEqual(summary['comprehensively_complete_papers'], 0)
        manual = [json.loads(path.read_text()) for path in (ROOT / 'evidence/comprehensive_review').glob('*.json')]
        self.assertGreaterEqual(len(manual), 3)
        self.assertEqual(summary['manual_records'], len(manual))
        self.assertEqual(summary['text_read_pages'], sum(len(r['text_read_pages']) for r in manual))
        self.assertEqual(summary['visually_inspected_pages'], sum(len(r['visually_inspected_pages']) for r in manual))
        b102 = json.loads((ROOT / 'evidence/comprehensive_review/B1-02.json').read_text())
        self.assertEqual(len(b102['references']), 15)
        self.assertEqual(next(r for r in b102['issues'] if r['id'] == 'I01')['status'], 'HOLD_UNIT')
        b405 = json.loads((ROOT / 'evidence/comprehensive_review/B4-05.json').read_text())
        self.assertEqual(len(b405['equations']), 15)
        self.assertEqual(len(b405['references']), 11)
        self.assertIn('not_reproduced', b405['original_model_status'])

    def test_chemical_balance_check_detects_missing_hydrogen(self):
        balanced = diagnostics.reaction_residual([(1, 'CO2'), (4, 'H2')], [(1, 'CH4'), (2, 'H2O')])
        self.assertTrue(all(value == 0 for value in balanced.values()))
        unbalanced = diagnostics.reaction_residual([(1, 'CO2'), (3, 'H2')], [(1, 'CH4'), (2, 'H2O')])
        self.assertEqual(unbalanced['H'], 2)
        self.assertTrue(all(value == 0 for atom, value in unbalanced.items() if atom != 'H'))

    def test_printed_load_constraint_does_not_enforce_actual_concentration(self):
        # Test the source's equation, not a reconstructed full optimiser.
        delivered, q_source, capacity, q_limit = 1000, 4600, 6727, 1250
        self.assertLessEqual(delivered*q_source, capacity*q_limit)
        self.assertGreater(delivered*q_source, delivered*q_limit)
        self.assertGreater(min([4600, 5000, 2600]), max([1250, 2500]))
        self.assertLess(8460+9483, 6000+12000+8000)
        self.assertLess(8000/2, 6000)  # outage upper bound conflicts with unchanged base lower bound

    def test_diagnostics_stay_separate_and_keep_annualisation_explicit(self):
        diagnostics.validate_sources()
        result = {r['item']: r for r in diagnostics.diagnostics()}
        self.assertAlmostEqual(result['C08_difference']['value'], 7.294117647058824)
        self.assertAlmostEqual(result['I03_calendar']['value'], 4.7304)
        self.assertEqual(result['F06_topgas_branch_residual']['value'], 100)
        self.assertEqual(result['strict_quality_minimum_supply_gap']['value'], 8057)
        self.assertTrue(all(r['status'] == 'unverified_discovery_candidate'
                            for r in rows('outputs/comprehensive_review/discovery_candidates.csv')))

    def test_independent_cascade_reconstructs_targets_with_explicit_source_lag(self):
        data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B3-11.json').read_text())
        years = data['table6_years']
        supply = ooi.annual_rates(data['reservoirs'], years, lag=1)
        demand = ooi.annual_rates(data['plants'], years)
        additional, carry = ooi.cascade(supply, demand)
        self.assertEqual(supply, data['table6_supply'])
        self.assertEqual(demand, data['table6_demand'])
        self.assertEqual(carry, data['table6_feasible_cascade'])
        self.assertEqual((additional, carry[-1]), (40, 80))
        self.assertEqual(sum(supply), 1240)
        self.assertEqual(sum(demand), 1200)
        self.assertEqual(carry[years.index(8)], 0)
        self.assertEqual(ooi.annual_rates(data['reservoirs'], [3,4], lag=1), [0,40])
        self.assertEqual(ooi.hypothetical_target(data), dict(additional_storage_Mt=200,
                         excess_storage_Mt=100, matched_internal_storage_Mt=500))

    def test_literal_allocation_conflicts_are_not_hidden_by_aggregate_closure(self):
        data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B3-11.json').read_text())
        first = ooi.allocation_audit(data, 7)
        second = ooi.allocation_audit(data, 8)
        self.assertEqual(first['printed_allocation_total_Mt'], 1260)
        self.assertEqual(first['required_total_Mt'], 1200)
        self.assertEqual(first['plant_year_mismatches'][0]['difference_Mt'], 60)
        self.assertEqual(second['printed_allocation_total_Mt'], second['required_total_Mt'])
        self.assertEqual([(r['plant'], r['year'], r['difference_Mt']) for r in second['plant_year_mismatches']],
                         [('coal_A',8,-20), ('coal_A',10,-40), ('coal_B',21,60)])
        self.assertEqual(second['reservoir_audit']['B']['allocated_Mt'], 680)
        self.assertEqual(second['reservoir_audit']['B']['printed_capacity_Mt'], 660)
        self.assertEqual(first['reservoir_audit']['A']['rate_limit_exceedance_years'], {'6':60, '7':60})

    def test_one_checked_citation_does_not_close_its_own_reference_chain(self):
        citing = json.loads((ROOT / 'evidence/comprehensive_review/B4-05.json').read_text())
        cited = json.loads((ROOT / 'evidence/comprehensive_review/B3-11.json').read_text())
        edge = next(item for item in citing['references'] if item['id'] == 'R08')
        self.assertEqual(edge['verification_status'], 'primary_text_checked_partial_support_method_attribution_conflict')
        self.assertEqual(len(cited['references']), 25)
        self.assertEqual(cited['overall_status'], 'incomplete')
        self.assertIn('not pressure-constrained', json.loads(
            (ROOT / 'outputs/comprehensive_review/B3-11_reproduction.json').read_text())['interpretation'])


if __name__ == '__main__':
    unittest.main()
