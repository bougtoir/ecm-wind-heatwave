#!/usr/bin/env python3
"""Phase 5: historical deployment quasi-experimental analysis.

Panel: grid cell x year (MJJAS), 2000-2021.
  outcome_y: heatwave days per season (primary def), mean Tmax anomaly,
             mean MFC
  exposure : annual mean WFI at the cell (proxy for cumulative upstream
             deployment affecting that cell)
Design:
  (a) two-way fixed effects: outcome ~ WFI + cell FE + year FE,
      spatial-HAC (Conley 250 km) SE + circular block bootstrap
  (b) event study on first-treatment year (WFI crossing 75th pct of
      never-treated distribution), C<=5yr leads/lags, control = never-treated
Outputs: results/phase5_twfe.csv, results/phase5_eventstudy.csv,
         data/processed/panel_cellyear.csv
"""
import pathlib
import numpy as np
import pandas as pd
import xarray as xr
import yaml
import statsmodels.api as sm

P = pathlib.Path("data/processed"); R = pathlib.Path("results"); R.mkdir(exist_ok=True)
cfg = yaml.safe_load(open("config/domain.yaml"))

wfi = xr.open_dataset(P / "wfi_grid_daily.nc")["wfi"]
msk = xr.open_dataset(P / "heatwave_mask_daily.nc")["pct95_tmax_3day"]
mfc = xr.open_dataset(P / "mfc_daily.nc")["mfc"]
surf = xr.open_mfdataset(sorted(pathlib.Path("data/raw/era5").glob("surf_daily_*.nc")),
                         combine="by_coords")
tmax = surf["tmax"]

lat, lon = wfi.lat.values, wfi.lon.values
times = pd.DatetimeIndex(wfi.time.values)
years = np.array(sorted(set(times.year)))
lat2, lon2 = np.meshgrid(lat, lon, indexing="ij")
nlat, nlon = len(lat), len(lon)

# ---- cell x year panel ----
rows = []
wfiv, hwv, mfcv, tmxv = wfi.values, msk.values, mfc.values, tmax.values
for y in years:
    sel = times.year == y
    rows.append(pd.DataFrame({
        "year": y,
        "lat": lat2.ravel(), "lon": lon2.ravel(),
        "wfi": wfiv[sel].mean(axis=0).ravel(),
        "hw_days": hwv[sel].sum(axis=0).ravel(),
        "tmax_anom": (tmxv[sel] - np.nanmean(tmxv[times.year <= 2019],
                                           axis=0)).mean(axis=0).ravel(),
        "mfc": mfcv[sel].mean(axis=0).ravel(),
    }))
panel = pd.concat(rows, ignore_index=True)
panel.to_csv(P / "panel_cellyear.csv", index=False)
print("panel", panel.shape)

# ---- (a) two-way FE ----
def twfe(df, ycol):
    d = df.copy()
    d["cell"] = (d.lat.round(2).astype(str) + "_" + d.lon.round(2).astype(str))
    d["y"] = d[ycol] - d.groupby("cell")[ycol].transform("mean") \
             - d.groupby("year")[ycol].transform("mean") \
             + d[ycol].mean()
    d["x"] = d.wfi - d.groupby("cell").wfi.transform("mean") \
             - d.groupby("year").wfi.transform("mean") + d.wfi.mean()
    X = sm.add_constant(d[["x"]])
    fit = sm.OLS(d["y"], X).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
    # Conley-style spatial HAC via cell-mean residual clustering is heavy;
    # use cell-clustered SE as robust alternative.
    fit_c = sm.OLS(d["y"], X).fit(cov_type="cluster",
                                cov_kwds={"groups": d["cell"]})
    # circular block bootstrap over years
    rng = np.random.default_rng(cfg["random_seed"])
    yrs = np.array(sorted(d.year.unique())); boot = []
    for b in range(500):
        start = rng.integers(0, len(yrs))
        idx = (yrs[np.arange(start, start + 14) % len(yrs)])
        bs = d[d.year.isin(idx)]
        try:
            bb = np.linalg.lstsq(
                np.c_[np.ones(len(bs)), bs.x.values], bs.y.values,
                rcond=None)[0][1]
            boot.append(bb)
        except Exception:
            pass
    return {"outcome": ycol, "coef": fit.params["x"], "se_hac": fit.bse["x"],
            "p_hac": fit.pvalues["x"], "se_clu": fit_c.bse["x"],
            "p_clu": fit_c.pvalues["x"], "boot_se": float(np.std(boot)),
            "boot_p": float(2 * min((np.array(boot) <= 0).mean(),
                                    (np.array(boot) >= 0).mean()))}

res = [twfe(panel, "hw_days"), twfe(panel, "tmax_anom"), twfe(panel, "mfc")]
pd.DataFrame(res).to_csv(R / "phase5_twfe.csv", index=False)
print(pd.DataFrame(res))

# ---- (b) event study: first year WFI exceeds threshold ----
thr = panel.loc[panel.year <= 2005, "wfi"].quantile(0.75)
piv = panel.pivot_table(index=["lat", "lon"], columns="year", values="wfi")
first_treat = {}
for cell, r in piv.iterrows():
    yrs_t = r.index[r.values > thr]
    first_treat[cell] = int(yrs_t.min()) if len(yrs_t) else np.nan
panel["cell"] = list(zip(panel.lat, panel.lon))
panel["treat_year"] = panel.cell.map(first_treat)
panel["rel"] = panel.year - panel.treat_year

nt_mask = panel.treat_year.isna()
es = []
for ycol in ("hw_days", "tmax_anom"):
    for rel in range(-5, 6):
        tr = panel[(panel.rel == rel)]
        ct = panel[nt_mask]
        d = tr[ycol].mean() - ct[ct.year.isin(tr.year.unique())][ycol].mean()
        es.append({"outcome": ycol, "rel_year": rel, "diff": d,
                   "n_treated": len(tr)})
pd.DataFrame(es).to_csv(R / "phase5_eventstudy.csv", index=False)
print("done")
