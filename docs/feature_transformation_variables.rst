Feature Transformation 
=======================

Feature transformation was carried out to ensure that variables were more informative and suitable for model training.  
Categorical variables such as **major river basin (MRB)** and **dominant land cover (DLC)** were encoded with unique integer values to represent each class.  
For MRB, the HydroSHEDS-provided **HYBASID** was used as the unique identifier (Lehner et al., 2008).

Several continuous variables exhibited high skewness, particularly those related to spatial dimensions (e.g., capacity, area, and length).  
To address this, a **natural log transformation** was applied. The effect of this transformation is illustrated in Figure 4, where skewness reduction is shown for **original built capacity (OBC)** and **catchment area (CA)**.  
The original abbreviations and variable names were retained after transformation to ensure consistency across tables and figures.

Additionally, negative values of **sedimentation rate (SR)**—which can arise from sediment management interventions or short observation periods (Minocha and Hossain, 2025a)—were replaced with small nonzero values  
(0 MCM/year). This adjustment ensures that the models do not attempt to learn physically implausible negative values, while still preserving the integrity of the dataset.

Log-Transformed Features
-------------------------

The following variables were transformed using the natural logarithm.  
Original feature numbers and abbreviations have been retained for consistency.

.. list-table::
   :header-rows: 1
   :widths: 8 40 20

   * - No.
     - Name
     - Abbreviation
   * - P1
     - Original Built Capacity
     - log_OBC
   * - P2
     - Dam Height
     - log_HGT
   * - P6
     - Reservoir Area
     - log_RA
   * - P7
     - Reservoir Perimeter
     - log_RP
   * - P8
     - Flow Length
     - log_FL
   * - P9
     - Catchment Area
     - log_CA
   * - P10
     - Differential Catchment Area
     - log_DCA
   * - P14
     - Land cover of artificial surfaces
     - log_LCAS
   * - P15
     - Land cover of cropland
     - log_LCC
   * - P16
     - Land cover of grassland
     - log_LCG
   * - P17
     - Land cover of trees
     - log_LCT
   * - P18
     - Land cover of shrubs
     - log_LCS
   * - P19
     - Land cover of herbaceous vegetation
     - log_LCHV
   * - P20
     - Land cover of mangroves
     - log_LCM
   * - P21
     - Land cover of sparse vegetation
     - log_LCSV
   * - P22
     - Land cover of bare soil
     - log_LCBS
   * - P23
     - Land cover of snow and glaciers
     - log_LCSG
   * - P24
     - Land cover of water bodies
     - log_LCWB
   * - P36
     - Mean Annual Inflow
     - log_MAI
   * - P37
     - Peak Annual Inflow
     - log_PAI
   * - P39
     - Standard Deviation in Inflow
     - log_I_std
   * - P42
     - Mean Annual Outflow
     - log_MAO
   * - P43
     - Standard Deviation in Outflow
     - log_O_std
   * - P47
     - Mean Surface Area
     - log_SA_mean
   * - P48
     - Standard Deviation of Surface Area
     - log_SA_std
   * - P51
     - Kurtosis of Surface Area
     - log_SA_kurt
   * - P52
     - Mean Surface Area (clipped)
     - log_SA_mean_clip
   * - P62
     - Mean Annual Rainfall
     - log_MAR
   * - P74
     - Relative Original Capacity
     - log_ROBC
   * - P75
     - Geometry Complexity
     - log_GC
   * - P82
     - Rainfall per Unit Area
     - log_rain_per_area
   * - P83
     - Trapping Efficiency
     - log_TE
   * - P84
     - Residence Time
     - log_RT
   * - P85
     - Estimated Capacity Loss Rate
     - log_ECLR
   * - P86
     - Estimated Sedimentation Rate
     - log_ESR
   * - P87
     - Sediment Influx
     - log_SIN
   * - P88
     - Sediment Outflux
     - log_SOUT