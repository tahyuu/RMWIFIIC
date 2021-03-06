#!/usr/bin/env python

#from EventManager import *
from Configure import *
from Log import *
import serial
import time
import binascii
import exceptions
import sys
import os
from optparse import OptionParser
import subprocess
import re

class Comm232(serial.Serial):
    def __init__(self, config, log,  serial_port):
	#self.eventManager = eventManager
	#self.eventManager.RegisterListener( self )
	self.log = log
	self.config = config
	self.serial_port = serial_port
	self.verboseFlag = False

	self.PROMPT = self.config.Get('PROMPT')
	self.BOOT_PROMPT = self.config.Get('BOOT_PROMPT')

	cmdStr = '/usr/sbin/lsof ' + serial_port

	#lsopenfile = subprocess.Popen(cmdStr, shell=True, \
	#			      stdout=subprocess.PIPE, \
	#			      stderr=subprocess.PIPE)
	#lsopenfile.wait()
	#result = lsopenfile.communicate()
	#self.CheckPortAvailability(result)
	serial.Serial.__init__(self, \
			#port = self.config.Get('port'), \
			port = self.serial_port, \
			baudrate = self.config.Get('baudrate'), \
			bytesize = eval( self.config.Get('bytesize') ), \
			parity = eval(self.config.Get('parity')), \
			stopbits=eval(self.config.Get('stopbits')), \
			timeout=eval(self.config.Get('timeout')), \
			xonxoff=eval(self.config.Get('xonxoff')), \
			rtscts=eval(self.config.Get('rtscts')))
	#self.ClearCommPort()
	self.RecvFlag = True
	self.PromptState = ''

    def CheckPortAvailability(self, result):
	if len(result[0]):
	    print "Error: %s is occupied by other process" % self.serial_port
	elif len(result[1]):
	    print "Error: %s does not exist" % self.serial_port
	else:
	    return
	sys.exit(1)

    def ClearCommPort(self):
	while True:
	    ch = self.read(1)
            #ch_ascii = binascii.b2a_hex(ch)
	    if ch is '':
		break

    def Send(self, cmdAsciiStr):
	self.write(cmdAsciiStr)

    def SetVerbose(self):
	self.verboseFlag = True

    def UnsetVerbose(self):
	self.verboseFlag = False

    def SendReturn(self, cmdAsciiStr):
	#self.write('\r')
	#self.write('\r')
	for char in cmdAsciiStr:
	    self.write(char)
	self.write('\r')
	if self.log.isOpen():
	    self.log.Print('RS232 Send => ' + cmdAsciiStr)
	self.flush()
	#self.flushOutput()

    def RecvTerminatedBy(self, *prompt_ptr):
	if len(prompt_ptr) == 0:
	    prompt = self.PROMPT
	else:
	    prompt = prompt_ptr[0]
	index = 0
	line = ""
	line2 = ""
	while self.RecvFlag:
	    char = self.read(1)
	    if char is '':
		#print 'RS232 port communication timeout'
		#self.eventManager.Post( CommTimeoutEvent() )
		return 'No response from UUT. please check UUT and RS232 Cable'
	    line = line + char
	    line2 = line2 + char
	    #if self.verboseFlag == True:
	    #    if char == '\n' or char == '\r':
	#	    print
	#        if char != '' and ord(char) > 31 and ord(char) < 127:
	#            if char != '':
	#    	        sys.stdout.write(char)
	#    	        sys.stdout.flush()
	    #if char == '\n' or char == '\r':
	    #    print
	    #if char != '' and ord(char) > 31 and ord(char) < 127:
	    if char == '\n' or char == '\r':
	        sys.stdout.write(line2)
		line2 = ''
	        sys.stdout.flush()
	    if char == prompt[index]:
		index = index + 1 
		if index == len(prompt):
		    break
	    else:
		index = 0
	#line2 = line.replace('\r', '')
	#line3 = line2.replace('\n', ' ')
	#line4 = line.replace('->', '')
	#pattern = re.compile('\W+')
	#line5 = pattern.sub(' ', line4)
	if self.log.isOpen():
	    self.log.Print('RS232 Recv <= ' + line)
	return line

    def WaitForBootPrompt(self):
	timeout = self.getTimeout()
	#self.setTimeout(10)
	line = ''
	for i in range(20):
	    #self.Send('\r')
	    #line = line + self.read(2000)
	    line = self.read(20)
	    self.log.PrintNoTime(line)
	    if line.find(self.BOOT_PROMPT) >= 0: 
        	#self.setTimeout(timeout)
		return line
	#self.eventManager.Post( CommTimeoutEvent() )
	return 'FAIL'

    def EnterCmdPrompt(self):
	timeout = self.getTimeout()
        self.setTimeout(1)
	self.Send('\r')
	line = self.RecvTerminatedBy()
        self.setTimeout(timeout)
	self.PromptState = 'LSI_PROMPT'

    def EnterMfgCmdPrompt(self):
	timeout = self.getTimeout()
        self.setTimeout(1)
	self.Send('\r')
	line = self.read(2000)
	if line.find(self.PROMPT) >= 0:
	    self.SendReturn('mfg')
	    line = self.RecvTerminatedBy(self.MFG_PROMPT)
        self.setTimeout(timeout)
	self.PromptState = 'FLEX_PROMPT'

    def Notify(self, event):
	if isinstance( event, CommTimeoutEvent ):
	    print "Comm Notify called"
	    #self.RecvFlag = False
	    #sys.exit(1)

if __name__ == "__main__":
    parser = OptionParser(usage="usage: %prog [option] serial_port "
			        "(ttyUSB0 or ttyS0)",
			  version="0.1")
    parser.add_option("-t", "--timeout", \
		      action="store", \
		      dest="timeout", \
		      default="60", \
		      help="timeout specifies how much time to wait for \
			    Badger message")

    (options, args) = parser.parse_args()

    if len(args) != 1:
	parser.error("wrong number of arguments")
	sys.exit(1)
    else:
	serial_port = '' + args[0]

    home_dir = os.environ['HOME']	    
    #eventManager = EventManager()
    config = Configure('Config.txt')
    log = Log()
    log.Open('test.log')
    Comm = Comm232(config, log, serial_port)
    Comm.setPort(serial_port)
    Comm.setTimeout(int(options.timeout))

    #time.sleep(3)

    #Comm.WaitForBootPrompt() 

    if Comm.RecvFlag == False:
	sys.exit(3)

    #Comm.EnterCmdPrompt()
    #log.Print( 'Comm port time out is %d' % Comm.getTimeout() )

    num = 0
    #Comm.SendReturn('lspci')
    line = Comm.RecvTerminatedBy('~]#')
    print line

    Comm.close()
    log.Close()
