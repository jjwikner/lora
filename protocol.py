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

ctr = 0;
while ctr < 10:
    
    for freq in freqs:
        # Send the messages
        print('Sending at {}'.format(freq))
        sendResults = subprocess.run([executable, "sender", str(freq), "NODE ID: "+ mac ], stdout=subprocess.PIPE)
        # print(sendResults.stdout)

    for freq in freqs:
        # Listen for response
        rcvResults = subprocess.run([executable, "rec", str(freq), "single"], stdout=subprocess.PIPE)        
        if "Payload:" in rcvResults.stdout.decode("utf-8"): 
            print("Someone did something");
            print(rcvResults.stdout)
            
    ctr = ctr+1

