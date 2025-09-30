Data Introduction
=================

Introduction
------------

Over 10 global temporal data products and 5 static specialized datasets were processed, resulting in **88 variables** that capture various dimensions of the reservoir sedimentation process. These variables span reservoir design attributes, catchment characteristics, hydrological conditions, and climatic drivers.

For clarity, the data are described here in two parts:

1. **Observed Sedimentation Rates**  
   These serve as the **target variable** (predictand) for training and evaluating RECLAIM.

2. **Predictor Variables**  
   Predictor variables are grouped into two categories:  
   
   - **Static Features**  
     Represent long-term physical and design attributes of reservoirs and their catchments.  
   
   - **Dynamic Features**  
     Represent temporal variability in hydrological and climatic conditions.

Feature Tracking and Referencing
--------------------------------

To facilitate tracking and referencing of the variables, each feature is assigned a **unique ID**:

- Predictors are labeled **“P”** (e.g., P1, P2)  
- Target variables are labeled **“T”**  
- Other features not used directly in the RECLAIM model are labeled **“D”**, as they have been used solely to derive other predictors.  

For example, **D3** refers to the end year of the observation; while not itself a predictor, it was used to calculate the dam’s age at the end of the observation period, which became predictor **P73**. Each feature also has a concise abbreviation for ease of readability and analysis, which is used in tables, figures, and text.

Global Datasets
---------------

The following **global datasets** are used to generate features for RECLAIM:

- `glc_shared_combined.nc` – Land cover data  
- `hwsd2_soil_d1.nc` – Soil data  
- `terrain.nc` – Terrain and DEM derivatives  
- `veg_gain_loss_1960_2019.nc` – Vegetation gain/loss from 1960–2019  

These datasets can be **downloaded from OSF**:  
`Download Global Datasets<https://doi.org/10.5281/zenodo.17230533>`_

Model Development Data
----------------------

The **model development data** includes:

- All 88 predictor features  
- Additional columns from GRILSS or derived features used to generate other predictors  

The data was divided into **80% training**, **10% validation**, and **10% test** sets for developing and evaluating RECLAIM.

Note
----

The global datasets above can also be used to generate features using the **pyreclaim** Python package:  
`https://pypi.org/project/pyreclaim/`
