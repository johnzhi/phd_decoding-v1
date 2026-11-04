# Reference-data intake and inventory extension — 4 November 2026

The two new batches contain 104 uploads. 100 files were transferred and retained unchanged; four reports exceed the tool's32MiB limit. There are95 distinct accessible binaries across these batches, including duplicate editions/copies. Their catalogue records both identity and transfer status. PDF text is indexed, but this does not mean every page has received a scientific review.

The original literature corpus remains separately identified as 92 unique publications. The new material includes regulatory documents, spreadsheets, reports, dataset metadata and snapshots; these are not counted as 104 additional research papers.

## Capture utilities: what the NETL files support

The supplied macro workbooks are the **NGCC and pulverized-coal CCRDs**, not the industrial retrofit model. Their reference technology is CANSOLV, with different host/capture-rate cases. They do not establish actual energy demand for the 14-source South Sumatra model, which used its own process assumptions.

All original workbooks are retained. Native XML extraction archives cached cells, formulas and errors without running macros, refreshing links or recalculating user cases. The searchable native archive contains 1,013,036 nonempty/formula cells across 17 workbooks. This is a raw cell count, not a count of validated independent measurements. The current Japanese coefficient table extract contains 3,269 located factor records; other historical sheets remain available in the native archive.

Six NETL reference cases give these normalised requirements:

| Host / capture rate | Additional auxiliary electricity (kWh/t captured) | Steam electric opportunity loss (kWh/t) | Total make-up electricity equivalent (kWh/t) |
|---|---:|---:|---:|
| NGCC90% |151.539 |232.759 |384.298 |
| NGCC95% |151.351 |232.359 |383.710 |
| NGCC97% |153.329 |237.931 |391.260 |
| PC90% |118.616 |206.746 |325.362 |
| PC95% |118.381 |205.013 |323.394 |
| PC99% |118.897 |207.444 |326.341 |

These use reference flow and power cells on the `Cost Parameters` sheets, not arbitrary selected fleet summaries. The make-up route replaces power-output losses under a matched-output accounting scenario. It is **not physical electric demand alone**, and its steam component is not GJ of thermal heat.

A second, mutually exclusive route derives net reported steam-utility enthalpy import from the same PC report's labelled reboiler, reclaimer and dryer steam/condensate streams. The90/95% cases give approximately 2.75172/2.75040 GJ per reported tonne of CO₂ product and 116.763/116.626 kWh/t of additional auxiliaries. The heat metric is a documented boundary calculation, not a verbatim isolated reboiler-duty measurement; major-stream rounding, unshown minor streams and product composition limit its precision. Compression to dense-phase conditions is included in these reference inventories, so no duplicate compression load or unmatched liquefaction factor is added.

**Never add the electrical make-up route and the heat-plus-auxiliary route together.** Either would otherwise charge the steam penalty twice. The separate heat route excludes turbine derate. District-heat quality and an actual industrial steam supply are not established by an official reporting coefficient, so this route remains an accounting sensitivity.

## Utility factors and accounting scope

- Norway 2025 climate disclosure: **9.4 gCO₂e/kWh**, `Klimadeklarasjon!C8`. This is used as an as-reported climate-disclosure reference, not a marginal factor or future forecast. The spreadsheet alone does not document all lifecycle/method/horizon details.
- Norway 2025 market disclosure: **430.93 gCO₂/kWh**, `Varedeklarasjon!C8`. It is retained only as a distinct market-accounting sensitivity; it is not substituted for physically delivered electricity.
- The electricity-sales export declares a misleading used range of A1. Direct XML inspection recovers **101.0025 TWh without guarantees of origin** at B4 and **36.5945 TWh with guarantees** at B5. Their sum is 137.597 TWh; these are volumes, not emissions factors. No zero-carbon GO factor is inferred.
- Japan R8 electricity fallback: **0.000416 tCO₂/kWh =0.416 kgCO₂/kWh**, cell C1499. The header distinguishes R6 supply performance, R7 emissions and R8 reporting, with menu-specific qualifications. It is an official fallback scenario, not an identified supplier or a forecast.
- Japan R8 heat fallback: **0.0532 tCO₂/GJ =53.2 kgCO₂/GJ**, cell D47. It is a reporting factor, not proof of compatible industrial steam or complete lifecycle emissions.
- Japan gas factors remain in **tCO₂ per 1000m³**. They are not converted to delivered-heat emissions without a matched calorific basis, gas composition and boiler efficiency.

Supplier/menu base and adjusted factors are preserved separately. Zero adjusted entries are accounting quantities and do not establish zero lifecycle physical emissions. Historical factors are frozen reference scenarios over the model horizon, not future energy forecasts.

## Marine fuel: IMO default scenario now implemented

MEPC.391(81), physical PDF p51, Appendix2 row5, gives fossil MDO/MGO ULSFO defaults: WtT 17.7 gCO₂e/MJ; LCV 0.0427 MJ/g; CO₂ 3.206 g/g fuel; CH₄ 0.00005 g/g; N₂O 0.00018 g/g. The guideline's GWP100 values are 28 and 265 (physical p5).

These imply **0.75579 kgCO₂e/kg upstream**, **0.04910 kgCO₂e/kg for combustion CH₄/N₂O**, and **4.01089 kgCO₂e/kg WtW including CO₂**. The selected default matches a stated MDO/MGO category; actual bunker grade, upstream supply and engine/idle behaviour still need evidence. No LNG-specific slip factor is transferred.

## Model results after the new reference components

The extension evaluates 20 utility scenarios against 144 original comparisons and five design-controlled route cases: **2,980 inventory comparisons**. It retains the original operation, injection and capture outputs; utilities are charged against *captured*, not injected, mass. The reference-case capture percentage is not multiplied into already captured source flow again.

For the40,000m³ design-controlled5000km higher-service case relative to the1000km lower-service case:

- Original ship-combustion-only allowance: approximately+1.281 Mt.
- With IMO default WtW shipping and NGCC90% make-up electricity valued at the Norwegian2025 climate factor: approximately **+0.009 Mt** remains for other differential burdens.
- With the Japanese fallback electricity factor instead: approximately **−0.984 Mt**.
- With the paired PC90% heat-plus-auxiliary route and Japanese fallback factors: approximately **−1.207 Mt**.

These are **conditional inventory balances**, not full net avoided GHG or destination rankings. The9kt remainder is smaller than unresolved schedule/rounding/asset/process uncertainties; it cannot establish a robust benefit. Japanese reporting-only CO₂ coverage and Norway disclosure methodology are not silently treated as a complete harmonised LCA.

## Waves: snapshots, not an operating calendar

Both NetCDF files contain one timestamp (**2026-08-31 21:00 UTC**) and one spatial grid point. Locations are approximately −6.4°/128.4° and 18.0°/116.2°. Significant wave heights are 1.01 and 3.65 m at those points. Seventeen variables per file are extracted with units and metadata.

No historical frequency, route-wide wave exposure or annual downtime can be inferred from two snapshots. No threshold or shutoff rule is invented. The original deterministic calendar sensitivity remains in place. See `reference_data_requests.md` for suitable time-series exports.

## IBDP: provenance and what is still absent

The BagIt payload manifest lists 31 files; 27 match uploaded original bytes under SHA256 (and corresponding SHA512 checks). The four untransferred reports are recorded by name. This is not complete-bag validation. Supplied terms permit research use/sharing with attribution and prohibit sale; original terms and attribution accompany the retained package.

The `EventRates` workbook, relocation catalogue and `.rdv` file are **microseismic event records**, as the supplied README confirms. They are not CO₂ injection rate/pressure time series and do not calibrate injection capacity.

The 2012 injectivity report provides independent *simulation* reference values for **St.Peter and Knox-Potosi**, not observed Mt.Simon CCS1 injection history. For St.Peter it reports a 1980 psia bottomhole cap and first-year/last-year/average rates of 0.660/1.164/0.990 Mt/y over 20 years. Twelve located quantities are extracted, with formation and evidence type preserved. No interior annual series is interpolated or passed off as data. These endpoints and model constraints support a future independent reservoir benchmark, but do not supply the original South Sumatra kr,t arrays.

The World Bank attachment is a container-port report, not the Excel annex or a CO₂-terminal calendar. It is retained as context only. The actual injection-monitoring README and paired raw rate/pressure time series remain absent from the accessible uploads.
