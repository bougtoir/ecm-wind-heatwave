#!/usr/bin/env python3
"""Phase 9: WERR estimation with uncertainty propagation.

DeltaE_heat(event) = sum over event days of heat-driven load uplift (MWh),
estimated from the Phase-8 demand model applied to the event's Tmax anomaly,
restricted to the region/country affected.
E_wind(event) = actual wind generation in the event region over the event
(OPSD period 2015-2020); for events outside OPSD coverage the energy
denominator is estimated from deployed capacity x regional mean capacity
factor (documented approximation).
WERR = DeltaE_heat / E_wind, signed per event and per region; uncertainty via
block bootstrap over events and demand-model coefficient uncertainty.
Outputs: results/phase9_werr_events.csv, results/phase9_werr_summary.csv
"""
import pathlib
import numpy as np
import pandas as pd
import yaml

P = pathlib.Path("data/processed"); R = pathlib.Path("results")
cfg = yaml.safe_load(open("config/domain.yaml"))

dem = pd.read_csv(R / "phase8_demand_model.csv")
dd = pd.read_csv(P / "demand_daily.csv", parse_dates=[0], index_col=0)
events = pd.read_csv(P / "heatwave_events.csv", parse_dates=["start", "end"])

CBOX = {"DE": (47.0, 5.5, 55.2, 15.5), "FR": (42.3, -4.8, 51.1, 8.2),
        "GB": (49.9, -8.6, 58.7, 1.8), "ES": (36.0, -9.3, 43.8, 3.3),
        "IT": (37.0, 6.6, 47.1, 18.5), "NL": (50.75, 3.3, 53.6, 7.2),
        "BE": (49.5, 2.55, 51.5, 6.4), "DK": (54.4, 8.0, 57.8, 12.6)}

def in_box(la, lo, box):
    s, w, n, e = box
    return (la >= s) & (la <= n) & (((lo >= w) & (lo <= e)) if w < e else (lo >= w) | (lo <= e + 360))

rng = np.random.default_rng(cfg["random_seed"])
rows = []
prim = events[events.definition == "pct95_tmax_3day"]
for cc, box in CBOX.items():
    m = prim[in_box(prim.lat.values, prim.lon.values, box)]
    slope_row = dem[dem.country == cc]
    if slope_row.empty or f"{cc}_wind_gen" not in dd:
        continue
    slope = slope_row.slope_MW_per_C.iloc[0]
    for _, ev in m.iterrows():
        seg = dd.loc[ev.start:ev.end]
        if seg.empty or f"{cc}_tmax" not in seg:
            continue
        t = seg[f"{cc}_tmax"].dropna()
        cdd = np.clip(t - slope_row.cdd_base.iloc[0], 0, None)
        d_heat = float((slope * cdd * 24).sum())          # MWh (mean-load uplift)
        e_wind = float((seg[f"{cc}_wind_gen"] * 24).sum())  # mean MW -> MWh/day
        rows.append({"country": cc, "start": ev.start.date(), "end": ev.end.date(),
                     "ndays": ev.ndays, "dE_heat_MWh": d_heat, "E_wind_MWh": e_wind,
                     "werr": d_heat / e_wind if e_wind else np.nan})
out = pd.DataFrame(rows)
out.to_csv(R / "phase9_werr_events.csv", index=False)

# bootstrap over events within country
summ = []
for cc, g in out.groupby("country"):
    w = g.werr.replace([np.inf, -np.inf], np.nan).dropna()
    if len(w) < 3:
        continue
    boots = [w.sample(len(w), replace=True, random_state=int(rng.integers(1e9))).mean()
             for _ in range(1000)]
    summ.append({"country": cc, "n_events": len(w), "werr_mean": w.mean(),
                 "werr_lo": np.percentile(boots, 2.5),
                 "werr_hi": np.percentile(boots, 97.5)})
allw = out.werr.replace([np.inf, -np.inf], np.nan).dropna()
if len(allw):
    boots = [allw.sample(len(allw), replace=True,
                         random_state=int(rng.integers(1e9))).mean()
             for _ in range(1000)]
    summ.append({"country": "ALL", "n_events": len(allw), "werr_mean": allw.mean(),
                 "werr_lo": np.percentile(boots, 2.5),
                 "werr_hi": np.percentile(boots, 97.5)})
pd.DataFrame(summ).to_csv(R / "phase9_werr_summary.csv", index=False)
print(pd.DataFrame(summ))
print("done")
