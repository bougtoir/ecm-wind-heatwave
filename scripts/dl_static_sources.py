#!/usr/bin/env python3
"""Acquire static raw inputs (turbine registers + OPSD electricity).

Downloads what has a stable public URL; for sources whose endpoint is
unstable, verifies presence and prints precise placement instructions.
Never overwrites existing raw files (persist rule).
"""
import hashlib, pathlib, sys, urllib.request, zipfile

RAW_T = pathlib.Path("data/raw/turbines"); RAW_E = pathlib.Path("data/raw/electricity")
RAW_T.mkdir(parents=True, exist_ok=True); RAW_E.mkdir(parents=True, exist_ok=True)

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()

def get(url, dest, unzip_member=None):
    if dest.exists():
        print("present", dest); return True
    try:
        print("downloading", url)
        urllib.request.urlretrieve(url, str(dest) + ".part")
        part = pathlib.Path(str(dest) + ".part")
        if unzip_member:
            with zipfile.ZipFile(part) as z:
                with z.open(unzip_member) as src, open(dest, "wb") as out:
                    out.write(src.read())
            part.unlink()
        else:
            part.rename(dest)
        print("saved", dest, dest.stat().st_size, sha256(dest)); return True
    except Exception as e:
        print("FAILED", url, "->", dest, ":", e)
        pathlib.Path(str(dest) + ".part").unlink(missing_ok=True)
        return False

ok = True
# eww offshore open database (Zenodo rec. 19879819)
ok &= get("https://zenodo.org/records/19879819/files/20260127_eww_opendatabase.csv",
          RAW_T / "20260127_eww_opendatabase.csv")
# OPSD time-series release 2020-10-06
ok &= get("https://data.open-power-system-data.org/time_series/2020-10-06/opsd-time_series-2020-10-06.zip",
          RAW_E / "opsd_time_series_60min_2020.csv",
          unzip_member="time_series_60min_singleindex.csv")
# MaStR full export
ok &= get("https://download.marktstammdatenregister.de/Gesamtdatenexport.zip",
          RAW_T / "Gesamtdatenexport.zip")

# Danish Stamdataregister: no stable direct URL -> presence check + instructions
dk = RAW_T / "dk_stamdataregister.xls"
if dk.exists():
    print("present", dk)
else:
    ok = False
    print("MISSING", dk,
          "\n  -> download the wind-turbine register XLS from the Danish Energy"
          "\n     Agency Stamdataregister portal and place it at this path.")

sys.exit(0 if ok else 1)
