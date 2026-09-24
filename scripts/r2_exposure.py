#!/usr/bin/env python3
"""R2: exposure-chronology sensitivity.

WFI is linear in the capacity layer, so:
  A (current)  = dated_all + static_undated_OSM      [existing wfi_daily.csv]
  B (dated)    = A - S    (S = WFI from static layer alone)
  C (registry) = dated non-OSM only

We recompute ONLY the regional daily-mean WFI for S and for the non-OSM
dated layer, restricted to region mask cells (exact same kernel/winds),
then refit the Phase-3 regional regression spec per variant.

Outputs: results/exposure_chronology_sensitivity.csv, docs/EXPOSURE_SENSITIVITY.md
"""
import pathlib, sys
import numpy as np
import pandas as pd
import xarray as xr
import yaml
import statsmodels.api as sm
from scipy.interpolate import RegularGridInterpolator
from scipy.spatial import cKDTree

sys.path.insert(0, "scripts")
from grid_utils import canon

P = pathlib.Path("data/processed"); R = pathlib.Path("results")
ERA = pathlib.Path("data/raw/era5")
cfg = yaml.safe_load(open("config/domain.yaml"))

tb = pd.read_csv(P / "turbines.csv")
tb["year"] = pd.to_datetime(tb["commissioning"], errors="coerce").dt.year
med_cc = tb.groupby("country").capacity_mw.transform("median")
tb["capacity_mw"] = tb.capacity_mw.fillna(med_cc).fillna(tb.capacity_mw.median())

surf = xr.open_mfdataset(sorted(ERA.glob("surf_daily_*.nc")), combine="by_coords")
u10, v10 = canon(surf["u10"]).load(), canon(surf["v10"]).load()
lat, lon = u10.latitude.values, u10.longitude.values
times = pd.DatetimeIndex(u10.time.values)
lat2, lon2 = np.meshgrid(lat, lon, indexing="ij")
grid_pts = np.c_[lat2.ravel(), lon2.ravel()]
tree = cKDTree(grid_pts)

undated = tb[tb.year.isna() & (tb.source == "osm")]
dated_reg = tb[(tb.year.notna()) & (tb.source != "osm")].copy()
dated_reg["year"] = dated_reg.year.astype(int)

static = np.zeros(len(grid_pts))
if len(undated):
    _, ii = tree.query(np.c_[undated.lat, undated.lon])
    np.add.at(static, ii, undated.capacity_mw.values)
static = static.reshape(lat2.shape)

capC = {}
for y in range(2000, 2022):
    act = dated_reg[(dated_reg.year <= y) & (dated_reg.capacity_mw > 0)]
    d = np.zeros(len(grid_pts))
    if len(act):
        _, ii = tree.query(np.c_[act.lat, act.lon])
        np.add.at(d, ii, act.capacity_mw.values)
    capC[y] = d.reshape(lat2.shape)

# region masks (same as build_exposure/p3: +-3deg around last transect vertex)
REGIONS = {**{"domain": None}, **cfg["transects"]}
masks = {}
for name, tr in cfg["transects"].items():
    lonc, latc = np.array(tr["vertices"])[-1]
    masks[name] = (np.abs(lat2 - latc) <= 3.0) & (np.abs(lon2 - lonc) <= 3.0)

steps = np.arange(1, 7) * 50.0
weights = np.exp(-steps / 100.0)
KM_DEG_LAT = 110.57
coslat = np.cos(np.deg2rad(lat2))
kmx = 111.32 * coslat

def regional_wfi(layer_fn):
    """layer_fn(y)->capacity field; returns DataFrame of region daily mean WFI."""
    out = {k: np.zeros(len(times)) for k in REGIONS}
    interp, cy = None, None
    for ti in range(len(times)):
        y = times[ti].year
        if y != cy:
            interp = RegularGridInterpolator((lat, lon), layer_fn(y),
                                             bounds_error=False, fill_value=0.0)
            cy = y
        ux, vy = u10.values[ti], v10.values[ti]
        spd = np.hypot(ux, vy) + 1e-6
        dirx, diry = -ux / spd, -vy / spd
        acc = np.zeros(lat2.shape)
        for s, wt in zip(steps, weights):
            plat = lat2 + diry * s / KM_DEG_LAT
            plon = lon2 + dirx * s / kmx
            acc += wt * interp(np.c_[plat.ravel(), plon.ravel()]).reshape(plat.shape)
        out["domain"][ti] = acc.mean()
        for name, m in masks.items():
            out[name][ti] = acc[m].mean()
        if ti % 1000 == 0:
            print("day", ti, flush=True)
    return pd.DataFrame(out, index=times)

wfiA = pd.read_csv(P / "wfi_daily.csv", parse_dates=["time"]).set_index("time")
print("static-layer WFI...")
S = regional_wfi(lambda y: static)
print("registry-only WFI...")
C = regional_wfi(lambda y: capC[y])

panel = pd.read_csv(P / "panel_daily.csv", parse_dates=["time"])

def fit_beta(wfis):
    res = {}
    for rname in REGIONS:
        d = panel.copy()
        y = d[f"{rname}__tmax_anom"]
        X = pd.DataFrame({
            "wfi": wfis[rname].values,
            "z500": d[f"{rname}__z500_anom"], "slp": d[f"{rname}__slp_anom"],
            "tcwv": d[f"{rname}__tcwv_anom"], "sst": d[f"{rname}__sst"],
            "doy_sin": np.sin(2 * np.pi * d.time.dt.dayofyear / 365.25),
            "doy_cos": np.cos(2 * np.pi * d.time.dt.dayofyear / 365.25),
            "year": d.time.dt.year})
        X = X.dropna(axis=1)
        fit = sm.OLS(y, sm.add_constant(X), missing="drop").fit(
            cov_type="HAC", cov_kwds={"maxlags": 14})
        rng = np.random.default_rng(cfg["random_seed"])
        nb = len(d) // 14
        boot = []
        yv, Xv = y.values, sm.add_constant(X.values)
        for b in range(200):
            start = rng.integers(0, len(d), nb)
            idx = np.concatenate([np.arange(s0, s0 + 14) % len(d) for s0 in start])
            try:
                boot.append(np.linalg.lstsq(Xv[idx], yv[idx], rcond=None)[0][1])
            except Exception:
                pass
        res[rname] = {"coef": fit.params.get("wfi", np.nan),
                      "se": fit.bse.get("wfi", np.nan),
                      "boot_p": float(2 * min((np.array(boot) <= 0).mean(),
                                              (np.array(boot) >= 0).mean()))}
    return res

resA = fit_beta(wfiA)
resB = fit_beta(wfiA - S)
resC = fit_beta(C)

rows = []
for rname in REGIONS:
    for var, rr in (("A_current", resA), ("B_dated_only", resB), ("C_registry_only", resC)):
        rows.append({"region": rname, "variant": var,
                     "wfi_mean_2021": float((wfiA if var=="A_current" else (wfiA-S if var=="B_dated_only" else C))[rname][-153:].mean()),
                     "coef_wfi": rr[rname]["coef"], "se": rr[rname]["se"],
                     "boot_p": rr[rname]["boot_p"]})
out = pd.DataFrame(rows)
out.to_csv(R / "exposure_chronology_sensitivity.csv", index=False)
with open("docs/EXPOSURE_SENSITIVITY.md", "w") as f:
    f.write("# R2 exposure chronology sensitivity\n\n"
            "Variants: A = dated + static undated-OSM background (canonical); "
            "B = dated units only; C = dated registry units only (all OSM excluded).\n"
            "WFI recomputed per variant with identical kernel/winds; Phase-3 "
            "regional spec refit per variant.\n\n```\n" + out.to_string() + "\n```\n")
print(out.to_string())
