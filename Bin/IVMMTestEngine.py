import sys
import os
import Queue
from globalvar import *
currentDir = os.getcwd()
#import the base py file
sys.path.append(currentDir +"/Common")
sys.path.append(currentDir +"/Config")
sys.path.append(currentDir +"/TestItem")

import time
from Log import Log
from PSU import PSU
from Socket import Socket
from TestStepResult import TestStepResult
from multiprocessing import Queue as MultiprocessingQueue
from AssingmentAddress import AssingmentAddress
from GetFirmWareVer import GetFirmwareVer
#from ZTest import ZTest

#from Read3AxisAcceleration import Read3AxisAcceleration
from ReadTemper import ReadTemper
#from ReadADSVoltage import ReadADSVoltage
#from CANBus import CANBus
#from RS232 import RS232
#from FLASH import FLASH
from StartDDR import StartDDR 
from ReadDDR import ReadDDR 
from StartMMC import StartMMC 
from ReadMMC import ReadMMC
from Read3AxisAcceleration import Read3AxisAcceleration
from StartCanBus1 import StartCanBus1
from StartCanBus2 import StartCanBus2
from ReadCanBus1 import ReadCanBus1
from ReadCanBus2 import ReadCanBus2
from StartEMMC import StartEMMC
from ReadEMMC import ReadEMMC
from MtsInt_StationConfig import *
#from MMC import MMC
#from QUIT import QUIT
class BaseEngine:
	def __init__(self,parent):
		self.testCount=0
		self.parent=parent
	def RunTest(self):
		pass
	def PrepareForEachTest(self):
		pass
	def PopResults(self):
		pass
	def WriteTestResultToLog(self):
		pass

class IVMMTestEngine(BaseEngine):
	def __init__(self,parent):
		BaseEngine.__init__(self,parent)
		#self.testResults=Queue
		self.done_queue = MultiprocessingQueue()
		self.testItems=[AssingmentAddress,GetFirmwareVer,Read3AxisAcceleration,ReadTemper,StartCanBus1,ReadCanBus1,StartCanBus2,ReadCanBus2,StartEMMC,ReadEMMC,StartDDR,ReadDDR,StartMMC,ReadMMC]
		#self.testItems=[AssingmentAddress,GetFirmwareVer,Read3AxisAcceleration]
		#self.testCount=12*14
		#test times
		self.testTimes=48
		#test loop time
		self.oneUUTTestTime=13
		#all the uut test times this station is 24H
		self.totalTestTime=24*60*60
		#one cycle Test time not include wait time
		self.cycleTestTime=self.oneUUTTestTime*len(self.parent.testUUTs)
		#one cycle test time ----the sum of all the uut test time and wait time
		#total time- one cycle test time(not include wait time,sub the last cycle time)/testTimes-1
		self.cycleTime=((self.totalTestTime-self.cycleTestTime)/(self.testTimes-1))

		self.testCount=self.testTimes*len(self.testItems)
	def RunTest(self):
		i=0
		#8353000370
		#snlist_A=["8353000370","8353000222","8353000436","8353000347","8353000326","8353000261","8353000316","8353000142","8353000499","8353000339","8353000377","8353000300","8353000277","8353000270"]
		#snlist_B=["8353000329","8353000366","8353000296","8353000320","8353000428","8353000154","8353000380","8353000249","8353000319","8353000252","8353000221","8353000425","8353000241","8353000104"]
		#snlist_C=["8353000395","8353000426","8353000416","8353000408","8353000303","8353000310","8353000324","8353000341","8353000112","8353000244","8353000342","8353000034","8353000243","8353000497"]
		#snlist_D=["8353000458","8353000qqq","8353000332","8353000259","8353000349","8353000344","8353000355","8353000407","8353000380","8353000221","8353000341","8353000228","a","8353000427"]

		#snlist_D=["8353000458","8353000407","8353000427","8353000344"]
		#snlist=snlist_A+snlist_B+snlist_C+snlist_D
		for testUUT in self.parent.testUUTs:
			testUUT.testCount=self.testCount
			#testUUT.sN=snlist[i]
			self.parent.testUUTs[i]=testUUT
			i=i+1
		self.PrepareForEachTest()
		#self.parent.daemonStopSignal is the singnal from worker.it indicate the work is stop or not,if the work is stoped,the testengine will stop to run.
		global daemonStopSignal,mutex
		#get the daemonStopSignal
		if mutex.acquire():
			daemonStopSignal.value=0
			mutex.release()
		#recode the number of test times
		testFrequency=0
		#write you power on code here
		####################
		psu=PSU()
		psu.PowerOn()
		time.sleep(10)
		#write you power on code here
		testStartTime=time.time()
		while True:

			#get the daemonStopSignal
			test_demonStopSignal=daemonStopSignal.value
			#when the all the test stoped.or the stop button pushed. we need to end test
			if test_demonStopSignal==1:
				break
			testFrequency+=1
			allTimeOutStatus=True
			statusArray=[]
			i=0
			print "starting test .........................."
			loopStartTime=time.time()
			for testUUT in self.parent.testUUTs:
				if testUUT.startTime==0:
					testUUT.startTime=time.time()
				#get the daemonStopSignal
				socket=self.parent.testsockets[testUUT.testIndex]
				socket.sn=testUUT.sN
				test_demonStopSignal=daemonStopSignal.value
				#when the all the test stoped.or the stop button pushed. we need to end test
				if test_demonStopSignal==1:
					break
				#why will countine
				#if (not testUUT.testStatus) or (time.time()-testStartTime>60*60*12):
				if (not testUUT.testStatus): 
					i=i+1
					continue
				#init test socket	
				#socket=Socket(socketid)
				#excute test item one by one
				for ti in self.testItems:
					#get the daemonStopSignal
					test_demonStopSignal=daemonStopSignal.value
					#when the all the test stoped.or the stop button pushed. we need to end test
					if test_demonStopSignal==1:
						break
					obj=ti(socket)
					testResult=obj.Run()
					testResult.testGroup="Test frequency(%s)"%(testFrequency)
					#put result to don_queue
					#self.done_queue.put(testResult)

					#update the test status of testUUT
					if not testResult.testStatus:
						if testUUT.testStatus and testResult.recordResults:
							testUUT.testStatus=False
					testUUT.testItems.append(testResult)
					testUUT.endTime=testResult.endTime
					#testUUT.endTime=time.time()
					testUUT.testTime=testUUT.endTime-testUUT.startTime
					self.parent.testUUTs[i]=testUUT
					#testUUT.testItems.append(testResult)
					testUUT.log.Open("a")
					testUUT.log.Write(testResult.log)
					#when the test result fail we will exit this uut test
					if not testResult.testStatus:
						break
				#add status to an array only if the status array all are True test will exit
				#when the uut test failed or test time over 24H the uut test will exit the test
				#if (not testUUT.testStatus) or (time.time()-testUUT.startTime>60):
				if (not testUUT.testStatus) or (time.time()-testUUT.startTime>self.totalTestTime-self.cycleTestTime):
					#currentTimeOutStatus=True
					statusArray.append(True)
					#allTimeOutStatus=allTimeOutStatus and currentTimeOutStatus
					#print "uut%s is finished" %testUUT.testIndex
					#print "uut%s status is : %s" %(testUUT.testIndex,testUUT.testStatus)
					#continue	
				else:
					statusArray.append(False)
					#print "uut%s is not finished" %testUUT.testIndex
					#print "uut%s status is : %s" %(testUUT.testIndex,testUUT.testStatus)
					#currentTimeOutStatus=False
					#allTimeOutStatus=allTimeOutStatus and currentTimeOutStatus
				#statusArray.append(testUUT.testStatus)
				i=i+1
			#when all the test uut test over 24H or all the test uut failed. we will exit test
			statusFlag=True
			#print statusArray
			for status in statusArray:
				statusFlag=statusFlag and status
				if not statusFlag:
					break
			#print "*************************************************************************"
			#print testFrequency
			#print statusArray
			#print statusFlag
			#print "*************************************************************************"
			#print ""
			#print ""

			if statusFlag:
				break
			#wait for a few time
			#time.sleep(3600-(time.time-loopStartTime))
			#print "waiting................"
			#print "cycle test time %s" %(time.time()-loopStartTime)
			while True:
				#total remain time
				totalRemain=self.totalTestTime-(time.time()-testStartTime)
				#current remain time
				timeRemain=(self.cycleTime-(time.time()-loopStartTime))
				if timeRemain>totalRemain:
					timeRemain=totalRemain
				
				if timeRemain>3:
					time.sleep(3)
					#print "please wait for %d s .................." %timeRemain
				else:
					break
					
				test_demonStopSignal=daemonStopSignal.value
				if test_demonStopSignal==1:
					break
			#time.sleep(self.loopTime-())
			#time.sleep(10-(time.time()-loopStartTime))
		#write you power off code here
		psu.PowerOff()
		##########
		#write you power off code here

		#start flexflow save results

		#end flexflow save results

	def PrepareForEachTest(self):
		self.logpath=StationOptions["LogPath"]
		self.StationName=StationOptions["StationName"]
		self.TestDate = time.strftime("%Y%m%d")
		self.savepath = self.logpath + '/' + self.StationName + '/' + self.TestDate
		if os.path.exists(self.savepath):
		    pass
		else:
		    os.makedirs(self.savepath)
		k=0
		self.parent.testlogfiles=[]
		#for testUUT in self.parent.testUUTs:
		for sn in self.parent.snList:
			if not sn:
				#do not add file add space to testlogfiles array
				self.parent.testlogfiles.append("")
			else:
				#add file name to testlogfiles array
				testUUT=self.parent.testUUTs[k]
				socket=self.parent.testsockets[testUUT.testIndex]

				testUUT.log_filename = testUUT.sN + '_' + time.strftime("%Y%m%d%H%M%S")+"_"+str(socket.id) + '.log'
				testUUT.log_path = self.savepath
				self.parent.testlogfiles.append(testUUT.log_path + '/' + testUUT.log_filename)
				#print testUUT.log_path+"/"+testUUT.log_filename
				testUUT.log.fileName=testUUT.log_path+'/'+testUUT.log_filename
				testUUT.log.Open("a")
				testUUT.log.Write('                                                  ')
				testUUT.log.Write('##################################################')
				testUUT.log.Write('Station : '.rjust(20) + self.StationName)
				testUUT.log.Write('Date : '.rjust(20) + self.TestDate)
				testUUT.log.Write('SerialNumber : '.rjust(20) + testUUT.sN)
				#testUUT.log.Write('UUTType : '.rjust(20) + testUUT.pN)
				#testUUT.log.PrintNoTime('UUTType : '.rjust(20) + self.parent.TSLfile)
				#self.TSLfile = str(StationOptions["TestProgram"]).replace(".py","")
				#testUUT.log.PrintNoTime('PDUIP : '.rjust(20) + self.pduip)
				#testUUT.log.PrintNoTime('PDUPort : '.rjust(20) + self.pduport)
				#testUUT.log.PrintNoTime('TSIP : '.rjust(20) + self.tsip)
				#testUUT.log.PrintNoTime('TSIP : '.rjust(20) + socket.ip)
				#testUUT.log.PrintNoTime('TSPort : '.rjust(20) + str(socket.comPort))
				testUUT.log.Write('485Port: '.rjust(20) + str(socket.comPort))
				testUUT.log.Write('UUT Index : '.rjust(20) + str(testUUT.testIndex + 1))
				testUUT.log.Write('##################################################')
				#testUUT.log.Write('_testResults_')
				testUUT.log.Write('----------------- Start Testing ------------------')
				testUUT.log.Write('##################################################')
				self.parent.testUUTs[k]=testUUT
				k=k+1
	def getResult(self):
	    results=[]
	    while True:
	        try:
	             queue_data = self.done_queue.get_nowait()
		     results.append(queue_data)
	    	except Queue.Empty:
	       	     if self.done_queue.qsize() < 1:
		        break
	    return results
	def PopResults(self):
		 #update the results list
	         self.results=self.getResult()
	         for result in self.results:
			i=0
			for testUUT in self.parent.testUUTs:
				if result.testIndex==testUUT.testIndex:
					#update the test status of testUUT
					if not result.testStatus:
						if testUUT.testStatus and result.recordResults:
							testUUT.testStatus=False
					testUUT.testItems.append(result)
					testUUT.endTime=result.endTime
					#testUUT.endTime=time.time()
					testUUT.testTime=testUUT.endTime-testUUT.startTime
					self.parent.testUUTs[i]=testUUT
					break
				i=i+1
	def WriteTestResultToLog(self):
		for testUUT in self.parent.testUUTs:
			strReslt="testUUT testIndex is : %s "%testUUT.testIndex+"\r\n"
			test_demonStopSignal=daemonStopSignal.value
			if test_demonStopSignal==1:
				strResult='\n'+('Test Result:Terminate').center(60,'-')+'\n'+('Test Time:'+str(int(testUUT.testTime))).center(60,'-')+'\n'
			else:
				strResult='\n'+('Test Result:'+(testUUT.testStatus and "PASS" or "FAIL")).center(60,'-')+'\n'+('Test Time:'+str(int(testUUT.testTime))+"(s)").center(60,'-')+'\n'
			strResult+="#############################################################################################"+"\n"
			for testItem in testUUT.testItems:
				#check the testItem need to write into log file
				if testItem.recordResults:
					strResult+=testItem.testGroup.ljust(20)+" => ".rjust(10)+testItem.stepName.replace("Section","").ljust(30)+"         "+(testItem.testStatus and "PASS" or "FAIL")
					strResult+="\n"
			strResult+="#############################################################################################"
			testUUT.log.Open("a")
			#testUUT.log.Close()
			#testUUT.log.Replace("_testResults_",strResult,1,10)
			testUUT.log.Write(strResult)
			testUUT.log.Close()
			#testUUT.log.Write(strResult,testUUT.log_path + '/' + testUUT.log_filename)
		pass

if __name__=="__main__":
	#testItems=[AssingmentAddress, GetFirmwareVer, Read3AxisAcceleration,ReadTemper,ReadADSVoltage,CANBus, FLASH,DDR,MMC]
	#testItems=[AssingmentAddress,GetFirmwareVer,ReadTemper]
	#testItems=[ZTest]*100
	log=Log("test.log")
	log.Open("w")
	log.Write("")
	log.Write("*****************************************************")
	log.Write("Test Station : ".rjust(15)+"IVMM-Born-in")
	log.Write("Start Time : ".rjust(15),withReturn=False)
	log.Write("",withTime=True)
	log.Write("End Time : ".rjust(15),withReturn=False)
	log.Write("",withTime=True)
	log.Write("*****************************************************")
	log.Write("")
	log.Write("")
	socket=Socket(2)
	for ti in testItems:
		obj=ti(socket)
		print obj.Run().log
		log.Write(obj.Run().log)
		log.Write("")
	log.Write("Test End",withTime=True)
	log.Close()
