# Doge CICS Bonus Stuff

This is bonus stuff for Doge CICS for **tk4-**.

* `herclogo.txt` Replacement herclogo.txt for hercules
* `tk4-doge.ans` ANSI netsol/vtam replacement mockup
* `tk4-doge.jcl` JCL to replace netsol/vtam screen, generated with https://github.com/mainframed/ANSi2EBCDiC command: `ansi2ebcdic.py --netsol --ROW 23 --COL 32 --color YELLOW --file tk4-doge.jcl --member DOGESOL tk4-doge.ans`
* `tk4-.rc` Replaces the tk4- rc scripts, doesn't do anything but put the DOGE face instead of the **tk4-** cat