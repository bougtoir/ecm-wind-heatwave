# R10 clean reproducibility audit
- Fresh clone (/tmp/clean_checkout, branch revision/ecm-targeted), new venv,
  `pip install -r requirements.txt` — OK.
- `pytest tests/` — 3 passed (compile-all, canonical outputs, pooled row).
- `scripts/make_figures.py`, `scripts/build_manuscript.py`,
  `scripts/p12_qc.py` executed on the clone using shipped processed
  products -> manuscript.docx regenerated (30/30 refs cited) and QC ALL PASS.
- Boundary (documented): raw ERA5/OPSD re-download and the compute-heavy
  WFI grid / panel / WERR loops were not re-executed in the clean env; those
  steps have runnable scripts and the derived inputs are shipped + ledgered.
- Command set: `make figures manuscript qc test` (full `make all` requires
  raw acquisition first).
STATUS: PASS (with the stated raw-acquisition boundary).
