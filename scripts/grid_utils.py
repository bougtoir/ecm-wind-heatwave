"""Grid normalization: ERA5 files have dim order (time, longitude, latitude)
and 0-360 longitudes. Canonical form: (time, latitude, longitude) with
longitudes in [-180, 180), sorted ascending."""
import pathlib
import numpy as np
import xarray as xr

ERA = pathlib.Path("data/raw/era5")

def canon(da):
    if "longitude" in da.dims and "latitude" in da.dims and "time" in da.dims:
        da = da.transpose("time", "latitude", "longitude")
    lon = ((da.longitude.values + 180.0) % 360.0) - 180.0
    da = da.assign_coords(longitude=lon).sortby("longitude")
    return da

def open_surf():
    return xr.open_mfdataset(sorted(ERA.glob("surf_daily_*.nc")), combine="by_coords")

def open_qflux():
    return xr.open_mfdataset(sorted(ERA.glob("qflux_daily_*.nc")), combine="by_coords")

def open_hydro():
    return xr.open_mfdataset(sorted(ERA.glob("hydro_daily_*.nc")), combine="by_coords")
