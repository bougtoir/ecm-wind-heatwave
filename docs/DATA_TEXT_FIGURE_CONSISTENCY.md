# DATA → TEXT → FIGURE CONSISTENCY (2026-10-17)

Single source of truth: canonical CSVs/JSON in results/ + data/processed/;
manuscript tables, in-text numbers, figure bars/labels, highlights, cover
letter, graphical abstract are all generated at build time by
scripts/{build_manuscript,build_cover_letter,make_figures,make_graphical_abstract}.py.

## Independent recomputation (from canonical tables)
- Pooled WERR: mean(werr_event_level.werr) = -0.03550210793057187 =
  werr_pooled_summary.csv ✓; n events 3,017 = rows; country sums = 3,017 ✓
- Country WERR means: max |recomputed − file| = 5.6e-17 ✓
- β×WFI dT medians: NS-DK +1.84, UK-offshore +1.99, LC +1.35, Iberia
  −0.62, domain −1.93, France −0.002 — match dT_audit.json & text (±0.01) ✓
- 21,327 primary / 40,971 pct90 pixel-events; 140,010 turbines (83,575 OSM);
  97.1 GW 2021 capacity; 3,366 days MJJAS 2000–2021 (22 seasons) ✓
- FDR: 5/6 primary tests survive at q<0.05 ✓ (was mis-stated 4/6 — fixed)
- Falsification battery: 11 executed + 1 documented-infeasible ✓
- WRF: 6 states × 4 heatwaves × 3 members, NOT RUN — text consistent ✓
- Sign/units: MW×24h=MWh in E_wind; slopes MW/°C; β °C/MW; fluxes 10⁶ kg/s
  ✓; percent-vs-proportion: WERR reported as dimensionless ratio ✓

## Mismatches found & fixed
1. Cover letter & graphical abstract: stale pooled WERR (pre-revision
   -0.03 [-0.04,-0.02]) → both now generated from canonical → PASS
2. "4 of 6 FDR survivors" ×2 in text + manuscript_values.csv → 5/6 → PASS
3. manuscript_values.csv werr_ci -0.007 → -0.006 → PASS
4. §3.7 omitted IE 0.43 (largest positive) & CZ −0.88 → now reported with
   denominator caveat → PASS
5. Bundle's phase12_qc_report.json was stale (217/2387-word counts from a
   pre-finishing build) → regenerated (232/2643) → PASS

## Known structural notes
- Builder's pooled row comes from werr_country_summary.csv ALL row;
  werr_pooled_summary.csv is a byte-distinct canonical copy (same values,
  verified identical 2026-10-17).
- GB WERR [0,0] is a plug-in of the shrinkage rule — footnoted in Table 4.
- 501/3,017 country-events share a start date (overlapping pixel-events);
  documented limitation; event-level metric interpretation preserved.

Rendered-output inspection: figs 1–8 PNG regenerated bit-identical from
canonical inputs; GA regenerated; docx tables/text re-extracted post-build;
no exponent corruption, minus signs intact, legends unclipped. PASS overall.

## Country-day pass addendum (2026-10-17)
- New canonical outputs: results/country_day_werr.csv (2,362 rows),
  results/country_day_werr_summary.csv, results/event_country_day_crosswalk.csv
  (21,826 rows, multiplicity column).
- manuscript_values.csv: +6 rows (werr_cd, werr_cd_ci, werr_cd_unweighted,
  werr_cd_m2, werr_cd_equal_country, n_country_days).
- Manuscript abstract/§3.7/conclusions/Table 4, cover letter, highlights,
  graphical abstract all derive WERR_CD from canonical csv at build.
- Event-mean −0.036 preserved as legacy estimand; disagreement disclosed.
- "Preregistered" → "prespecified" (2 occurrences).
- Mutation test WERR_CD→0.999 propagated to manuscript/cover/highlights.

## DOCUMENT_LOCK re-verification (2026-10-25)
- Rebuilt manuscript from canonical CSVs on top of main 4b414ab: abstract/§3/Table 4/cover letter/highlights/GA all re-verified against country_day_werr_summary.csv (+0.0009 [−0.0048,+0.0098]) and werr_pooled_summary.csv (−0.036 [−0.067,−0.006]).
- New OMML equations introduce no values; definition paragraph lists symbolic factors only.
- tests/test_document_integrity.py::test_werr_cd_matches_canonical_csv + test_pooled_event_mean_distinct_from_werr_cd lock estimand separation. PASS.
