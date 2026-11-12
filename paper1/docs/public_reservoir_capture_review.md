# Public reservoir and capture evidence — 12 November 2026

The new public intake supplies a pressure-constrained reservoir simulation dataset and three complete **paired heat/work inventories at the reported MEA capture-and-compression boundary**. It does not supply a calibrated Japanese sink, a complete industrial-facility inventory or a full lifecycle result. Existing operating and allocation outputs remain unchanged.

## Sources and retrieval

- **PUB-BJARMELAND:** Norwegian Offshore Directorate, [CO₂ storage models](https://www.sodir.no/fakta/co2-handtering-ccs/lagringsmodeller/), page updated 6 August 2024; [Bjarmeland archive](https://www.sodir.no/globalassets/1-sodir/fakta/co-to/lagringsmodeller/barentshavet/bjarmeland.zip). Selected case `CO2_BJ_C07B9`, native files dated February 2014. This is a Norwegian model scenario, not observed operations or current allocated storage service.
- **PUB-CEMCAP:** Anantharaman, Fu, Roussanaly and Voldsund, *Design and performance of CEMCAP cement plant with MEA post combustion capture*, D4.2, Revision 1, [DOI 10.5281/zenodo.1150320](https://doi.org/10.5281/zenodo.1150320). Zenodo publication is 17 January 2018; the document gives actual delivery 26 September 2016 and a 28 March 2017 cover reference. These dates remain separate. This is a European reference cement-plant simulation, not a Japanese plant measurement.

Firecrawl searches identified the public Johansen study and CEMCAP report. Firecrawl read the Johansen accepted manuscript and CEMCAP landing page, then reported insufficient credits on the PDF/data-page calls. Direct HTTPS retrieved the CEMCAP PDF and official storage-model page/archive. Those downloads are not claimed as successful Firecrawl scrapes.

The [source manifest](../evidence/public_followup/source_manifest.json) records URLs, retrieval date, sizes and SHA256 hashes. The CEMCAP PDF matches Zenodo's published MD5 `7d6dbffda26d64a0f5a80a5543e9e7e6`. The upstream Bjarmeland ZIP has SHA256 `227f28201f1fffd11325f7204d91802dd0a191bfb9c29b71e84815379e6d28e2`. Its 63-member directory is recorded; nine selected members are repackaged into a 32,890,157-byte [source subset](../original/public_followup/Bjarmeland_C07B9_source_subset.zip), preserving each member's original bytes and hash. The complete 369 MiB upstream ZIP is not committed. The subset resolves the selected deck's three explicit INCLUDE dependencies and retains its native summary, binary summary/specification, print log and end report.

## Pressure-constrained reservoir dataset

The METRIC compositional deck includes grid coordinates, corner depths, active-cell flags, rock properties and overrides, EOS/component/PVT data, relative-permeability tables, initial conditions, well completions, boundary representation and dated controls. Its nominal grid is 166 × 120 × 105; that product is not the active-cell count. `WCONINJE` requests **1,500,000 SM3/day** of pure-CO₂ injection with a **225 bar absolute BHP ceiling**. The RSM labels `WBHP` as `BARSA`, resolving the pressure basis for this case. The deck's fracture-limit comment is a modelling assumption, not an independently validated geomechanical limit.

`public_reservoir_history.csv` contains **4,951 paired native summary rows**, from day 1 through day 18,263 (source start 1 January 2015; last report 1 January 2065). It preserves printed tokens and RSM line locators for field injection rate/cumulative volume, field pressure, GI injection rate/cumulative volume/BHP, and OP2 oil/water/gas production rates. No day-zero measurement or annual interpolation is invented.

The achieved GI rate spans **853,622.5–1,500,000 SM3/day**. Six initial records are below target and at the printed 225 bar ceiling. None exceeds it; field/well injection series agree at printed precision. Final cumulative injection is printed **2.74 × 10¹⁰ SM3**, not a high-precision mass. Native binary summaries are retained for future work; no ideal-gas, cargo or cross-source density converts standard volume to tonnes.

This is an **oil/water/gas model with a producer**, not saline-only validation. OP2 is shut until 2030 then opened; residual oil and production outcomes remain part of the context. The deck applies inactive/zero-porosity zones and 150-fold edge pore-volume multipliers. Its log reports an ignored GI completion at `(28,66,25)`, plus six linear-solver convergence warnings; the end report counts seven warnings and zero errors. Full print output and [located warning excerpts](../evidence/public_followup/bjarmeland_warning_excerpts.json) are preserved. Zero reported errors is not independent validation.

The acquisition gap is reduced: an inspectable pressure-constrained model and paired outputs are available. **A maximum-rate service curve is not established.** Almost all records attain the imposed target and do not reveal maximum feasible injection. An independent simulator run must verify effective completions, warnings, volume/mass reference, target sweeps, pressure controls, boundary sensitivity and production/retention accounting before supplying annual mass constraints to shipping. No EOR climate credit, permanent retention or oil-production counterfactual is inferred.

## Capture heat and electricity inventory

The [CEMCAP PDF](../original/public_followup/CEMCAP_D4.2.pdf), Table 5.3, physical pages 22–23 (printed 16–17), supplies all three cases together. Native cell extraction is checked against rendered pages. `public_capture_values.csv` retains 42 quantities with page/cell bounding boxes, exact tokens, source hash, case and units.

| Source case | Heat (GJ/t captured) | Capture auxiliaries (kWh/t) | Compression (kWh/t) | Total electricity (kWh/t) | Cooling duty (GJ/t) |
|---|---:|---:|---:|---:|---:|
| Low air leak, interconnected | 3.790 | 35.389 | 87.278 | 122.667 | 4.598 |
| Low air leak, direct | 3.733 | 35.333 | 87.222 | 122.556 | 4.833 |
| Typical air leak, interconnected design | 3.832 | 39.389 | 87.306 | 126.694 | 4.909 |

All use a **116.8°C reboiler and 2.45 bara steam**. Product pressure is **110 bar as printed**; that row has no gauge/absolute suffix. Capture fractions are 0.8994/0.8997/0.8996; wet product CO₂ mole fractions are 0.9983/0.9985/0.9983. Solvent makeup is **4.677 kg of 30 wt% solution per tonne captured**, not pure MEA. Table 5.2's rounded validation values do not replace Table 5.3's case-specific numbers.

Unit conversion is exact: 1 MJ/kg = 1 GJ/t, and electricity in MJ/kg × 1000/3.6 gives kWh/t. Capture auxiliary plus compression work equals reported total work for every case. Heat/electricity remain paired within each case. Repeating decimal conversions do not imply added measurement precision.

The reported electricity includes compression, with three stages, intercooling, a pump and aftercooler described in §5.2. No generic compression factor or turbine opportunity-loss electricity is added. Cooling duty is heat rejection, not electricity or purchased steam, and is not converted to power without a cooling-system inventory. FGD/SCR pretreatment is described before the MEA system; its incremental duties are not established by this table. Actual suppliers, cooling supply, materials, upstream emissions, construction and ship conditioning remain outside the verified pair. **Complete as-reported capture heat/work does not mean complete facility or lifecycle inventory.** A 110 bar outlet cannot silently replace the existing compressed/liquefied shipping boundary.

For continuity, `public_capture_inventory.csv` evaluates the paired demands with the previously retained Japanese reporting fallbacks: 53.2 kgCO₂/GJ and 0.416 kgCO₂/kWh. The resulting **252.657/249.579/256.567 kgCO₂/t captured** are reporting-factor sensitivities, not supplier-specific CO₂e or full LCA. No waste-heat credit, unverified boiler efficiency, cooling electricity or second capture-fraction multiplier is introduced. These rows are not appended to integrated pathway calculations before conditioning and utility compatibility are established.

## Screened and excluded evidence

- Firecrawl's Johansen accepted-manuscript text identifies a pressure-constrained study and MatMoRA geometry. MRST's dataset description explicitly lacks fluid data. Direct native-paper retrieval returned HTML rather than a PDF. Parser-created tables for figures are unverified, quarantined in the raw response and excluded from every numerical input.
- MRST's `pressureLimitedExample` and helpers were inspected at pinned commit `fa4ff98c78a217d527ae0ec08ecd90c56f66809b`. That is a separate Bjarmeland VE/atlas model with a 90%-overburden penalty, not this compositional case's 225 bar well control. The atlas download returned HTTP 403. No VE geology, pressure rule, porosity or fluid parameters are mixed into the selected deck.
- Cache-prefixed official ZIP links returned HTTP 403 to HEAD requests; the unprefixed official archive URL succeeded with GET. The downloaded ZIP was inspected; a denied HEAD is not evidence of missing data.
- The Tomakomai reboiler/aggregate leads remain unverified. This intake does not repair the June mass classification or missing monthly pressure datum.

## Reproduce and next work

```sh
python paper1/scripts/public_evidence_followup.py
python -m unittest discover -s paper1/tests -p test_public_evidence.py -v
python paper1/scripts/build_workbook.py
python paper1/scripts/build_documents.py
```

Checks verify source bytes, input closure, native cells, rate/pressure pairing, absolute-pressure bounds, field/well agreement and heat/work accounting. They do not rerun the reservoir simulator or validate actual facilities. The original 92-publication corpus remains unchanged; this public intake has its own registers. Next are a documented reservoir rerun and conditioning/utility reconciliation, not substitution of achieved volumes for annual maximum mass service.
