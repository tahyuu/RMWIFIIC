# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from Ui_main import Ui_MainWindow
#from testEngine import *
#from barcodedlg import *
from MtsInt_StationConfig import *
#from loadnewprogramdlg import *
import time
import datetime
import multiprocessing
from m_TestSocket import *
from m_TestUUT import *
from TSLEngine import *
#from IVMMTestEngine import *
#from TestEngine import *
from MulPools import * 

# this whole class is just another reference
class Worker (QThread):
    daemonIsRunning = False
    daemonStopSignal = False
    daemonCurrentDelay = 0

    def isDaemonRunning (self): return self.daemonIsRunning
    def setDaemonStopSignal (self, bool): self.daemonStopSignal = bool

    def __init__ (self, parent = None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.thread_to_run = None  # which def will be running
	self.TSLfile = str(StationOptions["TestProgram"]).replace(".py","")
        self.tslCreated = False
	self.UI=parent
	#self.TSLfile = "Borin_Test.py"
	#self.mp =MulPools(1)


    #Create a List to store all uuts test results

    #init m_ResultsList 
    	self.manager = multiprocessing.Manager()
	self.testUUTs= self.manager.list()
	#self.testUUTs= []
	self.testsockets= []
	self.testlogfiles=[]
	self.snList = []
	self.m_TSLfile=__import__(str(self.TSLfile))
	#self.testEngine=TSLEngine(self.m_TSLfile.Main,self)
        #print "in worker ......."
        #print self.m_TSLfile.Main
	self.testEngine=TSLEngine(self.m_TSLfile.Main,self)
	#self.testEngine=TestEngine(self)
	#self.testEngine=IVMMTestEngine(self)
    def __del__ (self):
        self.exiting = True
        self.thread_to_run = None
        self.wait()

    def run (self):
        if self.thread_to_run != None:
            self.thread_to_run(mode='continue')

    def stopDaemon(self):
	#"multi_pool stoped"
	#self.testEngine.multi_pool.terminate()
	#self.testEngine.mp.Stop()
	self.daemonStopSignal=True
	#set the daemonStopSignal to 1
	if mutex.acquire():
		daemonStopSignal.value =1
		mutex.release()
	#"multi_pool stoped"

    def startDaemon (self, mode = 'run', ):
	#set the daemonStopSignal to 0
	global daemonStopSignal,mutex
	if mutex.acquire():
		daemonStopSignal.value =0
		mutex.release()

	startTime = time.time()
        if mode == 'run':
            self.thread_to_run = self.startDaemon # I'd love to be able to just pass this as an argument on start() below
            return self.start() # this will begin the thread

        # this is where the thread actually begins
        self.daemonIsRunning = True

        self.daemonStopSignal = False
        sleepStep = 0.1 # don't know how to interrupt while sleeping - so the less sleepStep, the faster StopSignal will work
	i=0
	
#	while self.daemonStopSignal == False and not self.exiting and i<self.testCount:
	
	if self.daemonStopSignal == False and not self.exiting:


		print "thread starting"

		self.m_TSLfile=__import__(str(self.TSLfile))

		#start 2012-12-28 
		#self.testEngine.createTests()
		#self.testEngine.createTests()
                if  not self.tslCreated:
                    #print "create tsl .................................. create tsl"
		    self.testEngine.CreateTSL(Main)
                    self.tslCreated = True

		#self.testEngine.createPool()
		for sn in self.snList:
			if sn:
				testUUT = TestUUT(i)
				testUUT.sN = sn
				testUUT.testCount= self.testEngine.testCount
				self.testUUTs.append(testUUT)
			i = i  +  1
		#init the test Engine
		#self.testEngine=TSLEngine(self.m_TSLfile.Main,self)
		#self.testEngine=IVMMTestEngine(self)
		#run test Engine
		#if self.UI.testType=="single":
		#	self.testEngine.
		#self.testEngine.run()
		self.testEngine.RunTest()
		#end 2012-12-28
		print "Sub-process(es) done."
	print time.time() - startTime
	
	#self.testType="sync"
	if self.UI.testType=="sync":
        # daemon stopped, reseting everything
		pass
        	#self.daemonIsRunning = False
	else:
        	self.daemonIsRunning = False

if __name__=="__main__":
    work = Worker()
    work.startDaemon()
