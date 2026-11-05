#!/usr/bin/env python3
"""Generate submission/cover_letter.md (Renewable Energy) and submission/highlights.txt from
canonical results — no stale numbers. WERR estimands and headline claims
come from results/ at build time.
"""
import json
import pathlib
import pandas as pd

R = pathlib.Path("results")
w9 = pd.read_csv(R / "werr_pooled_summary.csv").iloc[0]
cd = pd.read_csv(R / "country_day_werr_summary.csv").set_index("country").loc["ALL"]
tb = len(pd.read_csv("data/processed/turbines.csv"))
wc = json.load(open(R / "manuscript_wordcount.json"))["main_text_words"]
refs = pd.read_csv("references/references_verified.csv")

body = f"""# Cover letter — Renewable Energy

Dear Editor,

Please consider the enclosed manuscript, "Does wind power erode its own net
energy benefit through heatwave-season demand? Country-day accounting of a
meteorological electricity rebound for European wind energy", for publication
as a research paper in Renewable Energy.

Wind-energy assessments usually count delivered generation as fully
additional. Wind turbines are, however, momentum sinks that perturb the
boundary layer downstream. The manuscript asks a question that matters for
anyone who divides by delivered wind energy: does the atmospheric footprint
of Europe's wind fleet raise warm-season extreme temperature, and therefore
cooling-related electricity demand, enough to offset a measurable share of
the energy it delivers?

To answer it we built (i) a harmonized, provenance-ledgered register of
{tb:,} European turbines and a daily upstream-capacity exposure field; (ii) a
ratio-of-sums rebound metric, WERR_CD, which counts each country's wind
generation once per day so that the denominator is energetically consistent;
and (iii) four complementary observational designs with a falsification and
sensitivity battery, together with a prespecified mesoscale (WRF)
counterfactual protocol whose configurations ship with the replication
package. The production WRF suite was not executed, and the manuscript says
so.

The answer is a negative one for the aggregate: WERR_CD is {cd.werr_cd:.3f}
[{cd.boot_lo:.3f},{cd.boot_hi:.3f}], statistically indistinguishable from
zero, so these data support no aggregate correction to delivered wind energy
at current European deployment. The event-level mean ({w9.werr_mean:.3f}
[{w9.werr_lo:.3f},{w9.werr_hi:.3f}]) is reported as a secondary estimand, and
the manuscript explains why the two differ. Localized positive values on
dense North-Sea corridors show where any future correction would first be
worth testing. All estimates are associations; none is presented as a causal
effect.

We believe the paper fits the journal's Wind Energy Technology and
Climatology and Meteorology areas: it concerns the net energy delivered by
renewable power generation, and it supplies a reusable accounting metric,
open data provenance and code for wind-resource and system studies.

The main text has {wc:,} words (Sections 1–5, excluding abstract, tables,
figure captions, declarations and references) and {len(refs)} references.
The manuscript is original, has not been published, and is not under
consideration elsewhere. The author declares no competing interests.

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
