#!/usr/bin/env python3
"""R1: revised WERR with coefficient-uncertainty propagation.

Same causal chain as Phase 9 (beta_r x WFI -> dT -> slope_c -> dE_heat;
dE_heat/E_wind per event), now with Monte-Carlo propagation of BOTH the
atmospheric coefficient (beta_r ~ N(beta, se)) and demand slope
(slope_c ~ N(slope, se)) uncertainty, layered on the event bootstrap.
Demand slopes = revised M1/M2 selection (results/demand_temperature_slopes.csv).

Outputs: results/werr_event_level.csv, werr_country_summary.csv,
         werr_pooled_summary.csv  (+ werr_m0_comparison via --m0 tag)
"""
import pathlib, sys
import numpy as np
import pandas as pd
import yaml

P = pathlib.Path("data/processed"); R = pathlib.Path("results")
cfg = yaml.safe_load(open("config/domain.yaml"))
MODE = sys.argv[1] if len(sys.argv) > 1 else "primary"
if MODE == "m0":
    dem = pd.read_csv("results/archived_original/phase8_demand_model.csv")
    dem = dem.rename(columns={"slope_MW_per_C": "slope_MW_per_C"}); dem["slope_se"] = np.nan
else:
    dem = pd.read_csv(R / "demand_temperature_slopes.csv")

preg = pd.read_csv(R / "phase3_panel_regression.csv")
wfi = pd.read_csv(P / "wfi_daily.csv", parse_dates=["time"]).set_index("time")
dd = pd.read_csv(P / "demand_daily.csv", parse_dates=[0], index_col=0)
events = pd.read_csv(P / "heatwave_events.csv", parse_dates=["start", "end"])

C2R = {"DE": "northsea_to_denmark_germany", "DK": "northsea_to_denmark_germany",
       "NL": "northsea_to_lowcountries", "BE": "northsea_to_lowcountries",
       "FR": "atlantic_to_france", "ES": "atlantic_to_iberia", "PT": "atlantic_to_iberia",
       "GB": "uk_offshore_to_continent", "IE": "uk_offshore_to_continent",
       "IT": "domain", "AT": "domain", "PL": "domain", "CZ": "domain"}
CBOX = {"DE": (47.0, 5.5, 55.2, 15.5), "FR": (42.3, -4.8, 51.1, 8.2),
        "GB": (49.9, -8.6, 58.7, 1.8), "ES": (36.0, -9.3, 43.8, 3.3),
        "IT": (37.0, 6.6, 47.1, 18.5), "NL": (50.75, 3.3, 53.6, 7.2),
        "BE": (49.5, 2.55, 51.5, 6.4), "DK": (54.4, 8.0, 57.8, 12.6),
        "IE": (51.4, -10.5, 55.4, -6.0), "PT": (36.8, -9.5, 42.2, -6.2),
        "PL": (49.0, 14.1, 54.9, 24.1), "AT": (46.4, 9.5, 49.0, 17.2),
        "CZ": (48.6, 12.1, 51.1, 18.9)}

def in_box(la, lo, box):
    s, w, n, e = box
    return (la >= s) & (la <= n) & (((lo >= w) & (lo <= e)) if w < e else (lo >= w) | (lo <= e + 360))

rng = np.random.default_rng(cfg["random_seed"])
beta = preg.set_index("region").coef_wfi
beta_se = preg.set_index("region").se

rows = []
prim = events[events.definition == "pct95_tmax_3day"]
for cc, box in CBOX.items():
    region = C2R[cc]
    sr = dem[dem.country == cc]
    if region not in beta.index or f"{cc}_wind_gen" not in dd or sr.empty:
        continue
    slope = float(sr.slope_MW_per_C.iloc[0]); sse = float(sr.slope_se.iloc[0])
    b, bs = float(beta[region]), float(beta_se[region])
    m = prim[in_box(prim.lat.values, prim.lon.values, box)]
    for _, ev in m.iterrows():
        seg = dd.loc[ev.start:ev.end]
        if seg.empty:
            continue
        w_ev = float(wfi.loc[ev.start:ev.end, region].mean())
        e_wind = float((seg[f"{cc}_wind_gen"] * 24).sum())
        if not e_wind:
            continue
        dT = b * w_ev
        d_heat = slope * dT * 24 * ev.ndays
        rows.append({"country": cc, "region": region, "start": ev.start.date(),
                     "end": ev.end.date(), "ndays": ev.ndays, "wfi_MW": w_ev,
                     "dT_attrib_C": dT, "dE_heat_MWh": d_heat,
                     "E_wind_MWh": e_wind, "werr": d_heat / e_wind,
                     "slope_used": slope, "slope_se": sse, "beta": b, "beta_se": bs})
out = pd.DataFrame(rows)
tag = "" if MODE == "primary" else f"_{MODE}"
out.to_csv(R / f"werr_event_level{tag}.csv", index=False)

# ---- MC propagation: per-country slope/beta redraw inside event bootstrap ----
B = 1000
summ = []
for cc, g in out.groupby("country"):
    w = g.werr.replace([np.inf, -np.inf], np.nan).dropna()
    if len(w) < 3:
        continue
    s0, sse0, b0, bse0 = g.slope_used.iloc[0], g.slope_se.iloc[0], g.beta.iloc[0], g.beta_se.iloc[0]
    means = []
    wvals = w.values
    for _ in range(B):
        idx = rng.integers(0, len(wvals), len(wvals))
        # scale events by coefficient redraw ratio: werr ∝ slope*beta
        s_d = s0 if not np.isfinite(sse0) or sse0 == 0 else rng.normal(s0, sse0)
        b_d = rng.normal(b0, bse0)
        means.append(wvals[idx].mean() * (s_d * b_d) / (s0 * b0) if s0 * b0 != 0 else wvals[idx].mean())
    summ.append({"country": cc, "region": g.region.iloc[0], "n_events": len(w),
                 "werr_mean": w.mean(), "werr_lo": np.percentile(means, 2.5),
                 "werr_hi": np.percentile(means, 97.5),
                 "werr_mean_coefmc": float(np.mean(means))})
allw = out.werr.replace([np.inf, -np.inf], np.nan).dropna()
if len(allw):
    # pooled MC: per-replicate per-country coefficient draws scale each event
    base = out.set_index("country")
    svec = base.slope_used.groupby("country").first()
    ssevec = base.slope_se.groupby("country").first()
    bvec = base.beta.groupby("country").first()
    bsevec = base.beta_se.groupby("country").first()
    scale0 = (svec * bvec)
    w_arr = allw.values
    c_arr = out.loc[allw.index, "country"].values
    ccat = pd.Categorical(c_arr, categories=svec.index).codes
    means = []
    for _ in range(B):
        idx = rng.integers(0, len(w_arr), len(w_arr))
        s_d = np.array([rng.normal(svec.iloc[k], ssevec.iloc[k])
                        if np.isfinite(ssevec.iloc[k]) and ssevec.iloc[k] > 0
                        else svec.iloc[k] for k in range(len(svec))])
        b_d = rng.normal(bvec.values, bsevec.values)
        sc = (s_d * b_d) / scale0.values
        sc[~np.isfinite(sc)] = 1.0
        means.append((w_arr[idx] * sc[ccat[idx]]).mean())
    summ.append({"country": "ALL", "region": "-", "n_events": len(allw),
                 "werr_mean": allw.mean(), "werr_lo": np.percentile(means, 2.5),
                 "werr_hi": np.percentile(means, 97.5),
                 "werr_mean_coefmc": np.mean(means)})
sdf = pd.DataFrame(summ)
sdf.to_csv(R / f"werr_country_summary{tag}.csv", index=False)
sdf[sdf.country == "ALL"].to_csv(R / f"werr_pooled_summary{tag}.csv", index=False)
print(MODE); print(sdf.round(4).to_string())
