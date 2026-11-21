#!/usr/bin/env python3
"""Independently reconstruct Eq.5, not pressure-limited storage service.

Uses only the visually checked Table18 bulk inputs and Table4 efficiencies.
Published densities are inputs: their calculator/EOS is not reproduced here.
Native sources and accepted Paper1 operating inputs are never rewritten.
"""
import csv
import hashlib
import json
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/comprehensive_review'


def load_inputs():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B4-08.json').read_text())
    if hashlib.sha256((ROOT / 'papers/B4-08.pdf').read_bytes()).hexdigest() != data['source_sha256']:
        raise ValueError('Stale Zhang/Lau source')
    return data


def resource_mt(area_km2, net_sand_m, density_kg_m3, porosity_percent, efficiency_percent):
    """Eq.5: convert area, two percentages and kg to Mt exactly once."""
    values = [D(str(v)) for v in (area_km2, net_sand_m, density_kg_m3,
                                 porosity_percent, efficiency_percent)]
    area, net_sand, density, porosity, efficiency = values
    if min(values) <= 0 or porosity > 100 or efficiency > 100:
        raise ValueError('Positive quantities and percentage units are required')
    return area * D(10)**6 * net_sand * density * porosity/100 * efficiency/100 / D(10)**9


def calculate(data):
    rows = []
    for basin in data['table18']:
        for case, efficiency in data['table4_efficiency_percent'].items():
            value = resource_mt(basin['area_km2'], basin['net_sand_m'], basin['density_kg_m3'],
                                basin['porosity_percent'], efficiency)
            reported = D(str(basin['table12_reported_Mt'][case]))
            rows.append(dict(basin=basin['basin'], case=case, efficiency_percent=efficiency,
                             independently_calculated_Mt=str(value), reported_Mt=str(reported),
                             calculated_minus_reported_Mt=str(value-reported),
                             nearest_integer_Mt=str(value.quantize(D('1'), rounding=ROUND_HALF_UP)),
                             within_half_printed_unit=abs(value-reported) <= D('.5'),
                             source_locator='Eq.5 p5; Table4 p4; Table12 p9; Table18 p18',
                             scope='independent_bulk_resource_component_not_pressure_service'))
    return rows


def reconciliation(data, rows):
    totals = {}
    for case in data['table4_efficiency_percent']:
        subset = [r for r in rows if r['case'] == case]
        totals[case] = dict(calculated_sum_Mt=str(sum(D(r['independently_calculated_Mt']) for r in subset)),
                            sum_of_printed_basin_rows_Mt=str(sum(D(r['reported_Mt']) for r in subset)),
                            printed_table12_total_Mt=data['table12_reported_total_Mt'][case])
    candidates = data['B4_06_capacity_candidates']
    return dict(source_sha256=data['source_sha256'], outputs=len(rows),
                all_24_basin_values_match_at_integer_Mt=all(r['within_half_printed_unit'] for r in rows),
                totals=totals,
                candidate_parent_resource_sum_Mt=str(sum(D(str(r['reported_resource_Mt'])) for r in candidates)),
                candidate_field_identities='unconfirmed; same basin/type/capacity only; not an explicit parent field join',
                peninsular_malaysia_sector_conflict=data['sector_label_conflict'],
                figure8b=dict(printed_mean_Mt='121.9', printed_n=57,
                             gas_plus_oil_table_total_Mt='6716',
                             table_total_divided_by_printed_n_Mt=str(D(6716)/57),
                             status='basis_unresolved; not a corrected histogram'),
                interpretation='Eq.5 bulk-resource component reproduced from published rounded inputs. '
                'No pressure, injection-rate, operational, EOS, complete field-by-field, financial or GHG model reproduced. '
                'Half a printed unit is a display-rounding comparison, not a measured uncertainty bound. '
                'Totals use different aggregation/display stages; preserve source totals, do not silently repair them.')


def main():
    data = load_inputs()
    rows = calculate(data)
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / 'B4-08_aquifer_reproduction.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    (OUT / 'B4-08_reconciliation.json').write_text(json.dumps(reconciliation(data, rows), indent=2)+'\n')
    print(f'Reconstructed {len(rows)} basin/scenario resource values; annual deliverability remains unestablished.')


if __name__ == '__main__':
    main()
