# European Wind Power → Moisture Transport → Heatwaves → Electricity Rebound

Reproducible pipeline testing whether large-scale European wind-energy deployment
generates atmospheric feedbacks (momentum extraction → moisture transport → soil
moisture → temperature) that materially alter net useful energy benefit through
heat-related electricity demand, quantified as

- WERR = ΔE_heat / E_wind  (Wind-induced meteorological Electricity Rebound Ratio)
- E_net = E_wind − ΔE_heat

Current target journal: *Renewable Energy* (Elsevier) — see
`docs/JOURNAL_TARGET_RENEWABLE_ENERGY.md` and `docs/JOURNAL_HISTORY.md`
(previously submitted to *Energy Conversion and Management*: desk rejected,
`docs/REJECTION_ECM.md`; the `ECM_*` zips and `docs/ECM_*` files are kept as the
record of that submission).

## Reproduce

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
make
```

`make` runs: processing → analyses → figures/tables → canonical manuscript values.
Licensed downloads (if any) are scripted in `scripts/` and documented in
`data/data_sources.md`. Public data are persisted under `data/raw/` with a
machine-readable acquisition ledger in `metadata/acquisition_ledger.csv`.

## Layout
config/ (all parameters), data/{raw,interim,processed}, src/, scripts/, tests/,
results/{tables,figures,diagnostics,simulations}, manuscript/, supplement/,
references/references_verified.csv, logs/, provenance/, docs/, handoffs/.

## Status
See `handoffs/` for per-phase handoffs and `docs/FINAL_HANDOFF.md` for what is
complete, impossible, or unverified.
