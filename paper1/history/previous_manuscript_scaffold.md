# Dynamic carbon break-even analysis of domestic and cross-border CO₂ storage: the decision value of reservoir deliverability and shipping utilisation

Working manuscript scaffold — no empirical model results have yet been generated. Statements about published studies refer to the supplied PDFs; their assumptions are not automatically validated for Japan, Malaysia or Australia. Source IDs and physical PDF pages refer to the accompanying evidence workbook. The original proposal is preserved.

## Abstract
Cross-border geological storage can enable CO₂ mitigation when domestic injection service is constrained or delayed, but additional conditioning, terminals and transport create greenhouse gas burdens. Existing research already models dynamic CCS infrastructure, pressure-limited storage, shipping uncertainty and life-cycle transport emissions. This study proposes to test the incremental decision value of jointly resolving annual storage deliverability and operational shipping under a common industrial-production baseline. Domestic-only, foreign-only and mixed pathways will be evaluated using four model variants that separately introduce time-dependent injection and voyage/terminal operations. Outputs will include cumulative retained CO₂, net avoided greenhouse gas emissions, feasible shipping utilisation, and the region where the additional retention from a foreign pathway equals its incremental whole-chain burden. Equal-retention controls and cross-evaluation of pathway choices will distinguish transport penalties from the benefit of additional storage. The prospective Japan–Malaysia–Australia application remains conditional on obtaining compatible, site-specific injection profiles and route inventories. No numerical conclusion about a preferred pathway is presented at this stage.

Keywords: geological CO₂ storage; deliverability; shipping; utilisation; lifecycle accounting; carbon break-even; model comparison.

## 1. Introduction
Geological storage resource, annual injection capability and accessible storage service answer different questions. A prospective reservoir may contain a large storage resource while pressure constraints, well development, temperature, water handling or commissioning prevent it from accepting captured CO₂ at the required time. For an industrial source, the relevant climate comparison is consequently between the quantities that competing pathways can retain and the greenhouse gas emissions incurred in enabling that retention. Distance alone cannot resolve the comparison.

Economic studies already connect transport configuration with reservoir properties. Wang et al. (2016) compare distance, injectivity and capacity in two-sink pipeline selection; Johnsson et al. (2017) and Kjärstad et al. (2016) show that shipping farther to better-injectivity reservoirs can be economically preferable in Nordic settings. These findings challenge nearest-sink screening, but economic preference is not itself evidence of greater net climate mitigation [B2-01, pp3–5; B3-39, p1; B3-33, p1]. Kang et al. (2015) also demonstrate scale-dependent transport costs, with a ranking reversal between pipeline and shipping in their selected cases; the route lengths differ and must remain part of the comparison [B3-07, pp6/18].

Temporal CCS planning is well established. Ooi et al. (2013) account for sink timing, injection rates and capacities through pinch analysis, while Lee et al. (2014) jointly represent capture retrofits, time-dependent source–sink constraints and compensatory power. Becattini et al. (2022) optimise yearly infrastructure decisions over 25 years, including overseas storage and a delayed hypothetical domestic sink, and calculate system emissions relative to business-as-usual. Bertoni et al. (2025) embed reduced-order reservoir physics in infrastructure optimisation. These contributions preclude a claim that dynamic deployment or baseline-based emissions accounting is introduced here for the first time [B3-11, p1; B3-14, p1; B3-42, pp1–7/15–16; B2-04, pp1/9–10].

Operational shipping also has substantial prior coverage. Bjerketvedt et al. (2020) link uncertain weather, vessel operation and buffers to transport completion and expected cost. Their optimal buffer depends on the required completion rate and cannot be represented by an unqualified percentage of ship size [B2-08, pp6–8]. Roussanaly et al. (2021) compare pressure, cargo capacity, logistics and conditioning, while Jeon et al. (2026) couple tank and cargo-handling dynamics to well-to-wake GHG intensity [B3-38, pp7–9; B3-29, pp4–10]. Additional voyage detail is therefore a modelling choice requiring a decision-relevant benefit, rather than a contribution in isolation.

Multi-period transport–storage emissions are likewise established. Fraga et al. (2024) combine post-capture conditioning, shipping, pipelines, hubs and wells in cost/GHG optimisation. Nöhl et al. (2025) compare prospective transport inventories and explicitly calculate cumulative carbon payback from switching infrastructure. A systematic review by Emborg et al. identifies inconsistent boundaries and omissions across CCS LCAs, reinforcing the need to disclose the denominator and included processes for every transferred factor [B2-12, pp5/18/20; B2-13, pp3–5; B3-27, p1].

Regional reservoir evidence suggests useful mechanisms to test, but does not yet establish a calibrated international case. Higashi-Niigata simulations predict pressure-limited injection and greater injected volume with pressure-relief wells, although the supplied figures do not expose the numerical vertical scales needed to recover absolute annual mass series. Malaysian studies demonstrate thermal pressure limits and pressure-management dependencies; an Australian South-West Hub model provides a conceptual reference configuration but excludes thermal stresses [B1-07, pp6–9; B1-08, pp7–10; B1-11, pp5–6; B1-12, pp18/21–22]. These are distinct sites and assumptions and cannot be combined into one purportedly verified sink.

More detailed dynamics need not always alter the result. Kolster et al. (2018) find limited long-horizon sensitivity to substantial multi-year injection-rate variations in the studied Bunter reservoir cases [B3-37, pp3–7]. A model-comparison study should allow this outcome and identify when a simpler representation is adequate.

The proposed research question is: under the same industrial service and no-CCS counterfactual, does jointly representing storage deliverability and operational shipping materially change the magnitude, sign or robustness of foreign-minus-domestic net mitigation? The intended contribution is the measured incremental value of the combined representation and the conditions under which it matters. The present review does not establish that this exact question is absent from all prior work.

The three objectives are retained from the proposal:

- Evaluate how injection capability, accessible cumulative storage and development timelines affect annual and cumulative storage under domestic and cross-border configurations.
- Quantify the effects of transport distance, flow, mode and infrastructure use on energy, lifecycle GHG burdens and emissions intensity.
- Determine when additional permanent storage enabled by cross-border transport outweighs the incremental lifecycle GHG burden.

## 2. Methods to implement

### 2.1 Common industrial service and boundaries
Select one named industrial source or explicitly defined cluster. Hold product output, source origin, eligible CO₂ supply, physical capture technology and no-CCS reference constant across domestic-only (D), foreign-only (F) and mixed (M) pathways. Separate technical capture potential from realised capture, which may be curtailed when downstream service is unavailable. A scenario permitting capture followed by venting must be declared and applied consistently rather than mixed with curtailment without explanation.

Use the proposal's 2030–2050 operating horizon with an explicit endpoint convention in the implementation. If all labelled calendar years are included, this means 21 annual bins from 2030-01-01 to 2051-01-01; an endpoint at 2050-01-01 would mean 20 bins and must not be silently substituted. Align published forecast dates to the chosen horizon without extrapolating unsupported site service. Declare the separate retention horizon and GHG characterisation metric.

Inventory incremental capture utilities, purification and conditioning, tanks and terminals, laden/return/port vessel operation, any pipeline segments, injection, pressure-management water handling, wells, relevant construction, monitoring and decommissioning. Record exclusions. Avoid allocating construction emissions both at installation and again through a per-tonne asset factor. Shore utilities require location/year factors; vessel power requires the applicable fuel/engine and upstream inventory. Background and foreground evolution must remain explicit.

### 2.2 Material balance and annual usable injection
For pathway s, let c(s,t) be captured mass, B(s,t) closing inventory, x(s,r,t) injected mass, v(s,t) captured-stream venting and l(s,t) other handling losses. Track uncaptured eligible source CO₂ separately as Q(t) − c(s,t). The annual balance is:

c(s,t) + B(s,t−1) = Σr x(s,r,t) + v(s,t) + l(s,t) + B(s,t).  (1)

Inventories include terminal, vessel and pipeline contents crossing an annual boundary. Their final fate must be stated. Material still buffered at the project endpoint cannot receive permanent-storage credit without a supported subsequent injection scenario and its emissions.

Use published site/year deliverability where available. A screening envelope can impose:

0 ≤ x(s,r,t) ≤ a(r,t) I(r,t);    Στ≤t x(s,r,τ) ≤ K(r).  (2)

I is the defined annual injection limit, a represents readiness/availability not already included in I, and K is accessible cumulative capacity allocated to the studied source. Avoid applying downtime twice. Where data support explicit physics, local injection pressure, thermal conditions, well counts and pressure interference constrain I. Average reservoir pressure below a fracture limit is insufficient to prove safe flowing bottomhole pressure.

Pressure-relief or brine-production cases require their own wells, pumping, treatment/disposal constraints, energy and CO₂ breakthrough fate. The enabling burden accompanies additional stored tonnes. A national prospective resource must not be substituted for K or I.

### 2.3 Voyage and terminal feasibility
Represent cargo mass capacity V(k) at the stated pressure, temperature, composition and density. Distinguish a trip loading fraction λ from tank heel and from annual fleet utilisation. Actual ship departures n are integer. For assigned marine mass M:

M(k,t) ≤ n(k,t) V(k) λ(k,t).  (3)

Round-trip time includes laden and return sailing, both port operations, and declared delay assumptions. For identical vessels on one route, N·floor(H/T_round) is a screening upper bound on completed annual voyages; the weaker aggregate vessel-hour condition alone can conceal calendar infeasibility. Short-period scheduling and port/buffer checks are required where binding. Seasonal weather data from another region are not transferred as local probabilities without justification.

Realised transported mass divided by technically achievable fleet capacity defines annual utilisation. Voyage loading, fleet utilisation, storage availability and source capture fraction are separate outputs. Zero-capacity cases return zero flow; ratios with zero denominators are undefined rather than reported as zero intensity.

### 2.4 BOG and cargo handling
Track liquid and vapor inventories, heat ingress, pressure and the selected management policy. Generated boil-off is not necessarily lost CO₂: recondensed gas remains cargo, retained heel remains inventory, and purge/venting reduces retained mass. Report their fates separately. A fixed boil-off generation specification must not be applied as a universal atmospheric-loss percentage.

Record the energy and recovery of liquefaction/purification for its actual inlet state. Model pressure-mismatch handling at source and destination, including vapor return, cooling/reliquefaction, pumping and heating as applicable. Cooling duty and electrical power are different quantities. Convert kW to kWh using a declared operating duration before dividing by mass. Keep unresolved source-unit corrections on hold.

### 2.5 Emissions and retention
The primary net-mitigation measure is the explicit common-reference difference:

A(s) = Σt [E0(t) − E(s,t)].  (4)

If each retained fossil-source tonne displaces one counterfactual emitted tonne and all other incremental burdens are accounted consistently, a useful reconciliation is:

A(s) = R(s) − Σt G(s,t).  (5)

This shortcut is conditional, not a universal treatment of biogenic CO₂, direct air capture, co-products or displaced utilities. Captured-source venting and leakage reduce R and must not also be added to G as the same source CO₂. Upstream fuel GHG, methane, N₂O and other incremental effects remain in G. For material delayed leakage, use a retention stock/flow model with a declared accounting horizon.

For voyage j, operating fuel can be represented by state-specific fuel rates and durations:

F(j) = f_laden(j) τ_laden(j) + f_return(j) τ_return(j) + f_port(j) τ_port(j).  (6)

Add auxiliary cargo-handling energy with its correct generation factor unless already included in F or a combined inventory. A reported well-to-wake factor already includes its upstream component. Factor values drawn from different engines or fuel pathways must not be averaged as though they were interchangeable.

Report captured, transported, injected and retained mass; absolute GHG and net mitigation; transport intensity; and mitigation per captured tonne side by side. A lower per-tonne transport intensity does not establish higher absolute avoided emissions.

### 2.6 Model-comparison design
B0 uses constant injection screening and a fixed transport factor. B1 adds annual storage deliverability. B2 uses the same static storage representation as B0 and adds operational shipping/terminals. B3 combines the dynamic storage and operational transport representations.

Specify the static proxy before seeing results: nameplate, annual-average and cumulative-delivery-preserving alternatives answer different questions. Use controls to separate commissioning effects from changing post-commissioning injection. Calibrate the fixed transport factor at a stated reference flow/state and use one consistent boundary across variants.

Let D(j) = A(F,j) − A(D,j). Report:

Full representation contrast = D(B3) − D(B0).  (7)
Deliverability contrast = D(B1) − D(B0).  (8)
Operations contrast = D(B2) − D(B0).  (9)
Two-factor interaction = D(B3) − D(B2) − D(B1) + D(B0).  (10)

Do not call the full contrast an interaction. If a simplified model selects a different route or fleet design, evaluate that selected decision again under the common detailed feasibility/accounting model before attributing a realised climate benefit to the change. Report infeasible selections explicitly. A null interaction or robust unchanged ranking remains an informative result.

### 2.7 Break-even, controls and uncertainty
The foreign-minus-domestic advantage is:

ΔA = A(F) − A(D).  (11)

Under Equation (5)'s assumptions, ΔA = ΔR − ΔG; the break-even set satisfies ΔR = ΔG. Map the frontier over storage service, readiness, distance, vessel design, utilisation and energy factors. Discrete voyages, fleets and infrastructure can produce multiple thresholds; do not assume one universal break-even distance.

Run a feasible equal-cumulative-retention control to separate additional-storage benefit from route burdens, while still reporting differing timing and capture utilities. Then allow unequal deliverability. Assess mixed allocation using a declared share grid or objective with the same constraints; mixed storage is not presumed superior.

Use defensible deterministic ranges and structural scenarios initially. Published case minima/maxima are not probability distributions. Estimate a probability of foreign benefit only if marginal distributions, correlations and scenario weights are supported. Include a low-sensitivity reservoir case informed by Kolster et al., pressure-management cases, energy-background evolution, alternative end-inventory fates and construction allocation.

### 2.8 Validation and traceability
Check annual/subannual material balances, injection/capacity/pressure constraints, integer-voyage calendars, port and buffer feasibility, zero-throughput cases and the emissions reconciliation. Validate subprocesses against compatible literature cases: stochastic shipping with Bjerketvedt, pressure/conditioning cases with Roussanaly, post-capture inventory components with Fraga, and reservoir temporal sensitivity with Kolster. A match to one component is not validation of the regional chain.

Every input requires original unit, source page/table, value type, feed/operating state, country/site, applicable year, denominator, inventory boundary and uncertainty. Data marked HOLD are excluded from the calibrated base case. Commercial access, permits and terminal compatibility are feasibility conditions requiring separate current evidence; historical governance papers do not prove them.

## 3. Prospective case study
First implement a controlled common-source domestic–foreign pair. Use Japan–Malaysia and Japan–Australia as prospective applications only after source/sink evidence passes the data requirements. Higashi-Niigata remains a candidate requiring numerical profiles; no supplied anonymised Malaysian case or conceptual Australian programme is treated as an available contracted sink. Narrowing to one defensible pair is preferable to inventing comparable data for three countries.

Prepare an input table grouped by source, reservoir service, route/vessels, terminal/process energy, emissions factors, assets and retention. Label verified site observations, published scenario inputs, calibrated model parameters and analyst assumptions separately. The evidence workbook is the provenance layer, not a ready-to-run harmonised parameter file.

## 4. Planned results — intentionally unpopulated
Table1: closest-prior-work comparison and proposed testable distinction. Table2: traceable case inputs with quality labels. Table3: route and fleet constraints. Table4: B0–B3 absolute mass/GHG results and contrasts. Table5: equal-retention control and robustness outcomes.

Figure1: system boundary and material flows. Figure2: annual source supply and usable sink service. Figure3: utilisation versus absolute and unit shipping emissions. Figure4: break-even regions. Figure5: main and interaction contrasts. Figure6: robustness and where simplified screening is adequate.

No study should be described as proving a preferred Japanese export destination until feasible schedules, traceable parameters and reproducible numerical results exist.

## 5. Discussion and limitations to test
Discuss whether differences arise from additional storage, capture curtailment, fleet thresholds, conditioning, reservoir pressure management or future energy supply. Separate economic contextual results from climate objectives. Report source-specific unit errors and excluded data rather than incorporating presumed repairs. Distinguish resource availability from injection service and geological injection from permanence. The present literature intake includes abstract-level screens and targeted extractions, not an exhaustive systematic review of every numerical inventory or supplement. The proposed novelty remains to be tested, including against the unsupplied Budiarto et al. 2025 paper.

## Selected references and local source IDs
- Wang et al. 2016. Effects of pipeline distance, injectivity and capacity on CO₂ pipeline and storage site selection. DOI 10.1016/j.ijggc.2016.05.006. [B2-01]
- Bjerketvedt, Tomasgard & Roussanaly 2020. Optimal design and cost of ship-based CO₂ transport under uncertainties and fluctuations. DOI 10.1016/j.ijggc.2020.103190. [B2-08]
- Fraga et al. 2024. Multi-period, multi-objective optimisation of the Northern Lights and Stella Maris carbon capture and storage chains. DOI 10.1016/j.ccst.2024.100190. [B2-12]
- Nöhl et al. 2025. How to transport carbon dioxide with minimal environmental impacts today and tomorrow? DOI 10.1016/j.jclepro.2025.145659. [B2-13]
- Bertoni et al. 2025. Optimizing carbon capture and storage infrastructure including physics-based reservoir modelling. DOI 10.1016/j.compchemeng.2025.109293. [B2-04]
- Gidden et al. 2025. A prudent planetary limit for geologic carbon storage. DOI 10.1038/s41586-025-09423-y. [B2-18]
- Ooi et al. 2013. Planning of carbon capture and storage with pinch analysis techniques. DOI 10.1016/j.cherd.2013.04.007. [B3-11]
- Lee, Tan & Chen 2014. A unified model for the deployment of carbon capture and storage. DOI 10.1016/j.apenergy.2014.01.080. [B3-14]
- Emborg et al. 2026. Life cycle assessment of carbon capture and storage value chains: a systematic, critical literature review. DOI 10.1016/j.spc.2025.09.015. [B3-27]
- Jeon et al. 2026. Integrated modelling and simulation of liquefied CO₂ tank and cargo handling system with new marine transportation greenhouse gas intensity. DOI 10.1016/j.energy.2025.139624. [B3-29]
- Roussanaly et al. 2014. Benchmarking of CO₂ transport technologies: PartII—Offshore pipeline and shipping to an offshore site. DOI 10.1016/j.ijggc.2014.06.019. [B3-36]
- Kolster et al. 2018. The impact of time-varying CO₂ injection rate on large scale storage in the UK Bunter Sandstone. DOI 10.1016/j.ijggc.2017.10.011. [B3-37]
- Roussanaly et al. 2021. At what pressure shall CO₂ be transported by ship? DOI 10.3390/en14185635. [B3-38]
- Johnsson et al. 2017. Linking the effect of reservoir injectivity and CO₂ transport logistics in the Nordic region. DOI 10.1016/j.egypro.2017.03.1824. [B3-39]
- Becattini et al. 2022. Carbon dioxide capture, transport and storage supply chains: optimal economic and environmental performance of infrastructure rollout. DOI 10.1016/j.ijggc.2022.103635. [B3-42]

Complete supplied-PDF titles, source paths, identifiers and reading stages are in Master library. Journal issue years are retained where they differ from DOI/online-publication years. Citation formatting and the final bibliography should be standardised after source and manuscript scope are finalised.
