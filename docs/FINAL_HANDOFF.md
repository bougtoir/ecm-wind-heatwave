# Final Handoff (independent audit round)

## State
- Public main: 6b7e789 (tree d9c09dce01d9e301f16d56965ddd6971816109b8) — PRs #2 (e5e3ded) and #3 (6b7e789) merged, no force-push, history preserved.
- This audit adds a focused fix branch only (wording + citation order); NOT merged — per instruction.
- Canonical values: WERR_CD +0.0009 [−0.0048, +0.0098] (2,362 country-days); event-mean WERR −0.036 [−0.067, −0.006] (3,017 events, secondary).
- Zips: ECM_submission_COUNTRY_DAY_FINAL.zip and ECM_reproducibility_COUNTRY_DAY_FINAL.zip regenerated on the fix branch (content-identical except regenerated manuscript/cover_letter/highlights and updated docs).

## How to reproduce
clone → unzip repro zip data/* → `pip install -r requirements.txt` → `pytest`, `p9b_country_day_werr.py`, `build_manuscript.py`, `p12_qc.py`.

## Outstanding (author, not Devin)
EM upload + keywords + ORCID + GenAI disclosure. Open item: reproducibility zip is 59 MiB (>50MB GitHub warn) — committed deliberately; consider LFS/external archive if repo size becomes a concern.
