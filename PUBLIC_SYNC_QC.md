# PUBLIC SYNC QC (2026-10-17)

## Tests / traceability
- pytest tests/test_smoke.py: 3/3 PASS (working tree AND fresh clone)
- p12_qc.py: 13/13 PASS on published docx
- Mutation tests: WERR_CD→0.999 propagated to manuscript/cover letter/
  highlights (disposable copy; canonical restored) PASS
- NUMERIC_PROVENANCE.csv: 635 tokens classified, all matched/verified

## Secrets / privacy / license gate
- grep scan of all tracked files for api_key/secret/token/password/
  private-key/env/pem/rsa: only `storage_options={"token":"anon"}`
  (anonymous GCS access) — no secrets, PASS
- No patient/personal data; manuscript stays anonymized
  ("[Anonymized for single-anonymized review]") consistent with ECM
  review policy
- Third-party data: ERA5 (CC-BY Copernicus), OPSD/ENTSO-E, OSM (ODbL
  attribution noted), MaStR registers — raw data NOT redistributed;
  acquisition scripts + SHA-256 ledger + processed derivatives only ✓
- LICENSE/README/.gitignore/layout respected; no invented license/DOI

## Reproducibility scope (honest)
- VERIFIED: cached-input reproduction — fresh clone + shipped
  data/processed reproduces WERR_CD = 0.0009 [−0.0048,+0.0098] exactly
  (diff-identical summary csv)
- NOT VERIFIED: full raw re-acquisition (ERA5/OPSD/OSM/MaStR,
  network-scale, manual register download); WRF suite (not run);
  off-season falsification (archive window)
- Remote manifest: 170 tracked files, sha256-local vs fresh-clone,
  0 diffs (PUBLIC_SYNC_MANIFEST.csv)
