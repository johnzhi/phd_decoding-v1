#!/usr/bin/env python3
"""Full-text/supplement consistency diagnostics, not an author MILP reproduction.

Never supplies missing kr,t, solves a guessed flowsheet, repairs a source figure,
or changes accepted Paper1 inputs. Figure11 averages may use different bases;
their differences are questions for reconciliation, not inferred author errors.
"""
import csv
import hashlib
import json
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/comprehensive_review'


def read_csv(path):
    with (ROOT / path).open(encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


def load_inputs():
    inputs = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B4-06.json').read_text())
    for path, expected in [('papers/B4-06.pdf', inputs['source_sha256']),
                           ('original/supplements/43979_2025_135_MOESM1_ESM.docx', inputs['supplement_sha256'])]:
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Stale Budiarto audit source: {path}')
    return inputs


def calculate(inputs):
    sources = read_csv('data/supplement_sources.csv')
    reservoirs = read_csv('data/supplement_reservoirs.csv')
    source = sum(D(row['co2_rate_mtpa']) for row in sources)
    unit_cost = sum(D(row['co2_rate_mtpa'])*D(row['capture_cost_usd_per_t']) for row in sources)/source
    rows = []

    def add(name, value, unit, locator, interpretation):
        rows.append(dict(check=name, value=str(value), unit=unit, source_locator=locator,
                         interpretation=interpretation, scope='diagnostic_not_independent_MILP_or_physical_service'))

    add('source_rate_sum', source, 'Mt/year', 'TableS1, all14 rows', 'Reported source-mass basis; no second90% capture multiplier applied.')
    add('source_mass_30_bins', source*30, 'Mt', 'TableS1; main pp10/16', 'Matches reported multiwell159.81Mt.')
    add('reservoir_resource_sum', sum(D(row['capacity_mt']) for row in reservoirs), 'Mt', 'TableS2', 'Total resources do not supply annual injectivity or allocated commercial service.')
    add('source_weighted_capture_cost', unit_cost, 'USD/t', 'TableS1', 'Weighted by the reported source rates; differs from Figure11 capture averages. Weighting/version/boundary clarification needed.')
    for entry in inputs['figure11']:
        values = {key:D(str(value)) for key,value in entry.items() if key != 'scenario'}
        component_sum = values['capture']+values['hub_transport']+values['storage']
        add(entry['scenario']+'_figure11_component_sum', component_sum, 'USD/t', 'Main p16 Figure11', 'Simple sum of three displayed averages; common denominator/weighting is not established.')
        add(entry['scenario']+'_figure11_full_minus_components', values['full_chain']-component_sum, 'USD/t', 'Main p16 Figure11', 'Nonzero reconciliation difference; no silent corrected cost or inferred missing cost component.')
    point = sum(D(str(row['point_transport'])) for row in inputs['figure11'])/3
    hub = sum(D(str(row['hub_transport'])) for row in inputs['figure11'])/3
    add('scenario_mean_point_transport', point, 'USD/t', 'Main p16 Figure11', 'Unweighted mean across three reported scenarios, not a volume-weighted project cost.')
    add('scenario_mean_hub_transport', hub, 'USD/t', 'Main p16 Figure11', 'Reconstructs reported16.72/t scenario mean.')
    add('scenario_mean_transport_reduction', (point-hub)/point*100, '%', 'Main pp1/16/18', 'Reconstructs approximately34%; no independent network design or GHG reduction.')
    added = D(str(inputs['reported_retention_Mt']['MW-A']))-D(str(inputs['reported_retention_Mt']['SW-A']))
    add('reported_multiwell_increment', added, 'Mt', 'Main p16', 'Difference of author outputs, not independently simulated storage uplift.')
    limit = D(str(inputs['early_SW_A_reported_injection_limit_Mt_per_year']))
    add('early_fixed_source_necessary_shortfall', source-limit, 'Mt/year', 'Main p10; Table1 p9; TableS1', 'If source5.327 is fixed and only2.05 can be stored, strict same-year conservation without escape/inventory is infeasible. Source curtailment/backlog treatment is unprinted.')
    add('two_year_nominal_shortfall', (source-limit)*len(inputs['early_SW_A_years']), 'Mt', 'Main p10 early two years', 'Conditional bound using the printed2.05 each year; differs from reported6.60Mt aggregate gap. Do not tune a missing injection array to close it.')
    add('SW_A_total_cost_divided_by_stored_mass', D(str(inputs['reported_SW_A_total_cost_billion_USD']))*1000/D(str(inputs['reported_retention_Mt']['SW-A'])), 'USD/t', 'Main p16', 'Undiscounted total/mass ratio; cannot be equated with a levelized cost without timing/annuity/denominator definitions.')
    for scenario, key in [('SW-A','figure6_SW_A_reservoir_totals_Mt'),('MW-A','figure7b_MW_A_reservoir_totals_Mt'),('MW-D','figure9_MW_D_reservoir_totals_Mt')]:
        total = sum(D(str(value)) for value in inputs[key].values() if value is not None)
        add(scenario+'_map_reservoir_total', total, 'Mt', f'Main {key}', 'Sum of printed reservoir-endpoint masses; unlabelled masses stay null. Matches reported scenario mass but does not regenerate optimisation.')
    rate = D(str(inputs['interest_rate']))
    years = inputs['economic_life_years']
    add('analyst_capital_recovery_factor', rate*(1+rate)**years/((1+rate)**years-1), 'year^-1', 'Main p8 stated8%,30years', 'Standard annuity reconstruction from stated assumptions; no author CAPEX/utility balance supplied.')
    return rows


def main():
    inputs = load_inputs()
    rows = calculate(inputs)
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / 'B4-06_diagnostics.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    print(f'Wrote {len(rows)} Budiarto diagnostics; original optimisation remains unreproduced.')


if __name__ == '__main__':
    main()
