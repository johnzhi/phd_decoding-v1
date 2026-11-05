# Operational model: implemented scope and results

This update implements B0–B3 at a clearly defined proxy-service and shipping boundary. It produces **144 pathway comparisons, 36 model contrasts, 6 equal-injection/added-vessel controls, 6 fleet-adequacy cases and 144 optional onboard-generator inventory scenarios**. These are model outputs, not additional observations or a calibrated Japan–Malaysia–Australia forecast.

## Inputs and provenance

`data/operational_parameters.csv` lists 30 located operating quantities. They overlap the broad extraction ledger; do not add these register counts together as independent data. Source rates and annual allocation figures remain in the supplementary datasets. Values newly used in the model, including the 3.206 tCO₂/t fuel factor, are explicitly located in this dedicated input register.

- Budiarto B4-06-S1: fourteen source rates sum to 5.327 Mt/y; the original thirty nominal years are retained. SW-A and MW-A allocation heatmaps define lower/higher-service *proxy schedules*. They are not measured physical injection upper bounds.
- Noh & Kang B4-09: vessel volumes 40,000/80,000/120,000 m³; one-way distance scenarios 1,000/5,000/10,000/15,000/20,000 km; 15 knots; 12-hour load/unload operations and 12 hours per port; 98% outbound fill and 5% return heel; 8000 operating hours per 8760-hour nominal year; terminal volume 150% of vessel volume; published fuel rates.
- **Density decision:** the explicit Table 1 value 1154 kg/m³ reproduces all 75 Table 7 fleet counts. It is conditionally selected for this scenario. The inconsistent 1.1546 kg/m³ prose is not silently repaired or treated as resolved. Reproducing fleet arithmetic does not independently measure fluid properties.
- Jeong B1-19 p4: 3.206 tCO₂/t fuel is an MGO combustion factor transferred explicitly to the MDO fuel-rate proxy. It is not a well-to-wake CO₂e factor. The optional generator scenario uses the published 197.5 g/kWh SFOC.

Nautical-mile conversion, means, integer vessel decisions and rounding envelopes are unit definitions or model calculations, not new empirical measurements. All structural choices are in `operational_model_conventions.json`.

## What is simulated

B0 uses a static service proxy and a fixed fuel factor calibrated at full source flow. B1 changes the service to annual values. B2 uses the static proxy and resolves discrete ship states, integer fleets, terminal buffers, cargo, heel and available operating windows. B3 combines annual service and operational shipping.

The continuous-time event model tracks loading, outbound movement, unloading and return, together with berth queues and unavailable periods. Published durations and constant active fuel rate determine operating fuel. Waiting/idle fuel lacks a supported quantity and is reported as an inventory gap rather than assigned a physical zero emission factor. Capture is curtailed when the source tank fills. Import injection follows the stated annual service proxy at a constant within-bin rate. Batch accounting assigns cargo at loading start and receives it at unloading end; no thermodynamic BOG dynamics are inferred.

The initial system has no CO₂ cargo. Heel is charged from the source, included in the marine balance and retained as inventory on return. At every event, captured mass equals injected mass plus source, destination and marine inventory. Cargo remaining at the project endpoint receives no injection/storage credit. Active periods obey the published 8000-hour annual limit, and port phases must fit within the prescribed windows.

Window placement is not provided by the source. The primary engineering scenario staggers annual availability across vessels; the sensitivity synchronises it. The source duration remains 8000 hours in both. One berth per terminal, the conservative start rule and greedy dispatch are declared structural conventions, not measured local conditions or an optimal schedule.

Two static representations are tested: a thirty-year aggregate mean, and readiness-preserving constant post-readiness rates per reservoir. Their nominal cumulative envelopes equal the original rounded-profile totals. Operational results need not equal them because of source limits, inventory, scheduling and capture curtailment.

## Meaning of the climate-related output

The reported allowance is additional injected mass minus additional inventoried ship-combustion CO₂. If a compatible fossil-source counterfactual and retention reconciliation are established, a full higher-service advantage requires its **additional uninventoried burdens** to be smaller than this allowance. Missing capture, upstream fuel, terminal/process, injection, asset and retention terms are not zeroed. `net_avoided_ghg_t` is deliberately empty.

The earlier Fraga aggregate GWP factors do not enter this operational calculation. Their fugitive-loss decomposition remains unresolved. The current allowance avoids claiming that an aggregate score is complete avoided GHG.

## Controls that change the interpretation

At 40,000 m³, the source annual-capacity formula gives 2 ships for the 1,000 km lower-service route. Under the selected staggered event-calendar and buffer conventions it achieves about93.3% of the continuous no-inventory reference. A restricted design search adds vessels until it reaches a transferred 99%-of-reference criterion, selecting 3 ships. This 99% is a declared adaptation of Bjerketvedt's completion criterion; it is not a local reliability probability, and its denominator is explicitly different from total source potential.

For the higher-service route, the corresponding selected fleets are 7 at 5,000 km, 14 at 10,000 km, 21 at 15,000 km and 25 at 20,000 km. This is minimum added fleet beyond the reference under the model's rules, not a full cost/capital optimum.

After that adequacy control, the conditional differential allowance is approximately **+1.281 Mt at 5,000 km** and **−4.923 Mt at 10,000 km**, relative to the lower-service1,000 km proxy. These are not destination rankings: changing availability placement or inventories changes the conclusion, and the missing differential burdens remain unknown.

A separate equal-injection control reaches the same injected mass on both paths. The longer route then adds approximately 4.385 Mt and 9.865 Mt of ship-combustion CO₂ at 5,000 and10,000 km. This isolates the transport penalty within the modelled boundary. Another control adds one vessel to each route: in the 10,000 km case the raw reference-fleet allowance changes sign. The apparent benefit in the uncorrected reference case therefore cannot support a robust route preference.

The nominal 5,000 km reference-fleet B3 allowance is about+11.514 Mt under staggered windows and−2.625 Mt under synchronised windows. That sensitivity is a warning about the unsupported availability calendar, not evidence for either local operating pattern. More geometry or a preferred-looking threshold cannot replace validating that assumption.

## What remains before a complete Paper 1 result

1. Independent physical annual injection limits, well schedules and raw allocations, rather than only optimised allocation figures.
2. A compatible source capture heat/electricity inventory and its energy-supply emissions.
3. Fuel upstream/non-CO₂ factors, realistic idle/port fuel, actual BOG/terminal duty and pressure-conditioning compatibility.
4. Injection, extra wells, water/pressure management, construction, monitoring and retention inventories.
5. Observed or defensibly designed availability calendars and fleet/berth constraints; three alternative priority controls are now implemented, but observed operator validation remains absent.
6. The original lower/higher comparisons are separate alternatives. A subsequent shared-source annual MILP and fixed-plan operating reevaluation are now implemented; detailed adaptive joint optimisation and complete lifecycle objective remain separate. See mixed_allocation.md.

A positive allowance is conditional; a negative allowance does not by itself prove a full disadvantage if omitted differential burdens favour that pathway. The complete accounting condition must be evaluated.

## Reproduce and verify

```sh
python paper1/scripts/operational_model.py
python -m unittest discover -s paper1/tests -v
```

The tests check located inputs, all 75 source fleet counts, zero-source behaviour, annual and total material balances, source and injection limits, buffer bounds, operating hours, fuel integration, preservation of static-proxy totals, equal-injection targets and the interaction identity. These verify implementation and selected source cases; they do not validate real reservoir physics or a complete regional lifecycle model.

Online investigation is recorded in `evidence/online/search_log.json`. Chrome tools were unavailable. One public GitHub repository query found no matching repository; this is not an exhaustive web search. The source paper's p18 says underlying data are available from the corresponding author on reasonable request. No author message was sent.

## Subsequent reference-inventory extension

The original operating outputs above retain their combustion-only boundary for audit. `reference_inventory.py` now replaces that fuel component with the IMO MDO/MGO default WtW scenario and adds named NETL/utility references against captured mass. It evaluates20 utility scenarios and2,980 paired balances. See [reference review](reference_dataset_review.md) for source boundaries and results. No missing duty, supplier identity or lifecycle component is zero-imputed.

Under the restricted fleet-adequacy control at5,000km, the NGCC90 replacement reference with Norway's2025 climate-disclosure factor leaves about+0.009Mt, compared with−0.984Mt using the Japanese reporting-electricity fallback and−1.207Mt for the paired PC90 heat-plus-auxiliary route/Japanese fallbacks. These partial balances supersede a climate interpretation of the earlier+1.281Mt combustion-only margin. Full net avoided emissions remain uncomputed.

The two uploaded wave files contain one point/time each, and the IBDP seismic-rate catalogue does not contain injection-rate histories. Independent St.Peter/Knox-Potosi simulation values are retained for future reservoir benchmarking without inventing missing annual curves. Realistic calendars and original independent rate constraints remain unresolved.

## Follow-up component and mixed-model checks

All92 unique supplied papers now have targeted full-text review of selected passages. `property_consistency.py` independently supports the selected1154kg/m3 pure-fluid table density under explicit pressure-reference interpretations without repairing the prose or measuring actual cargo. `mixed_allocation.py` adds12 annual mixed-integer plans,72 operating reevaluations and18 dispatch controls; [its specification](mixed_allocation.md) defines source sharing, disjoint sink groups, fixed annual plans and residual limits. `limitation_benchmarks.py` adds the paired MEA utility reference. The optional selected Northern Lights storage subset changes the previous near-zero5,000km partial margin to−4.44kt; these later checks supersede any claim of a positive full lifecycle advantage.
