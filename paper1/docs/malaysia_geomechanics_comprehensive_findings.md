# Malaysian coupled geomechanics audit — 21 November 2026

All 14 retained pages of Nik Kamaruddin et al. (2019), IPTC-19491-MS / B1-09, have been read and visually inspected. The [item record](comprehensive_review/B1-09.md) covers 15 figures, six tables, eleven printed correlations, eight bibliography entries and five additional data/model dependencies. The native text extraction omits several raster tables, references and a consequential leakage exclusion; the rendered pages govern those readings. Source SHA-256: `21f6c7d0425288d7a5f1376ef6d0d5230680aa783b3a62962996a0afd9d57da1`.

The paper remains **incomplete under the comprehensive-audit standard**. Cited originals, model/test/field arrays, full constitutive/coupling laws and external assets are unverified. Small graphics were enlarged; some tiny channel labels and exact data mappings still require native exports. The original PDF is unchanged and no source illustrations are newly redistributed.

## Pressure is not annual injection service

The anonymous Field X is a Central Luconia offshore Sarawak carbonate gas reservoir with production from 1995. The 2019 paper proposes injection from 2024 to 2040. Those are scenario dates, not evidence of subsequent operations. It is not assumed identical to the other anonymous Malaysian cases in Paper 1.

The authors recommend a maximum **reservoir pressure of 4,000 psi**, with reported minimum horizontal stress of 4,600–6,200 psi during injection. The stated 600 psi margin matches the lower endpoint; the upper endpoint differs by 2,200 psi. The lower margin is 13.04% of 4,600 psi or 15% of the recommendation, depending on the denominator. These are arithmetic distinctions, not probabilities or universal engineering rules.

The pressure basis (gauge/absolute), spatial/depth datum, conversion between reservoir pressure and flowing BHP, and the Figure 15 total-XX-to-Shmin mapping remain unresolved. A 4,000 psi reservoir recommendation does not supply an annual maximum mass-rate series, imported-CO2 access or permanent storage capacity. The full fracture model and uncertainty are unavailable.

Table 3's SH direction N20°E and Sh azimuth 110° are orthogonal under a common convention. They are not a contradiction. The 0.78 psi/ft Sh gradient, SH/Sh=1.04 and 0.45 psi/ft seawater gradient still leave the vertical stress, depth datum and complete boundary/pressure fields unspecified.

## Correlations and missing constitutive laws

All seven Table 1 rock-property expressions and four Table 2 ISAMGEO expressions were transcribed from the raster tables. Tables 1–2 do not explicitly define the input scale or valid range of Phi, or whether its convention changes between tables.

The diagnostic code evaluates both numeric 0.2 and 20, and 0.3 and 30, as **analyst convention examples**. It does not call them author cases. At Phi=0.2, Table 1 gives density 2.4028 g/cc and Poisson ratio 0.26183; at numeric 20, its density becomes negative. Table 2's reference-rate expression changes sign near the larger example. These results expose the importance of convention/range information; they do not resolve the intended author inputs or justify a silent correction.

The printed plastic volumetric strain reference rate is labelled unitless. Its reference time, stress normalisation, sign/domain restrictions and complete rate integration are absent. The paper describes UPVC/creep calibration, poroelastic horizontal strain and critical-state/contact mechanics without supplying their full yield, flow, hardening, creep, equilibrium or coupling derivations. Replaying eleven empirical correlations does not reproduce those models.

Four calibration MEMs, approximately two million cells and 23 selected stress states are model metadata. They are neither a convergence demonstration nor an annual schedule or uncertainty ensemble.

## Calibration, displacement and validation

The paper reports 9.6 ft subsidence in 2003, 11.3 ft predicted in 2013 and approximately 11.65 ft measured by GPS in 2014. The last two differ by 0.35 ft (0.10668 m), but are from different years. Their difference is not an aligned residual, RMSE or independent validation statistic.

Pore-collapse/creep parameters were iteratively adjusted within laboratory ranges to match GPS. Figure 6 also compares populated properties with the MEMs used to construct them. These are calibration checks. Figure 10's 2002–2012 bathymetry/model comparison is qualitative; survey registration, datum, errors and raw arrays are unavailable.

The forecast includes about 1 ft uplift, final 10.6 ft seabed subsidence and 16 ft reservoir compaction. Platform time series, spatial maxima, reference epochs and deformation definitions differ. Unit conversions preserve the reported magnitudes; they cannot convert displacement into working storage, annual injection or retained CO2.

## Fault and strain conclusions need their original bases

The model uses deformation as a workaround because plastic strain cannot be computed along its frictional elements. The adopted SF-30 analogue supplies normal/shear stiffness 66,311/30,945 psi/ft, cohesion 217.5 psi and friction angle 15°. Stiffness is stress per displacement, not an elastic modulus. The analogue is described as clastic, whereas Field X is carbonate; geographic proximity does not establish material equivalence.

The 0.5 cm (5 mm) maximum predicted slip is mainly generated during depletion. Figures/text identify faults 1, 5, 7 and 10; the conclusion says five affected faults. The fifth identity is unresolved. The comparison with Ekofisk's 43 cm and SF-30's 5.9 cm mixes different fields, fault positions, loading/material models and observed/predicted outcomes. It supplies no failure-probability reduction factor.

Figure 14 shows about 2% highest local equivalent plastic strain at crest cells with porosity above 30%. Table 6 cites other fields' **average or incremental average compaction strains**. Those are different metrics; its Matagorda description includes catastrophic completion failures after 0.25–1.25% incremental average strain. No universal 2% safety criterion is adopted.

Page 11 explicitly excludes a potential cement-bond pathway behind casing and caprock. Small calculated mechanical increments and no reported historical casing problem therefore do not establish no leakage, future integrity or permanent retention.

## Source support and Paper 1

All eight printed sources remain unverified. Specific identity/support issues include SF-30 2014 in body/table versus 2013 in the bibliography; Pereira 2002 versus 2012; and Tjia's printed Malay Basin title versus the claimed Sarawak stress support. Tables 4–5 report SF-30 in Sabah; the bibliography names the company Sarawak Shell Sdn Bhd, which does not establish a conflicting field location. The body also points to “Table 12” where the comparison is Table 5. Printed identities remain preserved rather than silently repaired.

[audit_malaysia_geomechanics.py](../scripts/audit_malaysia_geomechanics.py) produces [77 limited checks](../outputs/comprehensive_review/B1-09_diagnostics.csv): 44 analyst correlation evaluations, unit/orientation/margin distinctions and six explicit missing-input rows. Full dynamic reservoir, finite-element, ISAMGEO, fault, fracture, leakage, cost and GHG models remain unreproduced. Accepted operating/GHG inputs are unchanged. The next local paper is B1-10; external source/asset verification remains paused pending the requested Chrome connection.
