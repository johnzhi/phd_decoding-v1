# B2-18: prudent planetary storage limit — detailed findings

The retained 13-page PDF of Gidden et al., *A prudent planetary limit for geologic carbon storage*, Nature 645 (2025), DOI [10.1038/s41586-025-09423-y](https://doi.org/10.1038/s41586-025-09423-y), has been read as text and inspected as rendered pages. The four figure pages were enlarged to inspect their panels, captions, legends and labels. The record remains **incomplete**: the native GIS/IAM calculations, supplements and underlying source chain have not been independently verified or reproduced.

The [item-level record](comprehensive_review/B2-18.md) separates 16 sections, 14 lettered figure panels, 14 analyst transcriptions of prose relations, 14 variable/assumption groups, 66 claims and 16 open issues. There are no numbered main-PDF equations or tables. The three schematic subplots inside Figure 3a are recorded explicitly. All 93 printed bibliography entries have native page/line geometry in the [bibliography record](../evidence/comprehensive_review_inputs/B2-18_bibliography.json); reading those entries does not verify the originals.

## Cumulative resource and annual injection service

The central estimate is **1,460 GtCO₂**, with assessed sensitivities of **1,290–2,710 Gt**, after applying precautionary spatial exclusions to approximately 11,800 Gt of technical potential. It is a conditional, risk-screened cumulative resource. Its buffers and exclusions are policy and screening assumptions, rather than field-specific operating limits, failure probabilities or a universal legal quota.

The Methods explicitly incorporate pressure considerations. They use **0.037 Gt per 1,000 km³ of assessed bulk sediment volume**, for a **50-year injectivity period**, drawing on lower literature estimates and a closed-system pressure rationale. Describing the method as having no pressure consideration would be inaccurate. The coefficient is equivalent to **0.037 kg/m³ of bulk sediment**, or 37,000 t/km³; it is not the density of CO₂. It still supplies no site-specific pressure/rate/temperature history, calibrated well model or defensible annual service profile. Dividing a stock by 50 years only produces an arithmetic period average.

The central masks include protected areas, EEZ boundaries, polar circles, seismic hazard, SSP5 built-up urban areas in 2100 with a 25 km buffer, water depth up to 300 m, storage depth of 1–2.5 km, disputed areas and a 6 nautical mile buffer on each side of terrestrial international borders. The paper acknowledges that a pressure plume can extend beyond that border buffer. The seismic metric is probabilistic PGA hazard over 50 years, rather than a measured probability of injection failure. The offshore depth evidence contains discovered, abandoned, depleted and exploration assets; those points are not operating injection wells. Historical legal statements do not establish current project permissions.

Each exclusion removes volume from the area remaining after earlier layers. Consequently, the reported marginal contributions depend on order. Two disclosed overlapping-mask examples confirm that the final excluded union can remain the same while each layer's attributed loss changes. This only applies to fixed masks and weights; it does not reproduce ArcGIS geometry, raster resampling or the native sensitivity cases.

## Regional figures require reconciliation

Figure 2b reports central onshore/offshore resources of **1,010/450 Gt**. The enlarged Figure 2c retains these native labels and integer regional values:

| Native ring label | Ring | Sum of five region labels, Gt | Corresponding Figure 2b value, Gt |
| --- | --- | ---: | ---: |
| Offshore, top | Outer, technical | 5,701 | 6,060 |
| Offshore, top | Inner, central | 994 | 450 |
| Onshore, bottom | Outer, technical | 5,517 | 5,720 |
| Onshore, bottom | Inner, central | 452 | 1,010 |

The central discrepancies exceed ordinary display rounding. The technical totals also differ. These could involve labels, cases, region coverage or country allocation; the missing native arrays and regional crosswalk are needed to distinguish them. **No ring is silently swapped and no corrected regional resource is accepted.** The five-region outer sum is 11,218 Gt and inner sum 1,446 Gt, compared with Figure 2b's 11,780 and 1,460 Gt. Country/territory coverage remains open.

Other discrepancies need different treatment. The lower sensitivity's displayed 980 + 300 = 1,280 Gt can be reconciled with the displayed total 1,290 Gt by rounding. The quoted 175-fold scale-up is also compatible with rounded 8.7 Gt/year and 49 Mt/year inputs; their literal quotient of 177.55 is not proof of an arithmetic error. Those quantities also compare future storage demand against historical capture capacity, rather than two measured injection flows.

Figure 3b's caption specifies a scale of 1,000 Gt, while the axis additionally carries a ×10⁶ annotation. The native array/display convention remains unresolved. Applying both multipliers would invent a resource that the caption and other panels do not support.

## Temperature potential and competing storage uses

The stated temperature arithmetic is consistent under the disclosed assumptions:

| Resource, Gt | At 0.45 °C per 1,000 Gt | At 0.27 °C per 1,000 Gt |
| ---: | ---: | ---: |
| 1,290 | 0.5805 °C | 0.3483 °C |
| 1,460 | 0.6570 °C | 0.3942 °C |
| 2,710 | 1.2195 °C | 0.7317 °C |

The abstract's approximately 0.35–1.2 °C envelope combines storage and climate-response corners. The body's approximately 0.6–1.2 °C holds the central response coefficient fixed, while 0.35–0.7 °C uses the lower response. These are different conditional ranges, rather than inconsistent calculations.

This calculation assumes that all available stock serves **net atmospheric removal** and that the temperature response to negative emissions is sufficiently similar to the response to positive emissions. Storage used for fossil CCS or counterbalancing residual emissions competes with that use. A captured or injected tonne therefore cannot automatically be credited with the calculated cooling potential. Climate-response asymmetry and zero-emissions commitment remain explicit limitations. The paper's leakage threshold is a cited climate-accounting claim, not a measured field retention factor.

## Scenario extrapolation and thermodynamic assumptions

The Methods identify AR6 `Emissions|CO2` and `Carbon Sequestration|CCS`, interpolation to yearly values with pyam, annual cumulative sums through 2100, a first positive-to-negative emissions crossing for net zero, and remaining-stock divided by the injection rate at that point. They extrapolate annual storage with a first-order `slinear` spline until 2300. Figure 3c gives years after net zero at a fixed rate; Figure 3d gives calendar-year exceedance under extrapolation. These measures should not be interchanged.

The 400 disclosed synthetic annual rows illustrate why the native implementation matters. With 100 Gt already used, a 1,000 Gt stock and a 12 Gt/year endpoint, holding the rate fixed gives 75 remaining years. Extending a terminal slope of +0.4 Gt/year per year reaches the discrete threshold in 2144. A slope of −0.4 eventually yields negative injection under raw extrapolation; a nonnegative floor gives a different cumulative trajectory. **This does not establish that the authors' code permits negative storage.** Their floors, endpoint knots, filters, exact-zero handling and noncrossing treatment remain unverified. Synthetic examples do not reproduce the reported scenario percentiles or Asia results.

The depth discussion says that compression makes density decrease while the occupied volume decreases. Those statements conflict for equal mass. Its approximately 30-fold and 36-fold volume reductions also lack an explicit surface pressure basis. Six conditional pure-CO₂ EOS examples use the stated 15 °C surface temperature and 25 °C/km gradient, but explicitly analyst hydrostatic pressure assumptions. At 1.5 km, the equal-mass volume ratio is about 359 relative to 1 atmosphere, versus about 35.7 relative to 10 bar. This dependence prevents an automatic correction of the source's ratios. Neither analyst surface pressure is inferred to be native. The cited original is the 1976 *International Thermodynamic Tables of the Fluid State: Carbon Dioxide*; its relevant tables remain unverified.

## Original-source and asset status

One [scoped citation check](../evidence/comprehensive_review_inputs/B2-18_citation_checks.json) compares R024 against retained Wei et al. (2021), B2-16, pages 1 and 8. It supports the existence of earlier global, high-level onshore basin resource assessment using a DOE volumetric framework. That original expressly prohibits cross-border matching in its network model. This check verifies selected passages, not the full original or an exhaustive novelty claim. The other **92 direct originals** and **14 dependencies or audit requirements** remain open.

The native PDF advertises:

- [Author code](https://github.com/gidden/2024_gidden_cstorage).
- [Generated data record](https://zenodo.org/records/15657543); bibliography R093 instead prints [DOI 15657542](https://doi.org/10.5281/zenodo.15657542). A concept/version relationship is possible and remains unverified.
- [IIASA data explorer](https://cdr.apps.ece.iiasa.ac.at/story/prudent-carbon-storage).
- Publisher supplements, with at least Tables 1–7 and Figures 1–13 mentioned, and peer-review reports.

These assets have not been retrieved while external research is paused pending the requested Chrome connection. Public availability statements are preserved as leads. The native PDF also says “modified publication 2025”; its revision history has not been checked. No online absence, code license, dataset correspondence or successful author-model reproduction is inferred.

## Reproduction and Paper 1 use

Run `python paper1/scripts/audit_prudent_storage.py` for 41 limited checks, four regional ring comparisons, six temperature rows, two mask sequences, 400 synthetic extrapolation rows and six conditional pure-fluid state examples. Eight tests include exhaustive mask-pair/union comparisons and a closed-form annual-sum check. These verify components under disclosed conditions, not the native global GIS, country resources, IAM scenario selection, climate response or field service.

Paper 1 can cite the conditional resource and allocation context, including the pressure-aware coefficient and explicit deployment limitations. It should retain the figure/state/scenario qualifications and distinguish fossil abatement, residual offsets and net removal. This paper supplies neither native pressure-constrained reservoir operating data nor a complete matched capture-to-ship utility balance. Accepted operating/GHG inputs and numerical results remain unchanged, including the existing combined 1.5 MPa source-case HOLD. Continue with B3-01 while retaining all unresolved source and model work.
