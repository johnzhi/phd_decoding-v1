# Offshore-Japan deepwater-sediment audit — 21 November 2026

All 15 retained pages of Pilisi, Ghorbani and Vasantharajan (2012), CMTC151756 / B1-04, have been read and visually inspected. The [item record](comprehensive_review/B1-04.md) covers eight figures, three tables, one numbered equation, 28 printed bibliography entries and eight additional named dependencies. Figure 8's eight time labels and colour scale were enlarged. Source SHA-256: `e2002edadeea9291d60d0019b25accda0b2d36fd4f15a925235108bba43594e0`.

The paper remains **incomplete under the comprehensive-audit standard**. Its header identifies conference selection through abstract review and says the full contents were not reviewed. All underlying originals remain unverified. No external supplement/code search was performed during the requested Chrome wait. The retained original is unchanged; newly rendered source illustrations are not distributed in this checkpoint.

## Prescribed rate and missing pressure constraints

The three GEM/GHG cases prescribe 5,000 **reported tons/day** for 25 years, followed by 225 years without injection. With a declared 365-day calculation convention, that is 1.825 million reported tons/year and 45.625 million reported tons per case. The source does not define metric versus short tons, so this arithmetic does not convert them to tonnes.

These are input schedules. No allowable bottom-hole pressure, fracture criterion, pressure-controlled target sweep or validated well hydraulics establishes that this rate is deliverable. The 7-inch casing conveyance estimate of 3,000 tons/day is also an estimate, rather than an injectivity measurement. High initial pressure, porosity and an imposed rate do not independently demonstrate that low-permeability sediments accept that rate within safe pressure limits.

The reported 25×25×60 grid has 37,500 cells. Exact lateral dimensions, layer geometry, completed cells, realised property fields, pressure/flow boundaries, relative permeability, capillarity, brine composition/PVT, thermal coupling, seeds and convergence outputs are unavailable. The additional 3,000-ft-deep case needs its own domain: the principal cases describe only 328 ft of sediment. A complete GEM reproduction cannot be constructed by filling these gaps with defaults.

## Temperature, pressure and equation checks

The printed heat-flux magnitude relation, `Q = c × dT/dz`, closes dimensionally. A signed Fourier flux would additionally require the vertical-coordinate convention. The published 6 and 2 °F/100 ft gradients convert to **109.3613** and **36.4538 K/km**. Temperature differences use the factor 5/9, without subtracting 32.

Combining the stated heat-flow endpoints of 20–200 mW/m² and conductivity endpoints of 1.5–6 W/m/K conditionally gives 3.333–133.333 K/km. A tenfold heat-flow difference implies a tenfold gradient difference only when conductivity is held fixed.

The paper's own approximate supercritical condition on page 4 requires temperature above 88°F, while page 13 describes a transition at temperatures of at least 80°F. **80°F = 26.6667°C**, below **88°F = 31.1111°C**. This is an internal threshold check; it is not a new EOS or density calculation. Phase labels alone do not establish density relative to the actual pore fluid.

Continuing the main site's constant 6°F/100 ft gradient from a 35°F seafloor to 3,000 ft gives 215°F, whereas the additional case reports 200°F. The gradient may vary; the actual temperature array is needed. Both values are preserved. Pressure unit conversions retain an unspecified gauge/absolute datum and do not create fracture-pressure headroom.

## Plume figures and retention claims

Figures 7–8 show **global CO₂ mole fraction**, with colour levels from 0.00001 to 1. The positive lower limit does not establish exactly zero CO₂ in blue regions. Global composition is also different from phase saturation, mobile mass and a retained-carbon fraction.

Figure 8 has snapshots at injection start and years 10, 25, 50, 100, 150, 200 and 250; injection ends at year 25. Neither those finite snapshots nor approximate counts of high-composition cells establish infinite permanence, zero boundary leakage or a quantitative safety advantage. Raw mass balances, boundary fluxes, phase/flow histories and stability checks remain unavailable.

The authors call for further geomechanical/earthquake, displaced-fluid chemistry and hydrate studies. Those qualifications remain attached to their stronger claims of safer and permanent storage.

## Vessels, risers and citations

All 39 weather/material cells in Tables 1–2 are recorded. Suitability changes with depth: composite injection risers pass the shallower table but fail the approximately 18,000-ft table. The latter retains titanium drilling/injection risers for moderate and rough conditions. Check marks do not supply structural loads, stress/fatigue criteria, metocean return-period parameters or year-round operational availability.

The 500,000-ft³ carrier scale converts to 14,158.423296 m³. No density, fill, fleet, cycle, fuel, offloading or maintenance balance substantiates the separate 100/10-million-ton annual logistics claims. Multiple wells or ships may be intended; these are not treated as contradictory single-well estimates or validated services.

All 28 printed references have source-use notes. Eight further dependencies require identity resolution, including the IEA/IPCC-versus-EIA attribution, NASA imagery, Srinivasan 2008, Pilisi 2010, NOAA, Pickard 1990, Langseth/Tamaki 1992 and GEM/GHG. A related title or different year is not substituted for an original source.

## Consequence for Paper 1

This is a historical, hypothetical Japanese feasibility concept. It supplies neither a demonstrated pressure-constrained annual storage service nor a matched capture-to-injection heat/electric/fuel inventory. Its prescribed rate, plume colours and riser check marks remain outside accepted service, retention and GHG inputs.

[audit_deepwater_japan.py](../scripts/audit_deepwater_japan.py) produces [55 limited diagnostics](../outputs/comprehensive_review/B1-04_diagnostics.csv). It does not reproduce GEM/GHG, geostatistical, well, structural, density or safety models. Continue with B1-06 and the remaining local papers; B1-05 already has a reading record. The 92-paper goal remains active.
