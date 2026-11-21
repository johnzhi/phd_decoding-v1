#!/usr/bin/env python3
"""B1-16 source arithmetic and explicitly analyst-defined NRMS examples.

No native survey processing, saturation inversion, reservoir model, predictive
validation, detection probability, retained carbon or safe-rate model reproduced.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B1-16.json').read_text())
    if hashlib.sha256((ROOT / data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale Decatur monitoring source')
    return data


def conventional_nrms_percent(a, b):
    """Conventional analyst metric; paper's exact formula is not established."""
    if not a or len(a) != len(b) or not all(math.isfinite(x) for x in list(a) + list(b)):
        raise ValueError('Matched finite nonempty traces required')
    rms = lambda x: math.sqrt(sum(value * value for value in x) / len(x))
    denominator = rms(a) + rms(b)
    if denominator == 0:
        raise ValueError('Both-zero normalisation undefined')
    return 200 * rms([y - x for x, y in zip(a, b)]) / denominator


def gain_for_nrms_example(percent):
    """Choose the >1 amplitude-gain branch of the analyst scalar example."""
    if not 0 <= percent < 200:
        raise ValueError('Finite gain branch requires percentage in[0,200)')
    return (200 + percent) / (200 - percent)


def calculate(data):
    rows = []

    def add(item, value, unit, locator, interpretation, status='limited_source_arithmetic'):
        rows.append(dict(item=item, value=value, unit=unit, source_locator=locator,
                         calculation_status=status, interpretation=interpretation,
                         scope='not_native_monitoring_or_reservoir_model_or_accepted_service_retention_GHG_input'))

    injection = data['injection']
    add('nominal_goal_rate', injection['goal_t'] / injection['goal_years'], 't/year TARGET', 'Introduction p2',
        'Goal divided by planned duration, not observed annual flow, maximum service or a safe injection control.')
    add('reported_injected_fraction_of_goal', injection['reported_injected_t_approx'] / injection['goal_t'], 'fraction of project goal', 'Introduction p2',
        'Approximate reported cumulative injection, not a retained-carbon fraction.')
    add('goal_minus_reported_injection', injection['goal_t'] - injection['reported_injected_t_approx'], 't to goal under approximate reported mass', 'Introduction p2',
        'No actual completion date, annual injection limit or post-injection retention inferred.')
    milestones = data['monitoring']['VSP_cumulative_milestones_t_approx']
    for i, mass in enumerate(milestones):
        add('VSP_monitor_' + str(i+1) + '_fraction_of_goal', mass / injection['goal_t'], 'fraction of goal at cumulative snapshot', 'Section4.4 p3',
            'Milestones are approximate cumulative stocks; no survey calendar or independent injection quantity inferred.')
        if i:
            add(f'VSP_monitor_{i}_to_{i+1}_mass_increment', mass - milestones[i-1], 't between cumulative snapshots', 'Section4.4 p3',
                'Difference of cumulative values only, not an annual rate or extra mass to add to the final cumulative total.')
    add('sum_of_VSP_cumulative_snapshots_minus_latest', sum(milestones) - milestones[-1], 't DOUBLE-COUNT if snapshots were added', 'Section4.4 p3',
        'Diagnostic of a prohibited stock-flow interpretation, not a source discrepancy.', 'analyst_stock_flow_counterexample')

    geology = data['geology']
    for label in ('seal', 'MtSimon'):
        converted = geology[label + '_thickness_ft_approx'] * .3048
        add(label + '_thickness_from_ft', converted, 'm', 'Section2 p2', 'Unit conversion of rounded source values, not a geometry repair.')
        add(label + '_converted_minus_printed_m', converted - geology[label + '_thickness_m_approx'], 'm DIFFERENCE', 'Section2 p2',
            'Displayed rounding only; not a measurement error estimate.')
    add('reported_baffle_depth_interval', geology['baffle_depth_m'][1] - geology['baffle_depth_m'][0], 'm vertical interval', 'Section2 p2',
        'Approximate reported interval, not verified regional lateral extent or an impermeable seal.')
    geometry = data['geometry']
    for item, value, unit in [('CCS1_perforation_span', geometry['CCS1_perforation_m'][1] - geometry['CCS1_perforation_m'][0], 'm span'),
                              ('CCS1_sensor_to_perforation_top_interval', geometry['CCS1_perforation_m'][0] - geometry['CCS1_sensor_depth_m'], 'm'),
                              ('CCS1_sensor_to_perforation_bottom_interval', geometry['CCS1_perforation_m'][1] - geometry['CCS1_sensor_depth_m'], 'm'),
                              ('GM1_array_vertical_span', geometry['GM1_geophone_m'][1] - geometry['GM1_geophone_m'][0], 'm measured-depth span'),
                              ('VW2_array_vertical_span', geometry['VW2_geophone_m'][1] - geometry['VW2_geophone_m'][0], 'm measured-depth span'),
                              ('GM1_offset_from_ft', geometry['GM1_offset_west_ft'] * .3048, 'm converted from197ft')]:
        add(item, value, unit, 'Section3 pp2–3', 'Geometry/unit arithmetic only; not an actual BHP correction, regular geophone spacing or inferred pressure communication.')
    for port in data['pressures']:
        candidate = port['figure4_depth_ft'] * .3048
        add(f'zone{port["zone"]}_figure_depth_converted', candidate, 'm candidate from figure label', 'Figure4 p9',
            'Literal figure candidate only. Depth datum and well/port identity must be verified before replacing prose or calibrating pressure.')
        if port['prose_depth_m'] is not None:
            add(f'zone{port["zone"]}_figure_candidate_minus_prose', candidate - port['prose_depth_m'], 'm DIFFERENCE', 'Section4.2 / Figure4',
                'Zone4 discrepancy is far beyond ordinary one-foot/one-metre display rounding; no automatic correction.')
    zone4 = next(port for port in data['pressures'] if port['zone'] == 4)
    add('zone4_prose_minus_figure_depth_ft', zone4['prose_depth_ft'] - zone4['figure4_depth_ft'], 'ft DIFFERENCE', 'Section4.2 / Figure4',
        '6982 versus6838ft preserved; the plotted candidate is not certified as the correct datum.')
    add('one_psi_in_MPa', 6894.757293168 / 1e6, 'MPa per psi', 'Figure4 units / standard conversion',
        'Conversion does not determine gauge/absolute pressure or put different-depth ports on a common reference.', 'unit_identity')
    add('initial_CCS1_interval_top_shallower_than_baffle_top', geology['baffle_depth_m'][0] - data['RST']['first_CCS1_reported_m'][0], 'm interval-label DIFFERENCE', 'Sections2,4.1 / conclusions',
        'Literal interval wording needs native log/significance/datum clarification; no leaked mass or contradiction resolution is invented.')

    monitoring = data['monitoring']
    groups = [monitoring[key] for key in ('PreMtSimon_ports', 'MtSimon_ports', 'IrontonGalesville_ports')]
    add('port_partition_matches_11_labels', int(sorted(sum(groups, [])) == list(range(1, monitoring['ports_total'] + 1))), 'boolean0/1', 'Section3 p3',
        'Label partition only, not every-port sampling completeness or independent observations.')
    add('July2013_chemistry_sampled_zone_labels', len(monitoring['July2013_sampled_zones']), 'zones', 'Section4.3 p3',
        'Known CO2-bearing zones2/3 are excluded. Count does not establish detection limits or reservoir mass coverage.')
    for item, value, unit in [('RST_stated_baseline_plus_monitor_count', monitoring['RST_baselines'] + monitoring['RST_monitor_runs'], 'stated survey runs'),
                              ('VSP_baseline_plus_monitor_count', monitoring['VSP_baselines'] + monitoring['VSP_monitors'], 'stated surveys'),
                              ('fluid_baseline_plus_full_or_partial_round_count', monitoring['fluid_baseline_rounds'] + monitoring['fluid_full_or_partial_rounds'], 'rounds of unequal coverage')]:
        add(item, value, unit, 'Sections4.1,4.3,4.4 p3', 'Do not multiply by all wells/ports to infer independent complete samples; July2014 RST was still being analysed.')
    for label in ('unaffected', 'anomaly'):
        interval = data['VSP'][label + '_window_m']
        add('VSP_' + label + '_window_span', interval[1] - interval[0], 'm depth window', 'Section4.4 / Figure5',
            'Window thickness is not wave-propagation resolution, CO2 plume thickness or mapped mass.')

    trace = data['analyst_examples']['baseline_trace']
    for gain in data['analyst_examples']['gain_examples']:
        add(f'analyst_NRMS_gain_{gain:g}', conventional_nrms_percent(trace, [gain * x for x in trace]), '% in analyst metric', 'analyst conventional NRMS example; source metric unverified',
            'Same reference with amplitude scaling alone; no reservoir saturation or CO2 mass assigned. Not a replay of the author survey.', 'analyst_NRMS_counterexample')
    for percent in data['VSP']['reported_unaffected_NRMS_percent']:
        gain = gain_for_nrms_example(percent)
        add(f'analyst_positive_gain_for_NRMS_{percent:g}', gain, 'positive amplitude ratio EXAMPLE', 'analyst conventional NRMS algebra',
            'Nonunique interpretation example, not attribution of the observed survey anomaly to amplitude gain.', 'analyst_NRMS_counterexample')
        add(f'analyst_positive_gain_NRMS_{percent:g}_replay', conventional_nrms_percent(trace, [gain * x for x in trace]), '% in analyst metric', 'analyst conventional NRMS algebra',
            'Reconstructs the chosen example percentage; does not establish source processing or saturation/mass.', 'analyst_NRMS_counterexample')
    old = data['analyst_examples']['fraction_example_old']
    factor = 1 + data['microseismic']['reported_more_locatable_percent_approx'] / 100
    add('conditional_locatable_fraction_example_after', old * factor, 'example fraction of detected events', 'Section4.5 / explicit analyst example',
        '50% relative improvement could map .4 to .6; actual fractions/denominator and geometry effects remain unknown.', 'analyst_catalogue_denominator_example')
    add('conditional_old_fraction_upper_for_relative_factor', 1 / factor, 'fraction under fnew=factor*fold<=1', 'analyst probability bound',
        'Not an inferred old completeness, total events or quantitative risk reduction.', 'analyst_catalogue_denominator_example')
    return rows


def main():
    data = load_inputs()
    rows = calculate(data)
    output = ROOT / 'outputs/comprehensive_review'
    with (output / 'B1-16_checks.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    result = dict(study_id='B1-16', source_sha256=data['source_sha256'], check_count=len(rows), figures=7, separately_numbered_tables=0,
                  printed_numbered_equations=0, analyst_identities=8, native_models_reproduced=False, underlying_originals_verified=0,
                  accepted_inputs_changed=False, missing=data['missing'],
                  interpretation='Source arithmetic, unit/geometry checks and analyst conventional NRMS examples only. No native RST/VSP/geochemical/microseismic interpretation, reservoir prediction, retention fraction, risk probability, maximum annual service or matched GHG inventory reproduced.')
    (output / 'B1-16_reconciliation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
