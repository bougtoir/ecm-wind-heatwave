#!/usr/bin/env python3
"""Extract wind turbines (power=generator + generator:source=wind) from .osm.pbf files.
Streams nodes and ways; for ways uses the centroid of member-node locations.
Output: data/raw/turbines/osm_extracted/{CC}.csv with lat,lon,start_date,output,name
"""
import csv, pathlib, sys
import osmium

IN = pathlib.Path("data/raw/turbines/osm_pbf")
OUT = pathlib.Path("data/raw/turbines/osm_extracted")
OUT.mkdir(parents=True, exist_ok=True)

class WindHandler(osmium.SimpleHandler):
    def __init__(self, writer):
        super().__init__()
        self.w = writer
        self.loc = osmium.NodeLocationsForWays()
        self.loc.ignore_errors()

    def _is_wind(self, tags):
        return tags.get("power") == "generator" and (
            tags.get("generator:source") == "wind"
            or "wind" in (tags.get("generator:type") or ""))

    def _emit(self, lat, lon, tags):
        self.w.writerow([
            f"{lat:.7f}", f"{lon:.7f}",
            tags.get("start_date", ""),
            tags.get("generator:output:electricity", ""),
            (tags.get("name", "") or "").replace("\t", " ").replace("\n", " "),
        ])

    def node(self, n):
        if self._is_wind(n.tags) and n.location.valid():
            self._emit(n.location.lat, n.location.lon, n.tags)

    def way(self, w):
        if not self._is_wind(w.tags):
            return
        try:
            lats = [nd.location.lat for nd in w.nodes if nd.location.valid()]
            lons = [nd.location.lon for nd in w.nodes if nd.location.valid()]
            if lats:
                self._emit(sum(lats) / len(lats), sum(lons) / len(lons), w.tags)
        except Exception:
            pass

def main():
    for pbf in sorted(IN.glob("*.osm.pbf")):
        cc = pbf.stem.split(".")[0]
        dst = OUT / f"{cc}.csv"
        if dst.exists() and dst.stat().st_size > 50:
            print(cc, "exists", flush=True)
            continue
        n_rows = 0
        with open(dst, "w", newline="") as f:
            w = csv.writer(f, delimiter="\t")
            w.writerow(["lat", "lon", "start_date", "output", "name"])
            h = WindHandler(w)
            try:
                h.apply_file(str(pbf), locations=True, idx="flex_mem")
            except Exception as e:
                print(cc, "parse error:", str(e)[:200], flush=True)
        n_rows = sum(1 for _ in open(dst)) - 1
        print(cc, "rows", n_rows, flush=True)
    print("DONE")

if __name__ == "__main__":
    main()
