# PHASE 7 HANDOFF — Numerical counterfactuals (WRF)

## Status: NOT RUN on this VM (by design)

- Compute requirement ~68k core-hours / ~29 TB — exceeds the 2-vCPU VM by >100x
  (see docs/COMPUTE_BUDGET.md). Constraint honored: production-ready configs only.
- Deliverables: wrf/namelist.wps, wrf/namelist.input (d01 27 km + d02 9 km, YSU PBL,
  Thompson MP, RRTMG rad, Noah LSM, windfarm_opt=1 Fitch scheme),
  wrf/scenarios.md (S0/S50/S100/S150/S150u/S150d x 4 events x 3 perturbed ICs),
  wrf/gen_windturbines.py (scenario placement from data/processed/turbines.csv).
- Observational Phases 3–6 stand in as the empirical substitute; manuscript
  presents the WRF suite as a preregistered counterfactual design + limitation.
