# Ketzin coupled inversion: comprehensive reading findings

All nine retained pages of Wagner and Wiese (2018), B1-14, have been read and visually inspected, including enlarged figures, tables, captions and legends. The [item record](comprehensive_review/B1-14.md) covers eight figures, two tables, 18 section groups, 16 claim assessments and 12 analyst/prose identities. This PartII prints no numbered equations of its own; its forward/inverse equations are referred to PartI. Source SHA-256: `7ec340fa668a4d1ae467095965d5619766b265ac7a994574eabffe567a58a093`. The original PDF is unchanged; illustrations are not newly redistributed.

The paper remains **incomplete under the comprehensive-audit standard**. One citation has scoped checks against a retained original. The other38 printed sources, eight model/data dependencies, essential PartI methods and external assets remain unverified. The [68 limited checks](../outputs/comprehensive_review/B1-14_checks.csv) and [reconciliation](../outputs/comprehensive_review/B1-14_reconciliation.json) do not reproduce the native coupled inversion.

## What is coupled and what is calibrated

The study jointly uses pre-injection hydraulic tests, CO2 pressure changes, two arrival observations and processed crosshole electrical measurements. “Fully coupled” describes hydraulic/multiphase/geoelectrical inversion. It does not establish a coupled thermal-mechanical pressure limit, dynamic salt-precipitation simulation or maximum annual injection service.

Three pumping tests and three observation wells provide nine nominal well/test pairs. Two histories, o200p201 and o201p200, are rejected after incompatible fits and an instrument-swap explanation. Seven pairs appear in Figure5. The diagnosis is reported by the authors; raw logger/QA evidence is not retained for independent verification.

Removing those histories removes the earlier basis for a hydraulic-barrier hypothesis. It also removes sensitive information. The authors explicitly conclude that model nonuniqueness means a barrier **cannot be excluded**. A fitted permeability map is not proof of barrier absence or a unique geological field.

The model normally converged in3–5 iterations. Iteration5 was retained because later nearwell artifacts gave only marginal observation-cost improvement. Native priors, regularisers, Jacobians, residual weights, iteration traces, alternative starts and forward cases are missing. Convergence and calibration do not establish independent prediction or global optimality.

## Objective functions and observation quality

Table1's reductions reproduce approximately65%,96%,81%,77% and80% for hydraulic, arrival, CO2 pressure, electrical and total observation costs. These are reductions in weighted, normalised cost, not percentages of physical error, storage improvement or explained variance. The full regularised objective is not given in this part.

The electrical group is downweighted by ten. The text explicitly instructs multiplying its table objective by ten for comparison. Its inverted cost is.025; restoration gives.25. The square root then changes by √10, not ten. The rooted value.5 is a **normalised cost indicator**, not a verified50% raw resistivity error: PartI's residual normalisations and covariance are needed for that interpretation.

The printed inverted component costs sum to.0954, whereas the total is.094. Conditional nearest-display rounding intervals overlap, especially because hydraulic2×10−2 is coarse. No total is corrected. The count226×273=61,698 also closes, but daily averaging, smoothing, shared baselines and overlapping configurations mean these are not independently distributed observations.

The prose specifies a14day moving average; Figure7 labels the displayed red curve a moving median. These could be different inversion/display operations, but the mapping is not supplied. The grey2σ moving-standard-deviation band is not an independently verified95% confidence interval. Figure7b also shows a substantial quantitative mismatch, acknowledged in the text, with the inverse response leaving the displayed range while observations stay near one.

## Saturation, laboratory geometry and missing physics

The ambient core experiment gives n2.6; earlier work gives1.62 and1.65–1.8. The homogeneous, time-constant fitted exponent reaches its lower bound1.62. This can compensate for insensitive configurations and model limitations; it is not a unique measurement of the field exponent.

Analyst Archie identities use true homogeneous bulk resistivity, two-phase brine/CO2 pore fill and fixed fluid/surface/P/T effects. A field apparent-resistivity ratio is nonlocal, with positive and negative sensitivity and borehole/annulus influences. Directly applying the homogeneous inverse to field ratios can generate invalid saturations. Ratios below one can be valid apparent observations; they are not discarded or clipped into a gas estimate.

The sample is reported as55mm high with15mm radius, giving5.5cm height and approximately38.88mL bulk cylinder volume. Figure1 labels its axes centimetres, while z ticks0–.5 cover nearly the full depicted sample. This scale needs clarification; no label, native model geometry or result is repaired. Raw sample masses, saturation/resistivity fits and finite-electrode cases remain unavailable. Figure4's initial relative-permeability curves explicitly rely on unpublished core measurements.

## Pressure references, arrival times and a checked original

The pressure gauge is at550m, with a static CO2-column correction to640m. No native P/T/EOS profile or pressure-reference metadata is retained to reproduce that90m correction. Rate measurement8m upstream,5s acquisition,5min plotted pressure and rate-period endpoint observations are separate operations.

Pressure **differences** are fitted. Figure6's absolute offsets are permitted by that design, including the July4 example. Matching pressure changes is therefore not independent validation of an absolute BHP ceiling or a future maximum-rate forecast.

Table2 observed/modelled arrivals21.7/21.8 and271/283days give errors.1 and12days, or.4608% and4.428%. The printed.5%/4% labels are compatible with rounding. Their unweighted relative RMS is an analyst metric and is not equated to the differently normalised arrival objective.

The [Class2015 primary check](../evidence/comprehensive_review_inputs/B1-14_citation_checks.json) uses retained B1-15, SHA-256 `4c8ec9850a78e897d5d4f271cd04449b7cfeb448a69fd1339416e4c8d2221324`. Selected text and rendered pages1–3,5–6 support pressure/arrival calibration and explicitly describe gas-membrane sensors150m below ground, annulus accumulation, upward transport and several-day uncertainty. The same observed21.7/271days are confirmed. Class's ECLIPSE/DuMux predictions are different cases and are not substituted for B1-14's predictions or treated as independent data.

This supports B1-14's sensor-delay caveat, without validating its3% model-cell gas threshold. It does not complete the Class paper's comprehensive audit or verify its underlying citations. The subsequent [B1-15 reading](ketzin_history_comprehensive_findings.md) covers its full retained PDF and printed constitutive components while keeping native models and underlying originals open.

## Salt, skin and transfer to Paper1

The fitted equivalent skin is10.1, rounded to10 in the conclusion. The paper associates this with about15mD in a1m nearwell zone, an approximately eightfold local permeability reduction, and roughly doubled pressure variations. Constant skin is expressly a first approximation: precipitation grows during injection and rewetting can dissolve salt after a stop. Native dynamic salt, phase and geometry inputs are missing.

An independent two-zone radial Darcy identity illustrates why these numbers are not interchangeable:

`s = (k/ks − 1) ln(rs/rw)`

`pressure ratio = (L+s)/L`, with `L = ln(re/rw)`.

At the same state and pressure margin, the conditional rate ratio is the reciprocal. For analyst L5,10.1 and20 with s10.1, it is approximately.331,.5 and.664. The same skin therefore does not universally mean double pressure, half rate or an eightfold annual service decline. These are conditional counterexamples, not reproduced Ketzin gas-flow cases or adopted service factors. Actual well/far radii, phase mobility, time dependence and pressure constraints remain unknown.

Figure8's four plume maps show vertically integrated net thickness at31/101/146/200days. The weighting definition and native arrays are not given here. Qualitative agreement with earlier NW/S or westward migration supports an interpretation, not a complete mass/retention balance or quantitative independent future validation. Proposed seismic and PNG assimilation are future extensions, not completed inputs to the inversion.

Paper1 can use this study to motivate measurement QA, multiple data types, uncertainty and validation of approximate models. It cannot transfer skin, local permeability loss, objective reduction or small arrival errors into annual maximum service, permanent retention, safety probabilities, commercial allocation or GHG benefits. Accepted numerical inputs and operating/GHG results are unchanged.

All39 bibliography entries, including the split Lengler entry on pp8–9, are preserved in the [reference register](../evidence/comprehensive_review_inputs/B1-14_bibliography.json). The essential PartI original remains unverified; two p4 references print2008 instead of the listed2018 identity. No correction is imposed. Raw monitoring/lab/SCAL data, native forward/inverse cases, weights/filters and publisher/code/supplement/erratum checks remain open. External retrieval is paused pending the requested Chrome connection.

Validation for this checkpoint: the full92-paper inventory/hash check, workbook/document builds, link/diff checks and126 tests passed. New tests distinguish objective/residual scaling, preserve source rounding and incomplete citation states, check homogeneous Archie domains, and verify the radial skin identity against an independent numerical resistance integral. Passing these checks does not validate the unavailable field inversion.
