# B2-06 Multimodal strategic planning audit

Ayotte-Sauvé and colleagues’ “Multiperiod strategic planning of CO2 capture, transport, utilization and storage with multimodal transportation” develops geographically explicit annual infrastructure planning, fleet sizing, buffer storage and offshore injection choices. These are substantial prior contributions for Paper 1. Its Eastern Canadian results are explicitly illustrative and do not establish a calibrated national storage service or a complete lifecycle comparison.

The unchanged [27-page PDF](../papers/B2-06.pdf), DOI `10.1016/j.compchemeng.2025.109525`, has SHA-256 `d22b9de6a04b50ed10b83d7fe70aaf490821379766ca75c9f8962b81bb576aac`. All pages and internal Appendices A–D were read and visually inspected. The [item record](comprehensive_review/B2-06.md) covers 14 figures, Table D.1, 78 numbered equations including C.1, the five-step algorithm, nomenclature, appendix assignments and 65 bibliography entries. The comprehensive audit remains incomplete.

## Annual planning and operating feasibility

The model assumes steady processes, identical annual decisions within each planning period, deterministic inputs and immediate infrastructure availability at the start of the selected period. It explicitly leaves detailed vehicle schedules outside its scope. Annual fleet activity includes travel, loading, unloading and, for ships, berth time. Integer trip circulation also includes empty return trips: the printed Figure 3 example has 5.9 loaded-cargo equivalents, six outbound trips and six empty return trips. Six trips do not imply six required vehicles.

These constraints are useful planning approximations. They do not guarantee compatible daily vehicle assignments, shared berth occupancy, weather windows or buffer trajectories. An analyst example with two three-hour tasks required within the same three-hour window needs two vehicles, even though six total vehicle-hours fit easily inside one vehicle’s annual availability.

The source’s two-day buffer rule similarly uses average flows. At an analyst flow of 1 Mt/year, two days with a 20% margin give 6.58 kt of buffer. Delivering a hypothetical 40 kt uniformly over 24 hours into an initially empty tank, while withdrawing at 1 Mt/year, produces a 37.26 kt peak. This demonstrates why a reserve rule alone does not establish batch feasibility; it is not a recovered or failed Canadian schedule. The authors acknowledge that detailed scheduling is excluded.

Reservoir injectivity and lifetime capacity are supplied parameters. They can vary over time but are not calculated from a coupled pressure model here. Conditioning yields and costs also do not establish actual wellhead conditions, fracture avoidance, retained-carbon fractions or a complete capture-to-injection heat, electricity, cooling and supplier inventory.

## Questions in the printed formulation

Equation 10 bounds both process indices with the capacity indexed `1`, although Figure 1 and Appendix A define separate process capacities. A small analyst LP with `q1 = 1`, `q2 = 0` and `x2 ≥ 0.5` is feasible under that literal bound and infeasible under a separately labeled process-specific bound. The printed difference is confirmed by magnification. The unavailable native implementation has not been judged or silently corrected.

Equations 8 and 22 update inventory using annual flows without displaying the planning-period duration. Appendix A defines inventory as mass at the end of a period, and periods may span multiple years. Equation 18, in contrast, explicitly multiplies annual injection by period duration when calculating lifetime mass. In an analyst four-year example represented by two two-year periods, the literal inventory increments and the physical time integral differ. Native annual/period mapping, initial and closing stocks, and mass balances are needed to resolve the convention.

Other specific questions remain open:

- Equation 45 sums the auxiliary indirect-flow variable over ship types, while Equations 34–36 display its product linkage only for injection ships. Appendix A defines that variable more broadly. Transport-ship linkage or preprocessing needs verification.
- Equations 62–63 impose target equalities, whereas the case description calls the targets lower bounds. Yield losses, inventory changes and the actual native target constraints need a consistent mass balance.
- A positive minimum capacity addition in Equations 41–42 forces an addition in every period after opening. This is stronger than a one-time minimum installation.
- Equation 76 links opening events in the same period. A child opening after an already available hub would fail the literal event implication; cumulative availability would be a different constraint.
- Equation 68’s minimum-fleet conclusion requires a positive marginal cost for using vehicles and positive availability. “Nonzero” alone does not cover a negative coefficient.
- Equation 69’s loaded-mass fuel approximation needs an allocation for empty travel. The generalized objective also permits per-trip fuel costing, which can count empty returns correctly. The source should not be described as universally omitting empty-trip fuel.

## Heuristic and optimality claims

The five-step procedure solves a restricted first-period load model, an unrestricted load model, a fleet-sizing repair, a combined candidate and optionally the full model. The source acknowledges that loads underestimate actual trips, particularly for empty returns. Its printed equation references for removing and replacing vehicle constraints and costs need reconciliation with the numbered formulation.

A feasible repaired candidate still requires checking every full-model constraint and recomputing the full objective. A relaxation’s incumbent is not automatically a certified lower bound, and optimality of intermediate submodels does not establish global optimality of the full problem. The paper’s performance metric uses a common best lower bound from the standalone full-model run, rather than a known exact optimum.

All 30 gap/time pairs in [Table D.1’s transcription](../outputs/comprehensive_review/B2-06_performance.csv) are retained. For five periods, the displayed values support approximately 41.8% and 55% time savings at the stated common gap levels. For the 20-period example, 612 seconds is approximately 0.354% of two days, consistent with the rounded “0.4%” timing comparison. These are checks of reported arithmetic, not an independent runtime benchmark. Caption, refinement-stage and procedure-clock conventions still require native logs.

## Temporal partitions and illustrative results

The case uses 57.6 Mt/year from 144 emission points at 71 facilities and a 20-year horizon beginning in 2025. Its six equal-duration partitions contain 1, 2, 4, 5, 10 or 20 periods. Targets increase by `100/N` percent per period and reach the full annual target in the final period.

The [120 reconstructed annual target rows](../outputs/comprehensive_review/B2-06_ramp.csv) integrate to 1,152, 864, 720, 691.2, 633.6 and 604.8 Mt, respectively. **The authors explicitly acknowledge this change in cumulative service** and report cost per tonne as an additional comparison. The partitions therefore do not constitute a controlled comparison with an identical capture trajectory. The published total-cost and per-tonne percentage differences have overlapping conditional rounding intervals; no correction is forced from rounded point values.

The restricted-transshipment case contains several useful accounting distinctions:

- A 5 Mt/year transfer cap and an 8,000 t train correspond to 625 full-load equivalents per direction annually. A daily maximum requires additional calendar, partial-load or handling conventions; the annual constraint alone does not enforce four discharges on any particular day.
- A 10 kt injection ship carrying 457 kt/year requires at least 46 loaded trips, consistent with the reported example. The later 40 kt ship carrying 779 kt/year has 19.475 full-load equivalents and a conditional minimum of 20 loaded trips.
- Parallel pipeline capacities of 29.3 and 20.2 Mt/year total 49.5 Mt/year. That can legitimately exceed the reported 49.4 Mt/year achieved flow.
- The explicitly approximate pipeline-length components sum to 1,256 km versus a reported 1,253 km total. This is not a proven discrepancy at the stated precision.
- The body gives pipelines 19.1% of cost, while Figure 13 gives 19.2%. Both values remain visible. The pie’s 100.1% total is compatible with rounding and has not been normalized artificially.

The authors explicitly transfer US terrain-cost weights for illustration, neglect rail-spur costs at this scale and defer Canadian calibration, detailed transshipment siting and additional transit restrictions. These qualifications materially limit economic or operational transfer to Paper 1.

## Original sources and missing native assets

Two [scoped primary citation checks](../evidence/comprehensive_review_inputs/B2-06_citation_checks.json) preserve exact identities, hashes and inspected passages. Gabrielli et al. (2022), retained B4-07 pages 1–3, supports transport-backup and resilience context. It excludes storage-operation disruption risk, performs no independent risk assessment and uses container-based transport assumptions. Middleton and Bielicki (2009), retained B3-44 pages 1–2, supports raster-based candidate networks, partial capture and trunkline economies. It does not verify the later six SimCCS2.0 benchmark cases.

The other 63 printed originals remain unverified under this audit. The Alcalde entry combines a Nature Communications 2018 identity with a different DOI string; the Morbee DOI has a trailing `.Joris`. The Canadian 2021 Act and Element Energy 2018 are named in the text but absent from the printed bibliography. Literal identities and the complete native bibliography transcription are preserved in the [reference register](../evidence/comprehensive_review_inputs/B2-06_bibliography.json).

The paper states that data will be made available on request. Native GAMS/CPLEX cases, exact GIS realizations, cost vectors, parameter arrays, benchmark inputs, logs and rights have not been obtained. No matched external supplement or code was identified locally; that does not establish public absence. External retrieval remains paused pending the requested Chrome connection, and no author contact was made.

## Implications for Paper 1

Paper 1 acknowledges the existing work on geographically explicit multimodal planning, fleets, buffers, state changes and direct/indirect offshore injection. Its comparison should control common service and distinguish annual planning constraints from operating deliverability. The [99 limited checks](../outputs/comprehensive_review/B2-06_checks.csv) preserve printed quantities and analyst examples separately; they do not reproduce the Canadian optimization, warm-start procedure, six benchmarks, reservoir physics or actual schedules.

All 185 repository tests passed after register regeneration. No reported cost premium, fleet count, injectivity parameter, hypothetical schedule or partial process coefficient enters accepted operating/GHG inputs. Original files and existing numerical model outputs remain unchanged. Continue B2-07 locally; the full 92-paper goal remains active.
