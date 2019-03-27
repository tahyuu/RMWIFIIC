import multiprocessing
#from TS import TS
from E0995122 import *
from Orm_Results import TestResults
from Log import Log
import time
import UnitTest
from UnitTest import *
from multiprocessing import Lock
from globalvar import *
#from DiagE import *
class TestResult():
    def __init__(self,testIndex):
	self.testStatus=True
        self.assertItems=[]
	self.startTime=0
	self.endTime=0
	self.testTime=0
	self.testIndex=testIndex
	self.testName=""
	self.testGroup=""
	self.recordResults=True

class Consumer(multiprocessing.Process):
    
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.shouldStop = Value('i',0)

	#self.lock=lock

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                #print ('%s: Exiting' % proc_name)
                self.task_queue.task_done()
                break
            #print ('%s: %s' % (proc_name, next_task))
            #answer = next_task() # __call__()
            #answer =  next_task()
            for answer in next_task.__call__(self.result_queue):
            	self.result_queue.put(answer)
		#pass
	    #print answer
            self.task_queue.task_done()
            #self.result_queue.put(answer)
        return
#**************************************************************************************************************#
#below class is for new test program I decicde pass the done_queue to Task and task will excute the test item and 
#**************************************************************************************************************#
defaultTestLoader = TestLoader()
class Task_new(object):
    def __init__(self,testIndex,sN):
	self.testIndex=testIndex
	self.sN=sN
        #self.testRunner = None 
        self.verbosity = 1
        self.testRunner = NorTestRunner(verbosity=self.verbosity)
	#self.testRunner.results=result_queue
    def __call__(self):
        self.createTests()
        self.runTests()
    def createTests(self):
        self.test=TestSuite()
        self.testLoader = defaultTestLoader
        self.testLoader.loadTestFlow(Main,self.test)

    def runTests(self):
        if self.testRunner is None:
            self.testRunner = NorTestRunner(verbosity=self.verbosity)
	    self.restRunner.results=self.result_queue
        #result = self.testRunner.run(self.test)
        self.testRunner.run(self.test)
#       print "X"*20
#       for re in self.testRunner.testStepResults:
#               print ("%s" %re.testName).ljust(50) + re.testStatus +"  "
#               print re.assertItems[0].assertName
#       print "X"*20
        #sys.exit(not self.testRunner.wasSuccessful())
class Task(object):
    def __init__(self, taskitems,args,testIndex,taskName,recordResults,testUUT):
        self.tasks = taskitems
        self.args = args
	self.testIndex=testIndex
	self.taskName=taskName
	self.recordResults=recordResults
        self.testUUT=testUUT
	self.sN=testUUT.sN
    def RunItem(self,task):
        if type(task)==type(""):
            pass
        else:
            pass

    def __call__(self,result_queue):
        #time.sleep(0.2) # pretend to take some time to do the work
        #return '%s * %s = %s' % (self.a, self.b, self.a * self.b)
	#item=leaftsl
	#item="DiagE.DiagE"	
#	print self.args[0]
#	print self.args[1]
	i=0
	#log=Log("test.log")
	#log.Open('a')
	#log.Write(self.args[0])
	#ts=TS(log,self.args[1],self.args[2],"RIT")
	#ts.Connect(self.args[2]) 
        #print "taskes  is %s" %self.tasks
	global daemonStopSignal,mutex,uutStatusArr

        #for x in self.tasks:
        #    if type(x)==type(""):
        #        continue
        #continueprint "before set consummer, index is %s, status is %s" %(self.testIndex,uutStatusArr[self.testIndex])
        if uutStatusArr[self.testIndex]==1:
            return

	while i<len(self.tasks):

		test_demonStopSignal=False
		#get the daemonStopSignal
		test_demonStopSignal=daemonStopSignal.value
		#when the daemon stop, the task will exit
		if test_demonStopSignal==1:
			break
		item=self.tasks[i]
                #print "task is %s" %item
	        teststepfile,teststepclass = item.split('.')
	        #teststepfile,teststepclass = item.tsl[0].split('.')
        	#m_import=__import__("%s.%s" % ("TestSteps",teststepfile))
	        m_import=__import__("%s" % (teststepfile))
       		c_testStep=getattr(m_import,teststepclass)
	        #m_testStep=getattr(m_import,teststepfile)
	#       c_testStep = getattr(m_testStep,teststepclass)
		#teststepresult=TestResult(self.testIndex)
		#teststepresult.startTime=time.time()
		if teststepfile=="DiagReadEEP":
	       		o_testStep=c_testStep(log,"",ts,self.sN)
		else:
                        #print "arg0 is %s" %self.args[0]
	       		o_testStep=c_testStep()
                        o_testStep.log=Log()
                        print "file path is: %s; file name is: %s" %(self.testUUT.log_path,self.testUUT.log_filename)
                        if self.testUUT.log_path=="":
                            self.testUUT.log_path="D://MTS"
                        if self.testUUT.log_filename=="":
                            self.testUUT.log_filename="test.log"
			o_testStep.log.Open(self.testUUT.log_path + '/' + self.testUUT.log_filename,'a+')
                        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
                        o_testStep.com.log=o_testStep.log
                        

		teststepresult=TestResult(self.testIndex)
		teststepresult.testTime=teststepresult.endTime-teststepresult.startTime
       		#o_testStep=c_testStep(*args)
		teststepresult.testName=o_testStep.section_str
		teststepresult.testGroup=self.taskName
		teststepresult.recordResults=self.recordResults
		try:
		    testStatus=o_testStep.Run()
		except:
	            testStatus="FAIL"
		teststepresult.endTime=time.time()
		teststepresult.testTime=teststepresult.endTime-teststepresult.startTime
		if testStatus=="PASS":
	        	teststepresult.testStatus=True
	        	#print 'uut status arr is %s' %uutStatusArr[0]

		else:
	        	teststepresult.testStatus=False
	
		i=i+1
                #self.testUUT.testItems.append(teststepresult)
                teststepresult.assertItems=o_testStep.assertItems
                for assertItem in o_testStep.assertItems:
                    if not assertItem.testStatus:
                        uutStatusArr[self.testIndex]=1
                        break
                #result_queue.put(teststepresult)
		yield teststepresult
		if not teststepresult.testStatus:
			break
	#ts.Close()
	
    def __str__(self):
        #return '%s * %s' % (self.tasks, self.args)
	return ""


if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    
    # Start consumers
#    num_consumers = multiprocessing.cpu_count()
    num_consumers = 8
    print ('Creating %d consumers' % num_consumers)
    consumers = [ Consumer(tasks, results)
                  for i in range(num_consumers) ]
    for w in consumers:
        w.start()
    
    # Enqueue jobs
    num_jobs = 2 
    for i in range(num_jobs):
        #tasks.put(Task(i, i,results))
        tasks.put(Task(i, i))
	
    tasks.join()
    
    #for i in range(num_jobs):
    #    tasks.put(Task(i, i))

    #tasks.join()
    # Add a poison pill for each consumer
    for i in range(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()
    
    # Start printing results
    while num_jobs:
        result = results.get()
        print ('Result:', result)
        num_jobs -= 1

