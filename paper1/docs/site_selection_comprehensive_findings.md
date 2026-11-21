# Depleted-reservoir site-selection audit — 21 November 2026

All 14 retained pages of Hamid (2026), OTC-36331-MS / B1-10, have been read and visually inspected. The [item record](comprehensive_review/B1-10.md) covers eleven figures, no tables, thirteen numbered equations, five additional identities/constraints and an independent radial-flow derivation. Fifteen printed references and five additional dependencies are tracked. Source SHA-256: `0ccc6311dcc4b1a971a0f7cfa6f61c3891c11ec3403a98a6578993fb4145101a`.

The paper remains **incomplete under the comprehensive-audit standard**. The original PDF is unchanged. No source graphics are newly redistributed. Complete modified inputs, native outputs, project code, software/property versions, external assets and most cited originals remain unavailable or unverified.

## What the reported model establishes

The case has four anonymous reservoirs connected individually to a hub: Near at10km, Mid1/Mid2 at100km and Far at300km. Inputs are explicitly modified/anonymised. Each pipeline/reservoir has one injection well. The implemented allocation is annual economic dispatch; the full global MILP, binary activation and PSO comparison are omitted. The abstract's MILP/safety claims do not establish an independently verified global solution.

The model constrains **average reservoir pressure**, while the reported case explicitly allows flowing bottomhole pressure above the fracture limit. Figure8 shows Near and both mid-distance curves above the dashed threshold; the Far curve is below it. Positive near-well pressure gradients make the local constraint stricter even when small. Passing an average-pressure test cannot alone guarantee local fracture safety.

The paper discusses hydrostatic head, skin, choke cooling and phase sensitivity in its value-chain explanation. Its implemented model omits hydrostatic head and skin; complete fluid composition, EOS/property states, thermal/phase controls and well details are not supplied. It therefore does not provide validated annual maximum injection service or a complete capture-to-storage inventory.

## Graphic/text conflicts

Every equation and plot was enlarged where needed. Three consequential disagreements remain open:

- **Demand ramp:** the text says the first five years; Figure4 reaches10Mt/year around year10 after lower steps. No exact native annual schedule or integrated total is adopted.
- **BHP identity:** Figure8 labels its highest green curve Mid1; the body attributes elevated pressure to Mid2. Both printed identities remain; labels are not silently exchanged.
- **Cumulative baseline:** page11 quotes approximately USD230million for Figure6. Its endpoint is visibly above USD250million, approximately USD275–290million by a deliberately broad visual reading. Figure11 ends near the quoted USD148million for Far-only routing. The quoted230/148 comparison and the graphic interval are separate evidence, not a corrected source total.

The quoted difference is82millionUSD, or35.65% of230million. That arithmetic is not a verified saving, NPV, global optimum or transferable factor.

## Equation checks and limits

Eq1 is naturally a positive frictional pressure-loss magnitude; an actual downstream pressure gradient needs a sign convention. Eq2 requires consistent relative roughness/Reynolds number and a turbulent regime. Neither supplies a full thermal, phase or bathymetric model.

Eq3 is linear in **P/z** under fixed temperature, effective pore volume and suitable gas composition. If z depends on pressure, recovering pressure is implicit; it is not generally linear in pressure. Mass increments require a time conversion from rates. Residual gas, brine, rock and aquifer response, property calls and pressure-update controls remain unprovided.

Eq5 prints a radial pressure-squared increment without an explicit pi in its coefficient. An independent SI integration of axisymmetric gas Darcy flow, with constant viscosity/z/temperature, gives

\[
\dot m=\frac{2\pi r h k}{\mu}\frac{Mp}{zRT}\left|\frac{dp}{dr}\right|,
\qquad
\Delta(p^2)=\frac{\dot m\mu zRT}{\pi Mkh}\,\text{shape}.
\]

Holding the same `ln(re/rw)−0.75` shape term, the printed and independently derived increments differ by a factor of pi. This is a **geometry/convention question**, not a proven error in unpublished code. The cited Dake passage, unit/geometry conventions and applicability of constant-property gas pressure-squared flow to the dense-phase case still require verification. No replacement equation is promoted to accepted inputs.

Eq7 is dimensionally a constant-density pumping approximation. It does not by itself reproduce low-pressure gas compression with changing properties and heat rejection. Eq8 requires compatible power/tariff units: SI watts become kW before multiplying hours and a currency/kWh tariff. The source does not specify that unit basis, so a code conversion error is not established.

Eq9's `1.2 D^1.3 L` needs a dimensional cost coefficient or normalisation, currency year and length convention. Using metres versus kilometres changes its raw numeric output1,000fold. Raw results are left without assigned monetary units. Eq10 minimizes annual total cost; a marginal cost per mass still requires a derivative or explicit normalisation before Eq11.

An analyst counterexample also shows that start-of-year availability alone can exceed an end-of-year pressure bound. It is not attributed to the author code: native rate caps, within-step headroom, clipping/rescaling, time indexing and mass conservation are missing.

## Persistent assets and source support

The diameter curves are reoptimized each year after first-use construction. Figure10 changes roughly0.30→0.55m. A once-built pipe does not acquire those later diameters without a design/upgrade rule and corresponding costs. A fixed maximum-size design, material/pressure rating, well/BHP constraints and equivalent-service comparison are not supplied. The smaller quoted maximum change0.50→0.55m gives a10% diameter increase and21% area increase; these are geometric comparisons, not full network savings.

Two [scoped primary checks](../evidence/comprehensive_review_inputs/B1-10_citation_checks.json) use exact retained originals:

- **Bertoni et al. / B2-04:** the inspected abstract/methods and p7 Eqs29–34 support reservoir-dynamic MILP coupling. Its explicit BHP≤0.9pmax and hydrostatic/pumping relationships differ materially from Hamid's average-pressure proxy. Its own validation does not validate Hamid's case.
- **d’Amore et al. / B3-45:** the inspected p7–8 annual-cost formulation supports network design, routing/size binaries and geographic targets. These passages do not establish the pressure-evolving reservoir/injectivity attribution made jointly in B1-10. The exact original also includes Romano, omitted from B1-10's reference.

These are targeted citation checks, not full audits of either original or their citation chains/models. Thirteen other printed references and five additional dependencies remain unverified. No embedded supplement/code/data notice was found locally; public availability remains unverified during the requested Chrome wait.

[audit_site_selection.py](../scripts/audit_site_selection.py) retains [37 limited checks](../outputs/comprehensive_review/B1-10_diagnostics.csv), including eight explicit missing-input categories. The modified case, EOS, annual dispatch/diameter solver, global MILP and PSO remain unreproduced. Paper1 retains qualified method context and excludes this paper's cost comparison or unsafe allocations as calibrated physical/GHG inputs. B1-11 is next in the local queue.
