# B2-11 Swedish CHP capture audit

Beiron, Normann and Johnsson assess capture retrofits at 110 Swedish biomass/waste combined heat and power plants in 78 district-heating networks. Their study is useful for Paper 1 because capture heat changes electricity and useful-heat production, plant utilization and the captured-mass denominator. Its Swedish conditions can be discussed as a disclosed geographic/process reference. It does not supply pressure-constrained storage service or a complete matched capture-to-ship inventory.

All 14 pages of the [retained paper](../papers/B2-11.pdf) were read as text and visually inspected, with nine additional magnifications. This includes eleven figures, six tables, all captions/legends/footnotes, nomenclature, six numbered equations, the literature review and discussion. The [item record](comprehensive_review/B2-11.md) preserves 56 claim records and sixteen open issues. DOI: [10.1016/j.ijggc.2022.103684](https://doi.org/10.1016/j.ijggc.2022.103684), IJGGC 118 (2022) 103684, CC BY 4.0. Source SHA-256: `5522a8c750a21a7bb097b2ad86e815461a7b7a05d0c3dadc25bbd6865eef2d8a`.

## Heat and electricity boundaries

The source assumes 90% MEA capture from flue gas containing 13–15% CO₂, with a reboiler duty of **3.6 MJ/kg captured = 1 MWh/t captured**. Reboiler temperature is 120°C and steam supply 3 bar. Boiler load and industrial process-steam delivery are held constant when comparing reference and capture cases.

The **0.1 MWh/t captured electricity** applies to the combined absorption, compression and liquefaction boundary. It is distinct from the lost electricity generation caused by extracting steam from the CHP turbine. Equation 2 includes both the direct auxiliary work and this lost generation. Adding another unrelated compression/liquefaction duty to 0.1 MWh/t would risk double-counting.

The heat-recovery cases are 0%, 64% through heat exchangers, and up to 118% with heat pumps of COP 3. Heat pumps add 0.17 MWh/t electricity, making direct work 0.27 MWh/t in that case. At the paper's 40 €/MWh electricity price, direct work alone costs 4 or 10.8 €/t captured. These are not total electricity opportunity cost or total OPEX.

The recovery percentages are relative to **energy in the extracted steam**, rather than necessarily the same exact reboiler-duty denominator. If all quantities used precisely 1 MWh/t, then 0.64 + 3 × 0.17 = 1.15, leaving a 0.03 MWh/t residual against 1.18. This is a conditional basis check. Unrounded stream enthalpies and plant-specific results are missing, so it does not establish an energy error or justify changing the reported 0.17 to 0.18.

Physical cooling and MEA quantities, utility suppliers and emission factors are missing. Table 4 supplies prices, not those quantities. Aspen capture and referenced liquefaction cases are not available locally. The record therefore remains a partial inventory.

## Product conditions and local transport

Page 7 states a product at **15 bar and −25°C**, subsequently described as liquefied for trucking. Pressure basis, purity, composition and density are unspecified.

A conditional pure-CO₂ check using CoolProp 8.0.0, `HEOS::CO2`, gives saturation pressure about **16.827 bar absolute at −25°C**. Both 15 bar absolute and an analyst interpretation of 15 bar gauge plus one atmosphere are below that pure-fluid saturation pressure, yielding gas. Mixture behavior and the actual pressure convention remain unverified. No product condition, density or cargo mass is corrected from this diagnostic.

Table 6 specifies 33 m³ per truck. Equations 3–6 use continuous trip/fleet quantities, full-load daily volume, 50 km/h, one hour loading and three eight-hour shifts. Wage/fuel costs are multiplied by plant capacity factor. Five drivers approximate weekly coverage: 21 shifts divided by five workdays gives 4.2 driver equivalents, before leave/rest provisions.

The [volume grid](../outputs/comprehensive_review/B2-11_truck_volume_grid.csv) evaluates these printed components at explicitly analyst inputs: 1000 m³/day, five distances and three utilization factors, with a 365-day year. It separately shows a ceiling-fleet comparison. It is not an actual integer dispatch, roster, loading queue or native plant case. **Density and €/t remain blank.** No pure-fluid diagnostic density is adopted as truck payload.

## Annual operation and physical feasibility

Fourteen Ebsilon designs represent the portfolio, with fixed 88% turbine isentropic and 90% boiler efficiencies. All [Table 1 rows](../outputs/comprehensive_review/B2-11_representative_plants.csv) were transcribed, including extraction/deaerator pressures, industrial-steam entries and source footnotes. Two primary supplies are explicitly hot water; their liquid water states are consistent with the footnote and are not steam failures.

The spreadsheet follows a fixed merit order: excess heat, waste CHP, biomass CHP and peak units, with newer plants first within categories. Minimum loads are 0.7 and 0.4 for waste/biomass. All five logical rules were read. They do not fully specify first/last-unit, off/spill and previous-unit edge handling. A disclosed 10 MW plant facing 5 MW demand illustrates the need for such a rule when its online minimum is 7 MW; it does not prove a defect in the unavailable spreadsheet.

The model excludes maintenance, ramping, minimum up/down times, dynamics and thermal storage. Three measured city profiles from 2012 are mapped and scaled to networks; actual hourly arrays and leap-year treatment are missing. Analyst 8760-hour cost examples are not substituted for the native 2012 calendar. Figure 6's last labelled tick does not establish array length.

The authors explicitly acknowledge possible extraction pressures below 3 bar, insufficient remaining turbine steam and retrofit limitations at part load. Proposed alternatives include lower capture, higher-pressure extraction or an auxiliary boiler. Applying full-load ratios, linear utility demands and 90% capture whenever CHP runs is therefore not demonstrated annual physical feasibility.

## Cost and carbon denominators

Equation 1 fits absolute capital cost in k€ to captured flow in **kg/s**, with exponent 0.6339. Convert t/h to kg/s before use. The stated 25-year economic life includes two construction and 23 operating years. Alternative 23/25-year capital-recovery factors are shown conditionally; construction cash flows and price year do not permit selection of a unique native convention. Heat-pump and new-FGC capital mapping also require full case data.

Figures 8 and 11 clip cost axes at 100 and 150 €/t; clipping is not an upper cost bound. Figure 9's net OPEX describes the variable utility/opportunity/heat-credit ledger, while fixed OPEX at 6% of CAPEX appears separately in the MAC. Main cost estimates cover capture, conditioning and trucks to a hub, excluding shipping/storage.

Table 5 sums to **15.965 Mt/year CHP capture in the 64% case**, plus **9.1 Mt/year industrial capture** from a different portfolio. Combined 25.065 Mt is not the 110-CHP potential. The caption points to Figure 9 although the map is Figure 10; proposed hubs are not operating facilities.

The reported national capture range is 13.9–19.3 Mt/year, with 2.6–2.9 Mt fossil and approximately 10–16 Mt biogenic. MAC quantities are captured biogenic plus fossil CO₂, not avoided or permanently retained mass. National comparisons use different years/scopes: 52 Mt CO₂e, 43 Mt CO₂ and 2019 fossil CO₂ of 41 Mt. No single denominator is silently substituted for all claims.

The paper explicitly omits the carbon footprint of biomass supply and CO₂ transport, including truck emissions. Lost-power replacement, shipping, storage and retention inventories are also not established here. Its biogenic capture potential cannot be accepted as whole-chain net-negative emissions.

Nominal percentage points likewise need care. Figure 5b's Lillesjö electricity approximately 84→70% is about fourteen nominal percentage points. The 118% heat-recovery fraction differs from nominal DH retention; Lillesjö DH is approximately 110%, or 140% with a new FGC. Complete plant arrays are needed before interpreting a universal maximum. Table 2's waste composition sums to 100.1 wt%, compatible with one-decimal rounding; it is preserved without renormalization.

The claimed 2.0–2.3 MJ/kg KS-1 duty cites Zheng 2020, whose bibliography title concerns a single-component water-lean solvent. That attribution remains unverified pending the original. It does not authorize a lower Paper 1 utility input.

## Cited shipping cost and reproduction status

One exact citation has a [scoped original-passage check](../evidence/comprehensive_review_inputs/B2-11_citation_checks.json): Kjärstad et al. 2016, retained as B3-33, DOI 10.1016/j.ijggc.2016.08.024. Selected original pages 1, 2, 3 and 8 were text-read and visually inspected. The rest of the seventeen-page original and its literature chain remain pending.

The 14–22 €/t range concerns the Rautaruukki–Faludden bulk ship system at 20→1 Mt/year, excluding the collection grid. Its boundary starts at a 70 bar/20°C hub and ends at storage at 70 bar/0–20°C. It includes liquefaction, intermediate barge storage, port/loading/unloading, flashing and pumping/heating, plus subsea templates/wellheads/distribution/umbilicals; injection and water-production well drilling is excluded. It is not a freight-only increment matched to B2-11's already-conditioned product.

B2-11 separately uses an unverified Sandberg forecast of 30–55 €/t shipping/storage to discuss a 75–180 €/t total. Its endpoint arithmetic works. The audit does not allege that the authors added 14–22 €/t to their capture cost; it records the incompatible component boundaries and missing matched forecast case.

All 48 printed bibliography entries are recorded with native lines and page geometry, including Hirata's page continuation and the nonalphabetic Smith placement. **One scoped citation edge, 47 other unverified originals and twelve unverified dependencies** remain. The explicitly referenced publisher supplement/database is missing locally, not declared absent online. External retrieval remains paused under the user's Chrome-connection instruction.

The [calculation script](../scripts/audit_chp_capture.py) produces 65 limited checks, fifteen analyst truck examples and fourteen representative table rows. Seven new tests check finance repayment, unit/scale handling, truck conservation and utilization, conditional EOS bracketing, invalid domains and evidence status. Native Ebsilon/Aspen/spreadsheet cases, the 110-plant annual results, full costs, storage and LCI remain unreproduced. **No paper is certified complete and no accepted operating/GHG input changes.**
