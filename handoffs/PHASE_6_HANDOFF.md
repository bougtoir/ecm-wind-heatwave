# PHASE 6 HANDOFF — Falsification battery

## Products
- `results/phase6_falsification.csv`, `results/phase6_fdr.csv`

## Results
- C1 downwind exposure: p=0.09, opposite sign region → consistent with directional specificity
- C3 +45d placebo: p=0.48 null
- C4 off-season: NOT RUN — dataset is MJJAS-only (documented limitation)
- C5 SST outcome: null (p=0.39)
- C6 kernel variants (50/200 km, unweighted): all negative on domain — kernel sensitivity present; sign of domain coef not robust to kernel
- C7 leave-one-out: coefficients unstable across regions → effect is region-specific, not domain-wide
- FDR (BH q=0.05) on primary family: 4/6 region tests survive; France does not
