# R12 hostile ECM review — concern -> action -> status

1. ECM scope/materiality: "atmospheric result, not energy" -> abstract +
   conclusions now answer the ECM question directly: pooled WERR -0.036
   [-0.067,-0.007] means no robust aggregate rebound; materiality bounded
   and localized positives identified. -> IMPLEMENTED
2. WFI construct validity: kernel sensitivity already disclosed; variants
   tested; domain coefficient declared non-kernel-robust. -> DISCLOSED
3. Undated OSM chronology -> R2 variants: North-Sea positives robust;
   Iberia/France not; claims revised accordingly. -> IMPLEMENTED
4. Confounding/trend -> year covariate + harmonics + placebo + TWFE kept;
   residual risk in limitations. -> DISCLOSED
5. Post-treatment adjustment -> controls limited to contemporaneous
   circulation (z500, SLP, TCWV, SST) needed for isolation; no outcome
   descendants adjusted. -> DISCLOSED
6. Analog imbalance -> max |SMD| 0.27 reported; analogs framed as upper
   bound only. -> IMPLEMENTED
7. TWFE assumptions -> reported as fragile under year-block bootstrap;
   not relied upon. -> DISCLOSED
8. Pseudoreplication -> inference at region-day level with 14d block
   bootstrap/Newey-West; dependence acknowledged. -> DISCLOSED
9. Multiple testing -> BH-FDR on the 6-member primary family; battery
   reported in full including failures. -> DISCLOSED
10. Demand-slope instability -> M1 covariates + month-block SE + M2
    shrinkage; unstable slopes shrunk or fixed (GB=0); primary WERR
    propagates slope AND beta uncertainty. -> IMPLEMENTED
11. WERR denominator -> OPSD 2015-2020 only; documented; events outside
    coverage excluded. -> DISCLOSED
12. Uncertainty propagation -> previously event-bootstrap only; now MC
    coefficient draws inside each replicate; CIs widened honestly. -> IMPLEMENTED
13. Real-world vs simulation evidence -> WRF marked designed-not-executed
    throughout. -> IMPLEMENTED
14. Novelty of WERR -> terminology contrasted with the economics rebound
    effect and solar rebound (cited); bounded novelty claim only. -> DISCLOSED
15. Conclusions exceed evidence -> pooled CI excludes zero but is negative;
    no confirmation claim; "association-implied" wording throughout. -> IMPLEMENTED
16. Event-count inconsistency + unresolved code literal -> fixed (3,017
    canonical; literal removed). -> IMPLEMENTED
