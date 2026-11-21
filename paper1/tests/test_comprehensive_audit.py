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


class ComprehensiveAuditChecks(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
