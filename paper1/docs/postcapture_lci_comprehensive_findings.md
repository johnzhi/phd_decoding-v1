# B2-12 postcapture inventory audit

Fraga, Korre, Nie and Durucan model cost and GHG tradeoffs after capture for Northern Lights, Stella Maris and combined network analogues. The [retained paper](../papers/B2-12.pdf) is *Carbon Capture Science & Technology* 11 (2024) 100190, DOI [10.1016/j.ccst.2024.100190](https://doi.org/10.1016/j.ccst.2024.100190), under CC BY-NC-ND 4.0. SHA-256: `d72f7eb3ced1df218f53b4c2d3bf025331957a8ea362ad38b9bf5b6b6166ccf3`.

All 24 retained pages, including the internal appendix and references, were read as text and visually inspected, with sixteen magnifications. The [item record](comprehensive_review/B2-12.md) covers twenty figures, sixteen main numbered tables, Appendix A1/A2, thirteen numbered equations, notation, 87 claim records and 21 open issues. Original-source, asset and model verification remain incomplete. No paper or author model is certified complete. External retrieval remains paused pending the requested Chrome connection.

## Combined 1.5 MPa result placed on HOLD

Pages 20 and 22 describe a combined-concept best solution at 20% emission-objective weight, with **39.2 kgCO2e/t CO2 stored** and **11,617.7 ktCO2e** total emissions. Figure 20 on physical page 21 is captioned as the combined-concept best solutions. Its 1.5 MPa absolute-emissions mosaic labels these disjoint components:

| Figure 20 component | Labelled emissions (ktCO2e) |
| --- | ---: |
| Transport — ship operation | 9,043 |
| Transport — pipeline construction | 2,605 |
| Injection — well construction | 572 |
| **Subtotal of these three labels** | **12,220** |

That subtotal already exceeds the prose total by **602.3 ktCO2e**, before adding any other category. Under a conditional nearest-displayed-unit interpretation, the three integer labels have a lower sum of 12,218.5 kt, still above the prose total's upper value of 11,617.75 kt. These are display intervals, not measured uncertainty. Unlabelled positive components cannot reconcile the difference.

The figure may depict a different solution from the prose, or another source error may be present. Exact solution arrays and case/figure mappings are unavailable. The audit preserves both presentations and does not infer a corrected total, intensity or policy.

The [evidence record](../evidence/comprehensive_review_inputs/B2-12_case_conflict.json) preserves the native page locators, three manually read labels, rounding assumption and source hash. The [three checks](../outputs/comprehensive_review/B2-12_case_conflict_checks.csv) can be regenerated with [audit_postcapture_case_conflict.py](../scripts/audit_postcapture_case_conflict.py). No figure-area measurement is treated as a native result.

## Consequence for Paper 1

`gwp_combined15` remains quoted as 39.2 in the 250-row curated source table, with status `HOLD_CONFLICTING_BEST_SOLUTION_CASE`. It is removed from eligible analysis inputs and from its two Appendix A score calculations. The table keeps a clearly marked HOLD row; the threshold plot uses the five remaining eligible reported intensities.

Current benchmark input count is **133**, compared with the original 134. It produces **47 derived rows and 75 directly transcribed fleet rows**, compared with the previous 49 derived rows. This change removes a disputed source case from a supporting cross-study diagnostic. It does not change the controlled annual, shared-source, dispatch, primary-source or reference-inventory numerical outputs.

The other five intensities remain source-reported, partial postcapture scenarios. Their continued use in the explicitly conditional score is not independent validation of their native networks or whole-chain LCA. The reported-intensity range, reference intensity and algebraic crossing remain unchanged. The source quote on HOLD receives no substitute value.

## Inventory boundaries and pressure comparisons

The prospective inventory excludes capture/purification and several construction, coolant, maintenance, decommissioning and fugitive contributions. Liquefaction electricity is averaged across referenced process methods, with country-specific GaBi 2023.1 backgrounds. It is not a complete matched capture-to-ship heat/electricity/cooling/material balance. Feed CO₂ is assumed already within impurity limits; the eight upper limits are not an exact mixture.

The tables describe 0.7 and 1.5 MPa designs, while some prose uses 7 and 1.5 MPa and Appendix A2 labels tank designs 7 and 15 MPa. The separately stated 7 MPa inlet may be intentional; it is not automatically corrected along with the design labels. Gauge/absolute pressure and native states require verification.

The allowed vessel capacities also differ: low-pressure designs use a broader set, while high-pressure transport is restricted to 10 kt. Direct-injection ships form a separate option. Reported differences therefore do not isolate pressure as a causal variable. Generic inventories use transported mass, whereas network intensities use stored mass; neither denominator establishes whole-chain avoided emissions or permanent retention.

## Tank and ship material checks

Table 3 prints steel density as 7,861 **t/m³**. An explicit alternative interpretation as kg/m³ approximates the reported tank masses; the literal unit gives masses 1,000 times greater. Both remain visible. No source unit is silently repaired.

A thin-wall hoop-stress comparison and a cylinder with two flat ends approximate the displayed diameters, volumes and material quantities. These are analyst component calculations, not native pressure-vessel-code validation. The illustrative Figure 5 layouts use diameters of 17.50 and 7.00 m, different from Table 3's 13.96 and 6.52 m; their footprints cannot be adopted as the actual case layout.

Facility tank counts reconstruct using a ceiling: 6/10/20/50 kt cargo requires 2/2/4/10 low-pressure tanks at the printed 5.28 kt capacity. Ship tank factors in Table 10 instead approximately follow a continuous-capacity relationship. Exact sizing, material and characterization inputs are missing. The appendix's 50 kt storage value of 12,027 tCO₂e also differs from Table 5's 12,567; neither is selected as a correction.

DWT and base-ship-plus-tank additions reproduce selected printed components. Full GaBi/Panamax regression and characterization are unavailable, and Table 9's last DWT label is literally `200,0000`. These checks do not independently reproduce ship construction or additional direct-injection equipment.

## Operations and time factors

The body specifies terminal fugitives of **0.00286 tCO₂e/hour/site**, while Appendix A2 gives **0.0286**, ten times larger. A continuously active site over 30 nominal years would have different releases under those assumptions; no actual-site factor is chosen.

Table 12 pairs inputs headed g/km with outputs in kgCO₂e/km. Its arithmetic resembles an input-kg interpretation, differing by 1,000 from the literal g interpretation. The body lorry total of 7.78 also differs from appendix 7.7. These remain source questions, not accepted measured route inventories.

Loading/offloading work, the number of operations and rounded electricity factors need reconciliation. The ships' Table 13 factors can be compatible with two operations and an unrounded electricity factor near 0.03131 kgCO₂e/kWh, which could round to 0.03. That inverse calculation is not an accepted supplier factor. Appendix work for some capacities differs from the body's 0.2 kWh/t, and the truck row has an additional unresolved basis.

Equation 8 divides trip duration by 24 although its definition uses days and its fuel factor is per day. Its vent ratio is also positive before the stated 46-day pressure-buildup allowance. Neither a corrected trip convention nor a corrected vent law is adopted. Terminal recirculation and 98% filling do not supply a complete thermal/BOG model.

Equation 12 raises additional stock/activity questions: construction is multiplied by years, fleet counts need cargo-capacity scaling, and ongoing release uses an activation increment rather than the active state. A disclosed five-period example shows the distinction. Equation 13 separately uses active well counts for ongoing release. Native code, constraints and bookkeeping may differ from printed notation; these observations are not proof of implementation defects.

## Objective, calendars and geological service

The cost/GHG weighted sum does not print normalization or dimensional weights. The same numerical percentage can select a different design when emissions are expressed in kilograms rather than tonnes. A disclosed two-plan example demonstrates this unit dependence, without assuming how the native optimizer handles units.

A separate three-plan MILP has cost/emission points (0,10), (6,6) and (10,0). Weighted sums miss the nondominated middle point; an emission-limit formulation finds it. Thus a 10% weight sweep does not certify every nondominated discrete network. At 100% emissions weight, cost tie-breaking also needs clarification. None of these examples is a reproduced author network.

The chosen NL weights are explicitly 10% and 50% at the two pressures, despite blanket prose saying pressure does not change the chosen point. Conclusions also mention stochastic implementations although no stochastic scenario/information model is specified here. These distinctions remain explicit.

Source/hub/field numbers differ between prose, captions and legends. Five period-average profiles, rounded source totals and CAGR equivalents do not determine exact annual arrays. The 6,051 Mt field resources and opening periods are cumulative stocks, not pressure-constrained annual injection rates. Native pressure, well interference, safe operating schedules and retained-carbon verification are absent.

## Original-source and reproduction status

All **58 printed bibliography entries** are recorded with native line geometry, including column/page continuations. One [scoped original check](../evidence/comprehensive_review_inputs/B2-12_citation_checks.json) covers Roussanaly et al. 2021, retained as B3-38, DOI 10.3390/en14185635. Selected pages 1, 3 and 4 were text-read and visually inspected. They explicitly compare **7 and 15 barg**, describe capture-outlet through reconditioning boundaries, and examine feed, impurity and capacity constraints. They do not verify Fraga's averaged duties, assumed densities, native MILP or GHG factors. The remaining 24 pages of that original and its source chain remain pending.

The other 57 printed entries and fourteen native asset/model dependencies remain unverified. Internal Appendix A1/A2 was inspected. No embedded files or explicit external supplement/data/code notice were identified; this does not prove absence online.

[audit_postcapture_lci.py](../scripts/audit_postcapture_lci.py) produces **133 limited checks**, [28 source design rows](../outputs/comprehensive_review/B2-12_generic_designs.csv) with explicitly analyst round-trip/full-or-98%-cargo examples, and eleven scalarization rows. The three earlier case-conflict checks remain separate. Native GWP fields in the design examples stay blank. Full MoMILP, cost regression, licensed Sphera/GaBi/CML inventory, fluid/thermal and geological models remain unreproduced.

The existing combined-case HOLD exclusion is preserved. No additional operating/GHG inputs or corrected source values are accepted. Continue exact-source and native-asset verification; the next local main paper is B2-13.
