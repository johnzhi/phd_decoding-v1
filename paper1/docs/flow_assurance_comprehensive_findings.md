# Depleted-reservoir flow-assurance audit — 21 November 2026

All 13 retained pages of Charoensuk et al. (2025), OTC 35887-MS / B1-08, have been read and visually inspected. The [item record](comprehensive_review/B1-08.md) covers ten figures, four tables, two printed references and five additional method/model dependencies. No mathematical equations are printed; Peng-Robinson/PR78A, Multiflash, OLGA and techno-economic analyses are described without their complete implementation. Source SHA-256: `17904957ed801363b44321b42145777bd1d59f24094a03f0e91e226a0c5bbc03`.

The paper remains **incomplete under the comprehensive-audit standard**. Complete mixture, network, well, corrosion-test, operating and cost/energy inputs are unavailable locally. Cited originals and external assets remain unverified during the requested Chrome wait. The conference header reports abstract selection and says OTC did not review the contents. The native PDF is unchanged; newly rendered source illustrations are not redistributed.

## Case and pressure boundaries

The project separates CO₂ from sour-gas production, then compresses/dehydrates it and transports it 40 km offshore. Up to 2 MTPA is a **system design target**. Three representative reservoir categories do not disclose the actual compartment/well count or each well's absolute design capacity.

| Category | Approximate TVD | Starting pressure | Ending pressure |
|---|---:|---:|---:|
| Shallow | 650m | 25barg | 70barg |
| Intermediate | 1,550m | 30barg | 170barg |
| Deep | 1,700m | 50barg | 190barg |

These are model boundary states, not demonstrated maximum annual service or fracture-pressure limits. Gauge labels are retained, including the printed 73 barg critical-pressure reference. They are not silently used as absolute-pressure property inputs. TVD is also kept distinct from the tubing-profile length in Figure 4.

## Operating envelope and denominator checks

The three temperature criteria protect different locations:

- Piping downstream of the choke: minimum −46°C.
- SCSSV: minimum −7°C.
- Bottom hole: conservative temperature above 10°C to limit hydrate risk after contact with formation water.

At low flow, the reported SCSSV fluid temperature of −12.7°C is 5.7 K below its stated limit. Raising flow can reduce choke cooling at the valve while worsening the bottom-hole thermal/hydraulic condition elsewhere. No independent rate factor captures the whole envelope.

For the intermediate case at 80 barg upstream of the choke, a 50°C arrival gives a labelled 17°C bottom-hole temperature: a 7 K margin over the criterion. A 60°C arrival gives 30.6°C, but reportedly lowers maximum flow by about 20%. These points do not independently reproduce the optimality or full OLGA sensitivity curve.

The early-life shallow limit is **37.5% of its own well's design capacity**; the deep hydraulic limit is **80% of its own well's capacity**. They are not 37.5%/80% of the 2 MTPA project target, nor constant lifetime injection penalties. The labelled shallow boundary has only 0.6 K thermal margin; the deep boundary has 39.01 K but is hydraulically limited. Temperature margin is not a linear rate-capacity multiplier.

The later 50 barg reservoir-pressure guide and 80→100 barg upstream adjustment remain case-specific. No calendar for reaching those conditions or annual maximum-rate series is supplied.

## Corrosion and composition

The mixture is not fully specified. CO₂ purity above 99 mol%, hydrocarbon carryover below 1 mol% and continuous H₂O/H₂S/TEG labels do not supply the concentrations, heavy-hydrocarbon distribution or interaction parameters needed for independent PVT calculations.

The 40 ppmv water specification becomes 200 ppmv in the stated fivefold-water upset. A 0.001 vol% aqueous condensate fraction is 1×10⁻⁵ of volume; this is different from vapour-water concentration or the **TEG mass fraction above 85% within the liquid**.

Table 3's displayed corrosivity indices, relative to its baseline, are 1, 1, 3.2092 and3.2102. The two upset values differ by 0.10 percentage points of the reference, or about 0.0312% relative to the no-TEG upset. The separate text claim of corrosion inhibition above 85% therefore needs its original film/comparison basis; neither statement is silently corrected or used as an accepted factor. The reported material-test bound below 0.013 mm/year is below 13 µm/year, without a supplied native protocol or field-life extrapolation.

Maintaining the bulk CO₂ stream in its intended phase does not mean no trace aqueous phase exists. The paper explicitly acknowledges condensate and bottom-hole resaturation by connate water. Its phase/pressure and dehydration rules are not universal hydrate or corrosion guarantees.

## Design comparison and transient conditions

Table 4 reports the following relative quantities:

| Option | Pipe label | Energy index | CAPEX index | OPEX index | Reported GHG difference |
|---|---:|---:|---:|---:|---|
| Insulation | 14inch | 1.00 | 1.00 | 1.00 | Baseline |
| Offshore heater | 12inch | 1.50 | 1.40 | 1.40 | +60ktCO₂/year |
| Gas phase | 24inch | 0.90 | 1.10 | 0.90 | “Similar” |

Insulation is selected for minimum upfront capital and lower energy than offshore heating. Gas phase has lower reported energy/OPEX but **cannot maintain early total injection without more wells or larger tubing** at its 50 barg platform limit. Those changes are not a matched full-chain asset/cost/inventory comparison.

The 1.5 W/m²/K insulation U-value is a heat-transfer coefficient, not an insulation thickness. The heater's 20→50°C lift is 30 K, not a disclosed heater duty. Absolute energy/cost baselines, electricity supplier/emission factor and complete construction/material/production boundaries are absent. “Similar” remains qualitative, not numerical zero. The heater's CO₂/year difference is not a verified lifecycle CO₂e factor.

Initial start-up can briefly produce −64.6°C fluid downstream of the choke. Its 18.6 K difference below the piping design threshold does not alone demonstrate wall failure: wall response, exposure and ramp controls need reproduction. Shallow/intermediate wells may require hydrate inhibitor until bottom-hole temperature exceeds10°C.

The approximately two-hour “no-touch time” is a **warm-restart condition**, not a typical outage duration or availability probability. Cold restart first uses the deep reservoir before resuming other wells. Figures 9–10 show different transient flow/temperature paths; their operating pressures, flow denominators and initial/control states are not sufficiently supplied to merge them with the steady envelope or integrate annual service.

## Consequence for Paper 1

Use this source as case-specific evidence that pressure, temperature, rate, equipment and restart conditions interact. Do not join the anonymous PTTEP Sarawak case to other Malaysian studies without identity evidence. Its capture-from-sour-gas counterfactual includes enabled hydrocarbon development and differs from an existing Japanese industrial stream.

[audit_flow_assurance.py](../scripts/audit_flow_assurance.py) produces [53 limited checks](../outputs/comprehensive_review/B1-08_diagnostics.csv), including explicit missing well capacities, insulation thickness, heater duty, absolute energy and annual schedule. It does not reproduce PVT, corrosion, material tests, OLGA, full costs or net lifecycle GHG. Accepted operating/GHG inputs remain unchanged. Continue with B1-09 while original-source and model verification remain open.
