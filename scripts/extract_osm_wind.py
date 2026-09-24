#!/usr/bin/env python3
"""Extract wind turbines (power=generator + generator:source=wind) from .osm.pbf.

Two passes per file to bound memory:
  pass1: nodes only (no location index needed)
  pass2: ways only, centroid of member nodes (low-memory location index)
Output: data/raw/turbines/osm_extracted/{CC}.csv  (lat,lon,start_date,output,name)
"""
import csv, pathlib
import osmium

IN = pathlib.Path("data/raw/turbines/osm_pbf")
OUT = pathlib.Path("data/raw/turbines/osm_extracted")
OUT.mkdir(parents=True, exist_ok=True)

def is_wind(tags):
    return tags.get("power") == "generator" and (
        tags.get("generator:source") == "wind"
        or "wind" in (tags.get("generator:type") or ""))

class NodeHandler(osmium.SimpleHandler):
    def __init__(self, emit):
        super().__init__()
        self.emit = emit
    def node(self, n):
        if is_wind(n.tags) and n.location.valid():
            self.emit(n.location.lat, n.location.lon, n.tags)

class WayHandler(osmium.SimpleHandler):
    def __init__(self, emit):
        super().__init__()
        self.emit = emit
    def way(self, w):
        if not is_wind(w.tags):
            return
        try:
            lats = [nd.location.lat for nd in w.nodes if nd.location.valid()]
            lons = [nd.location.lon for nd in w.nodes if nd.location.valid()]
            if lats:
                self.emit(sum(lats) / len(lats), sum(lons) / len(lons), w.tags)
        except Exception:
            pass

def main():
    for pbf in sorted(IN.glob("*.osm.pbf")):
        cc = pbf.stem.split(".")[0]
        dst = OUT / f"{cc}.csv"
        if dst.exists() and dst.stat().st_size > 50 and not (OUT / f"{cc}.partial").exists():
            print(cc, "exists", flush=True)
            continue
        with open(dst, "w", newline="") as f:
            w = csv.writer(f, delimiter="\t")
            w.writerow(["lat", "lon", "start_date", "output", "name"])
            def emit(lat, lon, tags):
                w.writerow([f"{lat:.7f}", f"{lon:.7f}",
                            tags.get("start_date", ""),
                            tags.get("generator:output:electricity", ""),
                            (tags.get("name", "") or "").replace("\t", " ").replace("\n", " ")])
            try:
                NodeHandler(emit).apply_file(str(pbf))
            except Exception as e:
                print(cc, "node pass error:", str(e)[:150], flush=True)
            try:
                WayHandler(emit).apply_file(str(pbf), locations=True,
                                            idx="sparse_mem_array")
            except Exception as e:
                print(cc, "way pass error:", str(e)[:150], flush=True)
        n_rows = sum(1 for _ in open(dst)) - 1
        print(cc, "rows", n_rows, flush=True)
    print("DONE")

if __name__ == "__main__":
    main()
