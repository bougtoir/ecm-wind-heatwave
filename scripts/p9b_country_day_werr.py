#!/usr/bin/env python3
"""Phase 9b: country-day WERR (WERR_CD) — energy-accounting estimand.

Motivation (GATE 1 finding): the event-level WERR assigns each pixel-event
the whole country's actual wind generation over its days. 3,017 events map
to only 3,213 unique country-days (mean multiplicity 5.4x; DE 9.9x), so
event-level pooling reuses the same E_wind many times and overweights
pixel-dense regions and small denominators.

Country-day estimand (primary):
  WERR_CD = sum_{c,d in eligible} dE_heat(c,d) / sum_{c,d} E_wind(c,d)

  dE_heat(c,d) = slope_final_c * dT(c,d) * 24 * coverage(c,d)   [MWh]
  dT(c,d)      = beta_region(c) * wfi_region(c,d)               [C]
  coverage(c,d)= active pixels(c,d) / N_pixels(c)               [0,1]
  E_wind(c,d)  = wind_gen_c(d) * 24                             [MWh]

Eligible country-day (c,d): >=1 primary (pct95_tmax_3day) heatwave
pixel-event active in that country box on day d, AND demand_daily has
wind generation for c on d. Demand response is applied ONCE per
country-day; actual wind generation enters at most once per country-day.

Weighting: no population/load weights available; pixel-coverage fraction
is the prespecified transparent alternative (only the covered share of
national demand is treated as responding). Unweighted variant reported
as sensitivity. GB slope_final is 0 by the EB shrinkage rule: its days
contribute E_wind but zero dE_heat (documented, sensitivity excludes GB).

Uncertainty: (a) two-way block bootstrap, resampling countries and
calendar years with replacement (B=1000, seed from config); (b) delta
method on slope_se and beta_se per country-day; (c) LOO per country;
(d) alternate demand model m2_slope; (e) unweighted coverage variant.

Outputs:
  results/country_day_werr.csv          (per country-day)
  results/country_day_werr_summary.csv  (per-country + ALL estimands)
"""
import pathlib
import numpy as np
import pandas as pd
import yaml

P = pathlib.Path("data/processed"); R = pathlib.Path("results")
cfg = yaml.safe_load(open("config/domain.yaml"))
rng = np.random.default_rng(cfg["random_seed"])

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

dem = pd.read_csv(R / "demand_model_comparison.csv").set_index("country")
preg = pd.read_csv(R / "phase3_panel_regression.csv").set_index("region")
wfi = pd.read_csv(P / "wfi_daily.csv", parse_dates=["time"]).set_index("time")
dd = pd.read_csv(P / "demand_daily.csv", parse_dates=[0], index_col=0)
events = pd.read_csv(P / "heatwave_events.csv", parse_dates=["start", "end"])
prim = events[events.definition == "pct95_tmax_3day"]

# --- build per-country-day exposure frame ------------------------------
rows = []
log_zero_den = 0
for cc, box in CBOX.items():
    region = C2R[cc]
    col = f"{cc}_wind_gen"
    if region not in preg.index or col not in dd or cc not in dem.index:
        continue
    m = prim[in_box(prim.lat.values, prim.lon.values, box)]
    npix = m[["lat", "lon"]].drop_duplicates().shape[0]
    if npix == 0 or m.empty:
        continue
    b, bs = preg.loc[region, "coef_wfi"], preg.loc[region, "se"]
    sl, sls = dem.loc[cc, "slope_final"], dem.loc[cc, "se_final"]
    sl_m2, sls_m2 = dem.loc[cc, "m2_slope"], dem.loc[cc, "m2_se"]
    # active-pixel map: date -> count of distinct pixels with an event covering it
    active = {}
    for _, ev in m.iterrows():
        for d in pd.date_range(ev.start, ev.end):
            s = active.setdefault(d, set())
            s.add((ev.lat, ev.lon))
    wser = wfi[region]
    gser = dd[col]
    for d, pix in active.items():
        if d not in gser.index or d not in wser.index:
            continue
        gen = gser.loc[d]
        if pd.isna(gen):
            continue
        e_wind = float(gen * 24.0)
        if e_wind <= 0:
            log_zero_den += 1
            continue
        cov = len(pix) / npix
        w = float(wser.loc[d])
        dT = b * w
        rows.append({"country": cc, "date": d.date(), "region": region,
                     "n_active_pixels": len(pix), "n_pixels_box": npix,
                     "coverage_frac": cov, "wfi_MW": w,
                     "dT_attrib_C": dT,
                     "dE_heat_MWh": sl * dT * 24.0 * cov,
                     "dE_heat_MWh_unweighted": sl * dT * 24.0,
                     "dE_heat_MWh_m2": sl_m2 * dT * 24.0 * cov,
                     "E_wind_MWh": e_wind,
                     "dE_se_MWh": 24.0 * cov * np.sqrt(
                         (sls * dT) ** 2 + (sl * bs * w) ** 2)})
cd = pd.DataFrame(rows).sort_values(["country", "date"]).reset_index(drop=True)
cd["year"] = pd.to_datetime(cd["date"]).dt.year
cd.to_csv(R / "country_day_werr.csv", index=False)
print(f"zero/nonpositive-denominator country-days excluded: {log_zero_den}")
print(f"country-days: {len(cd)}  countries: {cd.country.nunique()}")

# --- summaries ----------------------------------------------------------
def ratio(g, num="dE_heat_MWh"):
    return g[num].sum() / g["E_wind_MWh"].sum()

summ = []
for cc, g in cd.groupby("country"):
    summ.append({"country": cc, "region": g.region.iloc[0],
                 "n_country_days": len(g),
                 "sum_dE_heat_MWh": g.dE_heat_MWh.sum(),
                 "sum_E_wind_MWh": g.E_wind_MWh.sum(),
                 "werr_cd": ratio(g),
                 "werr_cd_unweighted": ratio(g, "dE_heat_MWh_unweighted"),
                 "werr_cd_m2": ratio(g, "dE_heat_MWh_m2"),
                 "coverage_mean": g.coverage_frac.mean()})

allrow = {"country": "ALL", "region": "-", "n_country_days": len(cd),
          "sum_dE_heat_MWh": cd.dE_heat_MWh.sum(),
          "sum_E_wind_MWh": cd.E_wind_MWh.sum(),
          "werr_cd": ratio(cd),
          "werr_cd_unweighted": ratio(cd, "dE_heat_MWh_unweighted"),
          "werr_cd_m2": ratio(cd, "dE_heat_MWh_m2"),
          "coverage_mean": cd.coverage_frac.mean()}
summ.append(allrow)
S = pd.DataFrame(summ)

# equal-country summary: unweighted mean of per-country ratios
S.loc[S.country == "ALL", "werr_cd_equal_country"] = \
    S.loc[S.country != "ALL", "werr_cd"].mean()

# two-way block bootstrap: countries x years, ratio-of-sums recomputed
countries = cd.country.unique(); years = cd.year.unique()
B = 1000
boots = []
for _ in range(B):
    cs = rng.choice(countries, size=len(countries), replace=True)
    ys = rng.choice(years, size=len(years), replace=True)
    num = den = 0.0
    for c in cs:
        gc = cd[cd.country == c]
        for y in ys:
            gy = gc[gc.year == y]
            num += gy.dE_heat_MWh.sum(); den += gy.E_wind_MWh.sum()
    if den > 0:
        boots.append(num / den)
lo, hi = np.percentile(boots, [2.5, 97.5])
S.loc[S.country == "ALL", "boot_lo"] = lo
S.loc[S.country == "ALL", "boot_hi"] = hi

# delta-method CI on pooled ratio
num, den = cd.dE_heat_MWh.sum(), cd.E_wind_MWh.sum()
v = (cd.dE_se_MWh ** 2).sum() / den ** 2   # Var(num)/den^2, den fixed
S.loc[S.country == "ALL", "delta_se"] = np.sqrt(v)
S.loc[S.country == "ALL", "delta_lo"] = num / den - 1.96 * np.sqrt(v)
S.loc[S.country == "ALL", "delta_hi"] = num / den + 1.96 * np.sqrt(v)

# LOO
for cc in countries:
    g = cd[cd.country != cc]
    S.loc[S.country == "ALL", f"loo_{cc}"] = g.dE_heat_MWh.sum() / g.E_wind_MWh.sum()

# GB-excluded sensitivity (zero-slope plug-in)
g = cd[cd.country != "GB"]
S.loc[S.country == "ALL", "werr_cd_excl_GB"] = g.dE_heat_MWh.sum() / g.E_wind_MWh.sum()

S.to_csv(R / "country_day_werr_summary.csv", index=False)
print(S[["country", "n_country_days", "werr_cd", "werr_cd_unweighted",
         "werr_cd_m2", "coverage_mean"]].to_string(index=False))
print(f"ALL WERR_CD={allrow['werr_cd']:.4f} boot[{lo:.4f},{hi:.4f}] "
      f"delta[{num/den-1.96*np.sqrt(v):.4f},{num/den+1.96*np.sqrt(v):.4f}]")
print("done")
