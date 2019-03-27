#!/usr/bin/env python

import time
import sys
sys.path.append("../../../")
from Common.TestBase import *

class USBTest(TestBase):
    def __init__(self):
        self.section_str="USB Test"
        self.commType="SSHParamiko"
        TestBase.__init__(self)
    def Run(self):
        self.log.Print("###################################################################################################")
        self.log.Print("Sectioin: %s" %self.section_str)
        self.log.Print("###################################################################################################")
        #list usb
        self.log.Print(" ###  list usb ###")
        self.com.SendReturn('cat /proc/partitions')
        time.sleep(0.2)
        line=self.com.RecvTerminatedBy()
        print line
##        line=self.com.RecvTerminatedBy()
##        #umount /mnt/&mount /dev/sda1 /mnt/
##        self.log.Print(" ###   umount  usb ###")
##        self.com.SendReturn('umount /mnt/&mount /dev/sda1 /mnt/')
##        line=self.com.RecvTerminatedBy()
##
##        self.com.SendReturn('rm /boot/Image_test&rm /media/Imag')
##        line=self.com.RecvTerminatedBy()
##
##        self.com.SendReturn('md5sum /boot/Imag')
##        line=self.com.RecvTerminatedBy()
##
##        self.com.SendReturn('md5sum /boot/Imag')
##        line=self.com.RecvTerminatedBy()
##        print line
##        #self.log.Print(line)
##        print line
##        #self.failIf(False,"Just a sameple test%siiiiiiiiiiii")
        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        print line
        passFlag=line.find("boot0")>=0
        print "Flag is %s " %passFlag
        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

        self.passIf(passFlag,"USb Can Be found Test")
        #return "PASS"

if __name__=="__main__":
    led= USBTest()
    led.log.Open('test.log')
    print led.Run()
