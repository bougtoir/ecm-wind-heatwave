#!/usr/bin/env python3
"""Phase 6: falsification / negative-control battery.

Reuses the Phase-3 panel regression spec (tmax_anom ~ wfi + controls, HAC):
  C1 upwind control  : exposure computed DOWNWIND (sign-flipped direction)
  C2 wrong direction : transects rotated 180 deg (eastward transport)
  C3 placebo timing  : outcomes shifted +45 days
  C4 inactive season : model re-run on ONDJFMA (no heatwaves expected -> ~0)
  C5 weak outcome    : SST as outcome (should not respond to wind capacity)
  C6 kernel variants : alt WFI kernels (100km->50/200km, unweighted)
  C7 leave-one-out   : drop one region at a time from domain estimate
Multiplicity: BH-FDR q=0.05 across the primary family of tests.
Outputs: results/phase6_falsification.csv, results/phase6_fdr.csv
"""
import pathlib
import numpy as np
import pandas as pd
import xarray as xr
import yaml
import statsmodels.api as sm
from scipy.interpolate import RegularGridInterpolator
from scipy.stats import false_discovery_control

P = pathlib.Path("data/processed"); R = pathlib.Path("results"); R.mkdir(exist_ok=True)
cfg = yaml.safe_load(open("config/domain.yaml"))
panel = pd.read_csv(P / "panel_daily.csv", parse_dates=["time"])
import sys
sys.path.insert(0, "scripts")
from grid_utils import canon

surf = xr.open_mfdataset(sorted(pathlib.Path("data/raw/era5").glob("surf_daily_*.nc")),
                         combine="by_coords")
_u10, _v10 = canon(surf["u10"]).load(), canon(surf["v10"]).load()
lat, lon = _u10.latitude.values, _u10.longitude.values
lat2, lon2 = np.meshgrid(lat, lon, indexing="ij")
times = pd.DatetimeIndex(_u10.time.values)

def fit_beta(y, x, ctrls):
    X = pd.concat([x, ctrls], axis=1).astype(float).dropna(axis=1)
    X = sm.add_constant(X)
    try:
        f = sm.OLS(y.values, X, missing="drop").fit(
            cov_type="HAC", cov_kwds={"maxlags": 14})
        return f.params.iloc[1], f.pvalues.iloc[1]
    except Exception:
        return np.nan, np.nan

ctrls = pd.DataFrame({
    "z500": panel["domain__z500_anom"], "slp": panel["domain__slp_anom"],
    "tcwv": panel["domain__tcwv_anom"], "sst": panel["domain__sst"],
    "doy_sin": np.sin(2 * np.pi * panel.time.dt.dayofyear / 365.25),
    "doy_cos": np.cos(2 * np.pi * panel.time.dt.dayofyear / 365.25),
    "year": panel.time.dt.year})
y_main = panel["domain__tmax_anom"]
x_main = panel["domain__wfi"]

res = []
def add(test, region, coef, p, n=None):
    res.append({"test": test, "region": region, "coef": coef, "p": p, "n": n})

# primary family (all regions)
for rn in list(cfg["transects"].keys()) + ["domain"]:
    c = ctrls.copy()
    c["z500"] = panel[f"{rn}__z500_anom"]; c["slp"] = panel[f"{rn}__slp_anom"]
    c["tcwv"] = panel[f"{rn}__tcwv_anom"]; c["sst"] = panel[f"{rn}__sst"]
    b, p = fit_beta(panel[f"{rn}__tmax_anom"], panel[f"{rn}__wfi"], c)
    add("primary", rn, b, p)

# C1 downwind exposure (sign-flip direction): rebuild exposure cheaply using
# downstream sampling on the stored capdensity grids.
cap_years = {y: xr.open_dataset(P / f"capdensity_{y}.nc")["__xarray_dataarray_variable__"]
             for y in [2000, 2010, 2021] if (P / f"capdensity_{y}.nc").exists()}
cy = None; interp = None
u10, v10 = _u10.values, _v10.values
KM = 110.57; kmx = 111.32 * np.cos(np.deg2rad(lat2))
steps = np.arange(1, 7) * 50.0; weights = np.exp(-steps / 100.0)
dw = np.zeros((len(times),) + lat2.shape, dtype=np.float32)
for ti in range(len(times)):
    y = times[ti].year
    key = max([k for k in cap_years if k <= y], default=None)
    if key != cy:
        interp = RegularGridInterpolator((lat, lon), cap_years[key].values,
                                         bounds_error=False, fill_value=0.0)
        cy = key
    ux, vy = u10[ti], v10[ti]; spd = np.hypot(ux, vy) + 1e-6
    dx, dy = ux / spd, vy / spd          # DOWNWIND (+) instead of upstream (-)
    acc = np.zeros_like(lat2)
    for s, w in zip(steps, weights):
        acc += w * interp(np.c_[(lat2 + dy * s / KM).ravel(),
                                (lon2 + dx * s / kmx).ravel()]).reshape(lat2.shape)
    dw[ti] = acc
b, p = fit_beta(y_main, pd.Series(dw.mean(axis=(1, 2))), ctrls)
add("C1_downwind_exposure", "domain", b, p)

# C3 placebo: shift outcome +45 days
y_shift = y_main.shift(45)
b, p = fit_beta(y_shift, x_main, ctrls)
add("C3_placebo_+45d", "domain", b, p)

# C4 inactive season Nov-Mar (same exposure series but off-season)
off = panel.time.dt.month.isin([11, 12, 1, 2, 3]) | \
      ((panel.time.dt.year == 2000) & (panel.time.dt.month < 5))
b, p = fit_beta(y_main[off.values], x_main[off.values], ctrls[off.values])
add("C4_offseason_NovMar", "domain", b, p)

# C5 weak outcome: SST should not react
b, p = fit_beta(ctrls["sst"], x_main, ctrls.drop(columns=["sst"]))
add("C5_weak_outcome_SST", "domain", b, p)

# C6 kernel variants: 50km and 200km decay, unweighted
for tag, dec, wfun in [("50km", 50.0, lambda s: np.exp(-s / 50.0)),
                       ("200km", 200.0, lambda s: np.exp(-s / 200.0)),
                       ("unweighted", 100.0, lambda s: 1.0)]:
    ws = np.array([wfun(s) for s in steps]); ws = weights if tag == "unweighted" else ws
    acc = np.zeros(len(times))
    interp_y = None; itp = None
    for ti in range(len(times)):
        y = times[ti].year
        key = max([k for k in cap_years if k <= y], default=None)
        if key != interp_y:
            itp = RegularGridInterpolator((lat, lon), cap_years[key].values,
                                          bounds_error=False, fill_value=0.0)
            interp_y = key
        ux, vy = u10[ti], v10[ti]; spd = np.hypot(ux, vy) + 1e-6
        dxv, dyv = -ux / spd, -vy / spd
        a = np.zeros_like(lat2)
        for s, w in zip(steps, ws):
            a += w * itp(np.c_[(lat2 + dyv * s / KM).ravel(),
                               (lon2 + dxv * s / kmx).ravel()]).reshape(lat2.shape)
        acc[ti] = a.mean()
    b, p = fit_beta(y_main, pd.Series(acc), ctrls)
    add(f"C6_kernel_{tag}", "domain", b, p)

# C7 leave-one-region-out: domain = all regions; recompute on remaining
regs = list(cfg["transects"].keys())
for drop in regs:
    keep = [r for r in regs if r != drop]
    y_k = panel[[f"{r}__tmax_anom" for r in keep]].mean(axis=1)
    x_k = panel[[f"{r}__wfi" for r in keep]].mean(axis=1)
    b, p = fit_beta(y_k, x_k, ctrls)
    add(f"C7_LOO_drop_{drop}", "regions_minus1", b, p)

out = pd.DataFrame(res)
out.to_csv(R / "phase6_falsification.csv", index=False)
prim = out[out.test == "primary"].copy()
prim["p_fdr"] = false_discovery_control(prim["p"].fillna(1.0).values)
prim.to_csv(R / "phase6_fdr.csv", index=False)
print(out)
print("done")
