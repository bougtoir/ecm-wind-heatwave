# PHASE 3 HANDOFF — Observational panel + event composites

## Products
- `data/processed/panel_daily.csv` — 3366×54 regional daily panel (tmax_anom, hwfrac, wfi, mfc, z500/slp/tcwv anom, sst)
- `results/phase3_panel_regression.csv` — tmax_anom ~ wfi + controls, Newey-West(14) + 200× 14d circular block bootstrap
- `results/phase3_event_composites.csv` — transect flux/MFC composites, lags −10..+5

## Headline (interim, see Phase 6 for falsification)
- Regional β_wfi (°C per MW exposure): +3.7e-4..+5.5e-4 C/MW on North-Sea corridors (p<0.001 FDR-significant); ~0 France; negative Iberia/domain.
- Directionally consistent with downwind warming signal on strong offshore corridors, spatially heterogeneous.
