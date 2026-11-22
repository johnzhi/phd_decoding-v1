# B2-15 global pressure-limited storage audit

Smith, Hampson and Krevor estimate global pressure-limited storage in *International Journal of Greenhouse Gas Control* 137 (2024), 104220, DOI [10.1016/j.ijggc.2024.104220](https://doi.org/10.1016/j.ijggc.2024.104220). The [retained PDF](../papers/B2-15.pdf) is CC BY. SHA-256: `0e765af5db3780a2a31a7628c284ac8e52c42c4754d3ca7655368bcf7484e4fa`.

All **13 main-PDF pages** were read as text and visually inspected, with seven magnifications. The [item record](comprehensive_review/B2-15.md) covers all nine figures, two tables, six unnumbered Figure 1 relations, 61 claim records and sixteen open issues. All **68 printed bibliography entries** were read and preserved with native line geometry, including the IPCC 2018 continuation between pages 12 and 13. No new original-passage verification is claimed.

**Overall status remains incomplete.** The native global model, supporting assets and all cited-original chains remain unverified. This audit adds component checks, rather than a reproduced CO2BLOCK simulation or a calibrated field operating envelope.

## A public method with restricted underlying data

The paper describes CO2BLOCK as publicly available and open source. Its principal geological inputs include commercial Wood Mackenzie and C&C Reservoirs data, with some USGS inputs. Page 12 explicitly states:

> The authors do not have permission to share data.

The same page references a supporting list of basins and article-DOI supplementary material. The main text also refers to regional maps and results. None was retrieved or verified locally, and no direct repository URL is supplied in the retained paper. No repository address is guessed.

This establishes pressure-aware modelling precedent, but does **not** close the requirement for a reproducible public reservoir dataset. The exact commercial/USGS input subsets, lawful derived basin means, defaults, software version and scenario arrays are missing. The public status of an analytical tool does not make its global input dataset public.

External retrieval remains paused under the user's instruction to wait for the Chrome connection. No author was contacted. Local absence is not evidence that a supplementary asset is nonexistent online.

## What the model assumes

The study represents each basin as homogeneous, averages reservoir properties arithmetically, uses closed boundaries for every basin, and ignores stratigraphic and fault compartments. Injection points lie on Cartesian grids and operate at equal, constant rates over either thirty or eighty years.

Each point is a **storage site that may contain several wells**. The imposed ceiling is **5 Mt/y per site**. It must not be transferred as a per-well rate or a field measurement.

Four site counts—4, 25, 100 and 400—cross three spacings—5, 15 and 30 km—to make twelve scenarios. Scenario M selects each basin's greatest resource among these feasible patterns, separately for each horizon. It is a finite candidate maximum, not an unconstrained physical or cost optimum.

The [twelve design rows](../outputs/comprehensive_review/B2-15_source_designs.csv) retain the source patterns, nominal cell footprint and technical ceilings. Native pressure-limited rates are deliberately blank. For example, 400 sites at 30 km imply a nominal footprint of 360,000 km² under the printed area constraint; the node hull has a different margin convention. Neither calculation demonstrates actual well placement, permitting or safety.

The paper explicitly excludes project rollout time, detailed compartments and active pressure management. It does not estimate the extents of structural, stratigraphic, residual, dissolution or mineral trapping. Pressure feasibility therefore does not establish permanent retention.

## Input and population limits

The source scheme contains 764 basins. The paper repeatedly describes 248 modelled basins but also says 265 have sufficient data when explaining why Scenario 12 fits only twenty. The native population/filter mapping remains unresolved. The reported 992 sites in four-site scenarios give 992/4 = 248; this does not establish why seventeen other basins are omitted.

The European example starts with 72 basins, 8,739 records for 6,673 fields, and 7,046 depth-filtered entries, ending with 36 usable basins. Repeated measurements and variable-specific missingness require the actual property and weighting arrays before replication.

The depth filter is greater than 800 m. Depth alone does not establish supercritical temperature and pressure; actual P/T inputs and EOS/default settings are needed to verify states. The authors also acknowledge that petroleum-field sampling can produce optimistic porosity and permeability relative to sparsely sampled saline aquifers.

Whole basins are assigned to the country containing most basin area. This changes national comparisons—for example, Cormorant resource is assigned to Norway—and must not be interpreted as territorial ownership or contracted storage service.

The exploration filter is described both as excluding fewer than 100 wells and as requiring more than 100. Eligibility at exactly 100 wells needs clarification. The readiness scenario uses historical 2015/2018 index sources, not a verified current country ranking.

## Printed equations and independent checks

Figure 1 prints tensile and shear headroom expressions, a Lambert-W inversion and three geometric/technical inequalities. They were magnified and retained literally. Table 1 provides symbol descriptions but no numerical defaults or unit column.

The tensile relation is `ΔpMt = σ3 − p0 + S0`. The shear relation uses `(k0 − θ)/(1 − θ) × (σ1 − p0) + C cosφ sinφ`. Definitions of θ, the cohesion factor C and stress conventions require the original derivation. Under **explicit analyst conventional Mohr–Coulomb definitions**, a cohesion strength produces a cotangent term. That comparison does not establish an error: the source calls C a factor and its normalization is unknown. No corrected field pressure is inferred.

The printed injectivity expression includes a leading minus:

\[
Q_M(t)=-\frac{Q_r\Delta p_M}
{W[-\Delta p_M\exp(-\Delta p_r(t))]}.
\]

The main PDF does not state the pressure normalization or Lambert branch. [audit_pressure_limited_global.py](../scripts/audit_pressure_limited_global.py) therefore applies this expression only to **explicitly dimensionless synthetic variables**. With `q = Q/Qr`, its literal inversion satisfies:

\[
a=q(b-\ln q),\qquad q=-a/W(-a e^{-b}).
\]

Both real branches are checked. At `a = b = 2`, branch −1 recovers the reference ratio `q = 1`, while the principal branch gives another root. At smaller reference arguments, the reference root can lie on the principal branch. These are mathematical diagnostics of the missing convention; raw MPa values are never inserted and no native injection rates are claimed.

The printed plume-spacing inequality also needs clarification. Table 1 calls Q an injectivity/rate, while a diameter from mass conservation needs cumulative mass and a consistent total/per-site definition. Two synthetic cylinder examples include duration explicitly and close their mass balance. They do not repair the source notation or reproduce its plume, migration or pressure solution.

The native reference-pressure calculation, nonlinear superposition correction, defaults and code settings remain missing. A runnable inverse or failure-component example is not the complete author model.

## Horizon-specific resource and rate comparisons

The headline annual figures agree with cumulative mass divided by duration:

| Scenario M scope | Duration (years) | Reported resource (Gt) | Calculated mass/duration (Gt/y) | Quoted rate (Gt/y) |
| --- | ---: | ---: | ---: | ---: |
| Unrestricted | 30 | 3,640 | 121.333 | 121 |
| Unrestricted | 80 | 5,630 | 70.375 | 70 |
| Hydrocarbon history | 30 | 3,000 | 100.000 | 100 |
| Hydrocarbon history | 80 | 4,500 | 56.250 | 56 |
| Readiness Bands A/B | 30 | 780 | 26.000 | 26 |
| Readiness Bands A/B | 80 | 1,177 | 14.713 | 15 |

These are **separately optimized constant-rate horizon cases**. Connecting 121 and 70 as successive points of one actual deployment history would change their meaning.

A 10 Gt/y flat benchmark corresponds to 300 Gt over thirty years and 800 Gt over eighty. Figure 9's thirty-year readiness bars show Scenarios 11 and M above the former line. In the eighty-year panel only M is visibly above the latter. The target claim needs its mid-century scope preserved.

Figure 7 measures the fraction of **global resource**, while some prose refers to basin counts. It does not specify the duration or correspondence to readiness-filtered subsets. The quoted 91%/81% shares cannot automatically become subset percentages or failure probabilities. The roughly order-of-magnitude uncertainty is borrowed from earlier CO2BLOCK work, rather than a global probability distribution propagated here.

Figures 8a–f have different scenarios, horizons and symbol scales. The caption scales **diameter** to resource, with 1 or 4 Gt per millimetre depending on panel. Circle area must not be used linearly as resource. Blue site-limited circles indicate the imposed site-number/rate constraint, not the absence of other geological risks.

## Well analogues and physical transfer

Dividing the 5 Mt/y site cap by the cited 0.57 Mt/y average well rate gives 8.77, rounded to nine wells per site. The reported products agree:

- 73,508 sites / 4 sites per project = 18,377 project equivalents;
- 73,508 sites × 9 wells per site = 661,572 well equivalents;
- that well analogue is about 71.9% of the cited 920,000 petroleum-well count.

These are explicit analogues, not actual required wells or a construction schedule. A single 73,508 site count is reported without a clear horizon mapping, while Scenario M's composition changes between horizons. Actual per-well rates and integrity also vary. The cited 38% integrity survey must not be promoted to a global CO₂ leak/failure probability or retention factor.

National comparisons likewise combine different methods, data, geography and durations. Matching a reported Powder River total, or lying within an order-of-magnitude range for UK reservoirs, does not independently validate the global case. Closed boundaries, an imposed site cap, optimistic sampling, omitted compartments and omitted pressure management affect interpretation in different ways. The authors' upper estimates are scenario bounds, not proven physical bounds over all possible designs.

## Reproduction and Paper 1 status

The [input record](../evidence/comprehensive_review_inputs/B2-15.json), [bibliography](../evidence/comprehensive_review_inputs/B2-15_bibliography.json) and [reproduction summary](../outputs/comprehensive_review/B2-15_reproduction_summary.json) preserve provenance, formulas and missing fields. The script produces **53 limited checks**, twelve design rows, fourteen dimensionless Lambert roots and two mass-geometry examples. Eight focused tests check algebraic residuals and branches, reference scaling, conditional failure-envelope definitions, conservation/time/units, scenario scope and invalid domains.

Native global CO2BLOCK, basin data, scenario selection, field validation, uncertainty propagation and a complete utility/containment inventory remain unreproduced. All 68 originals and fourteen dependencies or scope requirements remain open.

Paper 1 should acknowledge existing pressure-aware global assessment and retain its separate need for calibrated field service and matched utilities. **No accepted operating/GHG input or current numerical result changes.** The prior combined 1.5 MPa HOLD remains, native files are preserved, and the comprehensive goal stays active.

Regenerate the scoped checks with:

```bash
python paper1/scripts/audit_pressure_limited_global.py
python -m unittest discover -s paper1/tests -p test_pressure_limited_global.py
```
