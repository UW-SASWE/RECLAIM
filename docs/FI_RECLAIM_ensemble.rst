Feature Importance of RECLAIM Ensemble
======================================

Because individual models can yield substantially different importance rankings, we adopted an **ensemble approach**: a weighted average (based on mean model weights used by RECLAIM in the training dataset) for Sedimentation Rate.  
Below table lists all 88 variables along with their importance, cumulative importance, and rank for ensemble in RECLAIM using mean of dynamnic weights in training data.

.. list-table:: **Feature importance of all 88 variables from RECLAIM ensemble.**
   :header-rows: 1
   :align: center
   :widths: 5 20 20 20

   * - Rank
     - Variable
     - Feature Importance (%)
     - Cumulative Importance (%)
   * - 1
     - log_OBC
     - 14.633882
     - 14.633882
   * - 2
     - log_LCWB
     - 8.004204
     - 22.638086
   * - 3
     - log_SA_mean_clip
     - 7.383239
     - 30.021326
   * - 4
     - log_CA
     - 6.589474
     - 36.610800
   * - 5
     - log_LCM
     - 4.316336
     - 40.927136
   * - 6
     - log_LCG
     - 3.379634
     - 44.306770
   * - 7
     - log_LCSG
     - 2.390016
     - 46.696786
   * - 8
     - log_SA_std
     - 1.985361
     - 48.682147
   * - 9
     - wind_mean
     - 1.840513
     - 50.522661
   * - 10
     - log_rain_per_area
     - 1.765137
     - 52.287797
   * - 11
     - log_LCC
     - 1.607280
     - 53.895078
   * - 12
     - AGE
     - 1.472827
     - 55.367905
   * - 13
     - R_SA_cap
     - 1.340215
     - 56.708120
   * - 14
     - log_O_std
     - 1.290960
     - 57.999079
   * - 15
     - SILT
     - 1.229707
     - 59.228786
   * - 16
     - log_LCS
     - 1.186893
     - 60.415679
   * - 17
     - LON
     - 1.109406
     - 61.525085
   * - 18
     - wind_cv
     - 1.087307
     - 62.612392
   * - 19
     - E_std
     - 1.055644
     - 63.668036
   * - 20
     - log_SOUT
     - 1.035725
     - 64.703761
   * - 21
     - NSSC1_std
     - 1.025786
     - 65.729547
   * - 22
     - log_MAR
     - 0.930290
     - 66.659837
   * - 23
     - log_DCA
     - 0.915694
     - 67.575531
   * - 24
     - NSSC2_max_persis
     - 0.882480
     - 68.458011
   * - 25
     - wind_kurt
     - 0.833630
     - 69.291641
   * - 26
     - wind_skew
     - 0.812826
     - 70.104466
   * - 27
     - log_LCAS
     - 0.805496
     - 70.909963
   * - 28
     - O_cv
     - 0.786492
     - 71.696454
   * - 29
     - AECC
     - 0.781898
     - 72.478352
   * - 30
     - SAND
     - 0.754986
     - 73.233339
   * - 31
     - log_MAO
     - 0.752642
     - 73.985981
   * - 32
     - NSSC2_mean
     - 0.717024
     - 74.703005
   * - 33
     - SLOP
     - 0.682984
     - 75.385989
   * - 34
     - log_LCT
     - 0.667932
     - 76.053921
   * - 35
     - I_cv
     - 0.647218
     - 76.701138
   * - 36
     - NVGF
     - 0.645478
     - 77.346616
   * - 37
     - NSSC1_cv
     - 0.644180
     - 77.990796
   * - 38
     - NSSC1_skew
     - 0.642675
     - 78.633471
   * - 39
     - R_shrub_bare
     - 0.632633
     - 79.266104
   * - 40
     - rel_SA_mean_clip
     - 0.627533
     - 79.893637
   * - 41
     - I_above_90
     - 0.622972
     - 80.516608
   * - 42
     - CURV
     - 0.612935
     - 81.129543
   * - 43
     - log_LCBS
     - 0.600176
     - 81.729719
   * - 44
     - log_ESR
     - 0.568189
     - 82.297908
   * - 45
     - wind_std
     - 0.562443
     - 82.860351
   * - 46
     - log_SA_mean
     - 0.545410
     - 83.405761
   * - 47
     - BULK
     - 0.537301
     - 83.943063
   * - 48
     - R_treaa_bare
     - 0.523224
     - 84.466287
   * - 49
     - R_coarse_sand
     - 0.517022
     - 84.983308
   * - 50
     - log_LCHV
     - 0.509614
     - 85.492923
   * - 51
     - ELEV
     - 0.506835
     - 85.999757
   * - 52
     - log_ROBC
     - 0.504507
     - 86.504264
   * - 53
     - I_max_persis
     - 0.499298
     - 87.003562
   * - 54
     - SA_skew
     - 0.490533
     - 87.494095
   * - 55
     - NSSC1_mean
     - 0.489971
     - 87.984066
   * - 56
     - ASP
     - 0.486329
     - 88.470395
   * - 57
     - NSSC1_kurt
     - 0.470670
     - 88.941065
   * - 58
     - log_HGT
     - 0.461355
     - 89.402420
   * - 59
     - log_GC
     - 0.454284
     - 89.856704
   * - 60
     - log_PAI
     - 0.448311
     - 90.305015
   * - 61
     - SA_cv
     - 0.447305
     - 90.752320
   * - 62
     - DLC
     - 0.445204
     - 91.197524
   * - 63
     - log_TE
     - 0.434373
     - 91.631898
   * - 64
     - E_mean
     - 0.423686
     - 92.055584
   * - 65
     - log_ECLR
     - 0.421004
     - 92.476587
   * - 66
     - #_rain_above_50
     - 0.419211
     - 92.895798
   * - 67
     - log_MAI
     - 0.396943
     - 93.292742
   * - 68
     - SA_above_90
     - 0.386455
     - 93.679196
   * - 69
     - log_SIN
     - 0.370423
     - 94.049620
   * - 70
     - log_RP
     - 0.369811
     - 94.419431
   * - 71
     - NSSC2_above_90
     - 0.367674
     - 94.787105
   * - 72
     - AECI
     - 0.363760
     - 95.150865
   * - 73
     - log_SA_kurt
     - 0.363547
     - 95.514412
   * - 74
     - #_rain_above_10
     - 0.350768
     - 95.865180
   * - 75
     - tmin_mean
     - 0.342336
     - 96.207516
   * - 76
     - COAR
     - 0.339481
     - 96.546997
   * - 77
     - log_FL
     - 0.338535
     - 96.885531
   * - 78
     - log_RT
     - 0.333771
     - 97.219302
   * - 79
     - log_I_std
     - 0.333185
     - 97.552487
   * - 80
     - CLAY
     - 0.330524
     - 97.883011
   * - 81
     - log_RA
     - 0.302114
     - 98.185125
   * - 82
     - tmax_mean
     - 0.285973
     - 98.471097
   * - 83
     - AECS
     - 0.284486
     - 98.755583
   * - 84
     - #_rain_above_100
     - 0.281851
     - 99.037435
   * - 85
     - MRB
     - 0.253738
     - 99.291173
   * - 86
     - HILL
     - 0.246680
     - 99.537852
   * - 87
     - LAT
     - 0.238995
     - 99.776847
   * - 88
     - log_LCSV
     - 0.223153
     - 100.000000
