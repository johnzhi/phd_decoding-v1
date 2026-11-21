#!/usr/bin/env python3
"""Inventory the supplied corpus and render explicitly authored review records.

No network access. Text matches are discovery candidates, never proof of reading.
The original targeted-review catalogue and numerical model inputs are not edited.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
REVIEWS = ROOT / 'evidence/comprehensive_review'
OUT = ROOT / 'outputs/comprehensive_review'
DOC = ROOT / 'docs/comprehensive_review'
MATCH = re.compile(r'\b(?:Fig(?:ure)?s?\.?\s*\d+[a-z]?|Tables?\s*\d+[a-z]?|'
                   r'(?:Eqs?\.?|Equations?)\s*\(?\d+\)?|'
                   r'supplement(?:ary|al)?|supporting information|data availability|'
                   r'code availability)\b', re.I)
DOI = re.compile(r'\b10\.\d{4,9}/[^\s<>"\]]+', re.I)


def write_csv(path, fields, rows):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def load_reviews(catalogue):
    result = {}
    for path in sorted(REVIEWS.glob('*.json')):
        review = json.loads(path.read_text(encoding='utf-8'))
        sid = review['study_id']
        source = catalogue[sid]
        if source['duplicate_of'] or sid in result:
            raise ValueError(f'Duplicate review identity: {sid}')
        if review['source_sha256'] != source['sha256']:
            raise ValueError(f'Stale manual review: {sid}')
        expected = set(range(1, int(source['pages']) + 1))
        for key in ('text_read_pages', 'visually_inspected_pages'):
            pages = review[key]
            if len(pages) != len(set(pages)) or not set(pages) <= expected:
                raise ValueError(f'Invalid manual coverage: {sid}/{key}')
        for category in ('sections', 'visuals', 'equations', 'claims', 'references', 'issues'):
            items = review[category]
            ids = [item['id'] for item in items]
            if len(ids) != len(set(ids)):
                raise ValueError(f'Duplicate item IDs: {sid}/{category}')
            for item in items:
                if not set(item['pages']) <= expected or not item['pages']:
                    raise ValueError(f'Unlocated item: {sid}/{item["id"]}')
        # No reviewed-page count, extraction, arithmetic replay or missing asset
        # can automatically promote a paper to comprehensive completion.
        if review['overall_status'] != 'incomplete':
            raise ValueError('Completion needs a separate evidence/closure review; not enabled here')
        result[sid] = review
    return result


def render_review(source, review):
    lines = [f'# {review["study_id"]}: {source["title"]}', '',
             f'**Overall status: {review["overall_status"]}.** {review["assessment"]}', '',
             f'Source SHA-256: `{review["source_sha256"]}`. Physical PDF pages are used throughout.', '',
             f'Text read: {review["text_read_pages"]}. Rendered pages inspected: {review["visually_inspected_pages"]}.', '',
             'These declarations concern the retained PDF. They do not establish verification of cited sources or reproduction.', '']
    for key, heading in [('sections', 'Sections and scope'), ('visuals', 'Figures, tables, captions and legends'),
                         ('equations', 'Equations and derivations'), ('variables', 'Variables, units and assumptions'),
                         ('claims', 'Claims and discussion'), ('references', 'Underlying cited sources'),
                         ('issues', 'Open issues and exclusions')]:
        lines.extend([f'## {heading}', ''])
        if not review[key]:
            lines.extend([review.get(f'{key}_absence', 'None identified in this retained PDF.'), ''])
        for item in review[key]:
            if isinstance(item, str):
                lines.extend([f'- {item}', ''])
                continue
            pages = ', '.join(map(str, item.get('pages', [])))
            lines.append(f'### {item["id"]}' + (f' — p{pages}' if pages else ''))
            lines.append('')
            for name, value in item.items():
                if name in ('id', 'pages'):
                    continue
                lines.extend([f'**{name.replace("_", " ")}:** {value}', ''])
    for key, heading in [('supplements', 'Supplements and missing assets'), ('reproduction', 'Independent reproduction'),
                         ('paper1_use', 'Use in Paper 1'), ('next_steps', 'Remaining work')]:
        lines.extend([f'## {heading}', '', review[key], ''])
    (DOC / f'{review["study_id"]}.md').write_text('\n'.join(lines), encoding='utf-8')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    DOC.mkdir(parents=True, exist_ok=True)
    with (ROOT / 'data/source_catalogue.csv').open(encoding='utf-8') as stream:
        sources = list(csv.DictReader(stream))
    catalogue = {row['study_id']: row for row in sources}
    reviews = load_reviews(catalogue)
    pages, candidates, links, papers = [], [], [], []
    for source in sources:
        sid = source['study_id']
        if source['duplicate_of']:
            continue
        path = ROOT / source['pdf_path']
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != source['sha256']:
            raise ValueError(f'Source hash mismatch: {sid}')
        review = reviews.get(sid, {})
        with fitz.open(path) as document:
            if len(document) != int(source['pages']):
                raise ValueError(f'Page count mismatch: {sid}')
            attachments = document.embfile_names()
            paper = dict(study_id=sid, title=source['title'], source_sha256=digest, pages=len(document),
                         text_read_pages=len(review.get('text_read_pages', [])),
                         visually_inspected_pages=len(review.get('visually_inspected_pages', [])),
                         audit_status='incomplete' if review else 'not_started',
                         underlying_source_status='unverified', supplement_status='not_established',
                         original_model_status=review.get('original_model_status', 'not_assessed'),
                         embedded_attachment_count=len(attachments),
                         manual_record=f'evidence/comprehensive_review/{sid}.json' if review else '',
                         prior_review_status=source['reading_stage'])
            papers.append(paper)
            for number, page in enumerate(document, 1):
                text = page.get_text(sort=True)
                pages.append(dict(study_id=sid, physical_page=number, source_sha256=digest,
                                  native_text_sha256=hashlib.sha256(text.encode()).hexdigest(),
                                  native_characters=len(text), embedded_image_count=len(page.get_images()),
                                  text_read=number in review.get('text_read_pages', []),
                                  visually_inspected=number in review.get('visually_inspected_pages', []),
                                  status='manual_read_with_open_checks' if number in review.get('text_read_pages', []) else 'pending'))
                for block in page.get_text('blocks'):
                    if block[6] != 0:
                        continue
                    value = block[4]
                    if MATCH.search(value):
                        candidates.append(dict(study_id=sid, physical_page=number,
                                               bbox=json.dumps([round(v, 2) for v in block[:4]]),
                                               matches='; '.join(dict.fromkeys(MATCH.findall(value))),
                                               excerpt=' '.join(value.split())[:1800],
                                               status='unverified_discovery_candidate'))
                for match in DOI.findall(text):
                    links.append(dict(study_id=sid, physical_page=number, kind='text_doi_candidate',
                                      target=match.rstrip('.,;:)'), status='not_retrieved_or_verified'))
                for link in page.get_links():
                    if link.get('uri'):
                        links.append(dict(study_id=sid, physical_page=number, kind='pdf_uri', target=link['uri'],
                                          status='not_retrieved_or_verified'))
            for attachment in attachments:
                links.append(dict(study_id=sid, physical_page='', kind='embedded_attachment_name',
                                  target=attachment, status='not_extracted_or_reviewed'))
        if review:
            render_review(source, review)
    write_csv(OUT / 'papers.csv', list(papers[0]), papers)
    write_csv(OUT / 'pages.csv', list(pages[0]), pages)
    write_csv(OUT / 'discovery_candidates.csv', ['study_id', 'physical_page', 'bbox', 'matches', 'excerpt', 'status'], candidates)
    write_csv(OUT / 'link_candidates.csv', ['study_id', 'physical_page', 'kind', 'target', 'status'], links)
    summary = dict(unique_papers=len(papers), retained_pdf_files=len(sources), unique_physical_pages=len(pages),
                   duplicate_publications={s['study_id']: s['duplicate_of'] for s in sources if s['duplicate_of']},
                   manual_records=len(reviews), text_read_pages=sum(p['text_read'] for p in pages),
                   visually_inspected_pages=sum(p['visually_inspected'] for p in pages),
                   comprehensively_complete_papers=0, discovery_candidates=len(candidates), link_candidates=len(links),
                   external_retrieval='paused_pending_requested_Chrome_connection',
                   note='Candidate counts include mentions and duplicates; they are not verified object/citation counts. '
                        'Page reading is not independent reproduction or cited-source verification.')
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    issues = [dict(study_id=sid, **item) for sid, review in reviews.items() for item in review['issues']]
    write_csv(OUT / 'issues.csv', ['study_id', 'id', 'pages', 'status', 'finding', 'action'],
              [dict(item, pages=','.join(map(str, item['pages']))) for item in issues])
    index = ['# Comprehensive audit progress', '',
             f'{len(papers)} unique publications; {len(pages):,} physical pages. '
             f'{len(reviews)} detailed reading records; {summary["text_read_pages"]} pages read as text and '
             f'{summary["visually_inspected_pages"]} rendered pages inspected. **0 comprehensively complete papers.**', '',
             'Full completion also requires source-support checks, supplements and independent model verification. '
             'Prior targeted reviews remain separate. External retrieval is paused pending the requested Chrome connection.', '',
             '| Paper | Text pages read | Rendered pages inspected | Overall status |',
             '| --- | ---: | ---: | --- |']
    for sid, review in reviews.items():
        index.append(f'| [{sid}]({sid}.md) | {len(review["text_read_pages"])} | '
                     f'{len(review["visually_inspected_pages"])} | {review["overall_status"]} |')
    index.extend(['', 'The other publications remain pending in this comprehensive audit. '
                  'The [complete paper register](../../outputs/comprehensive_review/papers.csv), '
                  '[page register](../../outputs/comprehensive_review/pages.csv), '
                  '[issues](../../outputs/comprehensive_review/issues.csv) and '
                  '[diagnostics](../../outputs/comprehensive_review/diagnostics.csv) preserve the detailed status.', '',
                  'Generated by `python paper1/scripts/comprehensive_audit.py` from the retained PDFs and explicitly '
                  'authored review records. Discovery candidates, DOI strings and PDF hyperlinks are unverified leads. '
                  'Their counts are not counts of figures, equations, cited sources read or models reproduced.', ''])
    (DOC / 'README.md').write_text('\n'.join(index), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
