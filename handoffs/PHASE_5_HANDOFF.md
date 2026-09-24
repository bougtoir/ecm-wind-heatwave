# PHASE 5 HANDOFF — Deployment quasi-experiment

## Products
- `data/processed/panel_cellyear.csv` — cell × year (2000–2021) panel
- `results/phase5_twfe.csv` — two-way FE (cell+year), HAC + cell-cluster + 500× year-block bootstrap
- `results/phase5_eventstudy.csv` — first-treatment event study (±5 yr), never-treated control

## Headline
- TWFE: hw_days +2.9e-4 d/MW (p=0.32 HAC), tmax_anom +6.8e-5 C/MW (p=0.05 HAC; cluster p<1e-3; bootstrap p=0.64) — statistically fragile, small.
- Event study: no clear post-treatment divergence; estimates hover around zero.
