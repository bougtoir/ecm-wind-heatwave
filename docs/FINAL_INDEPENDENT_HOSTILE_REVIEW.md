# Final Independent Hostile Review (public main 6b7e789)

Independent re-review of public `main` (merge commits e5e3ded + 6b7e789, tree d9c09dce01d9e301f16d56965ddd6971816109b8) against the current submission package. Findings are listed with severity, evidence, action, and post-fix status.

## Findings and resolutions

1. **Unproven "upper bound" claims** — SEVERITY: moderate. Evidence: §3.2 said β×WFI magnitudes "are upper bounds on the association-implied perturbation" and §3.3 read analog contrasts "as an upper bound under imperfect balance"; no bounding argument exists. ACTION: wording corrected to "not bounds either (no bounding argument is made)" and "raw matched contrasts — neither bounds nor causal effects". STATUS: FIXED.
2. **Table citation order violation** — SEVERITY: minor editorial. Evidence: §2.4 forward-cited Table 3 before Table 2's first citation (Vancouver/numbered-order rule). ACTION: forward cites replaced with §3.5 pointers; first-cite order now 1→2→3→4. STATUS: FIXED.
3. **"Causal closure" phrasing in cover letter** — SEVERITY: minor. Evidence: cover_letter.md described WRF suite as "the prespecified causal closure", implying causal identification beyond the associational design. ACTION: reworded "prespecified counterfactual suite". STATUS: FIXED.

## Criticisms examined and retained as disclosed limitations (no fix justified)

- **WFI/commissioning uncertainty** — WFI is built from the ledgered 140,010-turbine register; commissioning-year uncertainty is stated in §2.2–2.3 and the data availability statement. No defect demonstrated.
- **ERA5 1.5 m vs hub height** — exposed as a stated limitation: estimates are surface-layer associations, not hub-height power effects; β×WFI magnitudes are labelled scenario magnitudes, not observed ΔT.
- **Circulation confounding** — addressed by analog matching (|SMD| ≲ 0.27) and regional betas; residual confounding is disclosed; estimate remains associational.
- **Kernel/decay and leave-one-out fragility** — sensitivity battery (11 checks) reports non-robust regional signs; conclusions calibrated to corridors where sign survives (5/6 FDR).
- **TWFE/bootstrap weaknesses** — inference uses panel regression + country×year block bootstrap + delta method; no cluster-robust claim beyond what is shown.
- **MFC mediation unverified** — moisture-flux-convergence mediation is presented as a mechanism hypothesis, not verified; text does not claim observed MFC mediation.
- **Negative OOS R² for demand model** — honestly reported (Table 3, §3.5); coefficient uncertainty propagated rather than predictive skill claimed.
- **WRF not executed** — §4.1 labels the counterfactual suite "Prespecified counterfactual design (not executed)"; not "preregistered".
- **WERR_CD vs event-mean WERR** — kept as two distinct estimands: WERR_CD = +0.0009 [−0.0048, +0.0098] (ratio-of-sums, 2,362 country-days) is the energy-accounting estimand; event-mean −0.036 [−0.067, −0.006] is retained as the secondary per-event estimand and the multiplicative denominator reuse is disclosed (docs/EVENT_OVERLAP_AUDIT.md). Construction survived checks: eligibility mask from primary pct95_tmax_3day events, coverage-weighted ΔE, non-positive E_wind excluded (n=0), all quantities ratio-of-sums. VERDICT: WERR_CD stands as primary energy-accounting estimand.
- **Genuine ECM contribution** — paper delivers ledgered turbine register + WFI exposure field + prespecified counterfactual protocol; negative/near-null energy finding retained rather than suppressed.

## Hostile reviewers' verdicts

- ECM editor: no new blocker after three wording fixes; submission-ready modulo author's EM upload actions.
- Atmospheric reviewer: claims calibrated to association; WRF suite honestly unexecuted; kernel/LOO fragility disclosed.
- Causal-inference reviewer: β×WFI now correctly labelled non-causal and non-bounding; estimand separation clean.
- Energy-accounting reviewer: country-day ratio-of-sums is the defensible estimand; event-level retained as secondary with artifact disclosure.
