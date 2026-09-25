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
