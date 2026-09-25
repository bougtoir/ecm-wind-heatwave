# Revision changelog — targeted ECM revision
| # | Type | Defect | Files | Action | Before | After | Status |
|---|------|--------|-------|--------|--------|-------|--------|
| 1 | TYPE4 | Demand slopes fragile (neg OOS R2) feeding WERR | scripts/r1_demand.py, r1_werr.py, results/demand_*, werr_* | M0 reproduced; M1 covariate-enriched + blocked CV; M2 EB shrinkage for unstable slopes; MC propagation of slope+beta SEs; pooled WERR -0.036 [-0.067,-0.007] (was -0.029); fragile countries (IE 1.22->0.43, NL 0.34->0.13) shrink; CIs widen honestly | done |
| 2 | TYPE3 | OSM undated chronology | scripts/r2_exposure.py | variants A/B/C recomputed with identical kernel; North-Sea positives robust; FR flips + under dated-only; Iberia loses signal without OSM; domain robust negative | done |
| 3 | TYPE3 | falsification count wording | manuscript, docs | battery corrected to "11 executed checks + 1 infeasible off-season control"; max analog SMD 0.27 reported | done |
| 4 | TYPE1 | unresolved f-string literal, stale counts | build_manuscript.py, p12_qc.py | literal removed; single canonical event count (3,017); QC reads canonical WERR CSV | done |
| 5 | TYPE1 | causal wording | manuscript | "association-implied"/"associated with"; WRF designed-not-executed | done |
| 6 | TYPE1 | reference defects | references_verified.csv, build_manuscript.py | lundquist DOI->underlying article; volker->peer-reviewed GMD; rosenbaum1983 added; callaway to D3 | done |
| 7 | TYPE1 | ECM compliance | highlights.txt, docx | highlights <=85 chars; requirements doc refreshed | done |
| 8 | TYPE2 | bundles + clean test | ECM_*.zip | submission + reproducibility zips; clean clone build PASS | done |

## Finishing pass (2026-09-25, r3)
- Devin Review fixes: demand bootstrap restricted to training years with
  duplicate month resampling (np.isin dedupe bug); pooled MC now draws shared
  region coefficients once per replicate (r1_werr.py); Makefile acquire now
  includes dl_static_sources (registers/OPSD), extract_osm_wind, parse_mastr;
  submission artifacts re-synced and zip hash-verified.
- Implied ΔT verified against canonical files; manuscript states regional
  medians (+1.8/+2.0/+1.4 °C North-Sea corridors, -0.6 Iberia, -1.9 domain,
  ~0 France); bare "small" removed.
- "validated demand model" wording replaced; §2.7 now documents bootstrap,
  instability rule, EB shrinkage (mu, tau2, formula, affected countries,
  WERR-independence). Table 3 exposes CV/test R².
- "11-check falsification battery" renamed falsification-and-sensitivity
  battery; machine-readable inventory added (results/falsification_inventory.csv).
- ECM_submission_FINAL.zip + ECM_reproducibility_bundle_FINAL.zip built.
