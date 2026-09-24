# WRF counterfactual scenarios (Phase 7 — NOT RUN on this VM)

6 deployment states driven by `windturbines.txt` placement:
- S0     : no turbines (counterfactual baseline)
- S50    : capacity as of 2005
- S100   : capacity as of 2010
- S150   : capacity as of 2021 (full deployment; data/processed/turbines.csv)
- S150u  : 2021 deployment shifted 200 km upwind (siting sensitivity)
- S150d  : 2021 deployment shifted 200 km downwind (negative control)

Events (MJJAS European heatwaves, ERA5-based):
2019-07-22..28 (Western Europe), 2018-07-30..08-05 (Iberia),
2015-07-01..07 (Central Europe), 2003-08-01..13 (historic, optional).

Ensemble: 3 perturbed initial conditions per scenario x event
(ERA5 perturbed with 0.5 K / 1 m/s seed noise; seed = 20260924+k).

Per run: 10-day window = 3d spinup + 7d event.
Outputs needed: t2, qvapor column, u10/v10, PBLH, SWDOWN, RAINNC hourly on d02.

## Budget (documented, exceeds VM >100x)
WRF 4.x, 45 levels, d01 27km + d02 9km over Europe:
~90 min walltime per simulated day on 64 cores; 10 days x 6 scen x 4 events
x 3 members = 720 scenario-days ≈ 68,000 core-hours ≈ 1,100 node-days.
Storage: ~40 GB/event-member (d02 hourly) -> ~29 TB total (subset archiving).
Marked NOT RUN; see COMPUTE_BUDGET.md.
