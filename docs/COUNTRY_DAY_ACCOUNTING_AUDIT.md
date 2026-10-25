# Country-Day Accounting Audit

## Recomputation (independent code path, fresh clone)
WERR_CD recomputed WITHOUT p9b (direct build from heatwave_events.csv + wfi_daily.csv + demand_daily.csv + phase3_panel_regression.csv + demand_model_comparison.csv):
- WERR_CD = 0.000900817150901 — bitwise-equal to committed results/country_day_werr_summary.csv ALL row.
- 2,362 eligible country-days; 0 non-positive-denominator exclusions.
- Per-country ratios (ΣΔE/ΣE_wind) reproduced: DE +0.0016, FR −0.0001, GB 0, ES −0.0038, IT −0.0040, NL +0.0728, BE +0.0420, DK +0.0460, IE +0.1055, PT −0.0136, PL −0.0407, AT −0.0048, CZ −0.4592 — match committed.

## Record/key accounting
- 3,017 primary records = pixel-events (CBOX mask over pct95_tmax_3day events; event_id×lat×lon×start×end unique).
- 3,213 unique event-overlapping country-days; 2,362 pass E_wind eligibility (demand_daily.csv window 2014-12-31→2020-09-30 + gen>0).
- Mean denominator multiplicity of the OLD event-level design: 5.4× (DE 9.9×, PL 9.1×, GB 7.2×, FR 6.4×) — each pixel-event divided ΔE by the whole country's generation; disclosed as the reason event-mean WERR (−0.036) is not the energy-accounting estimand.

## Estimand construction (verified against script)
- ΔE(cd) = demand slope_final × β_region × WFI_region(d) × 24h × coverage(d); coverage = active-event pixels / n_pixels in CBOX; coverage applies to numerator only (pixel-fraction of country heating), denominator E_wind = gen × 24 (whole country; documented caveat — undercounts sub-national wind but is the available accounting boundary).
- Ratio-of-sums throughout; unweighted/m2/equal-country variants are sensitivity ratios-of-sums / means as labelled (−0.0049 / +0.0012 / −0.0199).
- Uncertainty: two-way country×year block bootstrap B=1000 → [−0.0048, +0.0098]; delta-method SE ±0.0002 propagated from slope_se and β_se.
- LOO: per-country leave-one-out columns present in summary (werr_cd_excl_GB etc.); range disclosed in §3.7.

## Checks
- Denominator reuse audit: each country-day enters the denominator exactly once. PASS.
- Missingness: days outside demand coverage window dropped silently-bounded to eligibility mask; logged in summary n_country_days. PASS.
- Event-mean comparison kept distinct (§3.7, Table 4, highlights, GA bottom line). PASS.
- Generalizability caveat: 13 CBOX countries only; caveat retained.
