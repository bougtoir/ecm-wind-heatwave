# Final QC report
- References: 30/30 exist (Crossref), all cited, claim mappings audited
  (CLAIM_REFERENCE_MATRIX.csv).
- Figures/tables: all 8 figs + 4 tables cited in order; ≤15 items.
- Quantitative traceability: manuscript_values.csv; placeholder/hard-code
  scan CLEAN; event counts consistent (3,017 analyzed; 21,327 pixel-events).
- Agreement across abstract/main/highlights/cover letter/graphical
  abstract: pooled WERR -0.036 [-0.067,-0.007].
- No unexecuted analysis presented as executed (WRF, C4 off-season
  explicitly not run).
- No unsupported causal claim (claim-strength audit).
- No hidden hard-coding: values generated at build; QC itself reads
  canonical CSVs (the stale -0.029 literal in p12_qc was fixed).
- Package claims match contents: ECM_submission.zip vs
  ECM_reproducibility_bundle.zip; availability text distinguishes the two.
- p12_qc: ALL PASS (results/phase12_qc_report.json).
PASS: zero unresolved critical/major discrepancies.
