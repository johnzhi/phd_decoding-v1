#!/usr/bin/env python3
"""B2-18 printed arithmetic and disclosed GIS/scenario/EOS components only.

No network. No author GIS, IAM arrays, pressure forecast or native model reproduced.
"""
from __future__ import annotations
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
import numpy as np
from scipy.interpolate import interp1d
from CoolProp.CoolProp import PropsSI

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/comprehensive_review'


def finite(values, *, nonnegative=False):
    if not values or any(not math.isfinite(x) or (nonnegative and x < 0) for x in values):
        raise ValueError('Finite values in the stated domain required')


def stock_from_bulk(volume_km3, coefficient_Gt_per_1000_km3):
    finite([volume_km3, coefficient_Gt_per_1000_km3], nonnegative=True)
    return volume_km3 * coefficient_Gt_per_1000_km3 / 1000


def temperature_potential(stock_Gt, tcre_C_per_1000Gt, fraction_available_for_net_CDR=1):
    finite([stock_Gt, tcre_C_per_1000Gt, fraction_available_for_net_CDR], nonnegative=True)
    if fraction_available_for_net_CDR > 1:
        raise ValueError('Available fraction must be at most one')
    return stock_Gt * tcre_C_per_1000Gt * fraction_available_for_net_CDR / 1000


def remaining_years(stock_Gt, used_Gt, rate_Gt_y):
    finite([stock_Gt, used_Gt, rate_Gt_y], nonnegative=True)
    if rate_Gt_y <= 0 or used_Gt > stock_Gt:
        raise ValueError('Positive rate and unexceeded stock required for this example')
    return (stock_Gt - used_Gt) / rate_Gt_y


def mask_sequence(weights, masks, order):
    finite(weights, nonnegative=True)
    if len(order) != len(masks) or set(order) != set(masks):
        raise ValueError('Order must contain each fixed mask exactly once')
    remaining = set(range(len(weights)))
    rows = []
    for name in order:
        cells = set(masks[name])
        if not cells <= set(range(len(weights))):
            raise ValueError('Mask cell outside grid')
        removed = sum(weights[i] for i in cells & remaining)
        remaining -= cells
        rows.append(dict(layer=name, removed=removed, remaining=sum(weights[i] for i in remaining)))
    return rows


def first_negative_year(years, values):
    """Disclosed convention: first integer negative after at least one positive.

    Native exact-zero/plateau, no-crossing and annual alignment remain unknown.
    """
    if len(years) != len(values) or len(years) < 2:
        raise ValueError('Two or more matched knots required')
    finite(list(years)); finite(list(values))
    if any(b <= a for a, b in zip(years, years[1:])) or any(int(x) != x for x in years):
        raise ValueError('Strictly increasing integer year knots required')
    annual = np.arange(years[0], years[-1] + 1, dtype=int)
    val = interp1d(years, values, kind='slinear')(annual)
    seen_positive = False
    for year, v in zip(annual, val):
        if v < 0 and seen_positive:
            return int(year)
        seen_positive |= bool(v > 0)
    return None


def extrapolate(years, rates, stock_Gt, used_Gt, end=2300):
    """Synthetic terminal-segment slinear extrapolation, no unreported floor.

    Strict discrete threshold: first annual cumulative value >= stock. Endpoint
    used_Gt already includes the final knot; future sum begins one year later.
    """
    if len(years) != len(rates) or len(years) < 2:
        raise ValueError('Two or more matched knots required')
    finite(list(years)); finite(list(rates), nonnegative=True)
    finite([stock_Gt, used_Gt], nonnegative=True)
    if any(b <= a for a, b in zip(years, years[1:])) or any(int(x) != x for x in years) or end <= years[-1] or used_Gt >= stock_Gt:
        raise ValueError('Increasing integer knots, later horizon and remaining stock required')
    annual = np.arange(years[-1] + 1, end + 1, dtype=int)
    raw = interp1d(years, rates, kind='slinear', fill_value='extrapolate')(annual)
    cumulative = used_Gt + np.cumsum(raw)
    rows = [dict(year=int(y), rate_Gt_y=float(q), cumulative_Gt=float(s)) for y, q, s in zip(annual, raw, cumulative)]
    crossing = next((r['year'] for r in rows if r['cumulative_Gt'] >= stock_Gt), None)
    return rows, crossing


def conditional_state(depth_m, surface_MPa, surface_C, gradient, water_density, g):
    finite([depth_m, surface_MPa, gradient, water_density, g], nonnegative=True)
    finite([surface_C])
    if min(depth_m, surface_MPa, water_density, g) <= 0:
        raise ValueError('Positive depth, pressure, water density and gravity required')
    t = surface_C + gradient * depth_m / 1000
    p = surface_MPa * 1e6 + water_density * g * depth_m
    rho_surface = PropsSI('D', 'P', surface_MPa * 1e6, 'T', surface_C + 273.15, 'CO2')
    rho = PropsSI('D', 'P', p, 'T', t + 273.15, 'CO2')
    return dict(depth_m=depth_m, surface_MPa_absolute=surface_MPa, temperature_C=t,
                pressure_MPa_absolute=p / 1e6, density_kg_m3=rho,
                surface_density_kg_m3=rho_surface, equal_mass_volume_reduction=rho / rho_surface,
                scope='Analyst hydrostatic pure-CO2 state; native surface pressure, fluids and density calculation unknown; not a field constraint')


def load_inputs():
    d = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B2-18.json').read_text())
    if hashlib.sha256((ROOT / d['source_path']).read_bytes()).hexdigest() != d['source_sha256']:
        raise ValueError('Stale source')
    return d


def calculate(d):
    checks = []
    def add(item, value, unit, scope):
        checks.append(dict(item=item, value=value, unit=unit, scope=scope))
    cases = {r['case']: r for r in d['stock_cases']}
    for name, r in cases.items():
        add(name + '_component_sum', r['onshore_Gt'] + r['offshore_Gt'], 'Gt', 'Printed Fig2b components, no guessed correction')
        add(name + '_sum_minus_total', r['onshore_Gt'] + r['offshore_Gt'] - r['total_Gt'], 'Gt', 'All totals/components rounded to .01 thousand Gt; 10 Gt lower-case difference is rounding compatible')
    add('central_onshore_fraction', cases['central']['onshore_Gt'] / cases['central']['total_Gt'] * 100, '%', 'Rounded display values support approximate 70/30 split')
    add('central_remaining_fraction', 1460 / 11780 * 100, '%', 'Stock ratio, not acceptance probability or annual availability')
    rings = []
    for ring in d['figure2c_rings']:
        s = sum(ring['values_Gt']); gap = s - ring['figure2b_comparator_Gt']
        # Five integer labels (+/- .5 each) and a .01-thousand-Gt comparator (+/-5).
        compatible = abs(gap) <= len(ring['values_Gt']) * .5 + 5
        rings.append(dict(**{k:v for k,v in ring.items() if k != 'values_Gt'}, sum_Gt=s, gap_Gt=gap,
                          rounding_compatible=compatible,
                          scope='Native label preserved; require region/case/label crosswalk and arrays; no automatic ring swap or correction'))
        add('Fig2c_' + ring['position'] + '_' + ring['ring'] + '_sum', s, 'Gt', 'Enlarged native labels, not author dataset reproduction')
    add('Fig2c_technical_total', sum(r['sum_Gt'] for r in rings if r['ring'] == 'outer_technical'), 'Gt', 'Five-region sums may omit territories; mapping not acquired')
    add('Fig2c_central_total', sum(r['sum_Gt'] for r in rings if r['ring'] == 'inner_central'), 'Gt', 'Not silently reconciled to 1460 Gt')
    coef = d['bulk_coefficient_Gt_per_1000_km3']; a = d['analyst']
    add('bulk_coefficient_kg_m3', coef * 1e12 / (1000 * 1e9), 'kg/m3 bulk', 'Effective aggregate coefficient includes borrowed pressure/50-year assumptions; not fluid density')
    add('bulk_coefficient_t_km3', coef * 1e9 / 1000, 't/km3 bulk', 'No pore fraction or new annual control inferred')
    toy_stock = stock_from_bulk(a['geometry_km2'] * a['assessed_thickness_km'], coef)
    add('analyst_geometry_stock', toy_stock * 1e9, 't', 'Synthetic 1km2 x 1.5km assessed sediment volume only')
    add('analyst_geometry_50yr_equivalent', toy_stock * 1e9 / d['coefficient_horizon_years'], 't/y', 'Arithmetic period average, NOT a pressure-constrained annual limit')
    temp = []
    for stock, tcre in itertools.product(d['sensitivity_stocks_Gt'], d['TCRE_C_per_1000Gt']):
        temp.append(dict(stock_Gt=stock, TCRE_C_per_1000Gt=tcre, temperature_C=temperature_potential(stock,tcre),
                         scope='Entire stock used for net CDR; assumes reversible linear climate response'))
    add('central_temperature_half_stock_for_CDR', temperature_potential(1460,.45,.5), 'degC', 'Disclosed 50% stock allocation, not actual climate outcome')
    add('historical_scale_ratio', d['net_zero_capture_Gt_y'] * 1000 / d['historical_capture_Mt_y'], 'ratio', 'Rounded 2024 capture capacity denominator, not observed injection flow')
    add('historical_scale_rounding_low', 8.65 * 1000 / 49.5, 'ratio', 'Assumes nearest .1Gt and1Mt rounding; source175 lies inside interval')
    add('historical_scale_rounding_high', 8.75 * 1000 / 48.5, 'ratio', 'No definite source175 arithmetic error established')
    add('basalt_cumulative', 1e-4 * 1e3, 'Mt', 'Cumulative since2014, not an annual operating limit')
    add('central_border_buffer', 6 * 1.852, 'km each side', 'Normative6nautical-mile terrestrial buffer, pressure plume may extend farther')
    add('border_sensitivity', 12 * 1.852, 'km each side', 'Full12nautical-mile sensitivity')
    add('analyst_remaining_at_NZ', remaining_years(1460,a['example_NZ_used_Gt'],a['example_rate_Gt_y']), 'years', 'Synthetic300Gt already used; not native scenario median')
    add('analyst_first_negative_year', first_negative_year(a['emission_years'],a['emissions_Gt_y']), 'year', 'Strict first integer negative convention, exact zero at2040 excluded; native convention unverified')
    sequences = []
    for order in itertools.permutations(a['masks']):
        sequences.append(dict(order=list(order), steps=mask_sequence(a['mask_weights'],a['masks'],order)))
    add('analyst_sum_standalone_mask_removals', sum(sum(a['mask_weights'][i] for i in cells) for cells in a['masks'].values()), 'synthetic weight', 'Overlapping masks double-count if standalone removals added')
    add('analyst_union_removed', sum(a['mask_weights'][i] for i in set().union(*[set(v) for v in a['masks'].values()])), 'synthetic weight', 'Union final exclusion independent of order only for same fixed masks/weights')
    scenarios = []
    for label, rates in [('rising',a['rising_rates_Gt_y']),('falling',a['falling_rates_Gt_y'])]:
        rows,crossing = extrapolate(a['extrapolation_years'],rates,a['stock_Gt'],a['already_used_Gt'])
        for r in rows:r['scenario']=label
        scenarios += rows
        add('analyst_' + label + '_crossing', crossing if crossing else 'not_crossed', 'calendar year', 'Synthetic >= threshold, cumulative annual sum; no native scenario replication')
        add('analyst_' + label + '_rate_2300', rows[-1]['rate_Gt_y'], 'Gt/y', 'Raw first-order extrapolation, no unreported floor')
        add('analyst_' + label + '_cumulative_2300', rows[-1]['cumulative_Gt'], 'Gt', 'Negative extrapolation illustrates missing-policy question, not proof native code allows negative storage')
    add('analyst_flat_remaining', remaining_years(a['stock_Gt'],a['already_used_Gt'],12), 'years', 'Flat endpoint rate differs from rising extrapolation')
    for years in a['leak_years']:
        add('analyst_retained_after_' + str(years), (1-a['leak_fraction_per_year'])**years * 100, '%', 'Single deposited cohort, constant compound leakage only; not continuous-injection/climate or measured-retention model')
    states = [conditional_state(z,p,a['surface_temperature_C'],a['geothermal_C_km'],a['hydrostatic_water_density_kg_m3'],a['g_m_s2']) for z,p in itertools.product(a['depths_m'],a['surface_pressures_MPa_absolute'])]
    return checks, rings, temp, sequences, scenarios, states


def main():
    d=load_inputs(); checks,rings,temp,sequences,scenarios,states=calculate(d);OUT.mkdir(parents=True,exist_ok=True)
    for suffix,rows in [('checks',checks),('rings',rings),('temperature',temp),('scenario_components',scenarios),('state_examples',states)]:
        p=OUT/f'B2-18_{suffix}.csv'
        with p.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    summary=dict(study_id='B2-18',checks=len(checks),ring_rows=len(rings),temperature_rows=len(temp),mask_sequences=sequences,synthetic_scenario_rows=len(scenarios),conditional_state_rows=len(states),
        all_ring_comparisons_rounding_compatible=all(r['rounding_compatible'] for r in rings),
        source_sha256=d['source_sha256'],original_GIS_IAM_models_reproduced=False,
        limits='Limited printed arithmetic and disclosed synthetic components. Native GIS masks, scenario arrays, code/SI, density basis, field pressure/rates, full utilities and climate response remain unverified. No operating/GHG input accepted.')
    (OUT/'B2-18_reproduction_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
