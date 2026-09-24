# NOVELTY AUDIT — Wind deployment → moisture transport → heatwaves → electricity rebound

Audited 2026-09-24. Classification: ESTABLISHED / PARTIALLY ESTABLISHED / APPARENTLY NOVEL / UNCERTAIN.
Verified citations in `references/references_verified.csv` (Crossref-checked).

## A. Quantitative wind deployment → ocean-to-continent moisture transport
**PARTIALLY ESTABLISHED.**
- Modeling: Fitch et al. (2012, MWR) WRF wind-farm parameterization (momentum sink + TKE source);
  Fitch et al. (2013, J. Climate) climate-model WFP; Fischereit et al. (2023, GMD) HARMONIE-AROME
  WFP evaluated against a full year of European forecasts; Comm. Earth & Env. (2026) projects
  post-2050 North Sea deployment reducing coastal precipitation 10–12% (modeled); J. Phys. Conf.
  Ser. (2026) WRF Southern Bight precipitation response.
- Observation: Siedersleben et al. (2018, ERL) offshore micrometeorological impacts;
  Al Fahel & Archer (2020, BAST) observed onshore precipitation changes after offshore builds.
- **Gap**: no study found that quantifies wind deployment → *vertically integrated moisture
  transport* (Q = (1/g)∫qv dp, MFC) along predefined ocean→continent transects from
  observations/reanalysis. Transport-budget framing appears unexplored.

## B. Downstream wind-farm modification → heatwave intensity
**PARTIALLY ESTABLISHED (mechanism) / APPARENTLY UNDEREXAMINED at heatwave level.**
- LST/satellite evidence of local, mostly nocturnal warming: Zhou et al. (2012, NCC; 2015 Sensors);
  Qian et al. (2022, ERL) 319 US farms.
- Large-scale modeling: Wang & Prinn (2010, ACP) GCM; Miller & Keith (2018, Joule) 0.24 °C
  continental-scale warming for 0.5 TW_e idealized US wind; Vautard et al. (2014, Nat. Commun.)
  European RCM finds **limited** impacts (±0.3 °C, 0–5% precip, winter only) — our study must
  engage with this upper bound directly rather than ignore it.
- **Gap**: no observational or event-level study linking deployment to *heatwave
  intensity/duration/Tmax/Tmin downstream* via the moisture/soil-moisture pathway. Vautard's
  limited-impact result means a null/bounded outcome is a scientifically respectable answer.

## C. Meteorological wind-farm effect → cooling/heat-related electricity demand
**APPARENTLY NOVEL.**
- Demand-temperature modeling is ESTABLISHED (ENTSO-E TRAPUNTA/ERAA methodology;
  Appl. Energy 2024 temperature-response functions).
- No study found coupling wind-farm-induced ΔT/Δheatwave metrics to electricity demand, i.e.
  translating the meteorological externality into a system cost/benefit quantity.

## D. WERR = ΔE_heat / E_wind (equivalent terminology)
**APPARENTLY NOVEL as defined; terminology must be disclaimed.**
- "Rebound effect" is established in energy economics (efficiency→demand) and renewables
  (behavioral rebound: SciDirect 2021 framework; solar rebound, Nature Energy 2026). Those are
  **behavioral/economic** rebounds, not meteorological externalities.
- WERR as defined here is a *meteorologically mediated* demand feedback, not behavioral rebound.
  Manuscript will define it as a distinct quantity, cite the rebound literature to position it,
  and avoid claiming the term "rebound" itself.

## E. Siting optimization including downstream meteorological/hydrological externality
**PARTIALLY ESTablished (wake externality) / APPARENTLY NOVEL (meteorological externality).**
- Wake-aware layout/siting and cluster-level wake externalities are established (two-scale
  theory, layout/control co-design literature).
- Optimization including downstream *meteorological/hydrological* externalities (induced
  cooling demand) not found → Phase 10 conditional as instructed.

## Interpretation guardrails (predefined)
- Clear support: signed downstream Δ in Q/MFC/SM/T + material WERR → net-energy paper.
- Negligible WERR with real physical effect: report quantified upper bound (consistent with
  Vautard 2014) — emphasize materiality test, do not exaggerate.
- Null physical effect: strong constraints/upper bounds; skip Phase 10.
- Heterogeneous/opposite signs: report conditions determining sign; preserve heterogeneity.
