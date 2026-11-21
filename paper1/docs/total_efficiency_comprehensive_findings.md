# Total-efficiency full-text audit — 21 November 2026

All 13 pages of García-Tenorio Corcuera and Petrakopoulou (2025), B1-03, have been read and visually inspected. The [item record](comprehensive_review/B1-03.md) covers 11 figures, 10 tables, 15 numbered equations and 94 printed bibliography entries, including three duplicate pairs. Small labels in Figures 2–5 were enlarged. Source SHA-256: `212cedb329b173a96c3a1aaeb61bd92b44e54c25049ab61e33a53fe365d244da`.

The paper remains **incomplete under the comprehensive-audit standard**. All underlying originals remain unverified. The exact input conversions, means, filtered observations, plant heat balance and author implementation are unavailable locally. The main PDF says data will be available on request; it does not establish public supplement/code availability. External retrieval remains paused pending the requested Chrome connection.

## Efficiency and energy bases

Equation 15 is dimensionally consistent when power is MW, fuel/captured mass flows are kg/s and lifecycle intensities are MJ/kg. Its expanded and factored forms agree. Earlier notation requires clarification:

- Equation 2's `PR` multiplies both electricity branches, whereas Equation 4 applies `Emix,p` only to the unknown-origin branch. General equivalence requires additional assumptions.
- Equation 8 defines `CO2trans` as a mass. With the other printed definitions, its literal units become MJ/kg², rather than MJ/kg. The station count and distance/station-spacing factor also need reconciliation.
- Equation 9 requires a per-mass electricity basis that is absent from the global `Elecc` definition.
- Equations 12–13 multiply mass flow by specific energy, giving MW, despite printed MJ/kg labels. Their leading dashes are list bullets.
- The reported MJ/MWnet metric lacks a time basis. It is not silently converted to MJ/MWh.

The stated plants have four 900 MW NG units at 57% conventional efficiency and four 600 MW coal units at 37%. Published no-CCS fuel flows multiplied by their LHVs and design efficiencies give **967.83435 MW** and **569.813616 MW**, respectively. Neither the unit/site boundary nor the allocation of internally supplied capture heat is resolved by these values.

Table 6 reports coal total efficiency 21.87% and relative drop 61.51%. Inverting the relative-drop definition implies a **56.81995% reference efficiency**, rather than the declared 37%. Using 37% gives a conditional arithmetic drop of **40.89189%**. This is a denominator diagnostic, not a corrected author-model result. The other coal sensitivity rows show the same approximate reference. The abstract's loss exceeding 50% for both fuels also conflicts with the detailed NG maximum of about 49%.

## Graphics and displayed sensitivity arithmetic

The complete natural-gas stage labels have these sums:

| Figure / case | Sum of printed shares |
|---|---:|
| 2 / CSU-N.a.1 | 97.8% |
| 3 / CSA-N.a.1 | 99.3% |
| 4 / CSU-N.a.1 | 106.6% |
| 4 / CSU-N.a.2 | 101.6% |
| 5 / CSA-N.a.1 | 111.9% |
| 5 / CSA-N.a.2 | 109.8% |

These differences exceed the ±0.2 percentage-point tolerance from rounding four labels to one decimal. The labels are preserved without forcing a partition or inferring replacements from bar heights. Coal processing labels in Figures 2–3 are omitted below 0.6%; those subtotals are not treated as complete partitions. Figure 5's caption says UK despite its CSA labels and Australian context.

All **168 displayed efficiency/drop values** and **112 parenthesised relative deviations** in Tables 5–10 are retained. All 112 deviations are compatible with conditional two-decimal display rounding. These intervals are arithmetic tolerances, not measured uncertainty. Agreement does not reproduce the underlying ±15% energy cases or resolve their efficiency references. Plot error bars represent filtered minima/maxima, with the stated 1.5×IQR exclusion rule, rather than confidence intervals. The doubled-transport-distance results are not independently reproduced from the ±15% tables.

## Captured mass, avoided emissions and annual scope

At 95% capture and a 90% capacity factor, the reported generated-CO2 flows imply **3.3995–3.4117 Mt/year captured** for NG and **7.8401–7.9315 Mt/year captured** for coal. These closely match the reported 3.4/7.9 Mt annual “savings.” Avoided emissions require an equivalent no-CCS production baseline and the additional fuel/utility emissions; captured mass alone does not establish that benefit.

The script retains a separate, explicitly conditional baseline-minus-vented calculation. It is **not a validated avoidance estimate**, because power, composition and auxiliary boundaries remain unresolved. In particular, Table 4 uses a coal generation yield of 3.39 kgCO2/kgfuel, while the body fuel/CO2 flows imply approximately 3.666. Neither is replaced by a guessed composition.

An earlier catalogue note incorrectly read page 9's “90% Cf” as capture fraction. It means **capacity factor**. The actual source discrepancy is page 9's near-100% capture context versus page 10's 95% capture context for the same 3.6/8.43 Mt/year claims. Their per-MW ratios use 900/600 MW single-unit ratings; the four-unit plant scope also needs clarification. Native quantities remain preserved.

## Inventory, citations and use in Paper 1

Table 3 compiles heterogeneous capture heat, compression, pipeline and injection examples. The five phase-power rows at 1.5 kg/s convert to 0.273067, 0.245467, 0.241267, 0.103133 and 0.055733 MJ electricity/kgCO2. The separate 31.7 kg/s, 30–35 MW case gives 0.94637–1.10410 MJ/kg. These conversions do not combine unlike cases into one inventory or verify their original models.

The 84 bar / 100 km spacing discussion is attached to **natural-gas fuel transport**, using a paper whose title concerns methane/hydrogen mixtures. Its exact conditions remain unverified. It supplies no general CO2 pipeline safety limit or reservoir pressure-constrained service curve.

The hypothetical UK/Australia proxies are disclosed. This paper does not supply one complete matched capture-to-ship heat/electric inventory or an annual pressure-constrained reservoir dataset. Paper 1 retains qualitative evidence about energy-boundary dependence and holds the disputed penalties, shares and annual avoidance claims out of accepted inputs.

[audit_total_efficiency.py](../scripts/audit_total_efficiency.py) generates [210 diagnostics](../outputs/comprehensive_review/B1-03_diagnostics.csv) and [112 sensitivity checks](../outputs/comprehensive_review/B1-03_sensitivity.csv) from source-hashed transcriptions. These checks and the Equation 15 component do not reproduce the full author cases. Continue B1-04 and the remaining local papers while original-source, supplementary-data and model-verification work stays open.
