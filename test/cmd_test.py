#!/usr/bin/python3

import utils
import os, time

while(True):
    result = utils.ssh_command("rdmsr 0x621")
    print("Uncore")
    print(result)

    result = utils.ssh_command("rdmsr 0x198")
    print("Core")
    print(result)
    time.sleep(1)
