Static Data Variables
====================

Static features in RECLAIM represent long-term physical, design, and catchment attributes of reservoirs that remain relatively constant over time. 
These variables are derived primarily from the GRILSS v1.2 dataset (Minocha and Hossain, 2025a,b) and several complementary global datasets, including GLC-SHARE, HWSD v2.0, and SRTM30_Plus. 
They include reservoir characteristics, catchment attributes, land cover, soil, and terrain properties that influence sedimentation processes.

Reservoir and Catchment Attributes
----------------------------------

The table below summarizes all static reservoir and catchment features used in RECLAIM. OSY-OEY defines the period of sedimentation observed. DL stands for dimensionless.

+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| No  | Name                               | Abbrev. | Description                                                              | Units                    |
+=====+====================================+=========+==========================================================================+==========================+
| D4  | Built Year                         | BY      | Year in which the construction of reservoir finished                     | X                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P1  | Original Built Capacity            | OBC     | Original design capacity of the reservoir                                | million cubic meter (MCM)|
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P2  | Dam Height                         | HGT     | Height of the impoundment of the reservoir                               | meter                    |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P3  | Major River Basin                  | MRB     | Name of the major river basin in which the reservoir is located          | X                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P4  | Latitude                           | LAT     | Geographical latitude of the impoundment                                 | degree                   |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P5  | Longitude                          | LON     | Geographical longitude of the impoundment                                | degree                   |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P6  | Reservoir Area                     | RA      | Nominal surface area of reservoir estimated using reservoir polygon      | sq km                    |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P7  | Reservoir Perimeter                | RP      | Nominal perimeter of the reservoir estimated using reservoir polygon     | km                       |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P8  | Flow Length                        | FL      | Shortest distance from reservoir inlet to dam outlet within reservoir    | km                       |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P9  | Catchment Area                     | CA      | Catchment area of the reservoir                                          | sq km                    |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P10 | Differential Catchment Area        | DCA     | Incremental catchment area excluding upstream reservoirs                 | sq km                    |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P11 | AEC Slope                          | AECS    | Mean slope of the area-elevation curve of the reservoir                  | km²/m                    |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P12 | AEC Curvature                      | AECC    | Mean curvature of the area-elevation curve of the reservoir              | km²/m²                   |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P13 | AEC Concavity Index                | AECI    | Ratio of area under straight line connecting min/max elevation to        | DL                       |
|     |                                    |         | actual AEC                                                               |                          |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P14 | Land Cover - Artificial Surfaces   | LCAS    | Percentage of catchment covered by artificial surfaces                   | %                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P15 | Land Cover - Cropland              | LCC     | Percentage of catchment covered by cropland                              | %                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P16 | Land Cover - Grassland             | LCG     | Percentage of catchment covered by grassland                             | %                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P17 | Land Cover - Trees                 | LCT     | Percentage of catchment covered by dense trees                           | %                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P18 | Land Cover - Shrubs                | LCS     | Percentage of catchment covered by shrubs                                | %                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P19 | Land Cover - Herbaceous Vegetation | LCHV    | Percentage of catchment covered by herbaceous vegetation                 | %                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P20 | Land Cover - Mangroves             | LCM     | Percentage of catchment covered by mangroves                             | %                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P21 | Land Cover - Sparse Vegetation     | LCSV    | Percentage of catchment covered by sparse vegetation                     | %                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P22 | Land Cover - Bare Soil             | LCBS    | Percentage of catchment covered by bare soil                             | %                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P23 | Land Cover - Snow and Glaciers     | LCSG    | Percentage of catchment covered by snow and glaciers                     | %                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P24 | Land Cover - Water Bodies          | LCWB    | Percentage of catchment covered by water bodies                          | %                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P25 | Dominant Land Cover                | DLC     | Dominant land cover type in the catchment                                | X                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P26 | Coarse Soil Composition            | COAR    | Mean percentage of coarse particles in the catchment soil                | %                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P27 | Sand Composition                   | SAND    | Mean percentage of sand in the catchment soil                            | %                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P28 | Silt Composition                   | SILT    | Mean percentage of silt in the catchment soil                            | %                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P29 | Clay Composition                   | CLAY    | Mean percentage of clay in the catchment soil                            | %                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P30 | Bulk Soil Density                  | BULK    | Mean bulk density of the catchment soil                                  | g/cm³                    |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P31 | Elevation                          | ELEV    | Mean elevation of the catchment above sea level                          | meter                    |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P32 | Slope                              | SLOP    | Mean ground slope within the catchment                                   | degrees                  |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P33 | Curvature                          | CURV    | Mean surface curvature of the terrain                                    | DL                       |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P34 | Aspect                             | ASP     | Mean orientation of slopes measured clockwise from north                 | degrees                  |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+
| P35 | Hillshade                          | HILL    | Mean relative illumination of terrain surface                            | X                        |
+-----+------------------------------------+---------+--------------------------------------------------------------------------+--------------------------+

.. note::
   Static features include attributes derived from reservoir polygons, catchment boundaries, and global datasets. While land cover can change over time, relative proportions are considered stable for modeling purposes. Dynamic changes in land use or sedimentation are described in dynamic variables, though are calculated within static features in reclaim.