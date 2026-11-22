# B2-09 risk-aware network planning audit

Kattel et al. formulate discrete pipeline/well investment and annual operations with a capacity-derating variant and a scenario-based CVaR shortfall penalty. This is relevant prior work for Paper 1's treatment of delivery limits and infrastructure decisions. The authors explicitly describe a synthetic example; it is not a documented pressure-constrained reservoir dataset or a complete utility inventory.

All 19 physical pages of the unchanged [retained paper](../papers/B2-09.pdf) were read as text and inspected as rendered pages, with nine additional magnifications. Coverage includes 13 figures, four numbered tables, the parameter/variable displays, 17 numbered equations and all 71 printed bibliography entries. DOI: `10.1016/j.enbuild.2026.117200`; SHA-256: `05a904cb3c6323a7a46919d1fbfe39dd7fb10ca10e859cd28c16a718fe1dda90`. The [item record](comprehensive_review/B2-09.md) contains 56 claims and nine open issues. The paper remains comprehensively incomplete.

## What the uncertainty formulations represent

Equations 10–11 replace every nominal pipe capacity and per-well injectivity by its own lower coefficient. With the assumed 40% deviation, each coefficient becomes its nominal value multiplied by `1 − 0.4Γ`. The displayed constraints do not include a shared sum or cardinality budget limiting how many components can deteriorate. The paper's description of Γ as the fraction of each worst-case shrinkage is consistent with these rows; its later “how many components” interpretation is not represented by a separate shared uncertainty constraint.

This distinction does not prove a defect in unavailable author code. A row with one uncertain coefficient can have a simple robust counterpart. It does mean that Paper 1 should describe the displayed operation as a fractional coefficient hedge, rather than assume that Γ counts simultaneous failures. The exact Bertsimas–Sim original and native formulation remain unverified. The derating and CVaR formulations are presented as separate variants; the displayed CVaR equations do not themselves include Γ.

The stochastic case has five common factors—1.0, 0.9, 0.8, 0.7 and 0.6—applied simultaneously to every pipe and well, with probability 0.2 each. At confidence 0.95, the upper 5% tail lies within the worst atom's 20% mass. The mathematical CVaR therefore equals the **largest modelled annual scenario loss**. It does not resolve an observed 5% failure frequency. Page 12's reference to the worst 5% of years differs from the later qualification on page 15.

The [independent component checks](../outputs/comprehensive_review/B2-09_checks.csv) implement the discrete tail integral and compare it with a separately constructed linear program. Both agree. This validates the limited mathematical component under supplied probabilities, rather than the choice of probabilities, common-factor correlation or native losses.

Equation 17 sums discounted yearly CVaRs. This is generally different from CVaR of total discounted shortfall. A disclosed two-year analyst example with crossing scenario losses gives an annual-tail sum of 20 and a horizon-tail value of 10 under unit weights. It illustrates the distinction, rather than identifying an error in this study's unavailable native case. Equality can hold under additional conditions, such as a common worst scenario across years.

All annual operating variables can adapt to the selected scenario. No staged observation process or chronological nonanticipativity constraints are supplied. Discounted tonnes also differ from ordinary cumulative injected mass and annual compliance quantities.

## Successful accounting checks and their limits

Magnification resolves the Figure 5 S5 ribbon as **78.9 Mt**, with one decimal. Its six reported arc quantities close exactly to the two sink totals at printed precision:

| Quantity | Reconstructed from printed values |
| --- | ---: |
| Gross 20-year source emissions | 1,011.12 Mt |
| Captured/injected arc and sink total | 822.46 Mt |
| Sink R1 / R2 totals | 491.43 / 331.03 Mt |
| Wells | 65 + 52 = 117 |
| Parallel pipe units across six arcs | 9 |
| Installed parallel pipe length | 911.44 pipe-km |

The blue source boxes give gross emissions, rather than the smaller captured arc flows. Their difference is not a source-node conservation failure. Pipe-km counts parallel assets, rather than just corridor length. Constant-rate cumulative well bounds accommodate the reported sink totals, but neither those bounds nor a cumulative Sankey reconstructs the annual operating schedule or pressure feasibility.

The prose also attributes R1's larger allocation partly to more favourable transport distances. Every displayed source-to-R1 distance, and H1-to-R1, is longer than its corresponding R2 distance. The claimed distance advantage therefore needs qualification. This does not overturn the allocation: injectivity, costs and network interactions also affect the design.

The two 90% factors produce a target of 40.95036 Mt/year, or 81% of gross potential emissions. Availability at 8,000/8,760 hours is a separate convention. Coal emissions calculated from the printed rounded 2.31 lb/kWh factor can be compatible with 18.396 Mt/year on a full-calendar potential basis. The rounded factor cannot reconcile that same mass on an 8,000-hour basis. Exact potential-versus-operation mapping remains open; this is not a demonstrated emission-factor error.

Source salvage values match 5% of capital. Fixed well and pipeline operating costs match the stated 2.5% rule at their display precision. The cost claims of 18.9%, 51.8%, 72% and 27.7% are compatible with intervals around rounded billion-dollar endpoints. Differences from ratios of central rounded values are not established errors.

## Objective, time and reliability questions

Several printed mappings still require native implementation:

- Pipeline variable cost is stated in dollars per tonne-km, but Equation 1 shows coefficient times flow without an explicit length factor. A preaggregated coefficient or an additional length multiplier is needed. Neither is silently supplied.
- The case gives an 85 USD/t credit for the first 12 years and zero thereafter. Equation 1's revenue symbol has no time index. The reported post-year-12 flow change needs the implemented time profile and annual outputs.
- Salvage uses a discount symbol with an unbound time index outside the annual sums, while prose specifies the final year.
- Capture capital and sink development costs are charged unconditionally in the displayed expression. Source/site opening binaries and their links are absent; the zero convention for the positive-integer notation is not explicit.
- The case states 8,000 operating hours, while the equations bound the operating fraction between zero and one. An explicit native fixed value or tighter availability bound is needed.

The robust design meets a hard annual target; the CVaR variant permits a shortfall and applies a finite penalty. They have different service requirements. High-penalty mean shortfall remains approximately 15 Mt/year—about 36.6% of the stated target. That fraction is not a failure probability, and the result does not establish small, infrequent missed deliveries or compliance with an unspecified reliability threshold.

The model's economic response after credit expiry can produce underoperation even when physical capacity exists. Such outcomes should not automatically be described as random geological or transport failure. The common-factor scenarios are assumed, not calibrated to actual operating events.

Plot interpretation also needs restraint. Figures 8–9 have local component decreases and crossings despite increasing overall trends. Expected-cost/risk scalarization has conditional monotonicity properties for globally optimal solutions on a common feasible set; mean shortfall, individual well counts and pipe length need not share them. Connected curves do not supply raw integer solutions. The prose's λ range of 1–50, Figure 10's labels through 27–30, and Figures 11–13's axes through 40 need exact output mapping.

## Sources and implications for Paper 1

Two [scoped original checks](../evidence/comprehensive_review_inputs/B2-09_citation_checks.json) support limited context:

- Wang et al. (2016), B2-01 pages 1–3, supports coupling of distance, injectivity, cumulative capacity and economics. Its two-sink analysis explicitly uses static supply and assumed per-well injectivity. It does not calibrate a 40% derating band, CVaR probabilities or annual pressure response.
- Middleton and Bielicki (2009), B3-44 pages 3–5, already integrates discrete sources, pipelines and sinks with present-value costs. It explicitly has no temporal component, uses a 25-year lifetime basis and artificially reduces California pipeline costs. This qualifies broad claims of integrated-design novelty without validating either native case.

The remaining 69 printed originals and 12 native dependencies are unverified. References 23–26 have printed identities concerning product design, PV decommissioning and green hydrogen alongside a network-MILP attribution. Reference 41 is a pressure-superposition paper, while the cost discussion points to De Simone/Krevor estimates. Exact support and cost lineage require original passages; titles alone are not treated as a complete support check.

All production capacities and locations are assumed. EPA, EIA and NETL data are suggested for future real-region applications. No reservoir pressure/BHP constraint, cumulative resource, well interference, composition, capture-to-ship heat/work/cooling balance, supplier inventory, post-closure mass balance or full building LCA is supplied. Phased construction, learning, richer pressure models and large-scale decomposition are discussed as extensions, rather than reproduced capabilities.

There is no internal appendix or embedded attachment. The paper offers data on request; no request was sent. External supplements, code, errata and rights remain unverified under the requested Chrome pause. Local absence is not evidence of public absence.

The [diagnostic script](../scripts/audit_risk_network.py) produces 71 limited checks and 11 fractional-capacity rows. Six new tests validate the tail integral against independent LPs, domains, a crossing-year counterexample and accounting/rounding boundaries; all 203 repository tests passed. Native optimization, scenario calibration, formation response, full utilities and LCA remain unreproduced. No accepted operating/GHG input changes.
