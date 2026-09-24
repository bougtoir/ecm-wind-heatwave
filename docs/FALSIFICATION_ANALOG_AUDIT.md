# R3 falsification + analog audit

## Executed test count (canonical: results/falsification_canonical.csv)
- 6 regional primary tests (northsea_to_lowcountries, northsea_to_denmark_germany,
  atlantic_to_france, atlantic_to_iberia, uk_offshore_to_continent, domain)
- 11 executed falsification checks: C1 downwind exposure, C3 +45d placebo,
  C5 weak outcome (SST), C6 kernel variants (50 km / 200 km / unweighted),
  C7 leave-one-region-out (5 drops)
- 1 prespecified control NOT RUN: C4 off-season (Nov–Mar) — the ERA5
  acquisition is MJJAS-only; off-season download exceeds the single-VM
  session budget (same boundary documented for WRF). Retained as limitation.
  Wording corrected everywhere: "a battery of 11 executed falsification
  checks (one further prespecified off-season control infeasible)".
- BH-FDR applied to the 6-member primary family only; 4/6 survive.

## Analog balance (results/analog_balance.csv)
- max |SMD| across regions/covariates = 0.266 (tcwv, atlantic_to_iberia);
  domain tcwv = 0.262; all other cells |SMD| <= 0.21.
- Interpretation: balance adequate for stratified estimation but imperfect;
  analog estimates read as an UPPER BOUND on the matched contrast and are
  not promoted beyond that anywhere in the manuscript.
