# Restricted aquifer pressure sink: comprehensive reading findings

All 14 retained pages of Razali et al. (2024), OTC34777MS / B1-13, have been read and visually inspected. The [item record](comprehensive_review/B1-13.md) covers 15 figures, eight raster tables, the numbered poroelastic equation, three explicit table relations, eight analyst identities/checks and 15 claim assessments. The native PDF is unchanged, SHA-256 `dd155953567fa75d1c50bb87ce184c0426f080453cbd033183fc98a0d3eb000b`. Source illustrations are not newly redistributed.

The paper remains **incomplete under the comprehensive-audit standard**. Four printed references and 13 additional method/data/background dependencies remain unverified. The [132 limited checks](../outputs/comprehensive_review/B1-13_checks.csv) reconstruct arithmetic and expose conditional basis questions; they do not reproduce the native Petrel, GEM2020.10 or geomechanical cases. [Missing inputs and reconciliation](../outputs/comprehensive_review/B1-13_reconciliation.json) remain explicit. The header says selection followed abstract review and OTC did not review the contents.

## Site, screening and model scope

This is an anonymous Z-field K-reservoir study in Peninsular Malaysia. A flank exploration well, an untested crest, laterally homogeneous average properties per layer and analogue permeability/PVT/SCAL limit its calibration. No core measurements are available for the geomechanical model. The study's proposed2025–2050 injection cases are not observed operation or current contracted storage access.

All four PDA elements are labelled Proven for presence/effectiveness, based on hydrocarbon observations and geological interpretation. These are not direct injected-CO2 integrity tests. Earlier rejection of J/L for trap risk differs from later J/K-best wording and the preliminary matrix's green trap cells; stage/case mapping needs clarification.

Table2's27 qualitative colour cells are preserved. Its lower legend physically places a colour-header row next to Depth, a depth threshold next to Thickness, a thickness threshold next to Porosity, and so on. No row shift is imposed to create a corrected screening rule. The main temperature header uses Fahrenheit while the legend uses Celsius. Green/Low Risk is not a measured failure probability.

Figure3's workflow screenshot carries the label “3D Gelama Field Model.” This is an unresolved template/case provenance clue, not sufficient evidence to identify anonymous Z or join it to another field.

## Volumetric accounting and inputs

Figure1's85×75×50 grid cells reproduce318,750;86×76×51 nodes reproduce333,336. The2D counts also close. These are metadata checks, not active-region volume or mesh-convergence validation. The two interpreted horizons and51 geological grid horizons represent different objects unless native subdivisions establish otherwise.

Table4's printed bulk/net/pore rows sum to1865/1184/23 million m³. All six net-volume rows are compatible with `bulk × NTG` when conditional nearest-display rounding of both inputs and output is allowed. Those rounding intervals are display checks, not measurement uncertainty.

None of the six printed pore volumes is compatible with `net volume × porosity` on the same assumed region/property basis, even under those display intervals. For K-10.2,353 million m³ net ×.16 gives56.48 million m³, while the table prints2 million m³ pore volume. This does not authorise correcting either value: active/Region1 masks, contact cuts, volume definitions and property bases are missing.

Table7's six Bscf capacities sum to157.02, versus the printed157.03 total; the.01 difference is compatible with row rounding. Individually rounded Table4 capacities sum to.15Tscf, while the finer aggregate rounds to.16Tscf. This explains the coarse sum without inventing lost gas or changing a source value.

Bg units and standard conditions are undefined, and numeric Swirr/relative-permeability curves are absent despite the prose describing adjustments. A conditional `pore volume/Bg` example needs an explicit reservoir/standard-volume convention and occupancy basis. Its inferred factors are not measured saturation or efficiency. Bscf is not converted to tonnes. The initial pressure values closely match `.433psi/ft × absolute contact depth`, but the paper describes mid-depth initialisation; pressure intercept, reference, mMD/contact/TVDSS and well-control mapping remain unresolved.

## Mechanical limits and operating controls

Table5 names John Fuller,GR,McNally and Horsrud correlations without supplying their full formulas, units or exact authorities. Static Poisson ratio `.9 × dynamic`, tensile strength `UCS/10`, SHmax/Shmin1.1, plasticity1.0–1.1 and strains.0008/.0005 are preserved as prescribed inputs. The sole numbered equation gives a constrained poroelastic horizontal-stress increment. It does not independently derive the caprock's response, the maximum.33 transfer ratio or a thermal/propagation limit.

The stated safety factor acts on the pressure increment:

`P_recommended = P_initial + (P_critical − P_initial)/1.5`.

This conditional rule matches all six Table6 recommendations within.4psi. Initial pressure is labelled psia, while the other stress/control headers say psi; compatible references are assumed only for this arithmetic replay. The critical caprock values themselves are not independently derived or validated.

Layer recommendations range4692–5292psi. The text sets a uniform injector BHP maximum5000psi, while average-reservoir-pressure plots approach5100psi. Raw comparisons place5000 above three layer recommendations, but well BHP, layer stress limits and reservoir averages can refer to different depths and quantities. Native trajectories, control reference locations, fluid-pressure corrections and violation histories are required before declaring either compliance or violation. No corrected limit is adopted.

Other controls are60MMscf/day gas,30,000 surfacebbl/day water production,800psi minimum producer BHP and a1MMscf/day producer-CO2 cutoff. The two-injector gas target's per-well versus total meaning, exact2050 endpoint and actual cutoff times are not supplied. Plot stages cannot replace native allocation and control histories. Temperature/thermal coupling, flow properties, failure cases and timestep/grid convergence are not documented sufficiently for independent reproduction.

## Reported outcomes and retained carbon

The reported cumulative injections4.9/80.13/95.44Bscf divided by157.03Bscf reproduce the rounded3/51/61% labels. One-producer and two-injector configurations give16.35× and19.48× the no-producer cumulative result; the second injector adds15.31Bscf, or19.11% of the one-injector result. These are comparisons of particular simulated cases, not general injectivity factors or proven global optima.

The no-producer case's4.9Bscf over its reported200days implies24.5MMscf/day average, distinct from the60MMscf/day target. The source's60MMscf/day is an upper control, not a constant achieved schedule. A25-year average or a calendar target product cannot establish annual maximum service.

Figure14 supports the prose's approximately40Mbbl as40million surfacebbl, and supplies the/day basis missing from the prose's21kbbl peak. The exact unit conversion is approximately6.36million surface m³. This is not reservoir voidage, pumping/treatment energy, brine mass or a general disposal inventory. The one-injector water total remains unknown rather than being assigned exact precision from its plot.

“Effective storage” is defined as cumulative injection to the horizon or producer-CO2 cutoff. CO2 produced below that threshold, dissolved in withdrawn brine, recycled, vented or otherwise lost is not reconciled. No post-injection retained-carbon balance or long-term monitoring series is supplied. The case therefore cannot establish permanent retention or net avoided GHG from its injected-volume outputs.

## Implications for Paper1 and remaining work

The authors explicitly recommend **not proceeding with Z-field injection planning** because the effective volume is small and dynamic inputs are highly uncertain (p13). Paper1 can use this as a qualified example of pressure management and its accompanying water requirement. It cannot adopt Z as a proven Malaysian sink, transfer the scenario uplift factors, infer current access, convert Bscf to unsupported tonnage or claim economic/lifecycle superiority.

The [reference register](../evidence/comprehensive_review_inputs/B1-13_bibliography.json) preserves all four printed sources and13 additional dependencies. The list lacks unique inline claim-to-reference attributions; exact original methods/support remain open. Similar M4/toolkit studies are not silently substituted. No embedded files or explicit availability notice establishes neither public supplement absence nor a code/data licence. External retrieval remains paused pending the requested Chrome connection.

Obtain native Region1/property/contact definitions, analogue PVT/SCAL and standard conditions, complete Petrel/GEM and geomechanical cases, pressure-depth/control metadata, produced-CO2/water fates and post-injection outputs. Then reproduce balances, controls, breakthrough, convergence and containment with adequate inputs and rights. Existing accepted numerical inputs and operating/GHG results remain unchanged.

Validation for this checkpoint: the full92-paper inventory/hash check, workbook/document builds, link/diff checks and122 tests passed. Tests cover pressure-increment versus total-pressure safety factors, independent unit/stock-flow checks, conditional volume-rounding incompatibility and preservation of missing standard conditions, unverified references and incomplete model states. Passing these checks does not validate unavailable author cases.
