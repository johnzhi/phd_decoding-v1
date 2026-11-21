#!/usr/bin/env python3
"""Independent CSCA calculation; audit literal allocations without repairing them."""
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/comprehensive_review'


def cascade(supply, demand):
    running = 0
    raw = []
    for source, sink in zip(supply, demand, strict=True):
        running += source-sink
        raw.append(running)
    additional = max(0, -min([0, *raw]))
    feasible = [value+additional for value in raw]
    return additional, feasible


def annual_rates(segments, years, lag=0):
    return [sum(rate for _, start, end, rate, _ in segments if start+lag <= year <= end+lag)
            for year in years]


def allocation_audit(inputs, option):
    allocations = inputs[f'table{option}_allocations']
    delivered, required, stored = defaultdict(float), defaultdict(float), defaultdict(float)
    for plant, start, end, rate, _ in inputs['plants']:
        for year in range(start, end+1):
            required[plant, year] += rate
    for plant, reservoir, start, end, rate in allocations:
        for year in range(start, end+1):
            delivered[plant, year] += rate
            stored[reservoir, year] += rate
    mismatches = [dict(plant=plant, year=year, required_Mt=required[plant, year],
                       delivered_Mt=delivered[plant, year],
                       difference_Mt=delivered[plant, year]-required[plant, year])
                  for plant, year in sorted(set(delivered) | set(required))
                  if delivered[plant, year] != required[plant, year]]
    capacity = {reservoir: dict(allocated_Mt=sum(value for (site, _), value in stored.items() if site == reservoir),
                               printed_capacity_Mt=total,
                               rate_limit_exceedance_years={str(year): value for (site, year), value in stored.items()
                                                           if site == reservoir and value > rate})
                for reservoir, _, _, rate, total in inputs['reservoirs']}
    return dict(option=option, printed_allocation_total_Mt=sum(delivered.values()),
                required_total_Mt=sum(required.values()), plant_year_mismatches=mismatches,
                reservoir_audit=capacity, scope='literal table replay; not corrected or physically validated scheduling')


def hypothetical_target(inputs):
    plants = inputs['hypothetical_plants']
    reservoirs = inputs['hypothetical_reservoirs']
    events = sorted({point for _, start, end, _, _ in plants for point in (start, end)} |
                    {year for _, year, _ in reservoirs})
    # Check the left limit before each reservoir opens; demand is continuous.
    deficits = [sum(max(0, min(year, end)-start)*rate for _, start, end, rate, _ in plants)
                -sum(mass for _, opens, mass in reservoirs if opens < year) for year in events]
    additional = max([0, *deficits])
    excess = additional+sum(mass for _, _, mass in reservoirs)-sum(mass for _, _, _, _, mass in plants)
    return dict(additional_storage_Mt=additional, excess_storage_Mt=excess,
                matched_internal_storage_Mt=sum(mass for _, _, _, _, mass in plants)-additional)


def plot_cascade(years, supply, demand, feasible, additional):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 1, figsize=(8.5, 6.5), sharex=True, layout='constrained')
    axes[0].step(years, supply, where='mid', label='Storage-service increment', color='#0072B2')
    axes[0].step(years, demand, where='mid', label='Captured-CO₂ demand', color='#D55E00')
    axes[0].set_ylabel('Mt per annual bin')
    axes[0].legend(loc='upper left', frameon=False)
    axes[0].set_title('Ooi et al. (2013): independent Table 6 reconstruction')
    axes[1].step(years, [v-additional for v in feasible], where='mid', label='Without external service', color='#D55E00')
    axes[1].step(years, feasible, where='mid', label=f'With {additional:g} Mt external service', color='#0072B2')
    axes[1].axhline(0, color='0.3', linewidth=0.8)
    axes[1].set_ylabel('Cumulative service balance (Mt)')
    axes[1].set_xlabel('Published annual time step (year)')
    axes[1].legend(loc='upper left', frameon=False)
    for ax in axes:
        ax.grid(alpha=0.2)
        ax.spines[['top', 'right']].set_visible(False)
    fig.supxlabel('Bankable service accounting; does not establish injection-rate feasibility', fontsize=9)
    for suffix in ('png', 'pdf'):
        fig.savefig(OUT / f'B3-11_cascade.{suffix}', dpi=180)
    plt.close(fig)


def main():
    inputs = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B3-11.json').read_text())
    path = ROOT / 'papers/B3-11.pdf'
    if hashlib.sha256(path.read_bytes()).hexdigest() != inputs['source_sha256']:
        raise ValueError('Stale Ooi source/transcription')
    years = inputs['table6_years']
    # Explicit source convention p5: developed atTk, usable atTk+1.
    supply = annual_rates(inputs['reservoirs'], years, lag=1)
    demand = annual_rates(inputs['plants'], years)
    additional, feasible = cascade(supply, demand)
    if supply != inputs['table6_supply'] or demand != inputs['table6_demand'] or feasible != inputs['table6_feasible_cascade']:
        raise ValueError('Independent cascade does not match the manually transcribed Table6')
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / 'B3-11_cascade.csv').open('w', newline='') as stream:
        fields = ['year', 'storage_service_increment_Mt', 'demand_Mt', 'net_Mt', 'feasible_carry_Mt']
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for year, source, sink, carry in zip(years, supply, demand, feasible, strict=True):
            writer.writerow(dict(zip(fields, [year, source, sink, source-sink, carry], strict=True)))
    result = dict(study_id='B3-11', source_sha256=inputs['source_sha256'],
                  hypothetical_case=hypothetical_target(inputs),
                  additional_storage_Mt=additional, excess_storage_Mt=feasible[-1],
                  table6_all_19_rows_match=True, source_lag_years=1,
                  injection_rate_feasibility_established=False,
                  interpretation='Bankable storage-service cascade, not pressure-constrained reservoir injection.',
                  allocation_audits=[allocation_audit(inputs, option) for option in (7, 8)])
    (OUT / 'B3-11_reproduction.json').write_text(json.dumps(result, indent=2)+'\n')
    plot_cascade(years, supply, demand, feasible, additional)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
