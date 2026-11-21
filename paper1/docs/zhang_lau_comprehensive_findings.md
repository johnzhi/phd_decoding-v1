# Zhang and Lau full-text audit — 21 November 2026

All 22 pages of B4-08, *Regional opportunities for CO₂ capture and storage in Southeast Asia*, have been read and visually inspected. The [detailed record](comprehensive_review/B4-08.md) covers 14 figures, 18 tables, 5 numbered equations, nomenclature, the internal Appendix A and 232 bibliography entries. Small equations and rotated appendix tables were magnified. Original PDF SHA-256: `2ce823ec9252e62017b76fe3281b0a05c80ed3a72b89f4caaa3dd7828e26fd4d`.

The paper remains **incomplete under the comprehensive-audit standard**. Reading the bibliography does not verify its underlying originals. Exact claim mapping, empirical derivations, complete field-model reproduction and separate code/data/supplement availability remain open. Appendix A is inside the main PDF, not a separate supplement. No embedded attachments are present; this does not establish absence of publisher assets online.

## What the independent calculation establishes

Equation 5 is a bulk-volume resource calculation: density × basin area × net sand thickness × porosity × storage efficiency. The [independent implementation](../scripts/reproduce_zhang_lau_aquifers.py) uses the eight visually checked Table 18 rows and Table 4 efficiencies of **0.51%, 2% and 5.5%**. It converts km² to m², both percentages to fractions and kg to Mt exactly once. The reported sand thickness is already net; the assumed net-to-gross ratio of 0.3 is not applied again.

All **24 basin/scenario values** agree with Table 12 at integer-Mt display precision. The [calculation table](../outputs/comprehensive_review/B4-08_aquifer_reproduction.csv) preserves unrounded calculations and differences; the [reconciliation](../outputs/comprehensive_review/B4-08_reconciliation.json) separately preserves printed row sums and totals. Published densities are inputs, not independently reproduced EOS outputs. Display-rounding agreement is not a measured uncertainty interval.

No pressure, injection-rate, well-interference or calendar-time constraint appears in this resource equation. The authors' 386,157 Mt total divided by 391.44 Mt/year emissions gives approximately 987 years as an accounting ratio. It does not demonstrate 987 years of feasible injection service.

## Primary-source support for Budiarto's resources

B4-06 reference 55 is this exact retained publication. Eight South Sumatra resource/type/basin matches occur in Tables 8 and 11:

| B4-06 anonymous ID | Candidate field in B4-08 | Type | Reported resource (Mt) |
|---|---|---|---|
| r1 | Musi | Gas | 68 |
| r2 | Jene | Oil | 6.8 |
| r3 | Sopa | Oil | 4.3 |
| r4 | Kuang | Oil | 23.3 |
| r5 | Suban | Gas | 234 |
| r6 | Dayung | Gas | 85 |
| r7 | Sumpal | Gas | 102 |
| r8 | Kaji-Semoga | Oil | 14 |

The sum is **537.4 Mt**, matching the parent benchmark. These field identities remain **candidates**: B4-06 does not explicitly name the fields corresponding to its anonymous IDs. Capacity matching does not authorise a silent join of PVT, well, readiness or annual-injection inputs.

Zhang and Lau assume oil/gas storage efficiency **E = 1** because field-specific data and simulations are limited (p5). Appendix Tables 14–17 provide bulk pressure, temperature, density, recovery, Bg/Bo and selected composition information. These support a regional voidage estimate, with stated assumptions. They do not supply complete compositional PVT, completion geometry, fracture limits, well simulation or the missing annual `kr,t` arrays. The citation edge is recorded as **primary text checked, partial resource/property support**.

## Questions and exclusions

- **Sector labels conflict.** Table 5 assigns Peninsular Malaysia 31.33 Mt/year to iron/steel and 7.11 to refineries; Table 13 assigns the reverse. Both source assignments remain preserved and excluded from harmonised sector inputs pending clarification.
- **MMP units and derivation need verification.** Magnification confirms Equation 4's constant 8864.9, exponent 1/1.012 and factor 1.005 raised to T. T is explicitly Fahrenheit, whereas appendix temperatures are Celsius. The local pressure output unit and validity range are not established. The essential He2015/Li2021 originals remain unchecked; no psi assumption or independently validated miscibility result is adopted.
- **Full field calculations remain unreproduced.** Rounded densities and formation factors, current versus generic recovery selection and the gas-condensate equation's implementation need unrounded inputs and derivation checks. A plausible analyst recovery rule is not substituted for author code.
- **Histogram basis remains unresolved.** Figure 8b prints mean 121.9 Mt and N=57, whereas the reported gas/oil total gives 6,716/57 = 117.82456 Mt. Preserve both and obtain the input version/sample definition. All three Figure 8 panels, including the aquifer panel, are present and inspected.
- **Transport and policy statements are proposals or historical assertions.** External originals remain unchecked; pipeline presence and proposed financing or risk transfer do not establish current capacity or rights.

## Consequence for Paper1

Retain the static resource quantities as attributed regional benchmarks. No resource becomes a Japanese annual injection bound, no anonymous field identity is confirmed, no disputed sector quantity becomes an accepted input, and no capture utility or complete GHG inventory is inferred. Existing operating/GHG outputs are unchanged.

Next: exact retained SimCCS B3-44, then B1-01 and remaining main PDFs. Continue item-level citation support and field-model derivations. External retrieval remains paused under the user's request to wait for a Chrome connection; no new public downloads or author contacts were made.
