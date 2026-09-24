# R2 exposure chronology sensitivity

Variants: A = dated + static undated-OSM background (canonical); B = dated units only; C = dated registry units only (all OSM excluded).
WFI recomputed per variant with identical kernel/winds; Phase-3 regional spec refit per variant.

```
                         region          variant  wfi_mean_2021      coef_wfi            se  boot_p
0                        domain        A_current     540.083492 -3.867946e-03  5.004505e-04    0.00
1                        domain     B_dated_only     176.115896 -3.642493e-03  1.040751e-03    0.00
2                        domain  C_registry_only     166.352185 -3.800711e-03  1.083234e-03    0.00
3      northsea_to_lowcountries        A_current    3868.101620  3.685533e-04  9.917210e-05    0.00
4      northsea_to_lowcountries     B_dated_only    2609.715067  2.472702e-04  1.015685e-04    0.01
5      northsea_to_lowcountries  C_registry_only    2495.837245  2.661555e-04  1.034047e-04    0.01
6   northsea_to_denmark_germany        A_current    4003.014308  5.038082e-04  8.009784e-05    0.00
7   northsea_to_denmark_germany     B_dated_only    3306.060289  5.076569e-04  8.742087e-05    0.00
8   northsea_to_denmark_germany  C_registry_only    3229.977981  5.280934e-04  8.827652e-05    0.00
9            atlantic_to_france        A_current    1541.110306 -1.280142e-06  1.537601e-04    0.91
10           atlantic_to_france     B_dated_only     145.679753  1.390903e-03  7.435873e-04    0.03
11           atlantic_to_france  C_registry_only     112.089373  1.657156e-03  8.442097e-04    0.02
12           atlantic_to_iberia        A_current    2975.750305 -2.134072e-04  5.104394e-05    0.00
13           atlantic_to_iberia     B_dated_only       2.366255 -9.895021e-03  6.007426e-02    0.80
14           atlantic_to_iberia  C_registry_only       0.000000  1.693360e-12  1.952536e-12    0.97
15     uk_offshore_to_continent        A_current    3712.051456  5.525070e-04  5.651349e-05    0.00
16     uk_offshore_to_continent     B_dated_only    2477.907535  3.471217e-04  6.477161e-05    0.00
17     uk_offshore_to_continent  C_registry_only    2347.194904  3.608092e-04  6.571020e-05    0.00
```
