# PHASE 8 HANDOFF — Temperature-sensitive demand model

## Products
- `data/processed/demand_daily.csv` — per-country daily mean/peak load + wind generation + box-mean Tmax (2015–2020)
- `results/phase8_demand_model.csv` — per-country deseasonalized CDD(>22°C) linear model, train 2015–18 / test 2019–20

## Headline
- Slopes: +5 (AT) .. +353 (FR) MW/°C; GB ≈ 0 (little heat-driven demand — plausible).
- Out-of-sample R² is weak/negative for several countries: residual load variance dominated by non-temperature factors. Used as a linear sensitivity coefficient only, with caveat; uncertainty propagated at event level.
