#!/usr/bin/env python3
"""Graphical abstract — all numbers derived from canonical outputs at build
time (no literals). Reproduces the 4-box causal-chain layout:
wind extraction -> atmosphere -> heatwaves -> demand/WERR.
"""
import pathlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

F = pathlib.Path("figs"); F.mkdir(exist_ok=True)
P = pathlib.Path("data/processed"); R = pathlib.Path("results")

w9 = pd.read_csv(R / "werr_pooled_summary.csv").iloc[0]
ev = pd.read_csv(P / "heatwave_events.csv")
n_pix = int((ev.definition == "pct95_tmax_3day").sum())
tb = pd.read_csv(P / "turbines.csv")
n_tb = len(tb)

fig, ax = plt.subplots(figsize=(10, 4.2), dpi=300)
ax.set_xlim(0, 10); ax.set_ylim(0, 4.2); ax.axis("off")

boxes = [
    (0.25, "Wind-energy\nextraction", f"({n_tb//1000}k turbines)", "#dcebf7"),
    (2.80, "Atmosphere", "wakes · moisture\nflux MFC", "#e4f2dc"),
    (5.35, "Heatwaves", f"Tmax pct95, {n_pix//1000}k\nevents", "#fdeadd"),
    (7.90, "Demand", "WERR =\nΔE/E_wind", "#fbdfe0"),
]
labels = ["perturbs", "may shift", "drives"]
for i, (x, title, sub, color) in enumerate(boxes):
    bb = FancyBboxPatch((x, 1.55), 1.85, 1.5,
                        boxstyle="round,pad=0.12,rounding_size=0.18",
                        fc=color, ec="k", lw=1.6)
    ax.add_patch(bb)
    ax.text(x + 0.925, 2.55, title, ha="center", va="center",
            fontsize=13, fontweight="bold")
    ax.text(x + 0.925, 1.95, sub, ha="center", va="center", fontsize=10.5,
            fontweight="bold")
    if i < 3:
        ar = FancyArrowPatch((x + 2.02, 2.3), (x + 2.50, 2.3),
                             arrowstyle="-|>", mutation_scale=26, lw=3, color="k")
        ax.add_patch(ar)
        ax.text(x + 2.26, 2.62, labels[i], ha="center", fontsize=10, style="italic")

ax.text(5.0, 0.72,
        f"Pooled WERR = {w9.werr_mean:.2f} [{w9.werr_lo:.2f},{w9.werr_hi:.2f}]: "
        "no robust aggregate rebound;",
        ha="center", fontsize=11.5, style="italic")
ax.text(5.0, 0.32,
        "localized positive rebound on dense North-Sea corridors",
        ha="center", fontsize=11.5, style="italic")

fig.savefig(F / "graphical_abstract.png", dpi=300, bbox_inches="tight")
fig.savefig(F / "graphical_abstract.pdf", bbox_inches="tight")
print("graphical_abstract written: pooled", w9.werr_mean, "events", n_pix)
