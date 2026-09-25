# Finishing audit (final 5-point pass)

## 1. Implied ΔT verification — VERIFIED, wording corrected
Trace: `dT = beta_region × wfi_MW` in results/werr_event_level.csv; β from
results/phase3_regions.csv (unit °C/MW); WFI unit = integrated upstream
capacity-weighted flux exposure in MW (scripts/build_exposure.py, no hidden
×10/×1000 anywhere). Event-median implied ΔT (results/dT_audit.json):
- northsea_to_denmark_germany β=5.04e-4 °C/MW, WFI med 3649 MW → ΔT med +1.84 °C (5–95% +1.4..+2.1)
- uk_offshore_to_continent β=5.53e-4, WFI med 3606 → +1.99 °C
- northsea_to_lowcountries β=3.69e-4, WFI med 3668 → +1.35 °C
- atlantic_to_iberia β=-2.13e-4, WFI med 2896 → -0.62 °C
- domain β=-3.87e-3, WFI med 499 → -1.93 °C
- atlantic_to_france β≈-1.3e-6 → ≈0 °C
"1–2 °C" is REPRESENTATIVE only on the high-exposure North-Sea corridors
(positive) and the domain (negative); it is not a small global effect.
Manuscript §3.2 and abstract now state regional medians explicitly and
removed the bare "small" qualifier.

## 2. Demand model wording + shrinkage documentation — DONE
- "validated demand model" removed everywhere; now "marginal demand-sensitivity
  model with propagated coefficient uncertainty". Methods §2.7 documents:
  month-block bootstrap SE (B=500, train years only, duplicate months kept),
  instability rule (sign flip across blocked-CV folds or |slope|/SE<1),
  normal-normal empirical-Bayes shrinkage to inverse-variance pooled mean
  (mu≈27 MW/°C, tau2≈9.5e3), posterior formula, affected countries
  (GB fixed 0; DK, AT, NO, FI, CH), and that the rule never uses WERR
  sign/magnitude. Table 3 exposes CV R² and 2019-20 test R² per country.
- Bug fixes (Devin Review): bootstrap restricted to training years and
  duplicate months preserved (concatenated row indices).

## 3. Falsification inventory — DONE
results/falsification_inventory.csv: 18 rows; 17 executed (6 primary + 11
non-primary: 3 falsification controls, 3 kernel/decay sensitivities,
5 leave-one-region-out robustness) + C4 off-season infeasible (MJJAS-only
archive; documented, never claimed). "11-check falsification battery"
renamed to "falsification-and-sensitivity battery (11 executed checks)"
everywhere. BH-FDR family remains the 6 primary regional tests.

## 4. Replication-package truth check — DONE
Present: README, requirements.txt, Makefile (acquire→analysis→revision→
figures→manuscript→qc; dl_static_sources.py added for registers/OPSD),
configs, all scripts, tests (3 smoke tests PASS), figure/table generators,
p12_qc value-checker (ALL PASS), SHA-256 ledgers, acquisition scripts,
redistributable derived data (data/processed, 86 MB), canonical results,
WRF namelists + scenario generator (wrf/), COMPUTE_BUDGET.md with explicit
"WRF production not executed". Availability statements match reality.
Stale submission artifacts replaced (manuscript.docx, pptx, fig8, graphical
abstract were outdated); ECM_submission_FINAL.zip contents hash-verified
byte-identical to submission/. ECM_reproducibility_bundle_FINAL.zip (69 MB)
contains the full working tree minus .git/raw-data/tmp/venv.

## 5. Cross-artifact consistency — DONE
Programmatic scan of manuscript.docx: no stale -0.029/-0.007/3,254/nine-test/
TODO/validated demand/unresolved {expr}. Canonical: 3,017 events;
pooled WERR -0.036 [-0.067,-0.006]; DK +0.091, NL +0.132, BE +0.071,
IE +0.43 (shrunk), GB fixed 0; 140k turbines; B=500 bootstrap, B=1000 MC.
p12_qc ALL PASS; pytest 3 PASS.
