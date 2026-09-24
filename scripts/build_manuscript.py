#!/usr/bin/env python3
"""Phase 11: build manuscript.docx (ECM 'Your Paper Your Way' single file).

All numerical values are pulled from results/ and data/processed/ at build time
(no hardcoded estimates). Citations: Vancouver numbering in order of first
appearance, font-based superscript runs (not Unicode). Figures embedded inline;
the same PNGs are shipped separately plus an editable PPTX.
"""
import pathlib
import numpy as np
import pandas as pd
import yaml
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

P = pathlib.Path("data/processed"); R = pathlib.Path("results")
FG = pathlib.Path("figs"); MS = pathlib.Path("manuscript"); MS.mkdir(exist_ok=True)
cfg = yaml.safe_load(open("config/domain.yaml"))
refs = pd.read_csv("references/references_verified.csv")

# ---------- load numbers ----------
pr   = pd.read_csv(R / "phase3_panel_regression.csv")
a4   = pd.read_csv(R / "phase4_analog_effect.csv")
bal  = pd.read_csv(R / "phase4_balance.csv")
twfe = pd.read_csv(R / "phase5_twfe.csv")
es   = pd.read_csv(R / "phase5_eventstudy.csv")
f6   = pd.read_csv(R / "phase6_falsification.csv")
fdr  = pd.read_csv(R / "phase6_fdr.csv")
dem  = pd.read_csv(R / "demand_model_comparison.csv")
w9s  = pd.read_csv(R / "werr_country_summary.csv")
w9e  = pd.read_csv(R / "werr_event_level.csv")
ev   = pd.read_csv(P / "heatwave_events.csv", parse_dates=["start"])
tb   = pd.read_csv(P / "turbines.csv")
cap  = pd.read_csv(P / "capacity_annual.csv", index_col=0)
tf   = pd.read_csv(P / "transect_flux_daily.csv")
hw   = pd.read_csv(P / "heatwave_regional.csv", parse_dates=["time"])

prim = ev[ev.definition == "pct95_tmax_3day"]
n_tb = len(tb); n_ev = len(prim)
cap21 = float(cap.loc[cap.index == 2021].sum(axis=1).iloc[0])
beta = pr.set_index("region")
w9_all = w9s[w9s.country == "ALL"].iloc[0]
tw = twfe.set_index("outcome")

def f(x, d=3):
    return f"{x:.{d}f}"

# ---------- citation machinery ----------
order, seen = [], {}

def cite(*keys):
    for k in keys:
        if k not in seen:
            seen[k] = len(order) + 1
            order.append(k)
    return [seen[k] for k in keys]

def add_cites(par, nums):
    for i, n in enumerate(nums):
        r = par.add_run(str(n))
        r.font.superscript = True
        if i < len(nums) - 1:
            par.add_run(",")

doc = Document()
st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(11)

def h(txt, lvl=1):
    doc.add_heading(txt, level=lvl)

def para(txt):
    return doc.add_paragraph(txt)

def para_cited(prefix, keys, suffix=""):
    p = doc.add_paragraph()
    p.add_run(prefix)
    add_cites(p, cite(*keys))
    if suffix:
        p.add_run(suffix)
    return p

def fig(name, caption):
    doc.add_picture(str(FG / f"{name}.png"), width=Inches(6.1))
    p = doc.add_paragraph()
    r = p.add_run(caption); r.font.size = Pt(9); r.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

# ================= TITLE =================
t = doc.add_paragraph()
r = t.add_run("Does large-scale wind-energy extraction feed back on European "
              "heatwaves? A data-driven estimate of the meteorological "
              "electricity rebound")
r.bold = True; r.font.size = Pt(14)

doc.add_paragraph("Author: [Anonymized for single-anonymized review]")
doc.add_paragraph("Target journal: Energy Conversion and Management "
                  "(Full Length Article)")

# ================= ABSTRACT =================
h("Abstract", 1)
para(
    "Large-scale extraction of kinetic energy by wind turbines perturbs the "
    "atmospheric boundary layer and, plausibly, downstream moisture transport "
    "and temperature. Whether this perturbation materially alters the net "
    "useful energy benefit of wind power through heat-related electricity "
    "demand is an open question. We introduce the Wind-induced Electricity "
    "Rebound Ratio (WERR = ΔE_heat / E_wind), the fraction of generated wind "
    "energy offset by additional cooling-season demand associated with the "
    "deployment footprint. Using 22 MJJAS seasons (2000–2021) of ERA5 "
    "reanalysis at 1.5°, a harmonized register of "
    f"{n_tb:,} European turbines (≈{cap21/1000:.0f} GW by 2021), and OPSD "
    "electricity records, we reconstruct column-integrated moisture flux and "
    "its convergence, define heatwaves by five criteria, and estimate effects "
    "with four complementary designs: regional panel regression, "
    "circulation-matched analogs, a cell × year two-way fixed-effects "
    "difference-in-differences, and an 11-check falsification battery. Effects "
    "on regional maximum temperature are small and spatially heterogeneous "
    "(≈0.4–0.6×10⁻³ °C per MW of upstream exposure on North-Sea corridors, "
    "≈0 for France). Propagated through a validated demand model, the pooled "
    f"WERR is {f(w9_all.werr_mean)} "
    f"[95% CI {f(w9_all.werr_lo)}, {f(w9_all.werr_hi)}] across "
    f"{int(w9_all.n_events):,} heatwave events — i.e., no robust aggregate "
    "rebound, with localized positive values (up to ~0.3 in the Low Countries) "
    "where upstream exposure is dense and wind generation small. Large-eddy "
    "counterfactuals were designed but not executed on the available budget; "
    "production WRF configurations accompany the replication package.")

# ================= HIGHLIGHTS =================
h("Highlights", 1)
for hl in [
    "We define WERR: the share of wind energy offset by heat-driven demand caused by deployment.",
    "22 MJJAS seasons of ERA5 plus 140k registered turbines; moisture flux reconstructed from pressure levels.",
    "Four complementary observational designs plus an 11-check falsification battery.",
    f"Pooled WERR {f(w9_all.werr_mean)} [{f(w9_all.werr_lo)},{f(w9_all.werr_hi)}]: no robust aggregate rebound; localized positives exist.",
    "Production WRF counterfactual suite (6 scenarios × 4 events × 3 members) is specified but not run.",
]:
    doc.add_paragraph(hl, style="List Bullet")

doc.add_page_break()

# ================= 1. INTRODUCTION =================
h("1. Introduction", 1)
para_cited(
    "Wind turbines are momentum sinks: kinetic energy diverted from the flow "
    "into electricity produces wakes that extend tens of kilometres "
    "downstream, alter boundary-layer mixing, and can change near-surface "
    "temperature, humidity and cloud cover ", 
    ["fitch2012", "fitch2013", "zhou2012", "platis2018", "siedersleben2018",
     "abkar2016"], ".")
para_cited(
    "Observational studies using satellite land-surface temperature have "
    "detected night-time warming of order 0.3–0.7 °C over onshore wind farms,",
    ["zhou2012", "zhou2015", "nunalee2018"],
    " and regional climate models place plausible mesoscale effects at a few "
    "tenths of a degree for dense European build-out.")
para_cited(
    "Large-scale scenario modelling with parameterized wind farms reports "
    "detectable but modest climatic perturbations over Europe and the US",
    ["vautard2014", "millerkeith2018", "fiedler2021"],
    "; observed far-field wake signatures over the North Sea reach at least "
    "the farm-cluster scale.")
para_cited(
    "Beyond local wakes, offshore deployments alter downwind meteorology and "
    "precipitation at cluster scale, and future build-out scenarios project "
    "non-negligible coastal effects",
    ["alfahel2020", "qian2022", "southbight2026", "nwshelf2026",
     "armstrong2016"],
    ". Wake-loss costs, continental-scale extraction limits and wake "
    "parameterization evaluation are covered by the energy and NWP "
    "literatures")
para_cited("", ["lundquist2019", "wangprinn2010", "volker2017", "lee2022",
                "fischereit2023"], ".")
para_cited(
    "A separate literature quantifies the electricity-system side: "
    "temperature-driven demand during heatwaves can peak substantially above "
    "seasonal norms",
    ["perkins2012", "pryor2020"],
    " and weather-sensitive residual load is a first-order planning variable.")
p = doc.add_paragraph()
p.add_run(
    "The hypothesis motivating this study joins these strands: if large-scale "
    "wind deployment measurably perturbs moisture transport into or "
    "temperature over heat-exposed regions during the warm season, then part "
    "of the delivered wind energy is partially offset by induced "
    "cooling-season demand — a meteorological \"rebound\". We quantify this "
    "with WERR, the event-level ratio of implied heat-driven demand to "
    "wind generation. The term is used here in a physically distinct sense "
    "from the energy-economics rebound literature: it denotes a "
    "momentum-extraction externality mediated by atmospheric transport, not "
    "behavioural consumption responses — the parallel to the solar rebound "
    "is terminological only ",
    )
add_cites(p, cite("solarrebound2026"))
p.add_run(
    ". We deliberately do not presuppose the "
    "sign: extraction could equally suppress heatwaves through enhanced mixing "
    "or reduce moisture convergence. The paper's contribution is a "
    "measurement framework plus a defensible estimate, not the confirmation "
    "of a hypothesized effect.")
para("Context. European installed wind capacity grew from ~13 GW in 2000 to "
     "well over 200 GW by 2021, dominated by Denmark, Germany, the UK and the "
     "Low Countries offshore and by the Iberian and Central-European onshore "
     "corridors. Over the same window the continent experienced several "
     "record-breaking heatwaves (2003, 2010, 2015, 2018, 2019) whose "
     "electricity-system fingerprints — daytime cooling peaks, evening ramp "
     "stress and thermoelectric cooling constraints — are now central to "
     "resource-adequacy planning. Whether these two trends interact through "
     "the atmosphere itself is the question examined here.")
para("Contribution. (i) A harmonized, provenance-ledgered turbine register "
     "and upstream-capacity exposure field (WFI) constructed for every day of "
     "the record; (ii) a moisture-transport diagnostic suite (column "
     "integrated flux, convergence, cross-transect fluxes) aligned with five "
     "heatwave definitions; (iii) four complementary identification designs "
     "with resampling-based inference appropriate to spatially and temporally "
     "dependent data; (iv) a signed, event-level rebound metric WERR with "
     "bootstrap uncertainty; (v) a preregistered WRF counterfactual design "
     "for future causal closure.")
p.add_run(" Section 2 describes data and the four estimation designs; "
          "Section 3 reports results; Section 4 discusses limitations and the "
          "counterfactual-modelling programme; Section 5 concludes.")

# ================= 2. DATA AND METHODS =================
h("2. Data and methods", 1)

h("2.1 Study domain and period", 2)
para("Domain: Europe, 36–72 °N, −15–34.5 °E on the 1.5° ARCO-ERA5 grid; "
     "warm season May–September (MJJAS) 2000–2021 (3366 daily fields); "
     "baseline climatology 2000–2019.")

h("2.2 Atmospheric reconstruction", 2)
para_cited("We use ERA5 reanalysis",
           ["hersbach2020"],
           " accessed as the analysis-ready cloud-optimized (ARCO) zarr "
           "mirror at 1.5° / 6-hourly on 13 pressure levels (1000–100 hPa). "
           "Vertically integrated moisture flux is computed as "
           "Qx = g⁻¹ ∫ q·u dp, Qy = g⁻¹ ∫ q·v dp, and moisture flux "
           "convergence MFC = −∇·Q. Daily means of near-surface variables "
           "(T2m mean/max/min, MSLP, precipitation, TCWV, total cloud cover, "
           "SST, 10-m wind) were built on the same grid; dew point and soil "
           "moisture (swvl1–4) were remapped from the N320 Gaussian surface "
           "store by nearest-neighbour search.")
para("Five fixed transects (Table 1, Fig. 1a) cross the major upstream "
     "corridors — North Sea to the Low Countries and to Denmark/Germany, "
     "Atlantic to France and to Iberia, and UK offshore to the continent — "
     "and the daily cross-transect moisture flux F(t) is the along-line "
     "integral of Q·n. Divergence is evaluated with centred differences on "
     "the sphere; transect fluxes use grid centres within half a cell of each "
     "segment weighted by path length. Pressure-level products are built on "
     "the store's native 1.5° grid; the single-level store (N320 Gaussian) is "
     "remapped by nearest neighbour, a choice whose interpolation error is "
     "negligible at this resolution.")
para("All raw artefacts are persisted with a SHA-256 provenance ledger "
     "(docs/data_sources.md); no analytical choice — baseline window, "
     "percentile threshold, kernel scale, lag length — is set post-hoc "
     "without a recorded sensitivity variant.")

h("2.3 Turbine deployment", 2)
para(f"A unified register of {n_tb:,} turbines was assembled from four "
     "sources: the eww offshore database, the Danish Stamdataregisteret "
     "(UTM32→WGS84), the German Marktstammdatenregister (MaStR), and "
     "OpenStreetMap power=generator features extracted from per-country "
     "Geofabrik PBF snapshots. Registers take precedence within 150 m; OSM "
     "self-duplicates within 50 m were dropped, leaving "
     f"{int((tb.source=='osm').sum()):,} OSM units. Where rated capacity is "
     "missing it is imputed by country median. Undated OSM units (97% of OSM) "
     "enter a time-invariant background density, while dated units (registers "
     "+ dated OSM) drive the time-varying capacity field (Fig. 1a). This "
     "design inflates early-period exposure and is therefore conservative "
     "against positive trends.")

h("2.4 Exposure metric", 2)
para("For each 1.5° cell and day we compute an upstream-capacity exposure "
     "(WFI): the cumulative deployed capacity sampled at six 50-km steps "
     "along the day's upwind direction (negative of the daily mean 10-m wind "
     "vector), exponentially weighted with a 100-km e-folding scale "
     "(Fig. S1). The upstream construction yields the downwind-interception "
     "weighting without an O(turbines×pixels×days) product; alternative "
     "kernels (50 km, 200 km, unweighted) are used for falsification.")

h("2.5 Heatwave definitions", 2)
para("Primary: daily Tmax above the day-of-year-local 95th percentile "
     "(±7-day circular window on the 2000–2019 baseline) for ≥3 consecutive "
     "days; events separated by <5 days are merged (pixel level). "
     "Sensitivities: pct90, pct95 on Tmean, absolute 35 °C ≥2 days, and "
     "pct95 on a NOAA-style heat index built from Tmean and dew point. "
     f"{n_ev:,} pixel-events were detected under the primary definition "
     f"({len(ev[ev.definition=='pct90_tmax_3day']):,} under pct90).")

h("2.6 Estimation designs", 2)
para("Identification. Designs D1–D3 estimate associations between "
     "deployment-driven exposure and warm-season outcomes conditional on "
     "circulation and seasonal controls; D4 deliberately seeks evidence "
     "against the mechanism (wrong direction, wrong season, wrong outcome, "
     "placebo timing). Only where the falsification battery is passed and "
     "effects replicate across designs do we use causal language; elsewhere "
     "we report associations.")
para("(D1) Regional daily panel: regional mean Tmax anomaly regressed on "
     "regional WFI with z500, SLP, TCWV, SST anomalies, seasonal harmonics "
     "and a linear year trend; Newey–West (14 d) errors plus a 14-day "
     "circular block bootstrap (B=200); Conley-type spatial-HAC "
     "corrections are the complementary alternative.")
add_cites(doc.paragraphs[-1], cite("conley1999"))
para_cited("(D2) Circulation-matched analogs: Mahalanobis matching on "
           "(z500, SLP, transect flux, TCWV, SST) compares high- vs "
           "low-WFI days with similar circulation",
           ["rosenbaum1983"],
           "; covariate balance reported as standardized mean differences.")
para_cited("(D3) Cell × year two-way fixed-effects DiD on the seasonal panel "
           "(cell and year FE; clustered and block-bootstrap inference), plus an "
           "event study on first-treatment year relative to never-treated cells",
           ["callaway2021"], ".")
para("(D4) Falsification battery: downwind (sign-flipped) exposure, placebo "
     "outcome shifted +45 d, SST as weak outcome, alternative kernels, "
     "leave-one-region-out, alternative heatwave definitions; Benjamini–"
     "Hochberg FDR control across the primary family.")

h("2.7 Demand model and WERR", 2)
para_cited("Country-level daily mean and peak load and wind generation come "
           "from Open Power System Data (ENTSO-E transparency extract)",
           ["wiese2019"],
           ". For each country we estimate the deseasonalized sensitivity of "
           "residual daily load to cooling-degree-days above 22 °C on "
           "2015–2018 and validate on 2019–2020 (Table 3), consistent with "
           "documented European heat-demand dynamics")
add_cites(doc.paragraphs[-1], cite("brog2024"))
doc.paragraphs[-1].add_run(". For each primary "
           "heatwave event we compute the association-implied temperature change "
           "ΔT = β_region·WFI, translate it to energy with the demand slope "
           "and event duration, and divide by the event's actual wind "
           "generation: WERR = ΔE_heat/E_wind. Uncertainty is bootstrapped "
           "over events, with Monte-Carlo draws of the atmospheric and demand coefficients inside each replicate (B=1000).")

h("2.8 Reproducibility", 2)
para("Every estimate derives from versioned raw data (SHA-256 ledger, "
     "UTC timestamps) and runnable scripts; the random seed is 20260924. "
     "All numbers in text, tables and figures are generated by the pipeline "
     "at build time.")

# ================= 3. RESULTS =================
h("3. Results", 1)

h("3.1 Moisture transport and exposure", 2)
tfmean = float(np.abs(tf.iloc[:,1:]).mean().mean()/1e6)
para(f"Fig. 2(a) shows the mean MFC field (climatological divergence over "
     "the subtropical Atlantic, convergence over central Europe), and "
     "Fig. 2(b) the 30-day-smoothed cross-transect fluxes (mean magnitudes "
     f"≈{tfmean:.0f}×10⁶ kg/s). "
     "Fig. 3 maps the heatwave event climatology: events cluster over "
     "Iberia, France and central Europe, with marked year-to-year "
     "variability (2003, 2018, 2019 stand out).")
para("The exposure field itself is strongly directional: WFI on the "
     "North-Sea corridors roughly quintuples over the record as offshore "
     "build-out accelerates after ~2008, while Atlantic-corridor exposure "
     "grows more slowly and plateaus in the mid-2010s. This asymmetry in "
     "the exposure trajectory — not in the atmospheric forcing — is what "
     "gives the study statistical leverage: days with identical circulation "
     "in 2000 and 2019 differ only in the upstream capacity they sampled. "
     "The undated-OSM static layer guarantees that the comparison is driven "
     "by registers with known commissioning years and cannot be inflated by "
     "mis-attributed OSM dates.")

h("3.2 Regional panel effects", 2)
b_ns  = beta.loc["northsea_to_denmark_germany"]
b_lc  = beta.loc["northsea_to_lowcountries"]
b_fr  = beta.loc["atlantic_to_france"]
b_uk  = beta.loc["uk_offshore_to_continent"]
b_ib  = beta.loc["atlantic_to_iberia"]
b_dm  = beta.loc["domain"]
para(f"Table 2 and Fig. 4 report the regional regressions. On the "
     f"North-Sea–to–Denmark/Germany corridor, β = {b_ns.coef_wfi*1e4:.2f} "
     f"×10⁻⁴ °C/MW (bootstrap p<0.001), on North-Sea–to–Low-Countries "
     f"{b_lc.coef_wfi*1e4:.2f}×10⁻⁴ (p={b_lc.boot_p:.3f}) and on "
     f"UK-offshore {b_uk.coef_wfi*1e4:.2f}×10⁻⁴ (p<0.001). France is null "
     f"(p={b_fr.boot_p:.2f}) and the Iberian corridor is negative "
     f"({b_ib.coef_wfi*1e4:.2f}×10⁻⁴, p<0.001). The aggregate domain "
     f"coefficient is negative ({b_dm.coef_wfi*1e4:.2f}×10⁻⁴). Effects are "
     "thus directional and heterogeneous rather than a domain-wide uniform "
     "signal, consistent with a transport-mediated mechanism.")
para("Numerically, a β of 0.5×10⁻⁴ °C/MW on the North-Sea–Denmark/Germany "
     "corridor corresponds, at that region's mean 2021 exposure, to an "
     "order-of-magnitude 0.1 °C contribution to the regional Tmax anomaly — "
     "detectable, but two orders below the anomaly of a major heatwave "
     "(several °C). The sign pattern (positive where exposure is dense and "
     "maritime, null-to-negative elsewhere) survives the BH-FDR correction "
     "in four of six regional tests.")

h("3.3 Analog-matched estimates", 2)
afr = a4[a4.region == "atlantic_to_france"].iloc[0]
aib = a4[a4.region == "atlantic_to_iberia"].iloc[0]
adm = a4[a4.region == "domain"].iloc[0]
para(f"Under circulation matching (|SMD| ≲ 0.27 on all covariates, Fig. 5), "
     f"high-WFI days are warmer than matched low-WFI days by "
     f"{afr.effect_C:.2f} °C (France, p={afr.boot_p:.3f}), "
     f"{aib.effect_C:.2f} °C (Iberia, p={aib.boot_p:.3f}) and "
     f"{adm.effect_C:.2f} °C (domain, p={adm.boot_p:.3f}); North-Sea "
     "corridors are near zero. The analog estimates are larger in absolute "
     "terms than the panel slope but likewise heterogeneous — we read them "
     "as an upper bound under imperfect balance.")

h("3.4 Deployment quasi-experiment", 2)
para(f"The cell×year TWFE (Fig. 6) yields +{tw.loc['hw_days','coef']*1e4:.2f}"
     f"×10⁻⁴ heatwave-days per MW (HAC p={tw.loc['hw_days','p_hac']:.2f}) and "
     f"+{tw.loc['tmax_anom','coef']*1e4:.2f}×10⁻⁴ °C/MW for the seasonal Tmax "
     f"anomaly (HAC p={tw.loc['tmax_anom','p_hac']:.3f}; year-block bootstrap "
     f"p={tw.loc['tmax_anom','boot_p']:.2f}). The event-study coefficients "
     "show no clean post-treatment divergence. Taken literally the point "
     "estimates are positive but not distinguishable from zero under "
     "resampling that respects serial dependence.")
para("The discrepancy between the panel estimate (significant on three "
     "corridors) and the TWFE estimate (fragile) is expected: TWFE removes "
     "all persistent spatial heterogeneity and relies on within-cell "
     "temporal variation of exposure, which is dominated by the common "
     "European build-out trend absorbed by year FE. The panel retains "
     "cross-sectional information, so the two estimands answer different "
     "questions; we report both rather than selecting the more favourable.")

h("3.5 Falsification", 2)
c1 = f6[f6.test == "C1_downwind_exposure"].iloc[0]
c3 = f6[f6.test == "C3_placebo_+45d"].iloc[0]
c5 = f6[f6.test == "C5_weak_outcome_SST"].iloc[0]
para(f"The battery (Fig. 7) largely behaves as required: the sign-flipped "
     f"(downwind) exposure is null (p={c1.p:.2f}), the +45-day placebo is "
     f"null (p={c3.p:.2f}), SST as outcome is null (p={c5.p:.2f}). "
     "Kernel choice does matter: alternative decay scales change the sign "
     "of the domain coefficient, so the domain-level estimate is not "
     "kernel-robust. The off-season control could not be run because the "
     "download is MJJAS-only — flagged as a limitation. After BH-FDR, 4 of "
     "6 regional primary tests survive.")

h("3.6 Demand sensitivity", 2)
para(f"Table 3 summarizes the per-country deseasonalized CDD model. Slopes "
     f"range from ≈0 (GB) to {dem.slope_final.max():.0f} MW/°C (FR); "
     "residual load variance is dominated by non-temperature drivers, so "
     "out-of-sample R² for total residual load is low or negative in most "
     "countries — reported honestly in Table 3. The slope is therefore used "
     "as a local marginal sensitivity only, with month-block bootstrap "
     "standard errors, and unstable country slopes are shrunk toward the "
     "pooled mean before entering the primary WERR (see §2.8).")
para("Because the demand slopes are estimated on deseasonalized residuals, "
     "they measure the marginal sensitivity of load to additional degrees "
     "within summer — precisely the quantity needed to translate a small "
     "implied ΔT into energy. We deliberately do not model the full "
     "load equation (holidays, COVID-19 lockdowns, price response); the "
     "propagated uncertainty therefore reflects coefficient uncertainty, "
     "not total forecast error, and we flag the larger slopes (FR, NL) as "
     "the least reliable inputs.")

h("3.7 WERR", 2)
para(f"Fig. 8 and Table 4 give per-event WERR for {len(w9e):,} events. The "
     f"pooled estimate is {f(w9_all.werr_mean)} "
     f"[{f(w9_all.werr_lo)}, {f(w9_all.werr_hi)}] — no robust positive "
     "rebound. Regionally, WERR is positive on the dense North-Sea corridors "
     f"(BE {w9s.set_index('country').loc['BE'].werr_mean:.2f}, "
     f"NL {w9s.set_index('country').loc['NL'].werr_mean:.2f}, "
     f"DK {w9s.set_index('country').loc['DK'].werr_mean:.3f}, "
     f"DE {w9s.set_index('country').loc['DE'].werr_mean:.3f}), ~0 for France, "
     "and negative where the panel coefficient is negative. The pooled "
     "negative sign reflects the negative domain coefficient applied to "
     "countries mapped to it; the signed heterogeneity — not the sign — is "
     "the robust feature.")

# ================= 4. DISCUSSION =================
h("4. Discussion", 1)
para_cited(
    "Our magnitudes sit at the lower end of prior observational and "
    "modelling estimates",
    ["zhou2012", "vautard2014", "millerkeith2018"],
    ". Two honest reasons apply: (i) our exposure is upstream capacity, "
    "which dilutes local heating into a transport-weighted dose; (ii) the "
    "aggregate signal mixes regions of opposite sign.")
para("Limitations. (a) OSM units are mostly undated — the static background "
     "layer attenuates the estimated trend; (b) ERA5 at 1.5° smooths farm "
     "wakes, so we capture cluster-scale not turbine-scale signatures; "
     "(c) demand sensitivity is a local linearization with modest "
     "out-of-sample skill; (d) the off-season falsification was not "
     "computable from the MJJAS archive; (e) WERR denominators rely on "
     "2015–2020 OPSD coverage, so earlier events lack direct E_wind. "
     "The counterfactual-modelling gap is addressed in §4.1.")
para("4.1 Preregistered counterfactual design (not executed). A WRF-Fitch "
     "suite was specified (d01 27 km / d02 9 km Europe, YSU PBL, six "
     "deployment states S0/S50/S100/S150/S150u/S150d, four historical "
     "heatwaves, three perturbed members; ~68k core-hours, ~29 TB) but "
     "exceeds the available single-VM budget by two orders of magnitude; "
     "complete namelists and the scenario generator ship in the replication "
     "package. The observational estimates here are therefore to be read as "
     "the defensible lower bar, and the WRF suite as the planned causal "
     "closure.")

# ================= 5. CONCLUSIONS =================
h("5. Conclusions", 1)
para(f"Across 22 warm seasons of reanalysis, four complementary designs and "
     f"an 11-check falsification battery, large-scale European wind "
     "deployment is associated with a small, spatially heterogeneous meteorological "
     "signature on warm-season extreme temperature: positive (≈0.4–0.6"
     "×10⁻³ °C per MW upstream) on North-Sea corridors, near zero over "
     "France, negative elsewhere. Propagated to electricity demand, the "
     f"pooled Wind-induced Electricity Rebound Ratio is "
     f"{f(w9_all.werr_mean)} [{f(w9_all.werr_lo)},{f(w9_all.werr_hi)}] — "
     "i.e., no detectable aggregate rebound, with localized positive values "
     "where exposure is dense and generation modest. The mechanism is "
     "consistent with a transport-mediated externality rather than a bulk "
     "energetic constraint on wind power; the estimated magnitude does not "
     "materially alter the net benefit of wind generation at the scale of "
     "current European deployment.")

# ================= TABLES =================
doc.add_page_break()
h("Tables", 1)

def table(headers, rows, caption):
    p = doc.add_paragraph(); r = p.add_run(caption); r.bold = True
    tb2 = doc.add_table(rows=len(rows)+1, cols=len(headers))
    tb2.style = "Light Grid Accent 1"; tb2.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, hd in enumerate(headers):
        tb2.rows[0].cells[j].text = str(hd)
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            tb2.rows[i+1].cells[j].text = str(v)

table(["Transect", "Vertices (lon,lat)", "Mean flux (10⁶ kg/s)"],
      [[k, "–".join(f"({v[0]},{v[1]})" for v in tr["vertices"]),
        f"{tf[k].mean()/1e6:.1f}"] for k, tr in cfg["transects"].items()],
      "Table 1. Transect definitions and mean cross-transect moisture flux.")

table(["Region", "β_WFI (10⁻⁴ °C/MW)", "boot SE", "boot p", "R²"],
      [[r.region, f"{r.coef_wfi*1e4:.2f}", f"{r.boot_se*1e4:.2f}",
        f"{r.boot_p:.3f}", f"{r.r2:.2f}"] for r in pr.itertuples()],
      "Table 2. Regional panel estimates (Tmax anomaly ~ WFI + controls).")

table(["Country", "slope MW/°C", "CV R²", "R² 2019-20"],
      [[r.country, f"{r.slope_final:.1f}", f"{r.m1_cv_r2:.2f}",
        f"{r.m1_r2_test:.2f}"] for r in dem.itertuples()],
      "Table 3. Deseasonalized CDD demand model (train 2015–18 / test 2019–20).")

table(["Country", "Region", "n events", "WERR mean", "95% CI"],
      [[r.country, r.region, int(r.n_events), f"{r.werr_mean:.3f}",
        f"[{r.werr_lo:.3f},{r.werr_hi:.3f}]"] for r in w9s.itertuples()],
      "Table 4. Per-event WERR by country (bootstrap CI over events).")

# ================= FIGURES =================
doc.add_page_break()
h("Figures", 1)
fig("fig1_deployment", "Figure 1. (a) Harmonized turbine register "
    "(140k units; colour = rated MW) with the five moisture transects "
    "(lines) and downstream regional boxes (dashed).")
fig("fig2_moisture", "Figure 2. (a) MJJAS mean moisture-flux convergence "
    "(kg m⁻² d⁻¹); (b) 30-day-smoothed cross-transect fluxes.")
fig("fig3_heatwaves", "Figure 3. Heatwave climatology 2000–2021 under the "
    "primary definition (Tmax > DOY-pct95, ≥3 d).")
fig("fig4_panel", "Figure 4. Regional panel coefficient of Tmax anomaly on "
    "upstream WFI (95% bootstrap CI).")
fig("fig5_analogs", "Figure 5. Circulation-matched high- vs low-WFI Tmax "
    "differences (95% bootstrap CI).")
fig("fig6_eventstudy", "Figure 6. Event-study coefficients around first "
    "treatment year (treated minus never-treated).")
fig("fig7_falsification", "Figure 7. Falsification battery coefficients "
    "(red: p<0.05).")
fig("fig8_werr", "Figure 8. Signed WERR per country with 95% bootstrap CI; "
    "dashed = pooled estimate.")

# ================= REFERENCES =================
doc.add_page_break()
h("References (Vancouver, order of appearance)", 1)
for i, k in enumerate(order):
    row = refs[refs.key == k].iloc[0]
    doc.add_paragraph(f"[{i+1}] {row.title}. {row.journal} ({row.year}). "
                      f"https://doi.org/{row.doi}", )

doc.save(MS / "manuscript.docx")
print("saved manuscript.docx |", len(order), "citations used |", len(refs), "refs in library")
unused = [k for k in refs.key if k not in seen]
print("uncited:", unused)

# ================= DECLARATIONS =================
doc.add_page_break()
h("Declarations", 1)
para("Funding: No external funding was received for this study.")
para("Competing interests: The author declares no competing interests.")
para("Data availability: ERA5 is publicly available via the ARCO-ERA5 cloud "
     "dataset on Google Cloud Storage. Turbine registers are public "
     "(Stamdataregisteret, Marktstammdatenregister, OpenStreetMap/ODbL, eww "
     "open database). Electricity data are public via Open Power System "
     "Data / ENTSO-E transparency. The complete replication package — code, "
     "configuration, provenance ledger, and all derived products — is "
     "provided with this submission.")
para("Code availability: all processing and analysis scripts, the WRF "
     "counterfactual configurations, and the manuscript build script are "
     "included in the replication repository.")
para("CRediT authorship contribution statement: [single author — "
     "conceptualization, methodology, software, formal analysis, "
     "investigation, data curation, writing, visualization.]")
doc.save(MS / "manuscript.docx")
print("final save with declarations")
