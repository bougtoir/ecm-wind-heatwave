#!/usr/bin/env python3
"""Phase 2a: moisture-transport reconstruction.

- Monthly Qx/Qy files (data/raw/era5/qflux_daily_*.nc) -> daily MFC = -div(Q)
  on the 1.5 deg lat-lon grid (spherical central differences).
- Transect flux F(t) = integral of Q . n ds along each config polyline.
Outputs:
  data/processed/mfc_daily.nc          (all MJJAS days, 2000-2021)
  data/processed/transect_flux_daily.csv
"""
import pathlib
import numpy as np
import pandas as pd
import xarray as xr
import yaml

ERA = pathlib.Path("data/raw/era5")
OUT = pathlib.Path("data/processed"); OUT.mkdir(parents=True, exist_ok=True)
cfg = yaml.safe_load(open("config/domain.yaml"))
R = 6371000.0
DEG = np.pi / 180.0

files = sorted(ERA.glob("qflux_daily_*.nc"))
print(len(files), "qflux files")
ds = xr.open_mfdataset(files, combine="by_coords", parallel=False)
qx, qy = ds["qx"], ds["qy"]
lat, lon = ds.latitude.values, ds.longitude.values

# --- MFC: -div Q, central differences on sphere (edges: one-sided) ---
dlon = np.gradient(lon) * DEG           # (nlon,)
dlat = np.gradient(lat) * DEG           # (nlat,)
coslat = np.cos(lat * DEG)              # (nlat,)
dqv_dlon = np.gradient(qx.values, axis=2) / dlon[None, None, :]          # dQx/dλ
dqv_dlat = np.gradient(qy.values, axis=1) / dlat[None, :, None]          # dQy/dφ
mfc = -(dqv_dlon / (R * coslat[None, :, None]) + dqv_dlat / R)           # kg m-2 s-1
ds["mfc"] = xr.DataArray(mfc, dims=("time", "latitude", "longitude"),
                         coords=ds.coords)
ds["mfc"].attrs.update(units="kg m-2 s-1", long_name="moisture flux convergence -div(Q)")
out = ds[["mfc", "qx", "qy", "z500", "t850"]]
enc = {v: {"zlib": True, "complevel": 4, "dtype": "float32"} for v in out.data_vars}
out.to_netcdf(OUT / "mfc_daily.nc", encoding=enc)
print("wrote mfc_daily.nc", dict(out.sizes))

# --- Transect fluxes ---
def seg_flux(qxd, qyd, verts):
    """Integrate Q.n ds along polyline using grid cells intersected by segments.
    Approximation: for each segment, sum Q·n over grid cells whose centres fall
    within half a cell of the segment, weighted by cell path length ds."""
    total = 0.0
    lonm, latm = np.meshgrid(lon, lat)
    for (x0, y0), (x1, y1) in zip(verts[:-1], verts[1:]):
        # segment vector and normal (pointing right of travel = toward continent)
        dxg, dyg = x1 - x0, y1 - y0
        L = np.hypot(dxg * 111.32 * np.cos(np.deg2rad((y0 + y1) / 2)), dyg * 110.57)  # km
        nx, ny = dyg, -dxg
        nn = np.hypot(nx, ny) or 1.0
        nx, ny = nx / nn, ny / nn
        # distance of each grid centre to the segment
        px, py = lonm - x0, latm - y0
        t = np.clip((px * dxg + py * dyg) / (dxg ** 2 + dyg ** 2), 0, 1)
        cx, cy = x0 + t * dxg, y0 + t * dyg
        dist = np.hypot((lonm - cx) * 111.32 * np.cos(np.deg2rad(latm)),
                        (latm - cy) * 110.57)  # km
        cell = 1.5 * 111.0  # grid cell ~ 167 km
        w = np.clip(1.0 - dist / (cell / 2), 0, None)
        if w.sum() == 0:
            continue
        w /= w.sum()
        qn = (qxd * nx + qyd * ny * np.cos(np.deg2rad(latm)))   # local normal component
        total += float((w * qn).sum()) * L * 1000.0            # kg s-1 (flux per transect)
    return total

records = []
qxa, qya = ds["qx"].values, ds["qy"].values
times = pd.DatetimeIndex(ds.time.values)
for ti in range(len(times)):
    row = {"time": times[ti]}
    for name, tr in cfg["transects"].items():
        row[name] = seg_flux(qxa[ti], qya[ti], tr["vertices"])
    records.append(row)
    if ti % 500 == 0:
        print("transect", ti, flush=True)
tf = pd.DataFrame(records)
tf.to_csv(OUT / "transect_flux_daily.csv", index=False)
print("wrote transect_flux_daily.csv", tf.shape)
