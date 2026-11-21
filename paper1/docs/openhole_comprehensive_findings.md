# Openhole-completion audit — 21 November 2026

All seven retained pages of Rashidi et al. (2024), ARMA-IGS-2024-0222 / B1-06, have been read and visually inspected. The [item record](comprehensive_review/B1-06.md) covers ten figures, two unnumbered stress formulas embedded in Figure 2, 15 printed references and four additional dependencies. All figure panels were enlarged. There are no numbered equations or tables. Source SHA-256: `75c8c033c0e0e421579c133857a41bed8b1908ccbbc316d5993732eff1c919a3`.

The paper remains **incomplete under the comprehensive-audit standard**. The underlying originals and complete coupled-model, failure and liner inputs are unverified or unavailable locally. No external supplement search was performed during the requested Chrome wait. The source PDF is preserved unchanged; newly rendered source illustrations are not redistributed.

## Scope of the model and results

The study selects offshore-Sarawak injector I-3 because it is marginally the least stable during drilling. One-way coupled thermal dynamic–geomechanical outputs supply stresses and pore pressures to an openhole-stability analysis. Figure 1 shows profiles for 2025, 2030, 2040 and 2048; detailed failure figures cover only 2025, 2030 and 2048. No detailed 2040 failure result is invented.

The observed patterns in the paper are **model predictions**, rather than field failure observations:

| State | Source gradient equivalent | Reported outcome |
|---|---:|---|
| 2025 end drilling | 11.3 ppg mud | Minor breakouts near two caption points |
| 2025 brine displacement | 12.3 ppg brine | No failures predicted |
| 2025 injection | 13.8 ppg injection gradient | No failures predicted |
| 2025 stoppage | 10.8 ppg pore-pressure gradient | Wide breakouts |
| 2030 injection / stoppage | 12.3 / 11.75 ppg, distinct roles | Hydraulic fractures; minor breakout during stoppage |
| 2048 injection / stoppage | 13.0 / 12.45 ppg, distinct roles | Narrow shear/hydraulic failures; wide breakouts during stoppage |

Exact geometry, material and thermal properties, orientations, stress histories, boundary conditions, solver settings, strengths and failure/damage criteria are unavailable. No author THM or stability case is independently reproduced.

## Mathematical and unit checks

Figure 2 prints simplified minimum and maximum circumferential-stress expressions:

`minimum = 3 SHmin − SHmax − Pw − P0`

`maximum = 3 SHmax − SHmin − Pw − P0`

Their difference is **4(SHmax − SHmin)**. With all other terms fixed, both change by −1 times a well-pressure increment. These literal identities do not include the changing coupled stresses, an inclined-well stress rotation, thermal/poroelastic corrections or a failure criterion. The original Fjaer derivation and meaning/convention of `P0` remain unverified.

The pressure-unit check explicitly assumes conventional pounds per **US gallon** and standard gravity. It gives 0.05194805 psi/ft per ppg, compared with the usual rounded coefficient of 0.052. A ppg gradient equivalent is not necessarily the actual CO₂ fluid density. No actual bottom-hole pressure is calculated from measured depth.

The source distinguishes MD, TVDSS and an SSTVD export axis. Pressure datums and their joins are not fully supplied. Page 5 calls 13.0 ppg a pore-pressure gradient, while Figure 9 calls it an injection gradient. Those roles are not silently equated. Figure 1's −150 to 10°F temperature scale suggests a change variable; no absolute reservoir temperature is recovered from it.

The reported cooling reductions of **78°F and 139°F** convert to **43.3333 K and 77.2222 K**. These are temperature differences, so subtracting 32 would be incorrect.

## Damage intervals and graphical limits

All caption depth intervals are retained as approximate **ft MD spans**. The 2030 stoppage's 15-ft breakout interval lies inside its 150-ft hydraulic-fracture interval: their union is 150 ft, rather than 165 ft. The 2048 stoppage's 150-ft and 330-ft intervals overlap by 50 ft, giving a 430-ft union, rather than 480 ft.

These calculations do not measure damaged rock volume, fracture height, leakage or the fraction of annual service lost. The two 2025 drilling breakout points have no reported width and are not converted to intervals.

The 0/5/10% DoD legend denotes **depth of damage**, with its percentage normalisation unspecified. It is not a probability scale. Some small export-channel abbreviations remain only partly legible or undefined; native numerical outputs and a channel dictionary are still required.

## Liner choice, references and Paper 1

The project selects a perforated liner for mechanical support and control of injection intervals. The paper does not provide a complete liner design, quantitative liner-versus-openhole rate/cost comparison, isolation validation or endurance test. Repeated-cycle weakening and possible caprock consequences are discussed without a supplied fatigue, fracture-propagation or leakage model. Field tests, optimisation and monitoring remain future work.

All 15 printed references have source-use notes. Fjaer 2008 versus 1992, Rutqvist 2009 versus the printed 2010 entry, missing Goodarzi 2012 and the project-model dependency remain unresolved. No underlying original is treated as verified by its bibliography entry.

Paper 1 can cite the case as evidence that cooling and operational transitions affect completion-integrity assessments. This anonymous Sarawak case is not automatically joined to other Malaysian studies. Neither its selected well, failure marks, DoD colours, ppg differences nor liner decision supplies an annual rate penalty, outage probability or permanent-retention fraction.

[audit_openhole_integrity.py](../scripts/audit_openhole_integrity.py) implements the Figure 2 algebra and [54 limited diagnostics](../outputs/comprehensive_review/B1-06_diagnostics.csv). Accepted operating/GHG inputs remain unchanged. Continue with B1-07 and the remaining papers while source, model and asset verification remain open.
