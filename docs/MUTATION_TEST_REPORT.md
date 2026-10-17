# MUTATION TEST REPORT (2026-10-17)

Method: disposable copy of the repo at /tmp/mut (data + results included);
canonical values altered; downstream outputs rebuilt; deliverables never
touched (mutations confined to /tmp/mut, deleted after).

## M1 — pooled WERR ×10 (werr_country_summary.csv + werr_pooled_summary.csv)
- manuscript.docx: pooled WERR rendered -0.36 ✓, old -0.036 absent ✓
- cover_letter.md (generated): updated ✓
- graphical_abstract.png (generated): updated ✓
- Unrelated values stable: β 5.04×10⁻⁴, 3,017 events ✓
- PASS

## M2 — n_events 3017→2500 (werr_country_summary.csv ALL row)
- manuscript abstract updated to "2,500" ✓
- PASS. Note: builder reads the ALL row of werr_country_summary.csv;
  werr_pooled_summary.csv is a redundant canonical copy. Documented in
  DATA_TEXT_FIGURE_CONSISTENCY.md.

## M3 — werr_event_level.csv truncated to 500 rows
- build_manuscript.py FAILS LOUDLY (KeyError 'uk_offshore_to_continent'
  in dT_med groupby) — correct behavior: no silent wrong output. PASS.

Restore: /tmp/mut deleted; canonical repo untouched (git diff clean on
results/ before commit).
