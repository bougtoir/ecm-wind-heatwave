# Data sources and provenance (Phase 1)

All raw files are persisted under `data/raw/` (never `/tmp`); derived artifacts under
`data/interim/` / `data/processed/`. Per-file SHA-256 and byte sizes are recorded in
`data/raw/acquisition_ledger.csv` (static downloads) and
`data/interim/era5/era5_ledger.json` (ERA5 monthly NetCDF outputs).
UTC timestamps below are acquisition times (UTC).

## Atmospheric reanalysis — ERA5 via Google ARCO (CC-BY-4.0)

Source: `gs://gcp-public-data-arco-era5` (public, anonymous GCS access; ERA5 ©
Copernicus C3S / ECMWF, CC-BY-4.0).

Two stores are used (decision documented in `docs/COMPUTE_BUDGET.md`):

| Store | Grid | Used for |
|---|---|---|
| `ar/1959-2022-6h-240x121_equiangular_with_poles_conservative.zarr` | 1.5° equiangular, 6-hourly, 13 pressure levels (50–1000 hPa) | t2m (mean/max/min), msl/sp, total precipitation, tcwv, tcc, sst, u10/v10, moisture flux q·u / q·v (Q_x, Q_y trapezoidal vertical integral with surface-pressure mask), z500, t850 |
| `co/single-level-reanalysis.zarr-v2` | N320 reduced Gaussian (~31 km), 1-hourly | swvl1–4 (soil moisture), d2m — remapped to the 1.5° target grid by cKDTree nearest neighbour |

Outputs: daily-resolution monthly NetCDF files in `data/interim/era5/`
(`surf_daily_YYYYMM.nc`, `qflux_daily_YYYYMM.nc`, `hydro_daily_YYYYMM.nc`),
May–Sep (MJJAS) 2000–2021. Q_x, Q_y in kg m⁻¹ s⁻¹; MFC computed downstream in
Phase 2 as −∇·Q on the 1.5° grid.

**Store coverage limits (verified live 2026-09-24):** `ar` ends 2021-12-31T18Z;
`co` single-level ends ~2021-08-31 → the canonical analysis period is MJJAS
2000–2021; soil-moisture/d2m for Sep 2021 is unavailable (flagged by QC).
Variables NOT in ARCO (evaporation, surface fluxes sshf/slhf, PBLH) are
unavailable; the H4 energy-partition hypothesis is assessed with proxy
variables (swvl, precipitation, RH/d2m-depression). Documented as a limitation.

## Wind-turbine deployment

| File | Source | Licence | Coverage |
|---|---|---|---|
| `data/raw/turbines/20260127_eww_opendatabase.csv` | Offshore wind-turbine open database (Zenodo rec. 19879819), retrieved 2026-09-24 | CC-BY-4.0 | European offshore farms: lat/lon, rated power, rotor diameter, hub height, commissioning date |
| `data/raw/turbines/dk_stamdataregister.xls` | Danish Energy Agency, Stamdataregister (Wind turbine register) | public | Danish turbines: location, capacity, commissioning |
| `data/raw/turbines/Gesamtdatenexport_20260924.zip` | Marktstammdatenregister (MaStR) full export 26.1, `download.marktstammdatenregister.de` | public (DL-DE-BY) | German installations incl. wind units: coordinates, capacity, commissioning date |
| `data/raw/turbines/osm/{CC}.csv` | OpenStreetMap via Overpass API (`generator:source=wind`), mirrors `overpass.osm.ch`, `maps.mail.ru`, `overpass.private.coffee` | ODbL | Supplementary turbine points for countries without a machine-readable register |

Rationale: the Global Energy Monitor wind tracker download endpoint was removed
(HTTP 410) and its API does not expose wind assets; national registers + OSM
provide equivalent or better coverage for the exposure reconstruction.
Tier-1 exposure series uses the registers (official commissioning dates);
OSM fills gaps and is cross-checked against registers.

## Electricity demand and generation — OPSD

`data/raw/electricity/opsd_time_series_60min_2020.csv`
Open Power System Data time-series release 2020-10-06 (CC-BY-4.0).
Hourly 2015–2020: `XX_load_actual_entsoe_transparency`,
`XX_wind_{onshore,offshore}_generation_actual`, day-ahead prices, capacity.
ENTSO-E Transparency API requires credentials not available in this
environment; OPSD is the documented fallback (see `docs/COMPUTE_BUDGET.md`).
Demand model (Phase 8) therefore covers 2015–2020, a subset of the
meteorological analysis period — limitation documented.
