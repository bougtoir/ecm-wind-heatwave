# DAG — Wind deployment → moisture → heatwave → electricity demand

Exposure X: cumulative upstream wind capacity / Wind-Flow Interception index WFI(x,t).
Mediators M: Δu(z) → ΔPBLH/TKE → ΔQ (vertically integrated moisture transport) → ΔMFC →
Δprecip/RH → Δsoil moisture → ΔLE/H partition.
Outcome Y1: ΔT2m/Tmax/Tmin, heatwave intensity/duration. Outcome Y2: Δ heat-related
electricity demand ΔE_heat. Composite: WERR = ΔE_heat/E_wind, E_net = E_wind − ΔE_heat.

Confounders (adjust, never adjust mediators):
- Synoptic circulation: blocking/ridging, advection, 500-hPa Z, SLP, NAO, seasonal circulation modes
- SST (Atlantic/Mediterranean/North Sea), land-use change, urban heat islands, aerosols
- Anthropogenic background warming (trend + climate indices)
- For Y2: secular demand trend, electrification, activity/holiday/weekday/hour, capacity growth

Design consequences:
- Estimate TOTAL effects of X on Y: do not condition on soil moisture/LE/H when estimating X→T.
- Analog matching on circulation fields (Phase 4) to isolate deployment differences under
  near-identical synoptic states.
- Event study / staggered DiD (Phase 5) on commissioning timing with spatial-HAC/block
  bootstrap inference; never iid SEs.
- Falsification (Phase 6): upwind controls, wrong-direction placebos, pre-construction
  placebos, shifted-farm placebos, inactive-season control, unrelated outcomes.
