import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import numpy as np

# Import utils
from reclaim.static_features.utils.flow_length import find_actual_flow_path, plot_flow_length_with_reservoir
from reclaim.static_features.utils.area_perimeter import calculate_length_area_meters
from reclaim.static_features.utils.aec_shape import concavity_index, mean_curvature, mean_slope


def reservoir_based_static_features(
    obc: float = None,
    hgt: float = None,
    mrb: str = None,
    lat: float = None,
    lon: float = None,
    by: int = None,
    reservoir_polygon: Polygon = None,
    inlet_point: Point = None,
    resolution: float = None,
    aec_df: pd.DataFrame = None,
    savepath_flowpath_fig: str = None,
) -> pd.DataFrame:
    """
    Compute reservoir-based features for RECLAIM input dataset.
    
    Parameters
    ----------
    obc : float, optional
        Original Built Capacity (MCM), original design capacity of the reservoir.
    hgt : float, optional
        Dam height (meters).
    mrb : str, optional
        Major river basin name.
    lat : float, optional
        Latitude of dam location (degrees).
    lon : float, optional
        Longitude of dam location (degrees).
    by : int, optional
        Build year of the reservoir.
    reservoir_polygon : shapely.geometry.Polygon, optional
        Reservoir polygon geometry used to compute area and perimeter.
    dam_point : shapely.geometry.Point, optional
        Location of the dam.
    inlet_point : shapely.geometry.Point, optional
        Reservoir inlet location (if not provided, estimated internally).
    resolution : float, optional
        Spatial resolution used in flow length calculations.
    aec_df : pd.DataFrame, optional
        Area-Elevation Curve dataframe with columns ['area', 'elevation'].
    savepath_flowpath_fig : str, optional
        Path to save the flow path figure, optional.
    
    Returns
    -------
    pd.DataFrame
        A single-row DataFrame with the following columns:
        - OBC: Original Built Capacity (MCM)
        - HGT: Dam Height (m)
        - MRB: Major River Basin
        - LAT: Latitude (deg)
        - LON: Longitude (deg)
        - BY: Build Year
        - RA: Reservoir Area (sq km)
        - RP: Reservoir Perimeter (km)
        - FL: Flow Length (km)
        - AECS: AEC Mean Slope (km2/m)
        - AECC: AEC Mean Curvature (km2/m2)
        - AECI: AEC Concavity Index (DL)
    """

    features = {
        "OBC": obc,
        "HGT": hgt,
        "MRB": mrb,
        "LAT": lat,
        "LON": lon,
        "BY": by,
        "RA": None,
        "RP": None,
        "FL": None,
        "AECS": None,
        "AECC": None,
        "AECI": None,
    }

    # Area and Perimeter
    if reservoir_polygon is not None and not reservoir_polygon.is_empty:
        features["RP"], features["RA"] = calculate_length_area_meters(reservoir_polygon, area=True)
        features["RA"] = features["RA"] / 1e6  # m2 → km2
        features["RP"] = features["RP"] / 1e3  # m → km
    else:
        features["RP"] = np.nan
        features["RA"] = np.nan

    # Flow Length
    dam_point = Point(lon, lat)
    if dam_point is not None and reservoir_polygon is not None and not reservoir_polygon.is_empty:
        try:
            simplified_reservoir, far_end_point, flow_path, _ = (
                find_actual_flow_path(dam_point, reservoir_polygon, inlet_point, resolution) 
            )
            if savepath_flowpath_fig is not None:
                plot_flow_length_with_reservoir(
                    dam_point,
                    reservoir_polygon,
                    far_end_point,
                    flow_path,
                    simplified_reservoir,
                    savepath_flowpath_fig
                )  
            if flow_path is not None: 
                gseries = gpd.GeoSeries([flow_path], crs="EPSG:4326")
                gseries = gseries.to_crs(epsg=3395)

                features["FL"] = gseries.length.iloc[0] / 1e3 # m → km  
            else:
                features["FL"] = np.nan
        except Exception as e:
            print(f"Flow length calculation failed: {e}")
            features["FL"] = np.nan
    else:
        features["FL"] = np.nan
    
    # AEC metrics
    if isinstance(aec_df, pd.DataFrame) and not aec_df.empty:
        features["AECS"] = mean_slope(aec_df)
        features["AECC"] = mean_curvature(aec_df)
        features["AECI"] = concavity_index(aec_df)
    else:
        features["AECS"] = np.nan
        features["AECC"] = np.nan
        features["AECI"] = np.nan

    return pd.DataFrame([features])