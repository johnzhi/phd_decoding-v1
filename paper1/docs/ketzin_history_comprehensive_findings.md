# Ketzin history matching: comprehensive reading findings

All ten retained pages of Class et al. (2015), B1-15, have been read and visually inspected, including enlarged equations, figures, tables, captions and legends. The [item record](comprehensive_review/B1-15.md) covers six figures, four tables, thirteen section groups, fourteen claim assessments, two phase functions in numbered Eq1, the inline Kozeny-Carman relation and nine analyst identities. Source SHA-256: `4c8ec9850a78e897d5d4f271cd04449b7cfeb448a69fd1339416e4c8d2221324`. The original PDF and its rights are preserved; scratch renders are not newly redistributed.

The paper remains **incomplete under the comprehensive-audit standard**. All27 printed underlying originals, eight additional model/data dependencies and external assets remain unverified. The [102 limited checks](../outputs/comprehensive_review/B1-15_checks.csv), [324 constitutive evaluation rows](../outputs/comprehensive_review/B1-15_printed_phase_curves.csv) and [reconciliation](../outputs/comprehensive_review/B1-15_reconciliation.json) do not reproduce the native reservoir or inverse models.

## Literal inputs and equations

Table1 prints a hydrostatic pressure gradient of **1.14 Pa/m** alongside62 bar at639.5 m. The native/rendered table confirms the literal value. Under the analyst identity dp/dz=rho*g it implies about0.116 kg/m3, and a20 m interval gives only0.000228 bar. These are dimensional diagnostics, not a replacement fluid property or accepted hydrostatic correction. The gradient remains on HOLD pending native inputs or an erratum. Gauge/absolute pressure basis is not specified. The entry pressure10952.87 Pa converts to0.1095287 bar; it is a capillary parameter, not a fracture or BHP ceiling.

The text introduces Brooks-Corey capillary pressure, but numbered Eq1 actually prints two **relative-permeability** functions:

`krw = krw,eq * ((Sw−Swr)/(1−Swr))^nw`

`krn = krn,eq * ((1−Sw−Snr)/(1−Snr−Swr))^nCO2`

The denominators differ. We preserve them exactly, with residuals Swr=.15/Snr=.05 and endpoints1/.85. Evaluation of both functions stays on the shared physical real domain .15≤Sw≤.95. Fractional powers would otherwise encounter negative bases; no undocumented clipping, hysteresis or phase-appearance rule is imposed. At Sw=.95 the literal wet law gives0.71646 for nw=5.5, rather than1; Case3's nw=9.46 gives0.56354. This establishes the printed expression's behavior, not an error in unpublished source code. The explicit pc(Sw), unpublished CO2SINK measurements and actual simulator endpoint handling remain missing.

The inline Kozeny-Carman multiplier in Section4.2 is independently evaluated:

`MK = Mphi^3 * (1−phi0)^2 / (1−Mphi*phi0)^2`, with `phi0=.2`.

Case3 Mphi=.5555 gives MK=.1388437553, agreeing with printed.1388 at four decimal places. Analyst differentiation gives `dlnMK/dlnMphi = 3 + 2*Mphi*phi0/(1−Mphi*phi0)`, about3.24997 at that value. The reference porosity becomes.1111 only at the chosen reference basis; it is not every cell's porosity. This reproduces a constitutive component, not the heterogeneous field, fitted parameter estimation or native forward model. Case3 MK is dependent, so it is not a fourth independent fitted parameter.

Salinity.2 kg salt/kg brine corresponds to.25 kg salt/kg water; the denominator matters. Pore compressibility7.2e−10/Pa, temperature gradient.03°C/m and Table1 Kv/Kh1/3 retain their distinct units and meanings. The74 m formation description and24+12+36=72 m geological zones require native mapping; we do not extend the mesh or alter thicknesses to make them equal.

## Calibration, prediction and observations

ApproachI manually adjusts six directional near/far permeability multipliers. Switching from Peneloux to Span-Wagner is accompanied by retuning the near multipliers from.34/.07/.07 to.25/.05/.05, while far modifiers stay.38/.10/.10. The reported up-to5% density difference does not establish a general proportional permeability uncertainty. Absolute anisotropy also needs the baseline tensor and coordinate orientation; a modifier ratio alone is insufficient. Native PVT states, viscosity/solubility implementations and case files remain missing.

Table3's gas-arrival percentage arithmetic is compatible with rounded source times. Small deviations from its printed percentages remain visible in the diagnostics. Dissolved-arrival observations are dashes and stay null. The21.7/271-day gas observations also occur in B1-14; reused measurements do not constitute independent validation across papers. Gas-membrane sensors150 m below ground detect gas after annulus accumulation, filter crossing and upward travel. Geological first contact can therefore precede reported detection by several days.

ApproachII fits eleven pressure points during days17–50 and a binary arrival step. The printed pressure sigma10000 Pa is0.1 bar. The binary-step sigmas.02/.05 are not documented as days; if residual scaling is unchanged and weights follow inverse variance, their relative weight becomes.16. That calculation is conditional, not verification of native iTOUGH2 covariance or objective normalization. Case2's porosity multiplier reaches its.6 lower bound. Case3 sensitivities218.4/34.3/10.8 are parameterisation/weight dependent, not variance shares or posterior probabilities. The phase exponent n is distinct from B1-14's Archie electrical exponent.

Figure2 shows that similar early fits diverge later. The source reports Case2 agreement for about380 days; Figures3 and5 show that later near/far modifications improve different windows and that ApproachII eventually overpredicts pressure. ApproachI reports stronger held-forward pressure agreement, including shut-ins, but raw rate/tank corrections, pressure histories, native parameters and independent convergence checks are unavailable. Its isothermal simulation does not independently reproduce the cold-injection thermal process.

Printed calendar labels also require clarification:

| Source labels | Explicit calendar diagnostic |
| --- | --- |
| 24 June2008 to31 December2011,1286 days |1285 elapsed days or1286 inclusive dates |
| 26 May2014, day2193 |2162 elapsed days from printed start; difference31 days |
|908 days beyond printed calibration endpoint |877 elapsed days between printed dates; difference31 days |
|1286 calibration plus908 forecast days |2194, versus printed final-day label2193 |

Day2193 under a zero-based start falls on26 June2014. This is a diagnostic, not a correction to the source. The day1424–1660 shut-in spans236 elapsed days, while text calls it about seven months and Figure5 labels six. We retain all descriptions and do not derive annual availability. The second day1764–1793 interval spans29 elapsed days; exact operating endpoints remain necessary.

## Geological feature and plume claims

The chosen nearfield is1000×900 m. Reading “enlarged by100 m in every direction” as shifting both bounds gives1200×1100 m, an area ratio about1.467. That is an explicit geometry interpretation pending the native mask. It does not define storage volume.

The150×20 m gas-retarding feature has5/6 m depth in different cases. Its geometric volumes15000/18000 m3 are not pore volume or stored mass. Reported Ktzi202 arrival changes from208.52 days to254.28/264.47 days. Nearfield and feature thickness change together, so the last improvement cannot be attributed solely to one extra metre. The authors call insertion somewhat arbitrary. At Figure4's day255, Case2's216.6-day arrival has occurred and Case2b-b2's264.47-day arrival has not, consistent with the illustrated comparison. Neither panel independently proves that feature exists geologically.

This feature lies between Ktzi201–202. B1-14's later discussion of a hydraulic200–201 barrier addresses a different well pair and mechanism; it cannot automatically refute this chosen gas-retarding feature.

Figure6 displays visibly different plumes despite calibrated pressure responses. It provides no full numeric axes, mapped property arrays, independent plume-volume validation or retained-carbon balance. The conclusions explicitly leave uncertainty quantification for future work. A fit, illustrative case comparison or sensitivity coefficient is not a posterior distribution, permanent-retention guarantee or maximum annual service.

## Sources, assets and Paper1 use

All27 bibliography entries are preserved in the [source register](../evidence/comprehensive_review_inputs/B1-15_bibliography.json), including literal identity anomalies and [26]'s printed operational-dataset identifier. Their source-support checks remain open. The exact geological arrays, mesh mappings, raw monitoring/tank corrections, unpublished SCAL/capillary data, PVT/EOS setup, inverse case files, native masks, software versions/rights and external supplement/code/erratum status remain unverified. No embedded files or explicit supplement notice was identified locally; no claim of public absence follows.

The B1-14→Class2015 citation retains its previous scoped support for calibration and sensor-delay cautions. This full retained-PDF reading does not independently validate B1-14 or complete Class's underlying literature chain. External retrieval remains paused pending the user's requested Chrome connection; available cloud browser controls do not establish a connected personal Chrome session.

Paper1 now uses this paper to separate calibration from independent prediction and phase-arrival evidence from identified geology. No annual injection bound, availability, barrier probability, retained fraction, utility/GHG factor or commercial allocation is transferred. Existing accepted operating and GHG numerical outputs remain unchanged.

The continuation queue moves to B1-16 while native models and underlying originals remain open. Validation includes source hashes, the92-paper register, domain and constitutive checks, explicit-calendar/missing-value checks, document/workbook builds and the repository test suite; these checks do not validate the unavailable field models.
