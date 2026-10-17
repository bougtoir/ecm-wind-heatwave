# HOSTILE REVIEW — ECM wind/heatwave/WERR package
Simulated handling editor + 4 hostile reviewers. Verdicts are on the
*current* package after implemented fixes; residual risks are explicit.
Date: 2026-10-17. Baseline audited: git b746b8e + FINAL zips.

## Verdict summary

| Role | Verdict |
|---|---|
| Handling editor | MAJOR (fixable in-session) → post-fix: submit-ready with honest claims |
| R1 atmospheric dynamics | MAJOR → MINOR residual |
| R2 causal inference | MAJOR → MINOR residual |
| R3 demand econometrics | MINOR |
| R4 energy-systems/ECM scope | MINOR |

Post-fix status: no remaining BLOCKER. One MAJOR-class scientific weakness
is irreducible without new simulations and is preserved as explicit claims
calibration (see R1-1, R2-2, FINAL_HOSTILE_DECISION.md → verdict SUBMIT
with calibrated claims).

---

## R1 — Atmospheric dynamics

**R1-1 (MAJOR). WFI is a constructed exposure index, not a demonstrated
moisture perturbation.** The chain WFI→β→ΔT→ΔE never measures a mediated
atmospheric response: Q/MFC fields are used as *covariates*, and no
analysis demonstrates that turbine deployment measurably changes Q or MFC.
Evidence: results/phase5_twfe.csv (mfc outcome: coef −1.05e-10, p=0.75 —
null); scripts/build_exposure.py (WFI = upstream-capacity index on 10-m
wind direction). Scientific consequence: all "effects" are associations
between a constructed exposure and temperature anomalies; WERR is a
scenario ratio, not an induced-demand estimate.
Fix implemented: §3.2 now states β×WFI medians are "scenario magnitudes …
not observed turbine-attributable warming … upper bounds"; abstract uses
"association-implied"; §3.7 notes association-implied scenario ratios.
Residual: the fundamental gap (no measured mediation) is irreducible
without causal simulations — WRF suite specified, NOT executed. Claim
level is now honestly "association-implied". Post-fix: MINOR.

**R1-2 (MINOR). Proxy construction details.** 10-m wind direction, 1.5°
grid, six 50-km steps, 100-km e-folding kernel, undated-OSM background —
all stated in §2.4 + sensitivity variants (kernel_50km/200km/unweighted,
dated-only, registry-only in results/exposure_chronology_sensitivity.csv).
Exposure misclassification acknowledged (§4 limitation a). Post-fix: PASS.

**R1-3 (MINOR). Wakes vs synoptic circulation.** D2 analog matching on
(z500, SLP, flux, TCWV, SST) is the correct guard; balance |SMD|≤0.27 is
modest (conventional <0.1 ideal) — text already reads analogs as "upper
bound under imperfect balance". Post-fix: PASS with note.

## R2 — Causal inference

**R2-1 (MINOR→fixed). Selective reporting of heterogeneity.** §3.7 listed
only North-Sea positive WERR (BE/NL/DK/DE) and omitted the largest
positive (IE +0.43) and the extreme negatives (CZ −0.88). A hostile reader
reads this as narrative steering.
Fix: §3.7 now names IE 0.43 (small-denominator flag) and CZ −0.88 with an
explicit "association-implied scenario ratio on small denominators, not
measured demand offsets" caveat; abstract reports the IE bound.
Post-fix: PASS.

**R2-2 (MAJOR→MINOR). Causal identification is fragile at domain level.**
TWFE tmax_anom: HAC p=0.047 vs year-block bootstrap p=0.64 (inference
fragile); kernel sign reversal (C6); LOO drops flip domain sign
(C7_LOO atlantic_france → +5.98e-4 p=0.0015; atlantic_iberia → +1.89e-3
p=4.5e-16). Evidence: results/phase5_twfe.csv, phase6_falsification.csv.
Consequence: the *domain-level* sign is not robust; corridor-level signs
are. Fix: §3.5 now states the domain sign is aggregation-sensitive and
kernel-non-robust explicitly; §3.7 says "signed heterogeneity — not the
sign — is the robust feature". Residual MINOR: pooled WERR sign inherits
domain-coefficient sensitivity — flagged in FINAL_HOSTILE_DECISION.md as
the key caveat a reviewer may still press.

**R2-3 (MINOR). Spatiotemporal confounding/autocorrelation.** NW(14d)+
circular block bootstrap B=200 in D1; cell×year FE + block bootstrap in
D3; placebo +45d null (p=0.48); downwind null (p=0.09); SST null (p=0.39).
Mediator-vs-confounder concern: TCWV/flux controls could themselves be
mediators — acknowledged by interpreting β as a *total* association
along the transport corridor. Post-fix: PASS (documented).

**R2-4 (fixed). Overlapping pixel-events.** 501 of 3,017 country-events
share a start date with another event in the same country box (different
pixels; spatial overlap). Event-level WERR double-counts E_wind across
overlapping pixel-events. Documented as a limitation; event-level metric
interpretation preserved. Would need a country-day deduplication rule to
resolve fully — noted in FINAL_HOSTILE_DECISION.md residual risks.

## R3 — Electricity-demand econometrics

**R3-1 (MINOR). Negative OOS R².** CV/test R² negative for most countries
(Table 3). Justified: slopes are *marginal* deseasonalized sensitivities,
not a load forecast; coefficient uncertainty is propagated (MC inside
bootstrap); unstable slopes shrunk (EB, training-data-only rule).
COVID-period handled via 2020 dummy in M1. Residual: FR/NL slopes flagged
least reliable — already in text. Post-fix: PASS.

**R3-2 (fixed). WERR denominator integrity.** E_wind>0 enforced in
r1_werr.py (events with zero generation skipped); units MW×24h=MWh
consistent; country→region map explicit (C2R in r1_werr.py). GB fixed at
0 by shrinkage → degenerate [0,0] CI now footnoted in Table 4.
Post-fix: PASS.

## R4 — Energy-systems / ECM scope

**R4-1 (MINOR). Energy-management contribution.** The deliverable is a
metric (WERR), a harmonized register, and a bounded negative result —
credible for ECM as an energy–atmosphere interface paper *because* it
does not claim unvalidated meteorological attribution. Cover letter frames
scope correctly. Post-fix: PASS.

**R4-2 (fixed). WRF/preregistration language.** Abstract said "Large-eddy
counterfactuals" — WRF-Fitch is mesoscale, and no LES exists. Fixed to
"Mesoscale WRF counterfactuals were designed but not executed". No claim
of numerical counterfactual confirmation anywhere (grep-verified); the
"preregistered" wording in §4.1 refers to the *design document* — kept
but §4.1 already says "design (not executed)". Post-fix: PASS.

## Additional hostile checks (prompt items 7–10)

- **11 checks genuinely executed?** falsification_inventory.csv: 18 rows —
  6 primary (family: BH-FDR) + 12 battery rows, 11 executed + C4 infeasible
  (documented, never claimed). Manuscript's "11 executed" = battery checks
  only (3 falsification + 3 kernel + 5 LOO). Consistent and now
  cross-referenced in §3.5. PASS.
- **Multiplicity:** BH-FDR applied to the 6-test primary family → 5/6
  survive (was mis-stated as 4/6 — FIXED in §3.2, §3.5,
  manuscript_values.csv).
- **Evidence-exceeding language scan:** abstract/GA/figs/conclusions/
  cover letter re-verified post-fix; GA and cover letter regenerated from
  canonical values. PASS.
- **Figures:** all 8 PNGs + GA regenerated from canonical inputs
  bit-identical for unchanged data (see MUTATION_TEST_REPORT.md).
