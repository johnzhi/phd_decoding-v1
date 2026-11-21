# Distance, injectivity and capacity: comprehensive reading findings

All eleven physical pages of Wang et al. (2016), B2-01, have been read and visually inspected, including eight figures, six tables, four numbered equations, nomenclature, the complete literature review, discussion and conclusion. Both decision trees were enlarged and every branch operator was checked. The [item record](comprehensive_review/B2-01.md) preserves page-level scope and open issues. DOI: `10.1016/j.ijggc.2016.05.006`; SHA-256: `1d220eda63796508f2197e73ac39e71dc4921939204d9477b274a1d2364177cc`. Native files and rights are unchanged.

The paper remains **incomplete under the comprehensive-audit standard**. One of its 45 direct citation edges has scoped primary support; the other 44 and six additional dependencies remain unverified. The [49 limited diagnostics](../outputs/comprehensive_review/B2-01_checks.csv) and [402 published-tree inference rows](../outputs/comprehensive_review/B2-01_published_tree_grid.csv) reconstruct available components. The [reconciliation](../outputs/comprehensive_review/B2-01_reconciliation.json) leaves native ICCSEM optimization, tree training/accuracy, physical reservoir dynamics and retention unreproduced.

## Model and economic boundary

The paper considers a constant source supplying two generic onshore sinks over 25 years. Scenario 1 has two infinite-capacity sinks. Scenario 2 has one finite and one infinite sink and compares LARGE, BOTH and SHIFT/SWITCH options. Several hybrid schedules and sink-to-sink pipeline extensions are excluded. Optimality within those options is not a proof that all temporal or shared-network alternatives are dominated.

Costs use 2012 Australian dollars and a 7% real discount rate. The pipeline assumptions include X65 steel, 8 MPa inlet/outlet conditions, 25°C and 15 MPa maximum working pressure. That pipeline pressure limit is not a reservoir BHP or fracture limit. The model excludes capture economics, reservoir heterogeneity and well interference. Its per-well injectivity is an assumed constant, with the well-capital component `flow / injectivity × cost per well`. This is useful economic coupling, but it does not supply pressure-constrained annual storage service.

Equation 1 divides discounted transport, booster, well and decommissioning costs by discounted transported/injected CO₂ minus transport/booster-generated CO₂. This is a levelized accounting boundary with missing native cost/emissions/timing functions. Discounting the denominator does not reduce physical injected mass. Capture burdens, upstream energy, leakage and long-term retained carbon are not fully inventoried.

## Units, ranges and graphic questions

The nomenclature defines sink capacity in Gt and source flow in Mt/year, while writing `R = C1/(25F)`. Explicit conversion gives `R = 1000 C1[Gt]/(25 F[Mt/year])`. The example `C1 = 0.25 Gt`, `F = 20 Mt/year` then gives the reported `R = 0.5`; the unconverted numerical quotient would not. Full-flow filling time is `25R` years, but that is not necessarily the optimized switching date or the BOTH allocation. The cited “35 Mtpa” storage-capacity wording also requires its underlying source rather than a guessed unit correction.

The stated injectivity range is 0.3–1.5 Mt/year/well, whose smallest possible ratio is 0.2. Table 1 includes ratios 1/6 and 0.1, while Figure 5 uses 0.125 Mt/year/well for one sink. These can be illustrative or differently mapped cases, but the complete absolute training vectors are unavailable. Values are preserved rather than clamped to the stated range or substituted into a regional physical model.

Figure 4's storage-cost labels also need clarification. At fixed source flow, second-sink injectivity and well cost, the stated linear well-cost component scales inversely with the injectivity ratio. Anchoring the first-sink labels to 3.4 AUD/t at ratio 0.1 would give approximately 1.7, 1.13 and 0.85 AUD/t at ratios 0.2, 0.3 and 0.4 under common timing and denominator treatment; the graphic instead labels 2.7, 2.1 and 1.4. The native decomposition could resolve the discrepancy, but it is not supplied. Neither the bars nor the reported crossover between 0.2 and 0.3 is silently corrected.

The global map and perspective cost surfaces were inspected as graphics. Unlabeled coordinates, exact mesh costs and interpolation results are not recoverable as native arrays. Their scale and unit bases—A-cent/t-km, AUD/t, AUD million and AUD billion—remain distinct.

## Published inference reproduced; training and accuracy remain open

Figures 6 and 8 provide enough information to reconstruct their categorical inference. The implementation retains every `>=` and `<` boundary and records each node, threshold and leaf. The 27 distinct Scenario 1 feature combinations and 375 Scenario 2 combinations produce 402 traceable outputs. These rows have **no native optimal labels** and are not a new accuracy test.

Both published examples are reproduced: SINK2 for Case 1 and BOTH for Case 2. In Case 1, however, the prose bullet calls Sink 1 farther away and more injectable, whereas the table ratios and subsequent traversal make Sink 2 farther away and more injectable. The source identities remain literal rather than silently swapped.

Table 2 and one prose description also disagree. The four-input version including flow has seven levels and 95.5% accuracy; the published three-level tree uses three inputs—distance ratio, injectivity ratio and well cost—and reports 95%. The finite-sink tree uses four features and has a six-decision maximum path. All branches can be executed without reproducing how those branches were learned.

Reported accuracy of 92.2–96.9% measures agreement with design labels. The paper does not supply the full labels, an independently documented training/test split, pruning details, confusion matrices or the economic regret of errors. These percentages do not establish safe injection rates, probability of optimal operation, reservoir reliability or retained carbon. Original ICCSEM and training workflows remain open.

The reported time ratios are about 427–515 across the two examples, consistent with “order 500” speedup. Those are calculations on source timings, not current hardware benchmarks or a measurement including generation of training labels.

## Geometry, prices and network transfer

The source assumes the sink-to-sink distance exceeds both source-to-sink distances. Its two arccos expressions are not both real for several listed distance ratios. The law of cosines provides the valid conditional test `cos(theta) < min[L1/(2L2), L2/(2L1)]`. Independent coordinate checks verify that distance condition. It does not prove that the proposed pairwise screening preserves every network optimum.

The claim that common steel or construction-cost changes effectively cancel in ratio-based screening also needs a boundary qualification. A common multiplier on pipeline costs does not multiply well costs. A synthetic example uses well-capital costs of 100/25 MAUD and pipeline costs of 100/150 MAUD: totals 200/175 favor the second sink, while doubling both pipeline costs gives 300/325 and favors the first. This is a mathematical counterexample to general cancellation, not a reconstruction or alleged software error in an author ICCSEM case.

The paper's average recompression share of 9% implies a 2.7% average transport-cost effect for a 30% component change under fixed other costs. Its stated 4.5% maximum can correspond to a different share; the average and maximum are not treated as a contradiction.

## Scoped original-source check and Paper 1

The exact retained Morbee et al. (2012) original, B3-13, matches DOI `10.1016/j.ijggc.2011.11.011`. Text and rendered physical pages 1–3 confirm spatial pipeline routing/preselection, staged MILP infrastructure planning and exogenous capture input. This supports the cited network-method context. It does not validate Wang's classifier, pairwise pruning or the specific West Poland example. B3-13's remaining pages, sources and native model are still pending under the comprehensive standard. [Citation provenance and limits](../evidence/comprehensive_review_inputs/B2-01_citation_check.json) record both PDF hashes and the exact inspected scope.

The [45-entry bibliography/dependency register](../evidence/comprehensive_review_inputs/B2-01_bibliography.json) preserves printed identity problems, including the Allinson 2006 DOI duplicated with Neal 2013 and an incomplete Stewart DOI. A different Middleton/SimCCS publication is not substituted for the cited original. No internal appendix, embedded file or explicit supplement notice was identified; public availability, native code, errata and rights remain unverified during the requested Chrome wait. No absence claim follows.

Paper 1 uses the study for transport–storage economic coupling and the distinction between screening, optimization and physical service. The available inference component is reproduced; its reported accuracy, cost model and pressure feasibility are not. No accepted operating, retention or GHG number changes. Continue with B2-02 while the original-source and native-model work remains open.

Validation: six new component/domain/provenance tests passed, followed by all 161 repository tests after register regeneration. Tests cover all eighteen published leaves, equality operators, independent coordinate/entropy checks, unit conversion and the conditional price example. Source and cited-original hashes are checked separately; these tests do not validate unavailable optimization labels or field physics.
