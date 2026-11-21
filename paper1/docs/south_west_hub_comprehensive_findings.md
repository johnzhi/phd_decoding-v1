# South-West Hub: comprehensive reading findings

All 26 retained pages of Hosseinzadeh et al. (2026), SPE234571MS / B1-12, have been read and visually inspected. The [item record](comprehensive_review/B1-12.md) covers 22 section groups, 17 figures, three tables, 13 numbered equations, six explicit identities/comparisons and 24 claim assessments. The source PDF remains unchanged, SHA-256 `cf2e2603165f4002afb0cf40db2ea4318a822721ff741202fbc4e92ece7d2231`. Source illustrations are not newly redistributed.

The paper remains **incomplete under the comprehensive-audit standard**. All 99 printed bibliography entries and 19 additional citation/data dependencies remain unverified. Native Visage/dynamic cases and essential inputs are unavailable; no complete author model is independently reproduced. The header states selection through abstract review and that SPE did not review the contents.

## What the model actually covers

This is a proposed Harvey-field storage study in the onshore southern Perth Basin, Western Australia. Four existing characterisation wells, three wells with usable correlation logs and nine planned injectors are distinct sets. The model transfers isothermal dynamic pressure/water-saturation histories to a one-way poroelastic Visage model. It does not demonstrate converged flow/property feedback or thermal coupling.

Thermal effects are deliberately excluded for lack of a temperature field and measured injection conditions. The authors explicitly reserve nearwell and cooled near-seal integrity for future full thermo-hydro-mechanical analysis (pp10,21–22). Their assertion that distant faults lie beyond the important cooling region still needs quantified thermal-front, rate, time and uncertainty evidence. p11 also says the caprock is treated as overburden and excluded from the modeled volume. Neither the generic seal-integrity motivation nor Figure7's overburden wording establishes a discretised, validated caprock failure model.

Five extra edge cells, geometric growth1.5,50m stiff plates and250×250m horizontal upscaling describe a numerical design. Full vertical mesh, plate materials, load/displacement constraints and convergence/boundary sensitivity studies are missing. Iterative fitting to the available LOT data is calibration; solver convergence is not independent field validation.

## Equations, units and material basis

The [90 limited checks](../outputs/comprehensive_review/B1-12_checks.csv) and [reconciliation](../outputs/comprehensive_review/B1-12_reconciliation.json) preserve the printed inputs. They are separate from accepted operating/GHG calculations.

- Eq1, `Vp=304.8/Delta_t` with transit time in microsecond/ft, produces km/s. At100microsecond/ft it gives3.048km/s, or3048m/s. The later m/s prose needs reconciliation with the empirical coefficients and density units. A unit inconsistency in print is not proof of an error in unavailable native code.
- Eq6 prints `Estatic=.41Edynamic−1.06`. The intercept must carry a modulus unit; its unit, regression domain and core residuals are not provided. A GPa illustration is explicitly conditional. The positive-static-modulus threshold is2.5854 in the intercept's unit.
- Eq13 visibly prints `E/(1−nu²)*epsilon_x`, rather than the `nuE` term in a symmetric coefficient swap. Subtracting printed Eq12 gives `SH−Sh=E*epsilon_y/(1+nu)`. The symmetric analyst comparison gives `E*(epsilon_y−epsilon_x)/(1+nu)`. At equal strains the printed form retains a horizontal difference, while the comparison does not. Both are recorded; no missing coefficient is silently inserted.
- Best-fit strains .1/.9 and Table3 strains have no stated numerical scale. For an analyst E5000MPa and nu.22, literal .1/.9 gives a printed horizontal difference3688.52MPa; multiplying both strain numbers by.001 gives3.6885MPa. These demonstrate the importance of scale and are not inferred Harvey stresses.
- Eq11's density integral needs compatible force/mass and area units to yield psi from lb/ft3 and ft. The explicit SI conversion of an analyst150lbm/ft3,5000ft column gives5208.33psi at standard gravity. The raw numeric product with g is not adopted as psi.

Formation-average comparisons remain conditional. Prose uses an undefined G token while Figure8 labels bulk modulus; dynamic/static and spatial weighting are not resolved. Applying nonlinear wave/UCS/friction relations to rounded mean velocities does not reconstruct the mean transformed logs. Consequently, differences among prose means, Figure8 and borrowed Table1 cannot establish a hidden model error or justify replacing any material input.

All ten Table1 rows and90 parameter cells are preserved. Two fault porosities mean HRP, host-rock porosity, and remain numeric nulls. All ten tensile strengths equal half cohesion. Inverting Eq9 reproduces the tabulated UCS values within0.046MPa from rounded cohesion/angle inputs. This is an internal arithmetic check, not independent laboratory validation, verification of Zhang2015 or identification of the active native cell/fault properties.

## Calibration, figures and calendars

Table2 separates pump pressure[psi] and LOT[MPa]; their difference is not labelled an error or a measured hydrostatic correction. Mud density, datum and raw pressure-time histories are missing. Hv3 at1467.4m is expressly a formation integrity test, which does not establish a measured fracture-stress equality.

Table3 reports7.4MPa at400m and26MPa at800m. Candidate Table2 observations are7.4MPa at209m and26.23MPa at848m. These are unresolved candidate pairings, not silently matched observations or corrected depths. Table3 K implies epsilon_y .85,1 and1.08, with scale still unknown.

At1500m the paper reports Sh32MPa, SH37MPa and ratio1.125. The reported pair gives1.15625. All source numbers remain intact. Its separate Sh-gradient statement prints .18MPa without a length denominator; no alternative gradient unit is guessed.

Figure10 has two pressure cross-sections with a basal-Eneabba index map. Its left legend reaches800psi while the caption says500psi. Body descriptions of an initial vertical profile and plan at3055m differ from caption2020/2050 cross-sections. Native quantities, total versus change, pressure reference and dates need resolution before extracting a pressure field.

Figure16 plots four different cells:40-29-49 at2020,40-39-26 at2030,50-36-49 at2035 and50-31-69 at3050. This cannot demonstrate a single cell's time trajectory. The year3050 is preserved. p19 histories2021–2035, the30year reference plan, Figure10/17 dates2020/2050 and the1000year goal remain distinct. No calendar correction or annual interpolation is inferred.

Figure17's selected pink intersection agrees with its displayed −2 no-failure category. The legend's highest numeric tick is1, whereas prose describes cap failure as code2; its date header is clipped. Whole-model no-failure is an author assertion, not an independently inspected all-cell dataset. Yield classification does not supply fault slip, permeability, leakage or failure probabilities.

## Pressure plan, sources and Paper1

The reference plan proposes a total800000t/year over30years, with nine wells completed in the lowest250m of Wonnerup and a360bar BHP constraint at2948m (p18). The product24Mt is nominal plan arithmetic. Equal division over nine wells is only an analyst example, not a reported allocation. The expression `360bar=Pp+.9*69bar` conditionally implies297.9bar reference Pp and62.1bar increment; neither is measured or independently justified without compatible pressure references and controls.

Keeping the plume below800mTVDss for1000years is a stated simulation goal, not a demonstrated retained-carbon balance. No native target sweep, per-well history, maximum annual mass service,1000year output or actual storage allocation is retained.

The [bibliography register](../evidence/comprehensive_review_inputs/B1-12_bibliography.json) preserves99 printed entries and19 additional dependencies. Missing or mismatched identities include Eaton1975, Fjaer2008, Wang2000/2017, Zoback2007, Pervukhina2017, King2008, Hillis/Reynolds2000, Gin/Qin and several years/spellings. Some cited titles raise geographic or subject-scope questions; exact original passages must establish whether they support the claims. A title or a similarly named retained paper is not a substitute. Public supplements, errata and code remain unverified while external retrieval is paused pending the requested Chrome connection.

Paper1 can retain a named Australian conceptual example of isothermal pressure-constrained design and geomechanical screening. It cannot adopt the nominal rate,24Mt,360bar, selected nonfailure plots or1000year target as calibrated annual maximum service, permanent retention, contracted imported-CO2 access or a GHG factor. Existing accepted inputs and numerical results are unchanged.

Validation for this checkpoint: the full92-paper inventory/hash check, document/workbook builds, link/diff checks and119 unit tests passed. Tests include independent SI/wave-elastic consistency, the literal strain symmetry counterexample and preservation of missing values, conflicting dates and incomplete evidence states. Passing these checks does not validate the unavailable author models.
