# PUBLIC REPOSITORY SYNC AUDIT (2026-10-17)

## Canonical repository
- Remote: github.com/bougtoir/ecm-wind-heatwave (public, not archived/fork)
- Default branch: **main**
- Repo name contains topic only, no journal name ✓

## TASK 1 findings
| Item | Value |
|---|---|
| Working branch | devin/hostile-audit |
| PR #2 | open → **MERGED** |
| Merge commit | **e5e3ded07f8ae30f2302aa8e85d93471b68eb59f** (merge, not squash; history preserved) |
| 84f2a51 in main | YES (parent of merge commit) |
| Branch protection | none (403 on rules API but main unprotected) |
| COUNTRY_DAY_FINAL on main | YES — zips, results/country_day_werr*.csv, all audit docs |

## TASK 2 validation (pre-merge)
- pytest 3/3 PASS; p12_qc 13/13 PASS
- WERR_CD +0.0009 [−0.0048, +0.0098] verified in canonical summary
- Event-mean −0.036 retained as legacy, NOT presented as principal
  estimand; WERR_CD preferred for energy accounting (disclosed)
- No secrets/credentials; data/raw not committed (large; shipped via
  reproducibility zip); .gitignore covers raw archives

## TASK 4 — fresh-clone public reproduction
- Fresh clone of main at e5e3ded → /tmp/fresh; pip install -r
  requirements.txt OK
- `data/processed` restored from ECM_reproducibility_COUNTRY_DAY_FINAL.zip
  (34 files — the documented cached-input path; raw re-acquisition is
  scripted separately, network-scale, not claimed)
- `python scripts/p9b_country_day_werr.py` → **WERR_CD = 0.0009
  [boot −0.0048, +0.0098]** — exact match to COUNTRY_DAY_FINAL
  (summary csv diff-identical)
- pytest 3/3 PASS on the fresh clone

## TASK 5 — future synchronization
- CI: .github/workflows/test.yml runs pytest on push to main and every PR.
- Standing workflow: devin/* branch → PR → checks green → merge to main.
- Never force-push main; never bypass protection (none present); merges
  via PR only. Branch-only pushes are NOT reported as synchronized.

## Sync-state vocabulary (TASK 6)
PUSHED_TO_FEATURE_BRANCH → PR_OPEN → **MERGED_TO_DEFAULT** →
**PUBLIC_REPRODUCIBILITY_PASS** ← current state (final, complete).

## Open items
- Classic branch-protection rules unreadable (403 — needs admin scope);
  main is unprotected per provider probe. If protection is added later,
  same PR workflow applies.
- 59 MiB repro zip exceeds GitHub's 50 MB warning threshold (committed
  successfully; consider Git LFS if future bundles grow).
