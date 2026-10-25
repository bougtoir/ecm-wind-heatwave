# PUBLIC SYNC PLAN (2026-10-17)

## Source of truth
Frozen audited state: commit `84f2a51` on `devin/hostile-audit`
(merged to main as `e5e3ded`). All numeric deliverables derive from
canonical `results/` + `data/processed/` at build time; nothing is
manually patched. Phases 1–10 NOT re-run.

## Inclusion manifest (categories)
| Category | Paths | Rationale |
|---|---|---|
| Scientific outputs | results/*.csv/.json (incl. country_day_werr*, event_country_day_crosswalk, NUMERIC_PROVENANCE) | canonical, verified |
| Manuscript/artifacts | manuscript/, submission/ (docx, figs png, pptx, GA, highlights, cover letter) | journal-facing |
| Code | scripts/*.py (pipeline + generators + audits), Makefile, tests/ | reproducibility |
| Config | config/domain.yaml | prespecified parameters |
| Audit docs | docs/*_AUDIT*.md, HOSTILE_REVIEW, VALIDATION_REPORT, FINAL_* | public reproducibility evidence |
| Deliverable zips | ECM_*_FINAL.zip, ECM_*_HOSTILE_AUDITED.zip | frozen packages |
| Processed data | via reproducibility zip only (data/processed not tracked) | size; document path |

## Exclusions
- `data/raw/` (network-scale acquisitions; scripts + ledger instead — see scripts/dl_static_sources.py, docs/data_sources.md)
- `data/` working tree locally restored (untracked; reproducibility zip is the transport)
- Internal session diagnostics / chat transcripts (not in repo)
- Secrets: none exist in the tree (gate result in PUBLIC_SYNC_QC.md)

## Estimand policy (§3 of the gate prompt)
Event-level mean WERR −0.036 [−0.067,−0.006] preserved as legacy
spatial-measurement estimand; country-day WERR_CD +0.0009 [−0.0048,+0.0098]
is the energy-accounting estimand. Both reported, never silently swapped.
