# Japanese case evidence and Northern Lights component audit — 5 November 2026

This intake has26 uploads,25 retained files and one unavailable IBDP ZIP exceeding the32MiB transfer limit. Seventeen PDFs contain1,186 indexed pages. Indexing is not a scientific review of every page. The dedicated register has420 located numeric records; source-native exports remain separate. These counts overlap their tables and are not independent observations.

## Tomakomai: a usable Japanese historical benchmark

D7-20 Table3-2, physical p3, supplies45 monthly records from April2016 to December2019 for Moebetsu and both formations, with separate monthly and cumulative quantities. The table is rotated; original PDF word coordinates recover180 numeric cells without OCR. Eight fiscal annual/cumulative cells are retained separately. Precision varies: one cell is0.01×10^4t, most are0.1×10^4t. Explicit printed zeros are retained at their original precision. None of the monthly/fiscal/cumulative series is normalised to another.

There are real source reconciliation issues. For April2018 the printed Moebetsu cumulative quantity is17.4×10^4t while the combined cumulative row prints18.8×10^4t. Other combined-row entries and monthly/fiscal sums also differ. The original strings and coordinates remain available. A discrepancy is a reason to request the native data, not a reason to silently repair a value.

D7-22 Table5.2-1, physical pp10–11, gives17 selected shut-in/test records with dates, reported measurement duration, prior average annualised injection rate, cumulative mass and cause. FOA17 continues beyond the reported endpoint; its end/duration remain empty. These are measurement windows, not a complete failure calendar. Reported measurement duration and full elapsed interval can differ; no future outage probability is inferred. Supply-side and compressor interruptions are distinguished from planned tests and inspection.

D7-18 Table5.1-3, physical p10, provides nine fall-off interpretations. Effective kh spans3,000–6,650mD·m, a ratio of2.217; these are source-inferred effective parameters rather than nine independent measurements of intrinsic permeability. FOT11 reports83,618t/y in this table, versus83,620t/y in the overview; both values remain distinct.

The2024 analysis explains a52m depth difference between the921mTVDSS PT sensor and973mTVDSS completion top. Reported density ranges470–670kg/m³. A hydrostatic reference calculation using standard gravity gives approximately101.99kPa difference across that density range, consistent with the report's approximate100kPa statement. This is about4.08 times the25kPa source history-match comparison level. It demonstrates why sensor depth and density correction matter; it does not validate our own reservoir forecast. The pressure plot on p14 has differing MPaA/MPaG labels, so no absolute-pressure trace is fitted from it.

The2019 report also supplies a coherent *prospective Case2*: a hypothetical2021 restart, operating rate220,000t/y with June shut-in, a12.93MPaG completion-top cap and pressure/plume screening over1,000 years. The30-realisation analysis reports capacity labels P90/P50/P10 of1.47/4.70/7.93Mt. They are simulated/source-labelled outputs, not an adopted probability distribution, independently measured annual upper bounds, future contracts or evidence that restart occurred. Alternative completion cases and capacity results are retained separately. Table5.4-5's pressure cap and fracture pressure must not be interchanged; some Case3-2 plot labels require reconciliation.

The September/October2026 newsletters still report injection terminated22November2019 and cumulative total300,110.3t. Historical project evidence does not establish current injection service. The2024 capture chapter describes maintenance and suspension; it does not supply the missing process-specific capture utility inventory.

## Japanese source exports: identities and units need care

`info.csv` identifies Nippon Steel (特定排出者コード985336900). The company export contains225 category/year cells for2009–2023, of which108 are numeric; absent reports remain missing. Categories and adjusted totals are not added together. The source notes describe changes to waste-derived emissions and later energy-category splitting, so changes across reporting definitions must not be mistaken for physical trends.

The facility export gives78 reporting-year records. Preserve its **report-year** header: it is not automatically the emissions fiscal year used in the company export. Similar facility names may refer to different reported boundaries; no automatic merging or summing is performed. Total GHG is not capturable CO₂, a stack concentration, capture fraction or a no-CCS industrial-production inventory.

The additional-information export refers to ENEOS and its Scope1/2/3 reporting, while the metadata identify Nippon Steel. It is not joined into the Nippon Steel inventory. Resolve its original exporter/entity before use. Tomakomai's refinery PSA stream is also not silently equated to either steel-site total.

## Northern Lights: component values and internal checks

D7-15 is a prospective March2023 transport/storage assessment. Its boundary starts with customer-liquefied CO₂, excluding customer capture and liquefaction. LNG/MDO European voyages, project throughput, infrastructure and GWP methodology remain specific to that study.

The appendices provide25 numeric component quantities and31 blank activity cells. Blanks remain unquantified. The numeric sum is3.31129812MtCO₂e, compared with the3.32Mt headline; the−8,701.88t difference is not forced away. Appendix ship-fuel GHG is2.638032Mt, while discussion p11 states2.15Mt/65%; both are preserved. Phase2 capacity wording, the lifetime throughput/injection duration and GWP references also need reconciliation before reconstructing the complete original LCA.

The reported source-carbon fugitives are96,725tCO₂, approximately0.75685kg per reference tonne stored. These must be reconciled with captured/injected/retained mass before a net-mitigation calculation. Adding the aggregate26kgCO₂e/t footprint to a model already charging ship fuel would overlap emissions and can double-count source losses.

A separate, optional sensitivity uses only printed **storage** components excluding `Other process emissions`. Their sum268,220tCO₂e divided by127.8Mt reference storage gives2.098748kgCO₂e/t. This is an average reference-burden transfer, not a marginal asset response or complete storage inventory. Missing blank categories and GWP/energy/phase differences remain. No aggregate shipping footprint is added.

Applied to the previously design-controlled5,000km comparison, this optional transfer adds about13.13kt and changes the NGCC90/Norway-climate margin from+8.69kt to−4.44kt. This conditional result shows how a small omitted-component scenario can reverse a near-zero margin. It does not establish a real destination ranking or full lifecycle disadvantage. The100 optional sensitivity rows retain null full-LCA results.

## Shipping and port context

The World Bank Excel annex is now available:424 rows with nonempty port names, CPPI indices/ranks, sample calls and berth share are retained. Container-port indices and berth-hours percentages do not supply absolute liquid-CO₂ terminal turnaround hours.

EXCOOL is a1,450m³,12-knot domestic demonstration vessel with maximum engine output1,471kW. Its greater-coasting/non-international specification and lack of a fuel/duty curve prevent transfer as the international40,000m³ fuel model or a weather limit. The2026 IMO circular gives a particular ethanol pathway factor; it does not supersede the fossil MDO/MGO default used by the current model.

## Data that now matters most

Prioritise Tomakomai's native timestamped rate/pressure/temperature data, sensor/depth/datum corrections and model exports. Its historical observations and simulation cases make it a stronger local benchmark. Raw realised rates still do not by themselves identify independently achievable maximum rates. Obtain the30-realisation Case2/Case3 inputs and pressure-constrained output schedules if the source model is to be independently reproduced. IBDP remains a useful alternative benchmark; its oversized ZIP still requires smaller parts.
