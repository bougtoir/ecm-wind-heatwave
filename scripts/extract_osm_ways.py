#!/usr/bin/env python3
"""Append way-tagged wind turbines to existing osm_extracted CSVs (disk-backed index)."""
import csv, pathlib
import osmium

IN = pathlib.Path("data/raw/turbines/osm_pbf")
OUT = pathlib.Path("data/raw/turbines/osm_extracted")

def is_wind(t):
    return t.get("power") == "generator" and (
        t.get("generator:source") == "wind"
        or "wind" in (t.get("generator:type") or ""))

class W(osmium.SimpleHandler):
    def __init__(self, emit):
        super().__init__()
        self.emit = emit
    def way(self, w):
        if not is_wind(w.tags):
            return
        try:
            la = [n.location.lat for n in w.nodes if n.location.valid()]
            lo = [n.location.lon for n in w.nodes if n.location.valid()]
            if la:
                self.emit(sum(la) / len(la), sum(lo) / len(lo), w.tags)
        except Exception:
            pass

for cc in ["DE", "FR", "IT"]:
    dst = OUT / f"{cc}.csv"
    with open(dst, "a", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        def emit(lat, lon, tags):
            w.writerow([f"{lat:.7f}", f"{lon:.7f}",
                        tags.get("start_date", ""),
                        tags.get("generator:output:electricity", ""),
                        (tags.get("name", "") or "").replace("\t", " ")])
        try:
            W(emit).apply_file(str(IN / f"{cc}.osm.pbf"), locations=True,
                               idx=f"sparse_file_array,data/tmp/{cc}_loc.idx")
        except Exception as e:
            print(cc, "way error", str(e)[:150], flush=True)
    print(cc, "rows", sum(1 for _ in open(dst)) - 1, flush=True)
print("DONE")
