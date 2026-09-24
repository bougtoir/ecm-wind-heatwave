#!/usr/bin/env python3
"""Phase 3: observational event/panel analysis.

Builds a daily regional panel (2000-2021 MJJAS) per region:
  outcome : regional Tmax anomaly, heatwave-day fraction
  exposure: WFI (upwind-capacity kernel)
  controls: z500, SLP, SST, TCWV, MFC anomalies, DOY, year
Outputs:
  data/processed/panel_daily.csv
  results/phase3_panel_regression.csv   (OLS + Conley-HAC + block bootstrap)
  results/phase3_event_composites.csv
"""
import pathlib
import numpy as np
import pandas as pd
import xarray as xr
import yaml

P = pathlib.Path("data/processed"); R = pathlib.Path("results"); R.mkdir(exist_ok=True)
ERA = pathlib.Path("data/raw/era5")
cfg = yaml.safe_load(open("config/domain.yaml"))

import sys
sys.path.insert(0, "scripts")
from grid_utils import canon

surf = xr.open_mfdataset(sorted(ERA.glob("surf_daily_*.nc")), combine="by_coords")
tmx = canon(surf["tmax"]).load()
lat, lon = tmx.latitude.values, tmx.longitude.values
times = pd.DatetimeIndex(tmx.time.values)
lat2, lon2 = np.meshgrid(lat, lon, indexing="ij")

wfi_ds = xr.open_dataset(P / "wfi_grid_daily.nc")
tf = pd.read_csv(P / "transect_flux_daily.csv", parse_dates=["time"])
msk = xr.open_dataset(P / "heatwave_mask_daily.nc")
mfc_ds = xr.open_dataset(P / "mfc_daily.nc")

REGIONS = {"domain": None}
latm = lat2.ravel(); lonm = lon2.ravel()
for name, tr in cfg["transects"].items():
    lonc, latc = np.array(tr["vertices"])[-1]
    REGIONS[name] = (np.abs(lat2 - latc) <= 3.0) & (np.abs(lon2 - lonc) <= 3.0)

def rmean(da3, m):
    v = da3.values if hasattr(da3, "values") else da3
    return (np.nanmean(v[:, m], axis=1) if m is not None
            else np.nanmean(v, axis=(1, 2)))

# climatological anomalies (baseline)
base = (times >= "2000-01-01") & (times <= "2019-12-31")
def anom(v):
    return v - np.nanmean(v[base], axis=0)

rows = {"time": times}
wf = wfi_ds["wfi"].values
mf = mfc_ds["mfc"].values
z5 = mfc_ds["z500"].values
hw = msk["pct95_tmax_3day"].values
tm = tmx.values
sl = canon(surf["msl"]).reindex_like(tmx).values
tw = canon(surf["tcwv"]).reindex_like(tmx).values
ss = canon(surf["sst"]).reindex_like(tmx).values

for rname, m in REGIONS.items():
    rows[f"{rname}__tmax_anom"] = anom(rmean(tm, m)) if m is not None else anom(tm.mean(axis=(1,2)))
    rows[f"{rname}__hwfrac"] = rmean(hw, m)
    rows[f"{rname}__wfi"] = rmean(wf, m)
    rows[f"{rname}__mfc"] = rmean(mf, m)
    rows[f"{rname}__z500_anom"] = anom(rmean(z5, m))
    rows[f"{rname}__slp_anom"] = anom(rmean(sl, m))
    rows[f"{rname}__tcwv_anom"] = anom(rmean(tw, m))
    rows[f"{rname}__sst"] = rmean(ss, m)

panel = pd.DataFrame(rows).merge(tf, on="time", how="left")
panel.to_csv(P / "panel_daily.csv", index=False)
print("panel", panel.shape)

# ---- regression: regional tmax_anom ~ wfi + controls ----
import statsmodels.api as sm

def conley_se(y, Xdf, latv, lonv, cutoff_km=250):
    """Spatial-HAC (Conley) with Bartlett kernel on pixel-weighted design.
    Here regions are single aggregate series -> fall back to Newey-West lag=14.
    """
    X = sm.add_constant(Xdf)
    mdl = sm.OLS(y, X, missing="drop")
    return mdl.fit(cov_type="HAC", cov_kwds={"maxlags": 14})

res = []
for rname in REGIONS:
    d = panel.copy()
    y = d[f"{rname}__tmax_anom"]
    X = pd.DataFrame({
        "wfi": d[f"{rname}__wfi"],
        "z500": d[f"{rname}__z500_anom"], "slp": d[f"{rname}__slp_anom"],
        "tcwv": d[f"{rname}__tcwv_anom"], "sst": d[f"{rname}__sst"],
        "doy_sin": np.sin(2 * np.pi * d.time.dt.dayofyear / 365.25),
        "doy_cos": np.cos(2 * np.pi * d.time.dt.dayofyear / 365.25),
        "year": d.time.dt.year,
    })
    X = X.dropna(axis=1)            # drop all-NaN controls (e.g. sst)
    fit = conley_se(y, X, None, None)
    res.append({"region": rname, "coef_wfi": fit.params.get("wfi", np.nan),
                "se": fit.bse.get("wfi", np.nan), "p": fit.pvalues.get("wfi", np.nan),
                "n": int(fit.nobs), "r2": fit.rsquared})
    # block bootstrap (14d circular)
    rng = np.random.default_rng(cfg["random_seed"])
    nb = len(d) // 14
    boot = []
    yv = y.values; Xv = X.values
    Xm = sm.add_constant(Xv)
    for b in range(200):
        start = rng.integers(0, len(d), nb)
        idx = np.concatenate([np.arange(s, s + 14) % len(d) for s in start])
        try:
            beta = np.linalg.lstsq(Xm[idx], yv[idx], rcond=None)[0][1]
            boot.append(beta)
        except Exception:
            pass
    res[-1]["boot_se"] = float(np.std(boot))
    res[-1]["boot_p"] = float(2 * min((np.array(boot) <= 0).mean(),
                                    (np.array(boot) >= 0).mean()))
pd.DataFrame(res).to_csv(R / "phase3_panel_regression.csv", index=False)
print(pd.DataFrame(res))

# ---- event composites: transect flux + MFC anomalies around regional events ----
comp = []
hwf = pd.read_csv(P / "heatwave_regional.csv", parse_dates=["time"])
for rname in cfg["transects"]:
    ev = panel.loc[panel[f"{rname}__hwfrac"] > 0.05, "time"]
    for lag in range(-10, 6):
        m = panel.time.isin(ev - pd.Timedelta(days=lag))
        comp.append({"region": rname, "lag": lag,
                     "transect_flux": panel.loc[m, rname].mean(),
                     "mfc": panel.loc[m, f"{rname}__mfc"].mean(),
                     "n": int(m.sum())})
pd.DataFrame(comp).to_csv(R / "phase3_event_composites.csv", index=False)
print("done")
