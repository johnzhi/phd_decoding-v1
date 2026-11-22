# Literature synthesis and 92-paper table

This package answers two requests: what Paper 1 can use from the **51 detailed main-PDF reviews**, and a full literature table for **all 92 unique supplied publications**. It is a fixed report of evidence saved at commit `7e3a6f756d6fe2a73d71f39e41239d180d98c21f`, prepared 22 November 2026 in Asia/Kuala_Lumpur time. Later audit progress does not silently change this checkpoint.

## Read or download

| Deliverable | Editable / searchable | PDF |
| --- | --- | --- |
| Usable evidence from all 51 | [Report](usable_51_report.md), [overview](usable_51_overview.md), [CSV](../../outputs/literature_synthesis/usable_51.csv) | [51-paper synthesis](usable_51_report.pdf) |
| Full literature table, 92 rows | [Excel workbook](../../outputs/literature_synthesis/literature_table_92.xlsx), [full CSV](../../outputs/literature_synthesis/literature_table_92.csv), [Markdown table](literature_table_92.md) | [Literature table](literature_table_92.pdf) |
| Proposed integrated introduction | [Markdown with references](proposed_introduction.md), [Word document](proposed_introduction.docx) | [Introduction](proposed_introduction.pdf) |
| Existing eligible inputs from the 51 | [54-row extract](../../outputs/literature_synthesis/eligible_inputs_from_51.csv) | Included by source in the synthesis |
| Provenance | [Manifest](../../outputs/literature_synthesis/manifest.json) | Source/evidence links in both reports |

The proposed introduction is a concrete reuse example in fresh wording. It is a separate revision candidate; it does not replace the current manuscript.

## What the review labels mean

**Detailed:** all retained main-PDF pages have text-reading and visual-inspection records. In this checkpoint that is 51 papers / 710 pages. Tiny illegible labels, scientific inconsistencies and missing assets remain explicit in their individual records. This label does not certify every cited source, derivation or author model.

**Targeted:** an earlier selected full-text methods/results review exists, but the expanded every-item main-PDF audit remains pending. There are 41 such papers / 591 pages. Resolving first-page author/year metadata for the table does not change that status.

**Comprehensively complete:** zero papers. Full closure also requires the requested underlying-source, claim, supplement and independent-model verification. Bibliography/dependency records are not verified originals; scoped passage checks do not complete the cited paper.

B3-46 is retained as a duplicate of B2-17 and excluded from the 92 canonical rows. Separate later reservoir/process/primary-reference assets, including Bjarmeland, CEMCAP, Tomakomai and EXCOOL, are outside the 92-paper corpus.

## Workbook and field guide

- **Literature92:** citation, title, theme, geography, method, system/time boundary, pressure/service representation, main finding, proposed use/placement, source locators, numerical-transfer rule, principal limitation and review basis. Native PDF and evidence links are pinned to the source commit.
- **Usable51:** the 51 detailed-review papers only, with a concrete Paper 1 role, placement, locator and transfer boundary.
- **Audit92:** text/visual coverage, full-model status, supplement status and scope of component reconstruction. Prior targeted-only papers retain pending comprehensive status.
- **Provenance92:** original filenames/upload IDs, PDF/page-text/review hashes, DOI or non-DOI identifier, bibliographic basis/date notes, duplicate alias and source commit.
- **Eligible54:** a verbatim extract of the 54 rows already in the main `analysis_inputs.csv` from B1-11, B1-19, B2-08, B2-12 and B4-06. These are source-context benchmarks, not independent measurements or automatic regional physical approvals. Other reference-input registers are not enumerated by this count.
- **Held39.2:** the exact B2-12 combined 1.5 MPa source row, still on HOLD and excluded from the eligible extract. It is displayed to prevent accidental reuse.
- **Themes:** one primary organisational theme per paper; counts describe this analyst grouping, not a systematic-review taxonomy.

Filter tables and frozen identifier columns support navigation. Wrapped cell text can exceed the default displayed height; use Excel's formula bar or AutoFit Row Height to read it in full. No cell contains a formula. CSV stores all fields in one row per canonical paper; spreadsheet views separate them for usability. PDF/Markdown show the substantive literature fields for every paper; the CSV/workbook contains additional audit and provenance fields.

The table's **main finding** comes from the existing source digest with separately authored qualifications where a later detailed review supersedes the earlier description. The **proposed use**, **placement**, **primary theme**, **method/scope summary** and **numerical-transfer rule** are analyst synthesis, not native author text. Native records are preserved. In particular a useful method does not approve all numerical claims in a paper, and an unrelated source error does not automatically invalidate a separately supported paired output.

Short author/year citations are populated for every paper. Forty-nine previously blank catalogue entries were resolved using retained native first-page text and existing detailed identity sections. Metadata display overrides are separate from the unchanged catalogue. Issue/online/DOI-token years are distinguished where relevant; B3-15's issue year remains unverified. Non-DOI conference identifiers are not converted into invented DOI links. Short citations do not claim to list every coauthor.

## Provenance and rebuilding

Human-authored inputs are [notes.tsv](../../evidence/literature_synthesis/notes.tsv), [metadata_overrides.json](../../evidence/literature_synthesis/metadata_overrides.json), [the overview](usable_51_overview.md) and [the introduction template](proposed_introduction.template.md). The generator reads source catalogue, page text, detailed records, selected-passage packets and the current main input register, verifies the fixed source checkpoint and native PDF hashes, then builds the deliverables. The manifest records source and output SHA-256 hashes, not a claim to have rerun author models.

From the repository root:

```sh
python -m pip install -r paper1/requirements.txt
python paper1/scripts/build_literature_synthesis.py
python paper1/scripts/validate_literature_synthesis.py
```

The build also needs the `pandoc` executable and DejaVu Sans fonts (`/usr/share/fonts/truetype/dejavu`). PDF and Office ZIP bytes may vary with library/container timestamps; regenerate semantic contents and manifests together. The script writes only this synthesis package and its outputs. It fails when protected sources or the 51-record membership differ from the checkpoint. For a future refresh, deliberately revise the snapshot, counts, authored findings and document dates together; preserve this historical membership/report when requested.

Existing source PDFs, comprehensive records, curated values, accepted inputs, numerical outputs and manuscript are unchanged. External original/code/SI retrieval remains paused pending the requested Chrome connection. The broader 92-paper audit remains open; the next main-PDF audit is B3-09.

## Validation for this delivery

All 306 existing repository tests passed. Package validation checks exact 92/51/41 membership, 54 unchanged eligible input rows, the preserved 39.2 HOLD, source/output hashes, local and pinned evidence links, workbook/Word ZIP integrity, workbook row counts/formula absence, complete PDF paper-ID coverage and text bounds. Selected table/report/intro pages were also rendered and visually inspected. These checks validate the deliverables and preservation; they do not complete author-model or underlying-literature verification.
