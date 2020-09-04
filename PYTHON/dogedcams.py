#!/usr/bin/python3

# Python script to upload cryptocurrency wallet info to a VSAM file
# Author: Soldier of FORTRAN
# Version: 1.0
# License: GPL

# Interesting resources:
# https://idiotmainframe.blogspot.com/2019/07/design-bms.html
# http://www.transvec.com/cics/

import sys
import os
import socket
import requests
import json
import configparser
import datetime
import logging
import argparse
import os.path
import time
from pprint import pprint
from os import path
from decimal import Decimal
import random

tmp_file = "doge.tmp"
running_folder = os.path.dirname(os.path.abspath(__file__))

IEFBR14 = '''//DOGEBR14 JOB CLASS=C,MSGCLASS=Z,MSGLEVEL=(1,1),
//*        NOTIFY={user},
//        USER={user},PASSWORD={password}
//DOGELOL EXEC PGM=IEFBR14''' 

IDCAMS = '''//DOGEVSM JOB (BAL),
//             'DOGEBANK VSAM',
//             CLASS=A,
//             MSGCLASS=Z,
//             TIME=1440,
//             MSGLEVEL=(1,1),
//*             NOTIFY={user},
//             USER={user},PASSWORD={password}
//DOGECAMS EXEC PGM=IDCAMS
//SYSPRINT DD   SYSOUT=*
//INDATA1  DD *
{records}
/*                                                                     
//SYSIN    DD *                                                        
 DELETE {vsam_file} CLUSTER PURGE
 /* IF THERE WAS NO DATASET TO DELETE, RESET CC           */
 IF LASTCC = 8 THEN
   DO
       SET LASTCC = 0
       SET MAXCC = 0
   END
 /* Create VSAM Key based */
 DEFINE CLUSTER (                    -
        NAME( {vsam_file} )          -
        VOLUME( {volume} )           -
        INDEXED                      -
        KEYS( 10,0 )                 -
        RECORDSIZE ( 80,80 )         -
        RECORDS( 500 )               -
        UNIQUE                       -
        ) -
        DATA ( NAME({vsam_file}.DATA)) -
        INDEX ( NAME({vsam_file}.INDEX))
                                                                      
 /* PUT THE DATA IN THE FILE */                                        
 IF LASTCC=0 THEN                    -                                 
     REPRO INFILE(INDATA1)           -                                 
     OUTDATASET({vsam_file})                                       
 IF LASTCC=0 THEN                    -                                 
     LISTCAT ALL ENTRY({vsam_file})                                
/*'''


def generate_fake_records(number_of_records=100):
    ''' Generates fake records JCL '''
    fake_labels = ['CIBC', 'DOGE Bank LLC', 'SUCH FUNDS', 'WOW MONEY','Fake','Banco do Brazil','Kraken','MTGOX']
    logger.debug("Generating {} fake records.".format(number_of_records))
    record = "{key:010d} {address:<034} {label:<10.10} {amount:+018.8f}"
    records = []
    records.append(record.format(key=1,address=0,label="Available", amount=+87654321.12345678))
    records.append(record.format(key=2,address=0,label="Pending", amount=-123456.654321))

    for i in range(1,int(number_of_records)):
        records.append(record.format(key=random.randint(1000000000,int(time.time())),address="nYLEKeZtqNSCAhMNKTFpFgZcnvf1DbFiSu",label=fake_labels[random.randint(0,7)], amount=random.uniform(-10000000,10000000)))

    records.append(record.format(key=9999999999,address='0',amount=0,label='Control Record'))
    records.sort()
    return records



def get_records(host='localhost', rpcUser=None, rpcPass=None, rpcPort=22555):
    ''' Gets DOGECOIN records from dogecoin RPC server '''
    

    try:
        with open(path.join(path.expanduser("~"), '.dogecoin', 'dogecoin.conf'), mode='r') as f:
            config_string = '[dogecoin]\n' + f.read()
    except:
        config_string = None
    
    config = configparser.ConfigParser()
    config.read_string(config_string)

    if not rpcUser and 'rpcuser' in config['dogecoin']:
        rpcUser = config['dogecoin']['rpcuser']
            
    if not rpcPass and 'rpcpassword' in config['dogecoin']:
        rpcPass = config['dogecoin']['rpcpassword']
    
    if rpcUser is None or rpcPass is None:
        logger.critical("rpcuser or rpcPass not in .dogecoin/dogecoin.conf and not passed to function")
        sys.exit(-1)

    serverURL = 'http://{user}:{passw}@{host}:{port}'.format(user=rpcUser,passw=rpcPass,host=host,port=rpcPort)
    serverPrint = 'http://{user}:{passw}@{host}:{port}'.format(user=rpcUser,passw=('*' * len(rpcPass)),host=host,port=rpcPort)

    logger.debug("Connecting to {}".format(serverPrint))
    
    headers = {'content-type': 'application/json'}

    record = "{key:010d} {address:<034} {label:<10.10} {amount:+018.8f}"
    records = []

    logger.debug("Getting current balance")
    try:
        payload = json.dumps({"method": 'getbalance', "params": [], "jsonrpc": "1.0"})
        balance = requests.post(serverURL, headers=headers, data=payload, timeout=10).json()['result']
        records.append(record.format(key=1,address=0,label="Available", amount=balance))
        logger.debug("Adding the following record: {}".format(record.format(key=1,address=0,label="Available", amount=balance)))

    except ValueError:
        logger.critical("Invalid Logon using {}".format(serverURL))
        sys.exit(-1)
    
    except requests.exceptions.ConnectTimeout:
        logger.critical("Could not connect to {}".format(serverURL))
        sys.exit(-1)
    logger.debug("Current balance {}".format(balance))

    logger.debug("Getting current unconfirmed balance")

    payload = json.dumps({"method": 'getunconfirmedbalance', "params": [], "jsonrpc": "1.0"})
    pending = requests.post(serverURL, headers=headers, data=payload).json()['result']
    records.append(record.format(key=2,address=0,label="Pending", amount=pending))
    logger.debug("Adding the following record: {}".format(record.format(key=2,address=0,label="Pending", amount=pending)))

    logger.debug("Current unconfirmed balance {}".format(pending))

    logger.debug("Getting all transactions")

    payload = json.dumps({"method": 'listtransactions', "params": [], "jsonrpc": "1.0"})
    recent  = requests.post(serverURL, headers=headers, data=payload).json()['result']
    logger.debug("Total records from wallet: {}".format(len(recent)))
    for activity in recent:
        key = activity['timereceived']
        address = activity['address']
        amount = activity['amount']
        try:
            label = activity['label']
        except:
            label = ''
        dup = False
        for x in records:
            if str(key) in x:
                dup = True
        if not dup:
            logger.debug("Adding the following record: {}".format(record.format(key=key,address=address,amount=amount,label=label)))
            records.append(record.format(key=key,address=address,amount=amount,label=label))
        else:
            logger.debug("Duplicate record! No insert: {}".format(record.format(key=key,address=address,amount=amount,label=label)))

    records.append(record.format(key=9999999999,address='0',amount=0,label='Control Record'))
    logger.debug("Adding the following record: {}".format(record.format(key=9999999999,address='0',amount=0,label='Control Record')))
    logger.debug("Total records being sent (including balance, pending and control record): {}".format(len(records)))
    return records

def test(user='DOGE', password='DOGECOIN',target='localhost', port=3505):
    ''' send IEFBR14 job to hercules sockdev '''
    logger.debug("Sending IEFBR14 to {}:{}".format(target,port))
    send_jcl(hostname=target, port=port, jcl=IEFBR14.format(user=user,password=password))

def test_print(user='DOGE', password='DOGECOIN',target='localhost', port=3505):
    ''' send IEFBR14 job to hercules sockdev '''
    print(IEFBR14.format(user=user,password=password))

def send_jcl(hostname='localhost',port=3505, jcl="", print_jcl=False):
    logger.debug("Sending VSAM update JCL to tk4- reader using {}:{}".format(hostname,port))
    if print_jcl:
        print("PRINTING JCL:\n{}\n{}\n{}\n".format('-'*80,jcl, '-'*80))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname,port))
    s.sendall(jcl.encode())
    s.close()

def generate_IDCAMS_JCL(user='herc01',password='cul8tr',vsam_file='DOGE.VSAM',records='', volume='pub012', reverse=True):

    if len(records) > 7648:
        if reverse:
            logger.debug("Records exceeds maximum records length of 7648. Getting last 7648 records. To get first 7648 records use --start-records-at-one")
            record0000000001 = records[0]
            record0000000002 = records[1]
            records = records[-7648:]
            records[0] = record0000000001
            records[1] = record0000000002
        else:
            logger.debug("Records exceeds maximum records length of 7648. Getting first 7648 records because --start-records-at-one was passed to script")
            record9999999999 = records[-1]
            records = records[:7648]
            records[-1] = record9999999999

    user = user.upper()
    password = password.upper()
    volume = volume.upper()
    vsam_file = vsam_file.upper()
    logger.debug("Generating IDCAMS JCL with the following options: user: {user} password: {password} vsam_file: {vsam_file} volume: {volume}".format(user=user,password=password,vsam_file=vsam_file,volume=volume))
    return IDCAMS.format(user=user,password=password,vsam_file=vsam_file,records='\n'.join(records),volume=volume)

def new_records(old_records, new_records):
    if old_records == new_records:
        logger.debug("no new records, update not required, force update with --force".format(running_folder,tmp_file))
        return False
    else:
        logger.debug("new records in wallet, sending update")
        return True

def get_commands(timeout=2, hostname='localhost', port=3506):
# From https://www.binarytides.com/receive-full-data-with-the-recv-socket-function-in-python/
    
    logger.debug('Connecting to tk4- printer {}:{} to get transactions.'.format(hostname,port))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname,port))
    s.setblocking(0)

    total_data=[]
    data=''
    begin=time.time()

    while 1:
        if total_data and time.time()-begin > timeout:
            break
        elif time.time()-begin > timeout*2:
            break
        
        try:
            data = s.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass
    
    doge_send = []
    for line in total_data:
        address = False
        amount = False
        if 'DOGECICS99' in line.decode():
            logger.debug('Found DOGECICS transaction: {}'.format(line.decode()))
            if len(line.decode().split()) == 3:
                address = line.decode().split()[1]
                amount = line.decode().split()[2]
                logger.debug('Correct record entry appending {} {}'.format(address, amount))
            doge_send.append({'address' : address, 'amount' : amount})
    return doge_send
    
def send_doge(address, amount=0, host='localhost', rpcUser=None, rpcPass=None, rpcPort=22555):
    ''' Sends amount of dogecoin to address '''
    logger.debug('Connecting to {}:{} to send {} to {}'.format(host,rpcPort, amount, address))

    try:
        with open(path.join(path.expanduser("~"), '.dogecoin', 'dogecoin.conf'), mode='r') as f:
            config_string = '[dogecoin]\n' + f.read()
    except:
        config_string = None
    
    config = configparser.ConfigParser()
    config.read_string(config_string)

    if not rpcUser and 'rpcuser' in config['dogecoin']:
        rpcUser = config['dogecoin']['rpcuser']
            
    if not rpcPass and 'rpcpassword' in config['dogecoin']:
        rpcPass = config['dogecoin']['rpcpassword']
    
    if rpcUser is None or rpcPass is None:
        logger.critical("rpcuser or rpcPass not in .dogecoin/dogecoin.conf and not passed to function")
        sys.exit(-1)

    serverURL = 'http://{user}:{passw}@{host}:{port}'.format(user=rpcUser,passw=rpcPass,host=host,port=rpcPort)
    serverPrint = 'http://{user}:{passw}@{host}:{port}'.format(user=rpcUser,passw=('*' * len(rpcPass)),host=host,port=rpcPort)

    logger.debug("Connecting to {}".format(serverPrint))
    
    headers = {'content-type': 'application/json'}

    logger.debug("Sending {} to {}".format(amount, address))
    try:
        payload = json.dumps({"method": 'sendtoaddress', "params": [address, amount], "jsonrpc": "1.0"})
        reply = requests.post(serverURL, headers=headers, data=payload, timeout=10).json()
        r = reply['result']
    except ValueError:
        logger.critical("Invalid Logon using {}".format(serverURL))
        sys.exit(-1)
    except requests.exceptions.ConnectTimeout:
        logger.critical("Could not connect to {}".format(serverURL))
        sys.exit(-1)
    logger.debug("Reply from dogecoin wallet: {}".format(r))

desc = '''DOGEdcams data generator for DOGE Bank. Used to send and receive funds between KICKS on TK4- and DogeCICS.'''
arg_parser = argparse.ArgumentParser(description=desc, 
                    usage='%(prog)s [options]', 
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
arg_parser.add_argument('-d', '--debug', help="Print lots of debugging statements", action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.WARNING)
arg_parser.add_argument('-t', '--test', help="Test sending JCL to TK4-", action="store_true")
arg_parser.add_argument('-p', '--print', help="Print JCL being sent to TK4", action="store_true")
arg_parser.add_argument('-f', '--force', help="Force VSAM update even if no changes to wallet", action="store_true")
arg_parser.add_argument('--fake', help="Generate fake records", default=None)
arg_parser.add_argument('--username', help="TK4- username for JCL", default='herc01')
arg_parser.add_argument('--password', help="TK4- password for JCL", default='cul8tr')
arg_parser.add_argument('--vsam_file', help="TK4- VSAM file used by dogekicks", default='DOGE.VSAM')
arg_parser.add_argument('--volume', help="TK4- volume to store VSAM file", default='pub012')
arg_parser.add_argument('--rdrport', help="TK4- Reader sockdev port", default=3505)
arg_parser.add_argument('--prtport', help="TK4- Printer sockdev port", default=3506)
arg_parser.add_argument('--hostname',  help="TK4- sockdev host", default="localhost")
arg_parser.add_argument('--rpcuser', help="Crypto wallet username", default=None)
arg_parser.add_argument('--rpcpass', help="Crypto wallet password", default=None)
arg_parser.add_argument('--rpchost', help="Crypto wallet hostname", default="localhost")
arg_parser.add_argument('--rpcport', help="Crypto wallet port", default="22555")
arg_parser.add_argument('--start-records-at-one', help="If there are more than 7648 records in DOGE the script will only put the 7,648 most resent transactions in VSAM. This flag reverses that action to store the first 7,648 records", action="store_false")
args = arg_parser.parse_args()	

# Create the Logger
logger = logging.getLogger(__name__)
logger.setLevel(args.loglevel)
logger_formatter = logging.Formatter('%(levelname)-8s :: %(funcName)-22s :: %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(logger_formatter)
ch.setLevel(args.loglevel)
logger.addHandler(ch)

# Print debug information
logger.debug("Using the following script options - Debug: True, Test: {}, Print: {}, Force: {}".format(args.test, args.print, args.force))
logger.debug("Using the following TK4- options - Hostname: {}, Username: {}, Password: {}, VSAM File: {}, Volume: {}, Reader Port: {}, Printer Port: {}".format(
            args.hostname, args.username, "*"*len(args.password), args.vsam_file, args.volume, args.rdrport, args.prtport))
logger.debug("Using the following Dogecoin options - RPC Host: {}, RPC User: {}, RPC Pass: {} RPC Port: {}".format(
            args.rpchost, args.rpcuser, "*"*len(args.rpchost), args.rpcport))
if args.test:
    logger.debug("Test mode enabled, not getting transactions from TK4- Queue")
if args.fake:
    logger.debug("Generating {} fake records.".format(args.fake))

# Get records from dogecoind, check if there's any new ones, create new VSAM file
if not args.fake:
    vsam_records = get_records(host=args.rpchost, rpcUser=args.rpcuser, rpcPass=args.rpcpass, rpcPort=args.rpcport)
else:
    vsam_records = generate_fake_records(number_of_records = int(args.fake))

doge_vsam_jcl = generate_IDCAMS_JCL(user=args.username,password=args.password,vsam_file=args.vsam_file,volume=args.volume,records=vsam_records, reverse=args.start_records_at_one)


if not os.path.isfile("{}/{}".format(running_folder,tmp_file)) or args.force:
    # If the tmp file doesn't exist or we need to force an update for some reason
    if not os.path.isfile("{}/{}".format(running_folder,tmp_file)):
        logger.debug("temp file {}/{} does not exist, creating".format(running_folder,tmp_file))
    else:
        logger.debug("forced update")
    
    if not args.test:
        send_jcl(hostname=args.hostname,port=args.rdrport, jcl=doge_vsam_jcl, print_jcl=args.print)
        logger.debug("creating: {}/{}".format(running_folder,tmp_file) )
        with open("{}/{}".format(running_folder,tmp_file), "w") as records_file:
            records_file.write('\n'.join(vsam_records))
    else:
        print("TEST MODE printing Doge records and JCL")
        print(doge_vsam_jcl)
else:
    # we've already uploaded a file, do we have new records?
    with open("{}/{}".format(running_folder,tmp_file), "r") as records_file:
        tmp = records_file.read()
    if new_records(tmp, '\n'.join(vsam_records)):
        if not args.test:
            send_jcl(hostname=args.hostname,port=args.rdrport, jcl=doge_vsam_jcl, print_jcl=args.print)
            logger.debug("updating: {}/{}".format(running_folder,tmp_file) )
            with open("{}/{}".format(running_folder,tmp_file), "w") as records_file:
                records_file.write('\n'.join(vsam_records))
        else:
            print("Test mode, new records found, printing JCL and old records")
            print("OLD RECORDS: \n{}".format(tmp))
            print("NEW RECORDS: \n{}".format('\n'.join(vsam_records)))
            print("JCL:\n{}".format(doge_vsam_jcl))
            

# Check if there's data on the printer queue, Process the entries, Send to dogecoind server
if not args.test:
    logger.debug("Getting records from tk4- Class D")
    sending = get_commands()
    if len(sending) < 1:
        logger.debug("Nothing to perform, exiting")
    for line in sending:
        logger.debug("Recieved Address: {} Amount: {}".format(line['amount'], line['address']))
        if line['amount'] and line['address']:
            m = str(Decimal(float(line['amount'].replace(',',''))).quantize(Decimal('1.00000000')))
            logger.debug("Sending {} to {}".format(m,line['address']))
            if not args.fake:
                send_doge(address=line['address'], amount=m, host=args.rpchost, rpcUser=args.rpcuser, rpcPass=args.rpcpass, rpcPort=args.rpcport)
            else:
                logger.debug("Fake Mode Enabled, not sending transactions printing to terminal")
                print("Fake Mode Send: {} {}".format(line['address'], m))
            # TODO: Refresh the VSAM file after we send this transaction.
        else:
            logger.debug("Address incorrect or amount missing. Not sending".format())
    

