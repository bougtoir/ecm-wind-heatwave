# VALIDATION REPORT (GATE 6, 2026-10-17)

Same VM, clean downstream build order executed:
`p9b_country_day_werr.py` → `make figures` (unchanged inputs →
bit-identical figs) → `build_manuscript.py` → `build_cover_letter.py`
→ `make_graphical_abstract.py` → `numeric_provenance.py` → `p12_qc.py`
→ pytest.

## Results
| Check | Result |
|---|---|
| p9b run | 2,362 country-days, 13 countries, 0 zero-denominator exclusions |
| pytest tests/test_smoke.py | 3/3 PASS |
| p12_qc.py | 13/13 PASS (abstract 250 w ≤250, 30/30 refs, figs 1–8 cited, 8 figs + 4 tables ≤15, no placeholder refs, declarations present) |
| Mutation test WERR_CD→0.999 | propagated to manuscript/cover letter/highlights ✓ (canonical restored; disposable copy deleted) |
| NUMERIC_PROVENANCE.csv | 635 tokens classified, all matched/verified |
| Recompute spot checks | country sums, pooled −0.0355, WERR_CD 0.0009 — match canonical |
| ZIP integrity | both zips testzip-clean; manifests verified |

## Not claimed
Full raw-data re-acquisition (ERA5/OPSD/OSM/MaStR) is NOT re-run — this
is cached-input reproduction. WRF suite still not executed. Off-season
falsification still infeasible on the MJJAS archive.
