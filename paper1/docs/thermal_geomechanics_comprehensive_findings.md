# Thermal geomechanics audit — 21 November 2026

All nine retained pages of Tan, Musa and Nik Kamaruddin (2024), ARMA-IGS-2024-0183 / B1-11, have been read and visually inspected. The [item record](comprehensive_review/B1-11.md) covers eight figures, six table objects, five numbered equations and five analyst identities/derivations. Table 3 is printed twice: cooled pressures on physical p6 and deformation on p8. The unnumbered compliance table is on p7. Source SHA-256: `1d1bd104cf39b9759920488454ef079e6712ba1a8b9a625957130baf7c5e262b`.

The paper remains **incomplete under the comprehensive-audit standard**. Nineteen cited originals and six additional method/data dependencies are unverified. Native logs, material/thermal tests, full field cases, geometric integrals, fault sensitivities and external assets remain unavailable locally. No complete physical model is independently reproduced. The original PDF is unchanged; source illustrations are not newly redistributed.

## Actual data versus the proposed workflow

The source is a preliminary showstopper assessment for an anonymous offshore Peninsular Malaysia Field X. It is not assumed identical to the Sarawak cases. The header states technical/critical paper review by at least two reviewers. Its2024 conclusion describes progression to a full coupled/thermal development-plan study; it does not establish actual2026 injection or access.

Table 1's152 check/cross cells and eight drilling years are transcribed in the [input record](../evidence/comprehensive_review_inputs/B1-11.json). All eight wells have compressional sonic but no measured shear sonic, borehole images or pre-existing1-DMEM checkmarks. Pressure-data checks occur only forA–D. Properties are log-derived: **no measured site rock mechanical properties were available**. ECD is assumed0.5ppg above static mud weight. Grouped MW/ECD or FIT/LOT/mini-frac availability does not establish an individual measured ECD or test type; noXLOT is available.

Daily drilling reports are crossed for all eight wells, while the narrative describes report review and extracted mud weights. End-of-well reports and summaries may provide information, but raw provenance is needed to resolve that distinction. Caliper/LOT/FIT matches are calibration checks, not independent core-test or holdout validation. The synthetic failure image in Figure 3 is not an observed borehole image.

## Pressure and thermal checks

The reported pressure pairs remain unchanged:

| Seal | Isothermal recommendation (psi) | Cooled recommendation (psi) | Printed-pair decrease (psi) |
|---|---:|---:|---:|
| A | 2153 | 1632 | 521 |
| B | 2731 | 2209 | 522 |
| C | 3264 | 2739 | 525 |
| D | 3701 | 3178 | 523 |

Initial/recommended headers saypsi, current reservoir pressure sayspsia and stresses saypsi. No common absolute/gauge datum is inferred. The estimated50°C cooling, stress-transfer upper ratio0.33 and safety factor1.5 are conditional scenario/method inputs, not field measurements or probabilities.

Assuming compatible references, the analyst rule

\[
P_{safe}=P_{current}+(S_{h,after}-P_{current})/1.5
\]

matches the isothermal recommendations within0.34 psi. An independently reconstructed linear caprock stress path also approximately reproduces the isothermal critical-stress column. This is a **conditional table-component check**, not validation of the source's transfer model, material parameters or pressure reference.

The same direct margin rule applied to cooled Seal A's printed2110psi stress and450psia current pressure gives1556.67, whereas the table recommends1632psi: a75.33 psi residual. Both source values remain preserved. B/D closely match the rule; C differs by about1psi. Unknown thermal/pressure inputs or a table/implementation issue may explain the discrepancy; no correction is selected.

Eq1 is explicitly for instantaneous pore-pressure changes, not geological stress reconstruction. Its alpha is not defined in the where-list; a Biot interpretation is provisional. Under the stated analyst convention `effective stress = total stress − alpha × pore pressure`, fixed-pore-pressure cooling that lowers total stress also lowers effective stress. The source's increase wording needs its coupled-pressure/sign conditions. Generic750m thermal extent and plume-density discussion are not adopted as field-calibrated transport laws.

## Compliance and degradation are case-specific

The printed Eq3 factorises as

\[
C_m=\frac{(1+\nu)(1-2\nu)}{(1-\nu)E_{sta}}.
\]

If static modulus isMPa, compliance is inverseMPa. Lower E increases compliance; increasing nu decreases it over the ordinary positive-nu elastic range. Their combined effect depends on the starting nu. With analyst-only relative changes E×0.74 and nu×1.1, the compliance ratio is about1.283 at nu0.25 but0.894 at nu0.40. These are examples, not native field inputs. A degraded nu reaching0.5 violates the assumed stable isotropic elastic domain.

The up-to26% E/strength decrease and10% nu increase come from a regional database, not this site's mechanical tests. Pressure/thickness/geometry and joint-property changes remain unprovided. The printed deformation comparisons are not uniform: GeertsmaP90 uplift0.19→0.12 m decreases36.84%, while P10 uplift0.014→0.020m increases42.86%. P50/P10 expansion also increases in some cases. Neither the37% decrease nor another single percentage is a general degradation or annual-rate factor.

The compliance table's LowP90/BaseP50/HighP10 order has increasing Cm, but the deformation table has largest outcomes inP90. Joint pressure, thickness, geometry, weighting and case construction are needed before interpreting this mapping. Labels are preserved; columns are not reordered or converted into calibrated probabilities.

## Uplift notation and facility claims

Eq2 uses DeltaH for layer thickness. Eq5 defines DeltaH as maximum compaction/expansion, while H is reservoir thickness. Under those literal definitions, DeltaH appears both in the geometric kernel and as DeltaH/H; its small-displacement response is quadratic. For positive expansion with nonnegative overburden,

\[
0\le S\le2(1-\nu)\Delta H^2/H.
\]

That bound and unit examples expose a notation/implementation question; they do not verify Bruno1990 or justify replacing DeltaH byH. The original derivation, full geometry and native code are missing. Geertsma's integralA is also missing. Signed Eq4/Eq5 output and positive table magnitudes require a common direction/datum convention.

The narrative adopts a maximum uplift of0.18 m; Table 3's cross-method maximum is0.19 m. The degraded maximum is0.12 m. The difference needs native case/precision reconciliation. Maximum vertical height alone does not validate facility integrity: differential movement, rate, loads, foundation/well tolerances and independent validation are not supplied.

## Fault and caprock scope

Of26 interpreted faults, the body focuses on major nearby faults; Figure6 names six surfaces and Figure 7 details Fault1. Zero fault cohesion and adjacent-rock friction reduced10/20% are assumptions, not fault tests. Reducing an angle is different from reducing its tangent by the same percentage. Dip/azimuth percentile values and joint distributions are missing.

Some points cross the0.8-angle failure line. The authors distinguish local failure from reactivation, but do not provide a quantitative propagation/permeability criterion. Those plots do not establish zero fault/leakage risk. Figure 5 also has unresolved case labels: the caption says injection to initial reservoir pressure, while the panel says maximum recommended pressure. Native full-seal/fault states are required.

[audit_thermal_geomechanics.py](../scripts/audit_thermal_geomechanics.py) retains [90 limited checks](../outputs/comprehensive_review/B1-11_diagnostics.csv), including eight explicit missing-input categories. Paper1 retains the pressure pairs for reported-value arithmetic with the new qualifications; no numerical input value or operating/GHG result is changed. Native thermal, fault, deformation and retention models remain unreproduced. B1-12 is next; external verification remains paused pending the requested Chrome connection.
