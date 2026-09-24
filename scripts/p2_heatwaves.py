#!/usr/bin/env python3
"""Phase 2b: heatwave event detection.

Primary def: Tmax > DOY-local 95th percentile (+-7-day circular window, baseline
2000-2019) for >=3 consecutive days; events separated by <5 days are merged.
Sensitivities: pct90, absolute 35C x>=2d, Tmean pct95, heat-index pct95.

Outputs:
  data/processed/heatwave_mask_daily.nc
  data/processed/heatwave_events.csv      per-gridcell event catalog
  data/processed/heatwave_regional.csv    daily fraction in event per region
"""
import pathlib
import numpy as np
import pandas as pd
import xarray as xr
import yaml

ERA = pathlib.Path("data/raw/era5")
OUT = pathlib.Path("data/processed"); OUT.mkdir(parents=True, exist_ok=True)
cfg = yaml.safe_load(open("config/domain.yaml"))
BASE0, BASE1 = cfg["period"]["baseline_climatology"]

surf = xr.open_mfdataset(sorted(ERA.glob("surf_daily_*.nc")), combine="by_coords")
tmax, tmean = surf["tmax"].load(), surf["t2m"].load()
times = pd.DatetimeIndex(surf.time.values)
lat, lon = surf.latitude.values, surf.longitude.values
nt = len(times)
print("surf loaded", tmax.shape)

# ---- d2m for heat index ----
try:
    hyd = xr.open_mfdataset(sorted(ERA.glob("hydro_daily_*.nc")), combine="by_coords")
    d2m = hyd["d2m"].reindex(time=surf.time).load()
except Exception:
    d2m = None
    print("hydro unavailable -> heat-index def skipped")

base_mask = (times >= BASE0) & (times <= BASE1)
doys = times.dayofyear.values
doys_b = doys[base_mask]

def pct_mask(vals, pct):
    """vals (time,lat,lon) -> bool exceedance of DOY-window percentile."""
    base = vals[base_mask]
    thr = np.empty((366,) + vals.shape[1:])
    for day in range(1, 367):
        sel = (((doys_b - day) % 366) <= 7) | (((day - doys_b) % 366) <= 7)
        thr[day - 1] = np.nanpercentile(base[sel], pct, axis=0)
    return vals > thr[doys - 1]

print("masks...")
masks = {}
masks["pct95_tmax_3day"] = pct_mask(tmax.values, 95)
masks["pct90_tmax_3day"] = pct_mask(tmax.values, 90)
masks["pct95_tmean_3day"] = pct_mask(tmean.values, 95)
masks["abs_35C_2day"] = tmax.values >= 35.0

if d2m is not None:
    T = tmean.values
    Td = d2m.values
    es = 6.112 * np.exp(17.67 * T / (T + 243.5))
    e = 6.112 * np.exp(17.67 * Td / (Td + 243.5))
    RH = np.clip(100 * e / es, 0, 100)
    Tf = T * 9 / 5 + 32
    HI = (-42.379 + 2.04901523 * Tf + 10.14333127 * RH - 0.22475541 * Tf * RH
          - 6.83783e-3 * Tf ** 2 - 5.481717e-2 * RH ** 2
          + 1.22874e-3 * Tf ** 2 * RH + 8.5282e-4 * Tf * RH ** 2
          - 1.99e-6 * Tf ** 2 * RH ** 2)
    hi = (HI - 32) * 5 / 9
    hi_da = xr.DataArray(hi, dims=tmax.dims, coords=tmax.coords)
    masks["pct95_heatindex_3day"] = pct_mask(hi, 95)

msk = xr.Dataset({k: xr.DataArray(v, dims=tmax.dims, coords=tmax.coords)
                  for k, v in masks.items()})
msk.to_netcdf(OUT / "heatwave_mask_daily.nc")
print("masks saved", list(masks))

# ---- event runs per pixel: >= min_len days, merge gaps <5 ----
def pixel_events(m1d, min_len):
    d = np.diff(m1d.astype(np.int8))
    starts = list(np.where(d == 1)[0] + 1) + ([0] if m1d[0] else [])
    ends = list(np.where(d == -1)[0] + 1) + ([nt] if m1d[-1] else [])
    ev = list(zip(sorted(starts), sorted(ends)))
    merged = []
    for s, e in ev:
        if merged and s - merged[-1][1] < 5:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    return [(s, e) for s, e in merged if e - s >= min_len]

MIN_LEN = {"pct95_tmax_3day": 3, "pct90_tmax_3day": 3, "pct95_tmean_3day": 3,
           "abs_35C_2day": 2, "pct95_heatindex_3day": 3}

# baseline mean tmax for cumulative anomaly
anom = tmax.values - np.nanmean(tmax.values[base_mask], axis=0)

records = []
npix = len(lat) * len(lon)
for name, m in masks.items():
    m2 = m.reshape(nt, -1)
    ml = MIN_LEN[name]
    n_ev = 0
    for c in range(npix):
        for s, e in pixel_events(m2[:, c], ml):
            ila, ilo = divmod(c, m.shape[2])
            records.append({
                "definition": name, "lat": lat[ila], "lon": lon[ilo],
                "start": str(times[s].date()), "end": str(times[e - 1].date()),
                "ndays": e - s,
                "peak_tmax": float(np.nanmax(tmax.values[s:e, ila, ilo])),
                "cum_anomaly": float(np.nansum(anom[s:e, ila, ilo])),
                "year": times[s].year,
            })
            n_ev += 1
    print(name, "events:", n_ev, flush=True)
pd.DataFrame(records).to_csv(OUT / "heatwave_events.csv", index=False)

# regional daily fraction in event (primary def)
prim = masks["pct95_tmax_3day"]
frac = pd.DataFrame({"time": times, "domain_frac": prim.mean(axis=(1, 2))})
lat2 = lat[:, None] * np.ones((1, len(lon)))
lon2 = np.ones((len(lat), 1)) * lon[None, :]
for name, tr in cfg["transects"].items():
    pts = np.array(tr["vertices"])
    lonc, latc = pts[-1]
    m = (np.abs(lat2 - latc) <= 3.0) & (np.abs(lon2 - lonc) <= 3.0)
    frac[name] = prim[:, m].mean(axis=1)
frac.to_csv(OUT / "heatwave_regional.csv", index=False)
print("done", frac.shape)
