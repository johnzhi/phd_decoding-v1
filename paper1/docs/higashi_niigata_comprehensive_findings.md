# Higashi-Niigata full-text audit — 21 November 2026

All 11 retained pages of Kukuu et al. (2025), SPE225812MS / B1-07, have been read and visually inspected. The [item record](comprehensive_review/B1-07.md) covers 13 figures, three tables, nine printed references and five additional dependencies. The source's numbering gaps are preserved: figures1,4–7,9–12,16–19 and tables2,3,8. No numbered or unnumbered equations are supplied. Source SHA-256: `98bcd58dcbe755c55963d9687e5c7527701ff0301139c6789a92c6c2ccccb275`.

The paper remains **incomplete under the comprehensive-audit standard**. Native geological/history/forecast arrays and commercial model cases are not retained, underlying originals remain unverified, and external asset retrieval remains paused pending the requested Chrome connection. The header reports conference selection through abstract review and says SPE did not review the contents. The original PDF is unchanged; newly rendered source illustrations are not redistributed.

## What is specified

The study generates100 geological realisations using Vsh, porosity/permeability relationships and Flow Zone Indicator methods, then selects10 after history matching. Its model has120×111×103 cells, of which276,410 are active, within a9×11km×1,800m bounding box.

The topology product is **1,371,960 cells**; the active count is about20.147% of that total. This is a count ratio, not a volume fraction, net-to-gross, porosity or storage efficiency. The gross bounding box is178.2km³, with no disclosed basis for converting it into pore volume or CO₂ capacity. Selecting10% of the generated models is likewise not a confidence level or calibrated probability.

Table8 specifies:

| Quantity | CaseA | CaseB |
|---|---|---|
| Injectors | 3 | 3 |
| Pressure-relief wells | 0 | 3 |
| Injection interval | 1Jan2029–1Jan2050 | Same |
| Model interval | 1Jan2029–1Jan2130 | Same |
| Injection-pressure limit | Initial reservoir pressure | Same |

The listed wells do not count every legacy field asset. The initial-pressure limit lacks a numerical value, reference date/datum and precise well-versus-field control definition. It cannot be treated as a demonstrated thermal fracture or fault-stability limit.

The intervals are21 injection years plus80 post-injection years: **7,670 +29,219 =36,889 calendar days**. These are model dates, not observed availability. Native operations between the April2022 history cutoff and January2029 injection start are not supplied by the date labels.

## What the figures do not supply

Historical and forecast plots have labelled units but no numerical vertical scales. Figures11/17 use **CO2_ton**, whereas their captions call the quantity injection volume. The ton convention and absolute scale remain unresolved; neither an absolute mass nor a volume-to-mass conversion is recovered.

Figure19 labels average reservoir pressure inMPa, without a visible numerical scale or datum. Its solid CaseA and dotted CaseB curves do not supply local BHP, pressure headroom or an exact pressure-limit delay. The averaging basis and relation to the ten realisations are not disclosed.

The cumulative/pressure plots run only to about2060, while Table8's simulation horizon ends in2130. Distribution maps label the final snapshot “Simulation End” without a raw timestamp. Their **High/Low** colours have no numerical scale or defined saturation/concentration variable. Tiny map aliases and scale-bar labels also require native exports. No plotted colour is converted into plume mass, retained fraction, zero breakthrough or an exact migration distance.

CaseA reportedly reaches its constraint around2040, making the target injection rate difficult to maintain. Its cumulative curves continue rising afterward. This is **not** evidence that injection stops in2040.

Figure9 contains six circle markers, while Table8 specifies three injectors. Figures10/16 identify the selected three injectors and three relief locations. Exact well aliases/coordinates and active controls remain necessary; six operating injectors are not inferred from the background symbols.

## Uplift, history matching and integrity

The reported25–30% cumulative uplift with pressure relief gives only a normalised **B/A index of1.25–1.30**. It does not establish an annual multiplier, absolute capacity or annual maximum-rate profile. No paired numerical member outputs are available to independently reproduce the percentage.

Water breakthrough is acknowledged to be difficult to match. The paper supplies visual history comparisons but no raw observations, objective, weights, tolerances, observation uncertainty or hold-out validation. Its claims of a highly accurate plan remain attributed rather than independently demonstrated.

Historical hydrocarbon containment, a50–120m mudstone seal and inferred low fault transmissibility support screening. They do not supply quantitative CO₂ entry-pressure, thermal/fracture/fault, legacy-well leakage or permanent-retention bounds. Full PVT, rock-flow, hysteresis, thermal, geometric and control inputs are absent.

Three added relief wells also require water pumping, handling/treatment, gas-content and asset inventories. Those quantities are unavailable. Additional injection cannot be equated with additional net lifecycle mitigation or cost savings.

## Source dependencies and Paper1

All nine printed references are individually mapped. Figure1 explicitly cites JOGMEC's program map; its own disclaimer says the areas are illustrative, not exact locations. The other cited pressure-management, water-extraction and project-example originals remain unverified. Retained B3-16 is a different paper from the Liu et al.2015 reference and is not substituted for it.

Five further dependencies cover official policy/legal texts, field observations, commercial model cases and FZI derivations. No embedded supplement or explicit code/data-availability notice was found in the retained PDF; that does not establish online absence.

Paper1 retains this named Japanese case as evidence of history-matched planning and pressure-management sensitivity. It is not a publicly complete numerical pressure-constrained dataset. [audit_higashi_niigata.py](../scripts/audit_higashi_niigata.py) produces [19 limited checks](../outputs/comprehensive_review/B1-07_diagnostics.csv), including explicit missing entries for absolute mass, pressure, annual injection and relief-water inventory. Accepted operating/GHG inputs remain unchanged. Continue with B1-08 while model, original-source and asset verification stay open.
