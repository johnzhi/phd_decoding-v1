#!/usr/bin/env python3
"""Check delivered literature coverage, preservation, links and artifact integrity."""

import csv
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlparse

import fitz
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper1"
DOCS = PAPER / "docs/literature_synthesis"
OUT = PAPER / "outputs/literature_synthesis"


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads((OUT / "manifest.json").read_text())
    snapshot = manifest["source_commit"]
    rows = read_csv(OUT / "literature_table_92.csv")
    manual = read_csv(OUT / "usable_51.csv")
    eligible = read_csv(OUT / "eligible_inputs_from_51.csv")
    inputs = read_csv(PAPER / "data/analysis_inputs.csv")
    catalogue = read_csv(PAPER / "data/source_catalogue.csv")
    by_id = {r["study_id"]: r for r in rows}
    canonical = {r["study_id"]: r for r in catalogue if not r["duplicate_of"]}
    detailed_ids = {r["study_id"] for r in manual}
    assert len(rows) == len(by_id) == 92 and set(by_id) == set(canonical)
    assert len(manual) == len(detailed_ids) == 51
    assert len(eligible) == 54 and eligible == [r for r in inputs if r["study_id"] in detailed_ids]
    assert len(inputs) == 133 and "B3-46" not in by_id
    assert sum(int(r["detailed_text_pages"]) for r in rows) == 710
    assert sum(int(r["detailed_visual_pages"]) for r in rows) == 710
    assert sum(int(r["main_pdf_pages"]) for r in rows) == 1301
    required = ["author_year", "title", "method", "boundary_and_time", "pressure_service", "main_finding", "paper1_use", "paper1_placement", "citation_locator", "numerical_use_rule", "principal_limit"]
    for r in rows:
        assert all(r[k].strip() for k in required), r["study_id"]
        assert r["source_commit"] == snapshot
        assert r["pdf_sha256"] == canonical[r["study_id"]]["sha256"]
        assert r["author_year"] != "See original paper"
        if r["study_id"] not in detailed_ids:
            assert r["review_basis"].startswith("Prior targeted")
            assert r["detailed_text_pages"] == r["detailed_visual_pages"] == "0"
        assert r["comprehensive_status"].startswith("Incomplete")
    held = next(r for r in read_csv(PAPER / "data/curated_values.csv") if r["value_id"] == "gwp_combined15")
    assert held["value"] == "39.2" and held["status"] == "HOLD_CONFLICTING_BEST_SOLUTION_CASE"
    assert not any(r["value_id"] == held["value_id"] for r in eligible + inputs)
    for rel, digest in manifest["protected_source_files"].items():
        current = (PAPER / rel).read_bytes()
        # A fresh checkout can have canonical LF rather than prior-generator CRLF.
        saved = subprocess.run(["git", "show", f"{snapshot}:paper1/{rel}"], cwd=ROOT, capture_output=True, check=True).stdout
        assert current.replace(b"\r\n", b"\n") == saved.replace(b"\r\n", b"\n"), rel
        assert hashlib.sha256(current.replace(b"\r\n", b"\n")).hexdigest() == digest, rel
    for source in manifest["sources"]:
        for path_key, hash_key in [("native_path", "native_sha256"), ("page_text_path", "page_text_sha256"), ("review_path", "review_sha256")]:
            assert sha(PAPER / source[path_key]) == source[hash_key], source[path_key]
    for rel, digest in manifest["curation_files"].items():
        assert sha(PAPER / rel) == digest, rel
    for rel, info in manifest["generated_files"].items():
        assert sha(PAPER / rel) == info["sha256"], rel
        assert (PAPER / rel).stat().st_size == info["bytes"], rel
    assert sha(PAPER / "scripts/build_literature_synthesis.py") == manifest["generator_sha256"]
    local_links = 0
    pinned_links = 0
    for path in DOCS.glob("*.md"):
        for url in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text()):
            parsed = urlparse(url)
            if not parsed.scheme:
                assert (path.parent / unquote(parsed.path)).resolve().exists(), (path, url)
                local_links += 1
            elif parsed.netloc == "github.com" and f"/blob/{snapshot}/paper1/" in parsed.path:
                rel = parsed.path.split(f"/blob/{snapshot}/paper1/", 1)[1]
                assert (PAPER / unquote(rel)).exists(), url
                pinned_links += 1
    for name in ["literature_table_92.xlsx"]:
        assert zipfile.ZipFile(OUT / name).testzip() is None
    assert zipfile.ZipFile(DOCS / "proposed_introduction.docx").testzip() is None
    wb = load_workbook(OUT / "literature_table_92.xlsx")
    for sheet, expected in [("Literature92", 92), ("Usable51", 51), ("Audit92", 92), ("Provenance92", 92), ("Eligible54", 54)]:
        assert wb[sheet].max_row - 1 == expected, sheet
        assert len(wb[sheet].tables) == 1 and wb[sheet].freeze_panes
    assert [r[0] for r in wb["Literature92"].iter_rows(min_row=2, values_only=True)] == list(by_id)
    assert not any(c.data_type == "f" for sheet in wb for row in sheet for c in row)
    pdf_stats = {}
    for name, ids in [("literature_table_92", set(by_id)), ("usable_51_report", detailed_ids), ("proposed_introduction", set())]:
        doc = fitz.open(DOCS / f"{name}.pdf")
        text = "\n".join(page.get_text() for page in doc)
        assert not (ids - set(re.findall(r"\bB[1-4]-\d{2}\b", text))), name
        assert "\ufffd" not in text
        for page in doc:
            for word in page.get_text("words"):
                assert word[0] >= -1 and word[1] >= -1 and word[2] <= page.rect.width + 1 and word[3] <= page.rect.height + 1, (name, word)
        pdf_stats[name] = {"pages": len(doc), "words": len(text.split()), "links": sum(len(page.get_links()) for page in doc)}
    print(json.dumps({
        "validation": "passed", "unique_papers": 92, "detailed": 51, "targeted": 41,
        "eligible_extract_rows": 54, "comprehensively_complete": 0,
        "local_markdown_links": local_links, "pinned_evidence_links": pinned_links,
        "native_sources_hashed": 92, "pdfs": pdf_stats,
        "protected_sources": "unchanged (Git LF canonicalisation respected)",
        "hold": "B2-12 combined1.5 MPa39.2 preserved and excluded",
    }, indent=2))


if __name__ == "__main__":
    main()
