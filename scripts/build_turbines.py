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
        d = pd.read_excel(dk, sheet_name=0, header=None)
        # locate header row containing 'Navn'/'effect'
        hdr = d.index[d.apply(lambda r: r.astype(str).str.contains("effect|Effect|Kapacitet|MW", case=False).any(), axis=1)]
        print("dk header candidates:", hdr.tolist()[:5], "shape", d.shape)
        # columns are parsed in the dedicated step below after header detection
        d.columns = d.iloc[hdr[0]].astype(str).str.strip() if len(hdr) else d.columns
        d = d.iloc[hdr[0] + 1:] if len(hdr) else d
        cols = {c.lower(): c for c in d.columns}
        lat_c = next((c for c in d.columns if "breddegrad" in c.lower() or "latitude" in c.lower() or "utm" in c.lower()), None)
        lon_c = next((c for c in d.columns if "l\xe6ngdegrad" in c.lower() or "longitude" in c.lower() or "utm" in c.lower()), None)
        cap_c = next((c for c in d.columns if "effect" in c.lower() or "kapacitet" in c.lower() or "kw" in c.lower()), None)
        com_c = next((c for c in d.columns if "tilkoblet" in c.lower() or "drift" in c.lower() or "commission" in c.lower()), None)
        print("dk cols:", lat_c, lon_c, cap_c, com_c, "|", list(d.columns)[:15])
        if lat_c and cap_c:
            fr = pd.DataFrame({
                "source": "dk_stamdata", "country": "Denmark",
                "lat": pd.to_numeric(d[lat_c], errors="coerce"),
                "lon": pd.to_numeric(d[lon_c], errors="coerce") if lon_c else pd.NA,
                "capacity_mw": pd.to_numeric(d[cap_c], errors="coerce") / (1000 if "kw" in cap_c.lower() else 1),
                "commissioning": pd.to_datetime(d[com_c], errors="coerce") if com_c else pd.NaT,
                "offshore": d.apply(lambda r: "hav" in str(r).lower(), axis=1) if "hav" else False,
                "rotor_diameter_m": pd.NA, "hub_height_m": pd.NA, "name": "DK turbine",
            })
            frames.append(fr)
            print("dk", len(fr))
    except Exception as e:
        print("dk parse FAILED:", e)

# ---- OSM tiles ----
rows = []
for f in sorted((RAW / "osm/tiles").glob("*.csv")):
    try:
        t = pd.read_csv(f, sep="\t", on_bad_lines="skip")
        if len(t) > 1:
            t["cc"] = f.name.split("_")[0]
            rows.append(t)
    except Exception:
        pass
if rows:
    osm = pd.concat(rows, ignore_index=True)
    osm.columns = [c.lstrip("@") for c in osm.columns]
    cc = osm["cc"]
    fr = pd.DataFrame({
        "source": "osm", "country": cc,
        "lat": pd.to_numeric(osm["lat"], errors="coerce"),
        "lon": pd.to_numeric(osm["lon"], errors="coerce"),
        "capacity_mw": pd.to_numeric(
            osm.get("generator:output:electricity", pd.Series(dtype=str)).astype(str)
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
