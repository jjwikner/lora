#!/usr/bin/python3

import os
import subprocess
import datetime
import time
import sys

from uuid import getnode as get_mac

def getmac(interface):
    try:
        mac = open('/sys/class/net/'+interface+'/address').readline()
    except:
        mac = "00:00:00:00:00:00"
    return mac[0:17]

executable = "./dragino_lora_app"
message = datetime.datetime.now().isoformat()
mac = getmac('wlan0')


freq1 = 868100000;
freq2 = 868200000;
freq2 = 868100000;

freqs = [freq1]

# Subfunctions here


ctr = 0;

noInterrupt = True


def loraWaitForCall():
    message = False
    for freq in freqs:
        # Listen for the response, if an ack is sent back, then that's the shit
        rcvResults = subprocess.run([executable, "rec", str(freq), "single"], stdout=subprocess.PIPE)        
        rcvResults = subprocess.run([executable, "rec", str(freq), "single"], stdout=subprocess.PIPE)
        rcvText    = rcvResults.stdout.decode("utf-8")
        if "Payload:" in rcvText:
            print(rcvResults.stdout)
            if "NODE ID:" in rcvText:
                msgS = rcvText.find('NODE ID:')+8
                msgE = rcvText.find('\n',msgS)
                message = rcvText[msgS:msgE]
                print("Message from {}".format(message))
    return message

def loraSendSignal(runs, message):
    ctr = 0
    while ctr < runs:
        print("MM{}".format(freqs))
        for freq in freqs:
            # Send the messages
            sendResults = subprocess.run([executable, "sender", str(freq), message ], stdout=subprocess.PIPE)
            print(sendResults.stdout)

        time.sleep(2);
        # Based on contact            
        ctr = ctr + 1


### MAIN

theMessage = False

if len(sys.argv) > 1: # Input argument

    while not theMessage:
        theMessage = loraWaitForCall()

    # send ACK
    print("Send ACK")

    loraSendSignal(10, theMessage + ":ACK")

else:

    loraSendSignal(10, "NODE ID:"+mac)

    theMessage = False
    
    while not theMessage:
        theMessage = loraWaitForCall()

    

