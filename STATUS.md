# STATUS — ECM wind/heatwave project (2026-09-25)

State: FINISHED — submission-grade. PR #1 open on
bougtoir/ecm-wind-heatwave (branch revision/ecm-targeted).

Canonical results
- Pooled WERR = -0.036 [-0.067, -0.006], 3,017 events
  (results/werr_pooled_summary.csv; primary = shrunk demand slopes + β)
- Country WERR: results/werr_country_summary.csv; events: werr_event_level.csv
- Demand: results/demand_model_comparison.csv + demand_temperature_slopes.csv
- Implied ΔT audit: results/dT_audit.json
- Falsification inventory: results/falsification_inventory.csv (17 executed,
  1 infeasible off-season — documented, never claimed)

Validation
- pytest: 3/3 PASS; p12_qc: ALL PASS (results/phase12_qc_report.json)
- Clean-checkout smoke build previously PASS (processed products copied;
  raw re-acquisition requires network + register manual download, see
  scripts/dl_static_sources.py instructions)
- Devin Review on PR #1: 5/5 findings fixed (bootstrap train-period +
  duplicate months; region-level β draws in pooled MC; Makefile acquire
  completeness; submission-zip freshness + hash check)

Packages
- ECM_submission_FINAL.zip — manuscript.docx (figures inline), 8 PNG figs,
  editable pptx, graphical abstract, highlights (≤85 chars), cover letter,
  references_verified.csv; contents SHA-verified vs disk
- ECM_reproducibility_bundle_FINAL.zip (69 MB) — code, configs, results,
  ledgers, WRF configs, docs, tests, processed data; no raw re-analysis data

Known limitations (documented, not hidden)
- Demand-model OOS R² low/negative in many countries → slopes used only as
  local marginal sensitivities with shrinkage + uncertainty propagation
- WRF counterfactual suite: designed, NOT executed (compute budget);
  wrf/ namelists + scenario generator included
- Off-season falsification infeasible on MJJAS-only archive

Remaining manual step: upload ECM_submission_FINAL.zip to Editorial Manager
with author ORCID details.

## Country-day gate (2026-10-17) — PR #2
- New estimand WERR_CD (country-day ratio-of-sums): +0.0009
  [-0.0048, +0.0098] over 2,362 eligible country-days — primary
  energy-accounting estimand. Event-mean -0.036 preserved as legacy.
- Overlap audit: 3,017 events → 3,213 unique country-days (mean mult 5.4x).
- Files: scripts/p9b_country_day_werr.py, results/country_day_werr*.csv,
  results/event_country_day_crosswalk.csv, docs/{EVENT_OVERLAP_AUDIT,
  COUNTRY_DAY_WERR_AUDIT, FOCUSED_HARDCODE_AUDIT, FOCUSED_HOSTILE_REVIEW,
  VALIDATION_REPORT}.md
- "Preregistered" → "prespecified". p12_qc 13/13 PASS, pytest 3/3.

## Public synchronization states (standing rule)
A task is NOT publicly synchronized on a feature-branch push.
States: PUSHED_TO_FEATURE_BRANCH → PR_OPEN → MERGED_TO_DEFAULT →
PUBLIC_REPRODUCIBILITY_PASS. Only the last counts as complete.
2026-10-17: PR #2 merged (e5e3ded); fresh-clone reproduction PASS
(WERR_CD 0.0009 [-0.0048,+0.0098]). See docs/PUBLIC_REPOSITORY_SYNC_AUDIT.md.

## FINAL_PUBLIC_INDEPENDENT_AUDIT (2026-10-17)
- Main verified at 6b7e789 (tree d9c09dce01d9e301f16d56965ddd6971816109b8).
- Independent audit gates A–F: PASS / PASS-WITH-FIXES (wording + table-order branch, unmerged).
- Sync state: MERGED_TO_DEFAULT + PUBLIC_REPRODUCIBILITY_PASS (archived-processed scope).
- Deliverables: docs/FINAL_INDEPENDENT_HOSTILE_REVIEW.md, FINAL_COMPUTATIONAL_INTEGRITY_AUDIT.md, COUNTRY_DAY_ACCOUNTING_AUDIT.md, FINAL_DATA_TEXT_FIGURE_CONSISTENCY.md, FINAL_REPRODUCIBILITY_SCOPE.md, FINAL_ECM_SUBMISSION_GATE.md, FINAL_HANDOFF.md.

## DOCUMENT_LOCK gate (2026-10-25)
- Document-integrity gates 0-7: PASS / PASS-WITH-FIXES on branch devin/document-integrity (PR open, unmerged).
- Fixes: Fig. S1 orphan cite removed; captions Figure→Fig.; panel Fig.1(a); 3 OMML equations (WFI/WERR_e/WERR_CD); 7 document-integrity regression tests (pytest 11/11).
- New zips: ECM_submission_DOCUMENT_LOCK.zip, ECM_reproducibility_DOCUMENT_LOCK.zip (CRC PASS, repro 66MB>50MB warn). Reproduction scope: archived-processed inputs.
