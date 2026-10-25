# Final Data→Text→Figure Consistency

## Cross-artifact checks
- WERR_CD: +0.0009 → rendered as 0.001 [−0.005, 0.010] in highlights; +0.0009 [−0.0048,+0.0098] in §3.7/conclusions/abstract/Table-4-adjacent text/GA bottom line — identical source (country_day_werr_summary.csv ALL row). PASS.
- Event-mean WERR −0.036 [−0.067, −0.006], n_events 3,017, n_turbines 140,010, n=21,327 pixel-events, 22 seasons, FDR 5/6, battery 11 checks — identical across abstract/§3/Table 4/cover letter/highlights/GA. PASS.
- Figure citations in text: 1,1,2,2,3,4,5,6,7,8 — first cites in order. PASS.
- Table citations in text: first-cite order now 1→2→3→4 (fixed forward-cite of Table 3 from §2.4). PASS.
- References: submission/references_verified.csv — 30 refs, Crossref-verified DOIs, no fabricated DOIs/URLs; numbering order matches first citation. PASS.
- Declarations: data availability (ARCO-ERA5 + ledger), prespecified-not-executed WRF, code availability → this repo. Consistent. PASS.
- ECM guide-for-authors items (abstract ≤250 → 246 words; highlights; cover letter; separate figure files; Vancouver-style refs) — docs/ECM_REQUIREMENTS_FINAL_CHECK.md stands. PASS. Editorial-system status NOT asserted — EM upload not performed.
- Signs/units/CI/rounding: spot-verified per NUMERIC_PROVENANCE display column; no stale −0.03 or 4/6-FDR remnants found (grep over manuscript text + submission files). PASS.
