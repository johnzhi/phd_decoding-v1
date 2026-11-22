# B2-12 postcapture inventory audit — in progress

Fraga, Korre, Nie and Durucan model cost and GHG tradeoffs after capture for Northern Lights, Stella Maris and combined network analogues. The [retained paper](../papers/B2-12.pdf) is *Carbon Capture Science & Technology* 11 (2024) 100190, DOI [10.1016/j.ccst.2024.100190](https://doi.org/10.1016/j.ccst.2024.100190), under CC BY-NC-ND 4.0. SHA-256: `d72f7eb3ced1df218f53b4c2d3bf025331957a8ea362ad38b9bf5b6b6166ccf3`.

All 24 retained pages, including the internal appendix and references, have been read as text and visually inspected, with sixteen magnifications. The complete item catalogue, remaining component checks and original-source/model verification are in progress. This interim finding does not certify the paper or its authors' models as complete. External retrieval remains paused pending the requested Chrome connection.

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

## Remaining audit work

The paper's prospective inventory excludes capture/purification and several construction, coolant, maintenance, decommissioning and fugitive contributions. Shipping capacities differ between pressure configurations, so their comparisons do not isolate pressure. Its transported/stored-mass denominators do not establish avoided emissions or permanent retention.

The full audit will retain the pressure/unit labels, tank material and integer-sizing bases, appendix/body factor differences, time/stock/activation notation, weighted-objective scaling and physical storage limits as separately located checks. Published formulas and partial component reconstructions do not establish that unavailable native code contains the same printed issues. Complete native cost/MoMILP/LCI cases, exact inventories and underlying originals remain unverified.
