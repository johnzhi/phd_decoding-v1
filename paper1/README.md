# Paper 1 research package

Start with [the manuscript](manuscript/Paper_1_draft.md), its editable DOCX, [all extracted values](data/all_extracted_values.csv), and [the evidence digest](docs/evidence_digest.md).

This package contains 92 unique supplied publications (93 PDFs), the original proposal, 1,642 extracted-value records, 250 curated PDF quantities and 134 original benchmark inputs, plus 352 numeric supplementary records. The results contain 49 calculations and 75 published fleet counts. Forty-eight publications have targeted extraction and 44 have abstract/relevance screening. These counts describe review coverage, not 92 fully inventoried papers.

The draft includes real source-based benchmark results and an explicitly labelled cross-study proxy stress test. Indonesian storage outcomes and Norwegian post-capture intensities are not presented as measured Japanese geology or as a calibrated international project. See [proxy register](docs/proxy_register.md), [data dictionary](docs/data_dictionary.md), and [remaining work](docs/remaining_work.md).

## Reproduce

From the repository root:

```sh
python -m pip install -r paper1/requirements.txt
python paper1/scripts/ingest_budiarto_supplement.py
python paper1/scripts/replay_budiarto_supplement.py
python paper1/scripts/reproduce.py
python paper1/scripts/operational_model.py
python paper1/scripts/ingest_reference_datasets.py
python paper1/scripts/extract_ibdp_reference.py
python paper1/scripts/reference_inventory.py
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

## Budiarto supplement update

The supplied supplementary DOCX is archived in `original/supplements/`. [Supplement review](docs/supplement_review.md) explains the 102 native-table values,250 rounded annual injection annotations and 470 blank grid cells. The 14 source rates sum to 5.327 Mt/year; over 30 annual bins this matches the reported 159.81 Mt multi-well storage total. Rounded annual schedules are replayed explicitly, without claiming an independent MILP or whole-chain mitigation simulation.

## Operational model

B0–B3 now run with explicitly declared aggregate service proxies, ship/terminal inventories and deterministic availability conventions. [Model scope and controls](docs/operational_model.md) explain the 144 comparisons and why they are conditional. [Operating inputs](data/operational_parameters.csv) list 30 source-located quantities; [data gaps](data/operational_data_gaps.csv) identify what is still required for full lifecycle GHG. Missing quantities are not zeroed, and complete net avoided emissions remain uncomputed.

## Reference datasets and inventory extension

The next intake contains **104 uploads,100 accessible files and95 distinct accessible binaries**. Four IBDP reports exceed the32MiB transfer-tool limit and are listed as unavailable. This intake is separate from the original92-publication review. Indexing a file does not imply exhaustive scientific review. See the [reference-data review](docs/reference_dataset_review.md) and [specific remaining data requests](docs/reference_data_requests.md).

The evidence workbook now includes77 located reference-inventory inputs,8 NETL capture-reference cases,12 Illinois reservoir-simulation quantities,3,269 located current Japanese factor records and34 wave-snapshot variables. Counts overlap their original tables and are not counts of independent observations. The raw native workbook archive retains1,013,036 nonempty/formula cells from17 workbooks, including formulas, cached values and errors; macros and external links were not run. This archive is searchable JSONL in `evidence/reference_workbooks/`, not approved model inputs.

Twenty distinct utility-accounting scenarios and the IMO MDO/MGO default fuel pathway produce2,980 partial inventory comparisons. Electrical replacement and heat-plus-auxiliary routes are mutually exclusive. The source-derived defaults improve the inventory but do not establish actual plant utilities, future grid factors or complete lifecycle GHG. The design-controlled5,000km case has only about+0.009Mt remaining allowance under the NGCC90/Norway-climate reference; Japanese fallback-factor examples are negative. No robust destination preference follows.

Both uploaded wave subsets are single-point, single-time snapshots. IBDP microseismic event rates are separate from injection rates. The supplied St.Peter/Knox-Potosi report is an independent simulation reference; paired injection-monitoring rate/pressure histories remain needed. The BagIt audit verifies27/31 expected payloads rather than a complete bag. [IBDP attribution and terms](original/dataset6/ATTRIBUTION.md) accompany the retained files.
