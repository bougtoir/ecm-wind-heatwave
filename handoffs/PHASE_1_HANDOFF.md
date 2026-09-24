# PHASE 1 HANDOFF — Data acquisition + QC

## Status: COMPLETE (QC pending p1_qc.py run)

## Datasets acquired (ledger: docs/data_sources.md)

### ERA5 (ARCO-ERA5 zarr, anonymous GCS, no API key)
- Primary store `ar/1959-2022-6h-240x121_equiangular_with_poles_conservative.zarr`
  (1.5°, 6-hourly, 13 pressure levels 100–1000 hPa).
- Box: lat 36–72 °N, lon −15–34.5 °E; period MJJAS 2000-05-01 → 2021-09-30.
- Outputs `data/raw/era5/`:
  - `surf_daily_YYYYMM.nc` — t2m_mean, tmax, tmin, msl, sp, tp, tcwv, tcc, sst, u10, v10
  - `qflux_daily_YYYYMM.nc` — vertically-integrated qx, qy (kg m⁻¹ s⁻¹), z500, t850
  - `hydro_daily_YYYYMM.nc` — d2m, swvl1–4 (Gaussian N320 remapped by cKDTree)
- 331 monthly files, ~2.5 GB. Verified: no NaN-excess, no time gaps.

### Turbine registers (140,010 units)
| source | n | notes |
|---|---|---|
| eww (empress.ewww.com.cn open db, offshore) | 6,544 | commissioned dates 98.6% |
| DK Stamdataregisteret | 7,614 | official register, UTM32→WGS84 |
| MaStR (BNetzA) | 42,277 | DE register, in-service status 35 |
| OSM (Geofabrik pbf, 16 countries) | 83,575 | dedupe vs registers @150 m; only ~3% dated |
- `data/processed/turbines.csv`; capacity imputation for missing = country median.
- Exposure design: dated turbines → time-varying density; undated OSM → static
  background layer (conservative, inflates early exposure → attenuates trend).
  Documented limitation: ~97% of OSM units lack commissioning dates.

### Electricity
- OPSD time_series_60min_2020.csv: hourly load + wind generation, 2015–2020,
  ~25 European countries (ENTSO-E transparency columns).

## Decisions / caveats for later phases
- ERA5 ends 2021-12-31 in ARCO-1.5° store → analysis period capped at 2021.
- surf files store dims (time, longitude, latitude) with 0–360 lons —
  `scripts/grid_utils.canon()` normalizes every array to
  (time, latitude, longitude) with lon ∈ [−180,180); applied in all analysis scripts.
- OSM capacity strings were unit-mixed (kW/MW/GW/W); parser in build_turbines.py
  normalizes to MW (verified: OSM total ≈ 133 GW vs ~200 GW European installed —
  consistent with OSM undercoverage).
- Overpass API abandoned (406/504/empty); Geofabrik pbf deterministic download.

## Next: PHASE 2 products already partially built in parallel
(mfc_daily.nc, transect_flux_daily.csv, heatwave masks/events done;
capdensity/wfi running at handoff write time)
