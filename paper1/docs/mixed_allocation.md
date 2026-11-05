# Shared-source annual allocation and fixed-plan reevaluation

`mixed_allocation.py` implements a new benchmark, not reproduction of Budiarto or Fraga. One1Mt/y published Noh transport-flow class is applied for30 nominal annual bins (2027–2056). It is not a measured Japanese industrial source. Source potential totals30Mt; unused supply remains uncaptured.

## Inputs, units and constraints

The eight MW-A reservoirs in TablesS2/FigureS9 are partitioned into disjoint r1–r4/r5–r8 groups. A control swaps which group receives the1000km route; the other route is5000 or10000km. Never add SW-A and MW-A as independent reservoirs. Annual rate bounds are the original chosen allocation outputs, explicitly exogenous proxy envelopes. A blank means no reported allocation, not geological zero. Reported resource/readiness remain enforced per reservoir.

Continuous allocation variables are inMt inside the MILP; integer voyage variables are counts. The partial objective is injected mass minus the uniform NETL-NGCC90/NVE2025-climate utility reference and IMO MDO/MGO default active-cycle WtW. InMt units, each flow coefficient is1-u/1000 (u:kg/t captured), and each voyage penalty is fuel_kg*IMO_kg_per_kg/1e9. Annual coarse capture equals planned injection. Source sums are at most1Mt/y, reservoir cumulative sums are at most reported resources, and route flow is at most net cargo times integer voyages. Voyage counts are bounded by assigned reference fleet times floor(8000h/cycle). Readiness and exogenous envelopes set upper bounds. Unit conversions are definitions, not empirical inputs.

Twelve problems are two long distances × two reservoir assignments × short-only/long-only/mixed. SciPy1.17/HiGHS reports optimal status and zero relative gap for these annual surrogate problems. This does not imply a detailed operating or lifecycle optimum. The three mode feasible sets are nested in the mixed mode; tests check its coarse objective cannot be worse than the exclusive modes under identical partition/distance.

## Detailed reevaluation and source topology

Each annual plan supplies a route-specific constant-within-year source share and an injection service cap to the existing event model. Two dedicated export tanks/loading berths split one common capture stream; receiving terminals are separate. Source shares sum to at most1Mt/y and are not adaptively reassigned when a route is blocked. No extra common-berth constraint is implied. Both reference fleet and one added vessel per assigned route are checked under index, earliest-window-end and least-active-hours priorities. This gives72 operating reevaluations and2160 annual rows.

Detailed capture, injection, fuel and ending stocks replace annual approximations. Endpoint inventory receives no injection credit. Actual reservoir-level redistribution is not optimised in the event model; total group injection stays within the aggregate planned yearly service and can be apportioned within its original allocations. Therefore no independent physical annual constraint is established. Assigned-fleet capital/idle burdens remain absent, including inactive-route assets; they are missing inventory terms, not free real assets.

## Results and checks

At5000km with r1–r4 on the short route, index dispatch and the added-vessel control, annual short-only/long-only/mixed plans allocate24.0/29.6/30.0Mt; operational injection is23.944/29.525/29.870Mt. Both assignments and distances are in the figure and CSVs; no geographic preferred route is inferred. The uniform utility factor and default ship fuel give partial component scores only. Complete-net-avoided fields remain empty.

Eighteen further dispatch controls compare the original six selected designs with identical fleets/source/calendar/service. Across these controls, rule changes span about−1.162 to+0.039Mt injected. This is deterministic algorithm sensitivity, not observed reliability or independent operator validation.

The test suite checks annual/cumulative source and resource bounds, readiness, disjoint groups, integer voyage/cargo/fuel consistency, nested coarse objectives, route-hour limits, variable-source zero years, default-policy regression and capture=injection+closing inventory. Numerical residuals establish conservation in the implementation, not physical field validation.

## Outputs and reproduction

- `mixed_reservoir_plans.csv`:2880 reservoir/year planned flows with envelope/resource/readiness metadata.
- `mixed_trip_plans.csv`:720 route/year integer voyage/fleet/cargo/fuel entries.
- `mixed_solver_audit.csv`:12 annual solve summaries.
- `mixed_operational_comparisons.csv`:72 fixed-plan operating results; `mixed_operational_annual.csv`:2160 annual rows.
- `dispatch_policy_controls.csv`:18 original-design rule comparisons.
- `mixed_validation.json` and `mixed_model_conventions.json`: checks, provenance and structural boundaries.

Run `python paper1/scripts/mixed_allocation.py` after the operational, reference-inventory and supplement outputs exist. The original operating outputs remain unchanged under default arguments; the extension adds variable source schedules and explicit dispatch/fleet choices.
