# Partial BOG reliquefaction: comprehensive retained-PDF findings

Chu, Chang and Chung (2012), *International Journal of Greenhouse Gas Control* 10, 46–55. DOI: [10.1016/j.ijggc.2012.05.016](https://doi.org/10.1016/j.ijggc.2012.05.016). Source: [B3-08](../papers/B3-08.pdf), SHA-256 `fb3fc40fbca20613816253c83c1f3655e849e9a21be7722582a6de4958f5d7a7`.

All **ten retained pages**, fifteen figures, six tables, nomenclature, thirteen numbered equations and six process assumptions were read and visually inspected. The process diagram and derivative/sensitivity plots received enlarged checks. The [item record](comprehensive_review/B3-08.md) tracks 42 claims, 18 variable groups and 17 issues. **The comprehensive audit remains incomplete.**

[Native equation regions](../evidence/comprehensive_review_inputs/B3-08_equations.json), [table rows and geometry](../evidence/comprehensive_review_inputs/B3-08_tables.json), [figure register](../evidence/comprehensive_review_inputs/B3-08_figures.json) and [bibliography](../evidence/comprehensive_review_inputs/B3-08_bibliography.json) preserve provenance. Thirty direct bibliography entries plus fourteen further dependencies are not 44 verified originals. Only one direct edge has a scoped original-passage check.

## An economic optimum with specific assumptions

The objective combines reliquefaction energy expense, penalties for vented and generator CO2, and revenue from recovered CO2 sold for EOR. It minimizes **financial treatment expense**, rather than complete lifecycle emissions or physical risk. A negative expense or lifecycle cost means assumed revenues exceed costs; it does not mean negative emissions or permanent storage.

The source reports different ranges in different passages:

| Passage/case | Reported optimum fraction |
| --- | --- |
| Abstract and conclusion, broad scenario wording | roughly 95.7–98.2% |
| Body, taxed scenarios | 97.2–98.1% |
| Body, no emissions penalty | 95.7–97.5% |
| Body, 20 USD/t penalty and varying oil price | 97.2–97.7% |

These are preserved separately. They are neither universal vessel loss rates nor validated optima for Paper 1's ships. The native work curve, exact derivative and case arrays are not supplied. Figure 13's approximate zero crossings lie around **98.1–98.6%**, without transparent correspondence to Figure 15's stated oil-price/tax cases. Axis, derivative-unit and case definitions require clarification; no axis shift is inferred.

## Generated BOG, bulk gas and CO2 recovery are different bases

The model assumes a 100000 m³ carrier, 1155 kg/m³ cargo density, 95% initial fill and 0.12%/day boil-off. The authors explicitly say detailed vessel, insulation, environment and voyage information were unavailable. The BOR rests on LNG analogies and an assumed 10 cm insulation layer.

The paper quotes 5400 kg/h nominal BOG, then uses **6000 kg/h** with a design margin. Applying the stated BOR to the nominal full cargo gives **5775 kg/h**; applying it to the 95% initial fill gives **5486.25 kg/h**. Approximation and volume/fill bases remain unresolved. None is substituted for the source's values or accepted as an observed BOR.

Table 3 describes CO2/N2/O2 bulk gas. The financial section then explicitly says “BOG” refers only to the **CO2 component**. Its generated/reliquefied/vented balance and recovery fraction need that component basis. Applying the reported fraction to all bulk BOG or total retained ship cargo would require further mass and phase accounting.

At 6000 kg/h and 90% of calendar time, the stated **47304 tonnes/year** follows exactly. This is design-load arithmetic, not actual annual venting. The cylindrical tank bodies alone also do not uniquely establish total usable volume; head geometry and capacity definitions are missing.

## Unit conversions and the missing generator factor

The nomenclature gives mass flow in **kg/h**, compressor power in **kW**, specific work in **kJ/kg**, fuel-energy cost in **USD/kJ**, and treatment expense in **USD/t BOG**. The compact equations require explicit time and mass/currency conversions.

For illustration, **analyst** specific work of 270 kJ/kg at the quoted 6000 kg/h is **450 kW**, or **75 kWh/t BOG**. Raw `kW / (kg/h)` is kWh/kg; it needs a factor 3600 to express kJ/kg. Multiplying kJ/kg by USD/kJ gives USD/kg; multiplying by 1000 gives USD/t.

A disclosed consistent diagnostic basis is:

`E_L = 1000 × w[kJ/kg] × C_L[USD/kJ]`

`E_P = [1 − x + gamma[kgCO2/kWh] × w/3600] × C_P[USD/tCO2]`.

These are unit diagnostics, not a claim that the unavailable native code omitted conversions. The generator coefficient is not numerically supplied. The stated fuel's 86% carbon gives **3.1533 kgCO2/kg fuel** under complete oxidation, but fuel rate or generator efficiency is still needed to calculate emissions per electrical kWh. Approximate graph heights do not supply a calibrated generator inventory.

The paper provides neither a complete matched capture heat/electricity/compression/liquefaction/cooling/supplier balance nor an annual reservoir pressure/well dataset.

## Phase and process feasibility remain open

The propane–**ethylene** JT cycle uses six explicit assumptions, including 40°C refrigerant outlet after seawater cooling, 5 K minimum approach and 80% compressor polytropic efficiency. Native stream pressures, refrigerant flows and detailed equipment outputs are missing.

The paper states that recovery above 98% requires cooling the BOG below **−65.6°C**, about **9 K below its quoted pure-CO2 triple temperature**. Table 1 also prints **0.917 mol% water** in stored liquid at −51°C, equivalent to 9170 ppmv as a composition conversion. Those values are preserved without guessed corrections.

A Peng–Robinson fluid calculation and a schematic do not establish mixture-solid/hydrate feasibility or treatment of that water. The pure triple-temperature comparison does not prove the exact mixture is infeasible; it identifies a material phase-validation requirement before reproducing or transferring the reported optimum. No corrected process temperature or composition is supplied. A separate pure-CO2 critical-density reference gives **467.60 kg/m³** with CoolProp 8.0.0/HEOS and the Span EOS, versus the source's **600 kg/m³** quote. This does not correct a native mixture or cargo density.

The pressure/level chart similarly comes from assumed heat ingress and a generic design-margin argument. It does not certify a seven-day voyage limit or observed pressure behavior for an operating vessel.

## Price cases and one algebraic qualification

The MDO baseline is **1100 USD/t in prose**, but Figure 8's caption says **1200 USD/t**. Both remain recorded. Oil-price projections use 2008 dollars from a 2010 outlook; carbon prices and EOR-sale proceeds are scenario assumptions, not verified current prices or eligibility.

The historical market table gives a 2009 value of **143.735 billion USD**, while the text says **114 billion USD**. Table-based growth of 6.42%, a mean value of 16.52 USD/tCO2e and a 40.85% mean-price fall agree with the approximate 6%, 16.5 and 41% statements. One-unit subtotal differences are compatible with rounding. The larger prose/table value discrepancy remains open.

Holding other inputs fixed, the source objective gives:

`partial E_T / partial C_P = 1 − x + generator-emission fraction >= 0`.

Thus raising the carbon penalty cannot lower treatment expense at a fixed design. Minimizing over the same feasible set preserves this nondecreasing relationship. The paper's decreasing-expense wording needs qualification: optimum recovery may rise while financial expense rises and profit falls. Figure 12 and Table 6 follow that direction.

Four **invented convex-work examples** test stationary conditions and endpoints against an independent scalar solver. They also demonstrate that the financial and emissions-proxy optima can differ. They are not fits to the native curve, reported optimum fractions or physical design recommendations.

## Rounded lifecycle costs can be reconciled

The vent-only totals reproduce the rounded values from `47304 t/year × 20 years × carbon price`. This is a compatible undiscounted diagnostic; no native discount rate or full cash-flow schedule is supplied.

For reliquefaction, inserting only the displayed annual profit, OPEX and capital gives different point results. Those differences are **not proof of a financial error**. A joint feasibility check permits common capital and OPEX values within all displayed rounding intervals.

For example, **analyst witness values** of capital 8.9 million USD, annual nonpower OPEX 1.347 million, and annual profits 2.897/2.807/2.652 million produce exactly the reported −22.1/−20.3/−17.2 million USD under the disclosed 20-year convention. Every witness value rounds to the table's display. These possible hidden values are not identified as the authors' actual inputs, and the calculation does not reproduce their full financial model.

## Original-source check and continuation

The [scoped citation record](../evidence/comprehensive_review_inputs/B3-08_citation_checks.json) checks **Aspelund et al. (2006), B3-35, pp1,3,6**, including the source state, impurities, near-triple concept, energy/cost lineage and dry-ice concerns. Its different composition, 2003 cost basis, economics and full-chain boundary do not validate this BOG process, BOR, thermophysical figures or optimum. Its 142 kWh/t and 1.4% source-chain emissions are not transferred into Paper 1.

Twenty-nine other originals and fourteen dependencies remain unverified. Ozaki/Ohsumi 2011 and Yoo et al. 2011 have different authors/titles but share the printed Energy Procedia pages; exact identities need checking. Native HYSYS assets, possible supplements and rights remain unverified while external retrieval is paused pending the requested Chrome connection. No author outreach was sent.

Run `python paper1/scripts/audit_partial_bog.py` for **41 limited checks, five conditional component splits, three cash-flow rows and four invented scalar cases**. Six tests cover dimensions, mass closure, joint rounding, stationary/boundary conditions and price/emissions distinctions. No B3-08 value enters accepted operating/GHG inputs; current numerical results and the combined 1.5 MPa HOLD remain unchanged. Continue with B3-09.
