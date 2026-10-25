# FINAL PUBLIC HANDOFF (2026-10-17)

## What was synced
All hostile-audited + country-day-gated ECM deliverables to public
bougtoir/ecm-wind-heatwave main (merge e5e3ded): code, configs, canonical
results incl. WERR_CD estimand, manuscript + journal-facing artifacts,
audit reports, provenance (NUMERIC_PROVENANCE.csv, 635 tokens), tests,
final zips, CI workflow (.github/workflows/test.yml), sync-state rule.

## What was excluded (intentional)
- Raw acquisitions (data/raw; scripts + ledgers instead)
- Working-tree data/processed dir (transport = reproducibility zip)
- Session-internal diagnostics
- Secrets: none present (scan PASS)

## Key scientific state (frozen)
- Event-mean WERR −0.036 [−0.067,−0.006] (legacy estimand, preserved)
- **WERR_CD +0.0009 [−0.0048,+0.0098]** (country-day energy-accounting
  estimand; overlap audit: 3,017 events → 3,213 unique country-days)
- Limitations disclosed in text: kernel/LOO instability, negative demand
  OOS R², pixel-event overlap, no causal/MFC-mediation claim, WRF not run

## Verification
Fresh-clone manifest: 170 files, 0 diffs; WERR_CD reproduced exactly;
pytest 3/3; p12_qc 13/13.

## Remaining blockers
None for synchronization. Open items: keywords/ORCID/GenAI at EM upload
(author); raw re-acquisition remains a scripted (not executed) path;
branch-protection rules unreadable at 403 scope (main unprotected today).
