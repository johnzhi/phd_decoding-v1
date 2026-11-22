# B2-08 stochastic shipping audit

Bjerketvedt, Tomasgard and Roussanaly’s “Optimal design and cost of ship-based CO2 transport under uncertainties and fluctuations” already combines capacity investment, buffers, weather-dependent sailing and operational recourse. Paper 1 must recognize this contribution. Its Norwegian case is a conditional planning study, with information, seasonal and process boundaries that prevent direct transfer of its buffer ratios or costs into a regional operating or lifecycle model.

All 13 pages of the unchanged [retained PDF](../papers/B2-08.pdf) were read and visually inspected, including 12 figures, six tables, 22 main equations, two appendix equations with reused numbering, the internal Appendix A and all 44 bibliography entries. Eight pages were additionally magnified. DOI: `10.1016/j.ijggc.2020.103190`; SHA-256: `060eb3b24c0362f5f16b202fe96d2fc8aee6c498d2cf97df21a3416796e1dcae`. The [item record](comprehensive_review/B2-08.md) retains 52 claims and nine open issues. The paper is not comprehensively complete.

## Information and operating boundaries

The case transports a fixed captured supply of 400,000 t/year over 715 km from Brevik to Kollsnes. The optimized chain starts at conditioning and ends after reconditioning; capture investment and downstream offshore pipeline/storage operation are outside the optimization. A very pure capture stream and no conditioning loss are assumed. Monetary penalties on venting do not establish complete lifecycle avoided emissions or permanent retention.

Each operational season contains 136 three-hour steps: 408 hours, or 17 days. Thirteen scenarios with two seasons each therefore represent 442 days. These are representative scenarios, rather than a continuous calendar or 442 days of independent operating validation. The authors explicitly acknowledge that all uncertainty for each 17-day scenario is known before operational recourse. Its objective is consequently optimistic relative to a comparable model with realistic information. The magnitude of that optimism and the effect on each individual capacity are not established by calling the bias “slight.”

The binary power strategy has scenario and season indices, but no hourly index. It selects a strategy for the representative season rather than providing arbitrary within-season power feedback. Exact sailing slots, probabilities, season weights and their conversion to annual costs are missing locally.

Source, ship and receiving inventories are closed cyclically within each separate representative season. The authors explicitly state that storage between months is not an option. The broader claim that seasonal storage is never cost-effective therefore extends beyond the represented feasible set. It needs a comparison that actually permits that strategy.

## Printed equations need reconciliation

Magnification confirms two questions in the printed formulation. Equations 17–18 increase receiving-buffer inventory with reconditioned outflow and decrease it with ship unloading, opposite the described physical roles. Equation 21 uses `≤` for a requirement described as a **minimum** transport fraction. It also has no displayed probability or season weights.

The [limited checks](../outputs/comprehensive_review/B2-08_checks.csv) keep literal expressions and analyst comparisons separate. A fixed-initial-inventory example exposes the receiving-sign difference. Importantly, if initial inventory is free and cyclic, and only symmetric capacity bounds apply, the complementary profile `C − y` can preserve feasibility and capacity cost. The printed sign question does not automatically prove that the native optimal cost is wrong. Likewise, a finite emissions penalty can encourage transport without making an upper-bound inequality a minimum requirement. No unavailable native code is silently repaired or judged defective.

Other implementation details remain open:

- Loading capacity is displayed as ship mass divided by 12 hours, while flow variables are masses in three-hour steps. A duration multiplier or a port-time parameter expressed in steps is needed. The native preprocessing convention is unknown.
- General balance equations include `h = 1`, alongside separate cyclic boundary equations. The predecessor and domain treatment need code verification.
- The conditioning and reconditioning terms in Equation 5 have no enclosing summation brackets, and the ship fuel coefficient lacks the scenario indices used by weather-dependent operations. Summation scope and coefficient preprocessing need clarification.
- Capacity costs based on annual rated flow need an explicit conversion to the per-step capacity variables. Numeric probabilities, seasonal weights and several continuous-variable domains are not fully supplied.

## Speed, weather and validation

Table 2 literally labels design power in watts with values 1,500–2,500. The inline added-wave resistance uses the first power of wave height, while Equation 22 uses its square. Equation 22 introduces `R_f`, whereas the nearby clear-water definition uses `R_cw`. Density is called relative density, although an SI force calculation requires mass density. Figure 4’s left panel starts near 15 knots and its right near 12 knots; the prose assigns constant and increased-power strategies in the opposite order.

The [78 conditional speed rows](../outputs/comprehensive_review/B2-08_speed.csv) evaluate Equation 22 with an explicit analyst assumption `R_f = P/V_design`, mass density 1,025 kg/m³ and standard gravity. Literal watts and a separately labelled kilowatt interpretation are retained. Both give 12 knots in calm water by construction, but diverge strongly under waves. This is a unit diagnostic, not a corrected source model, reconstruction of Figure 4, ship validation or accepted physical input.

The reported weather archive spans 1987–2016 at three-hour intervals and 1,106 points. More than 87,000 sailing simulations were reduced to 26 operational seasons. The exact MET product, route interpolation, simulator, scenario selection, weights and tail tests are not retained. The operator-validation statement has no accompanying measurements or error metrics locally. The authors themselves warn that extreme-weather delays may be understated. Neither storm frequency nor a selected 25-year scenario supplies an empirical ship-breakdown law.

## Buffer denominators and costs

The reported cases differ materially:

| Case | Source buffer | Fraction of 5,000 t ship |
| --- | ---: | ---: |
| 99% transport | 5,120 t | 102.4% |
| 100% transport | 5,890 t | 117.8% |
| Ideal one-cycle breakdown case | 8,660 t | 173.2% |

Their fractions of emissions accumulated over an average cycle use another denominator, approximately 4,330 t. The abstract and conclusion combine some lowest-cost and 118%-of-ship wording across the 99% and 100% cases. Paper 1 should retain the separate cases, rather than adopt a universal 18% buffer margin.

Most reported component arithmetic is compatible with its precision. The four main costs sum to 33.8 EUR/t. The 41.9 EUR/t cost for the last percentage point is approximately 24% above 33.8 and can be compatible with the rounded 1.8 MEUR increment. The reported 11.8 EUR/t energy total and rounded 7.8 plus 4.1 components have overlapping rounding intervals; their point-value difference is not a proven inconsistency.

Specific values still require native reconciliation. Table 4 lists 5,480 t as 110.0% of a 5,000 t ship, while the ratio is 109.6%. Ship investment and fixed-cost figures differ among Tables 1, 2 and 6. The stated 5.5% fixed-O&M rule matches rounded conditioning and buffer coefficients, but not the printed reconditioning coefficient. Harbor scaling uses exponent 0.85 in the prose and 0.8 in the appendix equation. Both conventions remain visible.

The standard end-of-year present-value factor for 25 years at 8% is about 10.6748, compared with Table 1’s 10.56. Normalizing 143 MEUR by 396,000 t/year and the standard factor is compatible with the rounded 33.8 EUR/t; the printed factor gives about 34.20. Construction timing, the three-year 40/30/30 investment schedule, penalty inclusion and actual transported-mass denominators need a common cash-flow basis before any correction is justified.

The 6.4 MEUR stochastic-design value, 4.1 MEUR fuel component and 1.9 EUR/t increase also have distinct bases. A disclosed calculation shows how different transported-mass denominators could explain a roughly 1.9 EUR/t comparison, but it does not resolve the native accounting. The body describes a total increase involving fuel, penalties and investment; the conclusion calls it a fuel-cost increase. Figure 9’s monetary/time basis and the breakdown cash flows remain open. Breakdown benefits are conditional on the ideal event assumptions, and the authors acknowledge missing fault statistics.

## Sources, utilities and reproduction limits

One [scoped original check](../evidence/comprehensive_review_inputs/B2-08_citation_checks.json) covers Roussanaly et al. (2014), retained B3-36 pages 1, 3 and 4. It supports distance/capacity benchmarking and conditioning context. Its 2–20 Mt/year offshore-delivery comparison differs from B2-08’s 0.4 Mt/year onshore-terminal chain, and it explicitly excludes glycol dehydration from its assessment. It does not supply a matched complete utility balance or validate B2-08’s stochastic buffer policy. The original begins on journal page 283, while B2-08’s bibliography prints 282; both identities are preserved.

The other 43 printed entries and twelve dependencies remain unverified. Jakobsen 2017a/b have matching printed titles and pages and are tracked as a candidate identity duplicate. Voldsund, MET, Eurostat, Worldwide and Anantharaman are named without complete corresponding bibliography entries. Appendix B explicitly points to external supplementary material, which is not retained locally. Public availability, contents and rights are unknown under the requested Chrome-connection pause; no author contact was made.

Appendix A’s PFD and utility prices do not provide complete stream states, capture heat, compression work, refrigeration, cooling, supplier emissions or downstream injection inventory. Dividing a rounded electricity-cost claim by a price produces only a conditional component estimate, which remains excluded from accepted operating/GHG inputs.

Seventy-three limited checks and six component tests cover printed arithmetic and disclosed LP, inventory, finance, scaling and speed examples. All 197 repository tests passed. They do not reproduce the native Pyomo/Gurobi optimizer, weather/scenario generation, Aspen/HYSYS/APEA processes, stochastic operating policy or breakdown model. Continue B2-09; no paper-completion claim is made.
