#!/usr/bin/env python
#
# Example of assembling all available unit tests into one suite. This usually
# varies greatly from one project to the next, so the code shown below will not
# be incorporated into the 'unittest' module. Instead, modify it for your own
# purposes.
# 
# $Id: alltests.py,v 1.3 2001/03/12 11:52:56 purcell Exp $

from MulPools import *
from UnitTest import *
import UnitTest
#from E0995122 import *
from listtests import *
from globalvar import *
from MtsInt_StationConfig import *
import copy
#class MTestCase:
#	def __init__(self):
#		self.testName=""
#		self.setUp=""
#		self.tearDown=""
#class TestCaseCreater:
#	'to creater the test sequence with the test flow which we defined'
#	def __init__(self,tester="aaaa"):
#		self.tester=tester
#		#self.main_testsuites==TestSuite()
#	def loadTestFlow(self,testDic,testsuits):
#		e=testDic
#		if e.has_key("testflow"):
#			if len(e["testflow"])>0:
#				for li in e["testflow"]:
#					if type(eval(li))==type({}):
#						#"to add the test suite in main test suites"
#						sub_testsuites=UnitTest.TestSuite()
#						self.loadTestFlow(eval(li),sub_testsuites)
#						testsuits.addTest(sub_testsuites)
#					elif type(eval(li))==type(TestCaseCreater):
#						#"to add the case in main test suites"
#						li==type(eval(li))
#						testsuits.addTest(makeSuite(eval(li)))
#
#defaultTestLoader = TestLoader()
#
#
#class TestEngineXX:
#	def __init__(self, module='__main__', defaultTest=None,
#                 argv=None, testRunner=None, testLoader=defaultTestLoader):
#		self.testcreater=TestCaseCreater()
#		self.main_testsuites=UnitTest.TestSuite()
#		self.verbosity = 1
#		self.defaultTest = defaultTest
#		self.testRunner = testRunner
#		self.testLoader = testLoader
#	def Print(self):
#		self.main_testsuites==UnitTest.TestSuite()
#		self.testcreater.loadTestFlow(Main,self.main_testsuites)
#	def runTests(self):
#		if self.testRunner is None:
#			self.testRunner = NorTestRunner(verbosity=self.verbosity)
#		#result = self.testRunner.run(self.test)
#		self.testRunner.run(self.main_testsuites)
#		print "X"*20
#		for re in self.testRunner.testStepResults:
#			print ("%s" %re.testName).ljust(50) + re.testStatus +"  "
#			print re.assertItems[0].assertName
#		print "X"*20
#		sys.exit(not self.testRunner.wasSuccessful())
#
class TestEngine:
    """A command-line program that runs a set of tests; this is primarily
       for making test modules conveniently executable.
    """
    USAGE = """\
Usage: %(progName)s [options] [test] [...]

Options:
  -h, --help       Show this message
  -v, --verbose    Verbose output
  -q, --quiet      Minimal output

Examples:
  %(progName)s                               - run default set of tests
  %(progName)s MyTestSuite                   - run suite 'MyTestSuite'
  %(progName)s MyTestCase.testSomething      - run MyTestCase.testSomething
  %(progName)s MyTestCase                    - run all 'test*' test methods
                                               in MyTestCase
"""
    def __init__(self,parent=None, module='__main__', defaultTest=None,
                 argv=None, testRunner=None, testLoader=defaultTestLoader):
        if type(module) == type(''):
            self.module = __import__(module)
            for part in string.split(module,'.')[1:]:
                self.module = getattr(self.module, part)
        else:
            self.module = module
        if argv is None:
            argv = sys.argv
        self.verbosity = 1
        self.defaultTest = defaultTest
        self.testRunner = testRunner
        self.testLoader = testLoader
        self.progName = os.path.basename(argv[0])
	self.parent=parent
	self.mpExist=None
	#poolmaxcount=2
	#poolcount = len(self.parent.testUUTs)<poolmaxcount and len(self.parent.testUUTs) or poolmaxcount
	#poolcount = (len(self.parent.testUUTs)<poolmaxcount and len(self.parent.testUUTs)>0)and len(self.parent.testUUTs) or poolmaxcount
	self.mp=None
	#self.mp=MulPools(poolcount)
	###################################################
        #self.parseArgs(argv)
        #self.runTests()
    def createPool(self):
	if self.parent.UI.testType=="single":
		#poolmaxcount=1
		poolcount=1
	else:
		poolmaxcount=StationOptions["NumMaxPool"]
		poolcount = (len(self.parent.testUUTs)>poolmaxcount and len(self.parent.testUUTs)>0)and len(self.parent.testUUTs) or poolmaxcount
	self.mp=MulPools(poolcount)

    def usageExit(self, msg=None):
        if msg: print msg
        print self.USAGE % self.__dict__
        sys.exit(2)

    def parseArgs(self, argv): 
	import getopt
	if 0==0:
            options, args = getopt.getopt(argv[1:], 'hHvq',
                                          ['help','verbose','quiet'])
            for opt, value in options:
                if opt in ('-h','-H','--help'):
                    self.usageExit()
                if opt in ('-q','--quiet'):
                    self.verbosity = 0
                if opt in ('-v','--verbose'):
                    self.verbosity = 2
            if len(args) == 0 and self.defaultTest is None:
                self.test = self.testLoader.loadTestsFromModule(self.module)
                return
            if len(args) > 0:
                self.testNames = args
            else:
                self.testNames = (self.defaultTest,)
            self.createTests()
        try:
	    pass
        except getopt.error, msg:
            self.usageExit(msg)

    def createTests(self):
#        self.test = self.testLoader.loadTestsFromNames(self.testNames,
#                                                       self.module)
	self.test1=TestSuite()
	self.testLoader.loadTestFlow(Main,self.test1)
	#self.test2=TestSuite()
	#self.testLoader.loadTestFlow(Main,self.test2)
	#self.test3=TestSuite()
	#self.testLoader.loadTestFlow(Main,self.test3)
	#self.testCount=self.test1.countTestCases()

    def runTests(self):
        #if self.testRunner is None:
        #    self.testRunner = NorTestRunner(verbosity=self.verbosity)
        #result = self.testRunner.run(self.test)
        #self.testRunner.run(self.test)
	#self.parent.daemonStopSignal is the singnal from worker.it indicate the work is stop or not,if the work is stoped,the testengine will stop to run.
	#get the daemonStopSignal
	if mutex.acquire():
		daemonStopSignal.value=0
		mutex.release()
	#print self.parent
	#print self.parent.UI
	if self.parent.UI.testType=="sync":
		self.createPool()
		self.mp.Start()
		pass
	elif self.parent.UI.testType=="single":
		self.createPool()
		self.mp.Start()
		self.test1.UpdateTestIndex(0)
		self.mp.SubmitTasks(self.test1)
		self.mp.JoinTasks()
		time.sleep(4)
		self.mp.Stop()
	else:
		i=0
		if not self.mpExist:
			self.createPool()
			self.mp.Start()
			self.mpExist=True
		for sn in self.parent.snList:
			if sn:
				temp_test=copy.deepcopy(self.test1)
				#temp_test=self.test1
				#eval("test_%s" %i)=self.test1
				#eval("test_%s" %i).UpdateTestIndex(i)
				#self.test1.UpdateTestIndex(i)
				temp_test.UpdateTestIndex(i)
				self.mp.SubmitTasks(temp_test)
				#self.mp.SubmitTasks(eval("test_%s" %i))
			i=i+1
		self.mp.JoinTasks()
		time.sleep(4)
		#self.mp.Stop()
	#for result in self.mp.PopResult():
	#	for re in result.assertItems:
	#		print re.assertName
#	time.sleep(20)
#	self.mp.SubmitTasks(self.test1)
	#self.mp.JoinTasks()
#	print "X"*20
#	for re in self.testRunner.testStepResults:
#		print ("%s" %re.testName).ljust(50) + re.testStatus +"  "
#		print re.assertItems[0].assertName
#	print "X"*20
        #sys.exit(not self.testRunner.wasSuccessful())
    def AssignTask(self,wIndex):
	temp_test=copy.deepcopy(self.test1)
	temp_test.UpdateTestIndex(wIndex)
	#self.test1.UpdateTestIndex(wIndex)
	#self.mp.Restart()
	self.mp.SubmitTasks(temp_test)
    def run(self):
	#self.createTests()
	#if self.parent.UI.testType=="single":
	#	self.test1.UpdateTestIndex(1)
	self.runTests()
    def PopResults(self):
        #update the results list
        self.results=self.mp.PopResult()
	t=None
        for result in self.results:
               i=0
               for testUUT in self.parent.testUUTs:
                       if result.testIndex==testUUT.testIndex:
                               #update the test status of testUUT
#                               if not result.testStatus:
#                                       if testUUT.testStatus and result.recordResults:
#                                               testUUT.testStatus=False
#                               testUUT.testItems.append(result)
#                               testUUT.endTime=result.endTime
#                               #testUUT.endTime=time.time()
#                               testUUT.testTime=testUUT.endTime-testUUT.startTime
#                               self.parent.testUUTs[i]=testUUT
                                #update the test status of testUUT
                                #if not result.testStatus:
                                       #if testUUT.testStatus and result.recordResults:
                                #       if testUUT.testStatus:
                                #               testUUT.testStatus=False
				for ast in result.assertItems:
                                	if not ast.testStatus:
                                       		if testUUT.testStatus:
                                               		testUUT.testStatus=False
	                        testUUT.testItems.append(result)
				testUUT.endTime=time.time()
				testUUT.testTime=testUUT.endTime-testUUT.startTime
                   		self.parent.testUUTs[i]=testUUT
				t=testUUT
					
                              	break
                       i=i+1



if __name__ == '__main__':
	pass
	te=TestEngine()
	te.run()
	#te.runTests()
	#UnitTest.main()
