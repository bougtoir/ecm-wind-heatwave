# ECM FIT AUDIT (Phase 0; repeat after manuscript)

Acting as ECM handling editor / desk-rejection reviewer.

## Desk-rejection risks identified → planned mitigations (implemented in design)

1. **Risk: reads as a meteorology paper, not an energy paper.**
   Mitigation: central question framed as net useful energy benefit:
   WERR = ΔE_heat / E_wind; E_net = E_wind − ΔE_heat. Introduction connects momentum
   extraction → atmospheric feedback → *system-level* energy evaluation. Electricity demand
   component (Phase 8) is essential, not appendage.
2. **Risk: detectable but energetically trivial effect oversold.**
   Mitigation: materiality is the headline criterion. Report WERR with uncertainty; a trivial
   WERR is reported as such (consistent with Vautard 2014's limited impacts).
3. **Risk: speculation about ΔE_heat without quantification.**
   Mitigation: ΔE_heat computed only via validated temperature-sensitive load model with
   out-of-sample validation; meteorological + demand uncertainty propagated to WERR.
4. **Risk: optimization as window dressing.**
   Mitigation: Phase 10 executed only if the meteorological effect is non-negligible; else a
   bounded discussion paragraph citing its conditional logic.
5. **Risk: causal overclaim from observational correlations.**
   Mitigation: DAG up front (config/dag.md); analog matching and staggered DiD with spatial-HAC
   inference; falsification battery (Phase 6); causal language only where design supports it;
   WRF counterfactual either run at feasible scale or explicitly marked NOT RUN with
   production configs + COMPUTE_BUDGET.md.
6. **Risk: "rebound" terminology clash with established energy-economics usage.**
   Mitigation: define WERR explicitly as a meteorologically mediated demand feedback;
   cite rebound literature to delineate.
7. **Risk: ECM formatting non-compliance.**
   Mitigation: ≤9,000 words, ≤15 tables+figures, abstract ≤250 words, highlights, graphical
   abstract, declarations — enforced in Phase 12 QC (docs/ECM_CURRENT_REQUIREMENTS.md).
8. **Risk: missing competing explanations for heatwave trends.**
   Mitigation: explicit controls/analogs for blocking, advection, NAO, SST, anthropogenic
   warming, soil-moisture feedback, aerosols, UHI, land use, demand trends, capacity growth.

## ECM scope self-test (run again in Phase 12)
(1) useful to energy-conversion/management readers; (2) ΔE_heat quantified;
(3) E_wind denominator defined; (4) WERR/E_net uncertainty propagated;
(5) atmospheric effects translated to system consequences without overclaim;
(6) optimization only if justified; (7) title/abstract foreground energy contribution;
(8) current ECM requirements satisfied.
