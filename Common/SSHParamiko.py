#!/usr/bin/python 
from Log import *
import paramiko
import threading
from Comm import *

class SSHParamiko(Comm):
    def __init__(self,log):
	Comm.__init__(self)
	self.status="CLOSED"
        self.log=log
	#self.connect(5)
	#pass
    def connect(self,timeout):
	try:
	    ##username= self.config.Get("username")
	    ##password= self.config.Get("password")
	    ##ipaddress= self.config.Get("ipaddress")
	    username= 'root'
	    password= 'hell05a'
	    ipaddress= '192.168.0.1'
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(ipaddress,22,username,password,timeout=timeout)
	    self.status="OPEN"
        except :
	    self.log.Print("Connect to UUT Fail. please check the connection")
            #print '\tError\n'
    def SendReturn(self, cmdAsciiStr):
	self.command=cmdAsciiStr
        #print "ROOT> %s" %cmdAsciiStr
	self.log.Print("\t%s" %cmdAsciiStr)
	#if True:
    def RecvTerminatedBy(self, *prompt_ptr):
	#if True:
        try:
	    if self.status=="CLOSED" or (not self.ssh):
		self.connect(5)
            stdin, stdout, stderr = self.ssh.exec_command(self.command)
            out = stdout.readlines()
            ret_str=""
            for o in out:
	    	self.log.PrintNoTimeWithoutReturn(o)
	    	ret_str=ret_str+o
                #print o,
                
            return ret_str
        except :
            self.log.PrintNoTimeWithoutReturn("Excute command Error")
            return 'Excute command Error'
    def setTimeout(self,timeout):
	#print "will set timeout to %s s" %timeout
	if self.status=="OPEN":
	    self.close()
	self.connect(timeout)
    def close(self):
        self.ssh.close()
	self.status="CLOSED"
    
if __name__=='__main__':

    #home_dir = os.environ['FT']	    
    #config = Configure(home_dir + '/FTConfig.txt')
    config = Configure('SFTConfig.txt')
    log = Log()
    log.Open('test.log')
    sshtest = SSHParamiko()
    sshtest.log=log
    sshtest.SendReturn('lspci -vvn')
    sshtest.RecvTerminatedBy()
    sshtest.close()
    sshtest.SendReturn('pwd')
    sshtest.RecvTerminatedBy()
    sshtest.setTimeout(10)
    sshtest.SendReturn('cd ..')
    sshtest.RecvTerminatedBy()
    sshtest.close()
    sshtest.SendReturn('pwd')
    sshtest.RecvTerminatedBy()
