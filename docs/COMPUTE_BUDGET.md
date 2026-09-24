# COMPUTE BUDGET — single VM (Phase 0 estimate)

VM resources: 2 vCPU, 7 GB RAM, ~100 GB free disk, no GPU, no CDS key stored.

| Work item | Planned scale | Est. resource | Feasibility | Decision |
|---|---|---|---|---|
| ERA5 surface vars (t2m,d2m,sp,msl,tp,e,sshf,slhf,pblh,skl,sst) Europe, MJJAS 2000-2024, hourly→daily | ARCO-ERA5 zarr, subset 37N..72N,15W..35E | ~50 GB network, ~15 GB stored daily fields, 4-8 h CPU | FEASIBLE via ARCO-ERA5 (anonymous GCS zarr); no CDS key needed | RUN |
| ERA5 pressure-level q,u,v (8 levels 850-400 hPa) for Q | same subset, MJJAS only | ~15 GB network, 2-4 h | FEASIBLE | RUN |
| Moisture transport Q, MFC, transects | daily, 0.25deg | CPU-hours | FEASIBLE | RUN |
| Turbine deployment DB | GEM Global Wind Power Tracker + OPSD renewable plants + OSM fallback | negligible | FEASIBLE | RUN |
| Electricity load/wind generation | OPSD time-series (hourly, multi-country, ~2015-2020) + national portals; ENTSO-E needs token (not provisioned) | negligible | FEASIBLE w/ OPSD | RUN (ENTSO-E: NOT RUN without token) |
| Analog matching / event study | grid-cell scale | CPU-minutes-hours | FEASIBLE | RUN |
| WRF counterfactual ensemble (S0..S150, multi-event, perturbed ICs) | production: ~days-weeks on HPC (>=32 cores, 100s GB) | exceeds VM by >100x | NOT FEASIBLE here | NOT RUN on VM — production WRF namelists/scripts + exact budget prepared; optionally a validated km-scale pilot IF time permits |
| Spatial bootstrap / Monte Carlo | B=1000 | CPU-hours | FEASIBLE (vectorized) | RUN |
| Siting optimization | conditional | CPU-hours | conditional | CONDITIONAL on Phase 7/5 signal |

WRF production budget estimate (for COMPUTE_BUDGET transparency): domain Europe ~25x25 km
inner/outer nests, 6 scenario x ~10 event days x spinup -> ~2-5k core-hours, ~50-200 GB
per scenario-day archived. Requires HPC; marked NOT RUN for this VM.
