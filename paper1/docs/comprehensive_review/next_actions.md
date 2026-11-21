# Continuation queue

The comprehensive audit is active and unfinished. Current coverage is generated in [README](README.md); the complete pending-paper list is in [papers.csv](../../outputs/comprehensive_review/papers.csv). Prior targeted reviews do not count as exhaustive completion.

1. Read B4-06 in full, inspect all rendered pages and reconcile its model equations/claims with the retained Budiarto supplementary DOCX and existing rounded-schedule replay. Identify every additional model input required for independent optimisation. Preserve blank cells and rounded quantities.
2. Continue the remaining main PDFs, giving priority to B1-01 and the pressure/injection, ship-conditioning and lifecycle papers used by Paper1. Each paper needs its own source-hash/page-anchored record covering all requested dimensions.
3. Check exact retained citation matches before seeking external sources. The B4-05→B3-11 edge is checked with partial support and a method-attribution conflict; this does not verify B3-11's own 25 references. Do not merge merely similar titles or versions.
4. External original papers, public supplements, code and errata remain pending under the user's request to wait for a Chrome connection. Local reading/reproduction can continue. Do not silently resume Firecrawl or direct public downloads.
5. Keep new diagnostic/reproduction artifacts separate from accepted Paper1 inputs. No disputed unit, guessed correction, missing stock boundary or unreproduced allocation becomes an operating/GHG input. Save verified checkpoints to the same GitHub branch.

Use `comprehensive_audit.py` to regenerate the corpus/page registers and rendered review records. Use `audit_diagnostics.py` for the first three papers' limited checks and `reproduce_ooi_cascade.py` for the independent service-cascade reconstruction and literal allocation diagnostics. These scripts are distinct from the main Paper1 model.
