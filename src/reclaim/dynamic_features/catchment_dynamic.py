import pandas as pd
import numpy as np
from typing import Dict, Sequence, List

from reclaim.dynamic_features.utils.rainfall import (
    mean_annual_rainfall_mm,
    mean_annual_rainy_days,
)
from reclaim.dynamic_features.utils.statistical_metrics import (
    annual_mean,
    annual_std,
    coefficient_of_variation,
    skewness,
    kurtosis_val,
)
from reclaim.dynamic_features.utils.ts_aggregate import compute_ts_aggregates

VARIABLE_FEATURES = {
        "precip": {
            "MAR": mean_annual_rainfall_mm,
            "#_rain_above_10": lambda ts: mean_annual_rainy_days(ts, threshold=10.0),
            "#_rain_above_50": lambda ts: mean_annual_rainy_days(ts, threshold=50.0),
            "#_rain_above_100": lambda ts: mean_annual_rainy_days(ts, threshold=100.0),
        },
        "tmin": {
            "tmin_mean": annual_mean,
        },
        "tmax": {
            "tmax_mean": annual_mean,
        },
        "wind": {
            "wind_mean": annual_mean,
            "wind_std": annual_std,
            "wind_cv": coefficient_of_variation,
            "wind_skew": skewness,
            "wind_kurt": kurtosis_val,
        },
    }


def catchment_based_dynamic_features(
    variable_info: Dict[str, Dict[str, str]],
    observation_intervals: List[Sequence[int]],
) -> pd.DataFrame:
    """
    Compute dynamic catchment-based features for a single reservoir's catchment,
    using precipitation, temperature, and wind speed time series.

    Required time series keys (case-sensitive)
        - "precip":  Daily precipitation in mm
        - "tmin":    Daily minimum temperature in °C
        - "tmax":    Daily maximum temperature in °C
        - "wind":    Daily wind speed in m/s

    Parameters
    ----------
    variable_info : dict
        Dictionary of input series metadata.
        Each key corresponds to a variable (precip, tmin, tmax, wind).
        Each value is a dict with:
            {
                "path": str,
                "time_column": str,
                "data_column": str
            }
            
    observation_intervals : list of list of int
        List of [start_year, end_year] intervals to compute features over.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing as many rows as there are observation intervals and columns corresponding to the computed catchment-based features.
        Missing variables in ``variable_info`` will result in NaN values for their features.
    Notes
    -----
    - Precipitation features are reported as mm/year (for MAR) and counts (rainy days).
    - Wind statistics include mean, std, CV, skewness, kurtosis.
    - Temperature features are simple annual means (°C).
    """

    all_vars = []

    for var, feat_dict in VARIABLE_FEATURES.items():
        if var not in variable_info:
            all_vars.append(
                pd.DataFrame(np.nan, index=range(len(observation_intervals)),
                             columns=feat_dict.keys())
            )
            continue

        path = variable_info[var]["path"]
        time_col = variable_info[var]["time_column"]
        data_col = variable_info[var]["data_column"]
        
        try:
            df_var = compute_ts_aggregates(
                ts_csv_path=path,
                time_column=time_col,
                value_column=data_col,
                feature_functions=feat_dict,
                intervals=observation_intervals,
            )
            all_vars.append(df_var)
        except Exception:
            df_var = pd.DataFrame()
            all_vars.append(df_var)

    return pd.concat(all_vars, axis=1)