# REPRODUCIBILITY FINAL CHECK (2026-10-17)

Scope: honest distinction — this verifies *cached-input reproduction*
(all scripts against the persisted processed products shipped in the
reproducibility bundle), NOT full raw-data re-acquisition (ERA5 ARCO,
MaStR, OSM PBF, OPSD, registers require network + one manual register
download; scripts/dl_static_sources.py documents it). No claim of full
public-data reproduction is made.

## Executed in this VM, fresh from the FINAL bundle inputs
- data/processed/ restored from ECM_reproducibility_bundle_FINAL.zip;
  diffed vs repo results/: byte-identical except stale qc_report →
  regenerated ✓
- `make figures` (make_figures.py + build_pptx.py): all 8 PNGs
  bit-identical to shipped figures; pptx rebuilt ✓
- `make manuscript` (build_manuscript.py): docx rebuilt post-fixes ✓
- New generators verified: make_graphical_abstract.py, build_cover_letter.py ✓
- pytest tests/test_smoke.py: 3/3 PASS ✓
- p12_qc.py: ALL PASS (abstract 232 w, body 2643 w, figs cited 1–8, 30 refs
  verified, 8 figs + 4 tables, ledger 11 hashed) ✓
- Mutation suite: 3/3 PASS (MUTATION_TEST_REPORT.md) ✓
- ZIP manifests inspected: submission zip = 14 journal-facing files;
  repro bundle = 226 files incl. scripts/configs/ledgers/processed data ✓

## Citations
30/30 refs carry DOIs verified via Crossref API (2026-09-24 ledger);
spot re-resolution 2026-10-17: 4/5 sampled DOIs resolve live; one AMS DOI
(10.1175/mwr-d-22-0118.1) returns HTTP 403 to scripted agents — a
publisher bot-block, not an invalid DOI (Crossref record exists).
Claim↔reference adjacency re-checked for all text altered in this pass
(no new citation contexts introduced).

## Not executed (documented, never claimed)
- Full raw re-acquisition (network-scale; ledger in docs/data_sources.md)
- WRF production suite (compute budget exceeded; configs + generator ship)
- Nov–Mar off-season falsification (MJJAS-only archive)
