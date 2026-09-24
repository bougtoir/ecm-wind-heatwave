#!/usr/bin/env python3
"""Phase 2c/5-prep: turbine deployment + WFI exposure fields.

1. data/processed/capacity_annual.csv  -- MW active per country-year (2000-2021)
2. data/processed/capdensity_YYYY.nc   -- MW per 1.5deg cell, cumulative active
3. data/processed/wfi_daily.csv        -- per-region daily WFI exposure series
4. data/processed/wfi_grid_daily.nc    -- WFI on the 1.5deg grid (float32)

WFI(x,t) = sum_j Cap_j(year(t)) * exp(-d_j/100km) sampled at 50km steps along the
UPSTREAM back-trajectory of the daily mean 10m wind at x (6 steps = 300 km).
Sampling upstream yields the downwind-interception weighting without an
O(turbines x pixels x days) product.
"""
import pathlib
import numpy as np
import pandas as pd
import xarray as xr
import yaml
from scipy.interpolate import RegularGridInterpolator
from scipy.spatial import cKDTree

OUT = pathlib.Path("data/processed"); OUT.mkdir(parents=True, exist_ok=True)
ERA = pathlib.Path("data/raw/era5")
cfg = yaml.safe_load(open("config/domain.yaml"))

tb = pd.read_csv(OUT / "turbines.csv")
tb["year"] = pd.to_datetime(tb["commissioning"], errors="coerce").dt.year
# capacity imputation for missing values: country median, else global median
med_cc = tb.groupby("country").capacity_mw.transform("median")
tb["capacity_mw"] = tb.capacity_mw.fillna(med_cc).fillna(tb.capacity_mw.median())
print("turbines", len(tb), "| with year:", tb.year.notna().sum())

import sys
sys.path.insert(0, "scripts")
from grid_utils import canon

surf = xr.open_mfdataset(sorted(ERA.glob("surf_daily_*.nc")), combine="by_coords")
_u10, _v10 = canon(surf["u10"]).load(), canon(surf["v10"]).load()
lat, lon = _u10.latitude.values, _u10.longitude.values
times = pd.DatetimeIndex(_u10.time.values)
lat2, lon2 = np.meshgrid(lat, lon, indexing="ij")
YEARS = range(2000, 2022)

# ---- capacity density per year on the 1.5deg grid ----
grid_pts = np.c_[lat2.ravel(), lon2.ravel()]
tree = cKDTree(grid_pts)
dated = tb.dropna(subset=["year"]).copy()
dated["year"] = dated["year"].astype(int)
# static background: undated OSM turbines (commissioning unknown)
undated = tb[tb.year.isna() & (tb.source == "osm")]
static = np.zeros(len(grid_pts))
if len(undated):
    _, ii = tree.query(np.c_[undated.lat, undated.lon])
    np.add.at(static, ii, undated.capacity_mw.values)
static = static.reshape(lat2.shape)
cap = {}
for y in YEARS:
    act = dated[(dated.year <= y) & (dated.capacity_mw > 0)]
    d = np.zeros(len(grid_pts))
    if len(act):
        _, ii = tree.query(np.c_[act.lat, act.lon])
        np.add.at(d, ii, act.capacity_mw.values)
    cap[y] = d.reshape(lat2.shape) + static   # + background layer
    da = xr.DataArray(cap[y], dims=("lat", "lon"), coords={"lat": lat, "lon": lon})
    da.to_netcdf(OUT / f"capdensity_{y}.nc")
# annual table (needs country mapping - use nearest-country of turbine's own cc col)
ann = dated.groupby(["year", "country"]).capacity_mw.sum().unstack(fill_value=0)
ann = ann.reindex(YEARS, fill_value=0).cumsum()
ann.to_csv(OUT / "capacity_annual.csv")
print("capacity_annual done")

# ---- daily WFI ----
u10 = _u10.values  # (time,lat,lon) m/s
v10 = _v10.values
nt = len(times)
nlat, nlon = len(lat), len(lon)
KM_DEG_LAT = 110.57
coslat = np.cos(np.deg2rad(lat2))
kmx = 111.32 * coslat  # km per deg lon at each cell

# interpolator per year is created on demand (year changes rarely)
interp = None
cy = None
wfi = np.zeros((nt, nlat, nlon), dtype=np.float32)
steps = np.arange(1, 7) * 50.0  # km upstream
weights = np.exp(-steps / 100.0)

for ti in range(nt):
    y = times[ti].year
    if y != cy:
        interp = RegularGridInterpolator(
            (lat, lon), cap[y], bounds_error=False, fill_value=0.0)
        cy = y
    ux, vy = u10[ti], v10[ti]
    spd = np.hypot(ux, vy) + 1e-6
    # upstream unit vector components in km-space
    dirx, diry = -ux / spd, -vy / spd
    acc = np.zeros((nlat, nlon))
    for s, wt in zip(steps, weights):
        plat = lat2 + diry * s / KM_DEG_LAT
        plon = lon2 + dirx * s / kmx
        acc += wt * interp(np.c_[plat.ravel(), plon.ravel()]).reshape(plat.shape)
    wfi[ti] = acc
    if ti % 500 == 0:
        print("wfi", ti, times[ti].date(), flush=True)

ds = xr.Dataset({"wfi": xr.DataArray(wfi, dims=("time", "lat", "lon"),
                                     coords={"time": times, "lat": lat, "lon": lon})})
ds["wfi"].attrs.update(units="MW", long_name="upwind-capacity exposure (WFI kernel)")
enc = {"wfi": {"zlib": True, "complevel": 4, "dtype": "float32"}}
ds.to_netcdf(OUT / "wfi_grid_daily.nc", encoding=enc)

# region daily means: domain + transect downstream boxes
rows = {"time": times}
rows["domain"] = wfi.mean(axis=(1, 2))
for name, tr in cfg["transects"].items():
    lonc, latc = np.array(tr["vertices"])[-1]
    m = (np.abs(lat2 - latc) <= 3.0) & (np.abs(lon2 - lonc) <= 3.0)
    rows[name] = wfi[:, m].mean(axis=1)
pd.DataFrame(rows).to_csv(OUT / "wfi_daily.csv", index=False)
print("done")
