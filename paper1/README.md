# Paper 1 research package

Start with [the manuscript](manuscript/Paper_1_draft.md), its editable DOCX, [all extracted values](data/all_extracted_values.csv), and [the evidence digest](docs/evidence_digest.md).

This package contains 92 unique supplied publications (93 PDFs), the original proposal, 1,290 extracted-value records, 250 curated quantities and 134 registered analysis inputs. The results contain 49 calculations and 75 published fleet counts. Forty-eight publications have targeted extraction and 44 have abstract/relevance screening. These counts describe review coverage, not 92 fully inventoried papers.

The draft includes real source-based benchmark results and an explicitly labelled cross-study proxy stress test. Indonesian storage outcomes and Norwegian post-capture intensities are not presented as measured Japanese geology or as a calibrated international project. See [proxy register](docs/proxy_register.md), [data dictionary](docs/data_dictionary.md), and [remaining work](docs/remaining_work.md).

## Reproduce

From the repository root:

```sh
python -m pip install -r paper1/requirements.txt
python paper1/scripts/reproduce.py
python -m unittest discover -s paper1/tests -v
python paper1/scripts/build_workbook.py
python paper1/scripts/build_documents.py
```

`reproduce.py` validates source hashes, page counts/text locators and calculation eligibility, then writes CSV/JSON results and publication-format PNG/PDF figures. It does not fit or simulate missing annual injection data. Hash/text checks cannot validate a paper's model or remove the need to inspect table mapping and boundaries. Dependencies are listed in requirements; DOCX generation additionally uses the `pandoc` command.

`extract_text.py` can regenerate plain PDF-page text with PyMuPDF, writing a separate directory so the retained layout-preserving text and locators are not overwritten. The provenance ledger remains authoritative for the retained extraction version.

## Files and preservation

`papers/` stores each retained original supplied PDF under its stable ID. Original filenames/hashes are in the catalogue; publication duplicate B3-46 is preserved. Existing PDFs in the repository root are untouched. `evidence/pages/` contains searchable per-page text. `original/` contains the user proposal. `history/` preserves previous preparation artifacts and scripts; historical scripts may have workspace-specific paths and are not the reproducibility entry point.

Previously downloaded originals are reused for same-title reuploads; no binary equivalence is asserted for each reupload. The Drive folder was not ingested. The planetary-limit ZIP exceeded the tool's 32 MiB transfer limit and is not archived; the standalone PDF is included. No results rely on uninspected ZIP contents.

The supplied scholarly PDFs retain their original rights and licences; no repository code licence is extended to them. All input/result files use explicit provenance rather than an unsupported claim of originality.
