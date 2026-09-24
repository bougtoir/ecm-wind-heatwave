#!/usr/bin/env python3
"""Stream ERA5 (ARCO-ERA5) -> daily aggregates over Europe, MJJAS 2000-2021.

Primary store: ar/1959-2022-6h-240x121 (1.5 deg equiangular, 6-hourly, 13 PLs).
  -> surf_daily_YYYYMM.nc : t2m mean/max/min, msl, sp, tp(mm/d), tcwv, tcc, sst, u10, v10
  -> qflux_daily_YYYYMM.nc: Qx, Qy (kg m-1 s-1) daily mean, z500, t850
Supplement: co/single-level-reanalysis (reduced Gaussian) for swvl1-4, d2m (daily means
  at 6-hourly sampling), remapped nearest-neighbour to the 1.5 deg grid.
"""
import calendar, hashlib, json, pathlib, sys, time
import numpy as np
import xarray as xr

AR = "gs://gcp-public-data-arco-era5/ar/1959-2022-6h-240x121_equiangular_with_poles_conservative.zarr"
CO = "gs://gcp-public-data-arco-era5/co/single-level-reanalysis.zarr-v2"
LATB, LONB = (35.0, 72.0), (-15.0, 35.0)
YEARS, MONTHS = range(2000, 2022), [5, 6, 7, 8, 9]
OUT = pathlib.Path("data/raw/era5"); OUT.mkdir(parents=True, exist_ok=True)

def box(d):
    """Subset Europe on the 1.5deg grid (lat ascending, lon 0..360)."""
    lat = d.latitude.values
    lon = d.longitude.values
    la = lat[(lat >= LATB[0]) & (lat <= LATB[1])]
    lo = lon[((lon + 180) % 360 - 180 >= LONB[0]) & ((lon + 180) % 360 - 180 <= LONB[1])]
    return d.sel(latitude=la, longitude=lo)

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def save(ds, path):
    enc = {v: {"zlib": True, "complevel": 4, "dtype": "float32"} for v in ds.data_vars}
    ds.to_netcdf(path, encoding=enc)
    return path.stat().st_size, sha(path)

def month_surf(ds, t0, t1):
    s = lambda v: box(ds[v]).sel(time=slice(t0, t1)).load()
    t2m = s("2m_temperature") - 273.15
    out = xr.Dataset({
        "t2m_mean": t2m.resample(time="1D").mean(),
        "tmax": t2m.resample(time="1D").max(),
        "tmin": t2m.resample(time="1D").min(),
        "msl": s("mean_sea_level_pressure").resample(time="1D").mean(),
        "sp": s("surface_pressure").resample(time="1D").mean(),
        "tp": s("total_precipitation_6hr").resample(time="1D").sum() * 1000.0,  # m -> mm
        "tcwv": s("total_column_water_vapour").resample(time="1D").mean(),
        "tcc": s("total_cloud_cover").resample(time="1D").mean(),
        "sst": (s("sea_surface_temperature") - 273.15).resample(time="1D").mean(),
        "u10": s("10m_u_component_of_wind").resample(time="1D").mean(),
        "v10": s("10m_v_component_of_wind").resample(time="1D").mean(),
    })
    return out

def month_qflux(ds, t0, t1):
    lev = ds.level.values.astype(float)
    q = box(ds["specific_humidity"]).sel(time=slice(t0, t1)).load()
    u = box(ds["u_component_of_wind"]).sel(time=slice(t0, t1)).load()
    v = box(ds["v_component_of_wind"]).sel(time=slice(t0, t1)).load()
    sp = box(ds["surface_pressure"]).sel(time=slice(t0, t1)).load().transpose("time", "latitude", "longitude").values  # Pa
    p = lev * 100.0  # Pa
    dp = np.diff(p)  # (12,)
    # mask levels above local surface pressure: use q from level k only if p_k <= ps+50 hPa pad
    li = np.argsort(p)  # ascending pressure order required for integration
    qv, uv, vv = (a.transpose("time", "level", "latitude", "longitude").values[:, li]
                  for a in (q, u, v))
    psort = np.sort(p)
    dpv = np.diff(psort)[None, :, None, None]
    mask = psort[None, :, None, None] <= (sp[:, None, :, :] + 5000.0)  # keep levels near/below surface
    f = qv * uv * mask[:, :, :, :]
    g = qv * vv * mask[:, :, :, :]
    fmid = (f[:, :-1] + f[:, 1:]) / 2.0
    gmid = (g[:, :-1] + g[:, 1:]) / 2.0
    w = mask[:, :-1] | mask[:, 1:]
    qx = (fmid * dpv * w).sum(axis=1) / 9.81
    qy = (gmid * dpv * w).sum(axis=1) / 9.81
    z500 = box(ds["geopotential"]).sel(level=500, time=slice(t0, t1)).load() / 9.81
    t850 = box(ds["temperature"]).sel(level=850, time=slice(t0, t1)).load() - 273.15
    coords = {"time": q.time, "latitude": q.latitude, "longitude": q.longitude}
    out = xr.Dataset({
        "qx": xr.DataArray(qx, dims=("time", "latitude", "longitude"), coords=coords).resample(time="1D").mean(),
        "qy": xr.DataArray(qy, dims=("time", "latitude", "longitude"), coords=coords).resample(time="1D").mean(),
        "z500": z500.resample(time="1D").mean().drop_vars("level", errors="ignore"),
        "t850": t850.resample(time="1D").mean().drop_vars("level", errors="ignore"),
    })
    return out

def month_gauss(ds, t0, t1, idx):
    out = {}
    shape = idx["mask_idx"].shape
    for v in ["swvl1", "swvl2", "swvl3", "swvl4", "d2m"]:
        arr = ds[v].sel(time=slice(t0, t1))
        arr = arr.sel(time=arr.time.dt.hour.isin([0, 6, 12, 18]))
        arr = arr.isel(values=idx["mask_idx"].ravel())
        m = arr.resample(time="1D").mean()  # (day, npts)
        days = m.time
        out[v] = (m.values.reshape(-1, shape[0], shape[1]), days.values)
    return out

def gauss_index_map(ds):
    """Nearest Gaussian point index for each target 1.5deg cell."""
    from scipy.spatial import cKDTree
    lat = np.asarray(ds.latitude); lon = ((np.asarray(ds.longitude) + 180) % 360) - 180
    sel = (lat >= LATB[0] - 3) & (lat <= LATB[1] + 3) & (lon >= LONB[0] - 3) & (lon <= LONB[1] + 3)
    idx = np.where(sel)[0]
    tree = cKDTree(np.c_[lat[idx], lon[idx]])
    tlat = np.arange(LATB[0], LATB[1] + 1e-6, 1.5)
    tlon = np.arange(LONB[0], LONB[1] + 1e-6, 1.5)
    T = np.meshgrid(tlat, tlon, indexing="ij")
    _, j = tree.query(np.c_[T[0].ravel(), T[1].ravel()])
    return {"mask_idx": idx[j].reshape(T[0].shape), "tlat": tlat, "tlon": tlon}

def main():
    ledger = []
    ar = xr.open_zarr(AR, consolidated=True, storage_options={"token": "anon"})
    co = xr.open_zarr(CO, consolidated=True, storage_options={"token": "anon"})
    idx = gauss_index_map(co)
    for year in YEARS:
        for month in MONTHS:
            tag = f"{year}{month:02d}"
            f1, f2, f3 = OUT / f"surf_daily_{tag}.nc", OUT / f"qflux_daily_{tag}.nc", OUT / f"hydro_daily_{tag}.nc"
            t0 = f"{year}-{month:02d}-01"
            t1 = f"{year}-{month:02d}-{calendar.monthrange(year, month)[1]}"
            t = time.time()
            try:
                if not f1.exists():
                    s, h = save(month_surf(ar, t0, t1), f1)
                    ledger.append(dict(file=f1.name, bytes=s, sha256=h)); print(tag, "surf", flush=True)
                if not f2.exists():
                    s, h = save(month_qflux(ar, t0, t1), f2)
                    ledger.append(dict(file=f2.name, bytes=s, sha256=h)); print(tag, "qflux", flush=True)
                if not f3.exists():
                    m = month_gauss(co, t0, t1, idx)
                    days = m["swvl1"][1]
                    dso = xr.Dataset(
                        {v: (("time", "latitude", "longitude"), m[v][0]) for v in m},
                        coords={"time": days,
                                "latitude": idx["tlat"], "longitude": idx["tlon"]})
                    if "d2m" in dso: dso["d2m"] = dso["d2m"] - 273.15
                    s, h = save(dso, f3)
                    ledger.append(dict(file=f3.name, bytes=s, sha256=h)); print(tag, "hydro", flush=True)
            except Exception as e:
                print(tag, "ERROR", str(e)[:300], flush=True)
                ledger.append(dict(file=tag, error=str(e)[:300]))
    (OUT / "era5_ledger.json").write_text(json.dumps(ledger, indent=1))
    print("DONE")

if __name__ == "__main__":
    main()
