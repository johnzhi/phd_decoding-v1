# Comprehensive scientific audit

Requested on21November2026: review every section, figure/graphic/table/caption/legend, equation/derivation/variable/unit/assumption, literature claim and its underlying cited source, result/discussion claim, supplement and independently reproducible model across all92 unique supplied publications. This work is **in progress**, not complete. The earlier targeted full-text reviews do not meet this expanded standard.

The [current progress register](comprehensive_review/README.md) distinguishes retained-PDF reading from scientific verification. The corpus has93 retained PDFs,92 unique publications and1,301 unique physical pages; B3-46 remains a preserved duplicate, not a second reviewed publication. Later reference intakes are separate assets and can support this audit where properly matched.

## Evidence required for closure

1. Read every physical page and inspect its rendered layout. Catalogue all sections, panels, captions, legends, table headers/footnotes and appendices. Magnify small labels and equations; native text can omit expressions and misrepresent tables. Record unreadable or unresolved content explicitly.
2. Transcribe and interpret every equation and its indices, variable domains, units, assumptions and stated derivation. Check dimensional/elemental/stock-flow consistency. Separate a source's literal notation from an analyst's proposed correction. Verify essential cited derivations in their original sources.
3. Map each direct bibliography entry and unnumbered named authority to the claim it supports. Locate the original, verify provenance and relevant passages/figures, and record disagreements or missing support. Reading a bibliography, matching a title/DOI or a prior targeted review is not this verification. Follow additional citation dependencies where necessary to validate a derivation or claim; do not label an unbounded recursive citation search complete.
4. Assess each result/discussion claim against the paper's inputs, calculations, figures and uncertainty. Recompute quantities that have sufficient inputs; retain exact source numbers and distinguish estimates read from plots. Claims depending on missing data or unsupported corrections stay open or excluded.
5. Check supplement/code/data availability, archives and version correspondence. Read supplied supplements fully. Independently reproduce author models only when inputs and methods suffice, then compare outputs, balances and uncertainty with stated tolerances. A rounded schedule replay, atom balance, arithmetic check or our own Paper1 model is not independent reproduction of an author's optimiser/reservoir/process model. Log missing assets and failed attempts rather than supplying guessed inputs.

These are separate dimensions. A paper is not comprehensively complete because every page was read. An unavailable original, unresolved mathematical convention or unreproduced model must remain visible. For non-model documents, justify why reproduction is not applicable and identify any underlying model-bearing paper; a synopsis does not replace it.

## Current substantive findings

- [B1-02](comprehensive_review/B1-02.md): all9 pages,9 figures, Table1 across2 pages and4 numbered reactions inspected. The table's literal gas-energy units remain on hold. Independent arithmetic supports the reported31%/24% counted-carbon reductions, subject to the explicit recycle boundary; it is not a complete lifecycle result. Figure6 needs flow-routing clarification. Figure8 was located and magnified after an initially missed lower panel; it is present.
- [B1-05](comprehensive_review/B1-05.md): all4 synopsis pages and the map inspected. The source really prints1.6tonnes/year; no missing multiplier is silently restored. Reported150kg/s and4Mt/year require an annualisation basis. OriginalSPE225882, itsTable1 and source trail are still missing. This is a synopsis of a paper stated not to be peer reviewed.
- [B4-05](comprehensive_review/B4-05.md): all6 pages,15 equations,2 figures,3 tables and nomenclature inspected. Literal transport-cost, period-unit, quality/load and outage-bound conventions need clarification. A small counterexample shows thatEq12 can allow a stream above the claimed concentration limit. This does not reproduce or establish a bug in the authors' unpublished implementation. The case is biochar/bio-oil, not calibrated geological CO2 storage.
- [B3-11](comprehensive_review/B3-11.md): all 11 pages, 11 figures and 8 tables inspected. Independent reconstruction matches the hypothetical 200/100 Mt external/excess targets and every one of the 19 main CSCA rows (40 Mt additional, 80 Mt excess). Literal allocation tables fail plant/year balances; Option 2 also exceeds reservoir B's total capacity. These conflicts remain on hold. The cumulative service method does not establish physical injection-rate feasibility. [Reconstructed figure](../outputs/comprehensive_review/B3-11_cascade.png) and [full calculations](../outputs/comprehensive_review/B3-11_reproduction.json) are retained.
- [B4-06 and its supplement](budiarto_comprehensive_findings.md): all 20 main pages, 11 figures, 3 tables and the retained DOCX's 3 tables/10 figures inspected. Twenty-one diagnostics reproduce source-mass, map-total and transport-average arithmetic while preserving annual injection-bound, source-balance, cost-basis and exact-route questions. Two of its 58 direct citation edges now have qualified primary support; the wider chain and complete process/well/MILP reproduction remain open.
- [B4-08](zhang_lau_comprehensive_findings.md): all 22 pages, 14 figures, 18 tables, 5 equations, nomenclature, internal appendix and 232 bibliography entries read/inspected. The independent Eq5 component reproduces all 24 aquifer basin/scenario values at displayed precision. The B4-06→B4-08 citation supports resource provenance with E=1 and limited properties, but does not establish anonymous field identities or annual pressure-constrained service. MMP units, field-model implementation, sector labels and histogram basis remain open. All 232 underlying originals remain unverified.

- [B3-44](simccs_comprehensive_findings.md): all nine pages, six figures, Table1, 23 numbered equations, the radial derivation and28 references inspected. Printed property/well-cost functions and21 unit/aggregation diagnostics are implemented; no California GIS/MILP or well iteration is independently reproduced. The paper explicitly uses simultaneous infrastructure, lifetime stocks and artificially reduced pipeline costs. Pressure-unit and printed-index questions remain on hold.

Three citation edges have now been checked against retained originals. B4-05's Ooi2013 citation supports temporal planning, but its MILP attribution conflicts with B3-11's graphical/algebraic method. B4-06's Zhang/Lau2022 citation supports regional resource provenance and limited properties, with pressure/time-dependent service still absent. B4-06’s SimCCS citation supports the static MILP mechanism, with artificial-cost and atemporal-case limits. The other underlying sources, including B3-11's own 25 and B4-08's 232 references, remain unverified under this expanded standard. No supplement absence on the public web is inferred from a local PDF having no embedded files. The CSCA and aquifer-resource accounting components are independently reproduced; no complete author optimiser, pressure-constrained reservoir or detailed valid allocation is claimed reproduced.

## Provenance, outputs and continuation

Manual records live in `evidence/comprehensive_review/*.json`, anchored to sourceSHA-256 and physical pages. The script validates hashes/page counts, creates the full92-paper/1,301-page pending register, inventories text/DOI/link candidates and renders the reading records. Extraction never creates a completed-reading declaration. The manual issue register is separate from the previous59 targeted-review issues so historical counts/statuses retain their meaning.

```sh
python paper1/scripts/comprehensive_audit.py
python paper1/scripts/audit_diagnostics.py
python paper1/scripts/reproduce_ooi_cascade.py
python paper1/scripts/audit_budiarto_fulltext.py
python paper1/scripts/reproduce_zhang_lau_aquifers.py
python paper1/scripts/audit_simccs_components.py
python -m unittest discover -s paper1/tests -v
```

Diagnostic calculations preserve printed quantities and explicit calendars/bases. They do not feed the operating/GHG model. Unsupported inputs remain excluded; original PDFs, targeted-review catalogue and existing Paper1 numerical outputs are preserved.

External retrieval remains paused under the user's explicit request to wait for a Chrome connection. Local reading and calculations can continue. Verification of missing cited originals, public supplements, errata and author code remains pending until permitted access is available. B4-08 and B3-44 retained primary checks are recorded with limits; B1-01 is next in the local queue.
