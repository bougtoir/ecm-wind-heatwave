#!/usr/bin/env python3
"""Download OSM wind-turbine generators via Overpass, 2-degree tiles, resumable."""
import csv, pathlib, random, time, urllib.parse, urllib.request

MIRRORS = [
    "https://overpass.private.coffee/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]
# country -> (south, west, north, east)
COUNTRIES = {
    "DE": (47.0, 5.0, 55.5, 15.5), "DK": (54.0, 7.5, 58.0, 13.0),
    "NL": (50.5, 3.0, 54.0, 7.5), "BE": (49.4, 2.5, 51.6, 6.5),
    "FR": (42.0, -5.5, 51.2, 9.0), "GB": (49.5, -11.0, 59.5, 2.5),
    "IE": (51.0, -11.0, 55.5, -5.0), "ES": (36.0, -9.5, 44.0, 4.5),
    "PT": (36.5, -10.0, 42.5, -6.0), "IT": (36.0, 6.0, 47.5, 19.0),
    "PL": (49.0, 14.0, 55.0, 24.5), "SE": (55.0, 10.5, 69.5, 24.5),
    "NO": (57.5, 4.0, 71.5, 31.0), "FI": (59.5, 19.0, 70.5, 32.0),
    "AT": (46.0, 9.5, 49.2, 17.5), "CZ": (48.5, 12.0, 51.2, 19.0),
}
STEP = 2.0
OUT = pathlib.Path("data/raw/turbines/osm/tiles")
OUT.mkdir(parents=True, exist_ok=True)

Q = ('[out:csv(::lat,::lon,"start_date","generator:output:electricity","name";true;"|")]'
     '[timeout:120];'
     '(node["power"="generator"]["generator:source"="wind"]({s},{w},{n},{e});'
     'way["power"="generator"]["generator:source"="wind"]({s},{w},{n},{e}););'
     'out center;')

def tiles():
    for cc, (s, w, n, e) in COUNTRIES.items():
        lat = s
        while lat < n:
            lon = w
            while lon < e:
                yield cc, lat, lon, min(lat + STEP, n), min(lon + STEP, e)
                lon += STEP
            lat += STEP

def fetch(q, mirror):
    req = urllib.request.Request(mirror, data=urllib.parse.urlencode({"data": q}).encode())
    with urllib.request.urlopen(req, timeout=240) as r:
        return r.read()

pending, done, failed = 0, 0, 0
for cc, s, w, n, e in tiles():
    dst = OUT / f"{cc}_{s:.1f}_{w:.1f}.csv"
    if dst.exists() and dst.stat().st_size > 50:
        done += 1
        continue
    pending += 1
    q = Q.format(s=s, w=w, n=n, e=e)
    ok = False
    for attempt in range(10):
        mirror = MIRRORS[attempt % len(MIRRORS)]
        try:
            body = fetch(q, mirror)
            if not body.startswith(b"@lat"):
                raise RuntimeError(body[:150].decode("utf-8", "ignore"))
            dst.write_bytes(body)
            nrows = body.count(b"\n") - 1
            print(dst.name, "OK", nrows, flush=True)
            ok = True
            break
        except Exception as ex:
            print(dst.name, "attempt", attempt, mirror.split("/")[2], str(ex)[:100], flush=True)
            time.sleep(10 + attempt * 8 + random.random() * 10)
    if not ok:
        failed += 1
        print(dst.name, "FAILED", flush=True)
    time.sleep(3 + random.random() * 4)

print(f"DONE pending={pending} done={done} failed={failed}", flush=True)
