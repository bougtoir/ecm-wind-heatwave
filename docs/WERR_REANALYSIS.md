# R1 demand/WERR reanalysis

## Predeclared model-selection criteria
1. scientific appropriateness of marginal temperature estimand (CDD slope)
2. temporal OOS stability (3 blocked year folds)
3. coefficient/sign stability
4. calibration in warm-season range
5. reproducibility
6. parsimony
Selection never uses WERR sign or magnitude.

## Models
- M0: Phase-8 exact reproduction (CDD>22, train 2015-18/test 2019-20)
- M1: CDD base {20,22,24} by blocked CV + weekday/holiday/trend/COVID covariates; month-block bootstrap SE (B=500)
- M2: empirical-Bayes shrinkage to inverse-variance pooled mean for countries with sign-unstable folds or |slope|/SE < 1; shrunk slopes feed PRIMARY WERR

Pooled prior mean slope 26.9 MW/C, tau2 9513.8. 6/17 countries shrunk in primary WERR.

## Comparison
```
   country  m0_slope  m0_r2_train  m0_r2_test  m0_cv_r2  m1_slope   m1_se  m1_r2_train  m1_r2_test  m1_cv_r2  cdd_base     m1_fold_slopes  sign_stable  m2_slope   m2_se  use_shrunk_primary  slope_final  se_final
0       DE    36.518        0.027      -0.392    -0.309    23.972   6.826        0.160      -0.061    -0.112      20.0     16.9;31.7;24.9         True    23.986   6.809               False       23.972     6.826
1       FR   353.152        0.089      -0.186    -0.320   336.188  80.695        0.145      -0.041    -0.229      22.0  289.2;419.4;404.2         True   210.522  62.175               False      336.188    80.695
2       GB     0.000        0.000      -2.414    -3.500     0.000     NaN        0.507       0.081    -1.395      22.0       0.0;0.0;-0.0        False       NaN     NaN                True        0.000     0.000
3       ES   170.637        0.120      -0.400    -0.577   175.968  64.691        0.173      -1.278    -0.992      22.0  144.6;208.7;146.8         True   130.433  53.911               False      175.968    64.691
4       IT    27.359        0.044       0.073    -0.242    20.164  14.387        0.214      -1.770    -6.506      20.0      5.9;23.7;27.3         True    20.308  14.233               False       20.164    14.387
5       NL   114.246        0.033       0.026    -0.905    44.908  25.031        0.483      -7.072    -7.266      20.0     49.3;74.4;56.2         True    43.796  24.246               False       44.908    25.031
6       BE    33.842        0.054      -0.973    -1.129    20.959   8.505        0.130      -1.110    -1.869      20.0      2.1;34.9;26.3         True    21.004   8.473               False       20.959     8.505
7       DK    21.744        0.049      -0.073    -0.373    41.623   8.231        0.135      -0.552    -0.244      24.0     -0.0;38.5;38.4        False    41.519   8.202                True       41.519     8.202
8       AT     4.666        0.001      -0.013    -0.363     2.097   8.133        0.253      -1.651    -1.560      20.0       0.7;11.3;9.4         True     2.269   8.105                True        2.269     8.105
9       PL    80.002        0.062       0.131    -0.248    62.440  11.742        0.352      -1.909    -1.680      20.0     56.5;73.6;62.2         True    61.932  11.658               False       62.440    11.742
10      SE    -8.234        0.001      -0.037    -0.075   -37.007  26.030        0.073      -0.116    -0.735      24.0   -0.0;-28.2;-18.2         True   -32.757  25.150               False      -37.007    26.030
11      NO   -25.349        0.000      -0.051    -0.909    33.069  18.402        0.151      -3.204   -19.171      20.0     -0.0;-4.9;-6.6        False    32.858  18.083                True       32.858    18.083
12      FI    60.715        0.022      -0.628    -1.064    23.285  31.044        0.099      -1.779    -2.134      20.0    -14.3;26.7;21.4        False    23.619  29.582                True       23.619    29.582
13      IE   253.001        0.009      -0.529    -0.410    89.183  18.955        0.323      -0.737    -0.809      22.0      0.0;77.1;98.3         True    86.918  18.607               False       89.183    18.955
14      PT    34.166        0.140      -0.037    -0.189    52.004   7.668        0.233      -0.848    -0.806      24.0     40.0;65.9;55.2         True    51.850   7.645               False       52.004     7.668
15      CZ    20.846        0.065       0.021    -0.577    16.232   4.629        0.358      -1.356    -1.967      20.0     15.2;20.3;19.9         True    16.256   4.624               False       16.232     4.629
16      CH   -24.105        0.001      -0.039    -0.766   -21.706  29.952        0.065      -0.523    -4.872      22.0     -3.2;18.5;-2.5        False   -17.516  28.632                True      -17.516    28.632
```
