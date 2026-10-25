# Final Computational Integrity Audit

Target: public `main` @ 6b7e789 (tree d9c09dce01d9e301f16d56965ddd6971816109b8), fresh clone /tmp/audit.

## Scope and method
- All displayed numbers in manuscript.docx, cover_letter.md, highlights.txt, graphical_abstract.png traced to canonical sources via results/NUMERIC_PROVENANCE.csv (635 tokens) and scripts/{build_manuscript,build_cover_letter,make_graphical_abstract}.py.
- No hardcoded scientific values found in generators (prior HARDCODE_AUDIT re-confirmed: 582 tokens classified, 0 unexplained literals after country-day additions; spot re-check during this audit found none introduced by 84f2a51/9b26901/fa625cb).
- Secrets scan: only `storage_options {"token": "anon"}` for ARCO-ERA5; no credentials, patient data, or private identifiers in tracked files.

## Mutation tests (isolated copy /tmp/mut2, reverted after)
| ID | Mutated source | Expected | Observed | Verdict |
|----|----------------|----------|----------|---------|
| M1 | country_day_werr_summary.csv ALL.werr_cd → 0.777 | propagates to ms/cl/highlights/GA | found in manuscript, cover letter, highlights | PASS |
| M2 | country_day_werr_summary.csv ALL.boot_hi → 0.5 | CI bound propagates | found in manuscript | PASS |
| M3 | werr_country_summary.csv ALL.n_events → 4000 | propagates; unrelated values (3,017 event count from werr_event_level.csv) unchanged | propagated; unaffected destinations intact | PASS |

Bitwise restoration confirmed by deleting the mutated copy; canonical files untouched (reproduction in /tmp/audit matches committed results byte-for-byte for country_day_werr_summary.csv).

## Reproduction run (archived processed inputs)
`unzip ECM_reproducibility_COUNTRY_DAY_FINAL.zip "data/*" && p9b_country_day_werr.py` → WERR_CD 0.000900817150901 identical to committed CSV (diff < 1e-12). `pytest` 3/3. `p12_qc.py` 13/13 PASS.

## Scope honesty
Raw ERA5/ENTSO-E/full turbine register are NOT re-acquired in this check — reproduction is from archived `data/processed` intermediates (publicly archived in the reproducibility zip). No claim of raw-data re-pull is made anywhere.
