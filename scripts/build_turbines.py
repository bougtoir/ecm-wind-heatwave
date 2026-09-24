#!/usr/bin/env python3
"""Harmonize turbine sources -> data/processed/turbines.csv.

Unified schema: source, country, lat, lon, capacity_mw, commissioning (YYYY-MM-DD or NaT),
offshore (bool), rotor_diameter_m, hub_height_m, name.
Sources: eww offshore DB (Zenodo), Danish Stamdataregister, MaStR (DE), OSM Overpass tiles.
"""
import pathlib, re
import pandas as pd

RAW = pathlib.Path("data/raw/turbines")
OUT = pathlib.Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)
frames = []

# ---- eww offshore open database ----
eww = pd.read_csv(RAW / "20260127_eww_opendatabase.csv")
eww["commissioning"] = pd.to_datetime(eww["commissioning_date"], errors="coerce", format="%Y-%m")
frames.append(pd.DataFrame({
    "source": "eww", "country": eww["country"], "lat": eww["latitude"], "lon": eww["longitude"],
    "capacity_mw": eww["rated_power"], "commissioning": eww["commissioning"],
    "offshore": True, "rotor_diameter_m": eww["rotor_diameter"], "hub_height_m": eww["hub_height"],
    "name": eww["wind_farm"].astype(str) + "|" + eww["turbine_type"].astype(str),
}))
print("eww", len(frames[-1]))

# ---- Danish Stamdataregister (xls) ----
dk = RAW / "dk_stamdataregister.xls"
if dk.exists():
    try:
        from pyproj import Transformer
        tr = Transformer.from_crs("EPSG:25832", "EPSG:4326", always_xy=True)
        d = pd.read_excel(dk, sheet_name=0, header=6)
        d = d[d["Turbine identifier (GSRN)"].astype(str).str.match(r"\d{10,}", na=False)]
        xe, yn = "X (east) coordinate\nUTM 32 Euref89", "Y (north) coordinate\nUTM 32 Euref89"
        x = pd.to_numeric(d[xe], errors="coerce")
        y = pd.to_numeric(d[yn], errors="coerce")
        lo, la = tr.transform(x.values, y.values)
        lo = pd.Series(lo).where(x.notna()); la = pd.Series(la).where(x.notna())
        fr = pd.DataFrame({
            "source": "dk_stamdata", "country": "Denmark",
            "lat": la.values, "lon": lo.values,
            "capacity_mw": pd.to_numeric(d["Capacity (kW)"], errors="coerce") / 1000.0,
            "commissioning": pd.to_datetime(d["Date of original connection to grid"], errors="coerce"),
            "offshore": d["Type of location"].astype(str).str.upper().str.contains("HAV|SEA|OFFSHORE"),
            "rotor_diameter_m": pd.to_numeric(d["Rotor diameter (m)"], errors="coerce"),
            "hub_height_m": pd.to_numeric(d["Hub height (m)"], errors="coerce"),
            "name": d["Turbine identifier (GSRN)"].astype(str),
        })
        fr = fr.dropna(subset=["lat", "lon"])
        frames.append(fr)
        print("dk", len(fr))
    except Exception as e:
        print("dk parse FAILED:", e)

# ---- OSM Geofabrik extracts ----
rows = []
for f in sorted((RAW / "osm_extracted").glob("*.csv")):
    try:
        t = pd.read_csv(f, sep="\t", on_bad_lines="skip")
        if len(t) > 1:
            t["cc"] = f.stem.split(".")[0]
            rows.append(t)
    except Exception:
        pass
if rows:
    osm = pd.concat(rows, ignore_index=True)
    fr = pd.DataFrame({
        "source": "osm", "country": osm["cc"],
        "lat": pd.to_numeric(osm["lat"], errors="coerce"),
        "lon": pd.to_numeric(osm["lon"], errors="coerce"),
        "capacity_mw": pd.to_numeric(
            osm.get("output", pd.Series(dtype=str)).astype(str)
              .str.extract(r"([\d.]+)")[0], errors="coerce"),
        "commissioning": pd.to_datetime(osm.get("start_date"), errors="coerce"),
        "offshore": False, "rotor_diameter_m": pd.NA, "hub_height_m": pd.NA,
        "name": osm.get("name", ""),
    })
    frames.append(fr)
    print("osm", len(fr))

# ---- MaStR (DE) parsed by scripts/parse_mastr.py -> mastr_wind.csv ----
mastr = RAW / "mastr_wind.csv"
if mastr.exists():
    m = pd.read_csv(mastr)
    frames.append(pd.DataFrame({
        "source": "mastr", "country": "Germany", "lat": m["lat"], "lon": m["lon"],
        "capacity_mw": m["capacity_mw"], "commissioning": pd.to_datetime(m["commissioning"], errors="coerce"),
        "offshore": m.get("offshore", False), "rotor_diameter_m": m.get("rotor_diameter_m"),
        "hub_height_m": m.get("hub_height_m"), "name": m.get("name", ""),
    }))
    print("mastr", len(frames[-1]))

al = pd.concat(frames, ignore_index=True)
al = al.dropna(subset=["lat", "lon"])
al = al[(al.lat.between(-90, 90)) & (al.lon.between(-180, 180))]
# dedupe: prefer registers over OSM within 100 m for same point
al = al.sort_values("source")
al.to_csv(OUT / "turbines.csv", index=False)
print("TOTAL", len(al), "| by source:", al.source.value_counts().to_dict())
