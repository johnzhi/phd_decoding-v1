# B2-02 prospective-assessment review: findings and limits

Pingping Wang, Ada Josefina Robinson and Stavros Papadokonstantakis (2024), DOI `10.3389/fenrg.2024.1412770`. All 26 physical pages of the [retained original](../papers/B2-02.pdf) were read and visually inspected, including seven figures, three tables, both numbered equations, the glossary and 192 printed bibliography entries. The [item register](comprehensive_review/B2-02.md) and [manual record](../evidence/comprehensive_review/B2-02.json) retain physical-page provenance, 93 claim records and open issues.

**This paper remains incomplete under the comprehensive-audit standard.** All 192 underlying originals and ten data/model dependencies remain unverified. Claim-to-reference pointers identify what this review attributes to a source; they do not verify that source. No native DAC cost projection, LCA inventory, IAM scenario or integrated feedback model is independently reproduced.

## What the paper supplies

This is a methodological review and proposed framework linking prospective TEA, prospective LCA and integrated assessment models. Figures 1, 6 and 7 describe information flows, scenario mapping and feedback. They do not provide an executable coupled case, a semantic crosswalk, convergence criteria, version-pinned code or native scenario arrays. Naming open-source tools is not evidence that the full workflow was run or validated.

The paper identifies useful requirements: common functional units, future incumbents as comparators, aligned foreground/background scenarios, uncertainty analysis and technology-specific detail. It does not supply the complete same-case heat, electricity, compression, liquefaction, cooling and supplier inventory sought for Paper 1, or pressure/rate data establishing annual reservoir service. “No additional energy for CO2 separation” in the inherent-capture discussion is a separation-boundary statement; it does not imply zero oxygen-production, total-process or conditioning energy.

## Learning equations: an available component and a literal mismatch

Equation 1 defines `LR = 1 − 2^(−b)`. The inverse is `b = −ln(1−LR)/ln(2)`, and a constant-rate component after `k` capacity doublings satisfies `C/C0 = (1−LR)^k`. Costs, capacity units and the service basis must be consistent. Learning from capacity is not a calendar forecast; deployment histories, learning periods and component assignments are still needed.

Equation 2 first gives `sum_i C0i (xti/x0i)^(−bi)`. Its expanded second term instead prints `C02 (xt2/x01)^(−b2)`, using the first component's initial capacity. This generally differs from the summation when initial capacities differ. The source notation is preserved; no correction is silently adopted and no defect in unavailable author software is alleged.

A disclosed synthetic example uses costs `(100,200)`, initial capacities `(10,100)` and learning rates `(0.2,0.1)`. At the initial capacities, the summation gives 300 while the literal expansion gives approximately 240.938. After each capacity doubles, the summation gives 260 and the expansion approximately 206.844. These arbitrary-unit examples expose the algebraic inequality, not a DAC forecast.

The [31 diagnostics](../outputs/comprehensive_review/B2-02_checks.csv) and [27 dimensionless component rows](../outputs/comprehensive_review/B2-02_learning_components.csv) reconstruct only these available learning components and conditional capacity-unit arithmetic. [Reconciliation](../outputs/comprehensive_review/B2-02_reconciliation.json) leaves native cost, inventory, IAM and coupling models open. The attributed technology-type learning means/stds `(0.22,0.05)`, `(0.13,0.04)` and `(0.05,0.04)` have no supplied probability distribution, bounds, dependencies or process assignments. No Monte Carlo forecast is invented.

## Tables and graphics constrain quantitative use

Table 1 contains 17 DAC projection rows from eight source groups. The [literal transcription](../evidence/comprehensive_review_inputs/B2-02.json) retains initial/future costs, technology, TRL, learning-rate strings, location, shared cells and both footnotes. Initial capacity is labelled tonnes CO2 while future capacity is labelled MtCO2: a comparable ratio requires a million-fold unit conversion. Whether every row shares the same cumulative-capacity and net-removal basis still requires the originals. The `1,4` target-capacity cell and slash conventions are preserved without guessing their meaning. Two starred DAC rows explicitly have unclear inclusion of storage. Cost years, component shares, utility cases and deployment histories are missing. Applying one aggregate learning rate to the displayed total cost would not reproduce the underlying component models.

Table 3 contains five CCS/DAC examples and twelve CCU routes. Their denominators include electricity service, cement, captured CO2 and CO2 treated; these are not interchangeable. The CCU impact column lacks explicit mass/impact units, DAC toxicity values `+18` and `+45.2` lack percent symbols, one human-health `55%` lacks an explicit sign, and “Water Land use” is ambiguous. The source says its CCU examples are not prospective LCA studies and declines to establish a universal technology ranking. Preserve those qualifications rather than repairing the table or treating negative comparative values as physical removal fractions.

Figure 2's smallest `0.01*` marker represents **unknown announced capacity**, as its caption states. It must not become a small positive capacity input. Overlapping project categories and markers do not supply exact project arrays. Historical 41/392 project counts, 102% growth, 361 Mt and around 400 Mt/year are not a common current operating dataset. The abstract and body describe 400 Mt/year as announced capacity; the conclusion calls it current deployment. No 2026 operating supply is inferred.

Figure 3 groups technologies into TRL 1–3, 4–6 and 7–9 bands. Its depleted-field and EGR placements differ from prose ranges of 6–8. The transport ring lies in the 7–9 band, while prose says transport has universally achieved TRL9. Exact technology, sector, scale and conditions need the originals. Ordinal maturity does not establish efficiency, availability, pressure safety or retention. Figure 1's embedded IPCC plot lacks recoverable complete scenario labels/arrays; no precise pathway is digitized. Figure 5's curves and uncertainty bands are conceptual, not quantitative trajectories or confidence intervals.

## Functional units, backgrounds and carbon fate

The paper proposes different units for net atmospheric CO2 removed/stored, point-source emissions avoided/stored and CO2 treated by utilization. Captured, treated, avoided, removed and retained mass remain distinct. Electricity/product services require matched reference processes and allocation. Carbon incorporated into a fuel can be emitted later; a negative comparative impact is not automatically permanent atmospheric removal.

The page 7 discussion permits cradle-to-gate comparison for chemically identical products, then says uncertain end-use may require excluding combustion. The latter wording requires exact-original checking. Cancellation of identical downstream phases in a comparative analysis differs from omitting absolute carbon fate when claiming storage or removal. Figure 6's no-discount/end-of-life statement assumes permanent storage; it does not demonstrate permanence.

Likewise, not modelling changes in a background process does not make its burdens zero. A sensitivity with and without background contributions must not be presented as a complete lifecycle result after dropping those contributions. Energy suppliers, evolving incumbents, scenario years/regions, technology mappings and inventory system models must remain consistent. Prospective databases may require licensed inventory access even when the transformation software is open source. Article CC BY rights do not grant rights to every cited inventory, simulator or model asset.

## Citation and asset work remains open

The [192-entry bibliography and ten dependencies](../evidence/comprehensive_review_inputs/B2-02_bibliography.json) preserve raw native excerpts and claim pointers. Particular questions include:

- Page 17 attributes SecMOD to Baumstark2021, whose printed entry is REMIND2.1. Figure 7 instead cites Reinert2022 for SecMOD.
- Page 17 describes Cox2018 passenger-car comparisons, while the printed 2018 title concerns air transportation.
- Page 20 cites Luo2022 for chemical-process flexibility, while its printed title concerns cotton-jeans footprints.
- Table 3's Volkart2018 CCS example and the Thonemann/Pizzol2019 prospective formic-acid method require exact-source checking. Related listed sources are not automatic corrections.
- The quoted LCA definition, PyPSA publication/release identity, MESSAGE badge URL, CRETE/CREATE status and REMIND/IMAGE sector-coverage assertion also require the exact originals/versions.

The retained CEMCAP D4.2 report is distinct from the cited Part1/Part2 journal papers. The retained 2009 SimCCS and 2025 prospective transport articles are distinct from the cited 2020 SimCCS and 2024 transport originals. No substitute-source verification is counted.

No embedded file, internal appendix or explicit supplement/data-code notice was identified in the retained PDF. That does not establish absence of public supplements, errata or code. Native cases, software releases, scenario arrays, foreground inventories, interface mappings, licenses and supplements remain open. External retrieval remains paused under the user's request to wait for a Chrome connection.

## Paper 1 and validation

Paper 1 uses this review for accounting and modelling discipline: distinguish carbon services, align foreground/background time and geography, retain future comparator changes and verify model mappings. None of its heterogeneous cost/impact ranges, ordinal TRLs, announced capacities or permanent-storage assumptions enters accepted operating/GHG inputs. Existing numerical results and original PDFs remain unchanged.

Four new tests check repeated percentage reductions independently of the power-law expression, baseline/unit invariance, the expanded-form counterexample and invalid/ambiguous inputs. All 165 repository tests passed after register regeneration. These checks do not validate missing author models. Continue B2-03 while citation, supplement and native-model verification remains active across all 92 unique papers.
