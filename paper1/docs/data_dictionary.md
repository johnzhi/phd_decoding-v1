# Data dictionary and interpretation

All CSV files are UTF-8. `pdf_page` is a physical 1-based PDF page, including front matter; it need not equal printed journal pagination. Numerical units are original unless a result explicitly states its conversion.

- `source_catalogue.csv`: stable study ID, title, DOI/report identifier, repository-relative PDF/text paths, PDF SHA256, page count, reading coverage and applicability. `duplicate_of` prevents duplicate publication counting.
- `all_extracted_values.csv`: consolidated 1,642-record extraction history, including grouped ranges and earlier derived conversions in dedicated columns. `Extraction status` does not approve use as a regional input. Original earlier 1,097 records remain in `previous_1097_records.csv`.
- `new_batch_values.csv`: 193 new atomic records from B4. Contains value ID, source, original unit, page/table, scenario, evidence type, boundary, transfer limits and source locator excerpt.
- `curated_values.csv`: 250 atomic located quantities, overlapping the broad ledger. `ACCEPTED_FOR_STATED_CONTEXT` means usable only with the stated boundary. `HOLD_CONFLICT` prevents calculation with inconsistent source values.
- `analysis_inputs.csv`: 134-row exact subset of curated values. Every registered row is used. `group` selects a defined calculation or reported output. No context-only value enters the model.
- `issues.csv`: 59 source/interpretation issues, including a partly closed supplement-availability issue, with handling instructions. A source token match does not resolve an issue.
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

## Japanese case-evidence intake

`dataset7_manifest.json` and `dataset7_catalogue.csv` identify26 uploads,25 retained files,17 PDFs/1,186 indexed pages and the unavailable oversized IBDP ZIP. `case_numeric_values.csv` contains420 located quantities, including180 coordinate-located monthly/cumulative cells,8 fiscal cells and overlapping component/test records. These are not420 independent observations. Dedicated registers remain separate from the original1,642-record ledger.

`tomakomai_monthly_history.csv` preserves printed strings and exact10^4t conversion for45 months; cumulative/formation/combined series are not reconciled silently. `tomakomai_shutin_tests.csv` distinguishes local-clock dates, measurement duration, elapsed window, prior average rate and cause; the final ongoing window is empty. `tomakomai_falloff_reference.csv` contains nine source-inferred effective-property cases. `tomakomai_completion_scenarios.csv` preserves conditional completion-policy capacities, not annual rates or adopted probabilities. `tomakomai_history_audit.csv` reports rather than removes rounding/source differences.

`japan_company_emissions.csv` contains225 category/year cells,108 numeric; missing reports stay missing. `japan_facility_candidates.csv` has78 reporting-year records without automatic site merging or conversion of total GHG into capture supply. The identity audit prevents joining ENEOS additional information to Nippon Steel metadata. `cppi_port_reference.csv` preserves424 nonempty port-name rows; container indices/berth shares are not absolute CO2-terminal delays. D7-07 native cells are an additional8,008 raw cells, separate from the earlier17-workbook archive.

`northern_lights_components.csv` retains25 numeric and31 blank activity cells. `case_evidence_calculations.csv` has8 derived checks; `northern_lights_storage_proxy_comparisons.csv` has100 optional average-storage-burden transfers with null full-LCA results. Captured-source fugitives/aggregate shipping are not added to the existing ship-fuel model. All reference scope, phase, horizon and GWP differences remain explicit in the case review.

## Follow-up full-text review and component checks

`deep_review_cards.json` contains 44 manually written reading cards with actual reviewed physical pages, methods, findings, transfer limits and located candidate quantities. `prepare_deep_review.py` creates navigation packets only; `finalize_deep_review.py` checks the manual cards before updating the catalogue/digest. All 92 unique publications now have targeted full-text review, with zero abstract-only. This is selected-passages review, not exhaustive numerical/supplement extraction.

`deep_review_values.csv` has 140 located records, overlapping source evidence rather than extending a count of independent observations. Eighteen accepted entries form `limitation_benchmark_inputs.csv`: two for a paired MEA utility reference and 16 for within-source benchmarks. The other 122 remain context/HOLD. `limitation_benchmark_results.csv` gives eight within-source calculations, preserving fault-pressure-increase and volumetric boundaries. `deep_capture_reference_case.csv` pairs heat/electricity from the same MEA case; `MEA_reference_comparisons.csv` has ten replacement-utility sensitivities with blank full-LCA results.

`property_check_inputs.csv` locates the printed temperature, pressure and conflicting density quantities. `property_consistency.csv` gives two independent pure-fluid EOS calculations under explicit pressure-reference interpretations. They are model results, not additional measurements. `property_consistency_summary.json` records CoolProp/EOS version and provenance; `property_fleet_sensitivity.csv` checks all 75 fleet counts without replacing original source inputs.

## Shared-source mixed benchmark

`mixed_model_conventions.json` declares the common 1 Mt/y source class, disjoint reservoir groups, route distances, objective, source topology and missing terms. These structural choices are not extracted observations. `mixed_reservoir_plans.csv` contains 2,880 planned reservoir/year flows with resource/readiness/exogenous allocation envelopes; `mixed_trip_plans.csv` contains 720 integer route/year voyage/cargo/fuel records. `mixed_solver_audit.csv` has 12 annual MILP results. A zero reported solver gap concerns only the stated annual surrogate objective.

`mixed_operational_comparisons.csv` has 72 fixed-plan operating reevaluations; `mixed_operational_annual.csv` has 2,160 annual rows. Common-source conservation, ending inventory, active hours and null complete-LCA outputs are explicit. Route source shares are constant within each nominal year and sum to no more than the common potential; blocked unused shares are not adaptively reassigned. Dedicated export/receiving berths are a declared topology. `dispatch_policy_controls.csv` gives 18 additional original-design checks under three rules, not observations or proof of optimal dispatch. Full specification: [mixed allocation](mixed_allocation.md).

The workbook is a display copy of CSV registers. XML-prohibited control codes introduced by PDF font extraction are removed from workbook text only; the original PDF and UTF-8 CSV excerpts remain unchanged. Formula-like text is escaped in the workbook.

## Partial monthly and EXCOOL compilations

`dataset8_manifest.json` identifies the two unchanged uploads. `D8-02_cells.jsonl.gz` preserves289 nonempty native workbook cells across six sheets; no macros, formulas or external links are executed. `partial_compilation_values.csv` locates58 numeric cells plus two text claims, originally marked as pending. The current overlay now verifies33 directly and two by primary-input arithmetic, with25 pending. Of nine URLs in `partial_primary_source_leads.csv`, three have retained targeted-verified primary PDFs and six remain leads. Counts overlap and do not extend the count of independent observations or92 unique reviewed publications.

`tomakomai_paired_partial.csv` preserves seven calendar-month records, six with mass/P/T. Missing December mass/cumulative stays empty; calendar-average t/day uses calendar days rather than operating days. `partial_csv_workbook_agreement.csv` checks28 duplicate fields. `tomakomai_partial_reconciliation.csv` gives three consecutive-month balances and a conditional display-rounding bound; `tomakomai_partial_coarse_comparison.csv` compares12 masses with the retained rounded table without promoting them to verified native data.

`excool_loading_trial_leads.csv` keeps seven test rows distinct, including two June2025 entries. `excool_trial_property_checks.csv` supplies pure-fluid, standard-atmosphere EOS reference results, not measured cargo phase/density or operating limits. `tomakomai_capture_energy_leads.csv` holds four unverified reboiler/aggregate leads outside the GHG model. `partial_supplied_gap_map.csv` retains the supplied status claims and separately explains the current implemented scope. Further interpretation: [partial review](partial_monthly_evidence_review.md).

## Retained primary follow-up

`dataset9_manifest.json` identifies four unchanged uploads, including three PDFs/46 indexed pages and a secondary ZIP. Its four extracted members remain evidence rather than instructions. `verification_package_status_audit.csv` contrasts the supplied online-inspection assertions with actual local primary status; only three sources are locally upgraded.

`primary_followup_values.csv` has100 targeted quantities with SHA256, page, source token, bounding box, unit, case and extraction mode. Nine raster Table2 cells are visually checked rather than native-text matches. `excool_verified_loading_tests.csv` preserves all seven Table3 rows and printed precision/after-loading scope. `excool_reported_voyage_reference.csv` records three reported phases, not a generated time series or annual calendar. `tomakomai_primary_injection_tables.csv` has four formation-month rows with actual/planned/cumulative fields; `tomakomai_primary_header_totals.csv` keeps two current header dates separate. `tomakomai_primary_well_means.csv` has ten well-month P/T/depth records with unspecified pressure/depth reference retained.

`primary_followup_calculations.csv` contains14 derived checks. The260316.2t hypothetical May quantity is explicitly excluded as a corrected observation; the original260414.4t label and98.1t discrepancy remain. Voyage endpoint rates are within-source checks, not fixed thermal laws. The EOS table now also tests conditional nearest-displayed-unit rounding against saturation; it does not measure uncertainty or actual phase. The live60-claim compilation register retains `original_compilation_status` while adding primary or derived provenance. Reproduce by running the primary-verification script after compilation ingestion. [Interpretation](primary_source_followup_review.md).

## Public reservoir/capture intake — 12 November 2026

- `evidence/public_followup/source_manifest.json`: native URLs, retrieval routes/date, size/hash, upstream Bjarmeland ZIP hash,63-member directory and nine retained-member hashes. The source subset is repackaged; selected member bytes remain unchanged. The CEMCAP PDF matches Zenodo's published MD5 as well as the recorded local SHA256. The new intake does not change the 92-publication supplied corpus.
- `public_reservoir_parameters.csv`: seven deck-located controls/assumptions. `line_1based` indexes the native DATA member decoded with Latin-1 and splitlines. Base porosity/permeability precede region overrides; they are not complete spatial fields or measured Japanese properties.
- `public_reservoir_history.csv`:4,951 source timesteps, case CO2_BJ_C07B9. `time_days` is elapsed source time. `FGIR`/`WGIR_GI` are SM3/day, `FGIT`/`WGIT_GI` are SM3, `FPR`/`WBHP_GI` are bar absolute; `WOPR_OP2`/`WWPR_OP2`/`WGPR_OP2` are SM3/day of their respective source phases. Each value retains an RSM line locator. Printed tokens/precision remain unchanged; there is no mass conversion, day-zero insertion, interpolation or maximum-service interpretation.
- `outputs/public_reservoir_audit.json`: source/member hashes, paired-record count, pressure/rate control audit, field/well agreement, include closure and all seven source warnings. It explicitly records no independent rerun, annual maximum service or regional input replacement. A source end report with zero errors does not validate the model.
- `public_capture_values.csv`:42 CEMCAP Table 5.3 values, three cases, physical pages 22/23 (printed 16/17), exact token/unit and native table cell bbox. Page renders were visually checked. `use_as_regional_calibrated_input` is false throughout.
- `public_capture_inventory.csv`: three paired converted heat/auxiliary/compression/electricity/cooling inventories and source steam/product conditions. `heat_electricity_pair_complete_as_reported` is true only at the reported MEA/compression boundary; `full_lifecycle` and `eligible_for_regional_lca` are false. Cooling is heat rejection;110bar product is not ship-ready cargo. Solvent makeup is kg of 30 wt% solution per tonne captured. `jp_reporting_utility_kgco2_per_t` uses existing named reporting factors, not actual supplier/LCA factors. No duplicate compression, derate, cooling electricity or waste-heat credit is added.
- `outputs/public_evidence_summary.json`: new intake counts and explicit scope flags. It is separate from original operating/GHG outputs.
- `evidence/public_followup/firecrawl/` and `screening/mrst/`: raw searches/scrapes/errors and pinned source-code leads. Parser-created graph tables and unmatched VE/atlas properties are excluded from numerical registers. They are screening evidence, not executable instructions.

[Review, source links, limits and reproduction](public_reservoir_capture_review.md). Rebuild with `python paper1/scripts/public_evidence_followup.py`.
