# DOGEDCAMS

A python script developed to create VSAM records of historical dogecoin (or really any crypto currency that uses RPC) and also send transactions entered in a KICKS application. 

If you're running both **dogecoin core** and **tk4-** on the same host you can run `dogedcams.py` and it will find the rpc settings, logon and connect to **tk4-** automatically. By default it uses the default **tk4-** credentials of `HERC01`/`CUL8TR`. The location of the VSAM file is `DOGE.VSAM`.  

Defaults overview:

* RPC: 
    * Hostname/port: localhost:22555
    * Username: read from RPC file in `~/.dogecoin/dogecoin.conf`
    * Password: read from RPC file in `~/.dogecoin/dogecoin.conf`
* tk4-:
    * JCL reader hostname/port: localhost:3505
    * JCL printer hostname/port: localhost:3506
    * Username: HERC01
    * Password: CUL8TR
    * VSAM Filename: `DOGE.VSAM`
    * Volume: `PUB012`

All of these options can be changed by passing arguments to the script (see help output below). For example to change the volume pass the argumen `--volume MTVROK` to change the volume.


There's a few other arguments worth discussing here:

* `--debug`/`-d` This prints verbose debug information so you can trouble shoot if you have issues
* `--force`/`-f` This argument will force a new VSAM file creation. Basically the script makes a new VSAM whenever it sees changes in your wallet. If there's no changes it doesn't update. But you can force changes with this flag. 
* `--print` This flag will print out all the JCL before sending it to **tk4-**
* `--test` This only prints whats about to be sent and doesn't get records from **tk4**
* `--start-records-at-one` **tk4-** max records on the default volume is 7,650. By default this script will show you the most recent 7,650 transactions. If you wish to instead show the first 7,650 records use this flag


## Help output from the script

```
usage: dogedcams.py [options]

DOGEdcams data generator for DOGE Bank. Used to send and receive funds between KICKS on TK4- and DogeCICS.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Print lots of debugging statements (default: 30)
  -t, --test            Test sending JCL to TK4- (default: False)
  -p, --print           Print JCL being sent to TK4 (default: False)
  -f, --force           Force VSAM update even if no changes to wallet (default: False)
  --fake FAKE           Generate fake records (default: None)
  --username USERNAME   TK4- username for JCL (default: herc01)
  --password PASSWORD   TK4- password for JCL (default: cul8tr)
  --vsam_file VSAM_FILE
                        TK4- VSAM file used by dogekicks (default: DOGE.VSAM)
  --volume VOLUME       TK4- volume to store VSAM file (default: pub012)
  --rdrport RDRPORT     TK4- Reader sockdev port (default: 3505)
  --prtport PRTPORT     TK4- Printer sockdev port (default: 3506)
  --hostname HOSTNAME   TK4- sockdev host (default: localhost)
  --rpcuser RPCUSER     Crypto wallet username (default: None)
  --rpcpass RPCPASS     Crypto wallet password (default: None)
  --rpchost RPCHOST     Crypto wallet hostname (default: localhost)
  --rpcport RPCPORT     Crypto wallet port (default: 22555)
  --start-records-at-one
                        If there are more than 7648 records in DOGE the script will only put the 7,648 most resent transactions in VSAM. This flag reverses that action to store the first 7,648 records (default: True)
```