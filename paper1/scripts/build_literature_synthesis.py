#!/usr/bin/env python3
"""Package the fixed 51-review/92-publication evidence snapshot for Paper 1.

No downloads, inference of missing native inputs, original-model claims or
numerical-input writes. Human-authored use notes are separate from native
source records. Fail if the source snapshot no longer matches the checkout.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import quote, urlparse
from xml.sax.saxutils import escape

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.table import Table as ExcelTable, TableStyleInfo
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    LongTable, Paragraph, SimpleDocTemplate, Spacer, TableStyle,
)

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper1"
EVIDENCE = PAPER / "evidence/literature_synthesis"
DOCS = PAPER / "docs/literature_synthesis"
OUT = PAPER / "outputs/literature_synthesis"
SNAPSHOT = "7e3a6f756d6fe2a73d71f39e41239d180d98c21f"
DATE = "22 November 2026 (Asia/Kuala_Lumpur)"
GH = f"https://github.com/johnzhi/phd_decoding-v1/blob/{SNAPSHOT}/paper1"
CURRENT_GH = "https://github.com/johnzhi/phd_decoding-v1/blob/research/paper-1-evidence-draft/paper1"
DETAILED = "Detailed main-PDF review; comprehensive verification open"
TARGETED = "Prior targeted review; detailed main-PDF audit pending"
EXPECTED_MANUAL = {
    *(f"B1-{n:02d}" for n in range(1, 21)),
    *(f"B2-{n:02d}" for n in range(1, 19)),
    *(f"B3-{n:02d}" for n in range(1, 9)),
    "B3-11", "B3-44", "B4-05", "B4-06", "B4-08",
}
PROTECTED = [
    "data/source_catalogue.csv", "data/analysis_inputs.csv", "data/curated_values.csv",
    "outputs/calculated_results.csv", "manuscript/Paper_1_draft.template.md",
    "outputs/comprehensive_review/summary.json",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path, delimiter: str = ",") -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=delimiter))


def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields or list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def snapshot_file(path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    saved = subprocess.run(
        ["git", "show", f"{SNAPSHOT}:{rel}"], cwd=ROOT, check=True, capture_output=True,
    ).stdout
    current = path.read_bytes()
    # Git's text/eol=lf attributes normalise CSVs that the prior generators
    # wrote with CRLF. Compare source text canonically, native PDFs separately.
    if saved.replace(b"\r\n", b"\n") != current.replace(b"\r\n", b"\n"):
        raise ValueError(f"Source differs from fixed snapshot: {rel}; explicitly revise snapshot and report before refresh")


def as_text(value) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value or "")


def prose(text: str) -> str:
    """Repair joined prose labels in summaries; native evidence stays untouched."""
    labels = "detailed|targeted|this|these|the|all|ongoing|within|checkpoint|Table|Tables|Fig|Figs|Figure|Figures|Eq|Eqs|Equation|Equations|case|Case|combined|Combined|Abstract|abstract|body|tax-body|value|are|is|as|at|and|for|from|over|a|an|approximately|by|with|than|versus|of|in|difference|sum|year|rate|separate|giving|buffers|Universal|universal|remaining"
    text = re.sub(r"\b(" + labels + r")(?=\d)", r"\1 ", text)
    text = re.sub(r"\b(MPa|psi|bar)(?=\d)", r"\1 ", text)
    text = re.sub(r"\bTable(?=[A-Z]\d)", "Table ", text)
    return re.sub(r"\bPaper1\b", "Paper 1", text)


def link(path: str) -> str:
    return GH + "/" + quote(path, safe="/")


def markdown_cell(value) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(headers: list[str], rows: list[list]) -> str:
    return "\n".join([
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
        *("| " + " | ".join(markdown_cell(v) for v in row) + " |" for row in rows),
    ]) + "\n"


def load_rows() -> tuple[list[dict], dict, list[dict], dict]:
    for rel in PROTECTED:
        snapshot_file(PAPER / rel)
    catalogue = read_csv(PAPER / "data/source_catalogue.csv")
    canonical = [r for r in catalogue if not r["duplicate_of"]]
    assert len(catalogue) == 93 and len(canonical) == 92
    assert {r["study_id"]: r["duplicate_of"] for r in catalogue if r["duplicate_of"]} == {"B3-46": "B2-17"}
    manual_paths = {p.stem: p for p in (PAPER / "evidence/comprehensive_review").glob("*.json")}
    assert set(manual_paths) == EXPECTED_MANUAL, "This is the fixed 51-review deliverable; revise explicitly for a later checkpoint"
    manual = {sid: json.loads(p.read_text()) for sid, p in manual_paths.items()}
    summary = json.loads((PAPER / "outputs/comprehensive_review/summary.json").read_text())
    assert (summary["manual_records"], summary["text_read_pages"], summary["visually_inspected_pages"], summary["comprehensively_complete_papers"]) == (51, 710, 710, 0)
    notes_list = read_csv(EVIDENCE / "notes.tsv", "\t")
    assert len(notes_list) == 92 and all(None not in r and all(r.values()) for r in notes_list)
    for note in notes_list:
        note["paper1_use"] = note.pop("usable_evidence")
        note["citation_locator"] = note.pop("source_locator")
    notes = {r["study_id"]: r for r in notes_list}
    assert len(notes) == 92 and set(notes) == {r["study_id"] for r in canonical}
    metadata = json.loads((EVIDENCE / "metadata_overrides.json").read_text())
    inputs = read_csv(PAPER / "data/analysis_inputs.csv")
    counts = Counter(r["study_id"] for r in inputs)
    assert len(inputs) == 133
    held = next(r for r in read_csv(PAPER / "data/curated_values.csv") if r["value_id"] == "gwp_combined15")
    assert held["status"] == "HOLD_CONFLICTING_BEST_SOLUTION_CASE" and held["value"] == "39.2"
    assert not any(r["value_id"] == "gwp_combined15" for r in inputs)
    manifest_sources = []
    result = []
    for c in canonical:
        sid = c["study_id"]
        native = PAPER / c["pdf_path"]
        pages_path = PAPER / c["page_text_path"]
        assert sha(native) == c["sha256"], sid
        snapshot_file(pages_path)
        pages = json.loads(pages_path.read_text())
        assert len(pages) == int(c["pages"]), sid
        m = manual.get(sid)
        if m:
            snapshot_file(manual_paths[sid])
            assert m["source_sha256"] == c["sha256"] and m["overall_status"] == "incomplete", sid
            assert sorted(m["text_read_pages"]) == list(range(1, len(pages) + 1)), sid
            assert sorted(m["visually_inspected_pages"]) == list(range(1, len(pages) + 1)), sid
            evidence_rel = f"evidence/comprehensive_review/{sid}.json"
            view_rel = f"docs/comprehensive_review/{sid}.md"
        else:
            packet = PAPER / f"evidence/deep_review/{sid}_packet.txt"
            # Initial-batch targeted evidence may live in the original extraction
            # and catalogue rather than a follow-up packet. Never invent a packet.
            evidence_rel = packet.relative_to(PAPER).as_posix() if packet.exists() else c["page_text_path"]
            view_rel = evidence_rel
            snapshot_file(PAPER / evidence_rel)
        meta = metadata["papers"].get(sid, {})
        author = meta.get("author_year", c["author_year"])
        assert author, sid
        years = re.findall(r"\b(?:19|20)\d{2}\b", author)
        year = meta.get("year", years[-1] if years else "Unverified")
        assert year != "Unverified", sid
        doi_url = f"https://doi.org/{c['doi']}" if c["doi"].startswith("10.") else ""
        role = "Existing bounded benchmark + methods/context" if counts[sid] else "Methods/context; numerical transfer requires stated conditions"
        if sid in {"B1-17", "B2-01", "B3-11", "B4-08"}:
            role = "Independent component checks + methods/context"
        elif sid == "B2-11":
            role = "Declared process reference + utility-accounting methods"
        row = {
            "study_id": sid,
            "author_year": author,
            "year": year,
            "title": metadata["titles"].get(sid, c["title"]),
            "doi_or_identifier": c["doi"],
            **{k: prose(v) for k, v in notes[sid].items() if k != "study_id"},
            "main_finding": prose(metadata["findings"].get(sid, c["digest"])),
            "use_role": role,
            "review_basis": DETAILED if m else TARGETED,
            "comprehensive_status": "Incomplete; zero fully closed corpus papers",
            "main_pdf_pages": len(pages),
            "detailed_text_pages": len(m["text_read_pages"]) if m else 0,
            "detailed_visual_pages": len(m["visually_inspected_pages"]) if m else 0,
            "eligible_analysis_input_rows": counts[sid],
            "eligible_analysis_input_ids": "; ".join(r["value_id"] for r in inputs if r["study_id"] == sid),
            "original_model_status": as_text(m["original_model_status"]) if m else "Not certified reproduced; detailed audit pending; see limited benchmark checks where stated",
            "supplement_status": as_text(m.get("supplement_status", m.get("supplements", "Not reported in this record"))) if m else "Not comprehensively audited; local absence does not prove no online supplement",
            "component_reproduction": as_text(m["reproduction"]) if m else "Prior targeted checks only; do not infer comprehensive author-model reproduction",
            "detailed_review_assessment": as_text(m["assessment"]) if m else "Prior selected full-text methods/results review retained; first-page metadata checked for this table; every-item review pending",
            "existing_paper1_use_record": as_text(m["paper1_use"]) if m else c["transferability_limits"],
            "original_catalogue_reading_stage": c["reading_stage"],
            "original_targeted_locators": c["checked_sections"],
            "bibliographic_note": meta.get("note", "Short citation retained from source catalogue; native PDF remains the authority."),
            "bibliographic_basis": "Native PDF p1 / detailed identity section; separate display correction" if meta else "Existing source catalogue and retained native PDF",
            "pdf_sha256": c["sha256"],
            "page_text_sha256": sha(pages_path),
            "evidence_record_sha256": sha(PAPER / evidence_rel),
            "source_pdf": link(c["pdf_path"]),
            "doi_url": doi_url,
            "review_evidence": link(view_rel),
            "review_record": link(evidence_rel),
            "page_text": link(c["page_text_path"]),
            "original_filename": c["original_filename"],
            "upload_file_id": c["upload_file_id"],
            "duplicate_alias": "B3-46 (preserved, excluded from 92)" if sid == "B2-17" else "",
            "source_commit": SNAPSHOT,
        }
        result.append(row)
        manifest_sources.append({
            "study_id": sid, "native_path": c["pdf_path"], "native_sha256": c["sha256"],
            "page_text_path": c["page_text_path"], "page_text_sha256": sha(pages_path),
            "review_path": evidence_rel, "review_sha256": sha(PAPER / evidence_rel),
        })
    eligible = [r for r in inputs if r["study_id"] in manual]
    assert len(eligible) == 54 and Counter(r["study_id"] for r in eligible) == {"B1-11": 8, "B1-19": 36, "B2-08": 3, "B2-12": 5, "B4-06": 2}
    assert sum(r["main_pdf_pages"] for r in result) == 1301
    manifest = {
        "date": DATE, "repository": "johnzhi/phd_decoding-v1", "branch": "research/paper-1-evidence-draft",
        "source_commit": SNAPSHOT, "unique_publications": 92, "retained_native_pdfs": 93,
        "detailed_main_pdf_reviews": 51, "prior_targeted_only": 41, "main_pages_in_corpus": 1301,
        "detailed_text_pages": 710, "detailed_visual_pages": 710, "comprehensively_complete": 0,
        "eligible_main_analysis_rows": 133, "eligible_rows_from_51": 54,
        "scoped_original_passage_edges": summary["primary_text_checked_citation_edges"],
        "bibliography_dependency_records": summary["manual_reference_records"],
        "duplicate_aliases": {"B3-46": "B2-17"},
        "external_retrieval": summary["external_retrieval"],
        "column_provenance": {
            "identity_native_files_hashes": "source_catalogue.csv; 49 blank short citations resolved from retained p1/identity sections in metadata_overrides.json; no remote bibliographic check",
            "method_scope_pressure_use_sections_locators_limits": "Human-authored notes.tsv, synthesised from retained targeted/detailed reviews and source passages; proposed Paper1 uses are analyst recommendations",
            "main_finding": "Existing source catalogue digest, with explicitly authored overrides for later detailed qualifications in metadata_overrides.json; joined prose labels are spaced for display, with native evidence unchanged",
            "audit_model_supplement_component_status": "Native detailed JSON record where available; otherwise explicitly targeted/pending",
            "eligible_input_counts_ids": "Unmodified analysis_inputs.csv; not an inventory of all other reference-input registers or a blanket safety approval",
        },
        "protected_source_files": {p: hashlib.sha256((PAPER / p).read_bytes().replace(b"\r\n", b"\n")).hexdigest() for p in PROTECTED},
        "snapshot_text_comparison": "Protected text SHA-256 values use canonical LF, consistent with repository text/eol=lf; native PDF hash checks are byte-exact",
        "sources": manifest_sources,
        "curation_files": {p.relative_to(PAPER).as_posix(): sha(p) for p in [EVIDENCE / "notes.tsv", EVIDENCE / "metadata_overrides.json", DOCS / "usable_51_overview.md", DOCS / "proposed_introduction.template.md", DOCS / "README.md"]},
    }
    return result, manifest, eligible, held


def build_markdown(rows: list[dict]) -> None:
    header = (
        "# Literature table — all 92 unique supplied publications\n\n"
        f"Prepared {DATE}. Source checkpoint `{SNAPSHOT}`. "
        "**51 detailed main-PDF reviews; 41 prior targeted reviews; zero comprehensively complete papers.** "
        "The duplicate B3-46 is represented once as B2-17. This is a supplied-corpus synthesis, not a new systematic search.\n\n"
        "Each of the 92 rows below states the study method, scope, usable finding, proposed Paper1 role, locator and principal limit. "
        "Detailed/Targeted marks the review basis, not a quality rank. The editable workbook and CSV also contain full provenance, "
        "pressure/time representations, original model/supplement status, input IDs and SHA-256 hashes. "
        "An eligible row means its existing source-context status in the main benchmark register; it does not establish regional physical safety or complete LCA.\n\n"
        "[Excel workbook](../../outputs/literature_synthesis/literature_table_92.xlsx) · "
        "[Full CSV](../../outputs/literature_synthesis/literature_table_92.csv) · "
        "[Readable PDF](literature_table_92.pdf) · [What the 51 can support](usable_51_report.md)\n\n"
        "## Theme index\n\n"
    )
    themes = sorted({r["theme"] for r in rows})
    header += markdown_table(["Theme", "All papers", "Detailed", "Targeted"], [
        [t, sum(r["theme"] == t for r in rows), sum(r["theme"] == t and r["review_basis"] == DETAILED for r in rows), sum(r["theme"] == t and r["review_basis"] == TARGETED for r in rows)] for t in themes
    ])
    body = [header]
    for batch in ["B1", "B2", "B3", "B4"]:
        body.append(f"\n## {batch} — retained source IDs\n")
        cells = []
        for r in rows:
            if not r["study_id"].startswith(batch):
                continue
            ref = f"**{r['study_id']}** — {r['author_year']}<br>[{r['title']}]({r['source_pdf']})"
            if r["doi_url"]:
                ref += f"<br>[DOI]({r['doi_url']})"
            cells.append([
                ref, f"{r['geography']}<br>{r['method']}<br>{r['boundary_and_time']}",
                r["main_finding"], f"{r['paper1_use']}<br>**Placement:** {r['paper1_placement']}",
                f"{r['citation_locator']}<br>[Review/evidence]({r['review_evidence']})",
                f"{r['principal_limit']}<br>**Transfer:** {r['numerical_use_rule']}",
                f"{'Detailed' if r['review_basis'] == DETAILED else 'Targeted'}<br>{r['eligible_analysis_input_rows']} existing main-input rows",
            ])
        body.append(markdown_table(["Paper / source", "Geography, method and scope", "Main finding", "Use in Paper1", "Locator / evidence", "Limits / numerical use", "Review basis"], cells))
    body.append(
        "\n## Interpretation and provenance\n\n"
        "Metadata display corrections are separate from the source catalogue. Examples include B2-06 (2026 volume, 2025 online), "
        "B2-16 (2021 publication despite a2020 DOI), B2-17 (2026 volume, 2025 online), B3-13 (2012), "
        "B3-18 (2008 issue, 2007 online), B3-25 (2024 issue, 2023 online) and B3-27 (2026 issue, 2025 online). "
        "B3-15 uses the retained2014 acceptance/copyright date with issue date unverified. B2-10 retains the GHGT-17 date and SSRN identifier rather than inventing a DOI. "
        "All original short citations, filenames, upload IDs and native hashes remain recoverable in the source catalogue/manifest.\n\n"
        "The source URLs are pinned to the evidence checkpoint, avoiding silent changes when the research branch advances. "
        "The 41 targeted-only rows preserve the prior selected-passage basis; inspecting identity metadata for this table does not promote them to detailed review. "
        "Proposed uses and placement are analyst recommendations. Underlying cited-source verification and full author-model reproduction remain open. "
        "Separate Bjarmeland, CEMCAP, primary Tomakomai and EXCOOL reference assets are outside this92-publication count. "
        "See the [provenance manifest](../../outputs/literature_synthesis/manifest.json) and [build/field guide](README.md).\n"
    )
    (DOCS / "literature_table_92.md").write_text("\n".join(body), encoding="utf-8")
    detailed = [r for r in rows if r["review_basis"] == DETAILED]
    report = (DOCS / "usable_51_overview.md").read_text() + "\n## 6. Paper-by-paper use matrix — all 51 detailed records\n\n"
    report += "Every row below has a complete main-PDF page-reading record; comprehensive verification remains incomplete. Use statements are recommendations with their stated transfer limits.\n\n"
    report += markdown_table(
        ["Paper / evidence", "Reusable contribution", "Where to use", "Exact source locator", "Numerical boundary / limit"],
        [[f"**{r['study_id']} — {r['author_year']}**<br>[Native PDF]({r['source_pdf']}) · [Detailed record]({r['review_evidence']})", r["paper1_use"], r["paper1_placement"], r["citation_locator"], f"{r['numerical_use_rule']} {r['principal_limit']}"] for r in detailed],
    )
    report += "\n## 7. Source references for the 51\n\n"
    for r in detailed:
        ident = f"[DOI {r['doi_or_identifier']}]({r['doi_url']})" if r["doi_url"] else r["doi_or_identifier"]
        report += f"- **{r['study_id']}** — {r['author_year']}. *{r['title']}*. {ident}. [Retained source]({r['source_pdf']}).\n"
    (DOCS / "usable_51_report.md").write_text(report, encoding="utf-8")
    intro = (DOCS / "proposed_introduction.template.md").read_text()
    cited = set(re.findall(r"\bB[1-4]-\d{2}\b", intro))
    intro += "\n## References cited in the draft and revision notes\n\n"
    for r in rows:
        if r["study_id"] in cited:
            ident = f"[DOI {r['doi_or_identifier']}]({r['doi_url']})" if r["doi_url"] else r["doi_or_identifier"]
            basis = "Detailed main-PDF review" if r["review_basis"] == DETAILED else "Prior targeted review"
            intro += f"- **{r['study_id']}** — {r['author_year']}. *{r['title']}*. {ident}. {basis}; [source]({r['source_pdf']}).\n"
    (DOCS / "proposed_introduction.md").write_text(intro, encoding="utf-8")


def build_workbook(rows: list[dict], eligible: list[dict], held: dict) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Read me"
    readme = [
        ["Paper 1 literature deliverables", "51 detailed reviews + full 92-publication table"],
        ["Prepared", DATE], ["Evidence commit", SNAPSHOT],
        ["Unique publications / native PDFs", "92 / 93; B3-46 duplicate of B2-17 is excluded from unique rows"],
        ["Review coverage", "51 detailed main-PDF records,710/1301 pages;41 prior targeted reviews"],
        ["Comprehensive closure", "0; cited originals, supplements and original models remain open"],
        ["Literature92", "One row per canonical paper: method, geography, scope, findings, use, locators and limits"],
        ["Usable51", "Paper-by-paper contributions and placement from detailed records only"],
        ["Audit92", "Coverage, native-model/supplement status and precise scope of independent checks"],
        ["Provenance92", "Pinned source/review links, native hashes, original filenames/upload IDs and bibliographic notes"],
        ["Eligible54", "Unmodified extract of54 main-analysis rows from five detailed-review papers; source-context eligibility only"],
        ["Held39.2", "The disputed B2-12 combined1.5MPa result remains HOLD and is absent from eligible inputs"],
        ["Other existing eligible rows", "79: four B3-38 conditioning and75 B4-09 fleet outputs; those papers remain targeted-only"],
        ["Counts are not independent evidence", "Input rows, bibliography records and citation checks have different meanings"],
        ["Use/placement fields", "Analyst recommendations, not statements that authors supplied our inputs or validated our region"],
        ["Numerical exclusion", "Follow the scenario-specific transfer rule; a useful method does not approve every number in a paper"],
        ["Geographic proxies", "Disclose original region, process, pressure/state, horizon, denominator and suppliers"],
        ["First-page metadata", "49 blank author/year entries resolved locally in a separate display file; catalogue unchanged"],
        ["External retrieval", "Still paused pending requested Chrome connection; no new Firecrawl/public downloads for these outputs"],
        ["Outside this92-paper corpus", "Bjarmeland/CEMCAP and later Tomakomai/EXCOOL references have separate provenance"],
        ["Refresh", "python paper1/scripts/build_literature_synthesis.py; fixed snapshot checks must pass"],
        ["Read full synthesis", CURRENT_GH + "/docs/literature_synthesis/usable_51_report.md"],
        ["Proposed introduction", CURRENT_GH + "/docs/literature_synthesis/proposed_introduction.md"],
    ]
    for row in readme:
        ws.append(row)
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 115
    ws.freeze_panes = "B2"
    for row in ws:
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row[0].row].height = 37
    for c in ws[1]:
        c.fill = PatternFill("solid", fgColor="123548")
        c.font = Font(color="FFFFFF", bold=True)
    core = [
        "study_id", "author_year", "title", "theme", "geography", "method", "boundary_and_time",
        "pressure_service", "main_finding", "paper1_use", "paper1_placement", "citation_locator",
        "numerical_use_rule", "principal_limit", "review_basis", "eligible_analysis_input_rows",
        "doi_or_identifier", "source_pdf", "review_evidence",
    ]
    uses = ["study_id", "author_year", "use_role", "paper1_use", "paper1_placement", "citation_locator", "numerical_use_rule", "principal_limit", "eligible_analysis_input_rows", "review_evidence"]
    audit = ["study_id", "review_basis", "comprehensive_status", "main_pdf_pages", "detailed_text_pages", "detailed_visual_pages", "original_model_status", "supplement_status", "component_reproduction", "detailed_review_assessment", "existing_paper1_use_record", "original_catalogue_reading_stage", "original_targeted_locators", "review_record"]
    provenance = ["study_id", "author_year", "year", "bibliographic_basis", "bibliographic_note", "doi_or_identifier", "doi_url", "source_pdf", "review_evidence", "review_record", "page_text", "pdf_sha256", "page_text_sha256", "evidence_record_sha256", "original_filename", "upload_file_id", "duplicate_alias", "source_commit"]
    def add_sheet(name, records, fields):
        sheet = wb.create_sheet(name)
        sheet.append(fields)
        for r in records:
            sheet.append([r.get(f, "") for f in fields])
        for col in sheet.columns:
            key = col[0].value
            sheet.column_dimensions[col[0].column_letter].width = 13 if key == "study_id" else 20 if key.endswith("pages") or key == "eligible_analysis_input_rows" else 40 if "sha256" in key or key.endswith("url") else 55
            for c in col:
                c.alignment = Alignment(wrap_text=True, vertical="top")
                c.font = Font(name="Calibri", size=11)
                if isinstance(c.value, str) and c.value.startswith("https://"):
                    c.hyperlink = c.value
                    c.font = Font(name="Calibri", size=11, color="0563C1", underline="single")
        for c in sheet[1]:
            c.fill = PatternFill("solid", fgColor="123548")
            c.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        sheet.row_dimensions[1].height = 34
        for i in range(2, sheet.max_row + 1):
            sheet.row_dimensions[i].height = 145 if name in {"Literature92", "Audit92", "Usable51"} else 80
        sheet.freeze_panes = "C2" if len(fields) > 4 else "B2"
        sheet.sheet_view.zoomScale = 75
        table = ExcelTable(displayName="T" + re.sub(r"[^A-Za-z0-9]", "", name), ref=sheet.dimensions)
        table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
        sheet.add_table(table)
        sheet.print_options.horizontalCentered = True
        return sheet
    add_sheet("Literature92", rows, core)
    add_sheet("Usable51", [r for r in rows if r["review_basis"] == DETAILED], uses)
    add_sheet("Audit92", rows, audit)
    add_sheet("Provenance92", rows, provenance)
    add_sheet("Eligible54", eligible, list(eligible[0]))
    add_sheet("Held39.2", [held], list(held))
    theme_rows = [{"theme": t, "all_papers": sum(r["theme"] == t for r in rows), "detailed": sum(r["theme"] == t and r["review_basis"] == DETAILED for r in rows), "targeted": sum(r["theme"] == t and r["review_basis"] == TARGETED for r in rows)} for t in sorted({r["theme"] for r in rows})]
    add_sheet("Themes", theme_rows, list(theme_rows[0]))
    wb.save(OUT / "literature_table_92.xlsx")


def register_fonts() -> None:
    font_root = Path("/usr/share/fonts/truetype/dejavu")
    for name, filename in [("DejaVu", "DejaVuSans.ttf"), ("DejaVu-Bold", "DejaVuSans-Bold.ttf"), ("DejaVu-Oblique", "DejaVuSans-Oblique.ttf"), ("DejaVu-BoldOblique", "DejaVuSans-BoldOblique.ttf")]:
        pdfmetrics.registerFont(TTFont(name, str(font_root / filename)))
    pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold", italic="DejaVu-Oblique", boldItalic="DejaVu-BoldOblique")


def pdf_styles():
    styles = getSampleStyleSheet()
    for name in styles.byName:
        styles[name].fontName = "DejaVu"
    styles["BodyText"].fontSize = 9.2
    styles["BodyText"].leading = 13
    styles["BodyText"].spaceAfter = 7
    styles["Heading1"].fontSize = 18
    styles["Heading1"].leading = 23
    styles["Heading2"].fontSize = 13
    styles["Heading2"].leading = 18
    styles["Heading3"].fontSize = 10.5
    styles["Heading3"].leading = 14
    for name in ["Heading1", "Heading2", "Heading3"]:
        styles[name].fontName = "DejaVu-Bold"
        styles[name].textColor = colors.HexColor("#123548")
        styles[name].spaceBefore = 13
        styles[name].spaceAfter = 8
    styles.add(ParagraphStyle("Cell", fontName="DejaVu", fontSize=8, leading=10.6, alignment=TA_LEFT, wordWrap="CJK"))
    styles.add(ParagraphStyle("Small", fontName="DejaVu", fontSize=8, leading=11, spaceAfter=6))
    return styles


def inline(text: str, base: Path) -> str:
    text = escape(text)
    def mdlink(m):
        label, url = m.groups()
        if not urlparse(url).scheme:
            # Snapshot evidence links are already absolute; new deliverable links
            # resolve on the work branch so PDFs remain usable off the filesystem.
            rel = (base / url.split("#", 1)[0]).resolve().relative_to(PAPER)
            url = CURRENT_GH + "/" + quote(rel.as_posix(), safe="/")
        return f'<link href="{url}" color="#0563C1">{label}</link>'
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", mdlink, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text.replace("&lt;br&gt;", "<br/>")


def footer(canvas, doc):
    canvas.saveState()
    w, _ = doc.pagesize
    canvas.setFont("DejaVu", 7)
    canvas.setFillColor(colors.HexColor("#526773"))
    canvas.drawString(doc.leftMargin, 22, "Paper 1 | evidence checkpoint 7e3a6f7 | 22 November 2026")
    canvas.drawRightString(w - doc.rightMargin, 22, str(doc.page))
    canvas.restoreState()


def markdown_pdf(source: Path, target: Path, styles) -> None:
    """Readable portrait report; wide Markdown matrices become labelled cards."""
    lines = source.read_text().splitlines()
    story = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            cells = [[c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", l)[1:-1]] for l in table_lines]
            headers = cells[0]
            for row in cells[2:]:
                assert len(row) == len(headers), (source, row)
                story.append(Paragraph(inline(row[0], source.parent), styles["Heading3"]))
                for key, value in zip(headers[1:], row[1:]):
                    story.append(Paragraph(f"<b>{escape(key)}:</b> " + inline(value, source.parent), styles["BodyText"]))
                story.append(Spacer(1, 7))
            continue
        if line.startswith("#"):
            level = min(len(line) - len(line.lstrip("#")), 3)
            story.append(Paragraph(inline(line.lstrip("# "), source.parent), styles[f"Heading{level}"]))
            i += 1
            continue
        paragraph = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].lstrip().startswith(("#", "|", "- ")):
            paragraph.append(lines[i].strip())
            i += 1
        value = " ".join(paragraph)
        if value.startswith("- "):
            value = "• " + value[2:]
        story.append(Paragraph(inline(value, source.parent), styles["BodyText"]))
    doc = SimpleDocTemplate(str(target), pagesize=A4, rightMargin=43, leftMargin=43, topMargin=38, bottomMargin=40, title=source.stem.replace("_", " "), author="Paper 1 research package")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def literature_pdf(rows: list[dict], styles) -> None:
    story = [Paragraph("Literature table: all 92 supplied publications", styles["Heading1"])]
    story.append(Paragraph("51 detailed main-PDF records; 41 prior targeted reviews; zero comprehensively complete papers. Duplicate B3-46 is counted once as B2-17. Physical PDF locators and links refer to checkpoint7e3a6f7. This supplied-corpus table is not a new systematic search.", styles["BodyText"]))
    story.append(Paragraph("This readable table contains each paper's citation, method/scope, finding, use and transfer limits. The accompanying Excel/CSV contains additional pressure/time, original-model/supplement, input-ID and SHA-256 provenance fields. Proposed uses are analyst recommendations; a method/context citation does not approve numerical transfer.", styles["BodyText"]))
    story.append(Paragraph(inline("[Full Excel workbook](../../outputs/literature_synthesis/literature_table_92.xlsx) · [51-paper synthesis](usable_51_report.md) · [Field/provenance guide](README.md)", DOCS), styles["BodyText"]))
    width = landscape(A4)[0] - 60
    col_widths = [width * v for v in [.19, .18, .21, .20, .22]]
    for batch in ["B1", "B2", "B3", "B4"]:
        story.append(Paragraph(f"{batch} — retained source IDs", styles["Heading2"]))
        data = [[Paragraph(f"<b>{h}</b>", styles["Cell"]) for h in ["Paper / review basis", "Method, geography, scope", "Main finding", "Use in Paper 1 / locator", "Limits / numerical boundary"]]]
        for r in rows:
            if not r["study_id"].startswith(batch):
                continue
            ref = f"<b>{r['study_id']} — {escape(r['author_year'])}</b><br/>{escape(r['title'])}<br/><b>{'Detailed' if r['review_basis'] == DETAILED else 'Targeted'}</b> · {r['eligible_analysis_input_rows']} existing main-input rows<br/>"
            ref += f'<link href="{r["source_pdf"]}" color="#0563C1">Native PDF</link> · <link href="{r["review_evidence"]}" color="#0563C1">Evidence</link>'
            if r["doi_url"]:
                ref += f'<br/><link href="{r["doi_url"]}" color="#0563C1">{escape(r["doi_or_identifier"])}</link>'
            else:
                ref += "<br/>" + escape(r["doi_or_identifier"])
            data.append([
                Paragraph(ref, styles["Cell"]),
                Paragraph(escape(f"{r['geography']} — {r['method']}") + "<br/><br/>" + escape(r["boundary_and_time"]) + "<br/><br/>" + escape(r["pressure_service"]), styles["Cell"]),
                Paragraph(escape(r["main_finding"]), styles["Cell"]),
                Paragraph(escape(r["paper1_use"]) + "<br/><br/><b>Placement:</b> " + escape(r["paper1_placement"]) + "<br/><br/><b>Locator:</b> " + escape(r["citation_locator"]), styles["Cell"]),
                Paragraph(escape(r["principal_limit"]) + "<br/><br/><b>Transfer:</b> " + escape(r["numerical_use_rule"]), styles["Cell"]),
            ])
        table = LongTable(data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DBE8EF")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOX", (0, 0), (-1, -1), .35, colors.HexColor("#A5BBC6")),
            ("INNERGRID", (0, 0), (-1, -1), .25, colors.HexColor("#CCD9DE")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F8FA")]),
            ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))
        story.extend([table, Spacer(1, 14)])
    doc = SimpleDocTemplate(str(DOCS / "literature_table_92.pdf"), pagesize=landscape(A4), leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=38, title="Literature table — 92 supplied publications", author="Paper 1 research package")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    rows, manifest, eligible, held = load_rows()
    write_csv(OUT / "literature_table_92.csv", rows)
    write_csv(OUT / "usable_51.csv", [r for r in rows if r["review_basis"] == DETAILED])
    write_csv(OUT / "eligible_inputs_from_51.csv", eligible)
    build_markdown(rows)
    build_workbook(rows, eligible, held)
    register_fonts()
    styles = pdf_styles()
    literature_pdf(rows, styles)
    for name in ["usable_51_report", "proposed_introduction"]:
        markdown_pdf(DOCS / f"{name}.md", DOCS / f"{name}.pdf", styles)
    subprocess.run(["pandoc", str(DOCS / "proposed_introduction.md"), "-o", str(DOCS / "proposed_introduction.docx"), "--metadata", "lang=en-GB"], cwd=ROOT, check=True)
    # A package manifest hashes generated outputs without self-reference.
    generated = [*OUT.glob("*.csv"), OUT / "literature_table_92.xlsx", *(DOCS / f"{n}.{s}" for n in ["usable_51_report", "literature_table_92", "proposed_introduction"] for s in ["md", "pdf"]), DOCS / "proposed_introduction.docx"]
    manifest["generated_files"] = {p.relative_to(PAPER).as_posix(): {"sha256": sha(p), "bytes": p.stat().st_size} for p in generated}
    manifest["generator_sha256"] = sha(Path(__file__))
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"papers": len(rows), "detailed": 51, "targeted": 41, "eligible_rows_from_51": len(eligible), "comprehensively_complete": 0, "generated_files": len(generated)}, indent=2))


if __name__ == "__main__":
    main()
