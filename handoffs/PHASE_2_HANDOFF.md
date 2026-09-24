# PHASE 2 HANDOFF — Moisture transport + heatwave products

## Products (data/processed/)
- `mfc_daily.nc` — MFC=-div(Q), qx, qy (kg/m/s), z500, t850; 3366 days × 25×34 grid, canonical (time, lat, lon −180..180)
- `transect_flux_daily.csv` — daily Q·n (kg/s) across 5 configured transects
- `heatwave_mask_daily.nc` — 5 definitions (pct95_tmax_3day primary; pct90, pct95_tmean, abs35C_2day, pct95_heatindex)
- `heatwave_events.csv` — 105,441 pixel-level events catalog
- `heatwave_regional.csv` — daily fraction-in-event per region + domain
- `capdensity_YYYY.nc`, `capacity_annual.csv` — cumulative MW per cell/year
- `wfi_grid_daily.nc`, `wfi_daily.csv` — upstream-capacity exposure (50 km steps ×6, exp(−d/100km))

## Method notes
- MFC via central differences on the sphere (gradient per axis / R cosφ)
- Baseline percentiles: DOY ±7-day circular window over 2000–2019
- Events: ≥ min days, merged across <5-day gaps; per-pixel catalog
- Grid normalization bug found & fixed: surf files native (time, lon, lat) with 0–360° lons; `grid_utils.canon()` applied in every script; transect fluxes recomputed (non-zero, ~10^7 kg/s scale)
