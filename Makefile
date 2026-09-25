PY = .venv/bin/python

.PHONY: all acquire analysis revision figures manuscript qc test smoke

all: acquire analysis revision figures manuscript qc

acquire:
	$(PY) scripts/dl_static_sources.py
	$(PY) scripts/dl_era5.py
	$(PY) scripts/dl_osm_pbf.py
	$(PY) scripts/extract_osm_wind.py
	$(PY) scripts/parse_mastr.py
	$(PY) scripts/build_turbines.py
	$(PY) scripts/p1_qc.py

analysis:
	$(PY) scripts/p2_moisture.py
	$(PY) scripts/p2_heatwaves.py
	$(PY) scripts/build_exposure.py
	$(PY) scripts/p3_events.py
	$(PY) scripts/p4_analogs.py
	$(PY) scripts/p5_deployment.py
	$(PY) scripts/p6_falsification.py
	$(PY) scripts/p8_demand.py
	$(PY) scripts/p9_werr.py

revision:
	$(PY) scripts/r1_demand.py
	$(PY) scripts/r1_werr.py primary
	$(PY) scripts/r1_werr.py m0
	$(PY) scripts/r2_exposure.py

figures:
	$(PY) scripts/make_figures.py
	$(PY) scripts/build_pptx.py

manuscript:
	$(PY) scripts/build_manuscript.py

qc:
	$(PY) scripts/p12_qc.py

smoke:
	$(PY) -m pytest tests/ -q

test: smoke
