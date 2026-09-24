# Revision changelog — targeted ECM revision
| # | Type | Defect | Files | Action | Before | After | Status |
|---|------|--------|-------|--------|--------|-------|--------|
| 1 | TYPE4 | Demand slopes fragile (neg OOS R2) feeding WERR | scripts/r1_demand.py, r1_werr.py, results/demand_*, werr_* | M0 reproduced; M1 covariate-enriched + blocked CV; M2 EB shrinkage for unstable slopes; MC propagation of slope+beta SEs; pooled WERR -0.036 [-0.067,-0.007] (was -0.029); fragile countries (IE 1.22->0.43, NL 0.34->0.13) shrink; CIs widen honestly | done |
| 2 | TYPE3 | OSM undated chronology | scripts/r2_exposure.py | variants A/B/C recomputed with identical kernel; North-Sea positives robust; FR flips + under dated-only; Iberia loses signal without OSM; domain robust negative | done |
