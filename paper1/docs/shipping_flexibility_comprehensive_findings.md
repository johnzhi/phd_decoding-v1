# B2-10 international shipping-flexibility audit

Fraga, Korre, Nie and Durucan compare UK, Northern Lights and Stella Maris network analogues to examine growth, delays and interconnection. This is relevant prior work for Paper 1's account of transport flexibility and staged infrastructure. The implementation reported here is deterministic cost minimization after capture. The broader model name and workflow do not establish a stochastic policy, a cost/GHG Pareto analysis or complete capture-to-storage climate results for this study.

All nine pages of the [retained GHGT-17 manuscript](../papers/B2-10.pdf), including internal Appendix A, were read as text and visually inspected, with thirteen magnifications. Coverage includes four numbered figures, two tables, all 24 appendix line/heatmap panels, one numbered objective and nine printed references. The printed source is [SSRN 5070419](https://ssrn.com/abstract=5070419), for GHGT-17, Calgary, 20–24 October 2024. SHA-256: `7f4394948f17ba0dea0bbdc4e7bd05c213d061313a83f6d13f51b3ee362bb260`. The [item record](comprehensive_review/B2-10.md) preserves 36 claims and eight open issues. No comprehensive completion is claimed.

## Scope and the scenario count

Page 3 explicitly states that this implementation uses a 30-year horizon at annual resolution and excludes stochasticity and multi-objective optimization. Equation 1 minimizes a sum of costs by transport mode, origin, destination and year. It does not print the underlying mass, capacity, asset, injection or domain constraints. The total includes conditioning, intermediate storage, transport and injection after capture.

Figure 1 shows the broader model family's cost, LCI and deterministic/stochastic/multi-objective workflow. It names CPLEX without an exact version, gap, solver log or executable case. The paper's source “emission profiles” are assumed CO₂ quantities to be handled, rather than a reported lifecycle GHG inventory. The abstract's language about maximizing storage does not constitute a separately printed storage-maximization objective or prove that every source quantity is injected.

The labels resolve the scenario-count ambiguity:

| Context | Baseline | Alternatives |
| --- | --- | --- |
| Integrated UK+NL+SM | 0 | a, c, e, g, i, x, y |
| UK standalone | 1 | b, f |
| NL+SM standalone | 2 | d, h, z |

There are **15 labelled designs: three baselines plus twelve alternatives**. The alternatives comprise four growth, four source-delay, two storage-delay and two interconnection cases. The abstract, results and conclusion call these “15 what-if scenarios,” while also discussing the baselines separately. No additional alternatives are inferred.

Table 1 compounds the mapping problem: its standalone storage-delay entries are “n/a,” omitting `z`, which appears in Table 2 and the result plots. Its “SM” column also corresponds to the broader NL+SM context elsewhere. The [scenario register](../outputs/comprehensive_review/B2-10_scenario_register.csv) preserves all fifteen labels and their stated baseline comparisons.

These are separately optimized deterministic what-ifs. No scenario probabilities or multistage information constraints are supplied. Six-year delays therefore do not establish an observed failure distribution or a tested recovery policy for unforeseen interruptions.

## Inputs and graphics that need native mapping

The model assumes ship capacities of 6, 20 and 50 kt CO₂, onshore pipeline diameters of 6, 12 and 18 inches, and offshore diameters of 36, 40 and 48 inches. Exact unit conversions do not establish hydraulic throughput or annual ship service. The intermediate buffer is sized to one cargo from the largest upstream ship. Actual arrival timing, load mix, weather, downtime and tank trajectories are not supplied.

The stated UK source profile runs from 2,016 to 2,034 kt/year, and NL+SM from 1,001 to 28,402 kt/year. Their combined endpoint quantities are 3,017 and 30,436 kt/year, with a stated horizon total of 333.8 Mt. These few quantities do not determine the thirty annual arrays. The UK baseline in Appendix A.1 appears below 1,000 kt at its first plotted year before approaching 2,016 kt, unlike the prose's first-year statement. This remains an apparent profile/index question; exact pixel readings are not substituted for native data.

Other identity questions are explicit:

- Prose and the map caption identify Yara as 1 and Norcem as 2. Figure 3's legend reverses those numbers.
- Figure 2's map uses hubs 11 and 12, while the prose/caption lists 10 and 11.
- Bunter Closure 36 appears on the UK map but is absent from the caption's injection-field list of 13–14.
- The NL+SM trip heatmap refers to base case 1, while its context and baseline row are 2.

No missing node 8, route distance or source assignment is invented. Geographic analogues and historical project descriptions are not present-day permits or storage allocations.

## Cost metrics and reported ranges

The appendix outer ranges reconcile several results:

| Metric | Reported outer variation across contexts |
| --- | ---: |
| Annual cost | −71% to +316% |
| Fleet size | −3 to +5 ships |
| Annual trips | −212 to +343 |

These are relative changes or count differences against specific baselines. They are not probabilities, horizon-wide savings or independent validation of optimal schedules. Fleet counts aggregate three cargo classes; trip counts lack loaded/empty-leg and utilization definitions. Annual well accumulation is named as a metric, but no corresponding series is supplied.

Table 2 needs further reconciliation. The growth row prints a levelized-cost range of −4.8% to −4.8%, despite differing signs in the plotted comparisons. It prints a positive, descending unit-cost range of 5.8% to 1.3% alongside “mostly lower” wording. The storage-delay row includes a −0.4% unit-cost endpoint although its summary says costs are higher. The interconnection row calls a mixed −0.5% to +3.3% range an increase. These signs and endpoints remain literal; no missing minus sign or replacement value is assumed.

Page 5 states that levelized cost uses a 10% discount rate, but full numerator, mass denominator, base year and timing conventions are absent. Equation 1 has no explicit discount factor; its cost terms might already embed discounting. The native implementation cannot be classified as undiscounted solely from that notation.

For a common feasible set, adding optional choices cannot increase the globally minimized value of the **same** objective. That does not imply that every differently discounted or normalized metric must fall. A disclosed two-plan LP illustrates this: a restricted plan costing `[0,101]` over two years has a lower present-value cost at 10% than an optional plan costing `[100,0]`, even though selecting the optional plan reduces undiscounted total cost from 101 to 100. The conditional levelized metric also rises with a fixed service denominator.

This example does not resolve the authors' metric definitions or prove their interconnection results right or wrong. It prevents a false error claim based only on the reported increase in one levelized metric. Exact cash flows, handled quantities, sunk assets and access rules are still required.

## Buffer, field and climate limits

A one-cargo tank can be adequate for a particular regular arrival cycle without guaranteeing continuous delivery. A separate analyst inventory LP starts with 20 mass units and withdraws two per hour. It covers ten hours without arrival; a twelve-hour gap requires four units of unmet delivery unless capacity and initial stock rise to 24. This is a mass-balance illustration, rather than an assumed weather event or a corrected native buffer.

The geological models cited here provide costing for platform/well and subsea designs. The retained paper does not supply a pressure-constrained annual reservoir dataset, well interference, safe BHP trajectories, a complete resource constraint or a post-closure mass balance. Likewise, postcapture cost components and a generic LCI workflow do not supply matched capture heat, compression/liquefaction work, cooling, utility suppliers or whole-chain avoided emissions.

The conclusion's fleet pooling and coordinated-network benefits remain case-specific planning interpretations. Exact objective definitions, common service, infrastructure timing and operational feasibility are needed before transferring the apparent savings. No cost difference, handled mass or model-family intensity becomes a Paper 1 climate or retention factor.

## Original-source and reproduction status

One [scoped original check](../evidence/comprehensive_review_inputs/B2-10_citation_checks.json) covers the exact Fraga et al. (2024) parent study, B2-12 pages 1–3. It supports the broader multi-objective cost/GHG framework with a prospective LCI after capture, and the discussion of batchwise hubs and cargo-based storage sizing. Its Northern Lights/Stella Maris cases differ from this UK-linked study; its reported 3.3–14.2% GHG intensities are not B2-10 results.

That check does not complete B2-12's audit, its cited-source chain or either native model. In particular, the 2024 parent is not a substitute for the separately cited 2021 cost-model paper. Eight other printed originals and ten native dependencies remain unverified.

Internal Appendix A was inspected in full. No embedded files or explicit separate supplement, code or data-availability notice was identified. Public availability, errata and rights remain unverified under the requested Chrome pause; no author contact was made. Absence locally is not absence online.

The [diagnostic script](../scripts/audit_shipping_flexibility.py) produces 60 limited checks and fifteen design-register rows. Three numerical tests cover optional-choice economics, an independently bounded inventory LP and financial/domain handling; all 206 repository tests passed. Native MoMilp/CPLEX cases, annual route/fleet/well schedules, regional cost models, field behaviour and LCI remain unreproduced. Original files and accepted operating/GHG inputs are unchanged.
