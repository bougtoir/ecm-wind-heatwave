# PR #4 Merge + Public Main Verification Audit

## Preflight (read-only)
- PR #4: devin/independent-audit-fixes → main, state open, mergeable, CI pytest PASS, no branch protection/review requirements (repo has no protection rules; 403 on rules API confirmed earlier).
- Pre-merge main HEAD: 6b7e789 (tree d9c09dce01d9e301f16d56965ddd6971816109b8); PR head 10263ed.
- Diff scope confirmed: 17 files — 3 editorial corrections (upper-bound wording §3.2/3.3, Table-3 forward-cite, cover-letter 'causal closure'), audit docs, regenerated downstream artifacts (manuscript.docx ×2, graphical_abstract.pdf, cover_letter.md, phase12_qc_report.json, zips). No unexplained science/code/data change; data/processed tracking reverted in-branch (untracked, zip-distributed).

## Merge
- Merged via normal merge commit, no force-push, history preserved. **Post-merge main: 59ccfe1d79ac23af98611fc0352c85bd7c628e84 (tree be8caf74…)**.
- Post-merge verification found one residual 'causal closure' in manuscript §1 (contribution v) — fixed via PR #5 (wording-only, CI PASS, merged): **final main b84af17c4db0dfa841894d515f7e3eba3f98eb2a (tree 4e602c09ad3f1607dbb3d546766640692bf85202)**.

## Public main independent verification (fresh clone /tmp/final)
- Tracked-file manifest: clone tree = 4e602c09… matches published main.
- `p9b_country_day_werr.py` on zip-restored data/processed → **WERR_CD = 0.000900817150901, boot [−0.0048, +0.0098], n=2,362 country-days** — identical to canonical.
- event-mean WERR −0.0355→display −0.036 [−0.067,−0.006] unchanged (regression check only).
- Editorial corrections verified in public clone: no 'upper bound', no 'causal closure' in manuscript or cover letter; table first-cite order 1→2→3→4.
- `pytest` 3/3 PASS; `p12_qc.py` 13/13 PASS.
- Secrets scan: clean (token:anon only). No raw/restricted data tracked (data/processed gitignored; distributed via zip).
- ZIPs correspond to merged source revision (regenerated on PR #4 branch). Repro zip 66 MB (>50 MB GitHub warn — known trade-off).
- Data/Code Availability wording = archived-processed scope; no raw-data rerun claimed.
