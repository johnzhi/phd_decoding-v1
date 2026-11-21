#!/usr/bin/env python3
"""Small independent diagnostics from explicitly located, manually read inputs.

These are not simulations or reproductions of the authors' optimisers. Outputs
live outside Paper 1's admitted model inputs and never repair disputed units.
"""
from pathlib import Path
import csv
import hashlib
import json
import re

import fitz

ROOT = Path(__file__).resolve().parents[1]


def atom_counts(formula):
    tokens = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
    if ''.join(element + number for element, number in tokens) != formula:
        raise ValueError(f'Unsupported formula: {formula}')
    result = {}
    for element, number in tokens:
        result[element] = result.get(element, 0) + int(number or 1)
    return result


def reaction_residual(reactants, products):
    result = {}
    for side, sign in ((reactants, -1), (products, 1)):
        for coefficient, formula in side:
            for element, count in atom_counts(formula).items():
                result[element] = result.get(element, 0) + sign * coefficient * count
    return result


def diagnostics():
    rows = []

    def add(sid, pages, item, expression, value, unit, meaning):
        rows.append(dict(study_id=sid, physical_pages=pages, item=item,
                         expression=expression, value=value, unit=unit,
                         interpretation=meaning, scope='diagnostic_only_not_original_model_reproduction'))

    reactions = [([(1, 'CO2'), (4, 'H2')], [(1, 'CH4'), (2, 'H2O')]),
                 ([(1, 'FeO'), (1, 'CO')], [(1, 'Fe'), (1, 'CO2')]),
                 ([(1, 'FeO'), (1, 'H2')], [(1, 'Fe'), (1, 'H2O')]),
                 ([(1, 'FeO'), (1, 'C')], [(1, 'Fe'), (1, 'CO')])]
    for index, (reactants, products) in enumerate(reactions, 1):
        residual = reaction_residual(reactants, products)
        add('B1-02', '2' if index == 1 else '4', f'E{index:02}',
            'product atoms minus reactant atoms', json.dumps(residual, sort_keys=True),
            'atoms per stoichiometric reaction', 'Zero residual verifies atom balance only, not reaction enthalpy/equilibrium.')
    methane = 100 * (425 - 293) / 425
    hydrogen = 100 * (425 - 324) / 425
    add('B1-02', '5,6', 'C08_methane', '100*(425-293)/425', methane, '%', 'Rounds to reported31%; same counted-carbon boundary only.')
    add('B1-02', '5,6', 'C08_hydrogen', '100*(425-324)/425', hydrogen, '%', 'Rounds to reported24%; not a lifecycle calculation.')
    add('B1-02', '5,6', 'C08_difference', '100*(324-293)/425', methane-hydrogen, 'percentage points', 'Unrounded advantage exceeds7percentage points.')
    for label, shares in [('conventional', [61, 9, 30]), ('hydrogen', [51, 48, 1]), ('recycling', [61, 35, 4])]:
        add('B1-02', '6', f'T01_reduction_shares_{label}', '+'.join(map(str, shares)), sum(shares), '%', 'Reported reduction-mode fractions sum to100; not a mass/energy balance.')
    add('B1-02', '6', 'F06_topgas_branch_residual', '1030-(500+270+160)', 1030-(500+270+160), 'Nm3/t-HM', 'Unexplained displayed branch difference; do not force a correction.')
    add('B1-02', '6', 'F06_export_branch_residual', '666-(500-204+270)', 666-(500-204+270), 'Nm3/t-HM', 'Same100 difference; detailed routing/bases needed.')
    add('B1-02', '6', 'F06_H2_stoichiometry_residual', '814-4*204', 814-4*204, 'Nm3/t-HM', 'Rounded printed H2 differs from ideal1:4 stoichiometry; reference states assumed equal solely for this diagnostic.')
    add('B1-02', '6', 'F06_water_stoichiometry_residual', '407-2*204', 407-2*204, 'Nm3/t-HM', 'Rounded printed water differs by1; no water energy/mass balance inferred.')
    add('B1-05', '3', 'I03_calendar', '150*365*24*3600/1e9', 150*365*24*3600/1e9, 'Mt/365-day year', 'Explicit continuous calendar diagnostic; source4Mt/y basis remains unknown.')
    base, forced = 20336817, 19009970
    add('B4-05', '5', 'C05_forced_hub_loss', '20336817-19009970', base-forced, 'USD', 'Difference of reported objectives; not an independent optimisation.')
    add('B4-05', '5', 'C05_forced_hub_loss_fraction', '100*(20336817-19009970)/20336817', 100*(base-forced)/base, '% of reported base', 'Not the abstract3% outage claim.')
    delivered, concentration, maximum, limit = 1000, 4600, 6727, 1250
    add('B4-05', '4,5', 'I02_load_rhs', '6727*1250', maximum*limit, 'g/year', 'Eq12 RHS forsi1 contaminant3.')
    add('B4-05', '4,5', 'I02_load_lhs', '1000*4600', delivered*concentration, 'g/year', 'Single-constraint counterexample, not a feasible whole-network solution: passes load bound despite4600>1250g/t.')
    add('B4-05', '5', 'strict_mixture_minimum', 'min(4600,5000,2600)', min(4600,5000,2600), 'g/t', 'Without removal or initially cleaner hub stock, nonnegative mixing cannot meet strict1250/2500g/t limits atsi1/si3.')
    add('B4-05', '5', 'strict_quality_remaining_sink_capacity', '8460+9483', 8460+9483, 't/year', 'Onlysi2/si4 pass this necessary contaminant3 bound; other impurities may further restrict flows.')
    add('B4-05', '5', 'strict_quality_minimum_supply_gap', '(6000+12000+8000)-(8460+9483)', (6000+12000+8000)-(8460+9483), 't/year', 'Necessary lower-bound excess under strict quality interpretation; temporary accumulation is not permanent sequestration.')
    return rows


def validate_sources():
    with (ROOT / 'data/source_catalogue.csv').open() as stream:
        catalogue = {row['study_id']: row for row in csv.DictReader(stream)}
    for sid in ('B1-02', 'B1-05', 'B4-05'):
        review = json.loads((ROOT / f'evidence/comprehensive_review/{sid}.json').read_text())
        path = ROOT / catalogue[sid]['pdf_path']
        if hashlib.sha256(path.read_bytes()).hexdigest() != review['source_sha256']:
            raise ValueError(f'Stale diagnostic inputs: {sid}')
    # Native tokens corroborate manual row/column mapping, not replace it.
    # Figure6's814 is raster content and is supported by the manual visual record.
    for sid, page, tokens in [('B1-02', 6, ['425', '324', '293']),
                              ('B1-05', 3, ['150', '1.6']),
                              ('B4-05', 5, ['20,336,817', '19,009,970', '6,727', '4,600', '1,250'])]:
        with fitz.open(ROOT / catalogue[sid]['pdf_path']) as document:
            text = document[page-1].get_text()
        for token in tokens:
            if token not in text:
                raise ValueError(f'Missing source token: {sid}/p{page}/{token}')


def main():
    validate_sources()
    rows = diagnostics()
    out = ROOT / 'outputs/comprehensive_review'
    out.mkdir(parents=True, exist_ok=True)
    with (out / 'diagnostics.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f'Wrote {len(rows)} diagnostics; no author model or Paper1 result replaced.')


if __name__ == '__main__':
    main()
