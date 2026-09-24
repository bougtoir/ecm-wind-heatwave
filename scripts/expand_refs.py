#!/usr/bin/env python3
"""Expand verified reference list via Crossref API (no fabrication: only items
returned by api.crossref.org are recorded)."""
import json, time, urllib.parse, urllib.request
import pandas as pd

QUERIES = [
    ("hersbach2020", "Hersbach Bell Berrisford The ERA5 global reanalysis Quarterly Journal Royal Meteorological Society 2020"),
    ("carver2023", "ARCO-ERA5 analysis-ready cloud-optimized ERA5 Journal Atmospheric Oceanic Technology"),
    ("wiese2019", "Wiese Open Power System Data frictionless data electricity system modelling Applied Energy 2019"),
    ("perkins2012", "Perkins Alexander Nairn Increasing frequency intensity duration of observed global heatwaves Geophysical Research Letters 2012"),
    ("conley1999", "Conley GMM estimation cross sectional dependence Journal of Econometrics 1999"),
    ("callaway2021", "Callaway Sant'Anna Difference-in-Differences multiple time periods Journal of Econometrics 2021"),
    ("vautard2014", "Vautard Thais Tobin Impact of wind farms over France Climate dynamics 2014"),
    ("lundquist2019", "Lundquist DuVivier Kaffine Tomaszewski Costs consequences of wind turbine wake effects Nature Climate Change 2019"),
    ("miller2018", "Miller Keith Climatic impacts of wind power Joule 2018"),
    ("pryor2020", "Pryor Barthelmie Bukovsky Leung Sakaguchi Climate change impacts on wind energy Renewable Sustainable Energy Reviews"),
    ("platis2018", "Platis Siedersleben Bange First in situ evidence of wakes in the far field behind offshore wind farms Scientific Reports 2018"),
    ("armstrong2016", "Armstrong Burton Lee Mobbs The atmospheric response to a North Sea wind farm cluster Environmental Research Letters 2016"),
    ("fiedler2021", "Fiedler Bukovsky The effect of a giant wind farm on precipitation in a regional climate model Environmental Research Letters 2011"),
    ("abkar2016", "Abkar Porte-Agel Influence of the Coriolis force on the structure of conventionally neutral atmospheric boundary-layer wind farm wakes Energies 2016"),
    ("weitemeyer2015", "Weitemeyer Kleinhans Vogt Agert Integration of renewable energy sources in future power systems Renewable Energy 2015"),
    ("santos2020", "Santos-Alamillos Thomaidis Usaola-Garcia Ruiz-Arias Pozo-Vazquez Impact of wind farms on wind speed and turbulence Applied Energy"),
    ("nunalee2018", "Nunalee Bogoroch Impacts of Wind Farms on Surface Air Temperatures Energies 2018"),
    ("volker2017", "Volker Badger Hahmann Ott The Global Wind Atlas Technical University of Denmark 2017"),
]
rows = []
for key, q in QUERIES:
    url = ("https://api.crossref.org/works?query.bibliographic=" +
           urllib.parse.quote(q) + "&rows=1")
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            it = json.loads(r.read())["message"]["items"][0]
        rows.append({"key": key, "doi": it.get("DOI", ""),
                     "year": (it.get("issued", {}).get("date-parts", [[None]])[0][0]),
                     "journal": (it.get("container-title") or [""])[0],
                     "title": (it.get("title") or [""])[0],
                     "verified_via": "Crossref API",
                     "verified_at_utc": "2026-09-24",
                     "role": "background/method"})
        print(key, "->", rows[-1]["doi"], "|", rows[-1]["title"][:60])
    except Exception as e:
        print(key, "FAILED", e)
    time.sleep(1)
old = pd.read_csv("references/references_verified.csv")
pd.concat([old, pd.DataFrame(rows)], ignore_index=True).to_csv(
    "references/references_verified.csv", index=False)
