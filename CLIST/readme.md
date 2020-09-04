# KICKS Clist replacement

The file `KICKS` in this folder replaces the CLIST from KICKS. If you installed it globally (or locally) you can upload this copy to replace the CLIST.

If you're hesitent then you can make the following changes. The reason for these changes is that KICKS needs to be able to reference (allocate) the VSAM file created by `dogedcams.py` in the `PYTHON` folder which generates JCL which creates JCL in `DOGE.VSAM`.

Manual instructions:

1) After `FREE  FI(PRODUCT)` (the first one), on a new line, put 

```clist
 /* FOR DOGE VSAM */
 FREE  FI(DOGEVSAM)
 ```

2) After ` ALLOC FI(PRODUCT) DA('&KIKID..KICKS.MURACH.PRODUCT') SHR`, on a new line, put:

```clist
 /* DOGE KICKS VSAM DATABASE */
 ALLOC FI(DOGEVSAM) DA('DOGE.VSAM') SHR
 ```

3) After `FREE  FI(PRODUCT)` (the second one), one a new line, put:

```clist
 /* FOR DOGE VSAM */
 FREE  FI(DOGEVSAM)
```