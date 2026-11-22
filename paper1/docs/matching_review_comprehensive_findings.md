# B2-17 critical source–sink review audit

Keyao Lin, Ning Wei, Dalin Jiang and Yao Zhang review CCUS source–sink matching in *Renewable and Sustainable Energy Reviews* 226 (2026), 116313, DOI [10.1016/j.rser.2025.116313](https://doi.org/10.1016/j.rser.2025.116313). The article was online on 20 September 2025; the 2025 DOI/online date and 2026 volume are compatible. The [retained PDF](../papers/B2-17.pdf) is CC BY 4.0, SHA-256 `ddd464b25455703f2ef321ca6919d777e60dd1e4016020e93ebcb1df6193d2ea`. B3-46 is its preserved duplicate and is not counted again.

All **27 physical pages** were text-read and visually inspected. The [item record](comprehensive_review/B2-17.md) covers eighteen figures, seven numbered tables with continuations, the abbreviation table, twelve Table 3 capacity equations, two inline climate/state relations, 109 claims and eighteen open issues. Enlargements cover equations, map legends and small table entries. Some overlapping field labels in Figure 16 remain unresolved; exact routes or operating arrays were not digitized from maps.

**Overall status remains incomplete.** All 251 bibliography entries were read and their native line geometry preserved. Two exact selected originals were checked; 249 other direct edges and fourteen dependencies or audit requirements remain unverified. The review's literature selection and cited author models have not been independently reproduced.

## What this review establishes

The paper organizes sources, sinks and matching across global, national, regional and industrial scales. It identifies four challenge groups: technology/economics/policy coordination; data accuracy and scale; transport and cluster collaboration; and algorithm/physics/time integration.

Its screening discussion includes five assessment scales, twenty secondary site criteria and pressure-aware CO2BLOCK precedent. Its transport/method discussion includes stochastic shipping, multiperiod planning, GIS, MILP/MINLP, fuzzy, graph, genetic and pinch approaches. Paper 1 must acknowledge this existing work and avoid claiming that all prior planning is static or disconnected from physical constraints.

The paper calls its synthesis systematic, but the retained PDF does not provide sufficient database queries, search dates, inclusion/exclusion decisions, screening records or quality/extraction matrices to reproduce literature selection. Reading its bibliography cannot establish that its claims about what most studies omit are representative or exhaustive. Its proposed ML, quantum, digital-twin and governance directions are **future recommendations**, rather than demonstrated implementations or performance benchmarks.

## Dates, resource labels and climate quantities

The review reports 36.3 Gt of 2024 fossil/industrial emissions with 0.9% growth in one cited series, and an IEA-labelled 37.8 Gt with 0.8% growth elsewhere. Different dataset boundaries must be reconciled before comparison; these are not automatically an arithmetic contradiction. The five quoted IEA region totals sum to 23.5 Gt, about 62.17% of 37.8, consistent with the stated share above 62.1%.

Figure 1 combines historical quantities with future decarbonization curves and “Scope 4” avoided equivalents. These are not observations of future emissions or an independently verified capture supply. Its whole-percent country shares sum to 101% and avoided-equivalent shares to 99%; rounding can explain those sums.

Figure 3's caption dates storage **potential to 2021** and project status to **2022**, while the prose calls the resource figures verified storage data in 2023. Its blue project category includes operation **and construction**, alongside development and suspension categories. The 135 labelled facilities therefore cannot be adopted as a current operating count, and the resource figures are not actual injected mass.

The enlarged country resource labels repeat **403.971 Gt and 3.117% for both Canada and the UK**. All sixteen country percentages sum to more than 100% if interpreted as a common nonoverlapping global partition, beyond their display precision. Native allocation, possible overlap and the exact original R27 must be checked. Both labels are preserved; neither country is deleted or assigned a guessed replacement.

Table 1 uses historical AR4-based GWP values, including CH₄ GWP100 =25. All six gas rows, lifetimes and 20/100/500-year values are retained in the [source transcription](../outputs/comprehensive_review/B2-17_source_GWP.csv). They do not become accepted current lifecycle factors. Mass-based GWP, per-molecule forcing, atmospheric lifetime, anthropogenic emission shares and geological retained mass are different quantities. The simplified 200-year CO₂ lifetime description supplies no retention factor for Paper 1.

## Resource arithmetic and physical limits

The three quoted Chinese saline resources—Songliao 694.5 Gt, Tarim 552.8 Gt and Bohai Bay 490.6 Gt—sum to **1,737.9 Gt**. Against the stated Chinese saline total of 2.42 trillion tonnes, that is **71.814%**, rather than the reported 50%. The original report's case and denominator remain unresolved. No corrected percentage is accepted.

Table 4 uses **10¹⁰ tonnes** for both theoretical resources and estimated cumulative emissions to 2060:

| Region | Resource interval | Interval midpoint | Figure 10 label | Cumulative emissions |
| --- | ---: | ---: | ---: | ---: |
| North America | 230–2,153 | 1,191.5 | 1,192 | 25 |
| Europe | 50 | 50 | 50 | 17 |
| Asia excluding China | 49–55 | 52 | 52 | 30 |
| China | 121–413 | 267 | 267 | 40 |
| Australia | 22–41 | 31.5 | 32 | 1.6 |

The graphic's “median interval estimates” match rounded **interval midpoints**. A probability median cannot be established without a distribution. A disclosed three-point example on China's same endpoints can have its median at either endpoint under different weights; it is not an inferred source uncertainty distribution.

Resource/emission ratios are cumulative comparisons. They do not establish annual injectivity, project availability, containment or permitting. Alternative North American/Canadian figures elsewhere use different cited assessments and possible unit/population bases; they are not silently combined into one harmonized resource.

Table 2's geothermal row includes adequate surface temperature, while its pressure-gradient row can read as a depth-based guarantee of supercritical conditions. Pressure and temperature must be considered **jointly**. Six synthetic hydrostatic/geothermal screens include a depth of **801 m**, explicitly above 800 m. With a 10°C surface temperature and 25°C/km gradient, the temperature is 30.025°C despite absolute pressure above 7.8 MPa; the pure-CO₂ critical temperature is not exceeded. A 15°C surface case changes the result at the same pressure. These illustrate why depth/pressure alone is insufficient; they do not invalidate a framework that applies adequate temperature too, or validate an actual mixture, well or injection limit. The source's joint >31.1°C and >7.8 MPa pair is a conservative sufficient pure-fluid condition, not a false critical-point claim.

## Every capacity relation retains its conventions

The twelve unnumbered equations in Table 3 cover material-balance oil and coal, three saline trapping expressions, three US DOE volumetric expressions, an areal expression, two further dissolution expressions and a solubility expression. No new native optimizer or field dataset is supplied by this review.

The [equation record](comprehensive_review/B2-17.md#equations-and-derivations) preserves all twelve literally and identifies:

- percentage-to-fraction conversion, effective geometry and storage-efficiency definitions;
- water-injection/production volumes at consistent reference conditions;
- standard versus reservoir/solution gas densities and the residual-density symbol;
- the coal `nc` name versus its kg/m³ unit and `Gc` m³/kg unit;
- the formation-volume ratio B alongside pore-volume geometry;
- missing oil/water solubility units and the Li expression's unknown coefficient R.

Magnification confirms that **Shen's CO₂ density multiplies the entire bracket**, including the water and oil dissolution terms. A text extraction that loses that bracket must not become a missing-density finding. The synthetic component retains the literal bracket with disclosed dimensionless toy coefficients; native solubility conventions remain unverified.

The Li expression states molar mass in g/mol but does not give R's unit. Under an explicitly declared mol/kg-water convention, a g-to-kg conversion is needed. That diagnostic does **not** establish a thousandfold source error or justify a corrected mass when the native convention is unknown.

Separate trapping estimates on the same pore volume cannot automatically be summed as independent resources. The analyst overlap example demonstrates this accounting point without claiming the review actually performs an invalid sum. None of these volumetric or trapping expressions supplies pressure-constrained annual service or a measured permanently retained fraction.

The EGR/ECBM paragraph also reverses its former/latter descriptions relative to the preceding EGR-then-ECBM order: coal adsorption/Qinshui describes the coalbed pathway, while depleted-gas pressure/K12-B describes gas recovery. Exact original mechanisms and outcomes remain open; the swapped descriptions are not transferred to Paper 1.

## Two exact original checks

**R172 → B2-08, Bjerketvedt et al. (2020), physical pp1,7,8.** The original supports a two-stage stochastic investment/operation model for 0.4 Mt/y over 715 km from Brevik. Its cases differ:

| Original case | Source buffer | Ship capacity | Buffer/ship |
| --- | ---: | ---: | ---: |
| Lowest average cost, 99% service, 33.8 €/t | 5,120 t | 5,000 t | 102.4% |
| 100% service | 5,890 t | 5,000 t | 117.8% |

The first buffer is about 118% of an **average-cycle** quantity, which is a different denominator. The original abstract itself combines the 33.8 €/t result with 18%-above-ship wording; the review inherits that ambiguity. It is not treated as an invented review error. The roughly 5–5.6% cost comparison concerns **neglecting weather uncertainty when designing capacities**, rather than eliminating buffers. Two stochastic decision stages must also be distinguished from the physical buffers at the two terminals. Native weather, process, optimization and full utility/LCA reproduction remain open.

**R200 → B2-16, Wei et al. (2021), physical pp1,4,8.** The original supports 3,093 selected clusters, 432 sinks, 85 regions, the cumulative 92 Gt case and its financial cost/GDP metric. Its input database has 4,220 clusters and 794 basins. Crucially, Methods p8 explicitly states that **cross-border CO₂ transport and matching are prohibited**. This is domestic matching at global scale; it does not demonstrate a transnational delivery network. Figure 15 reproduces resource maps and per-sink inventories, rather than actual international transport routes.

DOIs, source hashes, selected pages and qualifications are preserved in the [citation record](../evidence/comprehensive_review_inputs/B2-17_citation_checks.json). Neither selected check completes its cited original's full evidence/model chain.

Other model attributions remain open. R181 is a **2011** InfraCCS paper, not the retained 2012 Morbee publication; R180 is a **2020** SimCCS paper, not the retained 2009 version. Those older/different editions are not substituted as exact-source verification. Similarly, generic statements that MILP cannot handle vessel scheduling, dynamic information or uncertainty require formulation-specific evidence, rather than a universal conclusion about the mathematical method.

## Industry cases and the tenfold cement discrepancy

Table 7 contains fifteen study rows across pp17–18, with country, industry, research focus, findings and references. All were inspected, including continuations.

For the same described **229–627 cement plants and 20–60% reduction targets**, the body gives **79.4–269.5 billion CNY**, whereas Table 7 gives **794–2,695 billion CNY**. Both endpoints differ by a factor of ten. The exact original R238 is unverified locally. Both quotations remain on hold; neither becomes an accepted cost or a silently repaired decimal.

Other case quantities also need their native periods and boundaries. A 1,116-plant integrated case differs from a separate 1,186-source shared-network case. Only the first of the latter's four sector quantities is explicitly annual in the review prose. Water totals, capture flows, multi-decade reductions, stock coverage, currency and EOR revenue cannot be harmonized by assumption. Multiplying 170 Mt/y by 237 years gives a conditional 40.29 Gt, not a demonstrated 237-year pressure/containment history. The Dutch 32-million-ton quote likewise remains literal until its original is read.

Geographic maps, MCDM rankings and modeled project opportunities do not establish operating sites or safe annual limits. The qualitative transport-mode GHG ranking is not accepted without matched throughput, distance, state, energy and lifecycle boundaries. Economic EOR/uranium/gas/water benefits are not automatically net climate credits.

## Reproduction, missing assets and Paper 1

The [input record](../evidence/comprehensive_review_inputs/B2-17.json) separates source transcriptions from analyst assumptions. [audit_matching_review.py](../scripts/audit_matching_review.py) produces **44 limited checks**, five [resource interval rows](../outputs/comprehensive_review/B2-17_resource_intervals.csv), six [synthetic state screens](../outputs/comprehensive_review/B2-17_analyst_phase_screen.csv), six historical GWP rows and sixteen resource-label rows. Eight focused tests check mass/volume scaling, water adjustments, solubility/density units, the full Shen bracket, molar conversion, state requirements, interval medians and invalid domains.

These are accounting and component diagnostics. They do not reproduce literature selection, all cited reservoir/optimization/process/ML models, actual annual field service, uncertainty calibration or a complete LCA. The [reproduction summary](../outputs/comprehensive_review/B2-17_reproduction_summary.json) keeps those states explicit.

The main PDF offers data on request and contains no embedded files or explicit publisher SI/code availability section. Online assets remain unverified; no online absence is inferred. External retrieval is still paused pending the requested Chrome connection, and no author was contacted.

Reference **R185** gives a specific dataset lead: Fan et al., *Scientific Data* 12 (2025), 640, [10.1038/s41597-025-04875-3](https://doi.org/10.1038/s41597-025-04875-3). The bibliography names geological storage potential and injection-rate capacity based on a fine grid. This is **unverified bibliographic provenance**, not an acquired public pressure-constrained field dataset or evidence that its inputs meet Paper 1's requirements.

Paper 1 should use this review to frame established methods and explicit data/physics/uncertainty gaps, with exact-source qualifications. It supplies neither complete matched capture-to-ship utilities nor calibrated annual reservoir service. **No accepted operating/GHG input or current numerical result changes.** Native files, the prior combined 1.5 MPa HOLD and the incomplete comprehensive goal are preserved.

```bash
python paper1/scripts/audit_matching_review.py
python -m unittest discover -s paper1/tests -p test_matching_review.py
```
