import pandas as pd
import numpy as np

ALL_FEATURES = [
     'log_OBC', 'log_HGT', 'MRB', 'LAT', 'LON',
     'log_RA', 'log_RP', 'log_FL',
     'log_CA', 'log_DCA',
     
     'AECS', 'AECC','AECI',
     
     'log_LCAS', 'log_LCC',
     'log_LCG', 'log_LCT', 'log_LCS',
     'log_LCHV', 'log_LCM', 
     'log_LCSV','log_LCBS', 
     'log_LCSG', 'log_LCWB','DLC',
     
     'COAR', 'SAND', 'SILT', 'CLAY', 'BULK',
     
     'ELEV', 'SLOP', 'CURV', 'ASP', 'HILL',
     
     'log_MAI', 'log_PAI', 'I_cv',
     'log_I_std','I_above_90', 'I_max_persis',
     'log_MAO', 'log_O_std', 'O_cv',
     'E_mean', 'E_std',
     'log_SA_mean',  'log_SA_std', 'SA_cv', 'SA_skew', 'log_SA_kurt',
     'log_SA_mean_clip', 'SA_above_90',
     'NSSC1_mean', 'NSSC1_std', 'NSSC1_cv', 'NSSC1_skew', 'NSSC1_kurt', 
     'NSSC2_mean', 'NSSC2_above_90', 'NSSC2_max_persis',
     
     'log_MAR', '#_rain_above_10', '#_rain_above_50', '#_rain_above_100',
     'tmin_mean', 'tmax_mean',
     'wind_mean', 'wind_std', 'wind_cv', 'wind_skew', 'wind_kurt', 
     
     'AGE', 'log_ROBC', 'log_GC',
     'NVGF',
     'R_tree_bare', 'R_shrub_bare', 'R_coarse_sand',
     'log_rel_SA_mean_clip', 'log_R_SA_cap',
     'log_rain_per_area',
     'log_TE', 'log_RT', 'log_ECLR', 'ESR',
     'log_SIN', 'log_SOUT',
]

def engineer_and_transform_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer and transform features in reservoir/catchment dataset.

    Features are first engineered in raw space (linear), then log-transformations
    are applied in a single pass to avoid double-logging.

    Log-transformed columns are prefixed with ``log_`` to clearly indicate their state.

    Required input columns (abbreviations):
        - CA, DCA, OBC, HGT, RA, RP, FL
        - SA_mean, SA_mean_clip, SA_std, SA_kurt
        - PAI, MAI, MAO, I_std, O_std, MAR
        - OEY, BY, VGF, VLF
        - Land cover: LCAS, LCC, LCG, LCT, LCS, LCHV, LCM, LCSV, LCBS, LCSG, LCWB
        - COAR, SAND, NSSC2_mean
    """
    
    # Ensure required columns exist
    required_cols = ['CA', 'DCA', 'OBC', 'HGT', 'RA', 'RP', 'FL',
                     'SA_mean', 'SA_mean_clip', 'SA_std', 'SA_kurt',
                     'PAI', 'MAI', 'MAO', 'I_std', 'O_std', 'MAR',
                     'OEY', 'BY', 'VGF', 'VLF',
                     'LCAS','LCC','LCG','LCT','LCS','LCHV','LCM','LCSV','LCBS','LCSG','LCWB',
                     'COAR','SAND','NSSC2_mean']
    for col in required_cols:
        if col not in df.columns:
            df[col] = np.nan

    # -------------------------
    # ENGINEER RAW FEATURES
    # -------------------------
    inflow_cap_ratio = (df['MAI'] * 3600 * 24 * 365.25 / 1e6) / df['OBC']
    
    feature_dict = {
        "AGE": df["OEY"] - df["BY"],
        "ROBC": df["OBC"] / df["CA"],
        "NVGF": df["VGF"] - df["VLF"],
        "GC": df["RA"] / (df["RP"]**2),
        "rain_per_area": np.where(df["CA"]!=0, df["MAR"]/df["CA"], df["MAR"]),
        "R_tree_bare": np.where(df["LCBS"]!=0, df["LCT"]/df["LCBS"], df["LCT"]),
        "R_shrub_bare": np.where(df["LCBS"]!=0, df["LCS"]/df["LCBS"], df["LCS"]),
        "R_coarse_sand": df["COAR"]/df["SAND"],
        "RT": df["OBC"] * 1e6 / (df["MAI"] * 3600 * 24 * 365.25),
        "TE": np.exp(-0.0079 * inflow_cap_ratio) * 100,
        "ECLR": np.exp(-0.0079 * inflow_cap_ratio) * 100 * df["NSSC2_mean"] * inflow_cap_ratio,
        "ESR": np.exp(-0.0079 * inflow_cap_ratio) * 100 * df["NSSC2_mean"] * inflow_cap_ratio * df["OBC"] / 100,
        "rel_SA_mean_clip": df["SA_mean_clip"] / df["RA"],
        "R_SA_cap": df["SA_mean_clip"] / df["OBC"],
        "SIN": df["MAI"] * df["NSSC2_mean"],
        "SOUT": df["MAO"] * df["NSSC2_mean"],
    }
    
    df = pd.concat([df, pd.DataFrame(feature_dict)], axis=1)

    # Land cover log-area features
    lc_cols = ['LCAS','LCC','LCG','LCT','LCS','LCHV','LCM','LCSV','LCBS','LCSG','LCWB']
    # for col in lc_cols:
    #     df[col] = df["CA"] * df[col] / 100
    # Doing calculation along with taking log as done in model training. results will slightly differ for cases where percentage of LC is 0.
        
    # -------------------------
    # APPLY LOG TRANSFORMATIONS
    # -------------------------
    log_candidates = ['CA','DCA','OBC','HGT','RA','RP','FL',
                      'SA_mean','SA_mean_clip','SA_std','SA_kurt','PAI','MAI','MAO','I_std','O_std','MAR',
                      'ROBC','rain_per_area','GC','TE','RT','ECLR','SIN','SOUT', 'rel_SA_mean_clip', 'R_SA_cap'] + lc_cols

    for col in log_candidates:
        log_col = f'log_{col}'  # add prefix to avoid double log
        try:
            if col in ['ECLR','SIN','SOUT']:
                # Land cover columns can be zero (upto 15 decimal places), clip at 1e-15
                df[log_col] = np.log(df[col].clip(lower=1e-15))
            elif col in ['rain_per_area']:
                # Rain per area can be zero (upto 10 decimal places), clip at 1e-10
                df[log_col] = np.log(df[col].clip(lower=1e-10))
            elif col in lc_cols:
                df[log_col] = np.log(df["CA"].clip(lower=1e-6)) + np.log(df[col].clip(lower=1e-6)) - np.log(100)
            else:
                # All other columns can be zero (upto 6 decimal places), clip at 1e-6
                df[log_col] = np.log(df[col].clip(lower=1e-6))
        except Exception as e:
            raise ValueError(f"Error applying log transform to column '{col}': {e}")
    
    # Process DLc as categorical column
    df['DLC'] = df['DLC'].astype(int).fillna(0)
    
    # Add empty columns for any missing features
    for feature in ALL_FEATURES:
        if feature not in df.columns:
            df[feature] = np.nan
    
    return df