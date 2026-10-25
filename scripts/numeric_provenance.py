#!/usr/bin/env python3
"""GATE B: extract every numeric claim from deliverables (manuscript.docx,
cover_letter.md, highlights.txt) and match each to a canonical results/
or data/processed source within rounding tolerance.

Outputs:
  results/NUMERIC_PROVENANCE.csv
  stdout summary of unmatched / stale claims
"""
import re, json, pathlib
import numpy as np
import pandas as pd
from docx import Document

R = pathlib.Path("results"); P = pathlib.Path("data/processed")

# ---------- canonical value universe ----------
canon = []  # (path, key, value)


def add(path, key, val):
    try:
        canon.append((path, key, float(val)))
    except (TypeError, ValueError):
        pass


def add_csv(path):
    df = pd.read_csv(path)
    for i, r in df.iterrows():
        rowid = "|".join(str(v) for v in r.values[:2])
        for c in df.columns:
            add(str(path), f"{rowid}|{c}", r[c])


for f in R.glob("*.csv"):
    add_csv(f)
for f in P.glob("*.csv"):
    df = pd.read_csv(f)
    add(str(f), "n_rows", len(df))
    for c in df.select_dtypes("number").columns:
        s = df[c]
        for stat, v in [("mean", s.mean()), ("median", s.median()),
                        ("min", s.min()), ("max", s.max()), ("sum", s.sum())]:
            add(str(f), f"{c}|{stat}", v)
dta = json.load(open(R / "dT_audit.json"))
for reg, d in dta.items():
    for k, v in d.items():
        add("results/dT_audit.json", f"{reg}|{k}", v)

canon_arr = np.array([c[2] for c in canon], dtype=float)


def match(val):
    """Return (path,key,scale) if val matches a canonical value under
    common display scalings (x1, x1e4, x1e-4, x1e6, x1e-6, x24) and
    rounding to the displayed precision."""
    best = None
    for scale in [1.0, 1e4, 1e-4, 1e6, 1e-6, 24.0, 100.0, 0.01]:
        target = val / scale
        if not np.isfinite(target):
            continue
        d = np.abs(canon_arr - target)
        tol = max(abs(target) * 5e-3, 5e-4) + 1e-12
        i = d.argmin()
        if d[i] <= tol:
            best = (canon[i][0], canon[i][1], scale, float(d[i]))
            break
    return best


# ---------- harvest numeric strings ----------
NUM = re.compile(r"-?\d[\d,]*\.?\d*(?:[eE][+-]?\d+)?")
rows = []


def harvest(text, artifact, location):
    for m in NUM.finditer(text):
        s = m.group(0)
        if len(s) <= 1 and s in "0123456789":
            continue  # skip lone digits (section numbers, counts of words)
        v = float(s.replace(",", ""))
        ctx = text[max(0, m.start() - 60):m.end() + 20].replace("\n", " ")
        rows.append({"artifact": artifact, "location": location,
                     "display": s, "value": v, "context": ctx})


doc = Document("manuscript/manuscript.docx")
for i, p in enumerate(doc.paragraphs):
    if p.text.strip():
        harvest(p.text, "manuscript.docx", f"para{i}")
for ti, t in enumerate(doc.tables):
    for ri, row in enumerate(t.rows):
        for ci, cell in enumerate(row.cells):
            harvest(cell.text, "manuscript.docx", f"table{ti}r{ri}c{ci}")
harvest(open("submission/cover_letter.md").read(),
        "cover_letter.md", "body")
harvest(open("submission/highlights.txt").read(),
        "highlights.txt", "body")

out = []
for r in rows:
    v = r["value"]
    # skip things that are clearly non-empirical (years, coords, format specs)
    ctx = r["context"].lower()
    if re.search(r"\b(19|20)\d\d\b", r["display"]) and v >= 1900 and v <= 2100 \
            and float(v).is_integer():
        cls, mt = "context-year", None
    elif any(k in ctx for k in ["lon", "lat", "°n", "°e", "36–72", "−15", "-15"]):
        cls, mt = "geometry/config", None
    else:
        mt = match(v)
        cls = "derived" if mt else "UNMATCHED"
    out.append({**r, "class": cls,
                "canon_path": mt[0] if mt else "",
                "canon_key": mt[1] if mt else "",
                "scale": mt[2] if mt else "",
                "abs_diff": mt[3] if mt else ""})

df = pd.DataFrame(out)
df.to_csv(R / "NUMERIC_PROVENANCE.csv", index=False)
un = df[df["class"] == "UNMATCHED"]
print(f"total numeric tokens: {len(df)}; unmatched: {len(un)}")
for _, r in un.iterrows():
    print(f"  {r.artifact} {r.location} [{r.display}] …{r.context}…")
