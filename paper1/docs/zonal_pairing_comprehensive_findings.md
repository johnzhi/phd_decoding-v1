# B2-14 zone-scale source–sink audit

Wei, Lin, Liu, Jiang, Wang, Jiao, Dahowski and Li present a Chinese national geological/economic matching framework in *Environmental Science & Technology* 60 (2026), 19170–19184, DOI [10.1021/acs.est.5c14041](https://doi.org/10.1021/acs.est.5c14041). The [retained PDF](../papers/B2-14.pdf) is CC BY-NC-ND 4.0. SHA-256: `6b9a35f4f9a54d69147ea2e94636fecc3032b11b96cb91930aeced048850416c`.

All **15 main-PDF pages** were read as text and visually inspected, with eight magnifications. The [item record](comprehensive_review/B2-14.md) covers 28 section records, ten numbered figures plus the graphical abstract, three tables, 62 claim records and sixteen open issues. The main PDF contains **no formal numbered equations**: algorithms and mathematical realizations are deferred to the explicit SM1 supplement. Seven equation/diagnostic records describe that absence and independent checks, rather than reconstructed native formulae.

**Overall status is incomplete.** All 63 printed bibliography entries were inspected and preserved with native line geometry, including reference 19's column continuation. Two cited originals received scoped passage checks; 61 other originals and fourteen dependencies or scope requirements remain unverified. The small labels inside the schematic GIS-layer thumbnails in Figure 1 are unresolved; they are not claimed as exact dataset identification.

## Output resolution does not establish geological accuracy

The authors explicitly restrict the framework to **macro-assessment and preliminary feasibility**, stating that it cannot underpin screening of particular sites or project design (page 4). They also state that the 1 km grid is generated from geological data with well spacing around **20–50 km**, and cannot resolve faults, channels or permeability barriers absent from those observations (page 5).

Table 1 associates one well per 25, 100, 400 or 2,500 km² with spacing below 5, 10, 20 or 50 km. Square-root arithmetic reproduces those boundary numbers under a square-grid convention. It does not prove equivalence for irregular well patterns, and the strict inequalities and printed map-scale notation remain unchanged.

The alternative 0.01° × 0.01° grid is not automatically a constant 1 km². Three disclosed spherical examples show latitude-dependent area; no source projection or erroneous native area calculation is inferred. Original CRS, masks, resampling and aggregation weights are required to reproduce capacity integration.

Two synthetic fields also demonstrate the information limit: both equal one at coarse endpoints, while one has an unobserved positive interior peak. They remain indistinguishable from those observations despite a fine output grid. The 72 example rows are not native geology, an uncertainty distribution or an error estimate for China.

## Emission inventory and captive-power overlap

Table 2 reports these 2022 sector totals:

| Sector | Source records | CO₂ stream (Mt/y) |
| --- | ---: | ---: |
| Coal power | 1,133 | 4,658.2 |
| Crude steel | 280 | 1,763.4 |
| Coal chemical | 312 | 392.7 |
| Cement | 2,948 | 2,099.9 |
| Printed summary | 4,673 | 8,914.1 |

The counts sum correctly. The emission rows sum to **8,914.2 Mt/y**, a 0.1 Mt/y difference compatible with conditional nearest-displayed-unit rounding. That observation does not justify silently changing the printed summary. The 226 Mt/y high-concentration column also needs native stream membership before any addition to the total.

Applying the stated 85% net-capture assumption to the printed summary gives **7,576.985 Mt/y**, consistent with the rounded 7.6 Gt/y statement. Stream concentration in vol% is distinct from capture efficiency; captured mass is distinct from full-chain avoidance and geological retention.

The paper acknowledges possible captive-power double counting. Its 320 Mt/y captive quantity is about **6.87%** of the printed coal-power total. Subtracting it conditionally gives 4,338.2 Mt/y, resembling the prose's 4.34 Gt/y, and changes the 85%-capture product by 272 Mt/y. This is a diagnostic hypothesis, **not a corrected inventory**. Exact facility overlap and the criterion for calling the effect negligible remain unavailable.

## Balanced resource stocks, different annual matching shares

All Table 3 sums close at displayed precision:

| P50 quantity | Onshore | Offshore | Total |
| --- | ---: | ---: | ---: |
| Theoretical resource (Gt) | 1,305.7 | 1,201.6 | 2,507.3 |
| Effective resource (Gt) | 756.2 | 743.6 | 1,499.8 |
| Matched flow, 150 km (Mt/y) | 3,757.7 | 453.3 | 4,211.0 |
| Matched flow, 300 km (Mt/y) | 4,993.1 | 476.2 | 5,469.3 |
| Matched flow, 800 km (Mt/y) | 5,559.2 | 548.2 | 6,107.4 |

Resources are nearly balanced onshore/offshore, while roughly **89–91% of annual matched flow is onshore**. The two statements concern different quantities. Neither the stocks nor the matching outputs establish pressure-constrained annual injection limits. Dividing a resource by a chosen lifetime cannot supply that missing physical service.

Pressure buildup, well-field design, geofluid production and water-recovery wells are discussed, but native pressure controls, well interference, water volumes, pumping/disposal utilities and retention verification are not supplied in the main PDF. The P10–P90 capacity range does not close those gaps. Matching uses P50 values; quantile conventions and joint geological/economic uncertainty remain unverified.

## Percentage and cost boundaries remain unresolved

The body describes 4.2 Gt/y at 150 km and 6.0 Gt/y at 800 km below 90 USD/t, calling them 59–79% of captured emissions. Literal arithmetic gives:

- 4.2 / 7.6 = **55.26%**;
- 6.0 / 7.6 = **78.95%**.

If both masses are conditionally rounded to the nearest 0.1 Gt, the first fraction cannot exceed approximately **56.29%**, below 58.5% needed to round to 59%. That rules out this particular display-rounding explanation; it does not recover the actual denominator or a corrected result.

Other statements need separate case mappings: the abstract gives 60–75%, the body describes over 69% in a cost range and over 79% of cases below 90 USD/t, and the implications give 64–75% of industrial emissions within 300 km. For the same Table 2/3 case, all 300 km matches are **61.36% of gross emissions** or **72.18% of calculated captured mass**, before cost filtering. The source may use different cases or denominators; none is selected silently.

Similarly, the 800 km total is about **80.6% of calculated captured mass**, but **68.5% of gross emissions**. It cannot automatically validate an unqualified claim to manage 80% of coal-sector emissions. Source-count eligibility, captured mass, avoided mass and stored mass remain distinct.

All costs are said to be escalated to 2022 USD. Original indices, regional coefficients and case budgets are unavailable locally. Typical storage ranges of 3–10 USD/t onshore and 10–60 offshore are not universal bounds: Figure 7 includes a >100 USD/t class and a `None` category, which is not zero cost.

Figure 1 is an illustration using **50% net capture, 250 km and LACOE in USD/MWh versus installed GW**. It cannot be pooled with the main 85%-capture, USD/t cases. Figure 8 distinguishes levelized and avoidance costs, while Figure 9's abatement-cost caption has a Levelized Cost ordinate and logarithmic matched-capacity axis. Figure 10 uses a linear annual-capacity axis. Exact native curve and denominator arrays remain missing; no exact results are recovered from pixels.

## Candidate coverage, deployment and prior work

The statement that over 99% of sources have a candidate within 800 km concerns geographic source-count coverage. A disclosed two-source/shared-sink LP illustrates why this differs from feasible mass delivery: all sources can have candidates while a shared capacity allows only half their demand. The LP is a diagnostic counterexample, **not the unprinted ITEAM formulation**.

The source assumes prompt retrofit and operation at modeled capacity. Its twelve coalitions, enterprise-sharing stages, provincial agreements and statutory carbon corridors are proposals, rather than a reproduced annual construction, dispatch or operating policy. Nor does a named cost synergy establish a complete low-carbon electricity, heat or water inventory.

Two [scoped cited-original checks](../evidence/comprehensive_review_inputs/B2-14_citation_checks.json) qualify context:

- **Reference 23, Lin et al./B2-17, pages 1–3:** supports the stated data-scale, technology/economy/policy, transport/cluster and algorithm/physics challenges. It does not establish that every previous model lacks integration or validate Wei's results. The 2025 DOI/online date and 2026 volume do not create an identity conflict; B3-46 remains its duplicate.
- **Reference 52, Middleton and Bielicki/B3-44, pages 1–2:** supports integrated capture/transport/storage economics, shared trunklines and a 1 km cost raster. This establishes earlier high-resolution infrastructure-cost modelling, without equating it to the new geological database or reproducing either native case.

The Fan et al. *Scientific Data* 2025, 12:640 citation is an **unverified future lead** for a public injection-capacity dataset. Its title alone does not establish pressure-constrained service, adequate metadata or model validity. It has not been retrieved under the continuing external-search pause.

## Reproduction and Paper 1 status

The [inputs](../evidence/comprehensive_review_inputs/B2-14.json), [native bibliography record](../evidence/comprehensive_review_inputs/B2-14_bibliography.json) and [reproduction summary](../outputs/comprehensive_review/B2-14_reproduction_summary.json) preserve source numbers, provenance and missing fields. [audit_zonal_pairing.py](../scripts/audit_zonal_pairing.py) produces **57 limited checks**, three spherical cells, 72 synthetic grid rows and three disclosed LP cases. Six focused tests cover geometry, underdetermination, shared service, unit scaling, rounding/denominators and invalid domains.

Native ITEAM/GIS, cost surfaces, source matching, capacity algorithms, pressure models, cost curves and full utilities remain unreproduced. Page 13 states that data can be requested and SM1 is free online; neither was acquired locally and no author was contacted. External retrieval remains paused pending the requested Chrome connection.

Paper 1 acknowledges the existing national integration and coalition-planning framework while preserving its stated limits. **No accepted operating/GHG input or current numerical result changes.** The prior combined 1.5 MPa HOLD remains; native files are preserved and the comprehensive goal stays active.

Regenerate the scoped checks with:

```bash
python paper1/scripts/audit_zonal_pairing.py
python -m unittest discover -s paper1/tests -p test_zonal_pairing.py
```
