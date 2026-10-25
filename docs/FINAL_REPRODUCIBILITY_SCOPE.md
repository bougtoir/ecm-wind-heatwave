# Final Reproducibility Scope

## Clean-environment verification (this audit)
Fresh clone /tmp/audit of public main 6b7e789; data/processed restored from ECM_reproducibility_COUNTRY_DAY_FINAL.zip; system python venv (~/repos/ecm-wind-heatwave/.venv, requirements.txt installed):
- `p9b_country_day_werr.py` → results identical (WERR_CD 0.000900817150901).
- `build_manuscript.py`, `build_cover_letter.py`, `make_graphical_abstract.py`, `numeric_provenance.py` → regenerate cleanly.
- `pytest` 3/3; `p12_qc.py` 13/13.

## What is reproduced from what
- REPRODUCED: all displayed numbers from archived `data/processed` intermediates (publicly distributed in the reproducibility zip). Label: **archived-processed-inputs reproduction**.
- NOT REPRODUCED HERE: raw-source acquisition (ARCO-ERA5 pulls, ENTSO-E/OPSD downloads, turbine register harmonization). Scripts exist (p0*–p8*, scripts/) but require multi-GB public data pulls; no artefact claims raw re-acquisition. Label: **not executed; not claimed**.

## Honest scope statement
The public package reproduces every published number from its archived processed inputs. Raw-data re-pull is documented via docs/data_sources.md provenance ledger (SHA-256 of raw snapshots persisted locally per project rule; raw data not redistributed).
