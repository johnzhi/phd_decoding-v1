# Continuation queue

The comprehensive audit is active and unfinished. Reading is not citation verification or full model reproduction. See the [progress register](README.md) and [complete pending-paper list](../../outputs/comprehensive_review/papers.csv).

1. Review B1-09, then the remaining local main PDFs, prioritising pressure/injection, ship conditioning and lifecycle evidence. The [B1-08 findings](../flow_assurance_comprehensive_findings.md) cover all13 pages and53 limited checks. Own-well capacity fractions, transient warm-restart time, corrosion reference bases and equivalent-service/utility boundaries remain qualified; full models andseven source/method dependencies stay open. The [B1-07 findings](../higashi_niigata_comprehensive_findings.md) cover all11 pages and preserve the unscaled pressure/CO2 curves, missing annual outputs and relief-water inventory. Its14 source/model dependencies and complete history/forecast cases remain open.
2. Continue exact retained-source support checks. Three citation edges have qualified primary checks; their limits are in the [audit overview](../comprehensive_audit.md). Similar titles, changed editions or different DOIs are not substitute originals.
3. Resolve the missing case/supplement inputs recorded for each paper. Recent [B1-06](../openhole_comprehensive_findings.md), [B1-04](../deepwater_japan_comprehensive_findings.md), [B1-03](../total_efficiency_comprehensive_findings.md) and [B1-01](../occs_comprehensive_findings.md) records retain their open models and scientific qualifications. The retained B4-06 supplement does not close that paper's full optimiser or physical service model.
4. External originals, publisher supplements, errata, code and author requests remain pending under the user's request to wait for a Chrome connection. Local reading/calculations can continue. Do not silently resume Firecrawl or direct public downloads.
5. Keep diagnostics separate from accepted Paper1 operating/GHG inputs. Preserve source hashes, units, missing values and unresolved identities; save verified checkpoints to the same GitHub branch.

Run `comprehensive_audit.py` to regenerate the corpus/page registers and authored views. The limited diagnostic/reproduction scripts and their scope are listed in the [audit overview](../comprehensive_audit.md). `audit_higashi_niigata.py` explicitly leaves absolute mass, pressure, annual flow and relief-water inventory uncomputed.

`audit_flow_assurance.py` checks displayed margins/indices while preserving missing well capacities, absolute utilities and annual schedules.
