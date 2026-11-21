# B2-03 stochastic deployment: findings and limits

Chinmay M. Aras and M.M. Faruque Hasan (2025), DOI `10.1016/j.compchemeng.2025.109300`. All 11 physical pages of the [retained original](../papers/B2-03.pdf) were read and visually inspected: eight figures, 35 numbered equations, two algorithms, both unnumbered nomenclature/symbol objects and all 31 bibliography entries. The [item register](comprehensive_review/B2-03.md) and [manual record](../evidence/comprehensive_review/B2-03.json) retain the page-level evidence and 25 claim records.

**The paper remains incomplete under the comprehensive-audit standard.** Two direct citation edges have scoped primary support; 29 other originals and ten native data/model dependencies remain unverified. The explicitly referenced supplement and data/code are not matched in retained local assets. No native Illinois/Gurobi/SAA/CDF, physical reservoir or lifecycle model is independently reproduced.

## What is optimized

The case has 820 sources emitting an estimated 458,673 kt/year, three sequestration sites and five utilization sites, including two Appalachian sites. Commissioning is planned for 2026–2050 using a five-year forecast window. The base allocation is 4.8 billion dollars per period, the discount rate is 3% and the social cost is 42 dollars/ton. Ten batches of 25 scenarios generate candidate schedules; 5,000 scenarios evaluate a selected design. The reported solver setup is Python3.9.6/Gurobi11.0.3 with a 1% gap. Native data, seeds, cost arrays, output logs and runtime measurements are absent here.

A selected source is nominally sized to its full emissions. Its flow cohort begins at commissioning and continues at a constant annual rate for plant lifetime `L`. Individual source–sink pipelines exclude shared trunklines. Costs and benefits are lifetime NPVs charged against the allocation for the commissioning period. This is not an independently reconstructed annual cash ledger. Plant lifetime is defined but no numeric `L` is identified in the main PDF; the 25-year planning horizon is not silently substituted for it. Whole-life commitments can extend beyond 2050.

The objective monetizes avoided social damage and EOR revenue, less infrastructure/storage costs. It differs from maximizing capture mass alone. EOR revenues and direct capture do not account for all additional oil, capture, transport, storage and energy-supply lifecycle emissions. No pressure/injectivity model establishes annual deliverability or permanent retained mass.

## Printed formulations need reconciliation

Equations 7 and 13 subtract `(CI−CO)mu`, making operating cost a positive objective contribution. Equation 1, the rolling formulations and the explanation subtract `(CI+CO)mu`. A disclosed arbitrary-unit one-project example gives −10 with plus costs and +30 with the literal stochastic sign, changing the optional-build choice. This tests the printed algebra; it does not establish what the unavailable author code does.

Pipeline cost terms leave sink index `k` free without summing over it. The scalar objective/budget needs an explicit aggregation rule. The pipeline coefficient is described as NPV of a pipeline but multiplies capacity, so its units also need the supplement. Equation 25 changes social-cost notation to `CC^Soc`; the rolling endpoint `Gamma` is used as a set; some domains and old-flow carryover in Equation 26 are unclear. The explanatory prose also sums the uncaptured-emission penalty over sinks, while the displayed objective has a single penalty term. These are preserved rather than silently repaired into a complete executable model.

Storage constraints use `sum(y) <= St/L`, a lifetime stock reservation when units agree. The symbols list instead calls scenario `St` a yearly amount. A stock, a stock divided by assumed lifetime and pressure-constrained annual injection service are different concepts. Source and native supplement definitions must settle this before quantitative transfer.

## Rolling algorithms and recourse

Both algorithms print `arg min` for maximization models. They also remove newly built sources from `I_A` before deducting `L*sum(y)` over `I_A`. Under the intended nonnegative source balance, newly built sources then disappear from that storage sum.

A literal bookkeeping example starts with 25 arbitrary stock units and two cohorts of 2 units/year lasting 10 years. With the printed set-update order, both cohorts are admitted while the available-stock variable stays at 25; actual commitments total 40. A comparison that deducts the new commitment admits one cohort and leaves five stock units. This exposes a problem with the literal order, not an observed defect in native code or a corrected Illinois run. The source's general no-storage-violation assertion needs actual reserve traces and implementation evidence.

Deployment variables `mu` and `h` have no scenario index. Scenario recourse changes flows and undesired uncaptured mass. Additional first-stage links selected in anticipation of uncertainty are different from building a pipe conditionally after a storage realization is observed. The narrative of extra construction as recourse requires clarification of the information structure. Persistence of scenario identities between windows, reservations based on flows, and later fixed-design LP reoptimization also need native correspondence.

## Statistical bounds are not established by feasibility

The source acknowledges that rolling-horizon schedules may be globally suboptimal. Equation 31 nevertheless asserts that any feasible rolling candidate's sampled objective dominates the true-optimal policy's sampled objective. Feasibility alone cannot justify that inequality. A global SAA optimizer and the appropriate common feasibility assumptions are needed for the usual expected SAA optimum argument.

A disclosed two-period, one-sink mathematical example gives reward 5 for a one-period rolling strategy and 10 for the full-horizon optimum. Independent MILP and exhaustive enumeration agree. A deterministic distribution is a special stochastic case, so a feasible rolling value can lie below the true optimum. The example is not an Illinois model reconstruction.

Equations 33 and 35 are finite sample means. Even in a one-policy example with equiprobable reward 0 or 2 and true expectation 1, a finite realization can lie on either side. An estimator, an expectation bound and a confidence bound are different. Native candidate selection, independent evaluation, variances/confidence levels, solver bounds and the reported 1% gap require explicit treatment. No actual bound values or statistical validation arrays are reproduced here. A large sample count alone does not close this issue.

## Reported outputs and graphics

The reported 4,795 versus 145.24 kt mean lifetime deviations give a 96.9710% reduction, consistent with rounded 96.97%. This statistic is not a probability of failure, annual outage, capture efficiency or a retained-carbon fraction.

The reported emissions endpoints, 458,673 and 204,723 kt/year, imply a 253,950 kt/year difference and 55.36624% reduction. Nearest-one-decimal rounding gives 55.4%, while prose and Figure 8 report 55.3%. Truncation or different underlying values could explain it; both source numbers and the question remain visible, with no repaired author output.

Figure 6a shows newly commissioned annual capture capacity, not cumulative installed capacity. It fluctuates despite an overall decline from the stated 10,596 to 9,641 kt/year endpoints. Figure 6b and Figure 8 show direct regional emission-rate trajectories. The four allocations are 2.4/3.6/4.8/6 billion dollars with reported final reductions of 27.5/41.5/55.3/64.2%. Exact annual arrays, routes, diameters, source IDs and scenario outputs cannot be recovered from the maps or plotted markers. No plot-derived native dataset or marginal lifecycle optimum is invented.

## Primary-source support, supplements and Paper 1

The [two citation checks](../evidence/comprehensive_review_inputs/B2-03_citation_checks.json) anchor citing/cited hashes and inspected original pages:

- Middleton/Bielicki2009, exact retained B3-44, pages1–2, supports California source/reservoir selection and capacitated pipeline sizing, including trunklines and partial capture. Those options differ from this study's individual links/full nominal source capture.
- Morbee2012, exact retained B3-13, pages1–2, supports staged European InfraCCS planning, automatic clustering and pipeline preselection with an exogenous capture scenario.

These are method-context checks, not validation of Aras's Illinois inputs, algebra, reserve logic, statistics or physical service. They do not complete either cited paper. The [31-entry bibliography and ten dependencies](../evidence/comprehensive_review_inputs/B2-03_bibliography.json) preserve the remaining work.

Appendix A is a publisher-supplement notice, not internal supplementary methods. The main paper points to supplementary capture-cost and distance/pipeline-cost sections, and says data are available on request. No public absence follows from the missing local asset or zero embedded files. External retrieval remains paused under the requested Chrome connection; no author message was sent.

Paper 1 uses the study for commissioning/budget, stock/rate, fixed-design recourse and heuristic/statistical-bound distinctions. The findings qualify its “optimal” schedule and environmental interpretations. No source model inputs, operating/GHG outputs, annual physical service, risk probability or retained fraction changes.

The [30 limited checks](../outputs/comprehensive_review/B2-03_checks.csv), [stock example](../outputs/comprehensive_review/B2-03_stock_counterexample.csv) and [reconciliation](../outputs/comprehensive_review/B2-03_reconciliation.json) retain the exact scope. Four new tests check cost-sign choices, reservations, independent toy MILP and statistical/arithmetic examples. All 169 repository tests passed after register regeneration. Continue B2-04 while the 92-paper audit remains active.
