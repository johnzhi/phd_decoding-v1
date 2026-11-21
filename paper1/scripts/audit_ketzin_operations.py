#!/usr/bin/env python3
"""B1-17 source checks and its stated hypothetical hydrostatic recurrence.

Pure-CO2 single-phase columns use the pinned HEOS/Span-Wagner backend, standard
gravity and the reported linear geotherm. Stop at the first liquid/gas branch
crossing: no undocumented two-phase density/quality rule is invented. These
columns are not the native monitoring, ASPEN correction or reservoir-test fit.
"""
import csv
from datetime import date
import gzip
import hashlib
import io
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B1-17.json').read_text())
    if hashlib.sha256((ROOT / data['source_path']).read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale Ketzin operations source')
    return data


def gauge_to_absolute(pressure_bar, assumed_atmosphere_bar=1):
    if not all(math.isfinite(x) for x in (pressure_bar, assumed_atmosphere_bar)) or assumed_atmosphere_bar <= 0:
        raise ValueError('Finite gauge reading and positive atmosphere required')
    return pressure_bar + assumed_atmosphere_bar


def hydrostatic_upward_step(pressure_Pa, density_kg_m3, distance_m, gravity=9.80665):
    if not all(math.isfinite(x) for x in (pressure_Pa, density_kg_m3, distance_m, gravity)):
        raise ValueError('Finite SI inputs required')
    if min(pressure_Pa, density_kg_m3, gravity) <= 0 or distance_m < 0:
        raise ValueError('Positive pressure/density/gravity and nonnegative distance required')
    result = pressure_Pa - density_kg_m3 * gravity * distance_m
    if result <= 0:
        raise ValueError('Column reached nonpositive absolute pressure')
    return result


def integrate_column(site, properties, step_m=.1, gravity=9.80665, surface_C=8):
    """Return successful nodes and explicit completion/blocker state.

    properties(P_Pa,T_K) returns (rho_kg_m3, phase_name). An opaque EOS failure
    is retained; a gas/liquid switch halts before that branch is used to march.
    """
    depth = site['depth_m']
    if not math.isfinite(step_m) or step_m <= 0 or depth <= 0:
        raise ValueError('Positive finite step and depth required')
    pressure = site['pressure_bar'] * 1e5
    rows = []
    old_phase = None
    for index in range(math.ceil(depth / step_m) + 1):
        z = max(0, depth - index * step_m)
        temperature = surface_C + (site['temperature_C'] - surface_C) * z / depth
        try:
            density, phase = properties(pressure, temperature + 273.15)
        except ValueError as error:
            return rows, dict(status='blocked_EOS_state', at_depth_m=z, temperature_C=temperature,
                              pressure_bar=pressure / 1e5, reason=str(error), surface_pressure_bar=None)
        node = dict(site=site['site'], depth_m=z, temperature_C=temperature, pressure_bar=pressure / 1e5,
                    density_kg_m3=density, phase=phase)
        if old_phase is not None and {old_phase, phase} == {'liquid', 'gas'}:
            return rows, dict(status='blocked_unspecified_two_phase_closure', at_depth_m=z,
                              temperature_C=temperature, pressure_bar=pressure / 1e5,
                              previous_phase=old_phase, candidate_phase=phase,
                              candidate_density_kg_m3=density, surface_pressure_bar=None,
                              reason='Explicit step crossed liquid/gas branches. Source does not specify mixture quality, interface or phase handling; no continued physical two-phase profile claimed.')
        rows.append(node)
        if z == 0:
            return rows, dict(status='single_phase_recurrence_completed_under_disclosed_backend',
                              surface_pressure_bar=pressure / 1e5, surface_density_kg_m3=density,
                              bottom_density_kg_m3=rows[0]['density_kg_m3'], nodes=len(rows))
        old_phase = phase
        pressure = hydrostatic_upward_step(pressure, density, min(step_m, z), gravity)
    raise RuntimeError('March did not terminate')


def source_checks(data):
    rows = []

    def add(item, value, unit, locator, interpretation, status='limited_source_arithmetic'):
        rows.append(dict(item=item, value=value, unit=unit, source_locator=locator,
                         calculation_status=status, interpretation=interpretation,
                         scope='not_native_reservoir_test_monitoring_or_accepted_service_retention_GHG_input'))

    op, plant, measurement = data['operation'], data['plant'], data['measurement']
    add('oxyfuel_share_of_reported_mass', op['oxyfuel_mass_t'] / op['mass_t'] * 100, '% of reported injected mass', 'Sections1–2 pp1,3',
        'Source origin share only; purity basis/composition and avoided or retained-carbon inventory are not inferred.')
    add('nominal_plant_setpoint', op['plant_setpoint_max_kg_h'] / 1000, 't/h equipment setpoint', 'Section2 pp2–3',
        'Equipment limit, not pressure-constrained reservoir maximum.')
    add('conditional_365day_plant_setpoint_mass', op['plant_setpoint_max_kg_h'] * data['analyst_examples']['annual_reference_hours'] / 1000,
        't per8760h at uninterrupted setpoint EXAMPLE', 'Section2 / explicit calendar example',
        'No downtime, actual yearly injection or maximum safe annual service inferred.', 'analyst_equipment_calendar_example')
    add('combined_tank_nominal_capacity', plant['tanks'] * plant['tank_capacity_t_each'], 't nameplate', 'Section2 p2',
        'Not available buffer, cargo or actual tank fill history.')
    add('delivered_to_desired_temperature_difference', plant['desired_injection_T_C_approx'] - plant['delivered_T_C'], 'K nominal endpoints', 'Section2 p2',
        'Not heat duty: enthalpy, phase, pressure, ambient heat and losses are missing.')
    add('conditional_heater_max_over_plant_max', plant['electric_heater_kWmax'] / (op['plant_setpoint_max_kg_h'] / 1000),
        'kWh/t only IF both nameplates coincide', 'Section2 / explicit equipment-ratio example',
        'Not reported utility intensity; ambient preheating and actual operating power unavailable.', 'analyst_nameplate_ratio_not_inventory')
    add('monthly_mean_rate_decrease', op['mean_monthly_early_t'] - op['mean_monthly_later_t'], 't/month difference', 'Section4.1 p4',
        'Different monitored periods and research schedules; not a calibrated permeability or annual-service penalty.')
    add('monthly_mean_relative_decrease', 100 * (1 - op['mean_monthly_later_t'] / op['mean_monthly_early_t']), '% of earlier mean', 'Section4.1 p4',
        'No causal rate/safety or availability factor adopted.')
    add('initial_to_day5_pressure_increase', op['after5days_bara_approx'] - op['initial_pressure_bara_approx'], 'bar approximate', 'Section4.1 p4',
        'Reported injection response, not a fracture/BHP limit or injectivity model.')
    add('sensor_to_injection_reference_interval', measurement['injection_reference_m'] - measurement['downhole_gauge_m'], 'm', 'Section3.3 p3',
        '80m here is distinct from B1-14’s550-to640m correction.')
    add('constant_2bar_correction_implied_mean_density', measurement['paper_approximate_BHP_increment_bar'] * 1e5 /
        (data['analyst_examples']['gravity_m_s2'] * (measurement['injection_reference_m'] - measurement['downhole_gauge_m'])),
        'kg/m3 under uniform-column identity', 'Section3.3 / analyst identity',
        'Dimensional interpretation only; not a measured density or the native ASPEN/Peng-Robinson calculation.', 'analyst_uniform_column_diagnostic')
    add('5min_to_example5s_interval_ratio', measurement['SCADA_mean_minutes'] * 60 / measurement['example_Fig3A_raw_seconds'], 'interval ratio', 'Section3 / Figure3A',
        'SCADA averaging versus special5s example; no complete60-sample population or full5s archive independently established.')
    add('nominal_DTS_profiles_per_day_if_continuous', 24 * 60 / measurement['DTS_interval_minutes'], 'profiles/day conditional', 'Section3.2 p3',
        'Sampling cadence only, not independent observations, actual uptime or a failure probability.')
    add('P300_reported_pressure_range_span', data['P300']['pressure_range_bara'][1] - data['P300']['pressure_range_bara'][0], 'bar', 'Section4.2 p4',
        'No correlated response detected in the reported record; no leakage detection or zero-transfer bound supplied.')
    tests = data['tests']
    test_mass_t = sum(tests['stage_rates_kg_h']) * tests['injection_hours_per_stage'] / 1000
    for item, value, unit in [('isochronal_four_stage_injection_mass', test_mass_t, 't prescribed stages'),
                              ('isochronal_four_stage_total_duration', len(tests['stage_rates_kg_h']) * (tests['injection_hours_per_stage'] + tests['shutin_hours_per_stage']), 'h'),
                              ('isochronal_stage_injection_time_fraction', tests['injection_hours_per_stage'] / (tests['injection_hours_per_stage'] + tests['shutin_hours_per_stage']), 'test-time fraction'),
                              ('four_cycle_duration', tests['cycles'] * tests['days_per_cycle'], 'days test schedule'),
                              ('four_cycle_date_elapsed', (date.fromisoformat(tests['cyclic_dates'][1]) - date.fromisoformat(tests['cyclic_dates'][0])).days, 'elapsed days'),
                              ('cyclic_observer_to_injector_pressure_span_ratio', tests['cyclic_observer_pressure_span_bar_approx'] / tests['cyclic_injector_pressure_span_bar_approx'], 'approximate response-span ratio')]:
        add(item, value, unit, 'Section4.4 / Figure5', 'Research test arithmetic only. Inclusive56-day date convention is compatible; no annual availability, pressure-transfer function or safe maximum inferred.')
    for arrival in data['arrivals']:
        end = date.fromisoformat(arrival['GMS_date'])
        for label, start in [('continuous', op['continuous_start']), ('comparison_June24', data['analyst_examples']['compared_start_date'])]:
            add(arrival['well'] + '_elapsed_from_' + label, (end - date.fromisoformat(start)).days, 'elapsed calendar days', 'Section4.5 / source calendar comparison',
                'Continuous injection began June30 after commissioning injections. Dates and first-detection clocks differ; sensor150m depth adds delay. No exact21.7day timer or native arrival model reproduced.')
    for entry in data['logging_table']:
        if entry['Ktzi201'] is not None and entry['Ktzi200'] is not None:
            add('logging_' + entry['date_as_printed'] + '_201_minus_200_pressure', entry['Ktzi201'][0] - entry['Ktzi200'][0], 'bar DIFFERENCE', 'Table1 p4',
                'Different630/620m depths and potentially different campaign days; not synchronized pressure loss or an actual common-datum correction.')
    for site in data['hypothetical_sites']:
        add(site['site'] + '_assumed_temperature_depth_gradient', (site['temperature_C'] - 8) / site['depth_m'], 'K/m', 'Table2 / Section5.4 pp9–10',
            'Linear8C surface geotherm in hypothetical pure-CO2 well, not measured current site thermal profile.')
        add(site['site'] + '_initial_pressure_over_temperature_above_surface', site['pressure_bar'] / (site['temperature_C'] - 8), 'bar/K ratio', 'Table2 / Figure8',
            'Approximate2.3/3.2 groups are not exact pressure-depth laws, fracture limits or transferable phase-depth thresholds.')
    return rows


def figure_endpoint_candidates():
    """Read three displayed curve endpoints; these are vector-graphic candidates.

    No curve fitting to computed outputs. Tick calibration and path identifiers
    are recorded. Bezier endpoints are display geometry, not native model data.
    """
    import fitz
    with fitz.open(ROOT / 'papers/B1-17.pdf') as doc:
        drawings = doc[9].get_drawings()
    x0 = drawings[9]['rect'].x0
    y0 = drawings[13]['rect'].y0
    y300 = drawings[10]['rect'].y0
    # Tick endpoints are found from the lower axis rather than text glyph centres.
    ticks = [d['rect'].x0 for d in drawings if d['rect'].width < .01 and 671 < d['rect'].y0 < 672 and d['rect'].height > 2]
    x120 = max(ticks)
    mappings = [('In Salah', 5, 0), ('Weyburn', 6, 0), ('Snovhit', 6, 1)]
    result = []
    for name, path, curve in mappings:
        point = drawings[path]['items'][curve][1]
        result.append(dict(site=name, PDF_path_index=path, PDF_curve_index=curve, x_pt=point.x, y_pt=point.y,
                           temperature_C=(point.x - x0) / (x120 - x0) * 120,
                           pressure_bar=(y0 - point.y) / (y0 - y300) * 300,
                           calibration=dict(x0=x0, x120=x120, y0=y0, y300=y300),
                           interpretation='SourceFig8 displayed Bezier endpoint; approximate graphic comparison only, not native author array',
                           analyst_comparison_tolerance_bar=2))
    return result


def main():
    import CoolProp
    import CoolProp.CoolProp as CP
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    data = load_inputs()
    out = ROOT / 'outputs/comprehensive_review'
    checks = source_checks(data)
    with (out / 'B1-17_checks.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(checks[0]), lineterminator='\n')
        writer.writeheader();writer.writerows(checks)
    phase_names = {getattr(CP, name): name.removeprefix('iphase_') for name in dir(CP) if name.startswith('iphase_')}
    state = CP.AbstractState('HEOS', 'CO2')

    def properties(pressure, temperature):
        state.update(CP.PT_INPUTS, pressure, temperature)
        return state.rhomass(), phase_names[state.phase()]

    profiles, results, refinements = [], [], []
    names = ['In Salah', 'Sleipner', 'Weyburn', 'Snovhit']
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for site in [next(site for site in data['hypothetical_sites'] if site['site'] == name) for name in names]:
        rows, status = integrate_column(site, properties)
        profiles.extend(rows)
        status.update(site=site['site'], step_m=.1, successful_nodes=len(rows))
        results.append(status)
        ax.plot([r['temperature_C'] for r in rows], [r['pressure_bar'] for r in rows],
                '--' if 'blocked' in status['status'] else '-', label=site['site'] + (' (phase closure open)' if 'blocked' in status['status'] else ''))
        ax.scatter([site['temperature_C']], [site['pressure_bar']], s=22)
        for step in (.2, .05):
            refined_rows, refined_status = integrate_column(site, properties, step_m=step)
            refinements.append(dict(site=site['site'], step_m=step, status=refined_status['status'],
                                    surface_pressure_bar=refined_status['surface_pressure_bar'],
                                    surface_difference_from_0_1m_bar=(refined_status['surface_pressure_bar'] - status['surface_pressure_bar'])
                                    if refined_status['surface_pressure_bar'] is not None and status['surface_pressure_bar'] is not None else None,
                                    halt_depth_m=refined_status.get('at_depth_m')))
    # Pure-fluid saturation boundary is independently calculated, not copied art.
    temperatures = [8 + i * (30.95 - 8) / 200 for i in range(201)]
    ax.plot(temperatures, [CP.PropsSI('P', 'T', t + 273.15, 'Q', 0, 'CO2') / 1e5 for t in temperatures], ':', color='gray', label='Pure-CO2 saturation boundary')
    endpoints = figure_endpoint_candidates()
    for point in endpoints:
        status = next(r for r in results if r['site'] == point['site'])
        point['computed_minus_displayed_endpoint_bar'] = status['surface_pressure_bar'] - point['pressure_bar']
        point['within_analyst_graphic_tolerance'] = abs(point['computed_minus_displayed_endpoint_bar']) <= point['analyst_comparison_tolerance_bar']
        ax.scatter(point['temperature_C'], point['pressure_bar'], marker='+', c='black', s=60)
    ax.set(xlabel='Temperature (°C)', ylabel='Absolute pressure (bar; model interpretation)',
           title='Independent implementation of B1-17 hypothetical columns')
    ax.grid(alpha=.2);ax.legend(fontsize=8)
    fig.text(.12, .015, 'Surface 8°C; reported linear geotherms; 0.1 m explicit steps; HEOS CO2; g=9.80665 m/s².\nSleipner halts at the first liquid/gas branch crossing. Black +: approximate source-figure endpoints.', fontsize=8)
    fig.tight_layout(rect=(0,.065,1,1))
    fig.savefig(out / 'B1-17_columns.png', dpi=180);plt.close(fig)
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(profiles[0]), lineterminator='\n')
    writer.writeheader();writer.writerows(profiles)
    (out / 'B1-17_columns.csv.gz').write_bytes(gzip.compress(buffer.getvalue().encode(), mtime=0))
    result = dict(study_id='B1-17', source_sha256=data['source_sha256'], limited_check_count=len(checks),
                  model_scope='Independent stated hypothetical pure-CO2 hydrostatic recurrence; single-phase domain only; no native author code, dynamic reservoir, monitoring or safety model reproduced',
                  software=dict(CoolProp=CoolProp.__version__, gitrevision=CP.get_global_param_string('gitrevision'),
                                backend='HEOS', fluid='CO2', EOS_BibTeX=CP.get_fluid_param_string('CO2', 'BibTeX-EOS')),
                  disclosed_assumptions=dict(gravity_m_s2=9.80665, pressure_table_interpreted_as_absolute_for_EOS=True,
                                             surface_temperature_C=8, source_step_m=.1,
                                             two_phase_rule='halt at first liquid/gas crossing; no imposed quality or saturation clipping'),
                  columns=results, refinement_checks=refinements, profile_rows=len(profiles), graphic_endpoint_checks=endpoints,
                  failed_exploratory_run=data['hydrostatic_model']['exploratory_unrestricted_failure'],
                  full_native_models_reproduced=False, accepted_inputs_changed=False, missing=data['missing'])
    (out / 'B1-17_reconciliation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: result[key] for key in ('study_id','limited_check_count','profile_rows','columns','refinement_checks','graphic_endpoint_checks')}, indent=2))


if __name__ == '__main__':
    main()
