# PHASE 9 HANDOFF — WERR estimate

## Method
Per event: dT_att = β_region(Phase3) × WFI_region(event mean); ΔE_heat = slope_country(Phase8) × dT_att × 24h × ndays; WERR = ΔE_heat / E_wind (actual OPSD wind generation, 2015–2020 events).

## Products
- `results/phase9_werr_events.csv` (3,254 events), `results/phase9_werr_summary.csv`

## Headline (signed estimates, bootstrap CI)
- Pooled ALL: WERR = −0.028 [−0.039, −0.018] — i.e., no detectable positive rebound at aggregate level; pooled sign slightly negative.
- Positive on North-Sea corridors: BE +0.11, NL +0.34, DK +0.05, DE +0.010; IE +1.2 (tiny E_wind denominator — flagged fragile).
- Negative/null: FR ≈ 0, ES −0.026, PT −0.030, IT −0.046, GB 0 (slope=0).
- Interpretation: meteorological rebound is spatially heterogeneous, small, and not robustly positive; does NOT confirm the headline hypothesis at aggregate scale.
