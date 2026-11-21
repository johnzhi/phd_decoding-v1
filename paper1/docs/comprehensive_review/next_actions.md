# Continuation queue

The comprehensive audit is active and unfinished. Current coverage is generated in [README](README.md); the complete pending-paper list is in [papers.csv](../../outputs/comprehensive_review/papers.csv). Prior targeted reviews do not count as exhaustive completion.

1. Review B1-01, then continue remaining local main PDFs. B4-06 reference55→Zhang/Lau2022 B4-08 now has partial resource/property support; reference31→SimCCS B3-44 supports the static MILP mechanism with artificial-cost qualifications. Their own232/28 originals and complete field/GIS/optimiser models remain open. The [Zhang–Lau](../zhang_lau_comprehensive_findings.md) and [SimCCS](../simccs_comprehensive_findings.md) findings distinguish implemented equations from missing author models.
2. Continue the remaining main PDFs, giving priority to B1-01 and the pressure/injection, ship-conditioning and lifecycle papers used by Paper1. Each paper needs its own source-hash/page-anchored record covering all requested dimensions.
3. Check exact retained citation matches before seeking external sources. The B4-05→B3-11 edge is checked with partial support and a method-attribution conflict; this does not verify B3-11's own 25 references. Do not merge merely similar titles or versions.
4. External original papers, public supplements, code and errata remain pending under the user's request to wait for a Chrome connection. Local reading/reproduction can continue. Do not silently resume Firecrawl or direct public downloads.
5. Keep new diagnostic/reproduction artifacts separate from accepted Paper1 inputs. No disputed unit, guessed correction, missing stock boundary or unreproduced allocation becomes an operating/GHG input. Save verified checkpoints to the same GitHub branch.

Use `comprehensive_audit.py` to regenerate corpus/page registers and rendered review records. `audit_diagnostics.py`, `reproduce_ooi_cascade.py`, `audit_budiarto_fulltext.py` and `reproduce_zhang_lau_aquifers.py` perform explicitly limited diagnostics/component reproductions, separate from the accepted Paper1 model.
