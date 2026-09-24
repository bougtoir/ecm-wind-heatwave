#!/usr/bin/env python3
"""Download Geofabrik country .osm.pbf extracts (sequential, resumable via curl -C)."""
import pathlib, subprocess, sys

BASE = "https://download.geofabrik.de/europe"
REGIONS = {
    "DE": "germany", "DK": "denmark", "NL": "netherlands", "BE": "belgium",
    "FR": "france", "GB": "great-britain", "IE": "ireland-and-northern-ireland",
    "ES": "spain", "PT": "portugal", "IT": "italy", "PL": "poland",
    "SE": "sweden", "NO": "norway", "FI": "finland", "AT": "austria",
    "CZ": "czech-republic",
}
OUT = pathlib.Path("data/raw/turbines/osm_pbf")
OUT.mkdir(parents=True, exist_ok=True)

for cc, region in REGIONS.items():
    url = f"{BASE}/{region}-latest.osm.pbf"
    dst = OUT / f"{cc}.osm.pbf"
    if dst.exists() and dst.stat().st_size > 1_000_000:
        print(cc, "exists", dst.stat().st_size, flush=True)
        continue
    for attempt in range(6):
        r = subprocess.run(["curl", "-sL", "-C", "-", "--fail", "-o", str(dst), url])
        if r.returncode == 0:
            print(cc, "OK", dst.stat().st_size, flush=True)
            break
        print(cc, "attempt", attempt, "curl rc", r.returncode, flush=True)
        import time; time.sleep(20 + attempt * 20)
    else:
        print(cc, "FAILED", flush=True)
print("DONE")
