#!/usr/bin/env python3
"""Parse MaStR EinheitenWind.xml inside the Gesamtdatenexport zip -> mastr_wind.csv.

Fields: EinheitMastrNummer, NameStromerzeugungseinheit, Breitengrad,
Laengengrad, Nettonennleistung (kW), Inbetriebnahmedatum,
WindAnLandOderAufSee, Nabenhoehe, Rotordurchmesser, EinheitBetriebsstatus.
XML is UTF-16; parsed by regex (single file, ~44k units).
"""
import csv, pathlib, re, zipfile

ZIP = pathlib.Path("data/raw/turbines/Gesamtdatenexport_20260924.zip")
OUT = pathlib.Path("data/raw/turbines/mastr_wind.csv")

FIELDS = ["EinheitMastrNummer", "NameStromerzeugungseinheit", "Breitengrad",
          "Laengengrad", "Nettonennleistung", "Inbetriebnahmedatum",
          "WindAnLandOderAufSee", "Nabenhoehe", "Rotordurchmesser",
          "EinheitBetriebsstatus", "Hersteller", "Typenbezeichnung"]

def val(block, tag):
    m = re.search(rf"<{tag}>(.*?)</{tag}>", block, flags=re.S)
    return m.group(1).strip() if m else ""

def main():
    zf = zipfile.ZipFile(ZIP)
    data = zf.read("EinheitenWind.xml").decode("utf-16", "ignore")
    blocks = re.findall(r"<EinheitWind>.*?</EinheitWind>", data, flags=re.S)
    print("units:", len(blocks))
    rows = []
    for b in blocks:
        r = {k: val(b, k) for k in FIELDS}
        try:
            r["capacity_mw"] = float(r["Nettonennleistung"]) / 1000.0
        except Exception:
            r["capacity_mw"] = ""
        r["offshore"] = r["WindAnLandOderAufSee"] not in ("", "888", "0")
        try:
            r["offshore"] = int(r["WindAnLandOderAufSee"]) in (889, 890)
        except Exception:
            pass
        rows.append({
            "mastr": r["EinheitMastrNummer"], "name": r["NameStromerzeugungseinheit"],
            "lat": r["Breitengrad"], "lon": r["Laengengrad"],
            "capacity_mw": r["capacity_mw"],
            "commissioning": r["Inbetriebnahmedatum"],
            "offshore": r["offshore"],
            "rotor_diameter_m": r["Rotordurchmesser"],
            "hub_height_m": r["Nabenhoehe"],
            "status": r["EinheitBetriebsstatus"],
        })
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print("wrote", OUT, len(rows))

if __name__ == "__main__":
    main()
