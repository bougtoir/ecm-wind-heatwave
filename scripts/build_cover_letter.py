#!/usr/bin/env python3
"""Generate submission/cover_letter.md from canonical results — no stale
numbers. Pooled WERR and headline claims come from results/ at build time.
"""
import pathlib
import pandas as pd

R = pathlib.Path("results")
w9 = pd.read_csv(R / "werr_pooled_summary.csv").iloc[0]

body = f"""# Cover letter — Energy Conversion and Management

Dear Editor,

We submit "Does large-scale wind-energy extraction feed back on European
heatwaves? A data-driven estimate of the meteorological electricity rebound"
for consideration as a Full Length Article.

The study asks whether momentum extraction by Europe's wind fleet perturbs
warm-season extreme temperature and the associated electricity demand enough
to offset a detectable fraction of delivered wind energy — the WERR metric
introduced here. Using 22 MJJAS seasons of ERA5, a 140k-turbine harmonized
register, and four complementary observational designs with a falsification
battery, we find a small, spatially heterogeneous effect and a pooled WERR
of {w9.werr_mean:.3f} [{w9.werr_lo:.3f},{w9.werr_hi:.3f}]: no robust aggregate
rebound, with localized positive values on dense North-Sea corridors and in
Ireland.

We believe ECM is the natural venue: the paper sits at the energy-system /
atmospheric-science interface, proposes a reusable metric, and is honest
about the sign and bounds of the effect. The replication package (data
ledger, code, WRF counterfactual configurations for the preregistered causal
closure) accompanies the submission.

The work is original, not under consideration elsewhere, and free of
competing interests.

Sincerely,
[Author]
"""
pathlib.Path("submission/cover_letter.md").write_text(body)
print("cover_letter.md regenerated, pooled WERR", w9.werr_mean)
