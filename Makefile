PY = .venv/bin/python

.PHONY: all data analysis figures manuscript qc test

all: data analysis figures manuscript qc

data:
	$(PY) scripts/p1_acquire.py
	$(PY) scripts/p1_qc.py

analysis:
	$(PY) scripts/p2_moisture_transport.py
	$(PY) scripts/p2_heatwaves.py
	$(PY) scripts/p3_events.py
	$(PY) scripts/p4_analogs.py
	$(PY) scripts/p5_deployment.py
	$(PY) scripts/p6_falsification.py
	$(PY) scripts/p8_demand.py
	$(PY) scripts/p9_werr.py

figures:
	$(PY) scripts/make_figures.py

manuscript:
	$(PY) scripts/make_manuscript.py

qc:
	$(PY) scripts/qc_consistency.py

test:
	$(PY) -m pytest tests/ -q
