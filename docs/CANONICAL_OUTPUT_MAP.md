# Canonical output map (manuscript value → generating artifact)
| Item | File | Script |
|---|---|---|
| Turbine register | data/processed/turbines.csv | scripts/build_turbines.py (+parse_mastr, extract_osm_*) |
| WFI daily + grid | data/processed/wfi_daily.csv, wfi_grid_daily.nc, capdensity_YYYY.nc | scripts/build_exposure.py |
| MFC + transect fluxes | data/processed/transect_fluxes.csv, mfc fields | scripts/p2_moisture.py |
| Heatwave events | data/processed/heatwave_events.csv, heatwave_regional.csv, heatwave_mask_daily.nc | scripts/p2_heatwaves.py |
| Regional panel β | results/phase3_panel_regression.csv, phase3_event_composites.csv | scripts/p3_events.py |
| Analog effects/balance | results/phase4_analog_effect.csv, phase4_balance.csv | scripts/p4_analogs.py |
| TWFE + event study | results/phase5_twfe.csv, phase5_eventstudy.csv | scripts/p5_deployment.py |
| Falsification + FDR | results/phase6_falsification.csv, phase6_fdr.csv | scripts/p6_falsification.py |
| Demand model | results/phase8_demand_model.csv | scripts/p8_demand.py |
| WERR | results/phase9_werr_events.csv, phase9_werr_summary.csv | scripts/p9_werr.py |
| Figures | figs/fig1–8 + graphical_abstract | scripts/make_figures.py |
| Manuscript | manuscript/manuscript.docx | scripts/build_manuscript.py |
| QC | results/phase12_qc_report.json | scripts/p12_qc.py |
| WRF configs | wrf/ | wrf/gen_windturbines.py |
