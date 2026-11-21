# LP ship–MP terminal interface: comprehensive reading findings

All fifteen physical pages of Deligiannis et al. (2026), B1-20, have been read and visually inspected: every section, twenty-two figures, seven tables, four numbered equations, nomenclature, conclusions, interests and data statement. The p-h diagrams were magnified; some overlaid contour labels and fine subcooling ticks remain unresolved for exact numeric readout. The [item record](comprehensive_review/B1-20.md) preserves that limitation. DOI: `10.1016/j.ijggc.2025.104544`; source SHA-256: `5bcd3ea93dce775fcc254ad13ba6e959617ff2c745635828fb1cc54b09b17602`. Native files and rights are unchanged.

The paper remains **incomplete under the comprehensive-audit standard**. All nineteen underlying originals and seven named dependencies remain unverified. The [196 limited diagnostics](../outputs/comprehensive_review/B1-20_checks.csv) reconstruct printed HTX area/cost and rounded electricity accounting, with conditional geometry and mixing examples. The [reconciliation](../outputs/comprehensive_review/B1-20_reconciliation.json) explicitly leaves the native COSSMOS/SRK tank, transfer, compressor, controller and optimization models unreproduced.

## Physical boundaries and transfer quantities

The case compares 7/8.5/10 bara ship tanks with 12/16/20 bara terminals. Pressures are explicitly absolute. The reference vessel has three 7300 m³ tanks, with 5840–8760 m³ per tank in sensitivity cases, and a 30000 m³ terminal tank. The paper gives approximately 24700 t as a reference and describes constant transported mass, while later tables report varying loading/discharging quantities. These definitions need native state and case mapping before using a common service denominator.

Under the conditional fixed-volume interpretation of 96% initial fill and 4% heel, three reference tanks transfer `3 × 7300 × (0.96−0.04) = 20148 m³`. Dividing by 12 h gives exactly the printed 1679 m³/h discharging rate for the whole vessel; the corresponding per-tank rate is 559.67 m³/h. This helps interpret the individual-tank language and 600 m³/h per-tank pump envelope, but it does not reproduce a pump curve or dynamic transfer. Rounded fixed densities give conditional net masses close to, and distinct from, Table 5's 22970/22602/22180 t. None replaces the source's actual reported masses.

Discharging raises liquid pressure and warms it toward terminal conditions. Vapor displaced from the terminal partly returns to the ship; subcooling can condense terminal vapor and reduce displaced mass. Loading depressurizes the liquid and can flash vapor, requiring return compression/cooling, excess-vapor treatment or liquid subcooling. Returned or re-liquefied vapor is not automatically atmospheric loss. The pure-CO₂ reference p-h chart is illustrative; it does not supply the actual Northern Lights mixture or native SRK property implementation.

## Equations and reconstructed components

Equation 2, `Q = U A LMTD`, uses `U = 2000 W m⁻² K⁻¹`. Converting reported MW to W reconstructs Table 4 areas within propagated display intervals. Equation 3 is the standard logarithmic mean of the two positive terminal temperature differences, with the equal-difference limit handled explicitly. Independent integration checks this algebra. Actual seawater/glycol/CO₂ boundary temperatures, exchanger design, variable properties and freezing protection remain missing; no native LMTD or thermal-duty prediction is reproduced.

Equation 4 uses `12003 × A^0.603 × 1.011187^Pressure`. Numerical terminal pressure in bar reproduces the nine reported costs within rounded-area intervals. The empirical coefficients retain their area, pressure and currency conventions; pressure in Pa cannot be substituted into that exponent. These are evaluations of the printed component equation, not independently validated vendor costs, installed costs or a known current cost vintage.

Equation 1 for spray cooling requires a careful mass boundary. With final mixed flow `M`, incoming hot vapor `G`, sprayed liquid `L`, and `M = G + L`, conservation gives `M htarget = (M−L) hhot + L hliquid`. Solving gives the printed form `L = M(htarget−hhot)/(hliquid−hhot)`. If instead the specified VR quantity is hot inlet flow, the appropriate expression is `L = G(hhot−htarget)/(htarget−hliquid)`. The source describes vapor demand at ship conditions, so the printed formula can be consistent with a final-flow definition; it is not automatically an algebra error. Native flow labels, enthalpies and phase completion are needed to reproduce its 5.7-t spray claim. That mass is 0.0231% of 24700 t; the printed 0.025% implies 22800 t, close to net discharge quantities but not a verified correction.

## Source conflicts retained on hold

At LP 8.5/MP 16 bara, Figure 6 gives heating demand of **4.4 kWh/t**. Figure 14's heater plus vaporizer labels instead sum to **10.5 kWh/t**, and Table 4's 19.8-MW duty is much closer to the latter under the stated duration and mass scale. Figure 10 also uses the low non-subcooled bar, making the subcooled bar larger at this point despite the broad heat-reduction explanation. Both printings are retained; no 4.4-to-10.5 correction is adopted.

Table 3 gives heater area **370–2500 m²**, whereas all Table 4 areas fall between **47 and 308 m²**. The ranges do not overlap. Scope, equipment or case metadata may explain this, but the source does not provide that reconciliation.

Figure 17 and Table 6 both describe vapor displaced during loading, yet all nine reported values differ. For example, at LP 7/MP 16 bara they give **3939 t** and **6741 t**. A total-versus-excess or state/case distinction is possible but unverified. Neither is substituted for the other or interpreted as vented CO₂.

Table 7 lists cooler electrical demands of **−47 and −18 kW** at two conditions, and includes them in signed totals. Negative thermal demand could indicate a heating need or a sign convention; it does not establish usable electrical generation. These entries remain literal and excluded from accepted power credits. They are not silently clamped to zero. The thermal-versus-electrical definition of the subcooler row also needs confirmation before applying COP 2.4 again.

## Electricity, timing and economic interpretation

The loading tables' costs agree with `power × 12 h × 0.11 EUR/kWh` within displayed precision. Their specific-demand numbers follow `power × 12 h / own-case loaded mass`, even though the tables label them `kWel/ton`. That is a power-versus-energy unit issue, not permission to change the source labels or assume an observed load profile. Component-sum differences of up to 1 kW remain recorded as rounding residuals.

Compressor/cooler demand alone and demand including excess-VR re-liquefaction are different comparison boundaries. Subcooling is more costly per reported tonne than compressor/cooler alone. Against the cases including re-liquefaction, it is cheaper per own-case tonne in only two of the nine printed comparisons, both at LP 7 bara. Total power, absolute cost and cost per tonne can rank differently because the cases use different loaded masses. The source's broadly similar ranges do not establish a universal lowest-cost strategy or a global optimization result.

Ship and shore discharge intensities approximately support Table 5's combined 0.03–0.05 EUR/t under its electricity-price assumption. These are selected interface loads, not full transfer or vessel cost. The fixed pump/compressor efficiencies, electrical efficiency and 4% distribution loss need distinct boundaries; a loss must not be counted twice. Neither Greek electricity pricing nor these physical loads supplies a Japanese utility supplier, capture heat inventory, annual berth/weather schedule, full shipping GHG or geological retention factor.

## Remaining verification and Paper 1

The [bibliography/dependency register](../evidence/comprehensive_review_inputs/B1-20_bibliography.json) retains nineteen printed entries, including incomplete or conflicting identities. Similarly titled liquefaction papers are not automatically the same original. Legal open-access and APOLLO funding claims are separate unverified dependencies. All authors' declared Ecolog/DNV employment interests and the explicit data-on-request statement were read. No request has been sent. No internal appendix, embedded file or explicit external supplement notice was identified; this does not establish public absence. External retrieval remains paused under the requested Chrome wait.

Paper 1 uses this study to qualify LP/MP transfer requirements, mass and vapor boundaries, heat versus electrical demand and conditional equipment choices. The unresolved values do not enter numerical operating/GHG inputs. Reproduction needs versioned COSSMOS/SRK cases and rights, chosen mixture, initial/boundary/control states, synchronous flows/enthalpies, equipment curves, full utilities, convergence and independent validation. Continue with B2-01 while these tasks remain open.

Validation: five new component/domain/provenance tests passed, followed by all 155 repository tests after source-hash and register regeneration. Tests verify mixing conservation, LMTD integration, displayed HTX components and accounting boundaries; they do not validate the unavailable native model or underlying source chain.
