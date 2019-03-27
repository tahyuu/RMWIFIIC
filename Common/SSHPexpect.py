#!/usr/bin/env python
#-*-coding:utf-8-*-
# date:2016-6-21
# author:root

import sys
from EventManager import *
from Configure import *
from Log import *
if 'linux' in sys.platform:
    my_os = 'linux'
    from  pexpect import *
elif 'win32' in sys.platform:
    my_os = 'win32'
    from  winpexpect import *
import optparse
from Comm import *


class SSHPexpect(Comm):
    def __init__(self,log):
	Comm.__init__(self)
	self.status="CLOSED"
	self.connect(5)
        self.log=log
    def connect(self,timeout):
#	username= self.config.Get("username")
#	password= self.config.Get("password")
#	ipaddress= self.config.Get("ipaddress")
	username= 'root'
	password= 'hell05a'
	ipaddress= '192.168.0.1'
        if my_os=='win32':
	    self.child = winspawn('ssh -o StrictHostKeyChecking=no %s@%s' %(username,ipaddress), timeout=timeout)
        elif my_os=='linux':
	    self.child = spawn('ssh -o StrictHostKeyChecking=no %s@%s' %(username,ipaddress), timeout=timeout)
	print self.child.before
	self.child.expect('password:')
	self.child.sendline(password)
	self.child.expect(']#')
    def SendReturn(self, cmdAsciiStr):
	if self.status=="CLOSED":
		self.connect(5)
		self.status="OPEN"
	self.log.Print("]# %s" %cmdAsciiStr+"\n")
	print "]# %s" %cmdAsciiStr
	self.child.sendline(cmdAsciiStr)

    def setTimeout(self,timeout):
	print "will set timeout to %s s" %timeout
	if self.status=="OPEN":
	    self.close()
	self.connect(timeout)

    def RecvTerminatedBy(self, *prompt_ptr):
	self.child.expect(']#')
	print self.child.before
	self.log.PrintNoTimeWithoutReturn(self.child.before)
    def close(self):
        pass
	


if __name__=="__main__":
    #home_dir = os.environ['FT']	    
    #config = Configure(home_dir + '/SFTConfig.txt')
    config = Configure('SFTConfig.txt')
    log = Log()
    log.Open('test.log')
    sshtest = SSHPexpect(config, log)
    sshtest.SendReturn('lspci -vvn')
    sshtest.RecvTerminatedBy()
    sshtest.setTimeout(60)
    sshtest.SendReturn('lspci -vvn')
    sshtest.RecvTerminatedBy()
    sshtest.SendReturn('cd ..')
    sshtest.RecvTerminatedBy()
    sshtest.SendReturn('pwd')
    sshtest.RecvTerminatedBy()


