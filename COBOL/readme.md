# CICS/KICKS COBOL Code

This folder contains COBOL code that drives DOGECOIN CICS. They can all be compiled using* in `compile_cobol.jcl`. 

* `DOGEMAIN` splash screen and main menu.
* `DOGESEND` send doge coin screen, enter an address and an amount.
* `DOGETRAN` wallet transaction history.
* `DOGEDEET` detailed transaction information.
* `DOGEQUIT` Cute exit message `(^-^)`

\* assuming you're using KICKS and its default instalation. For CICS it would need to reside in your resource pool and installed using CEDA. See [CICS Details](https://gist.github.com/mainframed/a8e94ec1e2d791eaf96d9aac981e2c10) for more information.