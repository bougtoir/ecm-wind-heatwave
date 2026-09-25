import py_compile, pathlib, pandas as pd

def test_scripts_compile():
    for f in sorted(pathlib.Path("scripts").glob("*.py")):
        py_compile.compile(str(f), doraise=True)

def test_canonical_outputs_present():
    for f in ["werr_country_summary.csv","werr_event_level.csv",
              "demand_temperature_slopes.csv","phase3_panel_regression.csv"]:
        assert pathlib.Path("results", f).exists(), f

def test_pooled_werr_row():
    s = pd.read_csv("results/werr_pooled_summary.csv")
    assert s.iloc[0].country == "ALL" and 2000 <= s.iloc[0].n_events <= 4000
