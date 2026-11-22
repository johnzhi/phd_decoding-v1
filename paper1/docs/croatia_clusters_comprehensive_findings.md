# Croatian CCUS clusters: comprehensive retained-PDF findings

Vulin and seven coauthors (2023), *International Journal of Greenhouse Gas Control* 124, 103857. DOI: [10.1016/j.ijggc.2023.103857](https://doi.org/10.1016/j.ijggc.2023.103857). Source: [B3-04](../papers/B3-04.pdf), SHA-256 `1350adda60535707db730edcecafd85628ab019d4615d4b7593bffda290d26a8`.

All **13 pages**, twelve figures, four tables, captions/legends and **159 substantive table cells** were read and visually inspected. Maps, lithology, cross-section and tables were enlarged. The [item-level record](comprehensive_review/B3-04.md) tracks 56 claims, eight analyst relations, 18 variable/assumption groups and 17 open issues. No native numbered equation was identified. **The comprehensive review remains incomplete.**

[Native table text and coordinates](../evidence/comprehensive_review_inputs/B3-04_tables.json) and [59-entry bibliography geometry](../evidence/comprehensive_review_inputs/B3-04_bibliography.json) retain provenance. Brezovac (2021), named for DSA Osijek on p8, lacks an explicit bibliography entry and remains unidentified. Together with fourteen further dependencies, these make 74 unverified records, not 74 verified originals. No new primary-passage citation edge is claimed.

## A screening study with confidential native forecasts

The paper identifies three clusters and recommends **Eastern Croatia for further study**. It considers onshore injection for early economic feasibility, using twelve emitters, existing transport corridors, depleted fields and deep saline aquifers. It does not present a solved national network-cost optimum or a complete capture-to-storage utility/LCA model.

Seven oil fields were represented with conceptual compositional Eclipse models. Production and final reservoir pressure were matched, production projected to 2025 and EOR simulated through 2040. Detailed static models and per-well data were explicitly omitted **because of confidentiality**. Ivanić/Žutica PVT studies informed their models; other fields used estimated minimum miscibility pressures. Native grids, connections, histories, controls, SCAL, compositions, MMP estimates and calibration residuals remain unavailable locally.

The common 2025 start was expressly **not optimized** for each field. Calibration is not independent prediction validation. MMP is a lower miscibility condition rather than a maximum geomechanically safe injection pressure. No timestamped native pressure/rate series or documented field pressure cap is supplied here.

The public-data availability statement refers to previously published data and Strategy CCUS reports. It does not provide the confidential inputs or establish independent model reproducibility. The exact deliverables and native cases remain unverified.

## Stocks, precision and readiness

All nineteen assets are described as Tier 2: fourteen depleted hydrocarbon fields and five DSAs. The authors explicitly call the regional aquifer capacities highly theoretical and say traps need further investigation. Table 1 sums to **2584.5 Mt**, with Sava 535.7 Mt and Drava/Osijek 2048.8 Mt. These agree with the rounded regional descriptions of 536 and 2049 Mt, but establish neither annual injectivity nor safe operating service.

Table 2's fourteen one-decimal field capacities sum to **143.6 Mt**. Figure 11's individually rounded labels sum to **146 Mt**, matching the prose. Every integer bar can be obtained by rounding its Table 2 value. This explains how different aggregate bases can arise; it does not validate a native field model or justify replacing either source number.

The same distinction affects Eastern Beničanci/Bokšić: Table 2 gives **8.8 + 13.6 = 22.4 Mt**, while rounded bars give **9 + 14 = 23 Mt**. Dividing those stocks by 0.86 Mt/y gives 26.05 or 26.74 years respectively. These are stock/rate quotients, not validated operating lives or proof that the fields can accept the source rate.

The text's nine Eastern fields/113 Mt and five Central fields/31 Mt do not identify exact membership. No alternative assignment is invented from numerical totals. Forecast availability dates range from 2021 to 2040, with delayed depletion already acknowledged. They do not establish present 2026 availability. EOR before complete depletion is distinct from later pure-storage readiness.

Table 3 lists ten generic screening criteria without the seven fields' actual measurements or certainty grades. The `CN` header uses percent while its criterion is `C5–C12`; the porosity `>11` unit cell is blank. Depth-to-top values of 727/750 m cannot automatically be compared with the `h >760 m` screening condition without confirming the depth/target basis. No universal classifier or verified all-pass result is reconstructed.

## Gross intake is not net storage or lifecycle avoidance

Table 4 reports annual injected CO2, produced/emitted CO2 and oil. Assuming each mean uses the same case, period and weights:

| Field | Mean injected, kt/y | Mean produced/vented, kt/y | Difference, kt/y |
| --- | ---: | ---: | ---: |
| Beničanci | 8542 | 5291 | 3251 |
| Ivanić | 5890 | 3501 | 2389 |
| Kloštar | 3957 | 2519 | 1438 |
| Lipovljani | 275 | 80 | 195 |
| Šandrovac | 2979 | 1274 | 1705 |
| Stružec | 5892 | 3593 | 2299 |
| Žutica | 1849 | 769 | 1080 |
| Sum | **29384** | **17027** | **12357** |

The aggregate unproduced fraction is **42.05%**, compatible with the paper's approximate overall 40% description. Field-specific produced fractions differ: Lipovljani is about 29.09%, while some exceed 60%. The generic 40–60% account need not bound every field or equal an unweighted field average.

These differences exclude complete capture/recovery energy, upstream burdens, additional oil combustion, market substitution and long-term fate. **42.05% is not an accepted Paper 1 retention or avoided-emission factor.**

The Lipovljani emitted-minimum cell is literally **`0 23`** in the retained table. It remains numeric **null**. Neither 0.23 nor 23 is guessed. Twenty unambiguous min/mean/max metric groups have ordered means; the unresolved group is excluded. Marginal minima/maxima do not reveal paired annual net extrema, so the audit does not subtract independent minimum/maximum columns as actual net flow.

## Testing the “any two or three” claim

The paper states that any combination of two or three fields would store the Central/Eastern emissions of 3.36 Mt/y. On the reported mean basis:

- **Gross intake:** Lipovljani + Žutica = **2.124 Mt/y**, below 3.36. Nineteen of 21 pairs and all 35 triples meet the target.
- **Unproduced difference:** Kloštar + Lipovljani + Žutica = **2.713 Mt/y**, below 3.36. Thirteen of 21 pairs and 32 of 35 triples meet it.

The full register contains 224 combinations across pair/triple size, gross/net basis and targets of 3.36/5.5 Mt/y. These refute a universal mean-rate reading. They do not establish an annual dispatch plan, capture fraction, pressure-constrained service, reliable simultaneous operation or full climate benefit. Desiring all seven full benchmark scenarios is also different from proving a minimum national import requirement.

Twenty-one separate analyst recycling examples hold gross injection `I` and produced CO2 `P` fixed, with recovery fraction `f` of 0, 0.5 or 1. Recycle is `fP`, fresh supply `I−fP`, venting `(1−f)P` and unproduced mass `I−P`. Both gross and fresh mass balances close. Perfect recovery improves the unproduced/fresh ratio under those assumptions, but no recovery plant, duty, impurities, dynamics, oil counterfactual or pressure response is modeled.

Seven further screens multiply mean differences by an analyst fifteen elapsed years (`2040−2025`) and compare with static Table 2 stocks. This is not native time integration; inclusive annual records could number sixteen. Static hydrocarbon-replacement estimates and dynamic EOR withdrawal/composition can have different bases. Large ratios require common-case reconciliation, rather than proving a physical capacity violation.

## Transport, costs and legal/source limits

The transport proposals concern **new CO2 pipelines along existing natural-gas corridors**, with road alternatives for small sources. They do not assume gas-pipeline repurposing. Corridor proximity, an existing Molve link and proposed reverse connections do not establish design suitability, rights, permission or available throughput. Central hub alternatives are conceptual; Eastern's 18–65 km geometry and no-upstream-hub recommendation are not a routing optimum. Body 175 km and conclusion 100 km criteria need reconciliation.

The capture charts use **2015 USD/t captured** and **2014 EUR/t** with different process boundaries. Exact unlabelled bar heights are not digitized into native data. The twelve-source sector pie sums to 5.54 Mt/y, compared with 5.53 in the body; displayed rounding accommodates the difference. Future closure and permission statements remain dated evidence. “Ready-to-transport” Rijeka CO2 does not specify composition, state or zero capture duty.

The native CCS Directive pointer is `2009/28/EC` and needs original verification. The EOR/ETS/Taxonomy eligibility statement is historical, rather than a current project determination. Brezovac identity, exact project reports and all underlying source/model chains remain open. Schematic TWT seconds are not depth kilometres; BNg and angular markers are not assigned guessed meanings.

Funding, eight author contributions and no-known-conflicts statement were read. Native copyright is Elsevier, all rights reserved. No embedded files or explicit supplement/code release were identified; no online absence is inferred. External retrieval remains paused pending the requested Chrome connection.

Run `python paper1/scripts/audit_croatia_clusters.py` for 56 checks, seven mean rows, 21 recovery examples, seven stock screens, two quotients and 224 subset screens. Three tests address mass conservation, source-driven sufficiency counterexamples and precision/unparsed-value separation. Native reservoir, optimized-network, utility and lifecycle models remain unreproduced.

Paper 1 can acknowledge existing cluster screening, staged storage alternatives and explicit data limitations. It must preserve stock/rate, precision, fresh/gross/recycled mass, availability and oil-climate boundaries. Accepted inputs/results and the combined 1.5 MPa source-case HOLD remain unchanged. Continue with B3-05.
