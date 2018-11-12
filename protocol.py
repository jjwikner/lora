#!/usr/bin/python3

import os
import subprocess
import datetime
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

freqs = [freq1, freq2]

# Subfunctions here


ctr = 0;

while ctr < 10:
    
    for freq in freqs:
        # Send the messages
        print('Sending at {}'.format(freq))
        sendResults = subprocess.run([executable, "sender", str(freq), "NODE ID:"+ mac ], stdout=subprocess.PIPE)
        # print(sendResults.stdout)

    for freq in freqs:
        # Listen for the response, if an ack is sent back, then that's the shit
        rcvResults = subprocess.run([executable, "rec", str(freq), "single"], stdout=subprocess.PIPE)        
        if "Payload:" in rcvResults.stdout.decode("utf-8"): 
            print("Someone did something");
            print(rcvResults.stdout)
            if "NODE ID:" in rcvResults.stdout.decode("utf-8"): # Check here if message is for you.
                print("Contact with master")

    # Based on contact
    
            
    ctr = ctr+1

