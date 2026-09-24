#!/usr/bin/env python3
"""Phase 4: circulation-matched analog analysis.

For each region and each MJJAS day, build the feature vector
  [z500_anom, slp_anom, upstream wind dir/speed (transect flux), tcwv_anom,
   sst, DOY]
on a common baseline (2000-2019). For every day, find its K nearest analogs
(whitened / Mahalanobis distance, DOY +-15d) among days in OTHER years.
Then estimate the deployment effect as the difference in Tmax anomaly between
analog days in the high-WFI era (post-2015) vs low-WFI era (pre-2010),
with a covariate-balance table and block-bootstrap CI.

Outputs:
  results/phase4_analog_effect.csv
  results/phase4_balance.csv
"""
import pathlib
import numpy as np
import pandas as pd
import yaml

P = pathlib.Path("data/processed"); R = pathlib.Path("results"); R.mkdir(exist_ok=True)
cfg = yaml.safe_load(open("config/domain.yaml"))
panel = pd.read_csv(P / "panel_daily.csv", parse_dates=["time"])
K = 30
res, bal = [], []

for rname in list(cfg["transects"].keys()) + ["domain"]:
    d = panel.dropna(subset=[f"{rname}__tmax_anom"]).reset_index(drop=True)
    feats = pd.DataFrame({
        "z500": d[f"{rname}__z500_anom"], "slp": d[f"{rname}__slp_anom"],
        "flux": d[rname] if rname in d else 0.0,
        "tcwv": d[f"{rname}__tcwv_anom"], "sst": d[f"{rname}__sst"],
    }).fillna(0.0)
    base = (d.time <= "2019-12-31")
    mu, sd = feats[base].mean(), feats[base].std().replace(0, 1)
    Z = ((feats - mu) / sd).values
    C = np.cov(Z[base.values].T) + 1e-6 * np.eye(Z.shape[1])
    Ci = np.linalg.inv(C)
    y = d[f"{rname}__tmax_anom"].values
    wfi = d[f"{rname}__wfi"].values
    doy = d.time.dt.dayofyear.values
    year = d.time.dt.year.values

    rng = np.random.default_rng(cfg["random_seed"])
    est = []
    n_hi = n_lo = 0
    hi_res, lo_res = [], []
    for i in range(len(d)):
        dd = np.abs(doy - doy[i]); dd = np.minimum(dd, 366 - dd)
        cand = np.where((dd <= 15) & (year != year[i]))[0]
        if len(cand) < K:
            continue
        diff = Z[cand] - Z[i]
        dist = np.einsum("ij,jk,ik->i", diff, Ci, diff)
        nn = cand[np.argsort(dist)[:K]]
        era = "hi" if year[i] >= 2015 else ("lo" if year[i] <= 2010 else "mid")
        if era == "hi":
            hi_res.append(y[i] - np.nanmean(y[nn])); n_hi += 1
        elif era == "lo":
            lo_res.append(y[i] - np.nanmean(y[nn])); n_lo += 1
    eff = np.nanmean(hi_res) - np.nanmean(lo_res)
    # bootstrap
    boot = []
    for b in range(500):
        bh = np.nanmean(rng.choice(hi_res, len(hi_res))) if hi_res else np.nan
        bl = np.nanmean(rng.choice(lo_res, len(lo_res))) if lo_res else np.nan
        boot.append(bh - bl)
    res.append({"region": rname, "analog_delta_hiC": np.nanmean(hi_res),
                "analog_delta_loC": np.nanmean(lo_res), "effect_C": eff,
                "boot_se": np.nanstd(boot),
                "boot_p": 2 * min((np.array(boot) <= 0).mean(), (np.array(boot) >= 0).mean()),
                "n_hi": n_hi, "n_lo": n_lo})
    # balance: mean |std diff| of features between eras
    hi_m = year >= 2015; lo_m = year <= 2010
    bal.append({"region": rname,
                **{f"smd_{c}": float((Z[hi_m, j].mean() - Z[lo_m, j].mean()) /
                                     (Z[:, j].std() + 1e-9))
                   for j, c in enumerate(feats.columns)}})
pd.DataFrame(res).to_csv(R / "phase4_analog_effect.csv", index=False)
pd.DataFrame(bal).to_csv(R / "phase4_balance.csv", index=False)
print(pd.DataFrame(res))
print("done")
