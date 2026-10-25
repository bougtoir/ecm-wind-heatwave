# PUBLIC MAIN VERIFICATION (2026-10-17)

- Remote: https://github.com/bougtoir/ecm-wind-heatwave (public)
- Default branch: main
- Merge commit: **e5e3ded07f8ae30f2302aa8e85d93471b68eb59f**
- Tree SHA: ede81182d6f1e294bba52736fb3000385a84d918
- PR #2: MERGED (devin/hostile-audit → main, merge commit, history
  preserved, no force-push)
- PR #3: this verification package (open at write time)

## Fresh public clone (same VM, /tmp/fresh)
- `git clone` of origin main → HEAD e5e3ded
- Manifest comparison: 170 tracked files vs approved local manifest —
  **0 sha256 differences** (PUBLIC_SYNC_MANIFEST.csv)
- Accessibility in clone: README, manuscript.docx, submission/,
  scripts/, config/, tests/, provenance + audit docs, data-acquisition
  docs, WRF NOT RUN statement — all present
- No private/unapproved artifacts: PASS (see QC secrets scan)
- Reproduction: unzip shipped `data/processed` from
  ECM_reproducibility_COUNTRY_DAY_FINAL.zip → `p9b_country_day_werr.py`
  → WERR_CD = **0.0009 [−0.0048, +0.0098]**, summary csv identical;
  pytest 3/3 PASS on the clone
- No open follow-up PRs besides #3

Sync state: **PUBLIC_REPRODUCIBILITY_PASS**
