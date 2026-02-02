import pandas as pd
import numpy as np
from pathlib import Path
from typing import Callable, Union, Sequence, List, Dict

FULL_RECORD_FEATURES = ["SA_mean", "SA_std", "SA_cv", "SA_skew", "SA_kurt", "NSSC2_max_persis"]

def build_intervals(start_year, end_year, time_interval):
    total_years = end_year - start_year + 1

    # Case 1: Entire window shorter than interval
    if total_years <= time_interval:
        return [[start_year, end_year]]

    remainder = total_years % time_interval
    outputs = []

    # First interval absorbs remainder (if any)
    first_len = time_interval + remainder if remainder != 0 else time_interval
    first_end = min(start_year + first_len - 1, end_year)
    outputs.append([start_year, first_end])

    # Remaining intervals
    current_start = first_end + 1
    while current_start <= end_year:
        current_end = current_start + time_interval - 1
        outputs.append([current_start, min(current_end, end_year)])
        current_start = current_end + 1

    return outputs

def compute_ts_aggregates(
    ts_csv_path: str,
    time_column: str,
    value_column: str,
    feature_functions: Dict[str, Callable],
    intervals: List[Sequence[int]],
) -> pd.DataFrame:
    """
    Compute an aggregate feature from a user-provided time series CSV for a single reservoir.

    Parameters
    ----------
    ts_csv_path : str
        Path to the CSV file containing the time series.
    time_column : str
        Name of the column representing dates/timestamps.
    value_column : str
        Name of the column representing the variable values.
    feature_functions : Dict[str, Callable]
        Dictionary where keys are feature names (column names for output DataFrame) and values are functions that take a pd.Series and return a single value.
    intervals : list of list of int
        List of [start_year, end_year] intervals to compute features over.

    Returns
    -------
    pd.DataFrame
        A single-row DataFrame containing the computed feature with the specified column name.
    """
    # --- Read CSV ONCE ---
    # Check if path exists 
    if not Path(ts_csv_path).is_file():
        raise FileNotFoundError(f"CSV file not found at path: {ts_csv_path}")
        
    df = pd.read_csv(ts_csv_path)
    if df.empty:
        raise ValueError(f"CSV at {ts_csv_path} is empty.")
    
    # Ensure columns exist
    if time_column not in df.columns:
        raise ValueError(f"Time column '{time_column}' not found in CSV.")
    if value_column not in df.columns:
        raise ValueError(f"Value column '{value_column}' not found in CSV.")

    # Ensure time column is datetime
    df[time_column] = pd.to_datetime(df[time_column], errors='coerce')
    if df[time_column].isna().all():
        raise ValueError(f"Time column '{time_column}' could not be converted to datetime.")

    # Set index 
    ts = df.set_index(time_column)[value_column].sort_index()
    
    if ts.empty:
        raise ValueError("Time series is completely empty. Please check the data or avoid providing this variable.")

    rows = []

    for osy, oey in intervals:
        ts_clip = ts[(ts.index.year >= osy) & (ts.index.year <= oey)]
        ts_till_end_year = ts[ts.index.year <= oey]

        row = {}
        for feat, func in feature_functions.items():
            try:
                if feat in FULL_RECORD_FEATURES:
                    row[feat] = func(ts_till_end_year) if not ts_till_end_year.empty else np.nan
                else:
                    row[feat] = func(ts_clip) if not ts_clip.empty else np.nan
            except Exception:
                row[feat] = np.nan

        rows.append(row)

    return pd.DataFrame(rows)