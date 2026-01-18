import os
import pandas as pd
import numpy as np
import xarray as xr
import rioxarray
import geopandas as gpd
import regionmask
import rasterio.features
from collections import Counter
from shapely.geometry import Polygon
from tqdm import tqdm


def compute_catchment_aggregate(
    netcdf_path,
    catchment_geometry,
    function_type="mean"  # Can be 'mean', 'mode', 'std', 'percent' or dict
) -> pd.DataFrame:
    """
    Compute catchment-based features by aggregating raster variables in a NetCDF file
    for a single catchment geometry.

    Parameters
    ----------
    netcdf_path : str or Path
        Path to the NetCDF file containing raster variables.

    catchment_geometry : shapely.geometry.Polygon or GeoSeries
        Catchment geometry (single polygon).

    function_type : str or dict, default="mean"
        Either a string ('mean', 'mode', 'std', 'percent') to apply to all variables,
        or a dictionary specifying function(s) per variable. Example::

            {
                "precip": "mean",
                "slope": ["mean", "std"],
                "landcover": {"type": "percent"}
            }

    Returns
    -------
    pd.DataFrame
        A single-row DataFrame with catchment-level features.
    """

    # Open dataset
    ds = xr.open_dataset(netcdf_path, chunks={'x': 200, 'y': 200})
    ds = ds.rio.write_crs("EPSG:4326")

    # Rename coords if needed
    if 'lon' in ds.dims and 'lat' in ds.dims:
        ds = ds.rename({'lon': 'x', 'lat': 'y'})

    variables = list(ds.data_vars)

    # Build function dict
    if isinstance(function_type, str):
        apply_func = {var: function_type for var in variables}
    elif isinstance(function_type, dict):
        apply_func = function_type
    else:
        raise ValueError("function_type must be a string or a dictionary.")

    # Order check
    y_order = "descending" if ds.y[0] > ds.y[-1] else "ascending"
    x_order = "descending" if ds.x[0] > ds.x[-1] else "ascending"

    # Get catchment bounds
    minx, miny, maxx, maxy = catchment_geometry.bounds
    if y_order == "descending":
        y_slice = slice(maxy, miny)
    else:
        y_slice = slice(miny, maxy)
    if x_order == "descending":
        x_slice = slice(maxx, minx)
    else:
        x_slice = slice(minx, maxx)

    # Subset dataset
    subset_ds = ds.sel(x=x_slice, y=y_slice)

    # Create mask
    catchment_gdf = gpd.GeoDataFrame({"geometry": [catchment_geometry]}, crs="EPSG:4326")
    mask_from_geopandas = regionmask.mask_geopandas(catchment_gdf, subset_ds.x, subset_ds.y)
    catchment_mask = mask_from_geopandas == 0

    if mask_from_geopandas.notnull().sum().sum().item() == 0:
        raise ValueError("Catchment mask is empty — geometry may not overlap the raster.")

    results = {}

    # Loop over variables
    for var in apply_func.keys():
        data = subset_ds[var]
        masked = data.where(catchment_mask).compute()
        arr = masked.where(~masked.isnull(), drop=True)

        # Skip if empty
        if arr.size == 0:
            continue

        func_list = apply_func[var]
        if not isinstance(func_list, list):
            func_list = [func_list]  # wrap into list

        for func_info in func_list:
            if isinstance(func_info, str):
                func = func_info
                threshold = None
                threshold_direction = None
            elif isinstance(func_info, dict):
                func = func_info.get("type")
                threshold = func_info.get("threshold", None)
                threshold_direction = func_info.get("direction", "greater")
            else:
                raise ValueError(f"Invalid function format for variable {var}")

            if func == "mean":
                results[f"{var}_mean"] = float(arr.mean().item())

            elif func == "mode":
                vals = arr.values.flatten()
                results[f"{var}_mode"] = Counter(vals).most_common(1)[0][0]

            elif func == "std":
                results[f"{var}_std"] = float(arr.std().item())

            elif func == "percent":
                vals = arr.values.flatten()
                total = len(vals)
                class_counts = Counter(vals)
                for cls, count in class_counts.items():
                    results[f"{var}_percent_{int(cls)}"] = (count / total) * 100

            elif func == "threshold_percent":
                if threshold is None:
                    raise ValueError(f"Threshold not provided for variable '{var}'")
                vals = arr.values.flatten()
                valid = vals[~np.isnan(vals)]
                if threshold_direction == "greater":
                    percent = (valid > threshold).sum() / len(valid) * 100
                    results[f"{var}_percent_above_{threshold}"] = percent
                else:
                    percent = (valid < threshold).sum() / len(valid) * 100
                    results[f"{var}_percent_below_{threshold}"] = percent

            else:
                raise ValueError(f"Unknown function type '{func}' for variable '{var}'")

    return pd.DataFrame([results])

def compute_catchment_aggregate_multi_reservoir(
    netcdf_path,
    catchments_gdf: gpd.GeoDataFrame,
    function_type="mean",
    idx_col: str = "idx",
) -> pd.DataFrame:
    """
    Compute catchment-based aggregated features for MULTIPLE catchments
    from a single NetCDF file (opened only once).

    Parameters
    ----------
    netcdf_path : str or Path
        Path to the NetCDF file containing raster variables.

    catchments_gdf : geopandas.GeoDataFrame
        GeoDataFrame containing multiple catchment geometries.
        Must include:
            - geometry column
            - idx_col identifying each reservoir

    function_type : str or dict, default="mean"
        Aggregation rule(s), same semantics as compute_catchment_aggregate().

    idx_col : str, default="idx"
        Column identifying reservoir index.

    Returns
    -------
    pd.DataFrame
        DataFrame indexed by idx with aggregated features.
    """

    ds = xr.open_dataset(netcdf_path, chunks={"x": 200, "y": 200})
    ds = ds.rio.write_crs("EPSG:4326")

    if "lon" in ds.dims and "lat" in ds.dims:
        ds = ds.rename({"lon": "x", "lat": "y"})

    variables = list(ds.data_vars)

    if isinstance(function_type, str):
        apply_func = {v: function_type for v in variables}
    elif isinstance(function_type, dict):
        apply_func = function_type
    else:
        raise ValueError("function_type must be a string or a dictionary.")

    # Determine coordinate ordering for slicing
    y_order = "descending" if ds.y[0] > ds.y[-1] else "ascending"
    x_order = "descending" if ds.x[0] > ds.x[-1] else "ascending"

    results = []
    
    # ---- Loop over catchments (cheap loop now)
    for _, row_gdf in tqdm(
        catchments_gdf.iterrows(),
        total=catchments_gdf.shape[0],
        desc=f"Aggregating static features of catchments related to {os.path.basename(netcdf_path)}",
        unit="catchment",
    ):
        idx = row_gdf[idx_col]
        geom = row_gdf.geometry

        row = {idx_col: idx}

        if geom is None or geom.is_empty:
            results.append(row)
            continue

        # ---- Spatial subset FIRST
        minx, miny, maxx, maxy = geom.bounds
        
        dx = float(abs(ds.x[1] - ds.x[0]))
        dy = float(abs(ds.y[1] - ds.y[0]))
        minx -= dx
        maxx += dx
        miny -= dy
        maxy += dy
        
        if y_order == "descending":
            y_slice = slice(maxy, miny)
        else:
            y_slice = slice(miny, maxy)

        if x_order == "descending":
            x_slice = slice(maxx, minx)
        else:
            x_slice = slice(minx, maxx)

        subset_ds = ds.sel(x=x_slice, y=y_slice)
        
        # -- Skip if empty subset 
        if subset_ds.x.size == 0 or subset_ds.y.size == 0:
            print(f"Warning: Subset for catchment idx={idx} is empty. Skipping.")
            results.append(row)
            continue

        # ---- Create mask on SUBSET
        catchment_gdf = gpd.GeoDataFrame(
            {idx_col: [idx]}, geometry=[geom], crs="EPSG:4326"
        )

        # mask_from_geopandas = regionmask.mask_geopandas(
        #     catchment_gdf, subset_ds.x, subset_ds.y
        # )

        # catchment_mask = mask_from_geopandas == 0
        
        # # Skip if no overlap
        # if mask_from_geopandas.notnull().sum().sum().item() == 0:
        #     results.append(row)
        #     continue
        
        transform = subset_ds.rio.transform()

        mask = rasterio.features.rasterize(
            [(geom, 1)],
            out_shape=(subset_ds.sizes["y"], subset_ds.sizes["x"]),
            transform=transform,
            all_touched=True,
            fill=0,
            dtype="uint8",
        )
        
        # --- fallback if rasterized mask is empty ---
        if mask.sum() == 0:
            # Compute centroid in raster CRS
            centroid = geom.centroid
            # Find nearest x, y indices in the subset
            x_idx = np.argmin(np.abs(subset_ds.x.values - centroid.x))
            y_idx = np.argmin(np.abs(subset_ds.y.values - centroid.y))
            
            # Create a mask with just the centroid pixel
            mask = np.zeros((subset_ds.sizes["y"], subset_ds.sizes["x"]), dtype=np.uint8)
            mask[y_idx, x_idx] = 1

        catchment_mask = xr.DataArray(
            mask,
            coords={"y": subset_ds.y, "x": subset_ds.x},
            dims=("y", "x"),
        )


        # ---- Aggregate variables
        for var, func_list in apply_func.items():
            data = subset_ds[var]

            masked = data.where(catchment_mask).compute()
            arr = masked.where(~masked.isnull(), drop=True)

            if arr.size == 0:
                continue

            func_list = func_list if isinstance(func_list, list) else [func_list]

            for func_info in func_list:
                if isinstance(func_info, str):
                    func = func_info
                    threshold = None
                    threshold_direction = None
                elif isinstance(func_info, dict):
                    func = func_info.get("type")
                    threshold = func_info.get("threshold", None)
                    threshold_direction = func_info.get("direction", "greater")
                else:
                    raise ValueError(f"Invalid function format for variable {var}")

                if func == "mean":
                    row[f"{var}_mean"] = float(arr.mean().item())

                elif func == "mode":
                    vals = arr.values.flatten()
                    row[f"{var}_mode"] = Counter(vals).most_common(1)[0][0]

                elif func == "std":
                    row[f"{var}_std"] = float(arr.std().item())

                elif func == "percent":
                    vals = arr.values.flatten()
                    total = len(vals)
                    class_counts = Counter(vals)
                    for cls, count in class_counts.items():
                        row[f"{var}_percent_{int(cls)}"] = (count / total) * 100

                elif func == "threshold_percent":
                    if threshold is None:
                        raise ValueError(f"Threshold not provided for variable '{var}'")
                    vals = arr.values.flatten()
                    valid = vals[~np.isnan(vals)]
                    if threshold_direction == "greater":
                        percent = (valid > threshold).sum() / len(valid) * 100
                        row[f"{var}_percent_above_{threshold}"] = percent
                    else:
                        percent = (valid < threshold).sum() / len(valid) * 100
                        row[f"{var}_percent_below_{threshold}"] = percent

                else:
                    raise ValueError(f"Unknown function type '{func}' for variable '{var}'")

        results.append(row)

    return pd.DataFrame(results).set_index(idx_col)