import csv
import importlib.util
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    with (ROOT / path).open(encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


spec = importlib.util.spec_from_file_location('audit_diagnostics', ROOT / 'scripts/audit_diagnostics.py')
diagnostics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagnostics)
zhang_spec = importlib.util.spec_from_file_location('reproduce_zhang_lau_aquifers', ROOT / 'scripts/reproduce_zhang_lau_aquifers.py')
zhang = importlib.util.module_from_spec(zhang_spec)
zhang_spec.loader.exec_module(zhang)
simccs_spec = importlib.util.spec_from_file_location('audit_simccs_components', ROOT / 'scripts/audit_simccs_components.py')
simccs = importlib.util.module_from_spec(simccs_spec)
simccs_spec.loader.exec_module(simccs)
occs_spec = importlib.util.spec_from_file_location('audit_occ_sustainability', ROOT / 'scripts/audit_occ_sustainability.py')
occs = importlib.util.module_from_spec(occs_spec)
occs_spec.loader.exec_module(occs)
total_spec = importlib.util.spec_from_file_location('audit_total_efficiency', ROOT / 'scripts/audit_total_efficiency.py')
total = importlib.util.module_from_spec(total_spec)
total_spec.loader.exec_module(total)
ooi_spec = importlib.util.spec_from_file_location('reproduce_ooi_cascade', ROOT / 'scripts/reproduce_ooi_cascade.py')
ooi = importlib.util.module_from_spec(ooi_spec)
ooi_spec.loader.exec_module(ooi)
budiarto_spec = importlib.util.spec_from_file_location('audit_budiarto_fulltext', ROOT / 'scripts/audit_budiarto_fulltext.py')
budiarto = importlib.util.module_from_spec(budiarto_spec)
budiarto_spec.loader.exec_module(budiarto)


class ComprehensiveAuditChecks(unittest.TestCase):
    def test_total_efficiency_component_obeys_power_units_and_scale(self):
        # Analyst unit example only: 2kg/s fuel at20MJ/kg, 4MW preparation,
        # 6MW CCS and10MW net output. Not an inferred author process case.
        eta = total.total_efficiency(10, 2, 20, 2, 3, 2)
        self.assertAlmostEqual(eta, 10/50)
        self.assertAlmostEqual(total.total_efficiency(20, 4, 20, 2, 6, 2), eta)
        self.assertAlmostEqual(total.total_efficiency(10, 2, 20, 0, 0, 0), .25)
        self.assertLess(eta, .25)

    def test_total_efficiency_rounding_check_is_not_blanket_acceptance(self):
        results = total.sensitivity(total.load_inputs())
        self.assertEqual(len(results), 112)
        self.assertTrue(all(r['compatible_with_display_rounding'] for r in results))
        # A one-percentage-point error in a printed deviation must fail.
        data = total.load_inputs()
        data['sensitivity_series'][0]['eta_deviation_pct'][0] += 1
        self.assertFalse(total.sensitivity(data)[0]['compatible_with_display_rounding'])
        low, high = total.change_interval(30, 20)
        self.assertLess(low, 50)
        self.assertGreater(high, 50)

    def test_capture_mass_is_kept_distinct_from_conditional_avoidance(self):
        results = {r['item']:r for r in total.calculate(total.load_inputs())}
        self.assertAlmostEqual(results['UK_NG_captured_95pct']['value'], 3.3995303424)
        self.assertAlmostEqual(results['UK_NG_conditional_baseline_minus_vented']['value'], 2.6348375304)
        self.assertIn('CONDITIONAL', results['UK_NG_conditional_baseline_minus_vented']['unit'])
        self.assertNotEqual(results['UK_NG_captured_95pct']['value'], results['UK_NG_conditional_baseline_minus_vented']['value'])
        self.assertAlmostEqual(results['T6_UK_coal_extraction_100_implied_reference_efficiency']['value'], 56.8199532346)
        self.assertAlmostEqual(results['T6_UK_coal_extraction_100_drop_using_declared_design']['value'], 40.8918918919)

    def test_total_efficiency_visual_and_source_holds_remain_open(self):
        data = total.load_inputs()
        result = {r['item']:r for r in total.calculate(data)}
        self.assertAlmostEqual(result['F5_CSA-N.a.1_printed_share_sum']['value'], 111.9)
        self.assertTrue(any(v is None for row in data['share_labels'] for v in row['shares_pct']))
        review = json.loads((ROOT/'evidence/comprehensive_review/B1-03.json').read_text())
        self.assertEqual(review['text_read_pages'], list(range(1,14)))
        self.assertEqual(review['visually_inspected_pages'], list(range(1,14)))
        self.assertEqual(len(review['visuals']), 21)
        self.assertEqual(len(review['equations']), 15)
        self.assertEqual(len(review['references']), 94)
        self.assertTrue(all(r['verification_status']=='unverified' for r in review['references']))
        self.assertEqual(review['overall_status'], 'incomplete')
        self.assertIn('not_reproduced',review['original_model_status'])

    def test_occs_printed_fixed_opex_annuity_cancels_without_repair(self):
        data = occs.load_inputs()
        result = {r['item']:r for r in occs.calculate(data)}
        self.assertAlmostEqual(result['CAPEX_divided_by_TEC']['value'], 2.86425)
        self.assertAlmostEqual(result['PV_FOPEX_divided_by_CAPEX']['value'], .03)
        self.assertAlmostEqual(result['NPC_without_VOPEX_divided_by_CAPEX']['value'], 1.03)
        for rate,years in [(.04,10),(.08,25),(.12,40)]:
            present,recovery = occs.annuity_factors(rate,years)
            self.assertAlmostEqual(.03*recovery*present,.03)
        self.assertLess(result['annual_FOPEX_divided_by_CAPEX']['value'], .003)

    def test_occs_energy_units_preserve_avoided_basis_and_necessary_bounds(self):
        data = occs.load_inputs()
        result = {r['item']:r for r in occs.calculate(data)}
        self.assertAlmostEqual(result['one_kW_annual_direct_CO2']['value'],2.587032)
        self.assertAlmostEqual(result['AS_electric_kWh_per_t_avoided']['value'],950/3.6)
        self.assertEqual(result['AS_electric_kWh_per_t_avoided']['unit'],'kWh/t AVOIDED')
        self.assertEqual(result['AS_cold_duty_to_available']['value'],1)
        self.assertGreater(result['MS_cold_duty_to_available']['value'],9)
        self.assertGreater(result['PSA_cold_duty_to_available']['value'],6)
        self.assertIsNone(data['table7'][2]['electric_MJ_per_kg_avoided'])

    def test_non_crossing_marginal_CDFs_allow_paired_rank_inversion(self):
        data = occs.load_inputs()
        first = data['CDF_counterexample']['A_uniform_support']
        second = data['CDF_counterexample']['B_uniform_support']
        for i in range(-20,121):
            x = i/100
            self.assertGreaterEqual(occs.uniform_cdf(x,*first),occs.uniform_cdf(x,*second)-1e-14)
        self.assertAlmostEqual(occs.counterexample_inversion_probability(data),9/32)
        # A>.6 and B<.4 is a positive-probability inversion subset under independence.
        self.assertGreater((1-occs.uniform_cdf(.6,*first))*occs.uniform_cdf(.4,*second),0)
        self.assertIn('not author case',data['CDF_counterexample']['joint_assumption'])

    def test_occs_main_reading_does_not_close_missing_supplement_or_models(self):
        review = json.loads((ROOT/'evidence/comprehensive_review/B1-01.json').read_text())
        self.assertEqual(review['text_read_pages'],list(range(1,16)))
        self.assertEqual(review['visually_inspected_pages'],list(range(1,16)))
        self.assertEqual(len(review['visuals']),20)
        self.assertEqual([e['id'] for e in review['equations']],[f'E{i:02}' for i in range(1,15)]+['U01','U02'])
        self.assertEqual(len(review['references']),65)
        self.assertTrue(all(e['verification_status']=='unverified' for e in review['references']))
        self.assertIn('not_retained',review['supplement_status'])
        self.assertEqual(review['overall_status'],'incomplete')

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
        self.assertEqual(refs['R55']['verification_status'], 'primary_text_checked_partial_support_resource_not_annual_service')
        self.assertEqual(refs['R31']['verification_status'], 'primary_text_checked_support_with_case_cost_and_time_limits')
        self.assertTrue(all(r['verification_status'] == 'unverified' for k,r in refs.items() if k not in {'R31','R55'}))

    def test_simccs_pressure_interfaces_match_independent_SI_derivation(self):
        data = simccs.load_inputs()
        sample = data['analyst_unit_example']
        rho, mu = simccs.properties(data, 340, 25)
        self.assertAlmostEqual(rho, 748.2)
        self.assertAlmostEqual(mu, .0637)
        velocity = sample['mass_kg_s']/(rho*math.pi*sample['pipe_diameter_m']**2/4)
        darcy_pa = data['published_constants']['friction_factor']*rho*velocity**2*(sample['pipe_length_km']*1000)/(2*sample['pipe_diameter_m'])
        literal = simccs.pressure_drop_literal(data, sample['mass_kg_s'], rho, sample['pipe_length_km'], sample['pipe_diameter_m'])
        self.assertAlmostEqual(literal, darcy_pa)
        checks = {r['item']:r for r in simccs.diagnostics(data)}
        self.assertAlmostEqual(float(checks['Eq16_literal_numeric_output']['value'])/float(checks['Eq16_SI_pressure_expressed_MPa']['value']), 1e6)
        self.assertAlmostEqual(float(checks['Eq18_SI_head_expressed_MPa']['value']), 7.339842)

    def test_simccs_radial_units_convert_millipascal_to_megapascal(self):
        data = simccs.load_inputs()
        rho, mu_mPa = simccs.properties(data, 340, 25)
        # Independent Pa-based expression must agree with the printed MPa-based one.
        expected = 2*math.pi*100/7.5*1e-13*rho/(mu_mPa*1e-3)*(5*1e6)
        actual = simccs.radial_mass_kg_s(data, 100, 1e-13, rho, mu_mPa, 5)
        self.assertAlmostEqual(actual, expected)
        unconverted = 2*math.pi*100/7.5*1e-13*rho/mu_mPa*5
        self.assertTrue(math.isclose(actual/unconverted, 1e9, rel_tol=1e-12))

    def test_simccs_equation_reading_is_not_original_case_or_citation_completion(self):
        review = json.loads((ROOT / 'evidence/comprehensive_review/B3-44.json').read_text())
        self.assertEqual(review['text_read_pages'], list(range(1,10)))
        self.assertEqual(review['visually_inspected_pages'], list(range(1,10)))
        self.assertEqual([e['id'] for e in review['equations']], [f'E{i:02}' for i in range(1,24)]+['D01'])
        self.assertEqual(len(review['visuals']),7)
        self.assertEqual(len(review['references']),28)
        self.assertEqual(review['overall_status'],'incomplete')
        self.assertTrue(all(e['verification_status']=='unverified' for e in review['references']))
        self.assertIn('HOLD_MASS_BALANCE_INDEX',{e['status'] for e in review['issues']})

    def test_aquifer_component_reproduction_handles_units_and_net_thickness_once(self):
        data = zhang.load_inputs()
        result = zhang.calculate(data)
        self.assertEqual(len(result), 24)
        self.assertTrue(all(r['within_half_printed_unit'] for r in result))
        self.assertTrue(all(r['nearest_integer_Mt'] == r['reported_Mt'] for r in result))
        # Hand calculation: 1 km2 × 10 m × 500 kg/m3 × 20% × 2% = .02 Mt.
        self.assertAlmostEqual(float(zhang.resource_mt(1,10,500,20,2)), .02)
        south_mid = next(r for r in result if r['basin']=='South Sumatra' and r['case']=='mid')
        self.assertAlmostEqual(float(south_mid['independently_calculated_Mt']), 26953.92)
        self.assertNotAlmostEqual(float(south_mid['independently_calculated_Mt']), 26953.92*.3)

    def test_resource_provenance_check_does_not_join_anonymous_fields_or_close_references(self):
        data = zhang.load_inputs()
        result = zhang.reconciliation(data, zhang.calculate(data))
        self.assertEqual(float(result['candidate_parent_resource_sum_Mt']), 537.4)
        self.assertTrue(all(r['identity_status'].startswith('unconfirmed') for r in data['B4_06_capacity_candidates']))
        self.assertEqual(data['sector_label_conflict']['table5_p5']['iron_and_steel'],31.33)
        self.assertEqual(data['sector_label_conflict']['table13_p11']['iron_and_steel'],7.11)
        review = json.loads((ROOT/'evidence/comprehensive_review/B4-08.json').read_text())
        bibliography = json.loads((ROOT/'evidence/comprehensive_review_inputs/B4-08_bibliography.json').read_text())
        self.assertEqual(review['overall_status'],'incomplete')
        self.assertEqual(review['text_read_pages'],list(range(1,23)))
        self.assertEqual(review['visually_inspected_pages'],list(range(1,23)))
        self.assertEqual(len(review['visuals']),32)
        self.assertEqual(len(review['equations']),5)
        self.assertEqual(len(review['references']),232)
        self.assertEqual(bibliography['entry_count'],232)
        self.assertEqual([r['id'] for r in review['references']],[r['id'] for r in bibliography['entries']])
        self.assertTrue(all(r['verification_status']=='unverified' for r in review['references']))
        self.assertEqual([r['pages'] for r in bibliography['entries'] if r['id']=='R093'],[[19,20]])

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
