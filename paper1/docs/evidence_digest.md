# Evidence digest and coverage

The current library contains **93 supplied PDF files, 92 unique publications and 1,301 physical pages across the unique publications**. B3-46 is a duplicate publication of B2-17. File hashes and original filenames are preserved in the source catalogue. Reuploads of previously supplied titles reuse the already downloaded version; this package does not assert that every reuploaded binary was separately compared. The retained PDFs are authoritative for this draft.

**48 unique publications have targeted methods/results extraction; 44 have abstract/relevance screening.** Targeted extraction is selective, not an assertion that every number in every paper has been inventoried. This is a purposive supplied-library synthesis, not a completed systematic review. The Budiarto supplement is now supplied and reviewed; other unsupplied supplements remain outside the evidence base.

The extraction ledger contains **1,642 records**: 1,097 preserved earlier records plus 193 atomic records from the nine new papers and 352 numeric records from the Budiarto supplement (102 native-table entries and 250 printed annual allocations). Records may contain ranges or grouped cases and are not independent measurements. `curated_values.csv` contains 250 explicitly located quantities (including selected earlier values). `analysis_inputs.csv` contains 134 rows, of which 75 are published fleet counts and 59 support 49 calculations. The 124-row results file therefore contains **49 derived results and 75 directly reported fleet outputs**. Do not add overlapping tables together to count unique data.

The separate supplement tables and annual grid retain a further 352 numeric records and 470 blank figure cells. The new annual replay is additional to the original 49 benchmark calculations; its outputs are not a new MILP optimisation. The separate operational extension now implements B0–B3 with 144 comparisons, explicit service proxies and incomplete lifecycle accounting; see `operational_model.md`.

The broad extraction ledger is an audit trail, not a harmonised input file. Only the dedicated analysis inputs enter calculations. Source input, simulated result, observation and derived quantity must remain distinct. No source-wide transferability is implied by accepting a quantity for its stated context.

The original proposal, earlier preparation snapshot and earlier scaffold are retained separately. Current documents supersede historical assertions that Budiarto was missing or that no benchmark results existed. All 14 proposal reference identities are now linked to supplied primary PDFs; their original novelty claims do not all survive verification.

The Google Drive folder was not ingested: no callable Drive capability was available in this session. The uploaded planetary-limit ZIP exceeded the file-transfer tool's 32 MiB limit and could not be archived or inspected; the standalone planetary-limit PDF is in the library. No data from that ZIP are claimed as extracted.

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

See supplied first page. Identifier: 10.3389/fenrg.2024.1412770. [PDF](../papers/B2-02.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Distinguishes evolving foreground technologies from changing socioeconomic/energy backgrounds and proposes integration with IAM scenarios.

Transfer limits: Review-level recommendations, not an empirical energy coefficient or future grid trajectory for the proposed countries.

### B2-03 — Multi-period Carbon Capture, Utilization, and Storage (CCUS) infrastructure design and planning under uncertainty

See supplied first page. Identifier: 10.1016/j.compchemeng.2025.109300. [PDF](../papers/B2-03.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Multi-period stochastic Illinois Basin CCUS planning uses rolling horizons and period budgets with uncertain geological volumes and recourse pipeline investment.

Transfer limits: Cost and EOR revenue objectives; do not import EOR credits or scenario probabilities into permanent-storage comparisons.

### B2-04 — Optimizing carbon capture and storage infrastructure including physics-based reservoir modelling

Bertoni, Møyner, Wiegner & Gazzani (2025). Identifier: 10.1016/j.compchemeng.2025.109293. [PDF](../papers/B2-04.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 4, 5, 9, 10.

POD/trajectory-piecewise-linear reduced reservoir dynamics are embedded in a CCS MILP. Pressure prediction is reported within ±5%, with 500–1800-fold speedup versus tested full simulations.

Transfer limits: Already integrates dynamic physics and infrastructure; accuracy is case/training-region dependent, not a universal reservoir error bound.

### B2-05 — Beyond pipelines Multi-modal CO2 transport enables timely CO2 capture, transport, and storage deployment

See supplied first page. Identifier: 10.1016/j.ijggc.2026.104698. [PDF](../papers/B2-05.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Swiss pipeline diffusion constraints cause a modelled 9% sequestration deficit; other transport modes close it at a 5% cost increase.

Transfer limits: Transport-enabled additional sequestration already established. Scenario results are not Japanese operational evidence.

### B2-06 — Multiperiod strategic planning of CO2 capture, transport, utilization and storage with multimodal transportation

See supplied first page. Identifier: 10.1016/j.compchemeng.2025.109525. [PDF](../papers/B2-06.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Canadian strategic MILP includes ships, trains, trucks, pipelines, buffers, transshipment, fleet sizing and offshore injection, and tests temporal-resolution effects.

Transfer limits: Integration of these components alone is not new. Heuristic cost improvements depend on the computational comparison and instance.

### B2-07 — From point-to-point to hub-and-cluster a systematic review of co-optimization of source–sink matching and transport networks for large-scale CO2 sequestration

See supplied first page. Identifier: 10.3389/fenvs.2026.1966624. [PDF](../papers/B2-07.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

PRISMA review directly synthesises 17 studies; emphasises auditable feasibility and optimality reporting, utilisation, phased access and governance.

Transfer limits: Review summaries are secondary evidence; do not use them to certify a global absence of the proposed method.

### B2-08 — Optimal design and cost of ship-based CO2 transport under uncertainties and fluctuations

Bjerketvedt, Tomasgard & Roussanaly (2020). Identifier: 10.1016/j.ijggc.2020.103190. [PDF](../papers/B2-08.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 6, 7, 8, 12.

Brevik–Kollsnes case transports 0.4 Mt/year over 715 km; stochastic sailing, buffers and speed/power responses affect transport completion and cost.

Transfer limits: Buffer ratios depend on 99% versus 100% transport case and denominator. Table 2 labels design power W for 1500–2500 values; clarify before using as physical watts.

### B2-09 — Risk aware planning of CO2 transport and geological storage networks for net zero buildings under capacity and injectivity uncertainty

See supplied first page. Identifier: 10.1016/j.enbuild.2026.117200. [PDF](../papers/B2-09.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Synthetic network compares deterministic, Gamma-robust and CVaR designs; equal nominal derating can cause very different well/pipeline cost increments.

Transfer limits: Entire dataset is explicitly synthetic; no country-specific capacities, empirical probabilities or real sink availability.

### B2-10 — Exploring the value of CO2 shipping transport flexibility in international batchwise transportation carbon capture and storage networks

See supplied first page. Identifier: SSRN5070419 / GHGT-17. [PDF](../papers/B2-10.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 3, 4, 5, 6.

Fraga GHGT-17 assesses 15 what-if scenarios including six-year source/sink delays and network interconnection over 30 years.

Transfer limits: Implemented analysis minimises cost after capture. Model name includes multi-objective but this paper is not a whole-chain baseline climate assessment.

### B2-11 — A techno-economic assessment of CO2 capture in biomass and waste-fired combined heat and power plants – A Swedish case study

See supplied first page. Identifier: 10.1016/j.ijggc.2022.103684. [PDF](../papers/B2-11.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

110 Swedish CHP plants yield a modelled potential up to 19.3 Mt/year, with capture plus trucking to nearest harbour costing 45–125 EUR/t.

Transfer limits: Boundary excludes onward shipping and final geological storage; biogenic/waste mixture needs a different reference than a fossil-only source.

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

See supplied first page. Identifier: 10.1021/acs.est.5c14041. [PDF](../papers/B2-14.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

China 1 km-grid source–sink framework reports theoretical/effective capacity and onshore/offshore cost differences and shared regional corridors.

Transfer limits: Theoretical and P50 effective resource totals are not annual injectable commercial service. Full-chain costs differ from storage-only costs.

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

See supplied first page. Identifier: 10.1016/j.rser.2025.116313. [PDF](../papers/B2-17.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Reviews source, sink and matching methods and identifies data-scale mismatches, rigid networks and weak links to physical dynamic evolution.

Transfer limits: Same publication uploaded again as B3-46; count once. Review claims do not replace primary benchmark extraction.

### B2-18 — A prudent planetary limit for geologic carbon storage

See supplied first page. Identifier: 10.1038/s41586-025-09423-y. [PDF](../papers/B2-18.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 2, 3, 4, 5, 8, 10.

Risk-based geospatial screening estimates a central prudent planetary storage limit of 1460 GtCO2 with sensitivity 1290–2710 GtCO2.

Transfer limits: This is a precautionary scenario-dependent estimate, not a legal universal quota or site injection rate. Exclusions and conversion assumptions must accompany it.

### B3-01 — Carbon dioxide capture and storage—liability for non-permanence under the UNFCCC

See supplied first page. Identifier: 10.1007/s10784-006-9004-4. [PDF](../papers/B3-01.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Discusses responsibility for leakage and cross-border CCS under the UNFCCC and historical Kyoto mechanisms.

Transfer limits: 2006 legal analysis; no claim that its description is the current Japan/Malaysia/Australia legal regime. Liability is not a physical retention factor.

### B3-02 — Assessing a Liability Regime for Carbon Capture and Storage

See supplied first page. Identifier: 10.1016/j.egypro.2009.02.277. [PDF](../papers/B3-02.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

US-focused discussion combines existing tort/environmental liability with bonding, insurance and long-term stewardship funding.

Transfer limits: Historical policy proposal, not present applicable law or a quantified leakage probability.

### B3-03 — Critical review and recommendations for strengthening health and safety and major accident prevention regulations for carbon capture and storage in UK ports

See supplied first page. Identifier: 10.1016/j.ijggc.2025.104479. [PDF](../papers/B3-03.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Identifies UK port health/safety regulatory gaps for large-scale CO2 handling and recommends guidance and legislative changes.

Transfer limits: Jurisdiction- and publication-date-specific; does not establish Asian terminal permission or physical operating limits.

### B3-04 — Development of CCUS clusters in Croatia

See supplied first page. Identifier: 10.1016/j.ijggc.2023.103857. [PDF](../papers/B3-04.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Croatian assessment identifies three onshore clusters and prioritises eastern/central options while noting storage-characterisation gaps.

Transfer limits: Regional early economic screening; large theoretical resource does not prove storage deliverability.

### B3-05 — Optimizing carbon capture and storage CCS infrastructure development using a python tool for source-sink matching and cluster formation

See supplied first page. Identifier: 10.1016/j.jclepro.2025.146563. [PDF](../papers/B3-05.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Kazakhstan Python MILP compares full/partial redirection and clustering radii. Claimed cost and emissions outcomes depend on cluster geometry.

Transfer limits: Abstract ambiguously calls a quantity both net abated and emissions; reconcile definitions and units before numerical transfer.

### B3-06 — Assessing-the-cost-reduction-potential-of-CCUS-cluster-projects-of-coal-fired-plants-in-Guangdong

See supplied first page. Identifier: 10.1007/s11707-022-1030-1. [PDF](../papers/B3-06.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Three Guangdong coal plants are compared as standalone versus a 9 Mt/year cluster, with reported 15.92% unit-cost saving.

Transfer limits: Abstract says 300 million tonnes per plant while cluster totals 9 million; apparent scale error needs body/table reconciliation.

### B3-07 — Estimation of CO2 Transport Costs in South Korea Using a Techno-Economic Model

See supplied first page. Identifier: 10.3390/en8032176. [PDF](../papers/B3-07.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 6, 10, 11, 18.

At 1 Mt/year, route-specific pipeline/ship costs are about USD33/28 per tonne; at 3 Mt/year they are USD21/23.

Transfer limits: Pipeline 530 km and shipping 724 km are unequal routes. Printed 2800 kg/s as 1 Mt/year on p11 is inconsistent; hold injection rate.

### B3-08 — Optimum liquefaction fraction for boil-off gas reliquefaction system of semi-pressurized liquid CO2 carriers based on economic evaluation

See supplied first page. Identifier: 10.1016/j.ijggc.2012.05.016. [PDF](../papers/B3-08.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Optimises reliquefied fraction against energy costs, CO2 sale value and venting penalty; economic optimum reported 95.7–98.2%.

Transfer limits: This is a fraction of BOG in the studied process, not voyage load fraction, capture rate or geological retention.

### B3-09 — Planning of carbon capture storage deployment using process graph approach

See supplied first page. Identifier: 10.1016/j.energy.2014.08.060. [PDF](../papers/B3-09.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

P-graph planning already matches fixed-life source flows to capacity-limited sinks with earliest availability and capture retrofit penalties.

Transfer limits: Illustrative cases, not site data or marine operational energy model.

### B3-10 — Optimization of liquefaction cycles applied to CO2 coming from onshore pipeline to offshore ship transportation

See supplied first page. Identifier: 10.1016/j.ccst.2024.100280. [PDF](../papers/B3-10.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Pipeline-to-ship liquefaction/purification compares open, closed and hybrid cycles; impurities change recovery and energy.

Transfer limits: Reported 21.8–40.9 kWh/t refers to specified pipeline-feed states, not compression from an atmospheric captured stream.

### B3-11 — Planning of carbon capture and storage with pinch analysis techniques

Ooi, Foo, Ng & Tan (2013). Identifier: 10.1016/j.cherd.2013.04.007. [PDF](../papers/B3-11.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Graphical pinch approach matches source flows against sink availability, injection-rate and cumulative-capacity constraints.

Transfer limits: Hypothetical examples show these temporal constraints predate current optimisation models; no shipping/GHG model.

### B3-12 — Large-scale CCS transport and storage networks in North-west and Central Europe

See supplied first page. Identifier: 10.1016/j.egypro.2011.02.176. [PDF](../papers/B3-12.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Source–sink mapping anticipates extensive international transport corridors and timely aquifer characterisation.

Transfer limits: Historical projections to 2050 are scenarios, not a report of infrastructure now installed.

### B3-13 — Optimised deployment of a European CO2 transport network

See supplied first page. Identifier: 10.1016/j.ijggc.2011.11.011. [PDF](../papers/B3-13.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

InfraCCS estimates a 2015–2050 least-cost European pipeline network, with clustering and candidate-route preselection.

Transfer limits: Historical scenario costs and excluded-sink assumptions cannot be transferred directly to Asia.

### B3-14 — A unified model for the deployment of carbon capture and storage

Lee, Tan & Chen (2014). Identifier: 10.1016/j.apenergy.2014.01.080. [PDF](../papers/B3-14.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Unified model already includes variable source rates, finite injection/capacity, sink readiness and compensatory power for capture energy losses.

Transfer limits: Matched output and capture-energy adjustment are established. Marine operational utilisation and dynamic reservoir profiles still need a distinct test.

### B3-15 — Modeling a Carbon Capture, Transport, and Storage Infrastructure for Europe

See supplied first page. Identifier: 10.1007/s10666-014-9409-3. [PDF](../papers/B3-15.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

CCTS-Mod chooses capture, pipeline and storage investments and operating quantities given carbon prices/costs and capacity.

Transfer limits: Price thresholds are model outcomes conditional on assumptions, not current universal deployment prices.

### B3-16 — Optimal well placement and brine extraction for pressure management during CO2 sequestration

See supplied first page. Identifier: 10.1016/j.ijggc.2015.07.025. [PDF](../papers/B3-16.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Constrained differential evolution selects brine-extraction locations/rates under fault-pressure limits in a hypothetical California reservoir.

Transfer limits: Water volume, treatment and disposal burdens must accompany extra storage; no transferable universal improvement ratio.

### B3-17 — Underground carbon dioxide storage in saline formations

See supplied first page. Identifier: 10.1680/warm.2010.163.2.77. [PDF](../papers/B3-17.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Reviews hydrodynamic, residual, solubility and mineral trapping and uncertainty in saline capacity estimates.

Transfer limits: Older review; timescales and uncertainty preclude assigning a single permanent-retention fraction.

### B3-18 — Screening and ranking framework for geologic CO2 storage site selection on the basis of health, safety, and environmental risk

See supplied first page. Identifier: 10.1007/s00254-007-0947-8. [PDF](../papers/B3-18.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Spreadsheet framework ranks primary/secondary containment and attenuation using scores and uncertainty.

Transfer limits: Expert scores are not calibrated probabilities or numerical retained-mass factors.

### B3-19 — Comparison of methods for geologic storage of carbon dioxide in saline formations

See supplied first page. Identifier: 10.1016/j.ijggc.2013.07.016. [PDF](../papers/B3-19.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Six estimation methods applied to 13 saline datasets often give statistically indistinguishable prospective estimates relative to geological uncertainty.

Transfer limits: Prospective capacity comparison is not annual usable injection or proof methods are interchangeable at detailed site scale.

### B3-20 — Hydraulic fracturing to enhance injectivity and storage capacity of CO2 storage reservoirs Benefits and risks

See supplied first page. Identifier: 10.1016/j.ijggc.2020.103105. [PDF](../papers/B3-20.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Simulations report 13–71% capacity increases from fractures/horizontal configurations relative to an unfractured vertical base case.

Transfer limits: Do not confuse earlier-study 10–35% with this study's range; benefits include footprint/permitting risks, not free extra capacity.

### B3-21 — Barriers or boosters the role of governance pathways in deploying offshore carbon capture and storage comparative implications from the EU and China

See supplied first page. Identifier: 10.3389/fmars.2025.1621290. [PDF](../papers/B3-21.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Compares EU legal and Chinese policy governance pathways and argues for a balanced portfolio of legal/policy tools.

Transfer limits: Doctrinal comparison, not proof of route permission or current treaty status in proposed countries.

### B3-22 — Three layers of energy law for examining CO2 transport for carbon-capture and storage

See supplied first page. Identifier: 10.1093/jwelb/jwx035. [PDF](../papers/B3-22.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Examines four European cross-border scenarios at international, national and local law levels.

Transfer limits: Use to structure a route-feasibility register; historical European analysis is not applicable Asian legal advice.

### B3-23 — Optimization of CO2 injection and brine production well placement using a genetic algorithm and artificial neural network-based proxy model

See supplied first page. Identifier: 10.1016/j.ijggc.2023.103915. [PDF](../papers/B3-23.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

ANN plus genetic algorithm approximates Pohang injection/extraction placement with fewer simulator runs.

Transfer limits: Reported computational saving is case-specific, not an injection-rate gain or reservoir model accuracy guarantee.

### B3-24 — CCS in the North Sea region A comparison on the cost-effectiveness of storing CO2 in the Utsira formation at regional and national scales

See supplied first page. Identifier: 10.1016/j.ijggc.2011.08.009. [PDF](../papers/B3-24.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Energy-system comparison finds substantial projected use of shared Utsira storage; annual injection constraints may limit those flows.

Transfer limits: Regional market and climate-policy assumptions; annual flows and cumulative storage must not be conflated.

### B3-25 — Cost allocation in CO2 transport A multi-actor perspective A general model to evaluate costs in infrastructure construction

See supplied first page. Identifier: 10.1016/j.jclepro.2023.140271. [PDF](../papers/B3-25.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Component-based equal cost-sharing rule addresses heterogeneous users, scaling and coalitional rationality.

Transfer limits: Financial cost allocation does not by itself allocate physical flows, embodied GHG or avoided-emission credits.

### B3-26 — Reducing costs of carbon capture and storage by shared reuse of existing pipeline—Case study of a CO2 capture cluster for industry and power in Scotland

See supplied first page. Identifier: 10.1016/j.ijggc.2016.06.004. [PDF](../papers/B3-26.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Scottish Feeder 10 reuse case connects coastal/industrial sources with staged 2–8 Mt/year capture scenarios.

Transfer limits: Reuse suitability, available capacity and material compatibility need separate evidence at a new route.

### B3-27 — Life cycle assessment of carbon capture and storage value chains A systematic, critical literature review

See supplied first page. Identifier: 10.1016/j.spc.2025.09.015. [PDF](../papers/B3-27.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 8, 9, 10.

Systematic review of 33 articles finds low comparability and omissions of transport, storage and monitoring; advocates clearer capture/conditioning inventories.

Transfer limits: Review literature values remain secondary until original sources checked. Abstract and body use different electricity-projection prevalence wording; do not infer exact counts.

### B3-28 — Carbon dioxide liquefaction and transport optimization for marine carbon sequestration A comprehensive review

See supplied first page. Identifier: 10.1016/j.rser.2026.116945. [PDF](../papers/B3-28.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Synthesises liquefaction, alternative physical states, BOG management and energy integration and identifies demonstration-data gaps.

Transfer limits: Do not transfer broad review ranges without feed state, process boundary, operating case and primary reference.

### B3-29 — Integrated modelling and simulation of liquefied CO2 tank and cargo handling system with new marine transportation greenhouse gas intensity

Jeon et al. (2026). Identifier: 10.1016/j.energy.2025.139624. [PDF](../papers/B3-29.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 4, 5, 6, 7, 8, 9, 10.

Coupled tank/CHS model compares venting, continuous and periodic reliquefaction with well-to-wake transport-work intensity; crossover depends on voyage duration and BOR.

Transfer limits: Already links dynamic tank operations, losses and GHG. The approximately 13-day result is case-specific, not a generic safe venting rule.

### B3-30 — Influence of system boundary conditions on the life cycle cost and carbon emissions of CO2 transport

See supplied first page. Identifier: 10.1016/j.ijggc.2023.103847. [PDF](../papers/B3-30.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

LPG-tanker and linked-power-system comparison shows changing system boundaries affects costs, emissions and break-even carbon price.

Transfer limits: Carbon-price break-even is economic; distinguish from Paper 1's net-mitigation break-even. LPG co-service requires an explicit counterfactual.

### B3-31 — Shared CO₂ capture, transport, and storage for decarbonizing industrial clusters

See supplied first page. Identifier: 10.1016/j.apenergy.2024.122775. [PDF](../papers/B3-31.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Louisiana cluster integrates process-based capture costs with pipeline routing and evaluates shared capture versus transport.

Transfer limits: Cost savings and capture-stream concentrations do not establish climate benefit or cross-border deliverability.

### B3-32 — Investing in CO2 transport infrastructure under uncertainty A comparison between ships and pipelines

See supplied first page. Identifier: 10.1016/j.ijggc.2015.07.013. [PDF](../papers/B3-32.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Ships/pipelines are compared with abandonment, temporary shutdown and alternate-sink options under uncertainty.

Transfer limits: Flexibility changes project value but did not reverse preferred mode in the studied cases; do not assume flexibility always changes decisions.

### B3-33 — Ship transport—A low cost and low risk CO2 transport option in the Nordic countries

Kjärstad, Skagestad, Eldrup & Johnsson (2016). Identifier: 10.1016/j.ijggc.2016.08.024. [PDF](../papers/B3-33.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Small coastal sources and long routes favour ships; better western injectivity may justify 800–1300 km additional transport economically.

Transfer limits: Closely related to Johnsson 2017; not independent proof of longer routes delivering more lifecycle net mitigation.

### B3-34 — CO2 maritime transportation

See supplied first page. Identifier: 10.1016/j.ijggc.2010.05.005. [PDF](../papers/B3-34.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

30,000 m3 carrier logistics compare approximately 7/15-bar storage regimes and shore/offshore terminals.

Transfer limits: Older conceptual transport-cost thresholds depend on flow, route and assumptions, not universal climate thresholds.

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

See supplied first page. Identifier: 10.1016/j.ijggc.2018.09.011. [PDF](../papers/B3-40.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

US assessment accounts for pressure interference and exclusion buffers around hydrocarbon reservoirs when computing saline injection/storage potential.

Transfer limits: Pre-brine-extraction resource scenario, not developed service. Avoid regional capacity figures as project injection constraints.

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

See supplied first page. Identifier: 10.1016/j.rser.2019.109280. [PDF](../papers/B3-43.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Two-stage stochastic MILP studies carbon-tax uncertainty and financial risk measures with cost/risk trade-offs.

Transfer limits: Tax scenarios and financial-risk probabilities are not physical reservoir uncertainty distributions.

### B3-44 — A scalable infrastructure model for carbon capture and storage_SimCCS

See supplied first page. Identifier: 10.1016/j.enpol.2008.09.049. [PDF](../papers/B3-44.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

Integrated source, sink, capacity and pipeline routing minimises annualised capture/transport/storage cost in a California example.

Transfer limits: Foundational network planning; not a dynamic shipping LCA or matched-country net-mitigation experiment.

### B3-45 — Optimal design of European supply chains for carbon capture and storage from industrial emission sources including pipe and ship transport

See supplied first page. Identifier: 10.1016/j.ijggc.2021.103372. [PDF](../papers/B3-45.pdf).

Reading stage: Abstract/relevance screening; detailed inventory extraction pending. Checked sections: PDF pages 1.

European industrial CCS MILP includes capture, pipe/ship transport and on/offshore storage; national versus common targets affect costs.

Transfer limits: Cost per tonne and source selection differ from a fixed common-source climate comparison; geographic restrictions are scenario-specific.

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
