#!/usr/bin/env python3
"""Check B1-03's displayed arithmetic without inventing missing author inputs.

Rounding compatibility is conditional on rounding to the displayed precision;
it is not a measurement error model. Captured mass and conditional avoided
mass are deliberately separate. No output is an accepted Paper1 input.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/comprehensive_review'


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B1-03.json').read_text())
    if hashlib.sha256((ROOT / data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale total-efficiency source')
    return data


def total_efficiency(power_mw, fuel_kg_s, lhv_mj_kg, prep_mj_kg,
                     captured_kg_s, ccs_mj_kg):
    """Eq15 in consistent MJ/s units; unavailable case intensities stay absent."""
    return power_mw / (fuel_kg_s * (lhv_mj_kg + prep_mj_kg)
                       + captured_kg_s * ccs_mj_kg)


def relative_change(modified, baseline):
    return 100 * (modified / baseline - 1)


def change_interval(modified, baseline, half_unit=.005):
    if baseline <= half_unit:
        raise ValueError('Positive denominator interval required')
    return (relative_change(modified-half_unit, baseline+half_unit),
            relative_change(modified+half_unit, baseline-half_unit))


def sensitivity(data):
    rows = []
    for series in data['sensitivity_series']:
        for metric in ('eta', 'drop'):
            baseline = series[metric][1]
            for slot, index in enumerate((0, 2)):
                modified = series[metric][index]
                reported = series[metric + '_deviation_pct'][slot]
                low, high = change_interval(modified, baseline)
                rows.append(dict(table=series['table'], physical_page=series['page'],
                                 country=series['country'], fuel=series['fuel'], stage=series['stage'],
                                 metric=metric, input_factor_pct=(85, 115)[slot],
                                 baseline_displayed_pct=baseline, modified_displayed_pct=modified,
                                 reported_relative_deviation_pct=reported,
                                 calculated_from_displayed_pct=relative_change(modified, baseline),
                                 conditional_rounding_low_pct=low, conditional_rounding_high_pct=high,
                                 compatible_with_display_rounding=(low <= reported+.005+1e-12
                                                                   and high >= reported-.005-1e-12),
                                 scope='printed_arithmetic_only_not_original_sensitivity_model'))
    return rows


def calculate(data):
    rows = []
    def add(item, value, unit, locator, interpretation):
        rows.append(dict(item=item, value=value, unit=unit, source_locator=locator,
                         interpretation=interpretation,
                         scope='diagnostic_only_not_author_case_or_accepted_operating_GHG_input'))
    seconds = data['year_days']*86400*data['capacity_factor']
    capture_fraction = data['reference_capture_fraction']
    add('operating_seconds_90pct_capacity_factor', seconds, 's/year', 'p6/p9',
        '365-day accounting convention for the stated90% capacity factor; not90% capture.')
    for fuel, case in data['fuels'].items():
        for name in ('design_efficiency_fraction', 'grid_generator_efficiency_fraction'):
            power = case['baseline_fuel_kg_s']*case['LHV_MJ_kg']*case[name]
            add(f'{fuel}_baseline_power_using_{name}', power, 'MW', 'p4/p5; Eq10',
                f"Compare stated per-unit {case['unit_power_MW']}MW; neither per-unit nor four-unit closure assumed.")
    for flow in data['reference_flows_95']:
        tag = flow['country']+'_'+flow['fuel']
        case = data['fuels'][flow['fuel']]
        generated = flow['generated_CO2_kg_s']
        ratio = generated/flow['fuel_kg_s']
        add(tag+'_generated_CO2_per_fuel', ratio, 'kgCO2/kgfuel', 'p6 versus Table4 p8',
            'Coal body flows imply approximately44/12, whereas Table4 uses3.39. No composition repair.')
        add(tag+'_captured_95pct', generated*capture_fraction*seconds/1e9, 'Mt/year CAPTURED', 'p6 reference flows',
            'Matches the scale of reported3.4/7.9 annual savings; capture is not avoided baseline emissions.')
        baseline = case['baseline_fuel_kg_s']*case['table4_generated_CO2_per_fuel']
        avoided = (baseline-(1-capture_fraction)*generated)*seconds/1e9
        add(tag+'_conditional_baseline_minus_vented', avoided, 'Mt/year CONDITIONAL arithmetic',
            'p5 baseline fuel; p6 flows; Table4 p8 yields',
            'Diagnostic only: these published values may not share power/composition boundaries. Not validated avoidance or lifecycle GHG.')
    add('p9_NG_annual_claim_per_900MW', 3.6e3/900, 'kt/MW/year', 'p9; p4 unit power',
        'Equals reported4; annual claim is on a single-unit scale, not all four900MW units.')
    add('p9_coal_annual_claim_per_600MW', 8.43e3/600, 'kt/MW/year', 'p9; p4 unit power',
        'Equals reported14.05; plant/unit scope requires clarification.')
    for phase, kw in data['table3_phase_power_kW'].items():
        add('Table3_'+phase+'_specific_electricity', kw/1000/data['table3_phase_flow_kg_s'],
            'MJe/kgCO2', 'Table3 p5',
            'Paired power/flow conversion only. Conditions and primary-source model not independently verified.')
    for mw in data['table3_other_case_power_MW']:
        add(f'Table3_other_case_{mw}MW_specific_electricity', mw/data['table3_other_case_flow_kg_s'],
            'MJe/kgCO2', 'Table3 p5 Wu/Li row',
            'Different31.7kg/s process case; not pooled with1.5kg/s phase comparisons.')
    for series in data['sensitivity_series']:
        tag = f"T{series['table']}_{series['country']}_{series['fuel']}_{series['stage']}"
        for index, factor in enumerate((85, 100, 115)):
            eta, drop = series['eta'][index], series['drop'][index]
            implied = eta/(1-drop/100)
            declared = data['fuels'][series['fuel']]['design_efficiency_fraction']*100
            add(f'{tag}_{factor}_implied_reference_efficiency', implied, '%',
                f"Table{series['table']} p{series['page']}",
                'Inverse of reported relative drop, not an author-model reconstruction.')
            add(f'{tag}_{factor}_drop_using_declared_design', 100*(1-eta/declared), '% relative loss',
                f"p4 and Table{series['table']} p{series['page']}",
                'Conditional comparison using the printed57%NG/37%coal design references. No corrected published result asserted.')
    for share in data['share_labels']:
        values = [v for v in share['shares_pct'] if v is not None]
        add(f"F{share['figure']}_{share['case']}_printed_share_sum", sum(values), '%',
            f"Figure{share['figure']} p{share['page']}",
            'All four labels printed; ordinary rounding alone permits +/-0.2 percentage points.'
            if share['all_four_labels_printed'] else
            'Processing label omitted by source for<0.6%; this subtotal is not a complete partition test.')
    return rows


def write_rows(path, rows):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    data = load_inputs()
    OUT.mkdir(parents=True, exist_ok=True)
    checks, deviations = calculate(data), sensitivity(data)
    write_rows(OUT / 'B1-03_diagnostics.csv', checks)
    write_rows(OUT / 'B1-03_sensitivity.csv', deviations)
    print(f'{len(checks)} diagnostics; {len(deviations)} displayed deviations checked; '
          f'{sum(not r["compatible_with_display_rounding"] for r in deviations)} outside conditional rounding intervals. '
          'Original author cases remain unreproduced.')


if __name__ == '__main__':
    main()
