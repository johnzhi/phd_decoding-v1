# SimCCS full-text audit — 21 November 2026

All nine pages of Middleton and Bielicki's *A scalable infrastructure model for carbon capture and storage: SimCCS* (2009) have been read and visually inspected. The [item record](comprehensive_review/B3-44.md) covers six figures, Table 1, all 23 numbered equations, the radial-flow derivation, variable/input/set definitions, six footnotes and 28 bibliography entries. Small equations and figure legends were magnified. Original SHA-256: `4a888e57269c2636426ca93b53d09a7ab62a8f5f192645e65d46e5c75f2b6d75`.

The paper remains **incomplete under the comprehensive-audit standard**. Exact underlying originals and author assets remain unverified. The original California GIS/MILP, well-count/pressure iteration and EOS regression fitting are not independently reproduced.

## What the source supports

The original combines geographic candidate-network generation with a MILP selecting capture sites, reservoirs, discrete pipeline sizes and flows. It supports Budiarto's reference 31 description of joint cost minimisation and network scale/utilisation mechanisms. The qualification matters: all infrastructure is built simultaneously, mass variables/capacities are converted to **25-year lifetime tonnes**, and each capture target is reoptimised from scratch. A 30 Mt/year solution is not a staged extension of the smaller solutions.

The California case has 37 sources and 14 depleted-oil field nodes. The source explicitly says pipeline construction costs were **artificially reduced** to emphasise the network's capabilities (pp5–6). The factor is not provided. The reported low transport costs and percentage savings are therefore not transferable calibrated prices or GHG benefits.

## Independent components and unit checks

The [implementation](../scripts/audit_simccs_components.py) reproduces the printed property and well-cost functions and generates [21 diagnostics](../outputs/comprehensive_review/B3-44_diagnostics.csv). All geometry/flow examples are explicitly analyst fixtures, not California field data. Nine [property-function evaluations](../outputs/comprehensive_review/B3-44_printed_property_functions.csv) use analyst-selected points; they do not establish the authors' fit domain or validate an EOS.

- **Pressure-drop interface:** Equation 16's factor 8000, with the printed kg/s, kg/m³, km and m inputs, gives pascals by the Darcy–Weisbach derivation. Equation 15 labels pressure drop MPa. An explicit factor of one million is required between these numerical bases. Both raw and SI-expressed MPa values are retained; no silent author-input correction is made.
- **Hydrostatic interface:** Equation 18, `1000 × density × g × depth_km`, likewise gives pascals. The surrounding P/T and injectivity calculations use MPa. Main p4 also cites equation 19 for head gain, whereas the actual head equation is 18.
- **Viscosity:** Footnote 6 explicitly distinguishes Equation 20's **mPa·s** from Equation 17's **MPa·s**. The conversion multiplier is `1e-9`; omitting it changes the computed radial rate by nine orders of magnitude. The independent MPa-based expression agrees with a separately constructed Pa-based expression.
- **Radial scope:** The integrated steady Darcy expression estimates well requirements, not a transient pressure front, multiphase relative permeability, interference or annual maximum service. The signed radial direction/integration-limit convention needs clarification.

These are checks of the printed specification. Without author code and coefficients, they do not establish an error in the unpublished implementation. A fresh CoolProp comparison was not performed because it is unavailable in this runtime; existing saved EOS outputs do not validate this fit or verify the underlying cited article.

## Remaining specification questions

The magnified incoming-neighbour subscript in Equation 4 includes `i∉R`; its intended indexing and the zero extension of source/sink variables need clarification. Equation 13 also prints a `j∈S` quantifier for `a_i`. Literal notation is preserved without inventing a corrected optimiser.

Table 1's source mean times count gives 64.824 Mt/year; if that mean were gross emissions, applying the stated maximum 90% would give 58.3416 Mt/year. The text's maximum is roughly 56 Mt/year. The original selected inputs and capacity definitions are needed to reconcile these quantities. The 3.1% mean reservoir-utilisation denominator is also unprovided. No capture correction or utilisation reinterpretation is adopted.

Full reproduction requires the MIT raster, corrected WestCarb2008 sites, all candidate arcs and capacities, fixed/variable costs, diameter data, cost-deflation factor, preprocessing/solver code and raw solutions. Later SimCCS versions are not substituted for this 2009 case. Separate supplement/code availability is unverified; no embedded attachments does not prove absence online.

## Consequence for Paper 1

Retain SimCCS as a qualified static network-method reference. Do not transfer lifetime stocks as annual storage limits, low demonstration transport costs as actual prices, or network savings as a lifecycle credit. Existing operating/GHG outputs are unchanged. B1-01 is next in the local audit queue; external retrieval remains paused pending the requested Chrome connection.
