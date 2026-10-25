#!/usr/bin/env python3
"""Generate submission/cover_letter.md and submission/highlights.txt from
canonical results — no stale numbers. WERR estimands and headline claims
come from results/ at build time.
"""
import pathlib
import pandas as pd

R = pathlib.Path("results")
w9 = pd.read_csv(R / "werr_pooled_summary.csv").iloc[0]
cd = pd.read_csv(R / "country_day_werr_summary.csv").set_index("country").loc["ALL"]

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
battery, we find a small, spatially heterogeneous effect. On the
energy-accounting country-day estimand (ratio of summed implied demand to
summed actual generation, each country's wind counted at most once per day)
WERR_CD is {cd.werr_cd:.3f} [{cd.boot_lo:.3f},{cd.boot_hi:.3f}]; the legacy
event-level mean is {w9.werr_mean:.3f} [{w9.werr_lo:.3f},{w9.werr_hi:.3f}].
Neither shows a robust aggregate rebound, with localized positive values on
dense North-Sea corridors and in Ireland.

We believe ECM is the natural venue: the paper sits at the energy-system /
atmospheric-science interface, proposes a reusable metric with a
denominator-consistent estimand, and is honest about the sign and bounds of
the effect. The replication package (data ledger, code, WRF counterfactual
configurations for the prespecified counterfactual suite) accompanies the
submission.

The work is original, not under consideration elsewhere, and free of
competing interests.

Sincerely,
[Author]
"""
pathlib.Path("submission/cover_letter.md").write_text(body)

hl = f"""- WERR: share of wind energy offset by deployment-linked heat demand.
- 22 warm seasons of ERA5 and a 140k-turbine provenance-ledgered register.
- Four designs plus a falsification-and-sensitivity battery (11 checks).
- Country-day WERR_CD {cd.werr_cd:.3f} [{cd.boot_lo:.3f},{cd.boot_hi:.3f}]; event mean {w9.werr_mean:.3f}.
- Production WRF counterfactual suite designed but not executed.
"""
pathlib.Path("submission/highlights.txt").write_text(hl)
print("cover_letter.md + highlights.txt regenerated, WERR_CD", cd.werr_cd)
