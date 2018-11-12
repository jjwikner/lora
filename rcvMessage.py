#!/usr/bin/python3

import os
from subprocess import call
import datetime

print("Hej!")

fileName = "./dragino_lora_app"

message = "abcdefghijklmnopqrstuwvxyz0123456789";
message = datetime.datetime.now().isoformat()
freq1 = 868100000;
freq2 = 868200000;

freqs = [freq1, freq2]

for freq in freqs:
    call([fileName, "rec", str(freq), "single"])


