#!/usr/bin/env python3
"""Check a reported-case lower bound; not a native MoMILP/LCI reproduction."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    data = json.loads((ROOT / 'evidence/comprehensive_review_inputs/B2-12_case_conflict.json').read_text())
    assert hashlib.sha256((ROOT / data['source_path']).read_bytes()).hexdigest() == data['source_sha256']
    labels = data['figure20']['disjoint_labelled_components_ktCO2e']
    subtotal = sum(labels.values())
    total = data['source_quote']['total_ktCO2e']
    lower = subtotal - .5 * len(labels)
    upper_total = total + .05
    rows = [dict(item='three_label_subtotal', value=subtotal, unit='ktCO2e', basis='Three disjoint Figure20 component labels; not a complete reconstructed total'),
            dict(item='subtotal_minus_reported_total', value=subtotal-total, unit='ktCO2e', basis='Literal printed numbers; no replacement total inferred'),
            dict(item='conditional_rounding_lower_bound_excess', value=lower-upper_total, unit='ktCO2e', basis=data['rounding_assumption'])]
    assert lower > upper_total
    out = ROOT / 'outputs/comprehensive_review/B2-12_case_conflict_checks.csv'
    with out.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0], lineterminator='\n')
        writer.writeheader();writer.writerows(rows)
    print(json.dumps(dict(study_id='B2-12',labelled_subtotal_kt=subtotal,reported_total_kt=total,
                          lower_bound_conflict=True,quoted_intensity_preserved=39.2,
                          case_status=data['status'],author_model='not_reproduced')))

if __name__ == '__main__':
    main()
