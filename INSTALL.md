# Installing DOGE CICS

These instructions are for DOGE CICS on KICKS for TSO on **tk4-**. For CICS, you're on your own `(^_-)`.

The install looks complicated but its not too daunting, just follow the steps to modify `tk4-`, which is the hardest part. 

## TK4- Changes

### First Steps

1. Download and install **tk4-** from http://wotho.ethz.ch/tk4-/ make sure you install `tk4-_v1.00_current.zip`.
    * Change to daemon mode by running the command `set_daemon_mode` in the folder `unattended`.
2. Install KICKS from https://github.com/moshix/kicks download `kicks-tso-v1r5m0.zip` 
    * It's easiest if you follow the instructions from [MOSHIX here](https://www.youtube.com/watch?v=u_ZSH9OagTM). 

## Create a New JES2 Socket

We need to setup a CLASS so KICKS/DOGE can communicate with the `dogedcams.py` python script. This script is used when you want to send DOGE coin using the send transaction or update the transaction history database.

First in **tk4-** you need to add the following to `local_conf/01` (dont worry, the file starts off as empty):

```
# SYSOUT=D (MSGCLASS?)
010E 1403 0.0.0.0:3506 sockdev
```

(This adds a new printer at address 10E, which is included with TK4- which you can see here: http://naspa.net/website/files/CD6/cookbook/genmvs.html)

Next, boot **tk4-** with the `./mvs` command in linux. Once its loaded, use `x3270`, connect to `localhost:3270` and logon as `herc01`/`cul8tr`, hit enter a bunch of times until you get to the `REVIEW FRONT END` (this is called `RFE` but I'll refer to it later as `REVIEW`). Type `3.4` and hit enter. In `Data set name prefix ==>` type `SYS1.JES2PARM` and hit enter. Right below the `S` on the left side of the screen type `E` and hit enter, then on the `.` in front of `JES2PARM` hit enter (you are now editing a members of a partitioned dataset: `SYS1.JES2PARM(JES2PARM)`).

**Pro Tips**: In this editor you enter new lines by typing `I#` in the left hand side where the numbers are. For example, `i23` would insert 23 lines. But be careful! If you hit enter any empty line gets deleted. If you screw up, don't hit `F3` to exit, this will autosave your changes, type `CANCEL` in the `Command ===>` area. Speaking of the `Command ===>` you can use `F` or `FIND` to search for the things you need to changes instead of using `F7`/`F8` to go down/up in the document. 

Next we're going to make the following changes:

1. Change `&MAXPART=6` to `&MAXPART=7`
2. Change `&NUMPRTS=3` to `&NUMPRTS=4`

(these increase the number of printers)

4. Change `I6       START,NAME=6,CLASS=SC` to `I6       START,NAME=6,CLASS=SCD`

(includes CLASS D in the initiators on startup)

5. Underneath the following: 
```
&C       NOJOURN,LOG,OUTPUT,PROCLIB=00,PERFORM=1, KICKS single thread  C
               CONVPARM=00000100099930E00011                            
```
add

```
***************                                                         
&D       NOJOURN,LOG,OUTPUT,PROCLIB=00,PERFORM=1, DOGE Output          C
               CONVPARM=00000100099930E00011                            
```
(This includes Class D)

6. Then add the following below the `PRINTER3` line:

```
PRINTER4       CLASS=D,SEP,AUTO,DSPLTCEL,NOPAUSE,UNIT=10E,DRAIN,       +
               UCS=QN,FCB=6                                             
```

So that it looks like this:

```
PRINTER1       CLASS=A,SEP,AUTO,DSPLTCEL,NOPAUSE,UNIT=00E,DRAIN,       +
               UCS=QN,FCB=6                                             
PRINTER2       CLASS=Z,SEP,AUTO,DSPLTCEL,NOPAUSE,UNIT=00F,DRAIN,       +
               UCS=QN,FCB=6                                             
PRINTER3       CLASS=X,SEP,AUTO,DSPLTCEL,NOPAUSE,UNIT=002,DRAIN,       +
               UCS=QN,FCB=6                                             
PRINTER4       CLASS=D,SEP,AUTO,DSPLTCEL,NOPAUSE,UNIT=10E,START,       +
               UCS=QN,FCB=6,FORMS=0001
```

(This adds the actual printer)

7. Change `$$D PRINT,SYSOUT,HOLD                HOLD - SYSOUT` to `$$D PRINT,SYSOUT,NOHOLD,TRKCEL      DOGE Printer for DOGECICS` 

(This changes the message class)

Ok, *phew* that was a lot of changes. But we're not done yet. 

Edit `SYS1.PARMLIB(STARTSTD)` (using the same method described above) and add `CMD $SPRT4` to the line below `CMD $SPRT3`

(this makes sure the printer is started on IPL)

Okay, we're done with **tk4-** surgery. The rest is easy. 

Take the following three lines and put them in a file called `dogebr14.jcl`:

```jcl
//DOGEBR14 JOB CLASS=D,MSGCLASS=D,MSGLEVEL=(1,1)                          
//DOGELOL EXEC PGM=IEFBR14                       
```

On your host machine (Linux only, sorry windows people) place `dogebr14.jcl` in `./local_scripts` in your **tk4-** folder.

Then take the following 9 lines and add them to `./local_scipts/01` in your **tk4-** folder:

```bash
# updated for DOGE

* Submitting DOGEBR14 to initialize Printer 4
sh cat local_scripts/dogebr14.jcl|nc -w1 localhost 3505
* Pausing for a second
pause 1
* Restarting Printer 4
/$sprt4
* Done
```

(this submits a dummy job and restarts the printer, without this the printer would die after first use and you'd have to restart it manually.)

You're now all set.

## Installing DOGECICS

### Creating Folder and upload

Next we need to install DOGECICS. First enable the **tk4-** ftp server in the hercules window (this is where the hercules emulator is running) next to `herc =====>` type: `/s ftpd,srvport=21021` (this assumes you have port 21021 available, if not use a different port).

Then, in **tk4-** get to REVIEW and type `3.2`. On the `COMMAND ===>` line type `A` but don't hit enter, hit tab until you get to `DATA SET NAME ===>` and type `'HERC01.DOGECICS'`. **Note the `'` you need those. You don't need to use `HERC01` but if you dont make sure you update the JCL later. Hit Enter and fill it out like so:

```                              
       NAME OF NEW DATA SET ==> 'HERC01.DOGECICS'
 
              RECORD FORMAT ==> FB
      LOGICAL RECORD LENGTH ==> 80
        PHYSICAL BLOCK SIZE ==> 19040
 
                     VOLUME ==> PUB002
                       UNIT ==>
 
      ALLOCATION SPACE UNIT ==> T       ( T OR C OR B )
     PRIMARY SPACE QUANTITY ==> 108
   SECONDARY SPACE QUANTITY ==> 6
 NUMBER OF DIRECTORY BLOCKS ==> 13
```
(this creates a partitioned dataset, or folder, called `HERC01.DOGECICS`)

using the ftp client in linux connect: `ftp localhost 21021`. Type `cd HERC01.DOGECICS`.

Make sure you're in the `DOGECICS/BMS` folder on linux (you can use `lcd` in ftp to change your local directory) then upload:

```bash
put DOGEDMAP
put DOGEGMSC
put DOGEMMAP
put DOGESMAP
put DOGETMAP
```

change the working directory to COBOL `lcd ../COBOL` then upload:

```bash
put DOGEDEET
put DOGEMAIN
put DOGEQUIT
put DOGESEND
put DOGETRAN
```

change the working directory to SIT `lcd ../SIT` then upload:

```
put KIKFCTDO
put KIKPCTDO
put KIKPPTDO
put KIKSITDO
```

change the working directory to JCL `lcd ../JCL` then upload:

```
put compile_cobol.jcl COMPCOBL
put compile_maps.jcl  COMPMAPS
```

If you're curious what each of these do, each folder has a `readme.md` that outlines what every file is for.

### Compiling Tables, Maps and COBOL

Assuming you're using the **tk4-** and **KICKS** defaults you can now compile the KICKS tables. Open, then submit them by editing them as outlined above in REVIEW and in the `Command ===>` line type `sub`.

* `HERC01.DOGECICS(KIKFCTDO)`
* `HERC01.DOGECICS(KIKPCTDO)`
* `HERC01.DOGECICS(KIKPPTDO)`
* `HERC01.DOGECICS(KIKSITDO)`

Then you do the same for the CICS Maps and COBOL programs:

* `HERC01.DOGECICS(COMPMAPS)` 
* `HERC01.DOGECICS(COMPCOBL)` 

These jobs aren't very complicated, see the `readme.md` in the JCL folder for what they do. 

This will take a while if you're running this on a Pi zero but shouldn't take more than a few minutes. You can watch the MIPS counter in hercules while you wait. 


### Change KICKS startup CLIST

This needs to be done so KICKS programs can access VSAM file `dogedcams.py` creates. 

You can either upload with FTP the file `CLIST/KICKS` to `SYS2.CMDPROC(KICKS)` (or `HERC01.KICKSSYS.V1R5M0.CLIST(KICKS)` depending on your install) or you can edit those files as follows: 

1. After both `FREE  FI(PRODUCT)` put:

```
/* FOR DOGE VSAM */
FREE  FI(DOGEVSAM)
```

**NOTE** You need to do the above in two places

2. After `ALLOC FI(PRODUCT) DA('&KIKID..KICKS.MURACH.PRODUCT') SHR` put:

```
/* DOGE KICKS VSAM DATABASE */                          
ALLOC FI(DOGEVSAM) DA('DOGE.VSAM') SHR                      
```

(`DOGE.VSAM` is where the python script stores its output for use in DOGE KICKS by default, if you've changed it make sure you make the same change above.)

## Install Dogecoin Core

Yes, you still need a dogecoin wallet for this to work. If you just want to look at CICS transactions see the section below for generating fake transactions without dogecoin.

1. Download **Dogecoin Core** from http://dogecoin.com/ for linux (may work in windows/mac but untested)

2. Launch dogecoin-qt: From the unzipped dogecoin core folder `./bin/dogecoin-qt` and wait 6 days for the blockchain to download (hope you got 40gb of free space)

3. Edit `~/.dogecoin/dogecoin.conf` and configure your RPC settings:

```
# DOGEBANK RPC Server Conf
server=1
rpcuser=doge
rpcpassword=egod
```

### Testnet

If you want to just play around without using/buying actual coins you can use testnet instead by adding `testnet=1` or by launching dogecoin with `./bin/dogecoin-qt -testnet`:

```
# DOGEBANK RPC Server Conf
server=1
rpcuser=doge
rpcpassword=egod
testnet=1
```
You can get testnet coins from: https://testnet-faucet.com/doge-testnet/. 

If you do this make sure you pass `--rpcport 44555` to the `dogedcams.py`.

# Updating VSAM and Getting Transactions

With everything setup, now we can generate the VSAM file and periodically check to see if we need to send funds. 

In the python folder is the script `dogedcams.py`. This script performs two functions:

1. If there are new records in dogecoin core it generates the JCL used to create a VSAM file on **tk4-**, and submits this JCL
2. Checks to see if there are any send records on the class D printer we created. Processes them and sends dogecoin as entered in the DSND transaction

See the `readme.md` in the PYTHON folder for details. **Note**: A temp file is created to track transactions so its not uploading new VSAM files all the time. You can force an update by using `--force` flag. 

If you don't want to install dogecoin core you can pass this script the argument `--fake` and it will generate fake transactions.

You can either manually run the script every time there's some new stuff going on or place it in cron and let it run every 5 minutes with `crontab -e` then insert:

```cron
*/5 * * * * /home/pi/DOGECICS/PYTHON/dogedcams.py --force
```

This all assumes you're running the python script on the same host as **dogecoin core** and **tk4-**. If not check out `readme.md` in the `PYTHON` for command option flags. 

**IMPORTANT**

* The VSAM file won't update while KICKS is running and fails silently. Exit KICKS then use `--force` to force an update. 
* Sent funds wont show up in the VSAM file until after you run the script again. 

# Using DOGECICS

DOGECICS is a simple CICS/KICKS application. Access CICS on **tk4-** by running `KICKS SIT(DO)` from the TSO `READY` prompt (hit `F3` a bunch). Once you're at the `K I C K S` screen *CLEAR* the screen with the `x3270` keyboard (top right hand button) and click `Clear`. With the screen clear type `DOGE` and away you go. To exit DOGECICS at any time hit `F3`. To Exit KICKS clear the screen and type `KSSF`.

It's made up of 5 transactions:

* **DOGE**: The splash page and the main menu
* **DTRN**: Transaction history - shows transaction history 
* **DEET**: Transactions details - Accessed through the transaction history transaction type `T` or hit `F6` to go back
* **DSND**: Send DOGE - Fill out the address and the amount you wish to send
* **QUIT**: Cheeky quit message

You can access the main menu by typing `W` in the `Option` field at any time after hitting `F5` on the splash screen. 

# BONUS CONTENT

If you really want to DOGE-ify your **tk4-** do the following:

**hercules message after loading RC scripts**

Replace `scripts/tk4-.rc` with the following:

```
#**********************************************************************
#***                                                                ***
#*** Script:  tk4-.rc                                               ***
#***                                                                ***
#*** Purpose: complete TK4- initialization and display logo         ***
#***                                                                ***
#*** Updated: 2016/08/19                                            ***
#***                                                                ***
#**********************************************************************
pause 1
script scripts/tk4-_updates.rc
${LOCALRC:=script scripts/local.rc}
pause 1
*                             Y.                      _
*                              YiL                   .```.
*                              Yii;      WOW       .; .;;`.
*                MUCH KICKS    YY;ii._           .;`.;;;; :
*                              iiYYYYYYiiiii;;;;i` ;;::;;;;  SUCH TK4-
*                          _.;YYYYYYiiiiiiYYYii  .;;.   ;;;    
*                       .YYYYYYYYYYiiYYYYYYYYYYYYii;`  ;;;;
*                     .YYYYYYY$$YYiiYY$$$$iiiYYYYYY;.ii;`..
*                    :YYY$!.  TYiiYY$$$$$YYYYYYYiiYYYYiYYii.
*                    Y$MM$:   :YYYYYY$!"``"4YYYYYiiiYYYYiiYY.
*                 `. :MM$$b.,dYY$$Yii" :`   :YYYYllYiiYYYiYY
*              _.._ :`4MM$!YYYYYYYYYii,.__.diii$$YYYYYYYYYYY
*              .,._ $b`P`     "4$$$$$iiiiiiii$$$$YY$$$$$$YiY;
*                 `,.`$:       :$$$$$$$$$YYYYY$$$$$$$$$YYiiYYL
*                  "`:$$.    .;PPb$~.,.``T$$YY$$$$YYYYYYiiiYYU:
*                ` ;$P$;;: ;;;;i$y$"!Y$$$b;$$$Y$YY$$YYYiiiYYiYY
*                  $Fi$$ .. ``:iii.`-";YYYYY$$YY$$$$$YYYiiYiYYY
*                  :Y$$rb ````  `_..;;i;YYY$YY$$$$$$$YYYYYYYiYY:
*                   :$$$$$i;;iiiiidYYYYYYYYYY$$$$$$YYYYYYYiiYYYY.
*                    `$$$$$$$YYYYYYYYYYYYY$$$$$$YYYYYYYYiiiYYYYYY
*                    .i!$$$$$$YYYYYYYYY$$$$$$YYY$$YYiiiiiiYYYYYYY
*                   :YYiii$$$$$$$YYYYYYY$$$$YY$$$$YYiiiiiYYYYYYi`
*
*            
*            TK3  created by Volker Bandke        vbandke@bsp-gmbh.com
*            TK4- update 8 by Juergen Winkelmann  winkelmann@id.ethz.ch
*                     see TK4-.CREDITS for complete credits
*            DOGE created by Soldier of FORTRAN
*
```

**Replace the hercules screen**

replace the file `herclogo.txt` in the **tk4-** root folder with the following:

```
@ALIGN NONE
@SBA 0,0
@SF P
Hercules Version  :
@SF HP
$(VERSION)
@NL
@SF P
Device number     :
@SF HP
$(CSS):$(CCUU)
@NL
@SF P
Subchannel        :
@SF HP
$(SUBCHAN)
@SF P
@ALIGN LEFT
                                                                      
                           DOGE Banking Systems                       
                                                                      
            DOGE  created by Soldier of FORTRAN                        
            KICKS created by Mike Noel          mikenoel137@gmail.com
            TK3   created by Volker Bandke      vbandke@bsp-gmbh.com   
            TK4-  update by Juergen Winkelmann  winkelmann@id.ethz.ch  
                     see TK4-.CREDITS for complete credits            
@SF HP
@NL                                                                      
                                                                      
                 ___           ___           ___           ___        
                /\  \         /\  \         /\  \         /\  \       
               /::\  \       /::\  \       /::\  \       /::\  \      
              /:/\:\  \     /:/\:\  \     /:/\:\  \     /:/\:\  \     
             /:/  \:\__\   /:/  \:\  \   /:/  \:\  \   /::\~\:\  \    
            /:/__/ \:|__| /:/__/ \:\__\ /:/__/_\:\__\ /:/\:\ \:\__\   
            \:\  \ /:/  / \:\  \ /:/  / \:\  /\ \/__/ \:\~\:\ \/__/   
             \:\  /:/  /   \:\  /:/  /   \:\ \:\__\    \:\ \:\__\     
              \:\/:/  /     \:\/:/  /     \:\/:/  /     \:\ \/__/     
               \::/__/       \::/  /       \::/  /       \:\__\       
                ~~            \/__/         \/__/         \/__/       
```

**Custom tk4- NETSOL Screen**

There's also a custom NETSOL (the second screen you see when you logon) that replaces the **tk4-** screen included in the `extras` folder. Upload the JCL file `doge-tk4.jcl` to wherever you like as `DOGETK4`, `HERC01.DOGECICS` will works if you don't know where to put it. Then submit the JCL. 

To see all the **bonus** changes you need to reset **tk4-**, from TSO type `SHUTDOWN` then when hercules exits type `./mvs` and you're good to go.
