# Evidence digest and coverage

The current library contains **93 supplied PDF files, 92 unique publications and 1,301 physical pages across the unique publications**. B3-46 is a duplicate publication of B2-17. File hashes and original filenames are preserved in the source catalogue. Reuploads of previously supplied titles reuse the already downloaded version; this package does not assert that every reuploaded binary was separately compared. The retained PDFs are authoritative for this draft.

**All 92 unique publications now have targeted full-text review: 48 initial targeted extractions and 44 follow-up reviews of selected methods/results passages; none remain abstract-only.** Targeted extraction is selective, not an assertion that every number in every paper has been inventoried. This is a purposive supplied-library synthesis, not a completed systematic review. The Budiarto supplement is now supplied and reviewed; other unsupplied supplements remain outside the evidence base.

The original extraction ledger contains **1,642 records**: 1,097 preserved earlier records plus 193 atomic records from the nine new papers and 352 numeric records from the Budiarto supplement (102 native-table entries and 250 printed annual allocations). Records may contain ranges or grouped cases and are not independent measurements. `curated_values.csv` contains 250 explicitly located quantities (including selected earlier values). `analysis_inputs.csv` contains 134 rows, of which 75 are published fleet counts and 59 support 49 calculations. The 124-row results file therefore contains **49 derived results and 75 directly reported fleet outputs**. Do not add overlapping tables together to count unique data.

The separate supplement tables and annual grid retain a further 352 numeric records and 470 blank figure cells. The new annual replay is additional to the original 49 benchmark calculations; its outputs are not a new MILP optimisation. The separate operational extension now implements B0–B3 with 144 comparisons, explicit service proxies and incomplete lifecycle accounting; see `operational_model.md`.

The broad extraction ledger is an audit trail, not a harmonised input file. Only the dedicated analysis inputs enter calculations. Source input, simulated result, observation and derived quantity must remain distinct. No source-wide transferability is implied by accepting a quantity for its stated context.

The original proposal, earlier preparation snapshot and earlier scaffold are retained separately. Current documents supersede historical assertions that Budiarto was missing or that no benchmark results existed. All 14 proposal reference identities are now linked to supplied primary PDFs; their original novelty claims do not all survive verification.

The Google Drive folder was not ingested: no callable Drive capability was available in this session. The uploaded planetary-limit ZIP exceeded the file-transfer tool's 32 MiB limit and could not be archived or inspected; the standalone planetary-limit PDF is in the library. No data from that ZIP are claimed as extracted.

## Reference-data update

The later reference-data intake has104 uploads:100 accessible files and95 distinct accessible binaries; four oversized IBDP reports remain unavailable. These include official factors, NETL files, IMO guidance, dataset snapshots and IBDP reports/catalogues. They are catalogued separately from the original 92-publication literature review. Page text is indexed, but targeted scientific review covers only the components used or screened for model suitability. See [reference review](reference_dataset_review.md) for the source-specific findings.

The new dedicated registers contain77 located reference-inventory inputs,8 derived NETL capture cases and12 located Illinois simulation quantities. They overlap original source material and are not additional independent measurements. The current Japanese tables contain3,269 located factor records; the raw17-workbook archive holds1,013,036 cached/formula cells including errors, not validated observations. Two wave snapshots yield34 located variables and no weather calendar. The source-driven extension produces2,980 partial inventory comparisons; complete net avoided GHG remains uncomputed.

## Japanese case-evidence update

The third intake adds26 uploads,25 accessible files and1,186 indexed pages across17 PDFs. Its420 located quantities and separate source-native exports are reviewed in [the case-evidence report](case_evidence_review.md). Tomakomai provides45 monthly records,17 shut-in/test windows, nine fall-off interpretations and conditional pressure/capacity scenarios. These are historical observations and source-model outputs, not independently calibrated annual maximum service. The original 92-publication coverage counts remain unchanged until the separate deepening review is completed.

Northern Lights components support8 derived checks and100 optional sensitivity rows. The Japanese source exports contain an unresolved ENEOS/Nippon Steel mismatch. The CPPI annex is now archived. The IBDP ZIP remains unavailable because of the32MiB transfer limit. No uninspected ZIP content is claimed as evidence.

## Main interpretation

A defensible Paper 1 contribution is a reproducible test of the additional decision value of jointly representing time-varying storage service and operational shipping. Prior work already includes dynamic infrastructure, common-reference emissions, reservoir constraints, resilience, operational shipping and carbon payback. The current draft contains actual literature calculations and a clearly labelled cross-study proxy stress test, with the complete annual regional comparison kept as a specified extension.

## Per-publication digest

### B1-01 — Onboard carbon capture and storage (OCCS) for fossil fuel-based shipping A sustainability assessment

Zanobetti et al. (2024). Identifier: 10.1016/j.jclepro.2024.143343. [PDF](../papers/B1-01.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

A 36 MW LNG cruise-ship case compares amine scrubbing, advanced cryogenic capture, membranes and adsorption using technical, economic, environmental and social indicators. Only amine scrubbing and advanced cryogenic capture meet the case-specific onboard integration constraints. At 95% capture, reported CO2 avoidance is 85.7% and 77.5%, respectively (p8, Table 7).

Transfer limits: Cruise-ship exhaust capture is not bulk CO2 cargo transport; LNG cold integration and waste-heat assumptions are not transferable to an ordinary CO2 carrier. Supplementary process inputs were not supplied.

### B1-02 — CO2 Reduction by Combining Methanation With the Blast Furnace

Kawashiri, Kashihara & Fukada (2023). Identifier: 10.33313/387/045. [PDF](../papers/B1-02.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

A carbon-recycling blast-furnace calculation compares methane recycling with direct hydrogen injection. Table 1 (p6) reports carbon consumption of 425, 324 and 293 kg/t hot metal for conventional, hydrogen and recycling cases; corresponding reported reductions are 24% and 31%.

Transfer limits: Recycled methane carbon is excluded from the paper's specific carbon-consumption accounting (p2). This is not geological storage or a whole-chain CCS LCA; the 31% cannot be used as a storage-retention or capture factor.

### B1-03 — Evaluating the impact of CO2 capture and storage on total efficiency A lifecycle analysis

García-Tenorio Corcuera & Petrakopoulou (2025). Identifier: 10.1016/j.clet.2025.101002. [PDF](../papers/B1-03.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

Hypothetical UK and Australian natural-gas and coal cases account for fuel preparation, conversion and CCS. The reference capture fraction is 95%. Table 3 (p5) assembles capture, compression and injection energy data from other publications. Results show strong dependence on fuel preparation and capture assumptions.

Transfer limits: Several unit/summary problems require resolution before calibration: MJ/MWnet lacks an explicit time basis in the reported energy metric; abstract says losses exceed 50% in both fuels whereas detailed NG results reach about 49%; body p9 labels the 3.6/8.43 Mt/year comparison at 90% capture but conclusion p10 says 95%. Do not quote these as harmonised measured penalties.

### B1-04 — CO2 Sequestration in Deepwater Sediments Offshore Japan

Pilisi, Ghorbani & Vasantharajan (2012). Identifier: CMTC-151756. [PDF](../papers/B1-04.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

Three ultra-deepwater Japanese sediment cases model shallow subseabed injection under high-pressure, low-temperature gravitational trapping. Table 3 (p10) specifies 5,000 tons/day for each case; injection lasts 25 years, followed by 225 years of migration simulation. Deeper/hotter injection can reverse the density advantage.

Transfer limits: A 2012 feasibility concept with unavailable offshore storage/injection vessels at the time of publication is not evidence of present service availability. Large assumed injection rates are not tested deliverability. Simulated immobility is not a measured permanent-retention fraction or proof of greater safety across sites.

### B1-05 — Independent Study Addresses Causes of Challenges in Asia Pacific Flagship CCS Project

Carpenter; synopsis of Sabzabadi, Gladman & Billingsley (2025). Identifier: SPE-1225-0011-JPT; synopsis of SPE-225882. [PDF](../papers/B1-05.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

The synopsis attributes Gorgon constraints to water treatment/reinjection and pressure management rather than failure of CO2 containment. It reports August 2019 injection start, a design rate described as 150 kg/s or 4 Mt/year, and four water-production wells. More brine cannot be extracted if its receiving formation cannot accept treated water.

Transfer limits: Do not present the synopsis as the underlying full technical paper or an audited current operational dataset. It prints sustained injection as “1.6 tonnes per year” (p3); retain the text and flag the apparent scale/unit error. Do not silently replace it with 1.6 Mt/year. Continuous annualisation of 150 kg/s also differs from 4 Mt/year unless an operating factor is assumed.

### B1-06 — Openhole completion integrity analysis for life of CO2 injector well

Rashidi et al. (2024). Identifier: ARMA-IGS-2024-0222. [PDF](../papers/B1-06.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

An offshore Sarawak injector is assessed during drilling, brine displacement, injection and stoppages using stress, pressure and temperature outputs from a thermal/dynamic/geomechanical model. Cooling and changing wellbore support cause different shear/tensile failures over time. A perforated liner is selected instead of an unsupported openhole.

Transfer limits: Pressure-gradient equivalents in ppg and failure intervals are well-specific simulated conditions. They do not establish a general outage probability, annual rate reduction or universal completion design.

### B1-07 — Leveraging Oil and Gas Legacy for Advanced CCS in Japan Realistic CO2 Storage Simulation in the Higashi-Niigata Gas Field

Kukuu et al. (2025). Identifier: 10.2118/225812-MS. [PDF](../papers/B1-07.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

Higashi-Niigata models 100 geological realisations, selecting 10 after history matching. Case A uses three CO2 injectors; Case B adds three pressure-relief wells. Injection is assumed from 1 January 2029 to 1 January 2050. Case A reaches its pressure limit around 2040; pressure relief increases injection volume by approximately 25–30% (p8).

Transfer limits: Figures 11/17/19 lack visible numerical vertical-axis scales in the supplied PDF (visually checked pp7/9). Absolute injected tonnes and pressure values cannot be reliably digitised. Obtain numerical annual series, initial pressure and well/service access before calibration. Do not invent a Mt/year profile from the relative uplift.

### B1-08 — Unlocking CO2 Injection in Depleted Reservoirs A Flow Assurance Modeling Approach for Carbon Capture and Storage

Charoensuk et al. (2025). Identifier: 10.4043/35887-MS. [PDF](../papers/B1-08.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

A Sarawak development targets up to 2.0 Mt/year through a 40 km offshore pipeline into shallow/intermediate/deep depleted reservoirs. Early-life thermal/hydraulic limits constrain the shallow case to 37.5% and deep case to 80% of well design capacity under specified conditions. An insulated pipeline is selected over offshore heating and gas-phase transport.

Transfer limits: Design/forecast, not measured storage performance or access for imported Japanese CO2. The system handles CO2 separated from sour-gas production, so its industrial counterfactual differs. The paper labels a critical pressure as 73 barg (p3); retain as printed and do not confuse this with absolute-pressure property data.

### B1-09 — 4-D Geomechanics Modelling for Potential CO2 Storage Site in Malaysia – Fault Reactivation and Maximum Pressure Injection Limit

Nik Kamaruddin et al. (2019). Identifier: IPTC-19491-MS. [PDF](../papers/B1-09.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

A Malaysian carbonate Field X model uses field subsidence and laboratory-derived compaction/creep properties. It recommends maximum injection reservoir pressure of 4,000 psi with a 600 psi safety margin, while minimum horizontal stress during injection is 4,600–6,200 psi (p13).

Transfer limits: An anonymised field is not a named storage service. The pressure ceiling cannot be transferred to another Malaysian sink or converted directly into tonnes/year without injectivity and well data. Planned 2024 injection start is a 2019 scenario assumption, not evidence it occurred.

### B1-10 — A Decision Framework for CO2 Storage Site Selection in Depleted Reservoirs

Hamid (2026). Identifier: 10.4043/36331-MS. [PDF](../papers/B1-10.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

A four-reservoir hub example supplies up to 10 Mt/year over 20 years with a five-year ramp. Transport distance, reservoir pressure evolution and injectivity influence annual allocation. A far-only route is reported at about USD148 million versus USD230 million in the compared configuration (p11).

Transfer limits: Inputs are explicitly modified/anonymised (p7). Average reservoir pressure is constrained but flowing bottomhole pressure is allowed above the fracture limit (pp10/12); such cases are not demonstrated injection-feasible. Do not inherit this as a safety constraint for Paper 1. Annual pipeline sizing also needs a fixed-design feasibility check.

### B1-11 — Systematic Feasibility Assessment of Geomechanical Risks for CO2 Injection and Long-Term Storage Incorporating Rock Properties Degradation and Thermal Effects

Tan, Musa & Nik Kamaruddin (2024). Identifier: ARMA-IGS-2024-0183. [PDF](../papers/B1-11.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

An offshore Peninsular Malaysia Field X assessment uses eight offset wells and an analytical caprock/fault workflow. With estimated 50°C cooling, recommended pressures for Seals A–D fall from 2153/2731/3264/3701 psi to 1632/2209/2739/3178 psi (pp5–6, Tables 2–3).

Transfer limits: No measured rock properties were available for the selected field (p4). The up-to-26% stiffness/strength reduction and up-to-10% Poisson-ratio increase are database-based sensitivity evidence (p3), not directly measured at this site. The text extraction displaces psi/psia headers; values were visually checked and original header labels preserved.

### B1-12 — Geomechanical Evolution of the South-West Hub Carbon Capture and Storage Reservoir in Western Australia

Hosseinzadeh et al. (2026). Identifier: 10.2118/234571-MS. [PDF](../papers/B1-12.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

South-West Hub/Harvey modelling describes a conceptual 800,000 tCO2/year, 30-year plan, nine injection wells and a reference BHP constraint of 360 bar at 2948 m (p18). No significant fault failure is predicted for the modelled isothermal pressure-driven response.

Transfer limits: Conference modelling does not establish present commercial availability or shipping access. Some text requires author/data clarification: 37/32 is not 1.125 (p18), a stress gradient is printed only in MPa, and Figure 10's pore-pressure range needs datum/quantity reconciliation. These do not justify silently changing reported numbers.

### B1-13 — Optimising the CO2 Storage Potential in Deep Saline Aquifer by Creating Pressure Sink

Razali et al. (2024). Identifier: 10.4043/34777-MS. [PDF](../papers/B1-13.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

A Malaysian restricted aquifer (K reservoirs, Z field) is simulated with and without brine production. Cumulative effective gas volumes are 4.9 Bscf without production, 80.13 Bscf with one injector/one producer, and 95.44 Bscf with two injectors/one producer. These are about 3%, 51% and 61% of theoretical volume (pp8–13).

Transfer limits: The authors ultimately do not recommend proceeding with Z-field injection planning because volume is small and inputs uncertain (p13). Do not select it as a proven Malaysian sink. Bscf/MMscf cannot be turned into tonnes without declared standard conditions/composition and conversion. PVT/SCAL and permeability include analogue-based inputs.

### B1-14 — Fully coupled inversion on a multi-physical reservoir model – Part II The Ketzin CO2 storage reservoir

Wagner & Wiese (2018). Identifier: 10.1016/j.ijggc.2018.04.009. [PDF](../papers/B1-14.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

Ketzin inversion jointly uses hydraulic/CO2 pressure, arrival times and geoelectric observations. A near-injector permeability reduction to about 15 mD (roughly eightfold) and equivalent skin of 10 explain pressure overburden attributed to salt precipitation. Observed/modelled arrivals are 21.7/21.8 days and 271/283 days (p6).

Transfer limits: The earlier hydraulic-barrier hypothesis is not substantiated after suspect data are removed, but non-uniqueness means a barrier is not excluded (p8). Do not turn the eightfold local permeability change into an eightfold annual site-capacity decline.

### B1-15 — Matching Pressure Measurements and Observed CO2 Arrival Times with Static and Dynamic Modelling at the Ketzin Storage site

Class et al. (2015). Identifier: 10.1016/j.egypro.2015.07.883. [PDF](../papers/B1-15.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

Ketzin models match pressure and CO2 arrival despite strong porosity/permeability correlations. Table 3 (p5) compares observed arrival times of 21.7 and 271 days with alternative simulated arrivals; pressure-only fit does not uniquely identify spatial geology.

Transfer limits: Table 1 prints a pressure gradient of 1.14 Pa/m (p4, visually confirmed). This is implausible as a normal brine hydrostatic gradient; hold this value pending correction, rather than insert a presumed exponent. Arrival dates depend on sensor location and completion, not merely plume contact.

### B1-16 — Integrated reservoir monitoring at the Illinois Basin – Decatur Project

Couëslan et al. (2014). Identifier: 10.1016/j.egypro.2014.11.306. [PDF](../papers/B1-16.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

Decatur couples time-lapse saturation logs, multilevel pressure, fluid chemistry, seismic and microseismic data. Approximately 925,300 tonnes had been injected by 1 September 2014 (p2), against a one-million-tonne three-year goal. Low-permeability layers restrict upward CO2 migration in the monitored interval.

Transfer limits: This is a US ethanol-fermentation source, not a fossil Japanese industrial baseline. Monitoring evidence of no detected migration is not a numerical permanence guarantee. The Zone 4 depth is inconsistent between p3 text and the other monitoring evidence; do not use that single text depth uncritically.

### B1-17 — Injection operation and operational pressure–temperature monitoring at the CO2 storage pilot site Ketzin, Germany—Design, results, recommendations

Liebscher et al. (2013). Identifier: 10.1016/j.ijggc.2013.02.019. [PDF](../papers/B1-17.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

Ketzin recorded 61,396 t by September 2012. Typical injection was 1–3 t/hour, with 3,250 kg/hour nominal plant capacity. BHP rose from about 62 bara initially to 73 bara after five days, then stabilised around 73–79 bara (pp3–5). Downhole monitoring is needed because wellhead signals alone can mislead.

Transfer limits: Pilot rates and reservoir data are not commercial Japanese/Malaysian/Australian service. The 61,396 t as-of-2012 and later approximately 67,000 t final injection in other Ketzin papers refer to different dates, not contradictory estimates. Correct for gauge/absolute pressure before comparison.

### B1-18 — CO2 Plume Tracking and History Matching Using Multilevel Pressure Monitoring at the Illinois Basin – Decatur Project

Strandli, Mehnert & Benson (2014). Identifier: 10.1016/j.egypro.2014.11.483. [PDF](../papers/B1-18.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

A layered radially symmetric Decatur model is calibrated over 40 days and compared against two years of pressure data. It uses an approximately 150 mD, 23–24 m injection interval and predicts mainly lateral migration below low-permeability layers (p8).

Transfer limits: Isothermal 49°C model neglects salinity explicitly, then rescales permeability for viscosity; several parameters are calibrated. US biogenic source and pressure-history fit do not define international route lifecycle emissions or a universal retained fraction.

### B1-19 — Optimization and economic evaluation of carbon dioxide BOG Re-liquefaction process considering storage pressure and nitrogen impurity

Jeong et al. (2025). Identifier: 10.1016/j.energy.2025.135837. [PDF](../papers/B1-19.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

Six reliquefaction process/pressure cases are compared at 0.05/0.10/0.15 mol% liquid nitrogen impurity. A 50,000 m3 carrier is assumed with 98% laden and 5% ballast filling, 0.1%/day mass-based boil-off, and 4000 operating hours/year for each voyage state. Annual CO2 includes purge plus auxiliary-generator emissions. Table 6 and Appendix A.6 have been transcribed into structured scenario data.

Transfer limits: Preserve the case/impurity combinations. Text on p8 claiming 79.2–84.6% and 89.8–95.6% reductions in compression-power emissions appears inconsistent with its much smaller stated power reductions and constant generator factor. Annual schedule (6 voyages/year and 8000 operating hours) is a modelling assumption, not a route-calibrated schedule.

### B1-20 — Interoperability and energy optimization in low pressure ship to medium pressure terminal interfacing

Deligiannis et al. (2026). Identifier: 10.1016/j.ijggc.2025.104544. [PDF](../papers/B1-20.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

LP ships (7–10 bara) interface with MP terminals (12–20 bara). Case specifications use three 7300 m3 tanks (sensitivity 5840–8760 m3 each), 96% filling and 4% heel. Tables 6–7 (pp13–14) give nine pressure-pair cases with and without loading-stream subcooling. Tables are transcribed with mass, power, cost and original specific-demand labels.

Transfer limits: Specific-demand labels kWel/ton are dimensionally inconsistent with the stated kWh/ton intent; several values are consistent with a 12-hour transfer. Derived conversions are separate and conditional. Some textual claims of lower subcooler cost are case dependent; the full nine-case table must govern. These are process energy/cost results, not route-wide GHG factors.

### B2-01 — Effects of pipeline distance, injectivity and capacity on CO2 pipeline and storage site selection

Wang, Fimbres Weihs, Neal & Wiley (2016). Identifier: 10.1016/j.ijggc.2016.05.006. [PDF](../papers/B2-01.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 3, 4, 5.

Two-sink pipeline screening explicitly compares injectivity, distance and cumulative capacity. A more distant, better-injectivity site may reduce cost. Flow supply is static.

Transfer limits: Economic prior art, not a matched climate-benefit result; 15–35 Mt/year trunk-line scale is not an individual ship route.

### B2-02 — Prospective techno-economic and life cycle assessment a review across established and emerging carbon capture, storage and utilization CCS CCU technologies

. Identifier: 10.3389/fenrg.2024.1412770. [PDF](../papers/B2-02.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 11,12,13,20.

Review of prospective TEA/LCA across technology maturity, scale-up, hybrid costing and foreground/background scenarios. Table2 distinguishes prospective from dynamic LCA; later sections discuss semantic matching between IAM technologies and LCI processes and the need for transparent model assumptions.

Comparisons depend on maturity, energy integration, functional-unit matching and future backgrounds. The review reports a cited heat-integration study where annual averaging differs materially from multi-period optimisation. A process in an integrated-assessment model need not map unambiguously to one inventory activity.

Transfer limits: This is secondary methodological synthesis, not measured heat/electricity or a supplier-matched inventory for our source. Cited percentages are context, not transferable uncertainty ranges or probability distributions. Static official factors do not become complete prospective backgrounds by virtue of being official.

### B2-03 — Multi-period Carbon Capture, Utilization, and Storage (CCUS) infrastructure design and planning under uncertainty

. Identifier: 10.1016/j.compchemeng.2025.109300. [PDF](../papers/B2-03.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,7.

Annual-budget deterministic and two-stage stochastic CCUS deployment MILPs with rolling horizons and sample-average approximation. Source/sink selection, start times and single source-sink pipelines are decisions. After a connection is chosen, annual transported quantity is constant. Geological storage volumes are uncertain inputs; full capture is imposed at selected sources.

The Illinois Basin case compares network decisions under capacity uncertainty. The stochastic design reduces the reported mean shortfall from4,795kt to145.24kt per scenario over plant operating lives. It evaluates fixed designs on5,000 scenarios, rather than inferring a generic probability of storage success. The analysis already combines temporal planning and uncertain sink capacities.

Transfer limits: Objective is economic benefit including social cost/EOR revenue under budgets, not harmonised lifecycle net mitigation. Source capture equals emissions by assumption. Missing supplements contain economic/cost details. Its uncertain volumes and recourse results do not supply physical annual pressure-constrained injection maxima or transferable reliability distributions.

### B2-04 — Optimizing carbon capture and storage infrastructure including physics-based reservoir modelling

Bertoni, Møyner, Wiegner & Gazzani (2025). Identifier: 10.1016/j.compchemeng.2025.109293. [PDF](../papers/B2-04.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 4, 5, 9, 10.

POD/trajectory-piecewise-linear reduced reservoir dynamics are embedded in a CCS MILP. Pressure prediction is reported within ±5%, with 500–1800-fold speedup versus tested full simulations.

Transfer limits: Already integrates dynamic physics and infrastructure; accuracy is case/training-region dependent, not a universal reservoir error bound.

### B2-05 — Beyond pipelines Multi-modal CO2 transport enables timely CO2 capture, transport, and storage deployment

. Identifier: 10.1016/j.ijggc.2026.104698. [PDF](../papers/B2-05.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,7,8.

Transition-pathway MILP models technology lifetimes, capacity additions, multimodal flows and speed-of-pipeline-deployment limits. Stored CO2 targets include direct source-stream losses; lifecycle burdens are represented in the model but excluded from the sequestration balance in Eq6. Storage is modelled as a service with annual/cumulative limits and operating costs/emissions, without explicit storage investment.

Constraining pipeline expansion produces unmet storage targets, while barges/ships bridge deployment limits. Early pipeline utilization is low; temporary multimodal capacity changes the transition even when final infrastructure looks similar. The body reports4.8Mt cumulative shortfall but Figure3 caption says1.7Mt, so that benchmark is held pending reconciliation.

Transfer limits: Cost-optimal transport deployment and direct sequestration targets do not establish full matched-source net climate benefit. Barge shares are tonne-kilometre shares, not source mass fractions or vessel availability. Storage-service simplification does not supply calibrated well pressure constraints. Supplement details are still needed to reproduce the original scenarios.

### B2-06 — Multiperiod strategic planning of CO2 capture, transport, utilization and storage with multimodal transportation

. Identifier: 10.1016/j.compchemeng.2025.109525. [PDF](../papers/B2-06.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 6,15,19,22.

Multiperiod strategic CCUS MILP includes gas/liquid/supercritical state changes, buffer balances, capture units, pipeline capacity choices and truck/rail/ship fleets, including direct offshore injection and floating storage interfaces. Yearly decisions are identical within a planning period; vehicle activity includes berth and travel/loading constraints. An illustrative Eastern Canada network uses GIS-based candidate links and a heuristic to reduce computational burden.

Time discretisation and transshipment constraints affect feasible infrastructure. Limiting emitter vehicle loading/unloading to5Mt/y prevents concentrating49.4Mt/y of train-to-offshore-pipeline transfers at one emitter. The constrained example uses trains, pipelines and a40kt ship delivering779kt/y in the last two years. The authors explicitly call the costs/geographic weighting illustrative while Canadian data are being developed.

Transfer limits: An annual strategic fleet formulation does not validate detailed ship schedules. Cost weights transferred from US studies and assumed transshipment capability are not actual Japanese terminal designs. It already represents phase transitions, buffers, utilization and changing injection limits, so these are prior art rather than unique Paper1 contributions. Monetary values are2025CAD; no conversion to GHG is justified.

### B2-07 — From point-to-point to hub-and-cluster a systematic review of co-optimization of source–sink matching and transport networks for large-scale CO2 sequestration

. Identifier: 10.3389/fenvs.2026.1966624. [PDF](../papers/B2-07.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,4,13,21.

PRISMA-guided source-sink/network co-optimisation review distinguishes contextual references from17 direct-evidence studies. Its extraction protocol codes system boundary, decisions, uncertainty, scale, computational reporting and limitations. It distinguishes sequential, monolithic and decomposition approaches and separates demonstrated methods from prospective AI/digital-twin capabilities.

The review argues for auditable feasibility/objective/runtime/gap reporting and matched static/perfect-information controls. Its proposed future scale benchmarks and digital-twin/learning directions are evaluation priorities, not verified achievements. Cross-study evidence does not support a universal algorithm ranking.

Transfer limits: The supplementary search/exclusion/extraction matrix is not supplied with our library, so the reported systematic-review workflow is described rather than independently reproduced. Counts are review metadata, not empirical reservoir or transport inputs. Prospective AI/closed-loop concepts do not validate safe operating policies or local access.

### B2-08 — Optimal design and cost of ship-based CO2 transport under uncertainties and fluctuations

Bjerketvedt, Tomasgard & Roussanaly (2020). Identifier: 10.1016/j.ijggc.2020.103190. [PDF](../papers/B2-08.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 6, 7, 8, 12.

Brevik–Kollsnes case transports 0.4 Mt/year over 715 km; stochastic sailing, buffers and speed/power responses affect transport completion and cost.

Transfer limits: Buffer ratios depend on 99% versus 100% transport case and denominator. Table 2 labels design power W for 1500–2500 values; clarify before using as physical watts.

### B2-09 — Risk aware planning of CO2 transport and geological storage networks for net zero buildings under capacity and injectivity uncertainty

. Identifier: 10.1016/j.enbuild.2026.117200. [PDF](../papers/B2-09.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,8,17.

Network MILP uses budgeted uncertainty for pipeline capacity and well injectivity, plus CVaR shortfall risk. It jointly designs shared hubs, integer pipelines/wells and discounted cost. The case is explicitly synthetic: five emission sources, one hub and two sinks, with assumed production capacities and straight-line geometry.

Risk preferences create discrete investment/cost-versus-shortfall tradeoffs. The authors state that regional use requires real source/storage data, pressure management, learning and correlated risks; the illustrative magnitudes do not calibrate physical deliverability. Model scale and uncertain asset capacities are distinct from a validated pressure forecast.

Transfer limits: Literature emission factors combined with assumed production are not observed source emissions. Robustness budgets/CVaR scenario preferences are design parameters, not measured probabilities for our sites. It is strong prior art for injectivity/capacity uncertainty, but no site-specific kr,t or actual permits can be transferred.

### B2-10 — Exploring the value of CO2 shipping transport flexibility in international batchwise transportation carbon capture and storage networks

See supplied first page. Identifier: SSRN5070419 / GHGT-17. [PDF](../papers/B2-10.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 3, 4, 5, 6.

Fraga GHGT-17 assesses 15 what-if scenarios including six-year source/sink delays and network interconnection over 30 years.

Transfer limits: Implemented analysis minimises cost after capture. Model name includes multi-objective but this paper is not a whole-chain baseline climate assessment.

### B2-11 — A techno-economic assessment of CO2 capture in biomass and waste-fired combined heat and power plants – A Swedish case study

. Identifier: 10.1016/j.ijggc.2022.103684. [PDF](../papers/B2-11.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,4,5,10.

Steam-cycle process models and an hourly district-heating unit-commitment model assess110 Swedish biomass/waste CHP plants. Fixed boiler load and maintained industrial-process heat define the reference service. A90% MEA capture case assumes reboiler duty3.6MJ/kg captured at120C with3bar steam, and0.1MWh/t electricity including capture/compression/liquefaction. Heat recovery is treated through the DH system rather than a generic negative capture duty.

Plant utilization and size jointly drive capture/local truck-transport costs. Higher heat recovery can change DH dispatch and electricity demand; the118% heat-recovery case requires heat pumps with0.17MWh/t additional electricity and COP3. It is not free energy or more than100% solvent heat-efficiency. Reported costs exclude onward ship transport and geological storage.

Transfer limits: This provides a transparent alternative MEA utility reference, not measured Japanese steel/refinery demand. Preserve the specified flue-gas/CHP conditions and avoid adding another liquefaction/compression charge. No DH displacement credit can be applied without a matched heating-system counterfactual. Biogenic/fossil shares cannot be transferred to a fossil industrial baseline.

### B2-12 — Multi-period, multi-objective optimisation of the Northern Lights and Stella Maris carbon capture and storage chains

Fraga, Korre, Nie & Durucan (2024). Identifier: 10.1016/j.ccst.2024.100190. [PDF](../papers/B2-12.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 5, 7, 8, 9, 10, 11, 12, 13, 15, 16, 18, 20, 21.

Multi-period cost/GHG optimisation incorporates conditioning, ships, pipelines, hubs and injection. Six best-solution cases yield 32.8–142.1 kgCO2e per tonne stored.

Transfer limits: Post-capture gate-to-gate boundary; no capture penalty or matched industrial no-CCS service. Maintenance/decommissioning exclusions and location-specific factors matter.

### B2-13 — How to transport carbon dioxide with minimal environmental impacts today and tomorrow A prospective life cycle assessment

Nöhl et al. (2025). Identifier: 10.1016/j.jclepro.2025.145659. [PDF](../papers/B2-13.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 3, 4, 5, 6, 8.

European prospective LCA uses transport-only and conditioning-inclusive boundaries, time-varying energy backgrounds and an explicit cumulative carbon-payback equation.

Transfer limits: Already models cumulative carbon payback. ISO-container ship concept and regional future inventories cannot be substituted for dedicated Asian CO2-carrier data.

### B2-14 — A High-Precision Geo-Spatial-Techno-Economic Framework for CO2 Source-Sink Pairing Land-Sea Synergy and Cross-Regional Coalitions in China

. Identifier: 10.1021/acs.est.5c14041. [PDF](../papers/B2-14.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,4,9.

ITEAM-CCS hub integrates onshore/offshore suitability, tiered storage capacities, techno-economics, source pairing and candidate pipelines. Separate onshore/offshore assessment criteria reflect different data and technical schemes. The authors explicitly limit the framework to macro-assessment/preliminary feasibility rather than project design.

Table3 distinguishes theoretical/effective resource inGt from source-matched annual amounts inMt/a at specified distance thresholds. National-scale spatial and cost heterogeneity supports cross-regional screening; a large resource does not automatically become developed yearly storage service.

Transfer limits: P50 resource labels and annual matched source quantities are different metrics. National matching is not pressure-constrained well delivery or contracted capacity. No Chinese basin value is assigned to a Japanese sink; detailed underlying geological/economic data are not fully supplied.

### B2-15 — Global analysis of geological CO2 storage by pressure-limited injection sites

See supplied first page. Identifier: 10.1016/j.ijggc.2024.104220. [PDF](../papers/B2-15.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 4, 5.

Global basin pressure model contrasts maximum physical injection patterns with hydrocarbon-exploration and storage-readiness restrictions.

Transfer limits: Global scenario stock/rates are upper-bound model results, not a regional contract; deployment and data coverage constrain applicability.

### B2-16 — A proposed global layout of carbon capture and storage in line with a 2 °C climate target

See supplied first page. Identifier: 10.1038/s41558-020-00960-0. [PDF](../papers/B2-16.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1.

Global clustered source–sink matching selects 3093 clusters and 432 sinks for a 92 Gt mitigation scenario, including saline storage and EOR.

Transfer limits: Includes EOR and economic oil-price assumptions; not a uniform permanent-retention or avoided-GHG inventory.

### B2-17 — Progress and perspectives in source-sink matching for CCUS A critical review

. Identifier: 10.1016/j.rser.2025.116313. [PDF](../papers/B2-17.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 5,9,22.

Critical review separates geographic assessment scales and compares material-balance/volumetric capacity equations for depleted reservoirs, saline formations and coal seams. Parameters include density, effective thickness, porosity, recovery/water history and storage-efficiency factors, which differ by method and trapping mechanism.

The review identifies multi-source geotechnical data, dynamic node-level carbon footprints, coordinated infrastructure and consistent spatiotemporal data as research needs. Its proposed integration with renewables/hydrogen is prospective. Capacity formulas require formation-specific inputs and compatible trapped-volume definitions.

Transfer limits: Review equations are not site calibration and do not provide independent annual pressure/rate arrays. GWP, storage factors and method-specific capacities cannot be mixed across bases. B3-46 is the same publication and remains excluded from unique-publication counting. Underlying data are stated available on request.

### B2-18 — A prudent planetary limit for geologic carbon storage

See supplied first page. Identifier: 10.1038/s41586-025-09423-y. [PDF](../papers/B2-18.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 2, 3, 4, 5, 8, 10.

Risk-based geospatial screening estimates a central prudent planetary storage limit of 1460 GtCO2 with sensitivity 1290–2710 GtCO2.

Transfer limits: This is a precautionary scenario-dependent estimate, not a legal universal quota or site injection rate. Exclusions and conversion assumptions must accompany it.

### B3-01 — Carbon dioxide capture and storage—liability for non-permanence under the UNFCCC

. Identifier: 10.1007/s10784-006-9004-4. [PDF](../papers/B3-01.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 2,4,11.

Historical UNFCCC/CDM policy analysis separates capture/compression, transport and storage and examines non-permanence, cross-border accounting and the economic value of temporary versus permanent credits. Crediting period is distinct from physical retention duration.

Temporary credits can lose value when crediting periods are shorter than actual retention. The conclusion treats CCS classification within the then-current climate regime as a policy question. Historical capacity/cost tables are secondary context, not a current service database.

Transfer limits: The2006 regime discussion does not establish present permits, accepted accounting or liability transfers. Crediting horizons are not leakage probabilities or measured retention fractions; old global resource ranges and capture costs are not Paper1 physical inputs.

### B3-02 — Assessing a Liability Regime for Carbon Capture and Storage

. Identifier: 10.1016/j.egypro.2009.02.277. [PDF](../papers/B3-02.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 2,4,7.

Legal/policy assessment reviews US environmental/tort liability and proposes adaptive risk management using insurance, bonding and pooled funding. It distinguishes active injection, operator post-closure responsibility and public long-term stewardship, with performance conditions for any transfer.

Risk can persist without atmospheric leakage, including brine displacement and pressure effects. The proposed funding tiers aim to preserve operator incentives and finance monitoring/remediation. Example monitoring periods are discussed as policy mechanisms rather than empirically optimal retention horizons.

Transfer limits: This2009 analysis is not a current permit or a quantitative leakage-rate dataset. Suggested15/30/50year arrangements cannot be turned into certain closure dates, zero future liability or permanence guarantees. Site-specific risk and regulation remain independent inputs.

### B3-03 — Critical review and recommendations for strengthening health and safety and major accident prevention regulations for carbon capture and storage in UK ports

. Identifier: 10.1016/j.ijggc.2025.104479. [PDF](../papers/B3-03.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,9,11.

UK-port regulatory analysis compares the Port Marine Safety Code, dangerous-goods harbour rules and COMAH with CO2 loading/unloading, temporary storage and intermodal transfer. It identifies exclusions/classification issues and evaluates amendment/guidance pathways.

Table2 maps gaps to recommendations and implementation mechanisms. The authors argue for context-specific hazards rather than assuming nonflammable CO2 poses no major-accident risk; handling quantity, temperature, pressure and phase matter.

Transfer limits: Recommendations are not proof that amendments were adopted or that a particular port is licensed. Generic cryogenic pressure/temperature descriptions are not vessel-specific operability limits, terminal dwell times or release probabilities. No quantitative risk frequency is transferred.

### B3-04 — Development of CCUS clusters in Croatia

. Identifier: 10.1016/j.ijggc.2023.103857. [PDF](../papers/B3-04.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,7,10.

Croatian cluster screening combines source maps, possible transport corridors, geological screening and conceptual compositional reservoir models. Confidentiality prevents detailed static/well inputs; historical production/final pressure are matched in generic models, with projected production and EOR periods.

Eastern and Central clusters differ in source density and hub needs. The Eastern cluster combines about0.86Mt/y of emissions with23Mt screened capacity at18–65km source distances. These are candidate configurations, not evidence of an operational source-storage contract.

Transfer limits: Generic EOR screening and total resource cannot establish annual service or a full climate benefit once oil-production consequences are included. Costs use their original vintage. Confidential data prevent independently reproducing reservoir forecasts, and numerical screening thresholds are not universal safety criteria.

### B3-05 — Optimizing carbon capture and storage CCS infrastructure development using a python tool for source-sink matching and cluster formation

. Identifier: 10.1016/j.jclepro.2025.146563. [PDF](../papers/B3-05.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,6,7,9,10.

Python clustering/source-sink framework combines DBSCAN, minimum spanning trees and alternative redirection rules with weighted cost/emissions objectives. Effective geological storage uses a volumetric efficiency equation. Great-circle pipeline approximations omit terrain, protected land and detailed least-cost routing; uncertainty is propagated through the transport-cost model.

Kazakhstan case results depend on clustering radius and redirection rule. Full redirection at100km gives201.38USD/t reported total cost versus207.61 for partial redirection. Capture dominates the reported environmental inventory. This supports testing topology and accounting, not adopting a universal near-zero transport burden.

Transfer limits: Cost/emission outcomes are scenario-specific and pipeline geometry is approximate. National emission totals and volumetric resource are not a plant capture stream or pressure-limited annual service. User-friendly/open-code claims do not establish independent hydraulic/site validation; the original implementation/data must be checked before reproduction.

### B3-06 — Assessing-the-cost-reduction-potential-of-CCUS-cluster-projects-of-coal-fired-plants-in-Guangdong

. Identifier: 10.1007/s11707-022-1030-1. [PDF](../papers/B3-06.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 7,9.

Cost comparison of three Guangdong coal-plant standalone versus shared capture/transport/storage projects. Scenarios assume1Mt/y or3Mt/y captured per plant, giving cluster totals3Mt/y and9Mt/y. Pipeline distances and shared facilities enter discounted unit-abatement-cost calculations.

The cluster cost decreases from475.81 to298.02CNY/t when the assumed capture scale triples. Table6 reports scenario-specific reductions relative to individual projects, and explicitly assumes shared O&M grows by only twofold. Body/table rates resolve the implausible abstract300Mt/y statement for these scenarios.

Transfer limits: Scale economies in cost are not GHG reductions. Capture rates are assumed scenarios, not observed operation. Table6 monetary/NPV entries and source-wide O&M scaling need reconciliation before independent financial reproduction; no cost-to-emissions conversion is used. Abstract-rate error remains recorded rather than silently repaired.

### B3-07 — Estimation of CO2 Transport Costs in South Korea Using a Techno-Economic Model

See supplied first page. Identifier: 10.3390/en8032176. [PDF](../papers/B3-07.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 6, 10, 11, 18.

At 1 Mt/year, route-specific pipeline/ship costs are about USD33/28 per tonne; at 3 Mt/year they are USD21/23.

Transfer limits: Pipeline 530 km and shipping 724 km are unequal routes. Printed 2800 kg/s as 1 Mt/year on p11 is inconsistent; hold injection rate.

### B3-08 — Optimum liquefaction fraction for boil-off gas reliquefaction system of semi-pressurized liquid CO2 carriers based on economic evaluation

. Identifier: 10.1016/j.ijggc.2012.05.016. [PDF](../papers/B3-08.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,6,9.

Process/economic optimisation of partial BOG reliquefaction for a semi-pressurised CO2 carrier. Compressor work rises sharply when condensing light impurities. The objective includes reliquefaction expenditure, fuel-generated emissions penalties and the value of recovered CO2, rather than only physical mass conservation.

The100,000m3 case specifies cargo density1155kg/m3, assumed0.12%/day BOG and6000kg/h process BOG load. Under the study fuel/carbon-price assumptions, the optimum reliquefaction fraction spans97.2–98.1%, not necessarily100%. Economic LCC benefits include sale/recovery assumptions.

Transfer limits: This old design/cost case does not establish the actual BOR, duty or venting of our vessel. The volume, insulation, composition and storage state differ. Financial optimum fractions are not universal cargo-loss rates or environmental optima; BOG generated, reliquefied and atmospherically vented must remain separate.

### B3-09 — Planning of carbon capture storage deployment using process graph approach

. Identifier: 10.1016/j.energy.2014.08.060. [PDF](../papers/B3-09.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 2,3,7,8.

P-graph superstructure selects power-plant capture technologies and source-sink matches under a relative cost limit. It explicitly represents lost power and compensatory generation to maintain the power-service baseline, plus cumulative sink capacity. MSG/SSG/LP techniques explore network alternatives.

The base case retains2250MW output with275MW compensatory generation. Reported residual emissions752.5t/h imply0.33444t/MWh, consistent with the rounded0.334 table result. A separate350Mt capture/240Mt storage example exposes a110Mt storage deficit. Compensation and finite storage were therefore prior art well before Paper1.

Transfer limits: Illustrative power-sector values are not an industrial-source regional inventory. Aggregate relative costs simplify economics, and cumulative capacity is not a pressure-constrained annual forecast. The capture/post-retrofit source baseline and compensatory generation cannot be mixed with a different industrial service.

### B3-10 — Optimization of liquefaction cycles applied to CO2 coming from onshore pipeline to offshore ship transportation

. Identifier: 10.1016/j.ccst.2024.100280. [PDF](../papers/B3-10.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,8,14.

Process simulation compares closed refrigerant, open CO2 and hybrid liquefaction configurations for pipeline-to-ship interfaces. Composition, inlet pressure, cooling-water conditions, heat-exchanger pinches and refrigerant selection are explicit. Purification is needed to achieve the ship specification for impurity-containing feed.

Pure CO2 can liquefy near-28C at15bar, whereas studied impure streams require approximately26/44bar at the same temperature. Cooling-water temperature and exchanger approach strongly affect electricity demand. The paper gives cost/recovery tradeoffs and different suitable configurations by feed condition.

Transfer limits: No single kWh/t factor can be transferred without inlet/outlet state, purity and compression boundary. Electricity-price sensitivity is financial, not physical GHG. Pure/impure pressure figures retain original bar units; avoid unqualified barg/bara conversion or duplicate liquefaction/compression charges.

### B3-11 — Planning of carbon capture and storage with pinch analysis techniques

Ooi, Foo, Ng & Tan (2013). Identifier: 10.1016/j.cherd.2013.04.007. [PDF](../papers/B3-11.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 4,8.

Pinch-analysis storage supply/demand composite curves represent source and reservoir operating windows, cumulative loads and annual injection-rate limits. Time pinch and grand-composite curves identify extra storage needs and excess capacity before detailed source-sink pairing.

The examples show that excess cumulative capacity can coexist with a time-specific deficit. Detailed curves guide pairings while attempting to avoid unnecessary route changes. A reported case has40Mt additional storage needed at one time and80Mt total excess elsewhere; these are distinct time/location quantities.

Transfer limits: The illustrative constant rates and operating lives are imposed planning inputs, not reservoir forecasts or measured annual maxima. No voyage physics, local GHG or calibrated pressure data are supplied. Multiple examples on the same page must not be combined as one dataset.

### B3-12 — Large-scale CCS transport and storage networks in North-west and Central Europe

. Identifier: 10.1016/j.egypro.2011.02.176. [PDF](../papers/B3-12.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 2,5.

CO2Europipe clusters European point sources and sinks from Geocapacity/EPER databases and performs source-sink matching for future transport corridors. National and cross-border clusters are screened under reference, offshore-only and EOR scenarios; source inventories date to2005/2007.

The study illustrates how restricting onshore storage concentrates cross-border flows and demands parallel pipelines. It explicitly calls some750Mt/y corridor results unrealistic. Rough pipeline construction rates are calculations from projected network totals, not observed contractor schedules.

Transfer limits: Historical scenario forecasts for2020–2050 are not actual deployed routes or current available storage. The250kt/y source screening threshold is not a minimum capture-plant size. No full lifecycle inventory, reservoir-pressure validation or shipping operating calendar follows from clustered resources.

### B3-13 — Optimised deployment of a European CO2 transport network

. Identifier: 10.1016/j.ijggc.2011.11.011. [PDF](../papers/B3-13.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 2,8,12.

InfraCCS combines automatic source/sink clustering, candidate pipeline preselection, geographic routing and a tractable multistep network optimisation. Offset-linear capacity costing approximates pipeline economies of scale; a PRIMES/PowerChoices capture scenario drives deployment.

Contrasting planning assumptions change projected2050 network length and investment: the displayed cases give11,663km/16.5billionEUR and17,602km/37.2billionEUR. Shared coordinated deployment and timing are therefore established planning components.

Transfer limits: These are historical model projections rather than current pipeline inventories, actual permissions or independent injection capacities. Cost per tonne depends on a15% annual capital-charge convention, not a physical emission factor. Original code/network inputs remain necessary for full reproduction.

### B3-14 — A unified model for the deployment of carbon capture and storage

Lee, Tan & Chen (2014). Identifier: 10.1016/j.apenergy.2014.01.080. [PDF](../papers/B3-14.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,6,7.

Unified multiperiod MILP jointly selects capture retrofits, source-sink allocation and compensatory low-carbon generation under power-cost, timing, injection-rate and cumulative-capacity limits. Emissions from replacement power are deducted from capture benefits; decisions change at time-interval boundaries.

The illustrated carbon reduction saturates at68.44% once cost limits reach1.45 or above; additional nominal resource does not always improve storage if injection or cost constraints bind. Temporal source/sink overlap and retrofit technology can determine the allocation. This is direct prior art for matched-output compensation and time-dependent constrained mitigation.

Transfer limits: Dimensionless cost and synthetic plant/sink cases do not supply a regional industrial inventory. Static exogenous injection limits are not calibrated pressure feedback. Higher gross capacity can have no effect, so Paper1 must allow null effects rather than force a preferred route.

### B3-15 — Modeling a Carbon Capture, Transport, and Storage Infrastructure for Europe

. Identifier: 10.1007/s10666-014-9409-3. [PDF](../papers/B3-15.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 2,4,7,12.

CCTS-Mod minimises discounted capture/certificate, pipeline planning/capacity and storage-investment costs with source mass balances and discrete pipeline additions. It distinguishes treated versus emitted streams and annual injection capacity investment. Regional storage availability and carbon-price scenarios determine whether facilities join the system.

Restricted offshore-only storage materially changes rollout and total stored volumes. The model notes that data are difficult to verify and its94Gt storage representation may overestimate exploitable capacity because suitable small/deep/dispersed resources may be uneconomic.

Transfer limits: Historical cost/certificate scenarios are not current construction, commercial allocation or full lifecycle mitigation. Variable storage costs are treated as negligible relative to capital, which does not imply zero operating GHG. Annual injection investment remains an exogenous planning representation, not a calibrated reservoir forecast.

### B3-16 — Optimal well placement and brine extraction for pressure management during CO2 sequestration

. Identifier: 10.1016/j.ijggc.2015.07.025. [PDF](../papers/B3-16.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 2,3,9,10.

Constrained differential evolution couples injection/extraction well locations and time-dependent brine rates to reservoir models. It minimises produced-brine/injected-CO2 volume ratio, subject to no CO2 breakthrough at producers and pressure-buildup limits at specified impact zones/faults. Well drilling costs are excluded from the proxy objective.

For five heterogeneous realisations and a1MPa fault-pressure-buildup constraint, Table3 gives optimal constant no-brine injection rates1.968,2.739,3.229,2.061 and2.451Mt/y. Optimal brine extraction can support a higher target, but placement and heterogeneity affect extraction volumes and the active number of producers.

Transfer limits: These are source-model results, not measured annual deliverability or transferable Japanese pressure limits. The1MPa criterion is a pressure increase at impact zones, not an absolute injection-well cap. Brine treatment/disposal and drilling GHG must be independently quantified; the optimisation objective does not supply them.

### B3-17 — Underground carbon dioxide storage in saline formations

. Identifier: 10.1680/warm.2010.163.2.77. [PDF](../papers/B3-17.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,6,9,10.

Review of saline-formation trapping, multiphase/geochemical processes, leakage pathways and economics. It distinguishes structural/stratigraphic and residual trapping from dissolution and mineral precipitation, and explains capillary breakthrough/fracture constraints.

Storage safety depends on site-specific pressure, sealing and geochemical conditions. Its reproduced cost/design tables include computed well rates and disparate pressure/thickness/permeability scenarios; they are not operational field measurements. Mineral trapping depends on mineralogy and reaction kinetics rather than an assumed instantaneous permanent fraction.

Transfer limits: Global resource ranges and historical secondary costs are not annual service or current permits. Extreme calculated well rates require the original design assumptions before use. No universal retention fraction, leakage distribution or brine-management burden is extracted from narrative trapping descriptions.

### B3-18 — Screening and ranking framework for geologic CO2 storage site selection on the basis of health, safety, and environmental risk

. Identifier: 10.1007/s00254-007-0947-8. [PDF](../papers/B3-18.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 4,6,7.

Transparent screening/ranking framework scores primary containment, secondary containment and attenuation from weighted geological/surface properties. User-assigned quality and confidence scores are kept separate. Illustrative Rio Vista, Ventura and Mammoth Mountain cases compare known geological features.

The paper explicitly describes score boundaries as arbitrary and acknowledges that candidate-site characteristics were not directly measured for these demonstrations. Consistent weights are needed for comparisons; greater knowledge can improve the apparent desirability even without changing physical attributes.

Transfer limits: Ordinal quality/confidence scores are not leakage probabilities, physical containment guarantees or calibrated pressure limits. They can organise screening but cannot set a retention multiplier or a CVaR distribution. Historical examples do not establish available injection service.

### B3-19 — Comparison of methods for geologic storage of carbon dioxide in saline formations

. Identifier: 10.1016/j.ijggc.2013.07.016. [PDF](../papers/B3-19.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,8,12.

Applies six transparent high-level storage-resource methods to a common saline-formation dataset and compares both raw capacity and normalised overall efficiency. Methods differ in boundary assumptions, trapping mechanisms, permeability/lithology classes and sustainable-pressure treatment.

Open-boundary resource methods are often not statistically distinguishable for the tested formations despite different raw efficiency definitions. The study normalises by formation pore space before comparison, illustrating why copying method-specific efficiencies into another formula can misstate resource.

Transfer limits: It excludes site-specific project design and economic/legal access; only selected methods consider injectivity. Its uncertainty intervals are conditional on the common geological dataset and do not supply our local capacity probabilities or annual kr,t. Similar resource estimates do not establish similar safe injection rates.

### B3-20 — Hydraulic fracturing to enhance injectivity and storage capacity of CO2 storage reservoirs Benefits and risks

. Identifier: 10.1016/j.ijggc.2020.103105. [PDF](../papers/B3-20.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,6,10.

Reservoir simulations compare vertical/horizontal wells and fracture configurations in an Illinois-basin storage/seal model based on FutureGen characterisation. Geometry, permeability/fracture scenarios and pressure-limited injection determine stored mass and plume/trapping behaviour.

Table2 shows configuration-dependent cumulative injection and end-of-injection rates: the vertical case13.14Mt/0.68Mt/y versus a6k horizontal case17.54Mt/0.85Mt/y. Fractures can improve access but expand plume extent and possible interaction with conductive pathways; post-injection trapping mechanisms must be assessed separately.

Transfer limits: Simulated fractures are not a universal injectivity uplift or approved operating method. End rates and cumulative totals cannot recover an unreported annual curve. Increased storage must be assessed with sealing, fracture propagation, drilling and operating burdens, not only tonnes injected.

### B3-21 — Barriers or boosters the role of governance pathways in deploying offshore carbon capture and storage comparative implications from the EU and China

. Identifier: 10.3389/fmars.2025.1621290. [PDF](../papers/B3-21.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,9,14.

Comparative legal/governance analysis of EU and China offshore CCS uses doctrinal and discourse analysis through the Collingridge-dilemma lens. It examines binding rules, policy architecture, technology maturity, environmental safeguards and cross-sector coordination.

The study contrasts governance pathways rather than supplying a quantified causal deployment model. It proposes adaptive permitting, coordination and economic-incentive mechanisms and identifies unresolved liability, legitimacy and cross-border fragmentation questions.

Transfer limits: Policy statements and proposed governance instruments do not establish current authorisation for a named route. London-Protocol developments require jurisdiction/project-specific checks; the review does not allocate capacity or validate physical retention. No permitting delay, probability or emissions factor is inferred.

### B3-22 — Three layers of energy law for examining CO2 transport for carbon-capture and storage

. Identifier: 10.1093/jwelb/jwx035. [PDF](../papers/B3-22.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 4,13,20.

Three-layer energy-law framework compares international, national and local/permitting issues across four European CO2 transport development scenarios. It combines legal assessment with stakeholder engagement and distinguishes cross-border instruments, domestic regulation and local approvals.

The2017 legal matrix identifies different barriers for Germany, Belgium, the Netherlands, UK and Norway. Commercial readiness requires available CO2, legal pathways, supportive parties, storage access and a viable business plan; these are separate conditions, not substitutes for one another.

Transfer limits: The historical status matrix is not current legal advice or evidence of2026 route approval. Qualitative legal rankings are not quantified commissioning dates, delay distributions or contracted annual storage service. Current treaties, permissions and operator contracts must be verified independently.

### B3-23 — Optimization of CO2 injection and brine production well placement using a genetic algorithm and artificial neural network-based proxy model

. Identifier: 10.1016/j.ijggc.2023.103915. [PDF](../papers/B3-23.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,8,12.

Genetic-algorithm well-placement optimisation compares a reservoir simulator with ANN proxies and a proxy retrained using new simulator evaluations. The Pohang model tests injector/producer combinations and CO2 breakthrough; offline and online-updated proxy strategies are explicitly compared.

Table3.3 shows an offline proxy predicting11.38% improvement while full-physics reevaluation gives3.19%. Updating the proxy reduces disagreement between predicted and simulator-evaluated improvements. This directly supports evaluating a coarse-model selected decision under the more detailed model.

Transfer limits: Full-physics validation here is model-to-model, not field validation or proof of global optimality. Cumulative quantities are reported in10^8m3 with their source basis; they are not converted to tonnes without state/composition. The proxy training domain and well-layout constraints cannot be transferred as universal injectivity.

### B3-24 — CCS in the North Sea region A comparison on the cost-effectiveness of storing CO2 in the Utsira formation at regional and national scales

. Identifier: 10.1016/j.ijggc.2011.08.009. [PDF](../papers/B3-24.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,9,14.

Coupled/harmonised national MARKAL and regional TIMES-PanEU energy-system models compare least-cost CCS under energy-service demands, trade, fuel-price and storage scenarios. Optimisation uses perfect foresight and five-year steps from2010 to2050; key economic/technology assumptions are harmonised while national policies and demand can differ.

National and regional models yield different projected CCS deployment, partly from nuclear-policy, fuel/technology and trade assumptions. The discussed2050 captured quantities are474Mt in national runs versus569Mt in the regional model, with country-specific storage allocations.

Transfer limits: These are historical energy-system scenarios, not actual2050 operating commitments or a controlled CO2-route-only comparison. Differences cannot be assigned solely to transport or injectivity because energy mixes/policies also change. No ship fuel curve, site-pressure validation or current capacity allocation follows.

### B3-25 — Cost allocation in CO2 transport A multi-actor perspective A general model to evaluate costs in infrastructure construction

. Identifier: 10.1016/j.jclepro.2023.140271. [PDF](../papers/B3-25.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,9,14.

Component-based cooperative cost-allocation model represents heterogeneous network-user requirements and derives an equal-component sharing rule with scaling and coalitional-rationality properties. A stylised Rotterdam transport/conditioning network illustrates the component decomposition.

Tables map onshore/offshore radius, capacity classes and conditioning levels to shared components and player groups. The later cost tables explicitly use older ZEP/JRC estimates to demonstrate relative scaling, while warning that absolute costs may no longer be accurate.

Transfer limits: Requirement levels1/2 are categorical in several dimensions, not physical Mt/y or pressure. Cost-allocation fairness is distinct from physical feasibility, lifecycle GHG allocation or a commercial tariff. Do not use the tables as current asset-emission or capacity data.

### B3-26 — Reducing costs of carbon capture and storage by shared reuse of existing pipeline—Case study of a CO2 capture cluster for industry and power in Scotland

. Identifier: 10.1016/j.ijggc.2016.06.004. [PDF](../papers/B3-26.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,6,8.

Scottish industrial-cluster feasibility/cost study combines2014 point-source emissions, estimated technically capturable fractions, feeder connections and potential reuse of existing gas pipelines. It evaluates clustering and capacity expansion rather than inferring that all site emissions can be captured.

Table2 distinguishes5.68Mt/y emitted from4.19Mt/y estimated capture, with site-specific assumed fractions. Existing Feeder10 nominal unboosted3.5Mt/y and theoretical10Mt/y gas-phase capacities imply different infrastructure needs. Feeder8 availability is expressly unconfirmed.

Transfer limits: Historical source inventories and theoretical pipeline reuse are not current permission or contracted access. Capture fractions are engineering estimates, not a universal90% multiplier. CAPEX/cost savings are not lifecycle GHG, and boosting/conditioning requirements must be resolved before treating a reused line as available transport.

### B3-27 — Life cycle assessment of carbon capture and storage value chains A systematic, critical literature review

See supplied first page. Identifier: 10.1016/j.spc.2025.09.015. [PDF](../papers/B3-27.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 8, 9, 10.

Systematic review of 33 articles finds low comparability and omissions of transport, storage and monitoring; advocates clearer capture/conditioning inventories.

Transfer limits: Review literature values remain secondary until original sources checked. Abstract and body use different electricity-projection prevalence wording; do not infer exact counts.

### B3-28 — Carbon dioxide liquefaction and transport optimization for marine carbon sequestration A comprehensive review

. Identifier: 10.1016/j.rser.2026.116945. [PDF](../papers/B3-28.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 4,12,15,16.

Marine-CCS review covers CO2 phase/heat-transfer behaviour, liquefaction cycles, transport concepts, BOG recovery and integrated vessel control. It compares cold-energy, ammonia/refrigerant and other integrated options and distinguishes simulation studies from shipboard evidence.

The synthesis identifies coupled propulsion/reliquefaction/auxiliary modelling, standardised specific-energy boundaries and long-term sea trials as unresolved needs. Claimed benefits depend on ambient conditions, pressure, fuel-side cooling availability and impurities; many proposed controls remain simulation-based.

Transfer limits: Secondary cross-study percentage savings are not directly comparable to primary matched-feed cases. LNG/ammonia cold-energy benefits cannot be transferred to a distillate-only ship with no such integration. The review supplies neither actual voyage duty nor validated wave/operating limits for our design.

### B3-29 — Integrated modelling and simulation of liquefied CO2 tank and cargo handling system with new marine transportation greenhouse gas intensity

Jeon et al. (2026). Identifier: 10.1016/j.energy.2025.139624. [PDF](../papers/B3-29.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 4, 5, 6, 7, 8, 9, 10.

Coupled tank/CHS model compares venting, continuous and periodic reliquefaction with well-to-wake transport-work intensity; crossover depends on voyage duration and BOR.

Transfer limits: Already links dynamic tank operations, losses and GHG. The approximately 13-day result is case-specific, not a generic safe venting rule.

### B3-30 — Influence of system boundary conditions on the life cycle cost and carbon emissions of CO2 transport

. Identifier: 10.1016/j.ijggc.2023.103847. [PDF](../papers/B3-30.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,6,9.

Life-cycle shipping model explores interconnected LPG/CO2 cargo systems with four boundary conventions. Vessel engine work, lifetime utilisation, construction and operation feed emissions/cost calculations. One boundary treats both materials as cargo; another includes downstream LPG carbon/source and CO2 sink effects.

The reported combined-cargo shipping factor0.048tCO2/t-cargo has a different denominator/boundary from stored-source CO2. The CO2-only example reports0.67Mt emissions and7.43Mt transported over its lifetime. Changing financial discount rates changes costs/profit but leaves physical transported/emitted quantities unchanged.

Transfer limits: A multi-cargo factor cannot be inserted as a per-tonne-stored or universal international CO2 factor. Tanker operating-cost proxies and country electricity assumptions remain source-specific. Cargo carbon must not be reclassified as independent transport emissions or avoided source emissions without a matched counterfactual.

### B3-31 — Shared CO₂ capture, transport, and storage for decarbonizing industrial clusters

. Identifier: 10.1016/j.apenergy.2024.122775. [PDF](../papers/B3-31.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,4,5,6,10.

Industrial capture process models span target-stream5/10/15/94mol% CO2 and multiple flow scales. Low-concentration cases use30wt% MEA,95% design capture and natural-gas cogeneration supplying parasitic heat/electricity; high-purity cases use dehydration/compression with grid electricity and a small gas boiler. Capturing cogeneration CO2 is a distinct larger system.

Coupled mass/carbon/energy balances show why capturing cogeneration emissions increases capture equipment/load and changes the functional denominator. The text reports about3.6GJ/t heat for low-concentration MEA cases and93% HHV cogeneration efficiency(84%steam,9%electricity). Compression reaches86barg before pumping to 110 barg; these are not ship-liquefaction conditions.

Transfer limits: Cost correlations by concentration/technology maturity are not lifecycle factors. Simulation capacities are full8760h design equivalents, not actual plant calendars. Pretreatment is not physically generalised and key process/equipment details are in unsupplied SI. Do not add grid or heat-supply emissions on top of the same cogeneration supply or apply capture fraction twice.

### B3-32 — Investing in CO2 transport infrastructure under uncertainty A comparison between ships and pipelines

. Identifier: 10.1016/j.ijggc.2015.07.013. [PDF](../papers/B3-32.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,11,17.

Whole-chain financial comparison uses discounted NPV and real-options analysis for coal-plant capture, ship/offshore-pipeline transport and storage. Options include capture shutdown, abandonment and switching reservoir under uncertain prices, utilisation and storage volumes. Continuous liquefaction and batch shipping require temporary storage.

Flexible decisions can change project value and ship-versus-pipeline investment decisions. The financial model is compared with literature cost cases and shows why matching electricity/fuel assumptions changes reported levelised transport costs. Reservoir exhaustion and abandonment probabilities are conditional model outputs.

Transfer limits: Option values and financial scenario probabilities are not measured maritime reliability, pressure-limited injection or a lifecycle climate optimum. Historical2010-price component assumptions and20–40% flashed-gas recirculation descriptions do not imply atmospheric vent losses. Storage access and energy-state compatibility still need separate evidence.

### B3-33 — Ship transport—A low cost and low risk CO2 transport option in the Nordic countries

Kjärstad, Skagestad, Eldrup & Johnsson (2016). Identifier: 10.1016/j.ijggc.2016.08.024. [PDF](../papers/B3-33.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,8,14.

Nordic transport study compares ship and pipeline costs across volumes/distances, selected source hubs and alternative storage sites with different injectivity. It examines ramp-up, pipeline underutilisation and cluster scale using historical regional source inventories.

For a500km/10Mtpa pipeline example,25% utilisation for the first ten years increases specific cost from8.4 to16.1EUR/t versus immediate full utilisation. More injective distant sinks and flexible shipping can be financially attractive; outcomes depend on network/cost assumptions and buildup of connected volumes.

Transfer limits: These are cost and scenario comparisons, not whole-chain climate rankings. Early utilisation does not determine ship fuel intensity or weather availability. Historical sources and candidate sites do not establish current capture contracts or injection access; no economic break-even distance becomes a carbon break-even distance.

### B3-34 — CO2 maritime transportation

. Identifier: 10.1016/j.ijggc.2010.05.005. [PDF](../papers/B3-34.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,5,7.

Conceptual maritime chain uses HYSYS conditioning/liquefaction, a designed30,000m3 carrier, receiving/injection equipment and onshore/offshore options. Two storage-state alternatives and several refrigeration/propulsion options are compared; integer ship additions matter.

The selected economic case uses-30C/15bar. Offshore unloading/injection uses5.2MW in the stated design with a24hour maximum on-station constraint. Reported350km/1100km financial crossovers differ by offshore versus harbour-to-harbour pipeline comparison.

Transfer limits: The technical design and old-vintage cost assumptions do not establish an actual fleet, universal offshore availability or a carbon break-even distance. Vessel-specific pumping power cannot be applied throughout every phase or transferred to another tank size/state without engineering support. No wave shutdown probability is inferred.

### B3-35 — Ship Transport of CO2 Technical Solutions and Analysis of Costs, Energy Utilization, Exergy Efficiency and CO2 Emissions

See supplied first page. Identifier: 10.1205/cherd.5147. [PDF](../papers/B3-35.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 7, 8, 9.

2006 chain concept reports 142 kWh/t energy, 60 kWh/t minimum work and 1.4% direct CO2 burden under its particular electricity assumptions.

Transfer limits: 142 combines electrical and fuel energy; 1.4% assumes nearly zero-emission liquefaction power. Do not combine with modern grid factors twice.

### B3-36 — Benchmarking of CO2 transport technologies Part II  Offshore pipeline and shipping to an offshore site

See supplied first page. Identifier: 10.1016/j.ijggc.2014.06.019. [PDF](../papers/B3-36.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 3, 4, 5.

Compares offshore pipeline and shipping technically, economically and in climate impact across 200–2000 km and 2–20 Mt/year.

Transfer limits: CO2-avoided transport costing already exists; input pressure, geography, electricity and financial bases must match before using outputs.

### B3-37 — The impact of time-varying CO2 injection rate on large scale storage in the UK Bunter Sandstone

Kolster, Agada, Mac Dowell & Krevor (2018). Identifier: 10.1016/j.ijggc.2017.10.011. [PDF](../papers/B3-37.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 3, 4, 5, 7.

Bunter simulations find large multi-year injection-rate oscillations and ramp direction have little effect on long-horizon reservoir response for tested cases.

Transfer limits: Direct counter-evidence to assuming dynamics always matter. Injection sites can represent multiple wells; do not interpret 12 sites as 12 single wells.

### B3-38 — At what Pressure Shall CO2 Be Transported by Ship An in-Depth Cost Comparison of 7 and 15 Barg Shipping

Roussanaly, Deng, Skaugen & Gundersen (2021). Identifier: 10.3390/en14185635. [PDF](../papers/B3-38.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 3, 4, 7, 8, 9, 10.

7 versus 15 barg shipping comparison provides compatible density, liquefaction, ship fuel, fleet and port-time data over a range of capacities/distances.

Transfer limits: 7 barg is not 7 bara. Baseline capacity limits 50/10 kt; larger extrapolated designs are sensitivity assumptions. Boil-off is neglected.

### B3-39 — Linking the Effect of Reservoir Injectivity and CO2 Transport Logistics in the Nordic Region

Johnsson, Skagestad, Eldrup & Kjärstad (2017). Identifier: 10.1016/j.egypro.2017.03.1824. [PDF](../papers/B3-39.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1.

Nordic analysis links transport volume/distance and reservoir injectivity; longer shipping to better western reservoirs can be cheaper.

Transfer limits: Economic comparison, not a whole-chain climate ranking. Related B3-33 case evidence should not be double-counted.

### B3-40 — Estimating the pressure-limited CO2 injection and storage capacity of the United States saline formations Effect of the presence of hydrocarbon reservoirs

. Identifier: 10.1016/j.ijggc.2018.09.011. [PDF](../papers/B3-40.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,6,9.

Pressure-limited US saline-formation assessment assigns equally spaced injection wells and uses3D TOUGH2-ECO2N simulations with geological properties and an80%-of-fracture-pressure constraint. Injection fronts/interference, hydrocarbon-reservoir coverage and economic minimum-rate screens govern aggregate development scenarios.

The reported Group3-and-higher rates change from1596.8 to682.7 to273.7Mt/y across hydrocarbon-reservoir handling scenarios. The250kt/y/well cutoff is an economic-development filter, not a physical minimum. Pressure-limited capacity is distinct from pore-volume resource and depends on well-development assumptions.

Transfer limits: National aggregate rates and25km spacing do not establish site service, local fracture limits, existing wells or commercial access. Published simulation outputs are useful independent pressure-constrained benchmarks, but a complete annual kr,t array and underlying realisations are not supplied. Constant50-year development scenarios are not observed operations.

### B3-41 — Assessment of CO2 geological storage capacity of saline aquifers under the North Sea

See supplied first page. Identifier: 10.1016/j.ijggc.2021.103463. [PDF](../papers/B3-41.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 9, 11, 12.

441 candidate sites are assessed with pressure-limited well models; Table 5 reports about 440 Gt capacity and country-level rates.

Transfer limits: Table 5 total rate 22620 Mt/year does not equal country-row sum 14664; scope also includes oil/gas fields. HOLD aggregate annual total pending clarification.

### B3-42 — Carbon dioxide capture, transport and storage supply chains Optimal economic and environmental performance of infrastructure rollout

Becattini et al. (2022). Identifier: 10.1016/j.ijggc.2022.103635. [PDF](../papers/B3-42.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 2, 3, 5, 6, 7, 10, 11, 15, 16, 17.

Swiss yearly 25-year optimisation models emissions relative to business-as-usual, overseas storage and a delayed hypothetical domestic sink.

Transfer limits: Already covers yearly baseline emissions and domestic/foreign rollout. Fixed transport coefficients and simplified storage differ from detailed coupled operational deliverability tests.

### B3-43 — Risk management optimization framework for the optimal deployment of carbon capture and storage system under uncertainty

. Identifier: 10.1016/j.rser.2019.109280. [PDF](../papers/B3-43.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,7,11.

Two-stage stochastic CCS deployment framework compares expected cost with variability, probabilistic financial risk and downside-risk metrics. Discrete capture/network decisions couple scenarios, while epsilon constraints trace economic-versus-risk tradeoffs for uncertain carbon-tax conditions.

Risk-metric selection changes the types of costly scenarios penalised and the resulting design. Threshold-dependent probabilistic/downside criteria reflect decision-maker preferences; computational difficulty differs with binary risk indicators. The study motivates explicit risk definitions rather than an undefined generic uncertainty score.

Transfer limits: Financial scenario probabilities/subjective thresholds are not empirical failure probabilities, uncertain physical injectivity distributions or a probability of climate benefit. This is prior art for risk-aware planning, not site calibration or a complete lifecycle comparison. No distribution is imported into Paper1.

### B3-44 — A scalable infrastructure model for carbon capture and storage_SimCCS

. Identifier: 10.1016/j.enpol.2008.09.049. [PDF](../papers/B3-44.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,6,8.

SimCCS combines least-cost geographic candidate-network generation with a MILP for source/reservoir opening, discrete pipeline sizes and flow conservation. Source/sink bounds and a system-wide capture target are linked in one atemporal infrastructure decision.

The California demonstration uses37 major sources and14 oil-field reservoirs. Aggregation creates cost economies, but the paper explicitly states pipeline construction costs were artificially reduced to emphasise network capabilities. It also states the2009 model is atemporal and each target is reoptimised from scratch.

Transfer limits: Low transport cost is not a transferable realistic price or GHG factor. Approximate radial-injectivity/property formulas have stated domains and do not resolve time-dependent pressure fronts. Original site data/code are needed for exact case reproduction; later dynamic SimCCS versions are not the same original model.

### B3-45 — Optimal design of European supply chains for carbon capture and storage from industrial emission sources including pipe and ship transport

. Identifier: 10.1016/j.ijggc.2021.103372. [PDF](../papers/B3-45.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 4,9,13.

Europe-wide economic MILP designs capture at steel/cement/refinery sources, pipeline/ship routes and onshore/offshore storage. Country-specific versus collective European capture targets and storage restrictions are compared; sector-specific capture and multimodal costs enter the supply-chain objective.

Offshore-only scenarios require more expensive transport and injection despite similar capture cost. Country-level and Europe-wide targets can change which sources capture CO2, not merely their destination. The paper highlights transnational cooperation requirements alongside economic savings.

Transfer limits: Cost-optimal source selection changes composition, so it is not a matched-source climate comparison. Representing all CCS stages economically does not provide complete lifecycle GHG. Ship-unit-cost sensitivity and projected fleets do not validate operational schedules, pressure-constrained annual service or actual cross-border access.

### B3-46 — Progress and perspectives in source-sink matching for CCUS_A critical review

See supplied first page. Identifier: 10.1016/j.rser.2025.116313. [PDF](../papers/B3-46.pdf).

Reading stage: Duplicate publication; canonical B2-17. Checked sections: PDF pages 1. Duplicate publication of B2-17; excluded from unique counts.

Same title, authors and DOI as B2-17; files differ in byte hash but represent the same publication.

Transfer limits: Register both uploaded files and count one unique study; source version differences not assumed scientifically meaningful.

### B4-01 — Carbon capture and storage at Malaysia power plants Evaluation of its feasibility and requisite enablers

Nasir & Go (2024). Identifier: 10.1016/j.jclepro.2024.143173. [PDF](../papers/B4-01.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: pp1, methods/results screening.

Malaysia power-plant decarbonisation with electricity/carbon-price and solar scenarios. The abstract reports a potential 60% reduction in energy-sector emissions; this is a modelled national scenario, not a Japanese source baseline.

Transfer limits: National power-sector scenario; reported potential is not accessible storage service.

### B4-02 — Determination of optimal volume of temporary storage tanks in a ship-based CCS chain

Seo et al. (2017). Identifier: 10.1016/j.ijggc.2017.06.017. [PDF](../papers/B4-02.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: pp3–4,7–8,11.

Temporary tank size trades capital cost against production losses. The studied optimum equals the 11,801 m3 ship; different ship sizes can deliver the same availability at different lifecycle costs. No universal buffer ratio follows.

Transfer limits: Korean weather/equipment failure assumptions; excludes unexpected well/reservoir failure.

### B4-03 — Design and operation strategy of CO₂ terminal

Zahid et al. (2015). Identifier: 10.1021/ie503696x. [PDF](../papers/B4-03.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: pp1,3,6–7,9,11.

Dynamic terminal model covers loading, holding, unloading and emergency shutdown. BOG depends on geometry, insulation, ambient temperature, pressure and fill. Two 5,000 m3 tanks serve a 5 Mt/y design; four ships are used in its operational example.

Transfer limits: Pure CO2, conceptual terminal; pressure datum must be preserved.

### B4-04 — Environmental techno-economic assessment of CO₂ maritime transport and offshore sequestration

Park et al. (2026). Identifier: 10.1016/j.psep.2026.109188. [PDF](../papers/B4-04.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: pp1,4,6,9.

Compares offshore/onboard injection and onboard capture. The low reported case burden is 8.71 kgCO2/t, but source throughput differs across configurations; it is not adopted as a matched-source whole-chain factor.

Transfer limits: Gate-to-gate; onboard capture changes throughput/denominator. Financial sensitivity direction needs clarification.

### B4-05 — Flexible Superstructure Synthesis Approach for Multi-Region and Multi-Period CCS Network Design

Liu & Isafiade (2025). Identifier: 10.3303/CET25120042. [PDF](../papers/B4-05.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: pp1–6.

Multi-region, multi-period synthesis includes time availability, varying CO2 supply and stream quality; a hub supplies temporary storage and mixing. A reported 3% reduction in loss of profit is an economic result, not a climate result.

Transfer limits: Illustrative economic superstructure, not a measured international storage chain.

### B4-06 — Multi-period superstructure optimization for CCS source-sink matching in South Sumatra industrial clusters

Budiarto et al. (2025). Identifier: 10.1007/s43979-025-00135-w. [PDF](../papers/B4-06.pdf). [Supplement review](supplement_review.md).

Reading stage: targeted main-paper and supplementary tables/figures extraction. Checked sections: pp1,7–10,12,16; supplement B4-06-S1 Tables S1–S3 and Figures S1–S10.

Reservoir-constrained source–sink optimisation links well simulations, readiness and multi-well development. SW-A stores 153.21 Mt and MW-A/MW-D store 159.81 Mt. This supplies a coherent published retention benchmark, but no complete GHG inventory for additional wells/pressure management. Supplement now supplies 14 source rates/costs, 8 capacities/start years/costs, 46 hub distances, and 250 rounded annual injection annotations across three scenarios. Source rates sum to 5.327 Mt/y and 159.81 Mt over 30 years.

Transfer limits: South Sumatra simulation proxy. Supplementary inputs and annual MILP allocation heatmaps are supplied; annotations have one decimal precision. Exact raw allocation output and annual physical maximum injection limits kr,t are not supplied as tabulated data. Capture/well GHG inventory and full network/process inputs remain incomplete.

### B4-07 — Optimization and assessment of carbon capture, transport and storage supply chains for industrial sectors The cost of resilience

Gabrielli et al. (2022). Identifier: 10.1016/j.ijggc.2022.103797. [PDF](../papers/B4-07.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: pp1, methods,10.

MILP minimises costs and emissions under resilience requirements. Expected carbon not stored is evaluated with specified simultaneous failures. Foreign versus domestic storage changes the cost of resilience; this is close prior work for timing, emissions and service availability.

Transfer limits: Swiss waste-to-energy; cost increases are resilience scenario results, not probabilities or Japanese inventories.

### B4-08 — Regional opportunities for CO₂ capture and storage in Southeast Asia

Zhang & Lau (2022). Identifier: 10.1016/j.ijggc.2022.103628. [PDF](../papers/B4-08.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: pp1, regional screening.

Maps sources and storage in a 1,000 km Singapore-centred region. Reports 391 Mt/y stationary emissions and mid resources of 0.5/6.2/379 Gt in oil/gas/aquifers. Arun is a named candidate with 1.3 Gt resource, but annual deliverability remains unestablished.

Transfer limits: Prospective resource estimates, not annual injection limits, allocations or proof of commercial availability.

### B4-09 — Techno-economic analysis of large-scale CO2 ship transport with onboard boil-off gas reliquefaction

Noh & Kang (2025). Identifier: 10.1016/j.ijggc.2025.104337. [PDF](../papers/B4-09.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: pp1,3,5–7,11,13.

Seventy-five shipping cases cover 40/80/120 thousand m3 ships, 1–20 Mt/y and 1,000–20,000 km. Fleet counts are integer and BOG reliquefaction/terminal costs are explicit. Published fleet table is retained as model output; the inconsistent density is on hold.

Transfer limits: Table 1 density is conditionally selected and reproduces 75 source fleet cases. Conflicting prose remains unresolved; this is not independent thermophysical validation.


## Operational-model update

The new forward model uses a separate 30-row located parameter register, supplementary source/schedule datasets and declared structural conventions. It produces144 comparisons and 36 contrasts, plus equal-injection, added-vessel and fleet-adequacy controls. Complete lifecycle net avoided GHG remains uncomputed. Refer to the [operational-model scope](operational_model.md) and the current manuscript; this extends the earlier supporting benchmarks.

## Public reservoir/capture follow-up — 12 November 2026

The [new primary-source review](public_reservoir_capture_review.md) retains the Norwegian Offshore Directorate's Bjarmeland case CO2_BJ_C07B9 with its input dependencies, native summaries and source warnings. Its4,951 paired records obey a 225 bar absolute BHP ceiling; six initial records are pressure-limited below the 1.5 millionSM3/day target. This is an oil/water/gas model with production and boundary multipliers, not observed or maximum annual mass storage service. No tonnes or retained-carbon credit are inferred from standard volumes.

CEMCAP D4.2 Table 5.3 adds 42 located values and three complete paired reported MEA heat/work inventories. The design case uses 3.832GJ/t captured and 126.694kWh/t including compression, at 116.8°C/2.45bara steam and 110 bar product as printed. Cooling duty, solvent-solution makeup and process boundaries remain explicit. Actual utilities, upstream pretreatment/cooling supply and ship conditioning remain unverified; full facility/LCA coverage is not claimed. Firecrawl discovery and its credit-exhaustion fallback to native HTTPS downloads are recorded. Unverified parser-generated graph values and unmatched model inputs are excluded. Existing operating/GHG results remain unchanged.
