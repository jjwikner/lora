#!/usr/bin/python3
#!/usr/local/bin/python3.6

import os
import subprocess
import datetime
import time
import sys

from uuid import getnode as get_mac

idTag = 'ID:'

def getmac(interface):
    try:
        mac = open('/sys/class/net/'+interface+'/address').readline()
    except:
        mac = "00:00:00:00:00:00"
    return mac[0:17]

executable = "./dragino_lora_app"
message    = datetime.datetime.now().isoformat()
localMac   = getmac('wlan0')


freq1 = 868100000;
freq2 = 868200000;
freq2 = 868100000;

freqs = [freq1]

# Subfunctions here


ctr = 0;

noInterrupt = True


def loraWaitForCall():
    print("Wait for call")
    message = False
    for freq in freqs:
        # Listen for the response, if an ack is sent back, then that's the shit
        rcvResults = subprocess.run([executable, "rec", str(freq), "single"], stdout=subprocess.PIPE)        
        rcvResults = subprocess.run([executable, "rec", str(freq), "single"], stdout=subprocess.PIPE)
        rcvText    = rcvResults.stdout.decode("utf-8")
        if "Payload:" in rcvText:
            #print(rcvResults.stdout)
            if "ID:" in rcvText:
                msgS = rcvText.find(idTag)+len(idTag)
                msgE = rcvText.find('\n',msgS)
                message = rcvText[msgS:msgE]
                print("Message from {}".format(message))
    return message

def loraSendMessage(runs, message):
    ##
    print("Send message {}".format(message))
    ctr = 0

    while ctr < runs:
        for freq in freqs:
            # Send the messages
            sendResults = subprocess.run([executable, "sender", str(freq), message ], stdout=subprocess.PIPE)
            #print(sendResults.stdout)
        time.sleep(1);
        # Based on contact            
        ctr = ctr + 1

### MAIN

theMessage = False

if len(sys.argv) > 1: # Input argument, if there is an input argument, then start in listen mode.

    print("Start in listen mode")
    while not theMessage:
        theMessage = loraWaitForCall()

    time.sleep(3)
    # send ACK
    print("Received message from {}. Return ACK.".format(theMessage))
    loraSendMessage(4, idTag + localMac + ":ACK")
    
else:

    print("Start in send mode")    
    loraSendMessage(4, idTag + localMac )
    theMessage = False    
    while not theMessage:
        theMessage = loraWaitForCall()


#try:
# keyboardinterrupt
