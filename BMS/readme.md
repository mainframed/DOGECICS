# CICS/KICKS Maps

This folder contains the the BMS maps used by DOGE. They can all be assembled using the jcl* in `compile_maps.jcl`. 

* `DOGEGMSC` map for DOGE *Good Morning* acts as the splash page. After assembly* resides in `HERC01.KICKS.V1R5M0.KIKRPL(DOGECN)`.
* `DOGEMMAP` map for DOGE main menu. After assembly* resides in `HERC01.KICKS.V1R5M0.KIKRPL(DOGEMM)`.
* `DOGESMAP` map for DOGE sending coin. After assembly* resides in `HERC01.KICKS.V1R5M0.KIKRPL(DOGEMM)`.
* `DOGETMAP` map for DOGE transaction history. After assembly* resides in `HERC01.KICKS.V1R5M0.KIKRPL(DOGEMM)`.
* `DOGEDMAP` map for DOGE transaction detail. After assembly* resides in `HERC01.KICKS.V1R5M0.KIKRPL(DOGEMM)`.

\* assuming you're using KICKS and its default instalation. For CICS it would need to reside in your resource pool. See [CICS Details](https://gist.github.com/mainframed/a8e94ec1e2d791eaf96d9aac981e2c10) for more information.