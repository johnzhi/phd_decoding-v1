# B2-16 global CCS layout audit

Yi-Ming Wei and colleagues propose a global clustered CCS layout in *Nature Climate Change* 11 (2021), 112–118, DOI [10.1038/s41558-020-00960-0](https://doi.org/10.1038/s41558-020-00960-0). The [retained PDF](../papers/B2-16.pdf), SHA-256 `ba2c448e350c1ccfd5f9acdf9f6458d41706e25736ea1b0fee00ee47a07428f0`, includes seven printed article pages and four online-methods/disclosure pages. Its exclusive Springer licence is preserved; it is not assumed to be CC BY.

All **eleven physical pages** were text-read and visually inspected. Enlargements cover the five figures, all eighteen panels, map and country-bar legends, captions and small formulae. All **33 numbered equations** and **51 bibliography entries** were inspected. The [item record](comprehensive_review/B2-16.md) contains twelve section records, 21 variable groups, 62 claims and fifteen open issues. No separately numbered main table was identified.

**The paper remains incomplete under the comprehensive standard.** Reading its main PDF does not verify all originals, supplements or native models. Two scoped original-passage checks were added; 49 other direct originals, fourteen dependencies or audit requirements, explicit supplementary material and native data/code remain unverified.

## Reported case and its boundary

The study constructs 4,220 emission clusters and 794 storage basins in 87 countries/regions. Its C3IAM/GCOP matching selects 3,093 clusters and 432 sinks in 85 regions for a cumulative **92 Gt** case over 2020–2050: **58.61 Gt saline storage and 33.39 Gt EOR**. These add to 92 Gt, with shares about 63.71% and 36.29%. The selected sink counts, 277 saline and 155 EOR, add to 432.

The 92 Gt target comes from a cited IEA 94 Gt contribution with 2 Gt omitted for data availability. Printed sector targets are 52 Gt power and 40 Gt nonpower. The exact climate-scenario original remains unverified; captured, transported, injected, avoided and permanently retained CO₂ must not be treated as interchangeable.

The storage inventory is **volumetric cumulative resource**: 168 Gt EOR plus 1,914 Gt saline, totalling 2,082 Gt. It does not provide a measured or calibrated pressure-constrained annual injection envelope. Oil storage uses the printed original-oil-in-place product with a standard CO₂ density of 1.977 kg/m³ and efficiency 0.6. The oil-volume conditions and replacement convention require clarification; the density is not silently replaced with a reservoir value. Saline resource multiplies basin area, effective area fraction, thickness, porosity, density 710 kg/m³ and efficiency 0.05. These quantities and their native scenario values are not sufficient to infer pressure feasibility or containment.

Figure 2 explicitly considers onshore injection while including offshore basin resource extent. Transnational resource is allocated in proportion to basin area. This differs from B2-15's majority-country whole-basin assignment, so national comparisons are affected by geography and allocation as well as physical modelling.

## Source construction and the threshold conflict

CARMA's 66,273 power plants from 2009 provide spatial emission shares scaled to 2017 IEA totals. Another 20,491 industrial points cover the USA, China and Europe. Elsewhere, 10 km EDGAR industrial emissions are downscaled to 1 km using land-cover exclusions. A 1 km output grid is therefore not evidence of 1 km measurement accuracy. The study assumes cluster locations remain largely unchanged to 2050.

Both descriptions use high-emission cells exceeding 10,000 t/y, but their cluster threshold differs:

| Location | Printed cluster threshold | Converted value |
| --- | --- | ---: |
| Main text, physical p2 | Total annual emissions exceeding 40,000 t | 0.04 Mt/y |
| Methods, physical p8 | Contiguous-area emissions exceeding 0.4 Mt | 400,000 t/y |

This is a **factor of ten**. The audit preserves both statements and does not choose which threshold generated the native 4,220 clusters.

The paper says 47% of clusters mix power and industrial emissions. Equation 4 weights capture prices by gross sector emissions, whereas Equations 7–10 divide source indices into power and nonpower sets and constrain total cluster emissions. The native allocation of mixed clusters, separate capture efficiencies and sector flows is not printed sufficiently to reconstruct it. A disclosed 70/30 synthetic cluster with 90%/60% capture efficiencies illustrates why applying one sector's efficiency to the entire cluster changes the bound; it does not establish a bug in the authors' code.

Figure 1's nine regional masses sum to 693.6 Gt versus the reported 693.8 Gt globally, and its shares sum to 99.9%; both differences are rounding-compatible. Whole-percent power pies likewise allow the difference between their weighted sum and 518.8 Gt. However, the eight named inventory regions imply about **81.565%** of emissions, rather than the approximately **84%** stated on p3. Their nearest-display upper bound remains below 83.5%. The case or denominator requires reconciliation; cluster counts and emission mass are not swapped to repair it.

## Matching, distances and financial accounting

The printed global matching model is a **cumulative linear program with domestic direct arcs**. Cross-border transport is expressly prohibited. Sink constraints are cumulative stock bounds; source constraints multiply emissions by capture efficiency. Despite surrounding prose referring to pipeline capacity, the latter do not independently specify arc or hydraulic capacity. The global matching LP contains no annual pressure history, route construction, shared-trunk opening or vessel dispatch decisions.

Power and nonpower targets are inequalities, not exact equalities. Negative EOR marginal costs can make additional capture reduce financial cost. Six explicitly synthetic cases compare the printed lower bounds with an analyst exact-target alternative at oil prices of 0, 55 and 95 USD/bbl. Their total lower-bound flows are 7, 9 and 10 Mt, while the exact-target comparison remains 7 Mt. These examples diagnose a mathematical possibility. They **do not establish that the native global case exceeds 92 Gt**.

The source reports 80% of matches within 300 km and no pair beyond 1,000 km. Figure 3's caption describes proportions of matches, whereas some national statements describe CO₂ mass. Those denominators require native arrays. Its world-map scale literally reads 0/15/30/60 km; no missing multiplier or route geometry is invented. Figure 4's country circles aggregate matching, rather than showing constructed pipelines. The eight selected-country masses sum to 69.8 Gt, about 75.87% of the target, consistent with the reported 76%. This is a different set of eight countries from Figure 1's inventory comparison.

Reported gross investment is **USD 8.20 trillion**: 4.45 capture, 3.25 transport and 0.50 storage. Subtracting **2.44 trillion EOR benefit** gives **5.76 trillion net cost**, in reported constant 2019 prices. The quoted 62.65 USD/t multiplied by 92 Gt gives 5.7638 trillion, compatible with rounded aggregates.

The claim that capture accounts for more than 77% uses the **net-cost denominator**: 4.45/5.76 ≈77.26%. Its share of gross investment is 4.45/8.20 ≈54.27%. This denominator distinction explains the statement without declaring an arithmetic error.

The EOR revenue basis remains unresolved. Equation 6 prints `Rev = oil price / dpr`, with `dpr = 4` but no unit. For Rev to be USD/t, dpr needs t/bbl units. **Under that explicit conditional interpretation**, 55/4 =13.75 USD/t and 33.39 Gt implies **0.4591125 trillion USD**, rather than the reported 2.44 trillion benefit. Native displacement units, time basis, revenue definition and case arrays are needed. The implied alternative displacement or price calculated by the script is a diagnostic, not a corrected input. The 55→95 sensitivity is reoptimized and is not reproduced by holding EOR volume fixed.

The 0.12% of cumulative GDP normalizes financial cost by an exogenous SSP2 projection; it is not an annual budget or proof of upfront financing. Similarly, four countries' financial surpluses normalized by GDP do not demonstrate causal GDP growth. Negative financial cost is not negative GHG emissions.

Two potential false errors are expressly avoided. The adjacent 2.01/2.02 trillion maximum-cost display intervals touch, so that difference is not declared a definite inconsistency. A mean oil breakeven of 134.58 USD/bbl can coexist with 75% of countries becoming profitable around/above 100 if the distribution is skewed. Native populations and weights are needed. The quoted 21.54% average EOR utilization also need not equal the global flow/stock ratio of 19.875% if it is an unweighted country mean; its basis remains open.

## Capture-cost equations and limited reconstruction

The power module optimizes a capacity path for four capture technologies. Its annual summation includes 2020 through 2050, or 31 calendar entries; that is distinguished from thirty elapsed years without automatically labelling it a duration error. The initial capacities, growth limits, learning onsets and 100 GW maturity branches require supplementary values and code. A negative-exponent power-law cost is singular at zero capacity unless initialization or a piecewise rule is supplied.

Equation 23 divides the LCOE difference by the difference in emission rates at equal electricity output. That gives **cost per avoided tonne**, which is not automatically the captured-tonne cost applied to network flow X. With explicit synthetic values, a 40 USD/MWh difference divided by 0.7 t avoided/MWh gives 57.1429 USD/t avoided; dividing by a separate 0.8 t captured/MWh gives 50 USD/t captured. No native plant output or capture inventory is inferred.

The printed Equation 24 capacity-factor multiplier is **CF₀/CFd**. It was checked enlarged and independently reconstructed from annualized capital, O&M, fuel and electricity output. The identity agrees under disclosed analyst assumptions. This is a component check, not a reproduced optimal power deployment or complete source-specific capture inventory.

The industrial deployment equation is the literal rising exponential-of-squared-distance segment:

\[
 tp(t)=tp_{max}\exp\left[-\left(U-U\frac{t-SD}{2050-SD}\right)^2\right].
\]

At the starting year it is generally nonzero, `tp_max exp(−U²)`; at 2050 it reaches `tp_max`. Twenty-one synthetic rows inspect its domain and endpoints. It is not substituted with a standard logistic curve.

Equation 29 reduces a cost-learning multiplier by 25% per five-year step when `tp > CR_min`, while the prose says costs begin declining below the threshold and also refers to a deployment-rate reduction. Initial and otherwise branches remain missing. CEPCI base normalization, annual captured mass, its connection to deployment and the mapping of BECCS into the original industrial inventory also remain unresolved. No sign, threshold or curve is silently repaired.

## Originals, supplements and use in Paper 1

Two exact retained originals were text-read and visually inspected at physical pp1–2:

- **R10 → B3-44, SimCCS (2009):** establishes earlier simultaneous source, capture, reservoir and capacitated-route optimization with shared trunklines. It qualifies a transport-only characterization; it does not validate this global case.
- **R16 → B3-13, InfraCCS (2012):** establishes a European model with five interdependent deployment steps, clustering, route preselection and coordinated cross-border networks. Its capture scenario is external. These selected passages do not complete the fourteen-page original or reproduce its model.

Hashes, DOIs, pages, support and limitations are retained in the [citation record](../evidence/comprehensive_review_inputs/B2-16_citation_checks.json). Bibliography line geometry is in the [native reference record](../evidence/comprehensive_review_inputs/B2-16_bibliography.json).

The article explicitly references SI Tables 1–6, Figures 1–3 and Note 1. Page 10 offers data and code upon reasonable request, and p11 links supplementary information at the DOI. None of those ten named components or the native implementation is verified locally; local absence is not online absence. External retrieval remains paused pending the requested Chrome connection. No author was contacted.

The [input record](../evidence/comprehensive_review_inputs/B2-16.json), [67 checks](../outputs/comprehensive_review/B2-16_checks.csv), [synthetic LP cases](../outputs/comprehensive_review/B2-16_analyst_LP.csv), [deployment rows](../outputs/comprehensive_review/B2-16_analyst_deployment.csv) and [reproduction summary](../outputs/comprehensive_review/B2-16_reproduction_summary.json) preserve the scientific boundaries. Eight focused tests check algebra, units, domains and optimization feasibility. Native GIS, global LP results, power/nonpower deployment, uncertainty and breakeven arrays, pressure service and complete LCA remain unreproduced.

Paper 1 should acknowledge global clustered planning and the earlier integrated/temporal methods. **This study does not close either the public pressure-constrained reservoir dataset or complete capture-to-ship heat/electricity inventory requirement.** No accepted operating/GHG input or current numerical result changes. Native files and the prior combined 1.5 MPa HOLD are preserved; the comprehensive goal remains active.

Regenerate only these scoped checks with:

```bash
python paper1/scripts/audit_global_layout.py
python -m unittest discover -s paper1/tests -p test_global_layout.py
```
