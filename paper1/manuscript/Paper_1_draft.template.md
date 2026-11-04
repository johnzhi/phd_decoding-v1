---
title: 'Dynamic carbon break-even analysis of domestic and cross-border CO₂ storage: an evidence-constrained framework and published-case benchmarks'
subtitle: 'Paper 1 — research draft v3, operational proxy model'
date: '4 November 2026'
lang: en-GB
---

**Draft status.** B0–B3 have now been implemented for a common-source, aggregate-service proxy and event-based shipping model. The model reports injected mass, inventories, ship-combustion CO₂ and the conditional allowance for uninventoried differential burdens. Complete lifecycle net avoided GHG is not computed. The supplied Indonesian allocations and published ship designs are scenario inputs, not measured Japanese geology or available international routes. Source/figure/table locators, structural scheduling conventions and missing quantities are explicit. Author names, affiliations and target-journal formatting remain to be supplied.

# Abstract

Cross-border CO₂ storage can enable additional injection when local service is constrained, but transport scheduling and incomplete emissions accounting can change the comparison. This study develops a source-traceable dynamic proxy model using supplied published evidence. Four variants combine static or annual aggregate storage-service proxies with fixed-factor or event-based shipping. The model tracks capture curtailment, integer fleets, port operations, source/destination buffers, initial heel and uncredited endpoint inventory over the original thirty nominal annual bins. Published shipping inputs reproduce all 75 reported fleet cases. However, that annual capacity calculation does not establish detailed scheduling feasibility: under the declared staggered-calendar proxy, a lower-service 1,000 km case needs three rather than two vessels to meet a transferred 99%-of-reference design criterion. Equal-injection and additional-vessel controls distinguish transport penalties from additional throughput. After fleet-adequacy control, the conditional allowance for uninventoried differential burdens is approximately +1.281 Mt at 5,000 km and −4.923 Mt at 10,000 km relative to the lower-service 1,000 km proxy. Calendar and fleet choices can change the sign, so no robust destination preference follows. Capture energy, upstream fuel, actual process duty, injection/assets and retention remain unquantified. The results establish a reproducible feasibility and accounting test, rather than complete regional lifecycle mitigation or independently calibrated reservoir performance.

**Keywords:** geological CO₂ storage; source–sink matching; deliverability; shipping; lifecycle accounting; carbon break-even; reproducible research.

# 1. Introduction

The amount of CO₂ that can be stored in principle is different from the amount an industrial source can inject at a particular time. Reservoir pressure, well development, commissioning, temperature and water handling can restrict usable storage service even where a large prospective resource is reported. For domestic and foreign pathways, the relevant climate comparison therefore concerns the CO₂ retained and the additional greenhouse gas emissions incurred in enabling that retention. Storage resource or transport distance alone cannot resolve this comparison.

Regional screening illustrates the distinction. Zhang and Lau identify 391 Mt/y of stationary emissions within a 1,000 km radius of Singapore and mid storage resources of 0.5 Gt in oil reservoirs, 6.2 Gt in gas reservoirs and 379 Gt in saline aquifers. Arun is a named gas-condensate candidate with a reported 1.3 Gt resource. These estimates identify candidates; they do not supply annual injection service, a commercial allocation or a commissioning schedule [B4-08, p1]. National Malaysian power-sector analysis similarly provides decarbonisation context rather than a matched Japanese industrial-source inventory [B4-01, p1].

The relation between transport and storage characteristics is already established in infrastructure research. Wang et al. examine how distance, injectivity and capacity affect pipeline and sink selection. Nordic studies show that a longer shipping route to a reservoir with favourable injectivity can be economically attractive [B2-01, pp3–5; B3-39, p1; B3-33, p1]. An economic preference, however, does not itself demonstrate greater net climate mitigation. Capture curtailment, route emissions, additional wells and differences in the reference industrial service must also be considered.

Temporal infrastructure planning also has substantial prior coverage. Ooi et al. incorporate source and sink timing, injection rates and capacities using pinch analysis. Lee et al. combine capture retrofits, time-dependent constraints and compensatory power. Becattini et al. optimise yearly infrastructure rollout over a 25-year horizon, including overseas storage, a delayed hypothetical domestic sink and emissions relative to business as usual [B3-11, p1; B3-14, p1; B3-42, pp1–7,15–16]. Bertoni et al. incorporate reservoir physics in infrastructure optimisation [B2-04, pp1,9–10]. Consequently, neither a dynamic deployment model nor a common-reference emissions comparison should be claimed as the first contribution of Paper 1.

The newly supplied South Sumatra study further narrows the gap. Budiarto et al. combine reservoir availability, well-derived injection limits and multi-period source–sink optimisation. Their single- and multi-well configurations produce different cumulative storage outcomes [B4-06, pp8–10,16]. Gabrielli et al. also consider costs, emissions and the ability to store captured carbon under infrastructure failures, including domestic and foreign storage configurations [B4-07, p1]. Additional retention from better storage service is therefore an established mechanism rather than a novel premise.

Operational transport and lifecycle modelling are likewise well developed. Bjerketvedt et al. connect uncertain weather, vessel operation and buffers to transport completion and expected cost. Roussanaly et al. compare pressure, conditioning and ship design; Jeon et al. couple tank and cargo-handling dynamics to marine GHG intensity. Fraga et al. integrate a prospective post-capture inventory with multi-period cost/GHG optimisation, and Nöhl et al. evaluate cumulative carbon payback from changing transport infrastructure [B2-08, pp6–8; B3-38, pp7–9; B3-29, pp4–10; B2-12, pp5–18; B2-13, pp3–5]. More operational detail is thus a modelling choice whose decision value requires evaluation.

A narrower question remains useful: under a common industrial-production counterfactual, when does jointly resolving annual storage deliverability and operational shipping change the magnitude, sign or robustness of the difference between domestic and foreign mitigation? This question allows an unchanged ranking or small interaction. Kolster et al., for example, find limited long-horizon sensitivity to substantial multi-year injection-rate variation in the studied Bunter cases [B3-37, pp3–7]. A model-comparison study should retain such a null-effect benchmark.

This draft makes three present contributions. First, it creates a page-located evidence register that distinguishes observations, published model inputs, published outputs and calculations. Second, it quantifies selected storage, pressure, conditioning, buffer and BOG benchmarks without synthesising unsupported annual profiles. Third, it derives a transparent proxy score and shows why converting that score into net avoided emissions requires further mass and inventory reconciliation. It then specifies the controlled annual model comparison needed for a regional extension. The exact absence of this model-comparison question from all prior literature is not asserted by the supplied-library review.

# 2. Evidence and methods

## 2.1 Library, extraction and scope

The retained library contains 93 PDF files representing 92 unique publications and 1,301 physical pages across the unique publications. The two supplied versions of the source–sink matching review B2-17/B3-46 are counted once as a publication and retained as separate files. Previously downloaded originals are reused for same-title reuploads; binary equivalence of every reupload has not been established. The retained PDFs and the supplementary DOCX, identified by SHA256, define the evidence used here. The DOCX belongs to B4-06 and is not counted as a new publication or PDF.

Targeted methods/results extraction covers 48 unique publications. Another 44 have abstract/relevance screening, so the review is a purposive synthesis of supplied materials rather than an exhaustive systematic review. The ledger contains 1,642 extracted records, including ranges and grouped cases. This number is not a count of independent observations. The Google Drive folder and oversized planetary-limit ZIP were not ingested; the standalone planetary-limit PDF is included. No uninspected contents are represented as evidence.

A separate curated PDF table records 250 atomic quantities, their original units, physical page/table, scenario, evidence type, inventory boundary and transfer limits. A 134-row subset enters the present analysis: 59 quantities support 49 calculations, and 75 entries preserve the published large-ship fleet table. An additional 352 numeric supplementary records comprise 102 native-table entries and 250 one-decimal annual allocation annotations. The full 720-cell figure grid preserves its 470 blanks separately. The annual reconstruction uses these supplementary tables and annotations in a dedicated pipeline. A dedicated 30-row operational-parameter register additionally locates every shipping/fuel/design quantity used by the new model; these quantities overlap the ledger and are not independent observations. The broad extraction ledger is not a ready-to-run harmonised input file. Values marked HOLD and context-only quantities cannot enter the calculation script. The source audit records 43 unresolved or consequential interpretation issues; an issue can remain open where the affected data are excluded from the calculation.

The calculations preserve original denominators. Unit conversions and algebraic definitions are distinguished from empirical inputs. Published minima and maxima are not treated as probability distributions. No cost factor is converted into GHG, no national resource is assigned as a source's annual allocation, and no missing graph scale is filled with an assumed value. Reported numbers retain their source precision even where machine-readable outputs carry additional computational decimals.

## 2.2 Selecting source and sink evidence

The intended Japan–Malaysia–Australia application is screened against the data required for an implementable model, rather than treated as a fixed set of available services. Higashi-Niigata is a named Japanese candidate with history-matched reservoir forecasts. Its pressure-relief case reports approximately 25–30% greater injection volume, but the supplied figures do not provide recoverable numerical vertical scales for complete absolute annual mass series [B1-07, pp6–9]. Assigning an arbitrary Mt/y scale would therefore be unsupported.

Malaysian Field X studies provide pressure constraints and thermal mechanisms but are anonymised; the studies cannot be assumed to describe one contracted storage service [B1-09, p13; B1-11, pp5–6]. The South-West Hub model supplies an Australian conceptual reference while excluding thermal stresses, so it cannot simply be combined with Malaysian thermal limits as a calibrated Australian sink [B1-12, pp18,21–22]. Regional resources and historical governance assessments do not establish present storage access.

The user authorised explicitly disclosed geographic proxies when local data are unavailable. The present numerical draft therefore selects the internally coherent South Sumatra single- versus multi-well outcomes as the storage-service benchmark. It uses published Norwegian post-capture GHG outcomes as separate burden scenarios. These substitutions test accounting sensitivity; they do not make Indonesian geology Japanese, or Norwegian energy factors applicable to an Asian route. No African dataset is introduced merely because a geographic proxy is permitted.

| Required component | Evidence selected | Role | Remaining transfer limit |
|---|---|---|---|
| Common source–sink storage comparison | Budiarto B4-06, p16 | Published lower/higher cumulative storage | Indonesian industrial system; annual allocation figures now supplied, but exact physical rate-constraint arrays remain unavailable |
| Post-capture burden scenarios | Fraga B2-12, pp18,20 | Reported GHG intensity scenarios | Different country/network portfolios; includes fugitives |
| Feed/pressure conditioning | Roussanaly B3-38, p7 Table 3 | Within-feed process comparison | Different inlet states cannot be pooled as one uncertainty range |
| Thermal pressure constraint | Tan B1-11, pp5–6 Tables 2–3 | Within-seal pressure sensitivity | Analytical field-specific ceiling, not an annual rate factor |
| Buffer and transport completion | Bjerketvedt B2-08, pp7–8 | Denominator and completion benchmark | Original route/weather assumptions |
| BOG process emissions | Jeong B1-19, p7 Table 6; p13 Table A6 | Partial-process intensity | Excludes full propulsion/upstream chain |
| Large-ship fleet counts | Noh and Kang B4-09, p6 Table 7 | Published integer fleet outputs | Density discrepancy prevents independent reconstruction |

## 2.3 Published-case calculations

The thermal benchmark compares the same seal under isothermal conditions and estimated cooling. For each seal, the pressure-ceiling reduction is the printed isothermal ceiling minus the printed cooled ceiling, divided by the former when expressed as a percentage. This percentage describes the stated pressure ceiling, not pressure headroom above initial reservoir pressure, and not an injection-rate reduction. Original psi labels are retained because pressure datums are not sufficiently clear to justify further conversion [B1-11, pp5–6].

Conditioning comparisons use four electricity requirements from the same source table: pure feed and pressurised inland feed, each at 7 and 15 barg. Differences are calculated within each feed case; pure-to-inland ratios are descriptive comparisons of different inlet conditions [B3-38, p7 Table 3]. No electricity emission factor is added, because a compatible regional/year background has not been selected.

Buffer ratios divide the reported buffer by the 5,000 t ship capacity. The 99% and 100% transport-completion cases are kept separate. The paper's use of average-cycle captured mass as another denominator is not relabelled as ship capacity [B2-08, pp7–8].

For the BOG benchmark, annual purge-plus-auxiliary-generation CO₂ from Table 6 is divided by transported mass from Table A6 for the same process and impurity case. Emissions are in t/y and mass in thousands of t/y; the resulting numerical ratio is kgCO₂/t transported. These are partial-process CO₂ intensities. They are neither full lifecycle CO₂e factors nor fractions of cargo necessarily lost to atmosphere [B1-19, pp7,13].

The large-ship source prints 1,154 kg/m³ in Table 1 and 1.1546 kg/m³ in the fleet-method prose. The operational scenario explicitly selects Table 1: together with the other printed inputs it reproduces all 75 fleet counts in Table 7. The inconsistent prose is not repaired or used. This arithmetic validation supports the declared Table 1 scenario but does not independently validate fluid properties [B4-09, pp3,5–6].

The Budiarto supplement adds three native tables and ten embedded figures [B4-06-S1]. Tables S1–S3 are extracted directly from DOCX cells; no OCR is needed for their 102 numeric entries. Figures S8–S10 provide annual MILP allocation heatmaps for 2027–2056. All 250 printed one-decimal annotations are transcribed with reservoir/year and image-cell locators. The 470 blank cells retain a distinct status. For reconstruction, totals sum the printed allocations, interpreting a blank as no reported allocation rather than a measured physical zero. Automated cell-occupancy and approximate colour checks support visual annotation review; colour-derived precision is not used in calculations.

The annotated heatmaps are outputs mr,t selected by the original optimisation, whereas the main paper's kr,t denotes the physical annual injection upper bound [B4-06, p9]. Substituting the former for the latter would predetermine aspects of the reconstructed solution. The present annual replay therefore checks the published outputs, readiness dates and cumulative totals; it does not reproduce the original MILP or independently identify a feasible maximum service profile. Figures S1–S7 relate pressure to rate/storage efficiency and are retained without claiming that they supply a complete numerical calendar-time constraint array.

The display-resolution audit assumes conventional rounding to the nearest 0.1 Mt/y. For n annotated cells, the conditional sum envelope is the printed sum ±0.05n Mt over one-year bins. This is a bound derived from the printed precision, conditional on the rounding convention and blank interpretation, rather than a confidence interval. Values are not scaled to force agreement with the main paper. Rounded annual sums can slightly exceed the nominal source rate; that alone is not evidence of physical excess injection.

## 2.4 Mitigation accounting and a deliberately bounded proxy score

For an actual pathway s under common industrial production, net avoided GHG is defined by an explicit no-CCS counterfactual:

$$A_s=\sum_t(E_{0,t}-E_{s,t}). \tag{1}$$

Under a fossil-source counterfactual where each retained tonne displaces one emitted tonne and all additional burdens are consistently counted, this can be reconciled as retained source CO₂ minus additional lifecycle GHG. Captured-source CO₂ vented or leaked must reduce retained mass; it must not also be subtracted as the same source loss within additional GHG. Upstream fuel methane and other incremental emissions remain additional burdens. Biogenic sources, direct air capture, displacement and co-products require their own counterfactual treatment.

The selected published aggregate GHG factors do not yet permit this reconciliation. Fraga's reported post-capture inventory includes fugitive emissions associated with intermediate facilities, transport and injection, as well as energy and construction terms [B2-12, pp8,16–18,23]. The Budiarto outcome is reported CO₂ stored. Combining these without separating source-loss terms can double-count a loss. The present cross-study quantity is therefore defined as a **reported-burden score**, not net avoided emissions:

$$S_i=R_i\left(1-\frac{e_i^{\mathrm{rep}}}{1000}\right), \tag{2}$$

where R is published cumulative stored mass and the reported intensity is in kgCO₂e/t stored. The factor 1,000 converts kilograms to tonnes; it is a unit definition. Equation (2) is an accounting diagnostic constructed from two published datasets. It is not claimed as an empirical result in either source.

For a lower-storage reference L and higher-storage case H, score equality gives:

$$\frac{R_H}{R_L}=\frac{1-e_L^{\mathrm{rep}}/1000}{1-e_H^{\mathrm{rep}}/1000}. \tag{3}$$

Equivalently, the reported-intensity crossing for a given storage ratio is:

$$e_{H,*}^{\mathrm{rep}}=1000\left[1-\frac{R_L}{R_H}\left(1-\frac{e_L^{\mathrm{rep}}}{1000}\right)\right]. \tag{4}$$

These are score crossings. To obtain a physical mitigation comparison, let Linc be captured-source losses already included in reported GWP and also deducted in the retained-mass accounting, and let Gom be additional GHG omitted from the adopted reported factor. After a compatible fossil-source and mass reconciliation:

$$\Delta A=\Delta S+\Delta L_{\mathrm{inc}}-\Delta G_{\mathrm{om}}. \tag{5}$$

The correction may also require revising R if the source's “stored” quantity actually denotes injection without the required retention adjustment. Neither correction is assigned an invented value here. Additional capture utilities, extra well development and pressure-management burdens are examples requiring evidence. Thus a positive score is insufficient to establish positive whole-chain mitigation advantage.

The proxy uses the published single-well SW-A storage outcome for L and the multi-well MW-A outcome for H. The lowest of the six reported Fraga best-solution intensities, Northern Lights at 0.7 MPa, is selected as a transparent reference. This is a normalisation choice, not a claim that the configuration is available domestically or is optimal in another region. Each of the six published outcomes is assigned to H in turn. No unreported intermediate GHG value is sampled and no probability is attached to a scenario.

## 2.5 Reproducibility and checks

Every calculation output records its input IDs, formula, unit and boundary. The repository validates retained PDF hashes, page-text counts, numeric source-token locators and calculation eligibility; these checks establish file identity and traceability rather than the scientific validity of a paper's model. Table mapping for the selected datasets is checked against the retained source pages. The analysis has no fitted reservoir parameters, random draws or fabricated annual injection series. The operational model adds explicitly declared fleet, berth, availability-window and dispatch structures; these are model design conventions, not observed local data. Tests check the threshold identity, unit scaling, zero-difference reference case, HOLD exclusion and provenance closure. Figures are generated from the same registered inputs/results.

## 2.6 Implemented operational proxy model

The present numerical extension uses the original thirty nominal 8,760-hour bins labelled 2027–2056 and a constant 5.327 Mt/y study-defined source flow. Actual Gregorian leap-year timing is not asserted. The lower/higher-service alternatives use SW-A/MW-A allocation sums as exogenous annual envelopes. Two static controls are derived from the same values: a constant whole-horizon mean and reservoir-specific post-readiness means. Each preserves the nominal cumulative rounded allocation total before applying the common source/transport constraints. These transformations do not establish independent physical injection limits.

B0/B1 use a fixed ship-fuel factor calibrated at full source flow, including the integer last voyage. B2/B3 use continuous-time events for loading, outbound movement, unloading and return. Cargo is assigned at loading start and received at unloading end. One loading berth and one receiving berth are declared structures. Published vessel volumes, fuel rates, port durations, speed, fill/heel fractions, terminal size and operating hours are used [B4-09, pp3,5–7]. The marine initial heel is charged from captured source CO₂; captured mass equals injected mass plus export, import and marine inventories. Source capture is curtailed at export-buffer capacity. Endpoint stocks are not credited as injected or permanently retained.

Published 8,000-hour annual availability is placed either in evenly staggered vessel windows or synchronised windows. Each active phase must finish within its window; a full nominal round trip must fit when loading begins. This is a conservative deterministic dispatch convention, not an observed weather calendar or an optimal schedule. Within each annual bin, capture potential and the proxy injection rate are constant. Injection cannot exceed available import inventory. Waiting fuel, actual BOG behaviour and leakage processes lack compatible inputs and are not simulated as measured quantities.

The reference fleet uses the source's integer annual-capacity formula. That design is held fixed through the thirty bins and checked in the detailed model. Equal-injection controls rerun both paths at the smaller baseline injected quantity, retaining uncredited residual inventory. An added-vessel control perturbs each fleet by one vessel. A restricted design search then selects the minimum added fleet beyond the reference reaching 99% of the continuous, no-inventory service reference. The percentage is transferred from a published transport-completion criterion [B2-08, p7], with its changed denominator explicitly declared; it is not a reliability probability or a cost-optimal fleet.

The directly inventoried component is active-cycle fuel-combustion CO₂. A published 3.206 tCO₂/t MGO factor is transferred to the source's MDO fuel-rate scenario [B1-19, p4; B4-09, pp5,7]. This does not provide upstream/non-CO₂ fuel GHG or idle/hotel fuel. An optional separate scenario applies published compressor nameplate power for 8,000 h/y with a published generator SFOC of 197.5 g/kWh; it is a costing-duty envelope, not a prediction of actual BOG load. The source's ambiguously LHV-labelled 0.084 kg/kWh value is not used.

Let U contain all uninventoried differential burdens, including any retention reconciliation needed when injected mass is used as a source-carbon proxy. The implemented climate-related output is:

$$H=\Delta R_{\mathrm{injected}}-\Delta G_{\mathrm{ship,CO2}},\qquad \Delta A=H-\Delta U. \tag{7}$$

The second equality is conditional on a compatible fossil-source counterfactual and consistent retention/loss treatment. A positive full advantage requires ΔU < H; ΔU is not assigned zero. Negative H alone cannot prove a full disadvantage if omitted differential terms favour that pathway. The complete net-avoided-GHG output remains empty. The earlier Fraga reported-burden score is retained as a supporting accounting audit and is not a parameter in this operational model.

The grid contains three source vessel sizes, five published higher-service distances, two static proxy definitions and the four variants. Additional calendar and rounding cases produce 144 comparisons and 36 contrasts. The two-factor interaction is calculated separately from the full B3-minus-B0 contrast. No geographic service availability, calibrated reservoir physics, mixed-network optimum or complete lifecycle inventory is inferred from this exercise.

# 3. Results

## 3.1 Published storage improvement is not a complete mitigation gain

The South Sumatra model reports 153.21 Mt stored for SW-A and 159.81 Mt for the multi-well cases. Their difference is **6.60 Mt**, or **4.31%** relative to SW-A. The study attributes the lower single-well storage to early injection-capacity limitations; this is a coherent published example of storage deliverability affecting cumulative capture/storage outcomes [B4-06, p16]. It is a simulated design result, not a measured field response.

The paper reports costs around USD17.53 billion for SW-A and around USD18 billion for the multi-well cases, with capture dominating chain cost [B4-06, p16]. Those economic values cannot supply the GHG of additional wells or pressure management. The two cumulative outcomes alone do not determine an annual injection profile; the now-supplied supplementary heatmaps provide a rounded allocation reconstruction. The increase establishes the magnitude of a published gross-storage effect and the associated data need; it does not establish a 6.60 Mt net GHG benefit or a Japanese domestic/export difference.

Tables S1–S3 establish a more complete common-source benchmark. Fourteen source rates sum to **5.327 Mt/y**, giving **159.81 Mt** across the original 30 annual bins, exactly matching the reported multi-well cumulative total. Eight candidate reservoirs have a summed model resource of **537.4 Mt**, with estimated start years from 2027 to 2039, and the network table provides 46 numeric hub distances. The resource sum is not an annual injection capacity or proof of available commercial storage. Source capture costs are not converted into capture GHG.

{{SUPPLEMENT_PARAMETER_TABLE}}

Replaying the printed annual cells gives the following cumulative totals. Differences from the main paper are preserved. Each reported main-paper total lies within the conditional worst-case envelope implied by its one-decimal annotations; this establishes compatibility with rounding, not exact reproduction. No annotated injection occurs before the corresponding Table S2 estimated readiness year.

{{ANNUAL_REPLAY_TABLE}}

![Annual and cumulative sums reconstructed from Budiarto supplementary Figures S8–S10. Each input is a printed one-decimal allocation. Blanks remain identified as no reported allocation; no interpolation or endpoint scaling is applied. The source-rate reference is the Table S1 sum. These are replayed published outputs, not new optimisation results or physical maximum service curves.](../outputs/figures/supplement_annual_replay.png)

The main paper defines source mass ms,t as captured CO₂ in its network mass balance [B4-06, p9]. Applying the stated capture-efficiency target again to Table S1's study-defined flow would change that quantity without support. A separate capture-energy and emissions inventory remains necessary for whole-chain accounting.

## 3.2 Operational results and design controls

Tabled results below use the 40,000 m³ design, aggregate-mean static control and staggered availability convention. They are model calculations from located inputs and declared structures. The raw reference-fleet B3 result at 10,000 km gives a positive allowance even where B0 is negative. The contrast cannot be attributed solely to geology: fleet/availability constraints also reduce the lower-service route's realised injection.

{{OPERATIONAL_COMPARISON_TABLE}}

![Four-variant comparison under the declared reference-fleet and staggered-calendar conventions. The ordinate is additional injected mass minus additional active-cycle ship-combustion CO₂; it is the allowance for uninventoried differential burdens, not complete avoided GHG. Non-monotonicity reflects integer fleet sizing and dispatch constraints. Lines connect the five scenario points and do not identify a continuous break-even frontier.](../outputs/figures/operational_allowance.png)

For the lower-service 1,000 km proxy, the annual source-model formula gives two ships. The detailed simulation reaches about 93.3% of the continuous no-inventory reference under the selected window/berth/buffer conventions. The restricted 99%-of-reference design control therefore selects three. The higher-service 10,000 km case similarly changes from thirteen to fourteen vessels. These are model-dependent design decisions, not evidence that actual ports require those fleets.

{{OPERATIONAL_DESIGN_TABLE}}

With that design control, the higher-minus-lower conditional allowance is approximately +1.281 Mt at 5,000 km and −4.923 Mt at 10,000 km. A full climate interpretation requires the unknown ΔU in Equation (7), including extra capture, upstream fuel, terminals, injection/assets and retention. No universal break-even distance is identified between these two scenario points.

The equal-injection control gives no additional injected benefit and additional ship-combustion penalties of approximately 4.385 and 9.865 Mt at 5,000 and 10,000 km. The one-added-vessel control changes the sign of the raw 10,000 km comparison. At 5,000 km, synchronising instead of staggering the same published availability duration changes the raw B3 allowance from about +11.514 to −2.625 Mt. Calendar placement is unsupported by local observations, so these are structural sensitivities rather than probabilities or preferred forecasts.

{{OPERATIONAL_CONTROL_TABLE}}

![Controls for the 40,000 m³ operational proxy. Left: adding one vessel to each route. Right: changing the placement of the same annual availability duration. Sign changes expose design/calendar sensitivity. Missing lifecycle terms remain outside every plotted value.](../outputs/figures/operational_controls.png)

For the reference fleet and aggregate-mean proxy, the full B3-minus-B0 allowance contrast at 5,000 km is about 9.945 Mt, while the two-factor interaction is about 0.293 Mt. At 10,000 km the corresponding values are 7.078 and 0.629 Mt. The full representation contrast is therefore not interchangeable with an interaction or a realised climate benefit. Re-evaluating fleet adequacy and omitted inventories is necessary before selecting a pathway.

## 3.3 Thermal and conditioning benchmarks

The four paired thermal cases show pressure-ceiling reductions of 521–525 psi, corresponding to 14.13–24.20% of their respective isothermal ceilings. The similar absolute changes produce different percentages because the starting ceilings differ. Transferring one percentage to another reservoir's injection rate would therefore lose both the physical quantity and the field context.

{{THERMAL_TABLE}}

![Published thermal pressure ceilings. Source: Tan et al., B1-11, physical pp5–6, Tables 2–3. These are analytical pressure results for four seals; the figure does not show injection rates or storage capacities.](../outputs/figures/thermal_pressure.png)

For pure feed, the 7/15 barg conditioning requirements are 96.3/90.4 kWh/t. For the pressurised inland-feed cases they are 17.4/9.0 kWh/t [B3-38, p7 Table 3]. The calculated within-feed differences are 5.9 and 8.4 kWh/t, respectively. Expressed relative to the 7 barg value, these are 6.13% and 48.28%. The pure-to-inland ratios at the same shipping pressure are 5.53 and 10.04. These comparisons show why a pressure choice cannot be evaluated without its inlet boundary; they do not show a universal shipping-energy saving.

![Conditioning electricity by feed and shipping pressure. Source: Roussanaly et al., B3-38, p7 Table 3. Different feeds have different inlet pressure conditions. Electricity is not converted to regional GHG.](../outputs/figures/liquefaction_feed_pressure.png)

## 3.4 Buffer, process-emissions and fleet benchmarks

The 99% transport-completion buffer of 5,120 t is **102.4%** of the 5,000 t ship capacity. The 100% completion buffer of 5,890 t is **117.8%** of ship capacity [B2-08, pp7–8]. An approximately 118% figure in the 99% case refers instead to average-cycle captured mass. A percentage without its denominator and completion requirement is therefore not a transferable design parameter.

The terminal literature reinforces this dependence on design and operating conditions. Seo et al. find an optimal temporary tank volume equal to the 11,801 m³ ship volume for their Korean case, which excludes unforeseen well/reservoir malfunctions [B4-02, pp3,8]. Zahid et al. model terminal loading, holding, unloading and emergency shutdown, including vapor return and BOG recycling [B4-03, pp1,3,9]. These results cannot be combined into a universal tank-to-ship ratio or a Japanese weather distribution.

Across the 18 paired Jeong cases, calculated purge-plus-auxiliary-generation intensity spans **1.27–21.25 kgCO₂/t transported**. The variation reflects different pressure/process and nitrogen cases, not repeated observations of one chain. The complete case matrix is provided below to preserve the pairing rather than using its extrema as a statistical range.

{{BOG_TABLE}}

![Partial process CO₂ intensity. Numerators: Jeong et al., B1-19, p7 Table 6; denominators: p13 Table A6. Lines connect the three reported impurity cases for readability and are not interpolation models. Full propulsion and upstream lifecycle GHG are excluded.](../outputs/figures/bog_partial_emissions.png)

The published large-ship fleet table also shows why annual throughput and distance need explicit representation. At 5 Mt/y, reported fleet counts for the 40,000 m³ design increase from 2 ships at 1,000 km to 24 at 20,000 km; the corresponding 120,000 m³ design uses 1 and 8 ships [B4-09, p6 Table 7]. The source fleet arithmetic is now reconstructed using the explicitly selected Table 1 density; its independent property validity remains unestablished. None is evidence that the proposed vessel or route is commercially available. The full 75-case table remains machine-readable in the repository.

## 3.5 Supporting accounting audit: published aggregate-burden score

The six Fraga best-solution intensities span 32.8–142.1 kgCO₂e/t stored. Their underlying networks, source portfolios and pressure configurations differ, so comparisons do not isolate pressure as a causal variable [B2-12, pp18,20]. With 32.8 kgCO₂e/t as the reference, Equation (3) gives score-equality storage uplifts from zero to 12.74%.

Cross-pairing these intensities with the South Sumatra storage outcomes gives the results below. The 4.31% storage uplift exceeds the score-equality requirement for the two Northern Lights and two combined-concept intensity scenarios, but is smaller than that for the two Stella Maris scenarios. This finding concerns the constructed score only. In particular, the negative Stella Maris score differences do not show that its real infrastructure has negative mitigation or is inferior for its intended source portfolio.

{{PROXY_TABLE}}

![Storage uplift required for equality of the reported-burden score, relative to the 32.8 kgCO₂e/t reference. Bars use the six published Fraga outcomes; the dashed line is the calculated Budiarto storage uplift. This is a cross-study accounting stress test, with fugitive-loss and omitted-burden corrections outstanding.](../outputs/figures/proxy_thresholds.png)

For the fixed published storage ratio, Equation (4) yields **72.74 kgCO₂e/t stored** as the high-storage scenario's reported-intensity crossing. It is useful as an audit target: an analysis claiming an advantage from these particular gross-storage values must examine its incremental inventory near this magnitude. It is not a generic allowable transport emission factor, a calibrated Japanese break-even threshold or a policy limit. Equation (5) determines how reconciling source losses and omitted GHG would change the score comparison.

# 4. Discussion

## 4.1 What the present evidence supports

The literature supports the mechanism behind Paper 1: usable storage service can affect the amount captured and stored, while conditioning, transport, buffers and operational states affect burdens and feasibility. It also shows why those components cannot be combined by selecting a convenient number from each paper. The variables may have different denominators, reference flows, countries, modelling horizons and physical meanings. Source-driven analysis therefore requires more than providing citations: the transferred quantity must still answer the question posed by the receiving model.

The present calculations expose three practical failures that such an audit can prevent. A thermal pressure decrease can be mislabelled as a rate decrease. A buffer-to-cycle-mass ratio can be mislabelled as a buffer-to-ship ratio. A lifecycle factor containing captured-source fugitives can be subtracted from already loss-adjusted retained mass, counting the loss twice. Each produces an apparently numerical answer while changing the underlying question.

The score crossing is consequently a diagnostic intermediate result. It shows how the published storage ratio interacts algebraically with the adopted reported intensities. It cannot decide between actual domestic and foreign services until the inventories are decomposed and geographically compatible. Reporting the correction term is preferable to setting unreported capture, well and water-handling burdens to zero. No Monte Carlo probability, confidence interval or country ranking is inferred from the selected cases.

## 4.2 How to use geographic proxies responsibly

A published non-local reservoir case can test whether a decision is sensitive to a particular service pattern, provided its provenance and limitations remain visible. It cannot establish that a Japanese sink has the same permeability, pressure interference, temperature response or commissioning date. The present Indonesian benchmark is retained under its original identity. The supplied rounded annual allocation profiles can now be used as labelled published schedules for replay and validation. Using them as exogenous proxy schedules in an additional scenario would require explicit disclosure; they do not establish independent physical service upper bounds or a local geological calibration.

Process proxies require the same care. Norwegian electricity and transport assumptions are scenario inputs here, not replacement estimates for Japanese or Malaysian energy systems. Resource estimates identify where to investigate; they do not allocate storage capacity to the chosen source. Studies of legal liability and governance can organise access questions but cannot certify current permits. A geographic scenario is physically meaningful only after source, route, terminal and storage-service constraints can be satisfied together.

## 4.3 Controlled annual extension: testing the value of model detail

The full-inventory extension should preserve the proposal's three objectives: quantify storage-service constraints, quantify transport/conditioning burdens and identify when additional retained CO₂ outweighs additional lifecycle GHG. It should use one common industrial-production/no-CCS baseline for domestic-only, foreign-only and mixed allocation. The proposal's 2030–2050 horizon is a research-design choice, not an extracted operating forecast; the endpoint convention must be stated before implementation. The present published cumulative benchmarks retain their original horizons and are not rescaled to this proposal horizon.

The material balance must distinguish source supply, realised capture, closing inventory, injection, handling losses and captured-stream venting. End-of-horizon material still in tanks or vessels receives no permanent-storage credit without a supported subsequent fate. Annual usable injection is constrained by readiness, wells, pressure/thermal limits and allocated cumulative storage. Downtime cannot be applied both within a published service profile and as an additional multiplier.

Shipping should resolve integer departures, laden and return transit, port operations, pressure compatibility and binding buffer limits. Voyage loading, heel and annual fleet utilisation are different quantities. BOG generation is not automatically atmospheric loss; recondensed gas, returned vapor and retained heel need their own mass states. Zero throughput has undefined per-tonne intensity, not an assumed zero-emission result. Port or pressure constraints can make a fleet-hour solution infeasible even if its aggregate annual capacity appears sufficient.

The implemented proxy comparison uses four controlled variants; the full regional extension should preserve their controls. B0 uses static injection screening and a fixed transport factor; B1 introduces annual deliverability; B2 keeps B0 storage and resolves operational shipping; B3 includes both. The static proxy and calibration flow must be specified before observing outcomes. Controls should distinguish changing post-commissioning service from commissioning delay and distinguish equal-retention route burdens from additional-storage effects.

For a full-inventory model, let Dj be foreign minus domestic net mitigation under variant j. The present prototype applies the same contrast algebra to its partial allowance H, with that boundary disclosed. The full representation contrast is D3 minus D0. The interaction is:

$$I=D_3-D_2-D_1+D_0. \tag{6}$$

Calling the full contrast an interaction would overstate the effect of coupling. If a simplified variant selects another route or fleet, its selected decision should be evaluated under the same detailed feasibility/accounting model before attributing a climate benefit to model resolution. A null interaction or unchanged robust ranking remains informative. Numerical B0–B3 results are now reported at the explicitly partial operating boundary; complete lifecycle net avoided GHG is not computed.

The physical break-even condition is additional retained source CO₂ equal to additional consistently counted lifecycle GHG under the common counterfactual. Integer fleets and phased assets may create several crossings rather than one universal distance. A regional application therefore needs supported annual injection series, route-state fuel/energy, local/year backgrounds, pressure-management inventory, asset construction and a retention horizon. Published aggregate outcomes alone cannot identify that frontier.

## 4.4 Limitations

The supplied-library review is selective: 44 unique publications remain at abstract/relevance stage and targeted extraction of the other 48 is not an exhaustive inventory of every supplement or numerical claim. The 1,642 records include contextual values unsuitable as direct model parameters. The score analysis combines independently optimised studies and does not reproduce either original optimisation, whose complete physical constraint arrays, detailed process/network inputs and code are not fully supplied. The Budiarto supplementary tables and rounded annual results are supplied and included; exact raw allocations and maximum-rate arrays remain distinct requirements.

Several unresolved source issues are deliberately excluded from use, including the Noh and Kang density discrepancy. File hashes and source-token checks establish provenance; they do not validate a reservoir forecast, measured permanent retention, commercial access or model assumptions. Missing quantities are identified rather than assigned plausible-looking values. The manuscript is an evidence-based methods and operational-proxy draft. The full regional lifecycle model, calibrated physical injection constraints, alternative dispatch validation and shared-source mixed optimisation remain specified research stages.

# 5. Conclusions

The implemented four-variant model makes the consequences of simplified shipping and service representations reviewable. Located published inputs reproduce all 75 source fleet counts, while the event model demonstrates that annual capacity arithmetic alone does not establish scheduling feasibility under a stated availability calendar and terminal configuration. Initial heel, capture curtailment and endpoint inventories materially belong in the balance.

Fleet-adequacy, equal-injection and added-vessel controls change the interpretation. After a declared design control, conditional allowances differ in sign between the selected 5,000 and 10,000 km scenarios. Calendar and fleet perturbations also change signs. These results support testing design feasibility and model sensitivity; they do not establish a robust geographic route preference.

Complete lifecycle mitigation remains uncomputed because compatible capture, fuel/process, injection/asset and retention inventories are incomplete. The reported allowance defines how small the unknown differential burdens must be for a full advantage. The next substantive data needs are compatible utility/GHG inventories and independent physical injection constraints, rather than an unqualified transfer of aggregate published GWP factors.

# Data and code availability

The accompanying GitHub research branch contains the retained PDFs, supplementary DOCX and its source images/tables, original proposal, source catalogue and page text, full extraction ledger, curated/analysis inputs, issue log, calculated CSV/JSON results, figure sources, tests and editable manuscript. The input register records every empirical quantity used in the calculations. Historical preparation outputs are separately archived and superseded by the current documents. The supplied scholarly documents retain their original rights and licences.

# References

The following references are cited by stable source ID. Full supplied-library titles, identifiers, original filenames and file hashes are in `data/source_catalogue.csv`; complete digests and reading stages are in `docs/evidence_digest.md`. Physical pages cited above refer to the retained PDFs.

{{REFERENCES}}
