#!/usr/bin/python3

import os, sys
import subprocess as sp

SERVER_ADDR = "root@10.227.14.177"

def _command(cmd):
    LOG_FILE = "/tmp/command.log"
    new_cmd = cmd + " > " + LOG_FILE
    os.system(new_cmd + " > " + LOG_FILE)
    output = open(LOG_FILE).read()
    return output

def command(cmd):
    print ("cmd:" + cmd)
    output = sp.getoutput(cmd)
    print("output:\n" + output)
    return output

def ssh_command(cmd):
    new_cmd = "ssh " + SERVER_ADDR + " '" + cmd + "'"
    return command(new_cmd)

def rdmsr(reg):
    cmd = "rdmsr " + reg
    return ssh_command(cmd)

def wrmsr(reg, value):
    cmd = "wrmsr " + reg + ' ' + value
    return ssh_command(cmd)

