# Korean transport costs: comprehensive retained-PDF findings

Kang, Seo, Chang, Kang and Huh (2015), *Energies* 8, 2176–2196. DOI: [10.3390/en8032176](https://doi.org/10.3390/en8032176). Retained source: [B3-07](../papers/B3-07.pdf), SHA-256 `cb1ef1b0e6b0cb2951f19fd44079f382185007977c23dde37ac806071aa77cfd`.

All **21 retained physical pages**, seven figures and all panels, four tables, captions, legends and six numbered equations were read as text and visually inspected. Figures 4–7 and Equation 2 received enlarged checks. The [item record](comprehensive_review/B3-07.md) tracks 47 claims, 18 variable groups and 18 issues. **Comprehensive status remains incomplete.**

[Native equation regions](../evidence/comprehensive_review_inputs/B3-07_equations.json), [table transcriptions and geometry](../evidence/comprehensive_review_inputs/B3-07_tables.json), [figure labels](../evidence/comprehensive_review_inputs/B3-07_figures.json) and [45-entry bibliography](../evidence/comprehensive_review_inputs/B3-07_bibliography.json) preserve provenance. Two additional named standards and fourteen dependencies bring the manual register to 61 items. Only two have scoped checks against exact originals; neither original paper is comprehensively complete.

## The comparison and its boundary

The three scenarios use Boryeong alone, Boryeong plus Hadong, or two sources feeding Ulsan and a shared offshore pipeline. They are restricted planning cases. Ulleung's **5 Gt** resource does not establish annual injection service. The paper expressly assumes **100 bar wellhead pressure** because the reservoir depth and conditions were undetermined. Its **86–150 bar** pipeline band and 150 m seawater depth are transport assumptions, rather than reservoir pressure calibration.

The system excludes **capture and storage costs**, while including initial compression or liquefaction, transport equipment and pumping/heating to the assumed wellhead state. The plots' “Injection” category means conditioning for injection; it does not demonstrate storage operation. Hub tank injection/discharge handling costs are explicitly excluded.

| Scenario 1 design load | Pipeline, about 530 km | Ship, about 724 km |
| --- | ---: | ---: |
| 1 Mt/year | about 33 USD/t | about 28 USD/t |
| 3 Mt/year | about 21 USD/t | about 23 USD/t |

These are approximate source-case unit costs per **transported** tonne, not avoided or permanently retained tonnes. The quoted scale reductions are approximately **36.36%** and **17.86%**. Unequal routes, duplicated conditioning, source locations and fixed cost assumptions prevent interpreting the crossover as a universal transport-distance rule.

## Rate, route and state discrepancies are preserved

The paper says approximately **2800 kg/s corresponds to 1 Mt/year** and describes continuous injection. Under a disclosed 365-day conversion, 1 Mt/year is **31.70979 kg/s**, whereas continuous 2800 kg/s gives **88.3008 Mt/year**. At the printed rate, 1 Mt would take about **99.21 hours**. No alternative unit or corrected source rate is proposed.

Table 2 lists shipping legs of **617 km** and **270 km**, totaling **887 km**. The discussion says **877 km** and a **22%** increase over 724 km. The table sum gives **22.51%**; the prose distance gives **21.13%**. Exact routing and rounding need clarification. Both original distances remain visible.

Figure 3 and the main text use feed **1 bar/35°C** and cargo **7 bar/−50°C**. Figure 4's detailed scheme instead labels feed **1 bar/25°C** and product **6 bar/−53°C**. Its components and recycles were inspected, but no native stream or duty balance establishes their case correspondence.

A **pure CO2, absolute-pressure** illustration using pinned CoolProp 8.0.0/HEOS gives about 1154.6 kg/m³ at 7 bar/−50°C. Nominal 6 bar/−53°C lies on the gas side of the saturation boundary; allowing the whole-number labels rounding intervals spans both gas and liquid. This does **not** establish a native HYSYS phase error or validate impurities, solids, hydrates or equipment. Similarly, pressure above the critical value alone does not establish a liquid pump inlet at 40°C.

## A conditional fleet timing bound

The study assumes three ships, 15 knots, 20 hours each for loading/unloading and two hours each for port entry/exit. With 724 km each way, those allowances give an ideal roundtrip of **96.12383 hours**.

**If each 20-hour unloading interval is the only direct well-delivery window**, three ships provide at most `3 × 20 / 96.12383 = 62.42%` continuous-time coverage, before weather, maintenance or extra stops. Five is then a necessary mathematical vessel-count bound, not a native optimum or recommended fleet.

The authors' actual injection duration, control, receiving buffer or operating chronology could change this interpretation. Their referenced availability model and native schedule are required before declaring the native design feasible or infeasible. The hub's separate two-hour pipeline-buffer assumption does not establish ship-side receiving continuity or annual field service.

## What the formula and financial checks establish

The six equations cover friction/gravity pressure difference, compressor capital, pump capital, booster capital, steel annulus weight and minimum wall thickness. Literal components were implemented with explicitly disclosed analyst geometry and properties. The native 64-design optimization remains unreproduced: actual standard sizes/schedules, friction/density, route profiles, booster assignments and cost arrays are missing.

Eight priced steel grades and eight diameter choices are consistent with 64 candidates; the ninth listed grade, X90, has **N/A** price. The annulus formula matches the independent outer-minus-inner-cylinder volume identity. Steel price/strength alone does not replace schedule and fabrication selection. Internet prices accessed in March 2015 and unspecified “ton” bases are not current cost inputs.

Equation 2 is linear in the number of fixed-flow trains, but sublinear in train flow at fixed train count. “No compression scale effect” therefore requires the native train-sizing rule. The 40 MW splitting threshold cannot determine train count without native power. The reported five stages at ratio 2.36 are compatible with rounding: the exact average ratio for 1 to 73.8 bar is about **2.36380**.

The **0.08 capital recovery factor** is also rounding-compatible with 20 years and 5% interest: the conventional component is **0.08024259/year**. It is not an 8% discount rate. No full author cash-flow replay is claimed.

Liquefaction's **1.6 CAPEX** and **1.7 OPEX** multipliers relative to compression are financial proxies, **not heat or electricity ratios**. Aggregate conditioning costs and the roughly 7 USD/t premium cannot supply actual duties. The paper has no complete matched capture heat, auxiliary electricity, compression, liquefaction, cooling or utility-supplier inventory. Likewise, 850 USD/ton fuel is a price, not an emissions factor.

## Two scoped original checks

The [citation checks](../evidence/comprehensive_review_inputs/B3-07_citation_checks.json) retain exact source hashes and inspected pages:

- **R013: Roussanaly, Brunsvold and Hognes (2014), B3-36, pp1,3,4,6.** Section 2.1 and Tables 1/2 explicitly start both transport chains at **1 bar**, with conditioning included. B3-07's description of references 11–14 as starting already above 100 bar does not describe this base case. The original excludes the glycol dehydration unit and uses different delivery conditions. Its selected passages do not provide a complete capture inventory or validate the Korean model.
- **R035: Aspelund, Mølnvik and de Koeijer (2006), B3-35, pp1,5,6.** Supports heating/pressurization, seawater-icing concerns, fuel-heating emissions and an alternative platform waste-heat route. Its offshore cases use **200–300 bar and 15–20°C**, or different transfer/heating stages; it also discusses batch injection. It does not certify B3-07's assumed 100 bar/10°C, continuous three-ship operation or disputed mass-rate equivalence. Its energy/GHG factors are not transferred.

## Hub interpretation and remaining evidence

Figure 7 has eleven cases. Comparing two distributed 1 Mt sources plus a hub with one concentrated 2 Mt source changes source geography and conditioning as well as the hub. The paper also discusses the more appropriate matched separate-source and marginal-addition comparisons. Their simple unit-cost averages rely on equal 1 Mt flows; unequal flows need mass weights.

The short 60 km shared trunk, only two source routes and extra equipment explain this case's small hub benefit. They do not establish that hubs are generally uneconomic. The concluding future-capacity recommendation still needs demand, timing and stranded-capacity analysis. Historical Korean deployment targets are not verified present operations.

Native HYSYS/economic files, pipeline candidate data, ship payload/schedules, GIS, full cited models and possible supplementary assets remain unverified. Article CC BY 4.0 does not supply those assets or their commercial software/data rights. External retrieval remains paused pending the requested Chrome connection; no outreach was sent.

Run `python paper1/scripts/audit_korea_transport.py` for **36 limited checks, nine steel rows, four compressor examples, three conditional fleet rows, seven nominal pure states and four rounding corners**. Five tests cover unit conversion, hydraulic/annulus identities, train scaling, the conditional timing bound and phase-rounding limits. No accepted operating/GHG input or current numerical result changed; the combined 1.5 MPa HOLD remains. Continue with B3-08.
