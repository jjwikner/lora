#!/usr/bin/python3

import os
from subprocess import call
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

call([executable, "sender", str(freq1), message])
call([executable, "sender", str(freq1), "NODE ID: "+ mac ])

call([executable, "sender", str(freq2), message])
call([executable, "sender", str(freq2), "NODE ID: "+ mac ])


