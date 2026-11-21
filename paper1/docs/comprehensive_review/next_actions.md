# Continuation queue

The comprehensive audit is active and unfinished. Current coverage is generated in [README](README.md); the complete pending-paper list is in [papers.csv](../../outputs/comprehensive_review/papers.csv). Prior targeted reviews do not count as exhaustive completion.

1. Review exact retained SimCCS B3-44, then B1-01. B4-06 reference55 is now checked against Zhang/Lau2022 B4-08 for partial resource/property support. B4-08 has all22 main pages inspected and its24 aquifer resource values independently reconstructed; its232 underlying sources and full field models remain open. See the [Zhang/Lau findings](../zhang_lau_comprehensive_findings.md) and [Budiarto findings](../budiarto_comprehensive_findings.md). B4-06 annual kr,t, exact routes and author optimisation remain unreproduced.
2. Continue the remaining main PDFs, giving priority to B1-01 and the pressure/injection, ship-conditioning and lifecycle papers used by Paper1. Each paper needs its own source-hash/page-anchored record covering all requested dimensions.
3. Check exact retained citation matches before seeking external sources. The B4-05→B3-11 edge is checked with partial support and a method-attribution conflict; this does not verify B3-11's own 25 references. Do not merge merely similar titles or versions.
4. External original papers, public supplements, code and errata remain pending under the user's request to wait for a Chrome connection. Local reading/reproduction can continue. Do not silently resume Firecrawl or direct public downloads.
5. Keep new diagnostic/reproduction artifacts separate from accepted Paper1 inputs. No disputed unit, guessed correction, missing stock boundary or unreproduced allocation becomes an operating/GHG input. Save verified checkpoints to the same GitHub branch.

Use `comprehensive_audit.py` to regenerate corpus/page registers and rendered review records. `audit_diagnostics.py`, `reproduce_ooi_cascade.py`, `audit_budiarto_fulltext.py` and `reproduce_zhang_lau_aquifers.py` perform explicitly limited diagnostics/component reproductions, separate from the accepted Paper1 model.
