#!/usr/bin/env python
from m_TestStepResult import *

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime 
from Orm_Results import TestResults
from Configure import *
from CommFactory import *
from Log import *
import ConfigParser	

#from sqlalchemy.ext.declarative import declarative_bas
#engine = create_engine('sqlite:///testResults.db')
engine = create_engine('sqlite:///:memory:', echo=True)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
session = Session()
testIndex = 1  

class TestBase():

    failureException = AssertionError

    def __init__(self,methodName='runTest'):
        """Create an instance of the class that will use the named test
           method when executed. Raises a ValueError if the instance does
           not have a method with the specified name.
        """
        self.cf = ConfigParser.ConfigParser()
        self.cf.read("~//MTS//Config//MTS001.ini")
	self.failureException = AssertionError
	self.testIndex=-1
	self.assertItems=[]
	self.startTime=""
	self.endTime=""
	self.endTime=""
        #self.logFile='test.log'
	self.log=Log()
	#self.log.Open(self.logFile)
        self.com=CommFactory.CreateComm(self.commType,self.log)
        #self.log=None
	self.alreadyShow=0
        #self.config = Configure('SFTConfig.txt')
        #self.log=Log()
        #self.log.Open("test.log")
        if True:
            self.__testMethodName = methodName
            testMethod = getattr(self, methodName)
            self.__testMethodDoc = testMethod.__doc__
        try:
            pass
        except AttributeError:
            raise ValueError, "no such test method in %s: %s" % \
                  (self.__class__, methodName)

    def shortDescription(self):
        """Returns a one-line description of the test, or None if no
        description has been provided.

        The default implementation of this method returns the first line of
        the specified test method's docstring.
        """
        doc = self.__testMethodDoc
        return doc and string.strip(string.split(doc, "\n")[0]) or None

    def Run(self):
        pass

    def runTest(self):
        self.__testFunc()

    def fail(self, msg=None):
        """Fail immediately, with the given message."""
        raise self.failureException, msg

    def failIf(self, expr,assertName=None, msg=None):
        "Fail the test if the expression is true."
	if not assertName:
		assertName=self.shortDescription()
	ta=TestAssert(assertName)
	ta.testValue=expr
	ta.testLolim=False
	ta.testHilim=False
	ta.testStatus=not expr
	self.assertItems.append(ta)
	engine = create_engine('sqlite:///:memory:', echo=True)
	Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
	session = Session()
	testName="This is a test item for development"
	testDescription="this is Description for test items"
	testValue="V1.00"
	hiLimit="V1.00"
	lowLimit="V1.00"
	testType="Equal"
	testStatus=not expr
	sendCommand="ver"
	reciveMsg="V1.00"
	SN="RMS0995122G008"
	Socket="4"
	global testIndex
	testIndex = testIndex +1
	startTime=datetime.now().strftime('%c')
	#tr=TestResults(serialNumber=SN,socketId=Socket,sequenceId="%s" %testIndex,testName=testName,testValue=testValue,hiLimit=hiLimit,lowLimit=lowLimit,testType=testType,testStatus=testStatus,startTime=self.startTime,endTime=self.endTime,testDescription=testDescription,sendCommand=sendCommand,reciveMsg=reciveMsg)
	#session.add(tr)
	#session.commit()
        #if expr: raise self.failureException, msg

    def failUnless(self, expr,assertName=None, msg=None):
        """Fail the test unless the expression is true."""

	if not assertName:
		assertName=self.shortDescription()
	ta=TestAssert(assertName)
	ta.testValue=expr
	ta.testLolim=True
	ta.testHilim=True
	ta.testStatus=expr
	self.assertItems.append(ta)
	# Add the test result to test Result Table in Data Base
	#engine = create_engine('sqlite:///:memory:', echo=True)
	#engine = create_engine('sqlite:///testResults.db')
	#Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
	#session = Session()
	#session.execute("delete from t_TestResults;")
	#session.commit()
	# to careate the data base tables
	#Base.metadata.create_all(engine) 
	testDescription="this is Description for test items"
	testType="Equal"
	sendCommand=""
	reciveMsg=""
	SN=""
	global testIndex
	testIndex = testIndex +1
	startTime=datetime.now().strftime('%c')
	#tr=TestResults(serialNumber=SN,socketId="",sequenceId="%s" %testIndex,testName=assertName,testValue=expr,hiLimit=ta.testHilim,lowLimit=ta.testLolim,testType=testType,testStatus=expr,startTime=self.startTime,endTime=self.endTime,testDescription=testDescription,sendCommand=sendCommand,reciveMsg=reciveMsg)
	#session.add(tr)
	#session.commit()
	#if not expr:
	#	print "FAIL"
        #if not expr: raise self.failureException, msg

    def failUnlessRaises(self, excClass, callableObj, *args, **kwargs):
        """Fail unless an exception of class excClass is thrown
           by callableObj when invoked with arguments args and keyword
           arguments kwargs. If a different type of exception is
           thrown, it will not be caught, and the test case will be
           deemed to have suffered an error, exactly as for an
           unexpected exception.
        """
        try:
            apply(callableObj, args, kwargs)
        except excClass:
            return
        else:
            if hasattr(excClass,'__name__'): excName = excClass.__name__
            else: excName = str(excClass)
            raise self.failureException, excName

    def failUnlessEqual(self, first, second,assertName=None, msg=None):
        """Fail if the two objects are unequal as determined by the '!='
           operator.
        """
	if not assertName:
		assertName=self.shortDescription()
	ta=TestAssert(assertName)
	ta.testValue=first
	ta.testLolim=second
	ta.testHilim=second
	ta.testStatus=(first==second)
	self.assertItems.append(ta)
	# Add the test result to test Result Table in Data Base
	testName="This is a test item for development"
	testDescription="this is Description for test items"
	testValue="V1.00"
	hiLimit="V1.00"
	lowLimit="V1.00"
	testType="Equal"
	testStatus=(first==second)
	sendCommand="ver"
	reciveMsg="V1.00"
	SN="RMS0995122G008"
	Socket="4"
	global testIndex
	testIndex = testIndex +1
	startTime=datetime.now().strftime('%c')
	#tr=TestResults(serialNumber=SN,socketId=Socket,sequenceId="%s" %testIndex,testName=testName,testValue=testValue,hiLimit=hiLimit,lowLimit=lowLimit,testType=testType,testStatus=testStatus,startTime=self.startTime,endTime=self.endTime,testDescription=testDescription,sendCommand=sendCommand,reciveMsg=reciveMsg)
	#session.add(tr)
	#session.commit()
        #if first != second:
        #    raise self.failureException, (msg or '%s != %s' % (first, second))

    def failIfEqual(self, first, second,assertName, msg=None):
        """Fail if the two objects are equal as determined by the '=='
           operator.
        """
	if not assertName:
		assertName=self.shortDescription()
	ta=TestAssert(assertName)
	ta.testValue=first
	ta.testLolim=second
	ta.testHilim=second
	ta.testStatus=(first!=second)
	self.assertItems.append(ta)
	testName="This is a test item for development"
	testDescription="this is Description for test items"
	testValue="V1.00"
	hiLimit="V1.00"
	lowLimit="V1.00"
	testType="Equal"
	assertItems.append(ta)
	sendCommand="ver"
	reciveMsg="V1.00"
	SN="RMS0995122G008"
	Socket="4"
	global testIndex
	testIndex = testIndex +1
	startTime=datetime.now().strftime('%c')
	#tr=TestResults(serialNumber=SN,socketId=Socket,sequenceId="%s" %testIndex,testName=testName,testValue=testValue,hiLimit=hiLimit,lowLimit=lowLimit,testType=testType,testStatus=testStatus,startTime=self.startTime,endTime=self.endTime,testDescription=testDescription,sendCommand=sendCommand,reciveMsg=reciveMsg)
	#session.add(tr)
	#session.commit()
        if first == second:
            raise self.failureException, (msg or '%s == %s' % (first, second))
    passUnless =  failIf

    passIf = failUnless

    passEqual = passEquals = assertEqual = assertEquals = failUnlessEqual

    passUnlessEqual = assertNotEqual = assertNotEquals = failIfEqual

    assertRaises = failUnlessRaises

    assert_ = failUnless
