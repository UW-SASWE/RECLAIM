Dynamic Features
================

DDynamic features capture the temporal variability in hydrological, climatic, and catchment conditions that influence sedimentation processes over time. These features were derived using the Reservoir Assessment Tool (RAT) 3.0, a scalable Python package that leverages satellite remote sensing to monitor reservoir water surface area, water level changes, and related hydrological variables. RAT enables the generation of time series for inflow, outflow, surface area, evaporation, and normalized suspended sediment concentration (NSSC) for each reservoir.  

For detailed usage and documentation, please refer to the RAT repository and documentation: `RAT 3.0 Documentation <https://rat-satellitedams.readthedocs.io/en/latest/>`_.
  

Reservoir and Catchment Attributes
----------------------------------

The table below summarizes all dynamic reservoir and catchment features used in RECLAIM. OSY-OEY defines the period of sedimentation observed. DL stands for dimensionless.


+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| No  | Name                                        | Abbrev.           | Time-Series                | Description                                                   | Units                    |
+=====+=============================================+===================+============================+===============================================================+==========================+
| P36 | Mean Annual Inflow                          | MAI               | Inflow (OSY-OEY)           | Mean of annual inflows.                                       | m3/s                     |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P37 | Peak Annual Inflow                          | PAI               | Inflow (OSY-OEY)           | Maximum annual inflow.                                        | m3/s                     |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P38 | Coefficient of Variation in Inflow          | I_cv              | Inflow (OSY-OEY)           | Mean ratio of the annual standard deviation to annual mean of | DL                       |
|     |                                             |                   |                            | inflow.                                                       |                          |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P39 | Standard Deviation in Inflow                | I_std             | Inflow (OSY-OEY)           | Mean of annual standard deviation of inflow.                  | m3/s                     |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P40 | Days with above 90 percentile inflow        | I_above_90        | Inflow (OSY-OEY)           | Number of days in a year with inflow exceeding 90th           | X                        |
|     |                                             |                   |                            | percentile.                                                   |                          |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P41 | Maximum annual persistence in inflow        | I_max_persis      | Inflow (OSY-OEY)           | Maximum of annual decorrelation time across all years.        | days                     |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P42 | Mean Annual Outflow                         | MAO               | Outflow (OSY-OEY)          | Mean of annual outflows.                                      | m3/s                     |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P43 | Standard Deviation in Outflow               | O_std             | Outflow (OSY-OEY)          | Mean of annual standard deviation of outflow.                 | m3/s                     |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P44 | Coefficient of Variation in Outflow         | O_cv              | Outflow (OSY-OEY)          | Mean ratio of the annual standard deviation to annual mean of | DL                       |
|     |                                             |                   |                            | outflow.                                                      |                          |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P45 | Mean Evaporation                            | E_mean            | Evaporation (OSY-OEY)      | Mean evaporation rate.                                        | mm/day                   |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P46 | Standard Deviation of Evaporation           | E_std             | Evaporation (OSY-OEY)      | Annual standard deviation of evaporation rate.                | mm/day                   |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P47 | Mean Surface Area                           | SA_mean           | Surface Area (1984-2023)   | Mean of surface area.                                         | km2                      |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P48 | Standard Deviation of Surface Area          | SA_std            | Surface Area (1984-2023)   | Annual standard deviation of surface area.                    | km2                      |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P49 | Coefficient of Variation in Surface Area    | SA_cv             | Surface Area (1984-2023)   | Mean ratio of standard deviation to mean of surface area.     | DL                       |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P50 | Skewness of Surface Area                    | SA_skew           | Surface Area (1984-2023)   | Mean skewness of surface area distribution.                   | DL                       |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P51 | Kurtosis of Surface Area                    | SA_kurt           | Surface Area (1984-2023)   | Mean kurtosis of surface area distribution.                   | DL                       |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P52 | Mean Surface Area (clipped)                 | SA_mean_clip      | Surface Area (OSY-OEY)     | Mean of surface area.                                         | km2                      |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P53 | Days with above 90 percentile surface area  | SA_above_90       | Surface Area (OSY-OEY)     | Number of days in a year with surface area exceeding 90th     | X                        |
|     |                                             |                   |                            | percentile.                                                   |                          |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P54 | Mean NSSC1                                  | NSSC1_mean        | NSSC1 (OSY-OEY)            | Mean NSSC1.                                                   | DL                       |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P55 | Standard Deviation of NSSC1                 | NSSC1_std         | NSSC1 (OSY-OEY)            | Annual standard deviation of NSSC1.                           | DL                       |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P56 | Coefficient of Variation in NSSC1           | NSSC1_cv          | NSSC1 (OSY-OEY)            | Mean ratio of standard deviation to mean of NSSC1.            | DL                       |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P57 | Skewness of NSSC1                           | NSSC1_skew        | NSSC1 (OSY-OEY)            | Mean skewness of NSSC1 distribution.                          | DL                       |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P58 | Kurtosis of NSSC1                           | NSSC1_kurt        | NSSC1 (OSY-OEY)            | Mean kurtosis of NSSC1 distribution.                          | DL                       |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P59 | Mean NSSC2                                  | NSSC2_mean        | NSSC2 (OSY-OEY)            | Mean NSSC2.                                                   | DL                       |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P60 | Days with above 90 percentile NSSC2         | NSSC2_above_90    | NSSC2 (OSY-OEY)            | Number of days in a year with NSSC2 exceeding 90th percentile.| DL                       |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P61 | Maximum annual persistence in NSSC2         | NSSC2_max_persis  | NSSC2 (OSY-OEY)            | Maximum of annual decorrelation time across all years.        | DL                       |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| D5  | Vegetation Gain Frequency                   | VGF               | HILDA+ (1960-2019)         | Mean frequency of vegetation gain in the reservoir catchment. | X                        |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| D6  | Vegetation Loss Frequency                   | VLF               | HILDA+ (1960-2019)         | Mean frequency of vegetation loss in the reservoir catchment. | X                        |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P62 | Mean Annual Rainfall                        | MAR               | Precipitation (OSY-OEY)    | Mean annual rainfall during observation period.               | mm/year                  |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P63 | Rainy days with 10 mm or more               | #_rain_above_10   | Precipitation (OSY-OEY)    | Number of days in a year with more than 10 mm rainfall.       | X                        |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P64 | Rainy days with 50 mm or more               | #_rain_above_50   | Precipitation (OSY-OEY)    | Number of days in a year with more than 50 mm rainfall.       | X                        |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P65 | Rainy days with 100 mm or more              | #_rain_above_100  | Precipitation (OSY-OEY)    | Number of days in a year with more than 100 mm rainfall.      | X                        |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P66 | Mean Minimum Temperature                    | tmin_mean         | Temperature (OSY-OEY)      | Mean of minimum temperature.                                  | °C                       |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P67 | Mean Maximum Temperature                    | tmax_mean         | Temperature (OSY-OEY)      | Mean of maximum temperature.                                  | °C                       |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P68 | Mean Wind Speed                             | wind_mean         | Wind Speed (OSY-OEY)       | Mean wind speed.                                              | m/s                      |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P69 | Standard Deviation of Wind Speed            | wind_std          | Wind Speed (OSY-OEY)       | Annual standard deviation of wind speed.                      | m/s                      |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P70 | Coefficient of Variation in Wind Speed      | wind_cv           | Wind Speed (OSY-OEY)       | Mean ratio of standard deviation to mean of wind speed.       | DL                       |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P71 | Skewness of Wind Speed                      | wind_skew         | Wind Speed (OSY-OEY)       | Mean skewness of wind speed distribution.                     | DL                       |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+
| P72 | Kurtosis of Wind Speed                      | wind_kurt         | Wind Speed (OSY-OEY)       | Mean kurtosis of wind speed distribution.                     | DL                       |
+-----+---------------------------------------------+-------------------+----------------------------+---------------------------------------------------------------+--------------------------+