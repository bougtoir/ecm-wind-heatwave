# FINAL HANDOFF — ECM wind × heatwave package (2026-10-17)

Branch: devin/hostile-audit → base: main (canonical HEAD before this pass: b746b8e).

## Deliverables (repo root)
- ECM_submission_HOSTILE_AUDITED.zip — 15 journal-facing files
- ECM_reproducibility_HOSTILE_AUDITED.zip — 146 files (scripts, configs,
  canonical outputs, processed data, ledgers, audit reports)

SHA-256 are printed in the commit message and docs/HOSTILE_REVIEW_ECM.md
appendix; recompute with `sha256sum ECM_*_HOSTILE_AUDITED.zip`.

## Audit reports (docs/)
- HOSTILE_REVIEW_ECM.md — editor + 4 hostile reviewers, verdicts, fixes
- HARDCODE_AUDIT.md — prohibited-hardcode definition, findings B1–B7
- DATA_TEXT_FIGURE_CONSISTENCY.md — independent recomputation ledger
- MUTATION_TEST_REPORT.md — M1–M3 propagation tests
- NUMERIC_PROVENANCE — results/NUMERIC_PROVENANCE.csv (582 tokens)
- REPRODUCIBILITY_FINAL_CHECK.md — cached-input repro, citations
- ECM_REQUIREMENTS_FINAL_CHECK.md — current ECM author requirements
- FINAL_HOSTILE_DECISION.md — **SUBMIT (calibrated claims)**

## New build tooling
scripts/make_graphical_abstract.py, scripts/build_cover_letter.py,
scripts/numeric_provenance.py. Makefile targets unchanged; run order:
`make figures` → `make manuscript` → build_cover_letter.py →
make_graphical_abstract.py → pytest → p12_qc.

## Test status at handoff
- pytest tests/test_smoke.py: 3/3 PASS
- scripts/p12_qc.py: ALL PASS (abstract 232 w, body 2643 w)
- Mutation tests M1–M3: PASS
- Figures: bit-identical rebuild from canonical inputs

## Honest residual risks (in manuscript text, not hidden)
Domain-sign fragility under kernel/LOO variants; no measured MFC
mediation; β×WFI is scenario magnitude not observed ΔT; overlapping
pixel-events; negative OOS R² in demand models; WRF suite designed but
not run; off-season falsification infeasible on MJJAS archive.

## Manual steps left for the author
Keywords at EM upload; ORCID link; GenAI disclosure checkbox;
named-author version is single-anonymized as required.
