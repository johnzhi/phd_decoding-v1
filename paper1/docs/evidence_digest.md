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

Transfer limits: Comprehensive main-PDF reading is recorded separately in evidence/comprehensive_review/B1-03.json. Hold calibration: MJ/MWnet lacks an explicit time basis; Eq2/4 grid-factor branches and Eq8/9 normalisations need reconciliation; Eq11–13 confuse specific and power units. Coal loss percentages imply about 56.8% reference efficiency rather than the declared 37%; several complete NG graphic shares fail the 100% partition. Body p9 associates 3.6/8.43 Mt/year with near-100% capture at 90% capacity factor, whereas conclusion p10 says 95% capture; the earlier 90%-capture attribution was incorrect. Annual savings closely reconstruct captured mass; baseline power/composition and avoided emissions remain unresolved. Table3 combines different literature cases, not one complete matched utility balance. See total_efficiency_comprehensive_findings.md; disputed inputs remain excluded.

### B1-04 — CO2 Sequestration in Deepwater Sediments Offshore Japan

Pilisi, Ghorbani & Vasantharajan (2012). Identifier: CMTC-151756. [PDF](../papers/B1-04.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

Three ultra-deepwater Japanese sediment cases model shallow subseabed injection under high-pressure, low-temperature gravitational trapping. Table 3 (p10) specifies 5,000 tons/day for each case; injection lasts 25 years, followed by 225 years of migration simulation. Deeper/hotter injection can reverse the density advantage.

Transfer limits: Historical2012 hypothetical feasibility concept; comprehensive main-PDF reading is recorded separately. The prescribed5000reported tons/day is not pressure-constrained deliverability; ton definition, pressure datum, fracture controls, full GEM/GHG fields/boundaries and structural riser inputs are unavailable. Global mole-fraction plots with a positive colour floor do not establish zero mobility, retained mass or permanent safety. The80F supercritical statement differs from the paper own>88F condition; actual density/brine/EOS and deeper-case geometry require clarification. No current storage service, comparative safety proof or complete utility inventory inferred. See deepwater_japan_comprehensive_findings.md; original model and all cited dependencies remain unverified.

### B1-05 — Independent Study Addresses Causes of Challenges in Asia Pacific Flagship CCS Project

Carpenter; synopsis of Sabzabadi, Gladman & Billingsley (2025). Identifier: SPE-1225-0011-JPT; synopsis of SPE-225882. [PDF](../papers/B1-05.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

The synopsis attributes Gorgon constraints to water treatment/reinjection and pressure management rather than failure of CO2 containment. It reports August 2019 injection start, a design rate described as 150 kg/s or 4 Mt/year, and four water-production wells. More brine cannot be extracted if its receiving formation cannot accept treated water.

Transfer limits: Do not present the synopsis as the underlying full technical paper or an audited current operational dataset. It prints sustained injection as “1.6 tonnes per year” (p3); retain the text and flag the apparent scale/unit error. Do not silently replace it with 1.6 Mt/year. Continuous annualisation of 150 kg/s also differs from 4 Mt/year unless an operating factor is assumed.

### B1-06 — Openhole completion integrity analysis for life of CO2 injector well

Rashidi et al. (2024). Identifier: ARMA-IGS-2024-0222. [PDF](../papers/B1-06.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

An offshore Sarawak injector is assessed during drilling, brine displacement, injection and stoppages using stress, pressure and temperature outputs from a thermal/dynamic/geomechanical model. Cooling and changing wellbore support cause different shear/tensile failures over time. A perforated liner is selected instead of an unsupported openhole.

Transfer limits: Comprehensive seven-page reading is recorded separately in evidence/comprehensive_review/B1-06.json. Ppg gradient equivalents are not CO2 density or actual BHP; MD, TVDSS, SSTVD, pore/wellbore pressure and the Figure1 temperature variable require reconciliation. DoD percentages have an unspecified normalisation. Selected I-3 failure maps and a perforated-liner decision do not establish outage probability, annual rate loss, caprock leakage or permanent retention. Complete THM, stress/property/failure inputs, detailed2040 outputs and liner/field validation remain unavailable locally;15 printed sources plus four named dependencies remain unverified. See openhole_comprehensive_findings.md; no anonymous Malaysian-field join or accepted input promotion.

### B1-07 — Leveraging Oil and Gas Legacy for Advanced CCS in Japan Realistic CO2 Storage Simulation in the Higashi-Niigata Gas Field

Kukuu et al. (2025). Identifier: 10.2118/225812-MS. [PDF](../papers/B1-07.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

Higashi-Niigata models 100 geological realisations, selecting 10 after history matching. Case A uses three CO2 injectors; Case B adds three pressure-relief wells. Injection is assumed from 1 January 2029 to 1 January 2050. Case A reaches its pressure limit around 2040; pressure relief increases injection volume by approximately 25–30% (p8).

Transfer limits: Comprehensive11-page reading is recorded separately in evidence/comprehensive_review/B1-07.json. History/forecast numerical vertical scales are absent. Figures11/17 label CO2_ton while captions call it volume; Figure19 labels MPa without a numerical scale/datum. Initial-reservoir-pressure value/reference/control is undisclosed. Relative25–30% cumulative uplift cannot supply absolute capacity, annual rates, a2040shutdown rule or netGHG benefit. Curves end around2060 despite a2130model horizon; map High/Low variable/final timestamps and tiny labels need native outputs. Match/model/relief-water arrays and original-source verification remain open. See higashi_niigata_comprehensive_findings.md; no unscaled curves promoted to accepted inputs.

### B1-08 — Unlocking CO2 Injection in Depleted Reservoirs A Flow Assurance Modeling Approach for Carbon Capture and Storage

Charoensuk et al. (2025). Identifier: 10.4043/35887-MS. [PDF](../papers/B1-08.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

A Sarawak development targets up to 2.0 Mt/year through a 40 km offshore pipeline into shallow/intermediate/deep depleted reservoirs. Early-life thermal/hydraulic limits constrain the shallow case to 37.5% and deep case to 80% of well design capacity under specified conditions. An insulated pipeline is selected over offshore heating and gas-phase transport.

Transfer limits: Comprehensive13-page reading is recorded separately in evidence/comprehensive_review/B1-08.json. This is a sour-gas development design/forecast, not observed service or imported JapaneseCO2 access. The37.5%shallow and80%deep limits use own-well design capacities under statedP/T, not the up-to2MTPA system target or annual/lifetime factors. Preserve gauge labels including73barg; exact mixture/OLGA inputs, corrosion comparison/test basis and temperature/pressure controls remain unverified. U-value is not insulation thickness, SimilarGHG is notzero, and the2h warm-restart window is not outage availability. Gas-phase costs/energy require changed wells/tubing for equivalent service; no fullTEA/utility/GHG inventory is reproduced. See flow_assurance_comprehensive_findings.md; accepted inputs remain unchanged.

### B1-09 — 4-D Geomechanics Modelling for Potential CO2 Storage Site in Malaysia – Fault Reactivation and Maximum Pressure Injection Limit

Nik Kamaruddin et al. (2019). Identifier: IPTC-19491-MS. [PDF](../papers/B1-09.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

A Malaysian carbonate Field X model uses field subsidence and laboratory-derived compaction/creep properties. It recommends maximum injection reservoir pressure of 4,000 psi with a 600 psi safety margin, while minimum horizontal stress during injection is 4,600–6,200 psi (p13).

Transfer limits: Comprehensive 14-page reading is recorded separately in evidence/comprehensive_review/B1-09.json. The 4000 psi reservoir-pressure recommendation and 600 psi lower-Shmin difference are not flowing BHP, annual maximum mass service or a transferable fracture limit; pressure basis/datum and total-XX-to-Shmin mapping remain unresolved. Eleven correlations lack explicit Phi scale/range and full creep time/law. Calibration is not independent validation; local maximum strain differs from cited average/incremental compaction. Four displayed affected faults versus five in the conclusion, citation years/geographic support and excluded cement/casing-caprock leakage remain open. Eight originals plus five model/data dependencies and external assets are unverified; full models unreproduced. Proposed 2024 start is a 2019 scenario. See malaysia_geomechanics_comprehensive_findings.md; no accepted input promotion.

### B1-10 — A Decision Framework for CO2 Storage Site Selection in Depleted Reservoirs

Hamid (2026). Identifier: 10.4043/36331-MS. [PDF](../papers/B1-10.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

A modified/anonymised four-reservoir screening case uses annual dispatch, pressure-tank and hydraulic relations. Text quotes up to10Mt/year over20years, a five-year ramp and230/148millionUSD baseline/Far-only costs. Comprehensive inspection finds conflicting ramp timing, BHP curve identity and Figure6 cost endpoint; quoted values remain separate from approximate graphics.

Transfer limits: Comprehensive 14-page reading is recorded separately in evidence/comprehensive_review/B1-10.json. Average reservoir pressure is constrained while BHP explicitly exceeds fracture pressure; allocations are not demonstrated safe annual service. Complete modified reservoir/PVT/cost/control inputs and global MILP/PSO are absent. Eq5 radial geometry, power/tariff/CAPEX units, marginal-cost construction, within-step mass/pressure closure and persistent pipeline sizing/costs need clarification. Figure4 ramp, Figure8 Mid1/Mid2 identity and Figure6 endpoint conflict with prose. Two retained citation edges have scoped primary checks; other originals/assets remain open. See site_selection_comprehensive_findings.md; no saving, annual rate or GHG promotion.

### B1-11 — Systematic Feasibility Assessment of Geomechanical Risks for CO2 Injection and Long-Term Storage Incorporating Rock Properties Degradation and Thermal Effects

Tan, Musa & Nik Kamaruddin (2024). Identifier: ARMA-IGS-2024-0183. [PDF](../papers/B1-11.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

An offshore Peninsular Malaysia Field X assessment uses eight offset wells and an analytical caprock/fault workflow. With estimated 50°C cooling, recommended pressures for Seals A–D fall from 2153/2731/3264/3701 psi to 1632/2209/2739/3178 psi (pp5–6, Tables 2–3).

Transfer limits: Comprehensive nine-page reading is recorded separately in evidence/comprehensive_review/B1-11.json. No site mechanical tests; synthetic shear/log correlations and assumed ECD limit calibration. Preserve psi/psia headers. Conditional safety-rule replay leaves a75.33psi residual for cooledSealA; do not repair2110/1632. Repeated Table3, Figure5 injection-level,0.18/0.19m maximum and Cm/deformation percentile mapping remain unresolved. Eq5 thickness/displacement semantics and deformation signs/geometry need originals/native code. Database26%E/strength and10%nu changes produce nonuniform results,not a universal37%factor. All19 cited originals plus six dependencies remain open. See thermal_geomechanics_comprehensive_findings.md; quoted pressure-pair arithmetic only,not validated annual service,facility safety,retention orGHG.

### B1-12 — Geomechanical Evolution of the South-West Hub Carbon Capture and Storage Reservoir in Western Australia

Hosseinzadeh et al. (2026). Identifier: 10.2118/234571-MS. [PDF](../papers/B1-12.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

South-West Hub/Harvey modelling describes a conceptual 800,000 tCO2/year, 30-year plan, nine injection wells and a reference BHP constraint of 360 bar at 2948 m (p18). No significant fault failure is predicted for the modelled isothermal pressure-driven response.

Transfer limits: Comprehensive26-page reading is recorded in evidence/comprehensive_review/B1-12.json:17 figures,3 tables,13 numbered equations and90 limited checks. Literal Eq13 has an asymmetric strain coefficient; strain scale, sonic/modulus units, G/bulk/static-dynamic basis and native property selection remain unresolved. Figure10 left legend800psi versus caption500,37/32 ratio1.15625 versus quoted1.125,LOT/FIT/depth/gradient-reference questions and inconsistent cell/calendar labels are retained. One-way isothermal model excludes caprock volume and cooled nearwell/near-seal conclusions. Nominal800000t/year,24Mt,360bar and1000y plume target are not calibrated maximum service or retained mass. All99 originals plus19 dependencies and external assets remain open; full native models unreproduced. See south_west_hub_comprehensive_findings.md; no accepted input promotion.

### B1-13 — Optimising the CO2 Storage Potential in Deep Saline Aquifer by Creating Pressure Sink

Razali et al. (2024). Identifier: 10.4043/34777-MS. [PDF](../papers/B1-13.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

A Malaysian restricted aquifer (K reservoirs, Z field) is simulated with and without brine production. Cumulative effective gas volumes are 4.9 Bscf without production, 80.13 Bscf with one injector/one producer, and 95.44 Bscf with two injectors/one producer. These are about 3%, 51% and 61% of theoretical volume (pp8–13).

Transfer limits: Comprehensive14-page reading is recorded in evidence/comprehensive_review/B1-13.json:15 figures,8 raster tables,one numbered equation and132 limited checks. Six pressure recommendations match the1.5 delta-margin rule within.4psi,not native geomechanical validation. Bulk*NTG net volumes are rounding-compatible; net*phi does not reproduce printed pore volumes on a common assumed region/property basis. Bg/Swirr/standard conditions,pressure/datum/control mapping,screening legend/stages and workflow template identity remain unresolved. Effective capacity is cumulative injection,not verified retainedCO2; brine and producedCO2 fates/inventory are missing. Preserve authors non-proceed recommendation. Four originals plus13 dependencies and external assets remain open; Petrel/GEM/failure models unreproduced. See pressure_sink_comprehensive_findings.md; no annual service,mass orGHG promotion.

### B1-14 — Fully coupled inversion on a multi-physical reservoir model – Part II The Ketzin CO2 storage reservoir

Wagner & Wiese (2018). Identifier: 10.1016/j.ijggc.2018.04.009. [PDF](../papers/B1-14.pdf).

Reading stage: Targeted methods/results extraction. Checked sections: See Batch1 studies/values.

Ketzin inversion jointly uses hydraulic/CO2 pressure, arrival times and geoelectric observations. A near-injector permeability reduction to about 15 mD (roughly eightfold) and equivalent skin of 10 explain pressure overburden attributed to salt precipitation. Observed/modelled arrivals are 21.7/21.8 days and 271/283 days (p6).

Transfer limits: Comprehensive nine-page reading is recorded in evidence/comprehensive_review/B1-14.json:8 figures,2 tables,no own numbered equations,12 analyst/prose identities and68 limited checks. Preserve barrier nonexclusion after two suspect histories are removed. ERT cost downweight10,mean/median mapping,lower-bound n,unpublished SCAL,pressure-difference offsets and550/640m datum correction limit verification. Static skin10.1,local15mD/factor8 anddoubled pressure are conditional equivalents,not annual-rate factors. Figure1 core/axis scale andcaption colour questions remain open. One scoped Class2015 citation check supports sensor/calibration caveats andshared observed arrivals;38 originals plus8 dependencies andessential PartI/native inversions remain unverified/unreproduced. See ketzin_inversion_comprehensive_findings.md; no maximum service,retention,safety orGHG promotion.

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

Wang, Robinson & Papadokonstantakis (2024). Identifier: 10.3389/fenrg.2024.1412770. [PDF](../papers/B2-02.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 11,12,13,20.

Review of prospective TEA/LCA across technology maturity, scale-up, hybrid costing and foreground/background scenarios. Table2 distinguishes prospective from dynamic LCA; later sections discuss semantic matching between IAM technologies and LCI processes and the need for transparent model assumptions.

Comparisons depend on maturity, energy integration, functional-unit matching and future backgrounds. The review reports a cited heat-integration study where annual averaging differs materially from multi-period optimisation. A process in an integrated-assessment model need not map unambiguously to one inventory activity.

Transfer limits: All26 main pages, seven figures, three tables, two numbered equations, glossary and192 references read/inspected under the comprehensive standard. The93-claim record and31 limited diagnostics reconstruct learning components, not native DAC/LCA/IAM or feedback models. Eq2 expanded denominator, Table1 capacity/cost/storage bases, Table3 units, announcement/operating status, TRL bands, carbon fate and citation attributions remain qualified. All192 originals and ten dependencies remain unverified. No complete same-case capture-to-ship utility, pressure-constrained reservoir service or lifecycle/retention input follows. See prospective_assessment_comprehensive_findings.md. Static official factors alone do not constitute complete prospective backgrounds.

### B2-03 — Multi-period Carbon Capture, Utilization, and Storage (CCUS) infrastructure design and planning under uncertainty

Aras & Hasan (2025). Identifier: 10.1016/j.compchemeng.2025.109300. [PDF](../papers/B2-03.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,7.

Annual-budget deterministic and two-stage stochastic CCUS deployment MILPs with rolling horizons and sample-average approximation. Source/sink selection, start times and single source-sink pipelines are decisions. After a connection is chosen, annual transported quantity is constant. Geological storage volumes are uncertain inputs; full capture is imposed at selected sources.

The Illinois Basin case compares network decisions under capacity uncertainty. The stochastic design reduces the reported mean shortfall from4,795kt to145.24kt per scenario over plant operating lives. It evaluates fixed designs on5,000 scenarios, rather than inferring a generic probability of storage success. The analysis already combines temporal planning and uncertain sink capacities.

Transfer limits: All11 pages,eight figures,35 numbered equations,two algorithms and both nomenclature/symbol objects read/inspected under the comprehensive standard.30 limited checks retain printed operating-cost sign,free sink index,remove-before-reserve and argmin/max questions; stock/rate/lifetime,recourse,statistical-bound and endpoint-rounding issues remain open. Two scoped exact-original checks support SimCCS/InfraCCS method context only;29 other originals,ten dependencies and the explicit publisher supplement remain unverified. No native Illinois/Gurobi/SAA/CDF or full physical/lifecycle model reproduced. Mean lifetime deviations are not annual reliability or retention factors. See stochastic_deployment_comprehensive_findings.md; no accepted operating/GHG input changes.

### B2-04 — Optimizing carbon capture and storage infrastructure including physics-based reservoir modelling

Bertoni, Møyner, Wiegner & Gazzani (2025). Identifier: 10.1016/j.compchemeng.2025.109293. [PDF](../papers/B2-04.pdf).

Reading stage: Targeted sections and quantitative extraction. Checked sections: PDF pages 1, 4, 5, 9, 10.

POD/trajectory-piecewise-linear reduced reservoir dynamics are embedded in a CCS MILP. Pressure prediction is reported within ±5%, with 500–1800-fold speedup versus tested full simulations.

Transfer limits: All12 pages,five figures,three tables,34 numbered equations,inline relations and nomenclature read/inspected under the comprehensive standard.35 limited checks use reported dimensions/timings and disclosed synthetic projected/selector/unit/pressure/pump cases. Typical±5% is well-cell simulator comparison,not a BHP/retention/global error bound. Source admits non-strict mass conservation andleaves pressure-dependent pipeline capacity tofuture work. Printed indices,bounds,time/flow/density/datum andpump-fit scope remain open. Two scoped originals support infrastructure context;29 other sources,eleven dependencies andexplicit SI unverified. No native MRST/AdOpT/validation,pump fit,physical service orcomplete utility inventory reproduced. See reservoir_rom_comprehensive_findings.md;accepted numeric inputs remain unchanged.

### B2-05 — Beyond pipelines Multi-modal CO2 transport enables timely CO2 capture, transport, and storage deployment

Burger, Shu, Bardow & Sansavini (2026). Identifier: 10.1016/j.ijggc.2026.104698. [PDF](../papers/B2-05.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 3,7,8.

Transition-pathway MILP models technology lifetimes, capacity additions, multimodal flows and speed-of-pipeline-deployment limits. Stored CO2 targets include direct source-stream losses; lifecycle burdens are represented in the model but excluded from the sequestration balance in Eq6. Storage is modelled as a service with annual/cumulative limits and operating costs/emissions, without explicit storage investment.

Constraining pipeline expansion produces unmet storage targets, while barges/ships bridge deployment limits. Early pipeline utilization is low; temporary multimodal capacity changes the transition even when final infrastructure looks similar. The body reports4.8Mt cumulative shortfall but Figure3 caption says1.7Mt, so that benchmark is held pending reconciliation.

Transfer limits: All 12 pages, six figures, two tables, 14 numbered equations and 73 references read/inspected under the comprehensive standard. Forty-nine limited checks reconstruct temporal/cost components and disclosed analyst cases, not the native Swiss optimization. The 4.8/1.7 Mt gap remains unresolved; period weights, CAPEX/annuity lineage, levelized-cost denominator and scenario-specific utilization need native checks. Two originals have scoped support; 71 other originals, ten dependencies and public code/data/SI remain unverified. Stored policy mass excludes lifecycle burdens; service-only storage and generic capture provide neither pressure-constrained service nor a complete same-case utility inventory. See pipeline_diffusion_comprehensive_findings.md; accepted numerical inputs remain unchanged.

### B2-06 — Multiperiod strategic planning of CO2 capture, transport, utilization and storage with multimodal transportation

Ayotte-Sauvé et al. (2026). Identifier: 10.1016/j.compchemeng.2025.109525. [PDF](../papers/B2-06.pdf).

Reading stage: Targeted methods/results extraction (follow-up full-text review). Checked sections: Selected full-text passages; physical PDF pages 6,15,19,22.

Multiperiod strategic CCUS MILP includes gas/liquid/supercritical state changes, buffer balances, capture units, pipeline capacity choices and truck/rail/ship fleets, including direct offshore injection and floating storage interfaces. Yearly decisions are identical within a planning period; vehicle activity includes berth and travel/loading constraints. An illustrative Eastern Canada network uses GIS-based candidate links and a heuristic to reduce computational burden.

Time discretisation and transshipment constraints affect feasible infrastructure. Limiting emitter vehicle loading/unloading to5Mt/y prevents concentrating49.4Mt/y of train-to-offshore-pipeline transfers at one emitter. The constrained example uses trains, pipelines and a40kt ship delivering779kt/y in the last two years. The authors explicitly call the costs/geographic weighting illustrative while Canadian data are being developed.

Transfer limits: All 27 pages and internal Appendices A–D read/inspected, including 14 figures, Table D.1, 78 numbered equations and 65 references. Ninety-nine limited checks, 120 stipulated target rows and 30 reported performance pairs do not reproduce the Canadian GAMS/CPLEX model, heuristic or six benchmarks. Printed process indices, inventory period duration, target wording, algorithm references, cost/domain and daily feasibility questions remain open. The source explicitly treats Canadian terrain costs/results as illustrative and acknowledges that time partitions change cumulative service. Two originals have scoped support; 63 other originals and 12 dependencies remain unverified. No calibrated pressure service, actual schedules, complete same-case utilities or retained-carbon input follows. See multimodal_strategy_comprehensive_findings.md; accepted numerical inputs remain unchanged.

### B2-07 — From point-to-point to hub-and-cluster a systematic review of co-optimization of source–sink matching and transport networks for large-scale CO2 sequestration

Hu, Wu, Yang & Zhou (2026). Identifier: 10.3389/fenvs.2026.1966624. [PDF](../papers/B2-07.pdf).

Reading stage: Detailed retained-PDF audit with open scientific verification. Checked sections: All 24 physical pages, figures, tables, equations and end matter; no paper-completion claim.

PRISMA-guided source-sink/network co-optimisation review distinguishes contextual references from17 direct-evidence studies. Its extraction protocol codes system boundary, decisions, uncertainty, scale, computational reporting and limitations. It distinguishes sequential, monolithic and decomposition approaches and separates demonstrated methods from prospective AI/digital-twin capabilities.

The review argues for auditable feasibility/objective/runtime/gap reporting and matched static/perfect-information controls. Its proposed future scale benchmarks and digital-twin/learning directions are evaluation priorities, not verified achievements. Cross-study evidence does not support a universal algorithm ranking.

Transfer limits: All 24 pages, 11 figures, six tables, 13 distinct displayed relations and 86 bibliography entries read/inspected. Forty-nine limited checks reconcile screening counts and analyst examples without reproducing search selection or any cited native model. The exact queries, exclusions and 17-study matrix are in an unretained supplement. Rate/stock, cost-time and graph links remain unresolved. Two scoped original checks qualify SimCCS dynamic/capture/solver attribution and Budiarto Pareto/LCA/entry-exit scope. Eighty-four other originals and twelve dependencies remain unverified. Prospective AI, quantum and national benchmark proposals are not achieved operating capabilities. See [detailed findings](cooptimization_review_comprehensive_findings.md); accepted numerical inputs remain unchanged.

### B2-08 — Optimal design and cost of ship-based CO2 transport under uncertainties and fluctuations

Bjerketvedt, Tomasgard & Roussanaly (2020). Identifier: 10.1016/j.ijggc.2020.103190. [PDF](../papers/B2-08.pdf).

Reading stage: Detailed retained-PDF audit with open scientific verification. Checked sections: All 13 pages, internal Appendix A, the Appendix B notice, figures, tables, equations, end matter and bibliography.

Brevik–Kollsnes case transports 0.4 Mt/year over 715 km; stochastic sailing, buffers and speed/power responses affect transport completion and cost.

Transfer limits: B2-08 adds all 13 pages, 12 figures, six tables, 24 main/appendix numbered equations, 52 claim records, 73 limited checks and 78 conditional speed rows. Printed receiving signs, minimum inequality, time/power/cost units, buffer cases and seasonal/information limits remain open. One scoped Roussanaly2014 check brings citation edges to nineteen; 43 other printed entries, twelve dependencies, explicit SI and native stochastic/weather/process/fault models remain unverified. No accepted operating or GHG input changes. Perfect17-day foresight and separate cyclic seasons qualify operational adaptation and seasonal-storage conclusions.99%case5120t=102.4%ship differs100%case5890t=117.8%; no universal18%margin. Cost-only prices/PFD do not supply complete capture heat/work/cooling or pressure-constrained storage service. See [detailed findings](stochastic_shipping_comprehensive_findings.md).

### B2-09 — Risk aware planning of CO2 transport and geological storage networks for net zero buildings under capacity and injectivity uncertainty

Kattel et al. (2026). Identifier: 10.1016/j.enbuild.2026.117200. [PDF](../papers/B2-09.pdf).

Reading stage: Detailed retained-PDF audit with open scientific verification. Checked sections: All 19 pages, figures, tables, numbered/inline equations, parameter and variable definitions, declarations and 71-entry bibliography.

The synthetic five-source/one-hub/two-sink network fixes integer initial pipes and wells while annual operation responds to economic and scenario inputs. Separate variants use hard-target fractional coefficient derates and soft-target CVaR penalties. The displayed Gamma constraints do not contain a shared cardinality budget controlling how many components degrade. Five equal-probability common-factor scenarios at alpha 0.95 make annual CVaR a maximum scenario loss, rather than a measured 5% failure frequency.

Rounded Sankey replay closes at 822.46 Mt with 117 wells and 911.44 pipe-km. Blue source boxes are gross emissions, not captured flows; magnification confirms the S5 ribbon as 78.9 Mt. Source salvage/fixed OPEX and rounded cost percentage claims reconcile at stated precision. High-lambda mean shortfall remains approximately 15 Mt/year, about 36.6% of the 40.95036 Mt/year target; this is neither a probability nor a delivery guarantee.

Transfer limits: B2-09 adds all 19 pages, 13 figures, four numbered tables, 17 numbered equations, 56 claim records, 71 limited checks and 11 coefficient-grid rows. Independent fractional derates, five-atom CVaR, annual/PV risk, objective/time/units and physical/lifecycle limits remain open. Flow totals and rounded cost percentages reconcile. Two scoped originals bring citation edges to twenty-one; 69 other originals, twelve dependencies and native optimization/calibration remain unverified. No accepted operating or GHG input changes. Pipeline variable length, revenue/salvage time, asset activation and 8000-hour availability mappings need native code. Annual discounted tails differ generally from horizon CVaR and physical cumulative mass. Static Wang/SimCCS passages support limited economic/design context, not risk calibration or annual pressure service. Native data-on-request assets, full utility/supplier inventory and building/retention LCA remain open. See [detailed findings](risk_network_comprehensive_findings.md).

### B2-10 — Exploring the value of CO2 shipping transport flexibility in international batchwise transportation carbon capture and storage networks

Fraga, Korre, Nie and Durucan (2024), GHGT-17. Identifier: SSRN5070419. [Retained PDF](../papers/B2-10.pdf); [printed SSRN link](https://ssrn.com/abstract=5070419).

Reading stage: Detailed retained-PDF audit with open scientific verification. Checked sections: All nine pages, internal Appendix A, all main figures/tables, 24 appendix panels, the numbered objective, acknowledgements and nine references.

The implementation is deterministic, annual-resolution, 30-year cost minimization after capture. It does not implement the broader model family's stochastic or multi-objective capabilities. Fifteen plotted designs consist of three baselines and twelve alternatives. Table1 omits z, while later tables/plots include it. Node labels, profile/index mapping and cost-range signs/denominators remain unresolved. Appendix outer annual-cost, fleet and trip changes reconcile the stated headline ranges; no exact annual arrays or native optimum are reconstructed.

Optional interconnection cannot worsen the globally minimized same objective on a common feasible set, but a differently discounted metric can increase. A disclosed two-plan LP demonstrates the distinction without asserting the native discount convention. A separate inventory LP shows why one cargo alone does not establish delayed-arrival service.

Transfer limits: B2-10 adds all nine pages and internal Appendix A, four numbered figures, two tables, 24 appendix panels, 36 claim records, 60 limited checks and a fifteen-design register. Three baselines/twelve alternatives, missing z, node labels, metric/calendar and buffer limits remain open. One exact parent-source check brings citation edges to twenty-two; eight other originals, ten dependencies and native MoMilp/CPLEX/process/field/LCI remain unverified. No accepted operating or GHG input changes. The exact2024 parent supports postcapture multiobjective/LCI lineage, not this UK-linked study's costs, delays or GHG factors. Native code, full constraints, annual inputs/results, timing and operational states are absent from the retained paper. No pressure-constrained annual service, complete capture utility/supplier inventory, current access or retained-carbon factor adopted. See [detailed findings](shipping_flexibility_comprehensive_findings.md).

### B2-11 — A techno-economic assessment of CO2 capture in biomass and waste-fired combined heat and power plants – A Swedish case study

Beiron, Normann and Johnsson (2022). DOI:10.1016/j.ijggc.2022.103684. [Retained PDF](../papers/B2-11.pdf); [detailed findings](chp_capture_comprehensive_findings.md).

Reading stage: all fourteen native pages text-read and visually inspected, plus nine magnifications. Eleven figures, six tables, six numbered equations, nomenclature and all48 printed references inspected. Comprehensive status remains incomplete; source checks and full model reproduction are separate.

The Swedish110-plant/78-network case assumes90% MEA capture with3.6MJ/kg heat at120°C and3bar steam. Base0.1MWh/t electricity already includes absorption/compression/liquefaction; lost CHP generation is separate. Heat pumps add0.17MWh/t atCOP3. The64/up-to118% recovery denominator is extracted-steam energy, not a generic solvent efficiency or negative heat input. Complete cooling/MEA quantities and utility suppliers are missing.

Conditional pureCO2 HEOS at15bara/−25°C gives gas; composition and pressure datum remain unknown. Density and tonne-based truck costing are not filled. The fixed-merit-order spreadsheet excludes dynamics/outages/storage, with native minimum-load/calendar and part-load steam feasibility unresolved. Main costs exclude shipping/storage; reported gross biogenic capture excludes biomass/transport LCI and is not verified net removal.

Transfer limits: B2-11 adds all 14 pages, eleven figures, six tables, six numbered equations, 56 claim records, 65 limited diagnostics, fifteen analyst truck-volume examples and fourteen transcribed representative cases. Bundled utility work, extracted-steam recovery, product state, part-load dispatch, cost timing and gross-versus-net climate boundaries remain open. One exact Kjärstad2016 check brings scoped citation edges to twenty-three; 47 other originals, twelve dependencies and explicit publisher SI remain unverified. No native Ebsilon/Aspen/spreadsheet or complete LCI model is reproduced, and no accepted operating/GHG input changes. The exact shipping original includes conditioning, storage and some subsea equipment; its70bar20°C boundary is not a compatible freight-only increment. Use as a disclosed Swedish process reference, with no Japanese facility or accepted model-input substitution.

### B2-12 — Multi-period, multi-objective optimisation of the Northern Lights and Stella Maris carbon capture and storage chains

Fraga, Korre, Nie and Durucan (2024). DOI:10.1016/j.ccst.2024.100190. [Retained PDF](../papers/B2-12.pdf); [detailed audit](postcapture_lci_comprehensive_findings.md).

Reading stage: all 24 native pages and internal appendix read as text and visually inspected, with sixteen magnifications. Twenty figures, sixteen main tables, AppendixA1/A2, thirteen numbered equations and all 58 printed references inspected. Overall status remains incomplete; source support and full model reproduction are separate.

The postcapture model combines delegated cost/MILP constraints with prospective partial GHG accounting over five six-year periods. Capture/purification are upstream; liquefaction work is averaged across methods and several material, utility, fugitive and lifecycle components are omitted. Pressures also allow different ship capacities, so differences are not isolated pressure effects. The6051Mt resource stock supplies no pressure-constrained annual service.

The133 component/mathematical checks plus three earlier lower-bound checks preserve steel/lorry units, pressure labels, integer/continuous tank sizing, body/appendix fugitives, time/activation, indexing and weighted-objective questions.28 source design labels have conditional analyst timing/full-or98%-cargo examples, with native GWP fields blank. Native MoMILP/cost/Sphera inventories, fluid/thermal and geological models remain unreproduced.

Transfer limits: B2-12 adds all 24 pages and internal Appendix A1/A2, twenty figures, sixteen main tables, thirteen numbered equations, 87 claim records, 133 component/mathematical checks plus three prior case-conflict checks, and 28 source-design rows with conditional timing examples. Pressure/units, material bases, time/activation, objective normalization, source labels and physical/lifecycle boundaries remain open. One scoped Roussanaly2021 original check brings citation edges to twenty-four; 57 other printed entries and fourteen native dependencies remain unverified. The combined1.5 MPa quote remains on HOLD and excluded from scores under7045333. No native cost/MoMILP/Sphera/field/complete LCI model reproduced and no additional operating/GHG input accepted. Its39.2 kgCO2e/t source quote remains preserved on HOLD after Figure 20’s three disjoint components exceed the11617.7kt prose total. The existing exclusion from current analysis and two AppendixA scores is retained; no replacement factor is invented. Other reported intensities remain explicitly conditional postcapture diagnostic scenarios, not complete regional LCA inputs.

### B2-13 — How to transport carbon dioxide with minimal environmental impacts today and tomorrow? A prospective life cycle assessment

Nöhl et al. (2025). DOI: 10.1016/j.jclepro.2025.145659. [Retained PDF](../papers/B2-13.pdf); [detailed audit](prospective_transport_comprehensive_findings.md).

Reading stage: All 11 retained main-PDF pages text-read and visually inspected, including five magnifications. Comprehensive verification remains incomplete.

The prospective European LCA distinguishes transport-only T from conditioning-inclusive T+C, uses future regional inventories and defines cumulative construction/operating carbon payback. Pure 1 bar/30°C feed is assumed; capture, purification and geological retention remain outside. The 4% returning ISO heel is not a vent-loss factor. Early battery-truck cases explicitly exceed approximately 44 t.

All 66 displayed payback cells and 272 category ranks are preserved. Train-to-small-dense payback is 6.7 years in 2040, HFO-to-gas is 12/20 years, and e-fuel-to-dense is 14–31 years. Dense pipelines rank first in 14 of 16 offshore categories, with water-use and freshwater-eutrophication exceptions despite broader conclusion wording. Fixed HFO background qualifies the 72–93% reduction claim. The 70 Gtkm/y and linear GVA calculation yield a conditional 0.023333–0.073889% sector allocation; a pipeline upper bound near 0.075% alone establishes neither universal compliance nor actual exceedance.

Transfer limits: 38 limited diagnostics, graphic transcriptions and a synthetic annual Equation 1 component do not reproduce the native LCA or payback cases. All 53 originals, thirteen dependencies or scope requirements, supplements A/B and licensed inventories remain unverified. No complete capture-to-ship utilities, pressure-constrained annual service or retained/avoided factor is added. European backgrounds require disclosed geographic proxy treatment; no accepted operating/GHG inputs change.

### B2-14 — A High-Precision Geo-Spatial-Techno-Economic Framework for CO2 Source-Sink Pairing: Land-Sea Synergy and Cross-Regional Coalitions in China

Wei et al. (2026). DOI: 10.1021/acs.est.5c14041. [Retained PDF](../papers/B2-14.pdf); [detailed audit](zonal_pairing_comprehensive_findings.md).

Reading stage: All 15 retained main-PDF pages text-read and visually inspected, with eight magnifications. Ten numbered figures plus the graphical abstract, three tables and all 63 printed references inspected; no formal numbered equations in the main PDF. Algorithms are deferred to unverified SM1. Comprehensive verification remains incomplete.

The national 1 km framework explicitly serves macro-assessment/prefeasibility rather than specific site screening or design. Geological support can be wells 20–50 km apart. Table 3 balances onshore/offshore resource stocks, while approximately 89–91% of annual matched flow is onshore. These are model allocations, not pressure-constrained annual service. The 4.2/7.6 ratio is 55.26%, rather than the nearby 59% claim; captive-power overlap, capture/avoidance/cost denominators and percentage ranges remain unresolved. No source correction is selected.

Transfer limits: 57 limited checks and disclosed spherical-grid, nonuniqueness and shared-sink LP examples do not reproduce native ITEAM/GIS/cost or physical models. Two scoped Lin/SimCCS checks support bounded context; 61 other originals, fourteen dependencies or scope requirements, explicit SM1 and native source data remain open. Prompt retrofitting is not staged construction/dispatch, and coalition proposals are not implemented sharing agreements. No accepted operating/GHG inputs or current numerical results change.

### B2-15 — Global analysis of geological CO2 storage by pressure-limited injection sites

Smith, Hampson and Krevor (2024). DOI: 10.1016/j.ijggc.2024.104220. [Retained PDF](../papers/B2-15.pdf); [detailed audit](pressure_limited_global_comprehensive_findings.md).

Reading stage: All 13 retained main-PDF pages text-read and visually inspected, including seven magnifications. Nine figures, two tables, six unnumbered Figure 1 relations and all 68 bibliography entries inspected. Comprehensive source/model verification remains incomplete.

CO2BLOCK models closed homogeneous basins with equal constant rates and a 5 Mt/y cap per multi-well storage site. The headline global/history/readiness resource divided by 30 or 80 years agrees with rounded annual figures; these are separately optimized horizon cases, rather than one evolving rate history. Basin populations 248/265, pressure-resource versus basin shares, Lambert normalization/branch, plume rate/mass definitions and the horizon of the reported site count remain open.

Transfer limits: The article is public, but its data statement explicitly says the authors lack permission to share data. No public reservoir dataset or native global model is acquired. The 53 diagnostics, twelve design rows, fourteen dimensionless Lambert roots and two mass-geometry examples are limited components. All 68 originals, fourteen dependencies or requirements, supplements, native defaults/code and field validation remain unverified. Historical well-rate and integrity analogues do not establish required wells or retention probabilities. No accepted operating/GHG input or current numerical result changes.

### B2-16 — A proposed global layout of carbon capture and storage in line with a 2 °C climate target

Yi-Ming Wei et al. (2021). DOI: 10.1038/s41558-020-00960-0. [Retained PDF](../papers/B2-16.pdf); [detailed audit](global_layout_comprehensive_findings.md).

Reading stage: All eleven retained main-PDF pages text-read and visually inspected; five figures/eighteen panels, 33 numbered equations, all 51 bibliography entries, 62 claims and fifteen issues recorded. This does not certify comprehensive completion.

The source proposes a cumulative domestic layout of 3,093 clusters and 432 sinks in 85 regions: 58.61 Gt saline plus 33.39 Gt EOR. Volumetric basin stock is not annual pressure-constrained service. The main-text 40,000 t/y cluster threshold differs tenfold from Methods 0.4 Mt/y. Mixed-sector capture, avoided-versus-captured cost, conditional EOR revenue units, learning initialization/thresholds and case denominators remain open. Financial EOR credits and cumulative-GDP ratios do not establish avoided GHG or causal growth.

Transfer limits: The 67 checks, nine transcribed country rows, 21 synthetic deployment rows and six synthetic LP cases do not reproduce native global C3IAM/GCOP. Two selected-original checks support and qualify earlier SimCCS/InfraCCS methods; 49 other direct originals, fourteen dependencies or requirements, explicit SI and data/code on request remain unverified. No complete matched capture-to-ship utility inventory or public field dataset is supplied. Accepted operating/GHG inputs and current results remain unchanged; the combined 1.5 MPa HOLD is preserved.

### B2-17 — Progress and perspectives in source-sink matching for CCUS: A critical review

Keyao Lin et al., online 2025/volume 2026. DOI: 10.1016/j.rser.2025.116313. [Retained PDF](../papers/B2-17.pdf); [detailed audit](matching_review_comprehensive_findings.md). B3-46 is its duplicate.

Reading stage: All 27 retained pages were text-read and visually inspected. Eighteen figures, seven numbered tables, the abbreviation table, twelve capacity equations and two inline relations, 109 claims and 251 bibliography entries are recorded. Some tiny map labels remain unresolved. This is not comprehensive completion.

The review synthesizes sources, sinks and matching across four scales and identifies data, physical, economic and coordination gaps. A reproducible literature-selection/extraction protocol is not supplied in the retained PDF. Resource/status dates, duplicated country labels, capacity units, stock/rate periods, historical GWP and future AI capabilities remain qualified. Cement costs differ tenfold between the body and Table 7. Exact original checks separate shipping buffer/service/weather cases and confirm that the cited Wei global model prohibits cross-border transport.

Transfer limits: The 44 limited checks, five resource interval rows and six synthetic state screens do not reproduce native selection or cited models. Two scoped citation checks do not complete original chains; 249 other direct originals and fourteen dependencies or requirements remain open. No complete matched capture-to-ship utilities or calibrated annual field-service dataset is acquired. Existing accepted inputs, current outputs and the combined 1.5 MPa HOLD are preserved.

### B2-18 — A prudent planetary limit for geologic carbon storage

Gidden et al. (2025), Nature 645, 124–132 plus Methods. DOI: 10.1038/s41586-025-09423-y. [PDF](../papers/B2-18.pdf). All 13 retained physical pages were read as text and inspected as renders, with enlarged figures. **Comprehensive status: incomplete.** See the [item record](comprehensive_review/B2-18.md) and [scientific findings](prudent_storage_comprehensive_findings.md).

The central 1,460 Gt (1,290–2,710 Gt) risk-screened stock uses an explicitly pressure-aware borrowed coefficient, 0.037 Gt per 1,000 km³ of assessed bulk sediment for a 50-year injectivity period. This is not a site-specific annual rate or calibrated pressure history. SSP5 urban buffers, PGA hazard, water/formation depth, borders and other exclusions are conditional screens. Marginal layer losses depend on order.

Figure 2c's native-labelled central offshore/onshore regional sums of 994/452 Gt do not reconcile with Figure 2b's 450/1,010 Gt; no labels or values are silently corrected. Temperature arithmetic is consistent under separate storage/TCRE assumptions. Density sign/surface state, Figure 3 units and scenario interpolation/extrapolation conventions remain open. Forty-one limited checks and disclosed synthetic components do not reproduce native GIS/IAM outputs.

All 93 printed bibliography entries were read. R024 has one scoped exact Wei2021 original check; the other 92 originals and fourteen dependencies remain unverified. Explicit publisher SI, GitHub code, Zenodo data, the explorer and peer-review reports have not been retrieved while external research is paused. No accepted operating/GHG input or numerical result changes; the combined 1.5 MPa HOLD remains.

### B3-01 — Carbon dioxide capture and storage—liability for non-permanence under the UNFCCC

Bode and Jung (2006), International Environmental Agreements 6, 173–186. DOI: 10.1007/s10784-006-9004-4. [PDF](../papers/B3-01.pdf). All 14 retained pages were read as text and inspected as renders, with enlarged graphics and formulae. **Comprehensive status: incomplete.** See the [item record](comprehensive_review/B3-01.md) and [scientific findings](ccs_liability_comprehensive_findings.md).

The conditional 2006 framework distinguishes six capture/storage combinations and proposed storage-country, capture-country or temporary-credit buyer responsibility. It does not establish current legal rules. Table 1's listed resource endpoints close at 476–5,880 Gt, but saline coverage, the 1,660 Gt best estimate and regional allocation require original data. Historical cost ranges lack a complete common utility/currency/mass boundary.

The native temporary-value identity is monetary, not a physical retention fraction. All twelve Table 4 values are preserved. Two disclosed cash-flow timing assumptions do not reproduce its nine nonzero-release cells; missing release/renewal/timing conventions remain open. Finite-credit examples show that zero physical leakage can coexist with lower financial value at credit expiry. The conclusion's literal (>0.01) lacks a unit and is not silently corrected.

The record includes two figures, four tables, two printed identities, 26 numbered footnotes, 48 claims and 39 limited checks. Thirty capacity cells, six historical classifications, twelve source credit-value cells, 24 finite-credit examples and three price-growth cases do not reproduce the native author model. All 38 originals and twelve dependencies remain unverified; no new primary-passage edge was added. No supplement/code/data statement or embedded file was identified; online assets remain unverified. Accepted operating/GHG inputs, primary outputs and the combined 1.5 MPa HOLD are preserved.

### B3-02 — Assessing a Liability Regime for Carbon Capture and Storage

Wilson, Klass and Bergan (2009), Energy Procedia 1, 4575–4582. DOI: 10.1016/j.egypro.2009.02.277. [PDF](../papers/B3-02.pdf). All eight retained pages were text-read and inspected as renders, with enlarged tables. **Comprehensive status: incomplete.** See the [item record](comprehensive_review/B3-02.md) and [scientific findings](liability_regime_comprehensive_findings.md).

The historical U.S. legal synthesis distinguishes statutory/tort remedies, bond/insurance/pool instruments and three proposed stewardship phases. Pressure, displaced brine and other local harms can occur without atmospheric leakage. Fifteen/thirty-year examples and fifty-year proposed monitoring do not imply automatic transfer: the paper explicitly says the proposed rule has no transfer provision. Actual performance, funding, coverage, caps and residual duties require definition.

Both dense tables and all fifty cells, including three blanks, were inspected. The record tracks 44 claims, four limited monetary checks, twelve synthetic loss-event rows, three pooling examples and six monitoring-funding cases. No native numerical author model was reported; the synthetic examples do not validate legal outcomes, current insurance or calibrated hazards.

Twenty bibliography originals, ten numbered legal/fund notes and twelve further dependencies remain unverified, with no new primary-passage edge. The longer Emory version is advertised but unverified. Native rendered 2009 metadata govern over hidden template placeholders, and the visible licence is CC BY-NC-ND. Accepted numerical inputs/results and the existing combined 1.5 MPa HOLD are preserved.

### B3-03 — Critical review and recommendations for strengthening health and safety and major accident prevention regulations for carbon capture and storage in UK ports

Dbouk and five coauthors (2025), IJGGC 147, 104479. DOI: 10.1016/j.ijggc.2025.104479. [PDF](../papers/B3-03.pdf). All 13 retained pages were text-read and inspected as renders; Figure 1 and both tables were enlarged. **Comprehensive status: incomplete.** See the [item record](comprehensive_review/B3-03.md) and [port-safety findings](port_safety_comprehensive_findings.md).

The authors propose clearer underlying PMSC performance goals, bespoke DGHAR guidance and two separate COMAH changes: address the transport/temporary-storage exclusion and recognize CO2 under a qualifying trigger. Three recognition routes do not automatically remove the independent exclusion. Recommendations and Table 1 equivalence judgments are not verified adopted law, site permission or quantitative safety outcomes.

All 21 substantive table cells, 24 numbered notes, 54 claims and six analyst relations are recorded. Six freight percentage checks are rounding-compatible. Three arithmetic checks, four constant-density buffer examples and two conditional handling examples preserve source/analyst boundaries. Notice lead time is not dwell; generic unpaired temperature/pressure ranges are not an operating envelope; scenario capture/import mass differs from commodity-specific handling or reservoir service.

All 87 bibliography originals, 24 notes and fourteen further dependencies remain unverified. Exact CCSA scenario provenance is unresolved, and an unpublished MCA report explicitly requires lead-author approval. No native quantitative author model or QRA was identified; cited shipping/risk models and possible publisher assets remain open. No new citation edge or accepted numerical input changes; the existing combined 1.5 MPa HOLD is preserved.

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
