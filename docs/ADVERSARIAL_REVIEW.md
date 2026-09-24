# Phase 12 — Adversarial self-review (reviewer 2 simulation) and dispositions

1. "1.5° ERA5 cannot see farm wakes." — Acknowledged in §4(b); the estimand
   is the cluster/region-scale signature via upstream exposure, not turbine
   wakes. The WRF suite is the designed closure.
2. "Confounding: build-out trends correlate with the warming trend." — Year
   FE / year covariate, event-study design, placebo timing and off-season
   controls target exactly this; residual risk disclosed.
3. "Exposure metric is heuristic." — Correct; three kernel variants and an
   unweighted variant are falsification tests; the domain coefficient is
   declared non-kernel-robust rather than hidden.
4. "OSM dates missing." — 97% of OSM units are undated and enter a static
   background layer, conservative wrt trends; registers drive timing.
5. "Demand model is weak." — Out-of-sample R² is weak/negative for several
   countries; slopes used only as local linear sensitivities and flagged.
6. "WERR denominator missing pre-2015." — OPSD coverage limits E_wind to
   2015–2020; earlier events excluded from WERR (documented).
7. "Multiple testing." — BH-FDR on the primary family; falsification battery
   reported in full, including failures (kernel sensitivity, LOO instability).
8. "Negative pooled WERR vs positive corridor estimates — contradiction?" —
   The sign map itself is the finding; pooled aggregates regions with
   opposite signs; signed heterogeneity reported, not averaged away.
9. "Novelty of 'rebound'." — Terminology disclaimed as physically distinct
   from the energy-economics rebound; NOVELTY_AUDIT.md documents the check.
10. "Causal language." — Associations reported as associations; causal
    closure deferred to the preregistered WRF counterfactual suite.
