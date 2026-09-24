#!/usr/bin/env python3
"""Parse MaStR Gesamtdatenexport zip -> data/raw/turbines/mastr_wind.csv.

Streams XML members matching wind-unit files. Extracts per unit:
MastrNummer, name, coordinates (Laengengrad/Breitengrad when present on the
unit, otherwise via Lokation join), Nettonennleistung (kW),
Inbetriebnahmedatum, offshore flag (Lage/Cluster fields).
"""
import csv, pathlib, sys, zipfile
import xml.etree.ElementTree as ET

ZIP = pathlib.Path("data/raw/turbines/Gesamtdatenexport_20260924.zip")
OUT = pathlib.Path("data/raw/turbines/mastr_wind.csv")

def norm(tag):
    return tag.split("}")[-1]

def childtext(el, *names):
    want = set(names)
    for c in el.iter():
        if norm(c.tag) in want and c.text:
            return c.text.strip()
    return ""

def main():
    zf = zipfile.ZipFile(ZIP)
    names = zf.namelist()
    print(len(names), "members")
    wind = [n for n in names if "wind" in n.lower() or "Wind" in n]
    lok = [n for n in names if "lokation" in n.lower()]
    print("wind members:", wind[:10], "| lok members:", lok[:5])

    # pass 1: locations -> coordinates
    coords = {}
    for n in lok:
        with zf.open(n) as f:
            for ev, el in ET.iterparse(f, events=("end",)):
                if norm(el.tag) in ("Lokation", "Netzanschlusspunkt"):
                    mid = childtext(el, "MastrNummer", "LokationMastrNummer")
                    la = childtext(el, "Breitengrad")
                    lo = childtext(el, "Laengengrad")
                    if mid and la:
                        coords[mid] = (la, lo)
                    el.clear()
        print("lok done", n, len(coords), flush=True)

    rows = []
    for n in wind:
        if "einheit" not in n.lower() and "anlage" not in n.lower():
            continue
        with zf.open(n) as f:
            for ev, el in ET.iterparse(f, events=("end",)):
                if "wind" in norm(el.tag).lower() and norm(el.tag).endswith("einheit") is False:
                    pass
                if norm(el.tag).lower().startswith("einheitwind") or norm(el.tag) == "EinheitWind":
                    mid = childtext(el, "EinheitMastrNummer", "EegMastrNummer", "MastrNummer")
                    la = childtext(el, "Breitengrad")
                    lo = childtext(el, "Laengengrad")
                    lokid = childtext(el, "LokationMastrNummer")
                    if not la and lokid in coords:
                        la, lo = coords[lokid]
                    rows.append({
                        "mastr": mid,
                        "name": childtext(el, "Name", "EinheitName"),
                        "lat": la, "lon": lo,
                        "capacity_mw": "",
                        "kw": childtext(el, "Nettonennleistung", "Bruttoleistung", "Nennleistung"),
                        "commissioning": childtext(el, "Inbetriebnahmedatum"),
                        "offshore": childtext(el, "Lage", "WindparkLage", "Cluster"),
                    })
                    el.clear()
        print("parsed", n, len(rows), flush=True)

    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["mastr", "name", "lat", "lon", "capacity_mw",
                                        "kw", "commissioning", "offshore"])
        w.writeheader()
        for r in rows:
            try:
                r["capacity_mw"] = float(r["kw"]) / 1000.0 if r["kw"] else ""
            except Exception:
                r["capacity_mw"] = ""
            r["offshore"] = str(r["offshore"]).lower() in ("see", "offshore", "true", "1")
            w.writerow(r)
    print("wrote", OUT, len(rows))

if __name__ == "__main__":
    main()
