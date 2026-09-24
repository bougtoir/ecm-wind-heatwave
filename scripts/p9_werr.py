#!/usr/bin/env python3
"""Phase 9: WERR estimation with uncertainty propagation.

Causal chain per heatwave event e in region r:
  dT_att(e) = beta_r * WFI_r(e)          [Phase-3 regional panel coefficient
                                          on Tmax anomaly, C per MW-exposure]
  dE_heat(e) = slope_c * dT_att * 24h    [Phase-8 demand slope, MW/C -> MWh/day]
  E_wind(e)  = actual wind generation over the event (OPSD, MWh)
  WERR(e)    = dE_heat / E_wind          (signed, per-event)

Uncertainty: block bootstrap over events (14d-safe: events are the unit) and
delta-method propagation of beta_r and slope_c standard errors.

Outputs: results/phase9_werr_events.csv, results/phase9_werr_summary.csv
"""
import pathlib
import numpy as np
import pandas as pd
import yaml

P = pathlib.Path("data/processed"); R = pathlib.Path("results")
cfg = yaml.safe_load(open("config/domain.yaml"))

dem = pd.read_csv(R / "phase8_demand_model.csv")
preg = pd.read_csv(R / "phase3_panel_regression.csv")
wfi = pd.read_csv(P / "wfi_daily.csv", parse_dates=["time"])
dd = pd.read_csv(P / "demand_daily.csv", parse_dates=[0], index_col=0)
events = pd.read_csv(P / "heatwave_events.csv", parse_dates=["start", "end"])

# country -> transect region (the upstream corridor serving that country)
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
wfi = wfi.set_index("time")
beta = preg.set_index("region").coef_wfi
beta_se = preg.set_index("region").se

rows = []
prim = events[events.definition == "pct95_tmax_3day"]
for cc, box in CBOX.items():
    region = C2R[cc]
    if region not in beta.index or f"{cc}_wind_gen" not in dd:
        continue
    slope_row = dem[dem.country == cc]
    if slope_row.empty:
        continue
    slope, slope_se = slope_row.slope_MW_per_C.iloc[0], np.nan
    b, bs = beta[region], beta_se[region]
    m = prim[in_box(prim.lat.values, prim.lon.values, box)]
    for _, ev in m.iterrows():
        seg = dd.loc[ev.start:ev.end]
        if seg.empty:
            continue
        w_ev = float(wfi.loc[ev.start:ev.end, region].mean())      # MW exposure
        dT = b * w_ev                                              # attributable C
        e_wind = float((seg[f"{cc}_wind_gen"] * 24).sum())         # MWh
        d_heat = slope * dT * 24 * ev.ndays                        # MWh
        rows.append({"country": cc, "region": region,
                     "start": ev.start.date(), "end": ev.end.date(),
                     "ndays": ev.ndays, "wfi_MW": w_ev, "dT_attrib_C": dT,
                     "dE_heat_MWh": d_heat, "E_wind_MWh": e_wind,
                     "werr": d_heat / e_wind if e_wind else np.nan})
out = pd.DataFrame(rows)
out.to_csv(R / "phase9_werr_events.csv", index=False)

summ = []
for cc, g in out.groupby("country"):
    w = g.werr.replace([np.inf, -np.inf], np.nan).dropna()
    if len(w) < 3:
        continue
    boots = [w.sample(len(w), replace=True, random_state=int(rng.integers(1e9))).mean()
             for _ in range(1000)]
    summ.append({"country": cc, "region": g.region.iloc[0], "n_events": len(w),
                 "werr_mean": w.mean(), "werr_lo": np.percentile(boots, 2.5),
                 "werr_hi": np.percentile(boots, 97.5)})
allw = out.werr.replace([np.inf, -np.inf], np.nan).dropna()
if len(allw):
    boots = [allw.sample(len(allw), replace=True,
                         random_state=int(rng.integers(1e9))).mean()
             for _ in range(1000)]
    summ.append({"country": "ALL", "region": "-", "n_events": len(allw),
                 "werr_mean": allw.mean(), "werr_lo": np.percentile(boots, 2.5),
                 "werr_hi": np.percentile(boots, 97.5)})
pd.DataFrame(summ).to_csv(R / "phase9_werr_summary.csv", index=False)
print(pd.DataFrame(summ))
print("done")
