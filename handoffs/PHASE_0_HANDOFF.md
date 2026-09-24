# PHASE 0 HANDOFF — repository, environment, provenance, literature, novelty, feasibility

## Done
- Repo scaffolded per spec (README, Makefile, config/, data tiers, src/, tests/,
  results/, manuscript/, docs/, handoffs/, references/, provenance/, logs/).
- Single config source of truth: `config/domain.yaml` (domain, period, transects,
  heatwave definitions, exposure kernel, inference policy, seed=20260924).
- DAG documented: `config/dag.md` — mediators vs confounders; no conditioning on
  mediators for total effects.
- ECM current requirements audited: `docs/ECM_CURRENT_REQUIREMENTS.md`
  (≤9,000 words; ≤15 tables+figures; abstract ≤250; highlights; graphical abstract;
  declarations; single-anonymized review).
- ECM fit audit (Phase 0 pass): `docs/ECM_FIT_AUDIT.md` — desk-rejection risks + mitigations.
- Literature/novelty audit: `docs/NOVELTY_AUDIT.md`; 16 references Crossref-verified in
  `references/references_verified.csv`.
  - A (deployment→moisture transport): PARTIALLY ESTABLISHED; Q/MFC transect framing unexplored.
  - B (deployment→heatwave): mechanism established; heatwave-level European analysis
    underexamined; Vautard 2014 limited-impact result bounds expectations.
  - C (meteorological effect→cooling demand): APPARENTLY NOVEL.
  - D (WERR equivalent term): APPARENTLY NOVEL as meteorological externality;
    "rebound" already used for behavioral/economic effects — disclaim.
  - E (siting w/ meteorological externality): APPARENTLY NOVEL beyond wake-aware siting.
- Compute budget: `docs/COMPUTE_BUDGET.md`. WRF production = NOT RUN on this VM
  (needs HPC); ARCO-ERA5 (anonymous Google Cloud zarr) replaces CDS for ERA5 —
  no credential needed. ENTSO-E API token absent → OPSD/national portals fallback.
- Environment: `requirements.txt` + `env_frozen.txt` locked env.

## Key defaults chosen (documented, not user-checked)
- Region: Europe 35–72N, 15W–35E, 0.25°. Period 2000–2024, MJJAS season.
- Primary heatwave def: Tmax > local 95th pct (2000–2019 baseline) ≥3 consecutive days.
- Primary exposure: WFI kernel, 100 km exponential decay, directional cosine weight.
- Inference: Conley spatial-HAC (250 km) + circular block bootstrap; BH-FDR per family.

## Unresolved risks
- ARCO-ERA5 access from this VM unverified until Phase 1 download test.
- Turbine commissioning-year coverage (GEM tracker) to be checked in Phase 1.
- 7 GB RAM forces chunked/streaming xarray processing throughout.
