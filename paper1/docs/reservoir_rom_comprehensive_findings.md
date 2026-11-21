# B2-04 reservoir ROM: findings and limits

Luca Bertoni, Olav Møyner, Jan Wiegner and Matteo Gazzani (2025), DOI `10.1016/j.compchemeng.2025.109293`. All 12 physical pages of the [retained original](../papers/B2-04.pdf) were read and visually inspected, including five figures, three tables, all 34 numbered equations, inline relations, nomenclature and 31 bibliography entries. The [item register](comprehensive_review/B2-04.md) and [manual record](../evidence/comprehensive_review/B2-04.json) retain 32 claim records and the mathematical/asset qualifications.

**The paper remains incomplete under the comprehensive-audit standard.** Two citation edges have scoped primary support; 29 other originals and eleven native dependencies remain unverified. No native MRST training/validation, AdOpT-NET0 optimization, pump fitting or physical safety/retention model is independently reproduced.

## Contribution and demonstrated scope

The study incorporates a reduced reservoir-pressure model into a CCS-chain MILP. It starts from compressible, immiscible two-phase MRST simulations, applies proper orthogonal decomposition and trajectory piecewise linearization, and uses candidate-selection constraints to connect the resulting affine updates to infrastructure decisions. This is relevant prior work for Paper 1: reservoir/infrastructure coupling is already demonstrated as a modelling approach.

The numerical reservoir example has 13,754 full states, implying 6,877 cells under the stated two-state-per-cell formulation. It retains 71 pressure modes and one saturation mode, giving 72 reduced states and a 99.4765% dimension reduction. Five 30-year simulations supply snapshots; one supplies the principal TPWL operators. Four additional five-year injection profiles are used for numerical validation. Actual grid, fluid, well, basis, Jacobian, initialization and trajectory arrays are not supplied in the main PDF.

The reported ±5% result concerns **typically observed well-cell pressure differences against the full simulator**, not field observations, a strict global error bound, BHP accuracy, pressure-buildup accuracy or a leakage/retention distribution. The paper notes missed small pressure oscillations and underprediction/overprediction in the higher/lower injection cases. It also explicitly admits that reconstructed states may not strictly satisfy mass conservation. No native mass-balance tolerance is verified here.

## Equations and native implementation questions

The Taylor and projected-update components are available mathematically. With the stated Petrov-Galerkin choice `Psi = J Phi`, the reduced operator is `(J Phi)^T(J Phi)`. Full column rank is needed; this normal-equation structure can be ill conditioned. A zero projected residual does not imply a zero full residual. The [synthetic reconstruction](../outputs/comprehensive_review/B2-04_reconciliation.json) agrees with an independent least-squares calculation while retaining a nonzero full residual. These dimensionless matrices are not MRST data or a measured carbon-mass error.

Several printed details require native code/SI correspondence:

- Equation 5 differentiates a residual with shifted time indices relative to the new-step residual being solved. An indexing or modified-Newton convention needs clarification.
- The saturation snapshot dimension described in the text differs from the phase-block dimensions needed by Equation 12.
- Equations 26–28 retain `i` inside sums over `j`, unlike the explicitly selected `j`-dependent quantities in Equations 23–25. A one-hot sum of an unchanged coefficient does not identify different candidate coefficients.
- Absolute-distance, minimum-selection and selected-state/operator products require bounded linearizations or indicators. The main text does not supply all native bounds, big-M values, endpoint/tie handling or signed-coordinate mappings.

These are questions about the literal presentation, not demonstrated defects in unavailable author software. The audit does not silently repair them into a native model.

The MILP distance also deliberately changes the earlier POD-TPWL metric: it discards saturation distance and normalizes cumulative-volume differences by training values. A disclosed example with current volume 18 and training volumes 10/30/50 changes the nearest candidate from 10 to 30. This is a metric change requiring validation, not an algebraically identical reformulation. Epsilon `0.001` also needs compatible volume/coordinate units.

A bounded synthetic selector implements the one-hot minimum rule with fixed current states/distances. It selects the nearest candidate even when the objective favors another candidate's output. It does **not** reproduce the native variable-distance reservoir MILP, its rate-controlled well Jacobian conversion or its training operators.

## Time, density and pressure boundaries

The full-chain model uses daily decisions and six-month reservoir states. Equation 29 divides its mass-flow numerator by both the number of daily intervals and their duration. That gives an average volumetric rate if the inputs are interval masses; if they are already mass rates, the additional duration changes the dimensions. The convention must agree with Equation 34 and the native data. Both interpretations remain visible; no corrected input is chosen.

Equation 30 uses a single-cell Peaceman relation with mobility evaluated at training-average saturation and density evaluated at training-average well-cell pressure. The earlier relation `rho = b rho_surface` defines `b` as reservoir/surface density; the accompanying prose instead describes surface/reservoir density. The two definitions are not interchangeable. Equation 32 then uses a surface-density reference for a constant-density hydrostatic column. Actual surface conditions, well-column density, phase pressure, WI, depth and gauge/absolute/datum conventions require the supplement. Synthetic densities of 2/800 kg/m3 and depth 1,500 m are illustrative, not inferred paper inputs.

The constraint `BHP <= 0.9 pmax` is enforced at the coarse model resolution with approximate properties. A simple compatible-unit example has mean-rate BHP 150 below limit 162 but daily-peak BHP 200. It demonstrates why an average-control constraint alone does not establish peak feasibility; it is not a prediction for this field. Likewise, the selected well-cell error result cannot be treated as a guaranteed BHP error allowance preserving a 10% pressure margin.

The source itself emphasizes that the model does not replace comprehensive full-scale simulations. It also identifies pressure-dependent pipeline transport capacity as future work and warns that omitting it can yield infeasible chain designs. Saturation constraints for leakage-risk regions would require additional validation, particularly when retaining only one saturation mode.

## Timing, case study and utility scope

The four Table 2 speed ratios reconstruct to approximately 522, 1,040, 1,020 and 1,860. Those timings cover point selection, the reduced update and reconstruction. They exclude a complete MILP solve and training. The illustrative full-chain problem instead reports 220,532 continuous variables, 94 binaries, a 94.39-second solve and a 2% Gurobi gap, with an order-100 increase in solve time relative to omitting the reservoir model. Neither timing comparison is independently benchmarked here.

Table 1's initial/final rates, cumulative masses and ramp durations are preserved. Figure 2 includes plateaus, so a ramp duration need not equal the absolute time at which a final rate is attained. Endpoints and ramp labels alone do not reconstruct the five-year cumulative masses; exact native profiles, clocks and integration rules remain necessary. No conflict is manufactured by assuming an unstated linear ramp from time zero.

The illustrative cluster has two cement plants and one WtE facility, daily exogenous profiles and an increasing CO2 tax. The narrative's roughly 3,700–4,100 t/day seasonal injection band excludes lower startup values visible in the plot. Exact daily capture/injection series, tax/cost inputs and pressure limits are not recovered from pixels.

Reported 1–1.5 kWh/t and a 20–40% increase concern the **dense-phase injection pump**. They do not include capture heat, capture auxiliary electricity, initial compression, liquefaction, cooling or utility-supplier burdens. The native fitted pump plane and its domain/error are delegated to SI. A separate synthetic tangent-plane example has the exact bilinear residual `(mass_rate−reference_rate)(head−reference_head)/(rho eta)`, showing that such a plane can over- or underestimate depending on its domain. It does not evaluate the unavailable author fit.

## Sources, supplements and Paper 1

The [citation checks](../evidence/comprehensive_review_inputs/B2-04_citation_checks.json) preserve source hashes and inspected scope. Exact Becattini2022/B3-42 pages1–3 support a time-resolved multimodal MILP and substantial transport costs in a Swiss WtE case, while assuming Northern Lights availability without a storage-capacity constraint. Exact SimCCS2009/B3-44 pages1–2 support capacitated source/sink/pipeline selection and trunklines. These are infrastructure-context checks, not validation of Bertoni's reservoir model or whole cited-paper closure.

The [bibliography and dependencies](../evidence/comprehensive_review_inputs/B2-04_bibliography.json) retain 31 originals and eleven native asset groups. Aras DOI `109203` is distinct from the retained multiperiod B2-03 DOI `109300`; the latter is not substituted. The explicit Appendix A notice and data-on-request statement remain open. Essential SI covers well-Jacobian conversion, reservoir properties, case assumptions and pump fitting. No embedded/matched local supplement was identified; no absence of public assets is claimed, and no author message was sent. External retrieval remains paused under the requested Chrome connection.

Paper 1 recognizes the prior coupling contribution and retains its accuracy, conservation, temporal, pipeline and utility boundaries. No annual physical service, field safety probability, retained fraction or complete energy/GHG factor enters accepted inputs. Original PDFs and existing numerical model outputs remain unchanged.

The [35 limited checks](../outputs/comprehensive_review/B2-04_checks.csv) and [pump-plane example](../outputs/comprehensive_review/B2-04_pump_plane_example.csv) retain reported quantities and analyst cases separately. Five new tests cover POD/sign invariance, independent least-squares projection, bounded selection, rate/density units and temporal/plane examples. All 174 repository tests passed after register regeneration. Continue B2-05 while the 92-paper audit remains active.
