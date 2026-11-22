# Python matching and clustering: comprehensive retained-PDF findings

Togay, Serik and Lee (2025), *Journal of Cleaner Production* 525, 146563. DOI: [10.1016/j.jclepro.2025.146563](https://doi.org/10.1016/j.jclepro.2025.146563). Source: [B3-05](../papers/B3-05.pdf), SHA-256 `24edcd8c8b194b47bf136cb5224e239f389fccc0798be6985ff416fb6be935fa`.

All **eleven retained pages**, graphical abstract, seven numbered figures, every panel/caption/legend and **nineteen printed equations** were read and visually inspected, with enlarged checks. The [item record](comprehensive_review/B3-05.md) maps 45 claims, 18 variable groups and 16 issues. No main-PDF table is present. **The comprehensive review remains incomplete.**

[Equation transcriptions and native regions](../evidence/comprehensive_review_inputs/B3-05_equations.json) preserve printed indices and expressions. [Bibliography geometry](../evidence/comprehensive_review_inputs/B3-05_bibliography.json) retains 48 entries. Three additional named authorities and fourteen dependencies bring the record to 65 source/dependency items, not 65 verified originals.

## Essential native assets remain open

Appendix A explicitly links a **separate publisher supplement**. Table A1 supplies capture/sector parameters; Table A2 supplies the seventeen storage-site properties; Figures A1/A2 contain additional designs. These assets have not been located or inspected locally. Their external availability is not inferred from the local search.

The exact advertised code URI is [https://github.com/aminatgy/CCS-NetOptmizer](https://github.com/aminatgy/CCS-NetOptmizer), while the prose uses “CCS-NetOptimizer.” The native URI is preserved. Repository commit, licence, dependencies, solver and full-case correspondence remain unverified. The paper says data will be available on request; no request has been sent. External retrieval remains paused pending the requested Chrome connection.

Consequently, the native Kazakhstan MILP, routing, hydraulic sizing and 5000-trial Monte Carlo study have **not** been independently reproduced. Synthetic examples and printed arithmetic below do not replace those models.

## Objective, assignment and time need explicit definitions

Equation 1 prints `minimize EI + TC`, while prose claims a weighted programme that first eliminates unstored emissions and then selects least cost. Weights, normalization, bounds and the complete solver formulation are not given. Unlike units cannot be added without defined scaling. Finite weights do not automatically establish strict priority.

A disclosed counterexample uses two analyst designs: one with zero residual and cost 1 billion USD; another with one residual unit and zero cost. With EI weight 100, using dollars selects the second; changing money units to billions selects the first. This illustrates the need for specified scaling. It does **not** identify the authors' weights or demonstrate their code's behavior.

Equation 17 literally sums over `i` while describing one sink per source. Its printed index is preserved rather than silently changed to `j`. Equation 18 compares captured `C_i` with storage `D_j`, but the annual-rate versus cumulative-stock horizon is not explicit. Equation 19 also needs route/source coupling, domains and clarification of the free sink index and minimum-distance expression.

A separate analyst example has 1 Mt/y and a 10 Mt stock: the raw numbers satisfy `1 ≤ 10`, but thirty years require 30 Mt. This does not prove how the native code handles time. The displayed static volumetric equation and nineteen constraints/relations do not themselves demonstrate the claimed multi-period or pressure-aware capability.

## Printed units and environmental boundaries

| Printed component | Audit qualification |
| --- | --- |
| Capture cost, `CRF × unit cost × annual flow` | Dimensionally USD/y under the stated inputs, despite a USD label. Capture fraction CRF differs from the Monte Carlo capital-recovery CRF in 1/y. |
| Pipeline/booster/well costs | Original coefficient units, currency year, scaling, `a1/a2`, annualization and well-count treatment need verification. No guessed million-dollar multiplier is supplied. |
| Compression with universal molar `R` and kg/s | Requires a molar-mass/specific-gas basis and W/MW conversion. Ideal-gas illustrations do not validate dense-phase CO2 equipment. |
| Injection power | Consistent hydraulic dimensions give watts; the printed `g` unit is m/s. Static/backpressure, gravity/datum, operating hours and phase need native verification. No sign correction is invented. |
| Fugitive factor 1.4 t/km/y with length in m | The stated units conflict; per-ton wording also differs from the equation. The factor's original calibration remains unverified. |
| Electricity intensity 0.882 kgCO2e/kWh | Annual energy gives kg/y, requiring conversion to t/y. Earlier symbols denote power, later kWh/y. Native mix factors and hours are unavailable. |

For illustration, the quoted leakage factor and an **analyst** 100 km give 140 t/y if length units match. Multiplying by 100000 m without converting the factor gives a raw number 1000 times larger. This is a unit diagnostic, not a native emission estimate or proof of an implementation error.

Similarly, **analyst** 1 MW for 8760 hours is 8.76 million kWh; the quoted grid intensity gives 7726.32 tCO2e/y after explicit conversion. These are not observed equipment loads or a verified grid calculation.

Most importantly, Equation 11 defines capture emissions as `(1−capture fraction) × source emissions`: **uncaptured residual CO2**, rather than a complete inventory of capture heat, auxiliary electricity, compression, cooling and suppliers. The reported 99.95% capture dominance therefore does not establish a capture-energy footprint. Figure 6 separately labels captured mass, residual capture EI, abated mass and source emissions; captured mass is not automatically an emitted burden.

Residual/abatement naming in the objective, abstract and captions needs reconciliation. The source-emission curve also varies across radius cases, so included source IDs, DBSCAN noise handling and common comparison coverage must be checked. No fixed national baseline or corrected emissions series is inferred from the plot. The leakage claim below 0.01%/y is not accepted as site-calibrated retention evidence.

## Geometry and cost comparisons are conditional

The seven displayed radii are **100, 180, 200, 240, 300, 360 and 400 km**. With `min_samples=2`, DBSCAN epsilon is a neighbor-distance threshold. Four analyst points at 0, 90, 180 and 270 km form one cluster at epsilon100; its diameter is 270 km and maximum centroid distance 135 km. A fifth point at1000 is noise. This Euclidean component check does not verify the native geodetic metric or source database.

A second synthetic triangle has source flows0/1/100 and root0. The shortest tree has length2 but flow-distance proxy201; a direct star is longer at2.414 yet has proxy142.421. Minimum geometric length therefore need not minimize a flow-weighted objective. This is not actual pipeline USD or proof that the native optimizer is suboptimal.

Fourteen rounded Figure 4 totals were transcribed. They are **nonmonotonic** across radius: full labels23,34,35,35,31,34,38 and partial24,36,35,35,31,34,38. The chart axis is BUSD, while component legends use MUSD. Figure 5 prose says11→10 MUSD and24→23 MUSD, whereas its axis and later uncertainty discussion use billions. That factor-1000 money-scale question remains unresolved.

The explicit100 km totals23.30/24.02 billion USD and unit costs201.38/207.61 USD/t imply approximately115.7 Mt denominators. They do not determine whether the native denominator is stored or abated mass, nor annual versus lifetime cost. Reported reuse amounts yield scale-free savings9.09% and4.17%; they do not resolve absolute currency. Unrestricted entry/exit to reused corridors, actual rights, integrity and parallel-pipe counting remain unverified.

Five uniform uncertainty marginals and5000 trials are reported. P5–P95 gives a central90% empirical envelope **under those assumptions**, not confidence in the median or true system prediction. Other-cost uncertainty, dependence and trial results are absent. Overlapping full/partial intervals do not establish equality, equivalence or paired ranking probabilities.

## Scoped original checks and remaining implications

Two [citation checks](../evidence/comprehensive_review_inputs/B3-05_citation_checks.json) were made against retained exact originals:

- **Lee, Tan and Chen2014 (B3-14), pp1–3:** verifies existing multi-period retrofit planning, explicit time intervals, finite injection/stock limits and compensatory-power emissions. Its network topology and pressure calibration remain outside this check.
- **Zhang et al.2019 (B3-43), pp1,2,4:** verifies carbon-tax uncertainty, financial-risk metrics and epsilon-constraint tradeoffs. Geological uncertainty is reviewed as context; the inspected passages do not establish an author-calibrated physical-failure model.

These add two scoped edges, not two completed papers. Other identity issues remain: the printed Zhang2023 title concerns DBSCAN pipeline-data work rather than the described Northeast China MILP; Knoope2013 is a pipeline-model review; Middleton2020 and the cited Energy Procedia2009 paper are not interchangeable with retained B3-44's IJGGC2009 article. No convenient edition substitution is made.

Funding, all three author contributions, AI-readability declaration and no-known-conflicts statement were read. The paper is CC BY-NC-ND4.0; repository rights remain a separate question. Current legal/incentive proposals and EOR benefits are not verified adoption, permits or whole-chain climate credits.

Run `python paper1/scripts/audit_python_matching.py` for **34 checks**, five synthetic graph points, three trees, four weight examples, two horizon examples and fourteen rounded cost labels. Four tests address dimensional conversion and the disclosed counterexamples. No B3-05 values are in the accepted input tables. Accepted inputs/results, including the combined 1.5 MPa HOLD, remain unchanged. Continue with B3-06 while SI, code and source/model dependencies stay open.
