#!/usr/bin/env python3
"""Generate WRF windturbines.txt files for each deployment scenario.

Input : data/processed/turbines.csv (unified register).
Output: wrf/scenario_SXX/windturbines.txt
WRF-Fitch format: one turbine per line: lat lon hubheight_m rotordiam_m
standh_m ? -> standard file has (lat, lon) then turbine spec lines.
Usage: python gen_windturbines.py <scenario>
"""
import sys
import pandas as pd

tb = pd.read_csv("data/processed/turbines.csv")
tb["year"] = pd.to_datetime(tb["commissioning"], errors="coerce").dt.year

SCEN = {"S0": -1, "S50": 2005, "S100": 2010, "S150": 2021,
        "S150u": 2021, "S150d": 2021}
scen = sys.argv[1]
assert scen in SCEN
yr = SCEN[scen]
act = tb if yr < 0 else tb[tb.year <= yr]
act = act.copy()
if scen == "S150u":          # upwind = west for westerlies
    act["lon"] -= 2.0
elif scen == "S150d":
    act["lon"] += 2.0
hub = act.hub_height_m.fillna(80).clip(20, 200)
rot = act.rotor_diameter_m.fillna(90).clip(20, 250)
out = f"wrf/scenario_{scen}/windturbines.txt"
with open(out, "w") as f:
    for _, r in act.iterrows():
        f.write(f"{r.lat:.5f} {r.lon:.5f}\n")
print(scen, len(act), "->", out)
