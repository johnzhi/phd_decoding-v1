# Data dictionary and interpretation

All CSV files are UTF-8. `pdf_page` is a physical 1-based PDF page, including front matter; it need not equal printed journal pagination. Numerical units are original unless a result explicitly states its conversion.

- `source_catalogue.csv`: stable study ID, title, DOI/report identifier, repository-relative PDF/text paths, PDF SHA256, page count, reading coverage and applicability. `duplicate_of` prevents duplicate publication counting.
- `all_extracted_values.csv`: consolidated 1,642-record extraction history, including grouped ranges and earlier derived conversions in dedicated columns. `Extraction status` does not approve use as a regional input. Original earlier 1,097 records remain in `previous_1097_records.csv`.
- `new_batch_values.csv`: 193 new atomic records from B4. Contains value ID, source, original unit, page/table, scenario, evidence type, boundary, transfer limits and source locator excerpt.
- `curated_values.csv`: 250 atomic located quantities, overlapping the broad ledger. `ACCEPTED_FOR_STATED_CONTEXT` means usable only with the stated boundary. `HOLD_CONFLICT` prevents calculation with inconsistent source values.
- `analysis_inputs.csv`: 134-row exact subset of curated values. Every registered row is used. `group` selects a defined calculation or reported output. No context-only value enters the model.
- `issues.csv`: 49 source/interpretation issues, including a partly closed supplement-availability issue, with handling instructions. A source token match does not resolve an issue.
- `proposal_claim_audit.csv`: original 14 proposed references linked to supplied primary PDFs, with corrections. This is a claim audit, not endorsement of novelty.
- `calculated_results.csv`: 49 derived rows and 75 directly transcribed published fleet outputs. `input_ids`, `equation`, units and boundary are explicit. `Rxxx` is an output ID, not an empirical observation.

Source excerpts are mechanically selected adjacent to a number to help navigation. For short tokens they can locate another occurrence on the same page; the scenario and table locator govern interpretation. Table-column mapping was checked for the calculation datasets. Automated checks verify presence, file identity and exclusion rules, not scientific validity.

A percentage, unit definition (1 t = 1000 kg) or algebraic identity is not an empirical assumed parameter. Any calculation from reported rounded values inherits their limited precision. Displayed decimals are computational, not additional empirical accuracy.

No probabilities are inferred from published ranges. No cost is converted to GHG. No national storage resource is treated as annual deliverability. No pressure ratio is treated as an injection-rate ratio. No missing graph scale is invented. No synthetic annual profile is derived from cumulative tonnes.

## Budiarto supplement update

- `supplement_documents.csv`: supplementary DOCX identity, parent publication and hash; it is not counted as a new unique publication or PDF.
- `supplement_sources.csv`, `supplement_reservoirs.csv`, `supplement_distances.csv`: faithful native-table extraction. The two dash distance entries remain missing; they are not zero-length links.
- `supplement_table_values.csv`: 102 atomic numeric entries from Tables S1–S3.
- `supplement_annual_injection.csv`: 720 scenario/reservoir/year cells (2027–2056), of which250 have printed one-decimal values and 470 are blank. `cell_bbox` locates the annotation in the exact extracted source image. Blanks are not numeric zeros.
- `supplement_values.csv`: the 352 numeric table/figure records added to the broad ledger. It overlaps the structured supplementary tables, so do not add their counts together.
- `supplement_annual_replay.csv`: sums printed allocations only. Blanks represent no reported allocation for this reconstruction. Nominal annual source-minus-allocation differences are not called measured venting or physical excess.
- `supplement_scenario_summary.csv` and `supplement_reservoir_audit.csv`: compare rounded allocations with main-paper totals/readiness/capacity. No rounding discrepancy is silently corrected.
- `conditional_rounding_*` assumes conventional nearest 0.1 printing (±0.05 per annotated cell). This derived display-resolution envelope is neither a statistical interval nor proof of raw-model reproduction. Source rates retain their three-decimal precision; the rate-sum halfwidth is likewise a resolution check.

The original134-row analysis input file and 250-row curated PDF table remain the first benchmark dataset. Supplementary numeric records are maintained separately so their different locators and precision are explicit. The source and image checks for them run in `replay_budiarto_supplement.py`.

## Operational extension

`operational_parameters.csv` contains 30 source-located operating quantities and their transfer restrictions, including quantities already represented elsewhere. It is a complete operating-input register, not 30 additional independent observations. `operational_model_conventions.json` records structural choices and excluded inventory components. The original 1,642-record extraction ledger remains separately stable; overlap between registers must not be added as unique data.

`operational_annual.csv` records actual simulated capture, injection, source/destination/marine stocks, fuel, active/waiting hours and curtailment. `operational_comparisons.csv` contains144 paired results; `net_avoided_ghg_t` is empty because the full inventory is missing. `operational_contrasts.csv` separates the full representation contrast from the two-factor interaction.

`operational_controls.csv` contains equal-injection and one-added-vessel controls. `operational_design_adequacy.csv` and `operational_design_comparisons.csv` report a restricted added-fleet search using a transferred 99%-of-continuous-no-inventory-reference criterion. It is not a reliability probability or economic optimum. `operational_reliquefaction_envelope.csv` adds an optional full-nameplate 8,000h/year generator-duty scenario, not a predicted BOG duty. `operational_fleet_validation.csv` reproduces 75 source fleet counts.

The allowance is injected-mass difference minus inventoried active ship-combustion CO₂ difference. Conditional full advantage requires additional uninventoried burdens to be less than that allowance, after source-counterfactual/retention reconciliation. No missing emission factor is imputed as zero. Outputs and analyst decisions are not empirical data.

## Reference-data intake

- `dataset5_manifest.json` and `dataset6_manifest.json`: upload identity, retained relative path, SHA256, file size, duplicate links, indexed PDF pages, and explicit transfer errors.104 uploads;100 available;95 distinct accessible binaries. `reference_dataset_catalogue.csv` adds review/transfer coverage. Indexed does not mean fully digested.
- `reference_workbooks/*_cells.jsonl.gz`: native sheet/cell identity, cached value, type, style index and formula/attributes.17 workbooks;1,013,036 nonempty/formula cells. Original ZIP/XML remains authoritative for styles and unsupported workbook features. No macro execution, external-link refresh or recalculation. These are raw archival cells, not analysis-approved measurements. The malformed Norway sales used range is handled by reconstructing omitted cell references in sheet row/column order.
- `reference_inventory_inputs.csv`:77 explicitly located numerical quantities used in reference capture/fuel/utility calculations. PDF pages are physical1-based. NETL cells are cached reference parameters. Exact lb–kg and power/energy unit conversions are definitions, not empirical assumptions.
- `netl_capture_reference_cases.csv`:8 normalised cases. `electric_makeup` is auxiliary demand plus steam-turbine electric opportunity loss; its heat field is empty. `heat_plus_aux` is derived net reported utility enthalpy import plus incremental auxiliaries, with no turbine-derate addition. Empty fields mean a different accounting route, not physical zero heat. Compression is already present within the reference boundary.
- `japan_current_factors.csv`:3,269 located current electricity/heat/gas reporting-factor records, with raw footnoted values, original unit, provider/menu/base/adjusted/fallback identity. They are not a matched actual supplier or full LCA. Historical workbook cells remain in the native archive. Gas volume is not converted to heat without a calorific and efficiency basis.
- `capture_utility_scenarios.csv`:20 reference combinations with distinct Norwegian climate disclosure, Japanese reporting fallback and market-disclosure accounting. Historical factors are frozen scenarios, not forecasts. Their methodological coverage is not silently harmonised.
- `reference_inventory_comparisons.csv`:2,980 conditional balances. Capture energy uses additional **captured** mass; marine default WtW replaces the earlier combustion-only component. `remaining_uninventoried_allowance_t` subtracts those named inventories from additional injection; its coverage follows the named factor scenario. `complete_net_avoided_ghg_t` is empty. These balances are not destination rankings or complete climate results.
- `wave_coverage.csv` and `wave_snapshot_values.csv`: two points with one timestamp each and34 variable values. Native float scaling/precision and units are preserved; no annual downtime or threshold is derived.
- `ibdp_reservoir_reference_values.csv`:12 quantities from the St.Peter/Knox-Potosi simulation report, with formation, page and evidence type. They are not Mt.Simon observed injection limits, and no unreported annual series is interpolated. Seismic-event rate workbooks are retained separately and do not represent CO₂ injection rates.
- `ibdp_bag_checksum_audit.csv`: payload/tag checks for supplied SHA256/SHA512 manifests.27/31 payload matches are partial validation; four oversized reports remain absent. IBDP terms and attribution are retained with the originals.

The original1,642-record literature ledger stays stable. Dedicated input/factor tables overlap source records and must not be summed into a count of independent data. Raw cell preservation, curated extraction, derived results and analyst conventions remain separate.
