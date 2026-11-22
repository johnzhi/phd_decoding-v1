# B2-07 source–sink and network review audit

Hu, Wu, Yang and Zhou’s “From point-to-point to hub-and-cluster: a systematic review of co-optimization of source–sink matching and transport networks for large-scale CO2 sequestration” is useful for distinguishing model scope, evidence maturity and evaluation standards. It explicitly declines a universal algorithm ranking and separates proposed AI and digital-twin capabilities from demonstrated network operation. Its systematic-review selection and several formulation and attribution details remain unverified.

All 24 pages of the unchanged [retained PDF](../papers/B2-07.pdf) were read and visually inspected, including 11 figures, six tables, 13 distinct unnumbered displayed mathematical relations and 86 bibliography entries. Pages 12, 15, 16 and 18 were additionally magnified. The DOI is `10.3389/fenvs.2026.1966624`; SHA-256 is `21a96f4a425beef54f68a5916da55c8aad2d6bd8351137a5c6389152dcc99363`. The CC-BY notice, editorial dates, funding, declarations and explicit supplement link were inspected. The [item record](comprehensive_review/B2-07.md) contains 88 claim records and nine open issues. The paper is not comprehensively complete.

## Search and evidence selection

The reported search took place on 16 September 2026. Web of Science supplied 518 records and Scopus supplied 1,051. Removing 427 duplicates from 1,569 records leaves 1,142; excluding 775 at title/abstract screening leaves 367 full-text reports. The five full-text exclusion counts—142, 86, 57, 46 and 19—sum to 350, leaving 17 reports for 17 included studies. All these arithmetic identities reconcile.

That does not reproduce the search, deduplication, retrieval or eligibility decisions. Exact database strings are assigned to Supplementary Table S1a; report-level exclusions and the extraction matrix are also assigned to the publisher supplement. Those assets are not retained locally. The main text does not provide a closed list and complete extraction record for all 17 studies. Table 6 contains five representative computational examples and must not be substituted for the complete eligible set. Main-text reporting also does not establish independent screening assignments, coding agreement or a reproducible quality appraisal; the missing supplement must be checked before concluding what it contains.

Eligibility allows partial linked decisions rather than requiring every decision to be optimized simultaneously. It does require identifiable geological sinks and extractable quantitative planning results. Contextual CCU, monitoring and general learning references are therefore distinct from direct eligible studies. The authors explicitly avoid pooled effects and do not infer missing comparison metrics. Their claim that the 17 studies exhaust the eligible search set remains an attributed result until the search and selection can be reproduced.

## Example equations and physical meaning

The compact allocation formulation on page 12 defines source and sink allocation totals and arc capacity bounds, but does not display incidence equations linking those totals to network arc flows. An analyst example with allocation and both terminal totals equal to one, but all arc flows and builds zero, satisfies the displayed bounds and definitions. This identifies an incomplete illustration; it is not evidence of a defect in any unavailable author implementation.

The longer schematic on pages 15–16 needs further specification:

- Injection `q_k` is explicitly defined in tonnes/year, while `C_k` is described as cumulative available storage. A literal `q_k ≤ C_k` does not establish lifetime resource feasibility. In an analyst example, 3 Mt/year satisfies a numerical bound of 10, but four years inject 12 Mt into a hypothetical 10 Mt resource.
- Hub conservation does not replace source delivery targets or sink-inflow linkage. With positive costs and only upper bounds, zero capture and zero flow minimize the schematic objective. A small independent MILP illustrates the difference between the displayed constraint classes, a separately added demand, and demand plus a sink-flow identity. These are disclosed analyst variants, not recovered source cases.
- The printed hub equation ends its quantifier after the membership symbol. The preceding prose supplies the intended intermediate-node set. The literal display and prose are preserved separately.
- Fixed capital and annual throughput costs require a common annualized or lifetime present-value basis. The basic expression has no explicit horizon or discounting. The dynamic expression introduces discount factors but leaves period-duration conventions and the capture term unresolved.
- A new-construction event variable does not alone define commissioned capacity, persistence, replacement or expansion. Asset-stock and flow-capacity links are still needed.
- Flow–diameter bounds and a written pressure interval do not independently establish pressure drop, temperature, phase stability or impurity feasibility. Those properties need valid preprocessing domains or additional physical constraints.
- The displayed robust min–max template does not specify recourse policies, information arrival or nonanticipativity. The discussion of multistage decisions is broader than that compact expression.

There is no complete native optimization case accompanying these illustrations locally. Synthetic examples cannot reproduce a cited network, physical reservoir or safety constraint.

## Two checks against original papers

Two [scoped citation records](../evidence/comprehensive_review_inputs/B2-07_citation_checks.json) preserve original hashes and inspected passages.

For Middleton and Bielicki (2009), retained B3-44 pages 1, 3 and 4 were read and visually inspected. They support integrated capture, pipeline and storage optimization. Page 3 already includes binary capture-facility investment and fixed and variable capture costs, and explicitly names ILOG CPLEX 11.0. Page 4 states that the model has **no temporal component**, with quantities converted to a 25-year lifetime basis. This contradicts the review’s attribution of a multiperiod dynamic framework to that 2009 paper and qualifies its solver-NR row. The generic introduction of capture investment cannot be assigned to 2014 without acknowledging the earlier formulation; the specific additional contributions of Hasan et al. still require their original paper.

For Budiarto et al. (2025), retained B4-06 pages 7, 8, 16 and 18 were read and visually inspected. They support a cost-minimizing allocation model using supplied annual injection limits and reservoir availability, with scenario and cost sensitivity analysis. The inspected objective and results do not demonstrate a Pareto frontier, full lifecycle assessment, endogenous emitter entry/exit or closed-loop adaptation. The review’s broader statements should use an appropriately matched source. This check does not reproduce Budiarto’s missing native annual-limit arrays, process/well simulations or MILP.

The other 84 printed originals and 12 implementation or asset dependencies remain unverified. The IEA project-database growth claim is assigned to an Energy Technology Perspectives reference and needs exact source support. A Zhao MMP-prediction entry appears in the bibliography without an explicit named main-body citation identified here; its supplement role remains unresolved. No substitute DOI, source or correction has been invented.

## Figures, reported scales and computation

Figure 8 is an illustration with 16 Mt/year of source rates and 780 Mt of storage resources. Their ratio is 48.75 years of aggregate full-rate service only under additional assumptions; it is not an operating-life or injectivity result. The illustrated 16–32 inch diameters do not supply hydraulic capacities.

Table 4 explicitly dates its project-status check to 4 August 2026. Porthos, Northern Lights, the proposed Summit Iowa filing and the Chinese planning model have different boundaries. The 688-mile Iowa figure is not the length of a verified operating national network. The Chinese approximately 80,700 km layout is a model output, not constructed infrastructure. Nominal project stocks, annual rates and expansion plans do not establish current access or operating availability.

Table 5’s pipeline and shipping cost ranges use different currencies, volumes, distances and case boundaries. They cannot support a matched cost ranking or a complete utility inventory. Figure 7 explicitly presents qualitative applicability regions rather than numerical modal thresholds.

Table 6 likewise warns against comparing different scopes and computational conditions. Its reported 258,900-second maximum runtime lies 300 seconds below a 72-hour cap; there is no contradiction. Solver gaps, piecewise-linear approximation errors and regret errors are distinct. The reported 10.09%, 1.55% and 0.52% approximation errors and 33-minute, 14-hour and 23-hour runtimes are not a controlled universal method ranking. None of the native benchmarks was rerun.

Figures 4–6 and the discussion explicitly treat integrated learning, adaptive dispatch and closed-loop twins as prospective. The proposed benchmark above 1,000 sources and 300 sinks is an evaluation priority, not a demonstrated achievement. The quantum statement concerns the reported 86-reference corpus, not a reproduced global search or hardware comparison. The disclosed use of AI for editing and figure alt text is provenance information, not evidence of a scientific error.

## Reproduction boundary and Paper 1

The [49 limited checks](../outputs/comprehensive_review/B2-07_checks.csv) reconstruct reported bookkeeping and arithmetic, together with labelled analyst examples for delivery linkage, stock/rate accounting, cost time bases, asset persistence and information constraints. Six tests verify these components using independent enumerations or identities. All 191 repository tests passed. They do not reproduce database selection, cited author models, trained AI, physical projects or quantum performance.

Paper 1 can use the review’s qualified guidance on common service, matched baselines, physical residuals, total computational effort and uncertainty. It should use the original papers for model provenance and substantive quantitative claims. No modal cost range, nominal storage quantity, future capability or benchmark target enters accepted operating or GHG inputs. External retrieval remains paused pending the requested Chrome connection; no author contact was made. Continue B2-08 while the 92-paper goal remains active.
