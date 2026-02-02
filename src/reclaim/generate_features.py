### Wrappers to compute all static, dynamic, and derived features for RECLAIM input dataset.

from typing import Dict, List
import pandas as pd
import geopandas as gpd
from tqdm import tqdm
import traceback
from dask import delayed, compute
from dask.diagnostics import ProgressBar

# Import from your package structure
from reclaim.static_features.reservoir_static import reservoir_based_static_features
from reclaim.static_features.catchment_static import catchment_based_static_features, catchment_based_static_features_multi_reservoir
from reclaim.dynamic_features.reservoir_dynamic import reservoir_based_dynamic_features
from reclaim.dynamic_features.catchment_dynamic import catchment_based_dynamic_features
from reclaim.dynamic_features.utils.ts_aggregate import build_intervals
from reclaim.derived_features.feature_engineering_and_transformation import engineer_and_transform_features


def create_features_per_reservoir(
    idx: int,
    observation_period: List[int],
    reservoir_static_params: dict,
    catchment_static_params: dict = None,
    reservoir_dynamic_info: dict = None,
    catchment_dynamic_info: dict = None,
    time_interval: int = None,
    feature_engineering: bool = True,
) -> pd.DataFrame:
    """
    Compute all static, dynamic, and derived features for a single reservoir observation.

    Parameters
    ----------
    idx : int
        Index of the reservoir sedimentation observation (for tracking/logging purposes).
    
    observation_period : list of int
        Two-element list [OSY, OEY] for observation start year and end year.
        
    reservoir_static_params : dict
        Parameters for reservoir_based_static_features(). Expected keys:
            - obc : float, Original Built Capacity (MCM)
            - hgt : float, Dam Height (m)
            - mrb : int, Major River Basin, optional
            - lat : float, Latitude (deg)
            - lon : float, Longitude (deg)
            - by : int, Build Year
            - reservoir_polygon : shapely.geometry.Polygon
            - inlet_point : shapely.geometry.Point, optional
            - resolution : float, optional
            - aec_df : pd.DataFrame with columns ['area', 'elevation']

    catchment_static_params : dict, optional
        Parameters for catchment_based_static_features(). Expected keys:
            - ca : float, Catchment Area (sq km)
            - dca : float, Differential Catchment Area (sq km)
            - catchment_geometry : shapely.geometry.Polygon or GeoSeries
            - glc_share_path : str, path to GLC-Share NetCDF (land cover)
            - hwsd2_path : str, path to HWSD2 NetCDF (soils)
            - hilda_veg_freq_path : str, path to HILDA vegetation NetCDF
            - terrain_path : str, path to terrain/DEM derivatives NetCDF

    reservoir_dynamic_info : dict, optional
        variable_info dict for reservoir time series. Required keys (case-sensitive):
            - "inflow":       {"path": str, "time_column": str, "data_column": str}
            - "outflow":      {"path": str, "time_column": str, "data_column": str}
            - "evaporation":  {"path": str, "time_column": str, "data_column": str}
            - "surface_area": {"path": str, "time_column": str, "data_column": str}
            - "nssc":         {"path": str, "time_column": str, "data_column": str}
            - "nssc2":        {"path": str, "time_column": str, "data_column": str}

    catchment_dynamic_info : dict, optional
        variable_info dict for catchment time series. Required keys (case-sensitive):
            - "precip": {"path": str, "time_column": str, "data_column": str}
            - "tmin":   {"path": str, "time_column": str, "data_column": str}
            - "tmax":   {"path": str, "time_column": str, "data_column": str}
            - "wind":   {"path": str, "time_column": str, "data_column": str}

    time_interval: int, optional
        Time interval in years between reservoir observations for dynamic feature calculations. The number of rows in the dynamic features will depend on this interval.
    
    Returns
    -------
    pd.DataFrame
        Single-row DataFrame with all features:
        - Reservoir static
        - Catchment static
        - Reservoir dynamic
        - Catchment dynamic
        - Derived/log-transformed (if requested)
    """
    
    # --- Observevation period features ---
    osy, oey = observation_period
    if time_interval is not None:
        intervals = build_intervals(osy, oey, time_interval)
    else:
        intervals = [(osy, oey)]
    # Create observation period dataframe with rows for each interval with same idx
    df_obs = pd.DataFrame({
    "idx": idx,
    "OSY": [i[0] for i in intervals],
    "OEY": [i[1] for i in intervals],
    })

    # --- Static features (computed ONCE) ---
    df_res_static = reservoir_based_static_features(**reservoir_static_params)
    if catchment_static_params is not None:
        df_catch_static = catchment_based_static_features(**catchment_static_params)
    else:
        df_catch_static = pd.DataFrame()
    
    static_block = pd.concat([df_res_static, df_catch_static], axis=1)
    # Repeat static rows to match number of intervals
    static_block = pd.concat(
        [static_block] * len(df_obs),
        ignore_index=True
    )

    # --- Dynamic features (computed ONCE - internally handles intervals) ---
    # Combine dynamic features for all intervals
    df_res_dyn = (
        reservoir_based_dynamic_features(
            reservoir_dynamic_info,
            intervals,
        )
        if reservoir_dynamic_info is not None
        else pd.DataFrame()
    )

    df_catch_dyn = (
        catchment_based_dynamic_features(
            catchment_dynamic_info,
            intervals,
        )
        if catchment_dynamic_info is not None
        else pd.DataFrame()
    )
    
    # --- Combine all features for all intervals in single dataframe ---
    df_out = pd.concat(
        [df_obs, static_block, df_res_dyn, df_catch_dyn],
        axis=1
    ).reset_index(drop=True)

    # --- Engineer ONLY if requested ---
    if feature_engineering:
        df_out = engineer_and_transform_features(df_out)

    return df_out

@delayed
def process_one_reservoir(r):
    try:
        df = create_features_per_reservoir(
            idx=r["idx"],
            observation_period=r["observation_period"],
            reservoir_static_params=r["reservoir_static_params"],
            catchment_static_params=None,
            reservoir_dynamic_info=r.get("reservoir_dynamic_info"),
            catchment_dynamic_info=r.get("catchment_dynamic_info"),
            time_interval=r.get("time_interval"),
            feature_engineering=False,
        )
        return r["idx"], df, None
    except Exception as e:
        return r["idx"], pd.DataFrame({"idx": [r["idx"]]}), {str(e):traceback.format_exc()}

def create_features_multi_reservoirs(
    reservoirs_input: List[Dict],
    error_log: bool = False,
) -> pd.DataFrame:
    """
    Compute features for multiple reservoirs using structured input.

    Parameters
    ----------
    reservoirs_input : list of dict
        Each element should be a dictionary with the following keys:
        
        - `idx` : int
            Index of the reservoir sedimentation observation.
        - `observation_period` : list of int
            Two-element list `[OSY, OEY]` specifying the observation period.
        - `reservoir_static_params` : dict
            Parameters for `reservoir_based_static_features()`.
        - `catchment_static_params` : dict
            Parameters for `catchment_based_static_features()`.
        - `reservoir_dynamic_info` : dict
            Parameters for `reservoir_based_dynamic_features()`.
        - `catchment_dynamic_info` : dict
            Parameters for `catchment_based_dynamic_features()`.
        - `time_interval` : int, optional
            Time interval in years between reservoir observations for dynamic feature calculations.

    Returns
    -------
    pd.DataFrame
        Combined DataFrame with one row per reservoir and time intervals
        in the observation period.
    """

    # -------- Collect catchments first (cheap, no tqdm needed)
    catchment_rows = []

    for r in reservoirs_input:
        c = r["catchment_static_params"]
        catchment_rows.append({
            "idx": r["idx"],
            "CA": c["ca"],
            "DCA": c["dca"],
            "geometry": c["catchment_geometry"],
        })

    catchments_gdf = gpd.GeoDataFrame(
        catchment_rows, geometry="geometry", crs="EPSG:4326"
    )

    # -------- Compute catchment static ONCE
    first = reservoirs_input[0]["catchment_static_params"]

    df_catch_static_all = catchment_based_static_features_multi_reservoir(
        catchments_gdf,
        glc_share_path=first["glc_share_path"],
        hwsd2_path=first["hwsd2_path"],
        hilda_veg_freq_path=first["hilda_veg_freq_path"],
        terrain_path=first["terrain_path"],
    )
    
    catch_static_lookup = df_catch_static_all.set_index("idx")
    # catch_static_lookup = pd.DataFrame()  # Placeholder if not computing

    # -------- Per-reservoir loop (tqdm HERE)
    tasks = [process_one_reservoir(r) for r in reservoirs_input]
    with ProgressBar():
        results = compute(*tasks, scheduler="processes", num_workers=4)
    
    all_reservoirs_static_info = []
    errors = {}
    
    for idx, df, err in results:
        all_reservoirs_static_info.append(df)
        if err is not None:
            errors[idx] = err

    # for r in tqdm(
    #     reservoirs_input,
    #     total=len(reservoirs_input),
    #     desc="Generating per-reservoir features",
    #     unit="reservoir",
    # ):
    #     try:
    #         df = create_features_per_reservoir(
    #             idx=r["idx"],
    #             observation_period=r["observation_period"],
    #             reservoir_static_params=r["reservoir_static_params"],
    #             catchment_static_params=None,  # already handled
    #             reservoir_dynamic_info=r.get("reservoir_dynamic_info"),
    #             catchment_dynamic_info=r.get("catchment_dynamic_info"),
    #             time_interval=r.get("time_interval"),
    #             feature_engineering=False,
    #         )
    #         all_reservoirs_static_info.append(df)
    #     except Exception as e:
    #         errors[r["idx"]] = e
    #         errors['traceback'] = traceback.print_exc()
    #         all_reservoirs_static_info.append(
    #             pd.DataFrame({"idx": r["idx"]})  # Append empty DataFrame for failed reservoir
    #         )
            
            

    # -------- Concatenate static info
    df_all = pd.concat(all_reservoirs_static_info, ignore_index=True)
    # CRITICAL: restore logical ordering
    df_all = df_all.sort_values(
        by=["idx", "OSY"],   #
        ascending=[True, True],
    ).reset_index(drop=True)
    
    
    # -------- Merge static catchment features with dynamic ONCE
    df_all = df_all.merge(
        catch_static_lookup,
        left_on="idx",
        right_index=True,
        how="left",
    )

    # -------- Engineer ONCE
    df_all = engineer_and_transform_features(df_all)
    
    if error_log:
        return df_all, errors
    else:
        return df_all