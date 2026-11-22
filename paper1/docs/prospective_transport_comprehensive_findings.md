# B2-13 prospective transport LCA audit

Nöhl, Burger, Oeuvray, Becattini, Seiler, Shu, Mazzotti and Bardow examine European CO₂ transport through 2100 in *Journal of Cleaner Production* 514 (2025) 145659, DOI [10.1016/j.jclepro.2025.145659](https://doi.org/10.1016/j.jclepro.2025.145659). The [retained PDF](../papers/B2-13.pdf) is CC BY 4.0. SHA-256: `4a0815a62c5f60d76eb4a939b2cfcd31ba50b48162b9762cdb0ac39dd25a423b`.

All **11 main-PDF pages** were read as text and visually inspected, with five magnifications. The [item record](comprehensive_review/B2-13.md) covers all five figures, ten panel/legend records, one numbered equation and five additional reconstructed relations, 24 variable/assumption groups, 79 claim records and 16 open issues. There are no standalone tables in the main PDF. All 53 printed references were inspected and preserved with native line geometry; none of their original passages was independently verified in this review.

**Overall status remains incomplete.** Supplements A/B, native models and licensed inventories are not verified locally. The paper states that models are included in supplementary material and data can be licensed from ecoinvent. Local absence does not establish online absence. External retrieval remains paused under the user's instruction to wait for a Chrome connection.

## Boundaries and reference flows

The paper distinguishes two boundaries, which must not be pooled:

| Boundary | Functional unit and included work | Material exclusions |
| --- | --- | --- |
| T | One tonne of conditioned CO₂ transported one kilometre; full outbound and empty-container return for batch modes; one-way pipeline service and pressure-loss work | Initial/final conditioning, capture, purification and geological storage/retention |
| T+C | One tonne of pure, unconditioned CO₂ at 1 bar and 30°C transported one kilometre, including transport and sink conditioning | Capture/purification and geological service/retention |

Figure 1 assigns pipeline pressurization needed to overcome pressure loss to T. Preparation up to the pipeline outlet-pressure state and subsequent sink conditioning additionally enter T+C. A combined inventory must avoid counting the same work twice.

The two receiving conditions are **gas at 25 bar** and **dense CO₂ at 70 bar above 1°C**, attributed to historical terminal/storage examples. They are not demonstrated bottom-hole pressure limits, annual injectivity or permanent-retention guarantees. The main PDF does not establish gauge/absolute pressure basis. No state or pressure correction is invented.

The paper names compression, pumping, cooling, refrigeration and heating, with surface-water cooling and ecoinvent heat-pump, water-pump and refrigeration models. It assumes capture already supplies pure CO₂. Its main PDF therefore does **not** supply a complete, matched capture-to-ship heat, electricity, cooling and supplier inventory. The reported ±4% reproduction of Deng's liquefaction energy is an author validation claim, rather than an independently verified process model.

## Returning heel is not a release

The ISO container has a **9.2 t tare** and **20.7 t liquid-CO₂ capacity at 16 bar**. The authors assume 4% of the CO₂ remains as gas for the return trip. If 20.7 t denotes the initial fill, conservation gives:

| Conditional quantity | Mass (t) |
| --- | ---: |
| Full container | 29.900 |
| Returning CO₂ heel | 0.828 |
| Container plus returning heel | 10.028 |
| CO₂ delivered | 19.872 |

These calculations do not establish the native LCI delivery denominator. The heel returns in the container; it is not a 4% atmospheric-loss factor. Nor does subtracting the full-container mass from the approximate 44 t gross truck mass validate actual vehicle weights or legal operation.

The paper explicitly says battery trucks exceed 44 t in its 2020 and 2025 cases. Those cases need a disclosed feasibility qualification. The 400 km baseline and 150/800 km sensitivity values describe driving-cycle autonomy, rather than actual transport distances or fleet schedules.

## Prospective inventories and pipeline cases

The modeled pipeline cases use **200 km**, **0.3 or 10 Mt/y**, ambient **15°C onshore or 4°C offshore**, and designs optimized for levelized transport cost. An 8 Mt/y supercritical inventory is a separate comparator. Prescribed transport flow does not establish pressure-constrained reservoir service; a cost optimum is not automatically an environmental optimum.

The background combines ecoinvent cutoff 3.8, premise and REMIND 2.1 under SSP2-NDC, SSP2-Base and SSP2-PkBudg500. These are conditional pathways, not probability-weighted empirical forecasts. The source has twelve plotted time points, with annual interpolation for the payback calculation.

Figures 2 and 5 place all lifecycle phases in the same year. That snapshot convention differs from constructing an asset in one year and operating it through a changing background. Figure 3 separately considers switching and a 40-year pipeline lifetime. Its use-phase series cannot be reconstructed by treating Figure 2's total lifecycle intensity as annual operating emissions.

HFO is deliberately held constant because premise lacks a prospective HFO market mix. The broad statement that transport impacts decline by 72–93% cannot be applied to that fixed mode. Electricity and e-fuel scenarios also depend on future electricity, materials and fuel-market assumptions. EUR represents the EU and UK; applying these inventories to Asia requires a disclosed geographic proxy.

## Carbon-payback equation and exceptions

Equation 1 compares old cumulative operating impacts with new construction plus new cumulative operating impacts. Capital is an impact stock; the integrated operating terms need impact-per-year units for the same service. The paper uses annual constant impacts, with each year's values obtained by linear interpolation.

The general first-crossing component is independently reconstructed in [audit_prospective_transport.py](../scripts/audit_prospective_transport.py). For constant rates with positive savings, payback equals capital divided by annual savings. Fractional-year, scale, horizon and reversal checks pass. The examples use explicitly synthetic inputs; they do not reproduce any native LCA case. With changing rates, a first crossing alone does not guarantee continued benefit after that date.

Figure 3 reports these train-to-0.3 Mt/y dense-pipeline paybacks:

| Switching year | Payback (years) |
| --- | ---: |
| 2020 | 3.3 |
| 2025 | 5.7 |
| 2030 | 7.1 |
| 2040 | 6.7 |
| 2050 | 6.4 |
| 2060 | 6.7 |
| 2070 | 7.3 |
| 2080 | 8.1 |

The sequence is not monotonic and does not support an unqualified under-three-year rule. Figure 4 rounds the 2040 train example to seven years. Other explicit exceptions include HFO ship to gas pipeline at **20 or 12 years**, and e-fuel ships to dense pipelines at **14–31 years**.

All **66 Figure 4 cells** are retained in [source_switches.csv](../outputs/comprehensive_review/B2-13_source_switches.csv): 45 onshore and 21 offshore, with 49 finite labels and 17 X entries. These are selected upper-triangle directions; all directed pairs would total 132. The finite count includes a parenthesized 16-year H₂-truck-to-electric-truck case exceeding the modeled lifetime. Displayed zero does not establish instantaneous payback, and no unprinted reverse direction or replacement policy is inferred.

## Category rankings and absolute-sustainability limits

All **272 Figure 5 ordinal ranks** were traced and corroborated against native vector geometry, preserving all sixteen category labels and source colours. The [rank table](../outputs/comprehensive_review/B2-13_source_ranks.csv) deliberately leaves absolute impacts blank. Circle **area**, rather than radius, represents the impact share; exact category magnitudes were not recovered from circles.

The 10 Mt/y dense pipeline ranks first in all sixteen onshore categories and **fourteen offshore categories**. HFO ships rank ahead for **water use and freshwater eutrophication** offshore. Section 3.4 states the fourteen-of-sixteen result, whereas the conclusion on page 10 says all categories. Paper 1 retains the two exceptions.

The ordinal reconstruction also confirms electric trucks ranking worse than H₂ trucks in 11 of 16 categories and diesel trucks in 4. HFO ships outperform ammonia ships in 9 of 15 non-climate categories and methanol ships in 7. These counts are not weighted sustainability scores or impact magnitudes.

For absolute sustainability, the source uses fifteen LCIA-based planetary boundaries and substitutes current global impact for land use. Thus not all sixteen denominators are defined planetary-boundary thresholds. Exact EF 3.0 versus the cited EF 3.1 normalization/land-use reference needs confirmation.

The demand calculation is 0.7 Gt/y × 100 km = **70 Gtkm/y**. Population allocation gives Europe 7.9% of global safe operating space, excluding Russia. A separate comparison to EU-27 road freight gives:

\[
\frac{70}{1800}\,(0.6\%\text{ to }1.9\%)
=0.023333\%\text{ to }0.073889\%.
\]

This assumes the same GVA per tkm and needs alignment between population Europe, EUR and EU-27 geography. The paper reports pipeline category shares up to approximately **0.075%**. An upper bound below 0.075% alone does not establish fit throughout the much narrower sector-allocation range, including its lower end. It also does not establish an actual exceedance: exact case/category arrays are unavailable. The result remains conditional on allocation, route distance, throughput, utilization, scenario and category definitions.

The selected 4 gCO₂e/tkm source intensity converts to **0.4 kgCO₂e/t at 100 km**, or **0.28 MtCO₂e/y at 70 Gtkm/y**. Those are conditional transport-only unit conversions, not a new European network LCA, a whole-chain avoided-emission factor or a storage-permanence result.

## Reproduction and Paper 1 status

The [input record](../evidence/comprehensive_review_inputs/B2-13.json), [bibliography](../evidence/comprehensive_review_inputs/B2-13_bibliography.json) and [reproduction summary](../outputs/comprehensive_review/B2-13_reproduction_summary.json) preserve provenance and missing fields. The script produces **38 limited checks**, 66 source switch cells, 272 ordinal ranks and 40 annual rows of one disclosed analyst example. Eight focused tests cover conservation, dimensional scaling, fractional payback, horizon and reversal behavior, interpolation, allocation units and source graphic consistency.

This does not reproduce native ecoinvent/premise/carculator LCA, Aspen conditioning, pipeline optimization, absolute planetary-impact arrays or author payback cases. All 53 originals and thirteen dependencies or scope requirements remain open. Paper 1 should acknowledge prospective transport and carbon-payback precedent, preserve the demonstrated tradeoffs and retain its distinct physical-service and whole-chain inventory requirements.

**No accepted operating/GHG input or current numerical result changes.** The prior combined 1.5 MPa HOLD remains. Native files and source hashes are preserved; the comprehensive goal remains active.

Regenerate the scoped calculations with:

```bash
python paper1/scripts/audit_prospective_transport.py
python -m unittest discover -s paper1/tests -p test_prospective_transport.py
```
