User Guide
===========

This guide provides step-by-step instructions to generate features for reservoirs and catchments, load pretrained RECLAIM models, and predict sedimentation rates (SR) using the ensemble model or individual base models.

Contents
--------
- Overview
- 1. Generating Features  
  - 1.1 Single Reservoir  
  - 1.2 Multiple Reservoirs  
- 2. Loading Pretrained RECLAIM Model  
- 3. Making Predictions  
  - 3.1 Predicting with Ensemble  
  - 3.2 Using Base Models  
- 4. Evaluating Predictions  
- 5. Saving and Loading Custom Trained Models  
- 6. Example Workflow  

Overview
--------
The RECLAIM package provides a stacked ensemble predictor for reservoir sedimentation rate (SR) by combining XGBoost, LightGBM, and CatBoost base models with a meta-model. It also includes utilities to generate features from static and dynamic reservoir and catchment data.

1. Generating Features
---------------------

1.1 Single Reservoir
````````````````````

To compute features for a single reservoir observation, use the `create_features_per_row` function in `generate_features.py`.

**Parameters**

- `reservoir_static_params`: dict  
  Required keys for reservoir static features:

  - `obc` : Original Built Capacity (MCM)  
  - `hgt` : Dam Height (m)  
  - `mrb` : Major River Basin  (optional)
  - `lat`, `lon` : Latitude & Longitude (degrees)  
  - `reservoir_polygon` : shapely Polygon  
  - `inlet_point` : shapely Point (optional)  
  - `resolution` : float (optional)  
  - `aec_df` : pd.DataFrame with `['area','elevation']`  

- `catchment_static_params`: dict  
  Required keys for catchment static features:

  - `ca` : Catchment Area (sq km)  
  - `dca` : Differential Catchment Area (sq km)  
  - `catchment_geometry` : shapely Polygon or GeoSeries  
  - `glc_share_path` : path to GLC-Share NetCDF (land cover)  
  - `hwsd2_path` : path to HWSD2 NetCDF (soils)  
  - `hilda_veg_freq_path` : path to HILDA vegetation NetCDF  
  - `terrain_path` : path to terrain/DEM derivatives NetCDF  

- `reservoir_dynamic_info` : dict (optional)  
  Must contain paths and column names for:

  - `inflow`, `outflow`, `evaporation`, `surface_area`, `nssc`, `nssc2`  

- `catchment_dynamic_info` : dict (optional)  
  Must contain paths and column names for:

  - `precip`, `tmin`, `tmax`, `wind`  

- `observation_period` : list `[OSY, OEY]` (optional)  
  Observation start and end year.

**Example**

.. code-block:: python
    from reclaim.generate_features import create_features_per_row

    reservoir_static = {
        "obc": 150.0,
        "hgt": 45.0,
        "mrb": "Ganges",
        "lat": 25.6,
        "lon": 81.9,
        "reservoir_polygon": reservoir_polygon,
        "aec_df": aec_df
    }

    catchment_static = {
        "ca": 1200,
        "dca": 50,
        "catchment_geometry": catchment_geom,
        "glc_share_path": "data/glc.nc",
        "hwsd2_path": "data/soil.nc",
        "hilda_veg_freq_path": "data/veg.nc",
        "terrain_path": "data/terrain.nc"
    }

    features = create_features_per_row(
        reservoir_static_params=reservoir_static,
        catchment_static_params=catchment_static,
        observation_period=[2000, 2020]
    )

1.2 Multiple Reservoirs
`````````````````````````

For batch processing, use `create_features_multi` with a list of reservoir dictionaries.

**Example**

.. code-block:: python

    from reclaim.generate_features import create_features_multi

    reservoirs_input = [
        {
            "reservoir_static_params": reservoir_static,
            "catchment_static_params": catchment_static,
            "observation_period": [2000, 2020]
        },
        {
            "reservoir_static_params": reservoir_static2,
            "catchment_static_params": catchment_static2,
            "observation_period": [2005, 2020]
        }
    ]

    features_df = create_features_multi(reservoirs_input)

This returns a combined DataFrame with one row per reservoir.

2. Loading Pretrained RECLAIM Model
-----------------------------------

The package includes a pretrained ensemble model stored in `pretrained_model` folder.

**Example**

.. code-block:: python

    from reclaim.reclaim import Reclaim

    model = Reclaim()
    model.load_model()  # Loads pretrained model from package folder

By default, this loads the XGBoost, LightGBM, CatBoost models and metadata (feature order, cat features).

3. Making Predictions
---------------------

3.1 Predicting with Ensemble
`````````````````````````

The ensemble prediction uses dynamic, instance-wise weights based on CatBoost output.

**Example**

.. code-block:: python

    predictions, weights = model.predict(features_df, return_weights=True)

**Parameters**

- `log_transform` (bool, default=True) – Apply log1p to stabilize high values  
- `dynamic_weight` (bool, default=True) – Use instance-wise weights  
- `threshold` (float, default=30) – Threshold separating low/high predictions  
- `sat_point` (float, default=70) – Saturation point for above-threshold weights  
- `smooth_factor` (float, default=0.2) – Controls sigmoid sharpness  

`weights` is a DataFrame showing the contribution of XGBoost, LightGBM, and CatBoost for each observation.

Or you can predict using simple average of individual base models:

.. code-block:: python

    average_pred = model.predict(features_df, log_transform=False, dynamic_weight=False)

3.2 Using Base Models
`````````````````````````

You can also predict explicitly using one of the base models:

.. code-block:: python

    model.main_model = "XGBoost"
    pred_xgb = model.predict(features_df)

4. Evaluating Predictions
-------------------------

Evaluate model performance on true SR values:

.. code-block:: python

    y_true = [...]  # true sedimentation rates
    metrics = model.evaluate(features_df, y_true)
    print(metrics)  # {'RMSE': ..., 'MAE': ..., 'R2': ...}

5. Saving and Loading Custom Trained Models
-------------------------------------------

Save models after custom training:

.. code-block:: python

    model.save_model(save_dir="custom_models", prefix="my_run")

Load previously saved models:

.. code-block:: python

    model.load_model(load_dir="custom_models", prefix="my_run")

6. Example Workflow
-------------------

Complete example from feature generation to prediction and evaluation:

.. code-block:: python

    from reclaim.generate_features import create_features_per_row
    from reclaim.reclaim import Reclaim

    # Step 1: Generate features
    features = create_features_per_row(
        reservoir_static_params=reservoir_static,
        catchment_static_params=catchment_static,
        observation_period=[2000, 2020]
    )

    # Step 2: Load pretrained model
    model = Reclaim()
    model.load_model()

    # Step 3: Predict sedimentation rates
    pred_sr, weights = model.predict(features, return_weights=True)

    # Step 4: Inspect predictions
    print(pred_sr)
    print(weights)

    # Step 5: Evaluate (if ground truth available)
    metrics = model.evaluate(features, y_true)
    print(metrics)