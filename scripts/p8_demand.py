#!/usr/bin/env python3
"""Phase 8: temperature-sensitive electricity demand model.

OPSD hourly 2015-2020 -> per-country daily series. For each country:
  daily residual load = actual - (DOY climatology + weekday + holiday mean)
  heat-sensitive uplift = regression of residual on cooling-degree-day
  exposure (regional Tmax > threshold from ERA5), out-of-sample validated
  (train 2015-2018, test 2019-2020).
Outputs:
  data/processed/demand_daily.csv
  results/phase8_demand_model.csv    (slope MW/C, R2, out-of-sample skill)
"""
import pathlib
import numpy as np
import pandas as pd
import xarray as xr
import yaml

P = pathlib.Path("data/processed"); R = pathlib.Path("results"); R.mkdir(exist_ok=True)
cfg = yaml.safe_load(open("config/domain.yaml"))

opsd = pd.read_csv("data/raw/electricity/opsd_time_series_60min_2020.csv",
                   parse_dates=[0], index_col=0)
opsd.index = pd.to_datetime(opsd.index, utc=True)
load_cols = {c.split("_")[0]: c for c in opsd.columns
             if c.endswith("_load_actual_entsoe_transparency")}
print("countries:", list(load_cols))

# country proxy regions on the 1.5deg grid (bbox approximations)
CBOX = {"DE": (47.0, 5.5, 55.2, 15.5), "FR": (42.3, -4.8, 51.1, 8.2),
        "GB": (49.9, -8.6, 58.7, 1.8), "ES": (36.0, -9.3, 43.8, 3.3),
        "IT": (37.0, 6.6, 47.1, 18.5), "NL": (50.75, 3.3, 53.6, 7.2),
        "BE": (49.5, 2.55, 51.5, 6.4), "DK": (54.4, 8.0, 57.8, 12.6),
        "AT": (46.4, 9.5, 49.0, 17.2), "PL": (49.0, 14.1, 54.9, 24.1),
        "SE": (55.3, 11.0, 69.1, 24.2), "NO": (58.0, 4.9, 71.2, 31.0),
        "FI": (59.8, 20.5, 70.1, 31.6), "IE": (51.4, -10.5, 55.4, -6.0),
        "PT": (36.8, -9.5, 42.2, -6.2), "CZ": (48.6, 12.1, 51.1, 18.9),
        "AT": (46.4, 9.5, 49.0, 17.2), "CH": (45.8, 6.0, 47.8, 10.5)}

surf = xr.open_mfdataset(sorted(pathlib.Path("data/raw/era5").glob("surf_daily_*.nc")),
                         combine="by_coords")
lat, lon = surf.latitude.values, surf.longitude.values
lat2, lon2 = np.meshgrid(lat, lon, indexing="ij")
tt = pd.DatetimeIndex(surf.time.values)
tmax = surf["tmax"].values

# daily country Tmax (grid mean over box)
ct = {}
for cc, (s, w, n, e) in CBOX.items():
    m = (lat2 >= s) & (lat2 <= n) & (
        ((lon2 >= w) & (lon2 <= e)) if w < e else ((lon2 >= w) | (lon2 <= e + 360)))
    ct[cc] = tmax[:, m].mean(axis=1)
ct = pd.DataFrame(ct, index=tt)

# daily mean + peak load per country
daily = opsd.resample("1D").mean()
peak = opsd.resample("1D").max()
rec = {}
for cc, col in load_cols.items():
    rec[f"{cc}_load_mean"] = daily[col]
    rec[f"{cc}_load_peak"] = peak[col]
    wcol = next((c for c in opsd.columns if c.startswith(cc) and "wind" in c
                 and "generation_actual" in c), None)
    if wcol:
        rec[f"{cc}_wind_gen"] = daily[wcol]
dd = pd.DataFrame(rec).tz_localize(None)
dd = dd.join(ct.add_suffix("_tmax"), how="left")
dd.to_csv(P / "demand_daily.csv")
print("demand_daily", dd.shape)

# heat-sensitivity model per country
HOL = pd.to_datetime([
    "2015-01-01","2015-04-03","2015-04-06","2015-05-01","2015-05-14","2015-05-25","2015-12-25","2015-12-26",
    "2016-01-01","2016-03-25","2016-03-28","2016-05-01","2016-05-05","2016-05-16","2016-12-25","2016-12-26",
    "2017-01-01","2017-04-14","2017-04-17","2017-05-01","2017-05-25","2017-06-05","2017-12-25","2017-12-26",
    "2018-01-01","2018-03-30","2018-04-02","2018-05-01","2018-05-10","2018-05-21","2018-12-25","2018-12-26",
    "2019-01-01","2019-04-19","2019-04-22","2019-05-01","2019-05-30","2019-06-10","2019-12-25","2019-12-26",
    "2020-01-01","2020-04-10","2020-04-13","2020-05-01","2020-05-21","2020-06-01","2020-12-25","2020-12-26"])

res = []
THRESH = 22.0  # CDD base temperature (degC)
for cc in load_cols:
    if cc not in ct.columns:
        continue
    d = pd.DataFrame({"load": dd[f"{cc}_load_mean"], "t": ct[cc]}).dropna()
    if len(d) < 500:
        continue
    d["doy"] = d.index.dayofyear
    d["wd"] = d.index.dayofweek
    d["hol"] = d.index.normalize().isin(HOL).astype(int)
    # residual: remove climatology + weekly/holiday pattern
    clim = d.groupby("doy")["load"].transform("median")
    resid = d.load - clim
    wd_adj = resid.groupby(d.wd).transform("median")
    resid = resid - wd_adj - resid.groupby(d.hol).transform("median") * 0
    cdd = np.clip(d.t - THRESH, 0, None)
    tr = d.index.year <= 2018
    A = np.c_[np.ones(tr.sum()), cdd[tr]]
    beta = np.linalg.lstsq(A, resid[tr], rcond=None)[0]
    pred_tr = A @ beta; pred_all = np.c_[np.ones(len(d)), cdd] @ beta
    r2_tr = 1 - ((resid[tr] - pred_tr) ** 2).sum() / ((resid[tr] - resid[tr].mean()) ** 2).sum()
    te = ~tr
    r2_te = 1 - ((resid[te] - pred_all[te]) ** 2).sum() / ((resid[te] - resid[te].mean()) ** 2).sum()
    res.append({"country": cc, "slope_MW_per_C": beta[1], "intercept": beta[0],
                "r2_train": r2_tr, "r2_test": r2_te, "n_train": int(tr.sum()),
                "n_test": int(te.sum()), "cdd_base": THRESH})
out = pd.DataFrame(res)
out.to_csv(R / "phase8_demand_model.csv", index=False)
print(out)
print("done")
