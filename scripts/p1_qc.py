#!/usr/bin/env python3
"""Phase 1 QC: schema, missingness, duplicates, coordinate bounds, unit sanity,
and the static-file acquisition ledger (SHA-256)."""
import csv, hashlib, json, pathlib, sys, zipfile
import numpy as np
import pandas as pd
import xarray as xr

RAW = pathlib.Path("data/raw")
INT = pathlib.Path("data/interim")
report = {"checks": [], "files": {}}

def check(name, ok, detail=""):
    report["checks"].append({"check": name, "ok": bool(ok), "detail": detail})
    print(("PASS" if ok else "FAIL"), name, "-", detail, flush=True)

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()

# ---- acquisition ledger for static raw files ----
LEDGER = RAW / "acquisition_ledger.csv"
rows = []
for p in sorted(RAW.rglob("*")):
    if p.is_file() and p.name != LEDGER.name:
        rows.append({"file": str(p), "bytes": p.stat().st_size, "sha256": sha256(p)})
with open(LEDGER, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["file", "bytes", "sha256"]); w.writeheader(); w.writerows(rows)
print(f"ledger: {len(rows)} files -> {LEDGER}", flush=True)

# ---- turbine sources ----
eww = pd.read_csv(RAW / "turbines/20260127_eww_opendatabase.csv")
check("eww_schema", {"latitude", "longitude", "rated_power", "commissioning_date"} <= set(eww.columns),
      f"{len(eww)} rows")
check("eww_coords", eww.latitude.between(-90, 90).all() and eww.longitude.between(-180, 180).all(),
      f"lat[{eww.latitude.min():.2f},{eww.latitude.max():.2f}] lon[{eww.longitude.min():.2f},{eww.longitude.max():.2f}]")
check("eww_power", (eww.rated_power.dropna() > 0).all(), f"max {eww.rated_power.max()} MW")
check("eww_dups", not eww.duplicated(subset=["latitude", "longitude"]).all() if len(eww) else True,
      f"{eww.duplicated(subset=['latitude','longitude']).sum()} duplicate coords")

mastr = RAW / "turbines/Gesamtdatenexport_20260924.zip"
if mastr.exists():
    check("mastr_zip", zipfile.is_zipfile(mastr), f"{mastr.stat().st_size/1e9:.2f} GB")

for csvp in sorted((RAW / "turbines/osm").glob("*.csv")):
    df = pd.read_csv(csvp, sep="\t", on_bad_lines="skip")
    n = len(df)
    report["files"][csvp.name] = {"rows": n}
    if n:
        check(f"osm_{csvp.stem}", df.iloc[:, 0].between(-90, 90).mean() > 0.99, f"{n} turbines")

# ---- OPSD ----
opsd = RAW / "electricity/opsd_time_series_60min_2020.csv"
if opsd.exists():
    head = pd.read_csv(opsd, nrows=5)
    ts = pd.read_csv(opsd, usecols=[0]).iloc[:, 0]
    check("opsd_time", str(ts.iloc[0])[:4] in ("2014", "2015"), f"{ts.iloc[0]} .. {ts.iloc[-1]}")
    load_cols = [c for c in head.columns if c.endswith("_load_actual_entsoe_transparency")]
    wind_cols = [c for c in head.columns if "wind" in c and "generation_actual" in c]
    check("opsd_cols", len(load_cols) >= 20 and len(wind_cols) >= 20,
          f"{len(load_cols)} load cols, {len(wind_cols)} wind-gen cols")
    na = pd.read_csv(opsd, usecols=["DE_load_actual_entsoe_transparency"]).iloc[:, 0]
    check("opsd_de_load", na.notna().mean() > 0.99, f"DE load missing {na.isna().mean():.3%}")

# ---- ERA5 monthly outputs ----
era = RAW / "era5"
led = era / "era5_ledger.json"
months_expected = [(y, m) for y in range(2000, 2022) for m in range(5, 10)]
if led.exists():
    ledger = json.loads(led.read_text())
    got = {r["file"] for r in ledger}
    on_disk = {p.name for p in era.glob("*_daily_*.nc")}
    missing = [f"surf_daily_{y}{m:02d}.nc" for y, m in months_expected
               if f"surf_daily_{y}{m:02d}.nc" not in on_disk]
    check("era5_complete", not missing,
          f"{len(on_disk)} on disk / {len(got)} ledger, missing: {missing[:6]}")
    for kind in ("surf", "qflux", "hydro"):
        files = sorted(era.glob(f"{kind}_daily_*.nc"))
        if files:
            ds = xr.open_dataset(files[0])
            times = pd.DatetimeIndex(ds.time.values)
            ok_time = (times.day == 1).sum() <= 2 and times.is_monotonic_increasing
            nan_frac = {v: float(ds[v].isnull().mean()) for v in ds.data_vars}
            check(f"era5_{kind}_sample", ok_time and max(nan_frac.values()) < 0.5,
                  f"{files[0].name} vars={list(ds.data_vars)} nanmax={max(nan_frac.values()):.3f}")
            ds.close()
    # unit sanity on latest file
    sf = sorted(era.glob("surf_daily_*.nc"))
    if sf:
        ds = xr.open_dataset(sf[len(sf) // 2])
        check("era5_tmax_range", -40 < float(ds.tmax.min()) and float(ds.tmax.max()) < 55,
              f"tmax [{float(ds.tmax.min()):.1f},{float(ds.tmax.max()):.1f}] C")
        ds.close()
    qf = sorted(era.glob("qflux_daily_*.nc"))
    if qf:
        ds = xr.open_dataset(qf[len(qf) // 2])
        qmax = float(np.abs(ds.qx.values).max())
        check("era5_qflux_range", qmax < 3000, f"qx max {qmax:.0f} kg/m/s")
        ds.close()

n_fail = sum(not c["ok"] for c in report["checks"])
INT.mkdir(parents=True, exist_ok=True)
(INT / "qc_report_phase1.json").write_text(json.dumps(report, indent=2, default=str))
print(f"\n{n_fail} failing checks -> {INT/'qc_report_phase1.json'}", flush=True)
sys.exit(0)
