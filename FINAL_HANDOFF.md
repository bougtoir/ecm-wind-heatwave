# FINAL HANDOFF — Renewable Energy retarget (2026-11-06)

Venue: **Renewable Energy** (Elsevier). ECM desk rejected (letter not supplied; see docs/REJECTION_ECM.md).
Branch: devin/*-retarget-renewable-energy → main (base 03e3c19, DOCUMENT_LOCK state).

## Rules diff vs ECM
See the table in docs/JOURNAL_TARGET_RENEWABLE_ENERGY.md. In short: `[n]` bracket citations
(was superscript); full author/volume/page entries; mandatory word-count statement;
≤50 references; advisory 4,000–6,000-word range (manuscript is 3,094 words: flagged risk);
highlights/graphical-abstract rules unchanged.

## Deliverables
- RenewableEnergy_submission_DOCUMENT_LOCK.zip — manuscript.docx, cover_letter.docx/.md,
  highlights.txt, graphical_abstract.pdf/.png, figures/Figure_1..8.png, figures_editable.pptx,
  references_verified.csv, README.txt.
- RenewableEnergy_reproducibility_DOCUMENT_LOCK.zip — tracked tree + data/processed.
- Build: `build_manuscript.py → cp manuscript/manuscript.docx submission/ → build_cover_letter.py →
  make_graphical_abstract.py → p12_qc.py → numeric_provenance.py → pytest → package_renewable_energy.py`.

## Verification
- p12_qc ALL PASS; pytest 13/13 (incl. document-integrity + new RE reference-style/front-matter tests).
- Numeric provenance: 471 tokens, 0 unmatched (fixed NaN-argmin bug in numeric_provenance.py that
  previously reported 561/642 false UNMATCHED; citations and reference-list entries now excluded).
- Fresh clone of public main 03e3c19 + DOCUMENT_LOCK repro zip → p9b → country_day_werr_summary.csv
  byte-identical (WERR_CD 0.000900817150901 [−0.0048474, +0.0097554], 2,362 country-days).
  Same check from the new RenewableEnergy repro zip: byte-identical.
- Reproduction scope: archived processed inputs; raw re-pull documented, not run.

## Author actions
Fill author/affiliation/ORCID in Editorial Manager, GenAI declaration, state the word count
(3,094) in the submission form, upload figures as separate files.

---

# FINAL HANDOFF — ECM wind × heatwave package (2026-10-17, country-day gate)

Branch: devin/hostile-audit → base: main (canonical HEAD before this pass: b746b8e).

## Deliverables (repo root)
- ECM_submission_COUNTRY_DAY_FINAL.zip — 16 journal-facing files (supersedes HOSTILE_AUDITED submission zip)
- ECM_reproducibility_COUNTRY_DAY_FINAL.zip — 157 files (supersedes HOSTILE_AUDITED bundle)
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
