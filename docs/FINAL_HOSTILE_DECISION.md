# FINAL HOSTILE DECISION — 2026-10-17

## Verdict: SUBMIT (with calibrated claims)

After the hostile-review pass, all BLOCKER defects were fixed and every
empirical number in every deliverable is generated from, or verified
against, the canonical outputs. No fabricated PASS: the irreducible
scientific limitations are preserved in the manuscript text itself.

## Residual risks a real referee may still press (disclosed, not hidden)
1. No measured mediation: WFI→ΔT is an association along a constructed
   exposure; MFC outcome null in TWFE. WERR is an association-propagated
   scenario ratio — the text now says so explicitly.
2. Domain sign fragility: kernel/LOO sensitivity flips the domain
   coefficient; corridor-level signs are stable. The pooled negative WERR
   inherits this — flagged in §3.5/§3.7.
3. Implied ΔT of order 1–2 °C reads large; labeled an upper-bound scenario
   magnitude, not observed causal warming.
4. Overlapping pixel-events (501/3,017 shared start dates) inflate the
   event count vs country-days; event-level framing retained with caveat.
5. Demand slopes have negative OOS R² in most countries; used only as
   marginal sensitivities with shrinkage + MC propagation — disclosed.
6. WRF counterfactual not run: no causal closure claimed; design ships.

## Fix ledger (implemented this pass)
- Stale WERR in cover letter + graphical abstract (BLOCKER×2) → both
  artifacts now generated from canonical CSVs
- FDR survivors 4/6 → 5/6 (text ×2 + manuscript_values.csv)
- werr_ci display −0.007 → −0.006
- IE 0.43 + CZ −0.88 heterogeneity reported with denominator caveats
- "Large-eddy" → "Mesoscale WRF"; β×WFI explicit "not causal ΔT" caveat
- GB [0,0] degenerate CI footnoted; EB μ/τ² now computed at build
- New scripts: make_graphical_abstract.py, build_cover_letter.py,
  numeric_provenance.py (audit tooling)

## Gates status
GATE A complete (verdicts above). GATE B PASS. GATE C PASS (cached-input
reproduction; raw re-acquisition honestly not claimed). GATE D complete
(all affected downstream outputs regenerated).
