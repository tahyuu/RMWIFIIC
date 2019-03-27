#!/usr/bin/env python
import time
import sys

class Power():
    def __init__(self):
        pass
    def PowerOn(self):
        for i in xrange(1):
            #sys.stdout.write("..")
            #sys.stdout.flush()
            time.sleep(1)
        #print
    def PowerOFF(self):
        for i in xrange(1):
            #sys.stdout.write("..")
            #sys.stdout.flush()
            time.sleep(1)
        #print



if __name__=="__main__":
    led= Power()
    led.On()
