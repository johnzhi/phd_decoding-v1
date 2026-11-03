# Data dictionary and interpretation

All CSV files are UTF-8. `pdf_page` is a physical 1-based PDF page, including front matter; it need not equal printed journal pagination. Numerical units are original unless a result explicitly states its conversion.

- `source_catalogue.csv`: stable study ID, title, DOI/report identifier, repository-relative PDF/text paths, PDF SHA256, page count, reading coverage and applicability. `duplicate_of` prevents duplicate publication counting.
- `all_extracted_values.csv`: consolidated 1,290-record extraction history, including grouped ranges and earlier derived conversions in dedicated columns. `Extraction status` does not approve use as a regional input. Original earlier 1,097 records remain in `previous_1097_records.csv`.
- `new_batch_values.csv`: 193 new atomic records from B4. Contains value ID, source, original unit, page/table, scenario, evidence type, boundary, transfer limits and source locator excerpt.
- `curated_values.csv`: 250 atomic located quantities, overlapping the broad ledger. `ACCEPTED_FOR_STATED_CONTEXT` means usable only with the stated boundary. `HOLD_CONFLICT` prevents calculation with inconsistent source values.
- `analysis_inputs.csv`: 134-row exact subset of curated values. Every registered row is used. `group` selects a defined calculation or reported output. No context-only value enters the model.
- `issues.csv`: original 29 source/interpretation issues plus eight new issues, with handling instructions. A source token match does not resolve an issue.
- `proposal_claim_audit.csv`: original 14 proposed references linked to supplied primary PDFs, with corrections. This is a claim audit, not endorsement of novelty.
- `calculated_results.csv`: 49 derived rows and 75 directly transcribed published fleet outputs. `input_ids`, `equation`, units and boundary are explicit. `Rxxx` is an output ID, not an empirical observation.

Source excerpts are mechanically selected adjacent to a number to help navigation. For short tokens they can locate another occurrence on the same page; the scenario and table locator govern interpretation. Table-column mapping was checked for the calculation datasets. Automated checks verify presence, file identity and exclusion rules, not scientific validity.

A percentage, unit definition (1 t = 1000 kg) or algebraic identity is not an empirical assumed parameter. Any calculation from reported rounded values inherits their limited precision. Displayed decimals are computational, not additional empirical accuracy.

No probabilities are inferred from published ranges. No cost is converted to GHG. No national storage resource is treated as annual deliverability. No pressure ratio is treated as an injection-rate ratio. No missing graph scale is invented. No synthetic annual profile is derived from cumulative tonnes.
