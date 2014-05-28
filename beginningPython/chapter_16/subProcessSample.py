#!/usr/bin/python
import subprocess

receive = subprocess.Popen('./subProcessSampleChild.py', \
        stdin = subprocess.PIPE)
        #stdout = subprocess.PIPE)
receive.stdin.write('azhe')
