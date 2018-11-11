#!/usr/bin/python3

import os
from subprocess import call
import datetime

print("Hej!")

fileName = "./dragino_lora_app"

message = "abcdefghijklmnopqrstuwvxyz0123456789";
message = datetime.datetime.now().isoformat()

call([fileName, "sender", message])

// Added a comment-line to test the chain between them.
