#!/usr/bin/env python3
"""Phase 11: manuscript figures (English labels, 300 dpi PNG + PDF)."""
import pathlib
import numpy as np
import pandas as pd
import xarray as xr
import yaml
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

F = pathlib.Path("figs"); F.mkdir(exist_ok=True)
P = pathlib.Path("data/processed"); R = pathlib.Path("results")
cfg = yaml.safe_load(open("config/domain.yaml"))
plt.rcParams.update({"font.size": 9, "figure.dpi": 130})

def save(fig, name):
    fig.tight_layout()
    fig.savefig(F / f"{name}.png", dpi=300)
    fig.savefig(F / f"{name}.pdf")
    plt.close(fig); print(name)

# ---- F1: turbines + transects + downstream boxes ----
tb = pd.read_csv(P / "turbines.csv")
fig, ax = plt.subplots(figsize=(6.2, 5.2))
sc = ax.scatter(tb.lon, tb.lat, s=0.3, c=tb.capacity_mw.fillna(1),
                cmap="viridis", alpha=0.5, vmin=0, vmax=8)
for name, tr in cfg["transects"].items():
    pts = np.array(tr["vertices"])
    ax.plot(pts[:, 0], pts[:, 1], lw=1.4, label=name.replace("_", " "))
    lc = pts[-1]
    ax.add_patch(plt.Rectangle((lc[0]-3, lc[1]-3), 6, 6,
                               fill=False, ls="--", lw=0.8, ec="k"))
ax.set_xlim(-15, 34.5); ax.set_ylim(36, 72)
ax.set_xlabel("Longitude (deg E)"); ax.set_ylabel("Latitude (deg N)")
ax.legend(fontsize=6, loc="lower right", framealpha=0.9)
fig.colorbar(sc, ax=ax, label="Turbine rated capacity (MW)", shrink=0.8)
ax.set_title("(a) Deployment & transects")
save(fig, "fig1_deployment")

# ---- F2: MFC climatology + transect flux seasonality ----
mfc = xr.open_dataset(P / "mfc_daily.nc")
tf = pd.read_csv(P / "transect_flux_daily.csv", parse_dates=["time"])
fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
im = ax[0].pcolormesh(mfc.longitude, mfc.latitude,
                      mfc.mfc.mean("time") * 86400, cmap="BrBG",
                      vmin=-0.5, vmax=0.5)
ax[0].set_title("(a) Mean MFC (kg m-2 day-1)")
fig.colorbar(im, ax=ax[0], shrink=0.8)
for i, c in enumerate(tf.columns[1:]):
    s = tf.set_index("time")[c] / 1e6
    s.rolling(30, center=True).mean().plot(
        ax=ax[1], label=c.replace("_", " "), lw=1, color=f"C{i}")
ax[1].set_ylabel("Transect flux (10^6 kg/s)")
ax[1].set_title("(b) Cross-transect moisture flux (30d mean)")
ax[1].legend(fontsize=6)
save(fig, "fig2_moisture")

# ---- F3: heatwave climatology ----
ev = pd.read_csv(P / "heatwave_events.csv", parse_dates=["start"])
prim = ev[ev.definition == "pct95_tmax_3day"]
fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
ax[0].hist2d(prim.lon, prim.lat, bins=[34, 25], cmap="magma")
ax[0].set_title("(a) Event count per cell (2000-2021)")
yy = prim.groupby("year").size()
ax[1].bar(yy.index, yy.values)
ax[1].set_title("(b) Events per year (primary def)")
ax[1].set_ylabel("pixel-events")
save(fig, "fig3_heatwaves")

# ---- F4: regional panel coefficients ----
pr = pd.read_csv(R / "phase3_panel_regression.csv")
fig, ax = plt.subplots(figsize=(6.5, 3.2))
y = np.arange(len(pr))
ax.errorbar(pr.coef_wfi * 1e4, y,
            xerr=1.96 * pr.boot_se * 1e4, fmt="o", ms=4)
ax.axvline(0, color="k", lw=0.6)
ax.set_yticks(y, pr.region.str.replace("_", " "))
ax.set_xlabel("beta_WFI (1e-4 degC per MW exposure)")
ax.set_title("(c) Panel effect of upstream deployment on Tmax anomaly")
save(fig, "fig4_panel")

# ---- F5: analog effects ----
a4 = pd.read_csv(R / "phase4_analog_effect.csv")
fig, ax = plt.subplots(figsize=(6.5, 3.2))
y = np.arange(len(a4))
ax.errorbar(a4.effect_C, y, xerr=1.96 * a4.boot_se, fmt="s", ms=4,
            color="darkred")
ax.axvline(0, color="k", lw=0.6)
ax.set_yticks(y, a4.region.str.replace("_", " "))
ax.set_xlabel("Circulation-matched high- vs low-WFI Tmax difference (degC)")
ax.set_title("(d) Analog-matched effect")
save(fig, "fig5_analogs")

# ---- F6: event study ----
es = pd.read_csv(R / "phase5_eventstudy.csv")
fig, ax = plt.subplots(figsize=(5.5, 3.2))
for oc, mk in [("hw_days", "o"), ("tmax_anom", "s")]:
    g = es[es.outcome == oc]
    ax.plot(g.rel_year, g["diff"], marker=mk, ms=4, label=oc)
ax.axvline(0, ls="--", color="k", lw=0.6); ax.axhline(0, lw=0.6, color="grey")
ax.set_xlabel("Years relative to treatment"); ax.legend()
ax.set_title("(e) Deployment event study")
save(fig, "fig6_eventstudy")

# ---- F7: falsification summary ----
f6 = pd.read_csv(R / "phase6_falsification.csv")
fig, ax = plt.subplots(figsize=(7, 3.6))
labels = f6.test + ("/" + f6.region).where(f6.region != "domain", "")
cols = ["firebrick" if p < 0.05 else "steelblue" for p in f6.p.fillna(1)]
ax.bar(range(len(f6)), f6.coef * 1e4, color=cols)
ax.set_xticks(range(len(f6)), [t[:22] for t in labels], rotation=70, ha="right",
              fontsize=6)
ax.axhline(0, lw=0.6, color="k")
ax.set_ylabel("coef (1e-4 degC/MW)")
ax.set_title("(f) Falsification battery")
save(fig, "fig7_falsification")

# ---- F8: WERR ----
w9 = pd.read_csv(R / "phase9_werr_summary.csv")
fig, ax = plt.subplots(figsize=(6.5, 3.4))
g = w9[w9.country != "ALL"]
y = np.arange(len(g))
ax.errorbar(g.werr_mean, y, xerr=[g.werr_mean - g.werr_lo, g.werr_hi - g.werr_mean],
            fmt="o", ms=4, color="teal")
allr = w9[w9.country == "ALL"].iloc[0]
ax.axvline(0, color="k", lw=0.6)
ax.axvline(allr.werr_mean, color="red", ls="--", lw=1,
           label=f"pooled {allr.werr_mean:.3f}")
ax.set_yticks(y, g.country)
ax.set_xlabel("WERR = dE_heat / E_wind (signed)")
ax.set_title("(g) Wind-induced Electricity Rebound Ratio")
ax.legend(fontsize=7)
save(fig, "fig8_werr")
print("all figs done")
