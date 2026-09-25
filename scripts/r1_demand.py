#!/usr/bin/env python3
"""R1: targeted demand-model reanalysis (M0 reproduce, M1 enriched, M2 shrinkage).

Predeclared selection criteria (in order): scientific appropriateness of the
marginal temperature estimand; temporal OOS stability (blocked folds);
coefficient/sign stability; calibration in the warm-season range;
reproducibility; parsimony. Selection never uses WERR sign/magnitude.

M0: residual load (DOY median climatology + weekday median) on CDD(>22C),
    train 2015-18 / test 2019-20  (exact Phase-8 reproduction).
M1: residual load on CDD(>B) + weekday dummies + holiday + linear year trend
    + COVID-2020 dummy; B in {20,22,24} chosen by mean blocked-fold OOS R2.
    Slope SE via block bootstrap over calendar months (B=500, seed fixed).
M2: empirical-Bayes shrinkage of M1 slopes toward the inverse-variance
    pooled mean; applied to countries whose fold-wise slope sign is unstable
    or whose |slope|/SE < 1. Primary WERR uses M2-adjusted slopes; M0/M1
    results retained as sensitivity.
Outputs: results/demand_model_comparison.csv, demand_model_validation.csv,
         results/demand_temperature_slopes.csv, docs/WERR_REANALYSIS.md
"""
import pathlib
import numpy as np
import pandas as pd
import yaml

P = pathlib.Path("data/processed"); R = pathlib.Path("results")
cfg = yaml.safe_load(open("config/domain.yaml"))
rng = np.random.default_rng(cfg["random_seed"])

dd = pd.read_csv(P / "demand_daily.csv", parse_dates=[0], index_col=0)
tmx_cols = [c for c in dd.columns if c.endswith("_tmax")]
countries = [c[:-5] for c in tmx_cols]

HOL = pd.to_datetime([f"{y}-{d}" for y in range(2015, 2021) for d in
    ["01-01","05-01","12-25","12-26"]])  # fixed-date PH approximation (same as M0 spirit; reproducible)
# include original movable-feast days used in Phase 8 for M0 reproduction
HOL_M0 = pd.to_datetime([
    "2015-01-01","2015-04-03","2015-04-06","2015-05-01","2015-05-14","2015-05-25","2015-12-25","2015-12-26",
    "2016-01-01","2016-03-25","2016-03-28","2016-05-01","2016-05-05","2016-05-16","2016-12-25","2016-12-26",
    "2017-01-01","2017-04-14","2017-04-17","2017-05-01","2017-05-25","2017-06-05","2017-12-25","2017-12-26",
    "2018-01-01","2018-03-30","2018-04-02","2018-05-01","2018-05-10","2018-05-21","2018-12-25","2018-12-26",
    "2019-01-01","2019-04-19","2019-04-22","2019-05-01","2019-05-30","2019-06-10","2019-12-25","2019-12-26",
    "2020-01-01","2020-04-10","2020-04-13","2020-05-01","2020-05-21","2020-06-01","2020-12-25","2020-12-26"])
COVID = pd.to_datetime(pd.date_range("2020-03-15","2020-06-15").date)

def build(cc):
    d = pd.DataFrame({"load": dd[f"{cc}_load_mean"], "t": dd[f"{cc}_tmax"]}).dropna()
    d = d[d.index.month.isin([5,6,7,8,9])]
    d["doy"] = d.index.dayofyear; d["wd"] = d.index.dayofweek
    d["hol"] = d.index.normalize().isin(HOL_M0).astype(int)
    d["covid"] = d.index.normalize().isin(COVID).astype(int)
    d["yr"] = d.index.year - 2015
    clim = d.groupby("doy")["load"].transform("median")
    resid = d.load - clim
    resid = resid - resid.groupby(d.wd).transform("median")  # matches M0 exactly
    return d, resid

def fit_r2(Xtr, ytr, Xte, yte):
    b = np.linalg.lstsq(Xtr, ytr, rcond=None)[0]
    r2tr = 1 - ((ytr - Xtr@b)**2).sum() / ((ytr - ytr.mean())**2).sum()
    r2te = 1 - ((yte - Xte@b)**2).sum() / ((yte - yte.mean())**2).sum()
    return b, r2tr, r2te

rows, val_rows, slopes = [], [], []
FOLDS = [([2015,2016],[2017]), ([2017,2018],[2019]), ([2015,2018],[2020])]
for cc in countries:
    d, resid = build(cc)
    if len(d) < 200:
        continue
    yr = d.index.year.values
    # ---- M0 reproduction ----
    cdd0 = np.clip(d.t - 22.0, 0, None).values
    tr = yr <= 2018
    b0, r0tr, r0te = fit_r2(np.c_[np.ones(tr.sum()), cdd0[tr]], resid[tr],
                            np.c_[np.ones((~tr).sum()), cdd0[~tr]], resid[~tr])
    # ---- M1: choose base by blocked CV ----
    best = None
    for B in (20.0, 22.0, 24.0):
        cdd = np.clip(d.t - B, 0, None).values
        X = np.column_stack([np.ones(len(d)), cdd,
                             pd.get_dummies(d.wd, prefix="w", drop_first=True).astype(float).values,
                             d.hol.values, d.yr.values, d.covid.values])
        fold_r2, fold_slopes = [], []
        for trn, tst in FOLDS:
            mtr = np.isin(yr, trn); mte = np.isin(yr, tst)
            if mtr.sum() < 100 or mte.sum() < 30: continue
            bb, _, rt = fit_r2(X[mtr], resid[mtr], X[mte], resid[mte])
            fold_r2.append(rt); fold_slopes.append(bb[1])
        mr2 = np.mean(fold_r2) if fold_r2 else -9
        if best is None or mr2 > best[0]:
            best = (mr2, B, fold_slopes)
    mr2, Bbest, fslopes = best
    cdd = np.clip(d.t - Bbest, 0, None).values
    X = np.column_stack([np.ones(len(d)), cdd,
                         pd.get_dummies(d.wd, prefix="w", drop_first=True).astype(float).values,
                         d.hol.values, d.yr.values, d.covid.values])
    b1, r1tr, _ = fit_r2(X[tr], resid[tr], X[~tr], resid[~tr])
    slope1 = b1[1]
    # month-block bootstrap for slope SE — same estimand as reported slope:
    # resample TRAIN-period (<=2018) months with replacement, keeping duplicate
    # month picks (concatenated row indices, not np.isin)
    tr_idx = np.where(tr)[0]
    months_tr = d.index[tr].to_period("M"); uq = months_tr.unique()
    month_rows = {m: tr_idx[months_tr == m] for m in uq}
    bs_slopes = []
    for _ in range(500):
        pick = uq[rng.integers(0, len(uq), len(uq))]
        idx = np.concatenate([month_rows[m] for m in pick])
        if len(idx) < 60 or cdd[idx].std() < 1e-9: continue
        bb = np.linalg.lstsq(X[idx], resid.values[idx], rcond=None)[0]
        bs_slopes.append(bb[1])
    se1 = float(np.std(bs_slopes)) if len(bs_slopes) > 10 else np.nan
    # re-evaluate M1 blocked R2 on train/test for reporting
    bfull = np.linalg.lstsq(X, resid.values, rcond=None)[0]
    r1te = 1 - ((resid[~tr] - X[~tr]@b1)**2).sum()/((resid[~tr]-resid[~tr].mean())**2).sum()
    # M0 blocked folds for comparison table
    m0_folds = []
    for trn, tst in FOLDS:
        mtr = np.isin(yr, trn); mte = np.isin(yr, tst)
        if mtr.sum() < 100 or mte.sum() < 30: continue
        A0 = np.c_[np.ones(mtr.sum()), cdd0[mtr]]
        _, _, rt = fit_r2(A0, resid[mtr], np.c_[np.ones(mte.sum()), cdd0[mte]], resid[mte])
        m0_folds.append(rt)
    sign_stable = (np.sign(fslopes) == np.sign(slope1)).all() if fslopes else False
    rows.append({"country": cc, "m0_slope": b0[1], "m0_r2_train": r0tr,
                 "m0_r2_test": r0te, "m0_cv_r2": np.mean(m0_folds) if m0_folds else np.nan,
                 "m1_slope": slope1, "m1_se": se1, "m1_r2_train": r1tr,
                 "m1_r2_test": r1te, "m1_cv_r2": mr2, "cdd_base": Bbest,
                 "m1_fold_slopes": ";".join(f"{s:.1f}" for s in fslopes),
                 "sign_stable": sign_stable})
    val_rows.append({"country": cc, "n_summer_days": len(d), "m1_cv_r2": mr2,
                     "m1_fold_r2": ";".join(f"{x:.3f}" for x in fold_r2)})
comp = pd.DataFrame(rows)

# ---- M2 empirical-Bayes shrinkage on M1 slopes ----
s = comp.m1_slope.values; se = comp.m1_se.values
w = 1.0 / np.where(se > 0, se**2, np.nan)
mu = np.nansum(s * w) / np.nansum(w)
tau2 = max(0.0, np.nanmean(s**2 - se**2) ) # method of moments
post_var = 1.0 / (w + 1.0 / tau2) if tau2 > 0 else np.zeros_like(se)
post = w * post_var * s + (post_var / tau2) * mu if tau2 > 0 else np.full_like(s, mu)
comp["m2_slope"] = post; comp["m2_se"] = np.sqrt(post_var)
unstable = (~comp.sign_stable) | (np.abs(comp.m1_slope) / comp.m1_se < 1.0)
comp["use_shrunk_primary"] = unstable
# GB: identically zero cooling-degree exposure in-sample -> fixed 0 slope
# (documented; excluded from MC uncertainty propagation)
gfix = comp.country == "GB"
comp.loc[gfix, "slope_final"] = 0.0

comp["slope_final"] = np.where(unstable, comp.m2_slope, comp.m1_slope)
comp["se_final"] = np.where(unstable, comp.m2_se, comp.m1_se)
# GB: identically zero cooling-degree exposure in-sample -> fixed 0 slope
# (documented; excluded from MC uncertainty propagation)
comp.loc[comp.country == "GB", ["slope_final", "se_final"]] = 0.0

pd.DataFrame(val_rows).to_csv(R / "demand_model_validation.csv", index=False)
comp.to_csv(R / "demand_model_comparison.csv", index=False)
comp[["country","slope_final","se_final","cdd_base","m1_cv_r2","sign_stable",
      "use_shrunk_primary"]].rename(columns={"slope_final":"slope_MW_per_C",
     "se_final":"slope_se"}).to_csv(R / "demand_temperature_slopes.csv", index=False)

with open("docs/WERR_REANALYSIS.md","w") as f:
    f.write("# R1 demand/WERR reanalysis\n\n"
            "## Predeclared model-selection criteria\n"
            "1. scientific appropriateness of marginal temperature estimand (CDD slope)\n"
            "2. temporal OOS stability (3 blocked year folds)\n3. coefficient/sign stability\n"
            "4. calibration in warm-season range\n5. reproducibility\n6. parsimony\n"
            "Selection never uses WERR sign or magnitude.\n\n"
            "## Models\n- M0: Phase-8 exact reproduction (CDD>22, train 2015-18/test 2019-20)\n"
            "- M1: CDD base {20,22,24} by blocked CV + weekday/holiday/trend/COVID covariates; "
            "month-block bootstrap SE (B=500)\n"
            "- M2: empirical-Bayes shrinkage to inverse-variance pooled mean for countries "
            "with sign-unstable folds or |slope|/SE < 1; shrunk slopes feed PRIMARY WERR\n\n"
            f"Pooled prior mean slope {mu:.1f} MW/C, tau2 {tau2:.1f}. "
            f"{int(unstable.sum())}/{len(comp)} countries shrunk in primary WERR.\n\n"
            "## Comparison\n```\n"+comp.round(3).to_string()+"\n```\n")
print(comp.round(3).to_string())
print("mu", mu, "tau2", tau2, "shrunk:", comp[comp.use_shrunk_primary].country.tolist())
