# COUNTRY-DAY WERR AUDIT (GATES 2–3, 2026-10-17)

## Estimand
WERR_CD = Σ dE_heat(c,d) / Σ E_wind(c,d) over eligible country-days.

- Eligible (c,d): ≥1 primary (pct95_tmax_3day) pixel-event active in the
  country box AND non-null positive wind generation in demand_daily.
- dE_heat(c,d) = slope_final_c × β_region × wfi_region(d) × 24 × coverage(c,d)
- coverage(c,d) = active pixels / N_pixels in box (prespecified
  transparent weight — no population/load weights exist in the data)
- E_wind(c,d) = actual daily generation × 24 — enters **at most once**
  per country-day. Demand response applied **once** per country-day.

Script: `scripts/p9b_country_day_werr.py`. Outputs:
`results/country_day_werr.csv` (2,362 rows) +
`results/country_day_werr_summary.csv`.

## Results
| estimand | value | 95% CI |
|---|---|---|
| **WERR_CD (coverage-weighted, primary)** | **+0.0009** | [−0.0048, +0.0098] (2-way block bootstrap, country×year, B=1000) |
| WERR_CD unweighted | −0.0049 | — |
| WERR_CD alternate demand model (m2) | +0.0012 | — |
| Equal-country mean of country ratios | −0.0199 | — |
| WERR_CD excl. GB (zero-slope plug-in) | see summary csv | — |
| delta-method SE | ±0.0002 | ignores day-level dependence — bootstrap CI is the honest one |
| LOO range | see summary csv loo_* columns | — |
| Legacy event-level mean | −0.0355 | [−0.067, −0.006] (kept, not overwritten) |

Zero/non-positive denominators: **0 country-days excluded**. Coverage
0.14–0.67 mean by country.

## Disagreement with event-level −0.036 — reported prominently
The two estimands differ in sign at the pooled level. Cause (not data
conflict): the event mean averages per-event ratios — small wind
denominators (CZ mean −0.46/event, IE +0.11) dominate; on the
ratio-of-sums those countries contribute little energy so the pooled
sum is dominated by large-generation countries (DE +0.002, ES −0.004,
FR −0.0001, GB 0). The manuscript now presents WERR_CD as the
energy-accounting estimand and keeps the event mean as the spatial
measurement summary; conclusions state "no detectable aggregate rebound"
under either estimand.

## Honest caveats preserved
- dE_heat remains association-implied (β×WFI×slope), not causally
  attributable.
- GB contributes denominator energy with a zero plug-in numerator —
  flagged.
- Eligibility requires OPSD coverage → 2015–2020 only; earlier events
  lack direct E_wind (2,362 days vs 3,213 calendar country-days
  overlapping events).
- coverage weight assumes demand responds proportionally to the covered
  share of national load; unweighted sensitivity flips pooled sign
  (−0.005) but stays ≈0 — documented.
