#!/usr/bin/env python
from E0995122 import * 
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, scoped_session
from Orm_Results import TestResults
import datetime
#from sqlalchemy.ext.declarative import declarative_bas
engine = create_engine('sqlite:///testResults.db')
#engine = create_engine('sqlite:///:memory:', echo=True)
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
session = Session()
testIndex = 0  
'''
Python unit testing framework, based on Erich Gamma's JUnit and Kent Beck's
Smalltalk testing framework.

This module contains the core framework classes that form the basis of
specific test cases and suites (TestCase, TestSuite etc.), and also a
text-based utility class for running the tests and reporting the results
(TextTestRunner).

Simple usage:

    import unittest

    class IntegerArithmenticTestCase(unittest.TestCase):
        def testAdd(self):  ## test method names begin 'test*'
            self.assertEquals((1 + 2), 3)
            self.assertEquals(0 + 1, 1)
        def testMultiply(self);
            self.assertEquals((0 * 10), 0)
            self.assertEquals((5 * 8), 40)

    if __name__ == '__main__':
        unittest.main()

Further information is available in the bundled documentation, and from

  http://pyunit.sourceforge.net/

Copyright (c) 1999, 2000, 2001 Steve Purcell
This module is free software, and you may redistribute it and/or modify
it under the same terms as Python itself, so long as this copyright message
and disclaimer are retained in their original form.

IN NO EVENT SHALL THE AUTHOR BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
THIS CODE, EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.

THE AUTHOR SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE.  THE CODE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS,
AND THERE IS NO OBLIGATION WHATSOEVER TO PROVIDE MAINTENANCE,
SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
'''

__author__ = "yong tan"
__email__ = "yong.tan@flextronics.com"
__version__ = "$Revision: 1.0 $"[11:-2]

import time
import sys
import traceback
import string
import os
import types
from m_TestStepResult import *

##############################################################################
# Test framework core
##############################################################################

class TestRunner:
    """Holder for test result information.

    Test results are automatically managed by the TestCase and TestSuite
    classes, and do not need to be explicitly manipulated by writers of tests.

    Each instance holds the total number of tests run, and collections of
    failures and errors that occurred among those test runs. The collections
    contain tuples of (testcase, exceptioninfo), where exceptioninfo is a
    tuple of values as returned by sys.exc_info().
    """
    def __init__(self,result_queue):
        self.failures = []
        self.errors = []
        self.testsRun = 0
        self.shouldStop = 0
	self.results=result_queue

    def startTest(self, test):
        "Called when the given test is about to be run"
        self.testsRun = self.testsRun + 1

    def stopTest(self, test):
        "Called when the given test has been run"
        pass

    def addError(self, test, err):
        "Called when an error has occurred"
	self.results.put(test)
        self.errors.append((test, err))

    def addFailure(self, test, err):
        "Called when a failure has occurred"
	self.results.put(test)
        self.failures.append((test, err))

    def addSuccess(self, test):
        "Called when a test has completed successfully"
	#print test
	#print len(test.assertItems)
	self.results.put(test)
        pass

    def wasSuccessful(self):
        "Tells whether or not this result was a success"
        return len(self.failures) == len(self.errors) == 0

    def stop(self):
        "Indicates that the tests should be aborted"
        self.shouldStop = 1

    def __repr__(self):
        return "<%s run=%i errors=%i failures=%i>" % \
               (self.__class__, self.testsRun, len(self.errors),
                len(self.failures))


class TestCase:
    """A class whose instances are single test cases.

    By default, the test code itself should be placed in a method named
    'runTest'.

    If the fixture may be used for many test cases, create as
    many test methods as are needed. When instantiating such a TestCase
    subclass, specify in the constructor arguments the name of the test method
    that the instance is to execute.

    Test authors should subclass TestCase for their own tests. Construction
    and deconstruction of the test's environment ('fixture') can be
    implemented by overriding the 'setUp' and 'tearDown' methods respectively.

    If it is necessary to override the __init__ method, the base class
    __init__ method must always be called. It is important that subclasses
    should not change the signature of their __init__ method, since instances
    of the classes are instantiated automatically by parts of the framework
    in order to be run.
    """

    # This attribute determines which exception will be raised when
    # the instance's assertion methods fail; test methods raising this
    # exception will be deemed to have 'failed' rather than 'errored'

    failureException = AssertionError

    def __init__(self, methodName='runTest'):
        """Create an instance of the class that will use the named test
           method when executed. Raises a ValueError if the instance does
           not have a method with the specified name.
        """
	self.assertItems=[]
	self.startTime=""
	self.endTime=""
	self.endTime=""
        try:
            self.__testMethodName = methodName
            testMethod = getattr(self, methodName)
            self.__testMethodDoc = testMethod.__doc__
        except AttributeError:
            raise ValueError, "no such test method in %s: %s" % \
                  (self.__class__, methodName)

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        pass

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        pass

    def countTestCases(self):
        return 1

    def defaultTestResult(self):
        return TestRunner()

    def shortDescription(self):
        """Returns a one-line description of the test, or None if no
        description has been provided.

        The default implementation of this method returns the first line of
        the specified test method's docstring.
        """
        doc = self.__testMethodDoc
        return doc and string.strip(string.split(doc, "\n")[0]) or None

    def id(self):
        return "%s.%s" % (self.__class__, self.__testMethodName)

    def __str__(self):
        return "%s (%s)" % (self.__testMethodName, self.__class__)

    def __repr__(self):
        return "<%s testMethod=%s>" % \
               (self.__class__, self.__testMethodName)

    def run(self, result=None):
        return self(result)

    def __call__(self, result=None):
        if result is None: result = self.defaultTestResult()
        result.startTest(self)
        testMethod = getattr(self, self.__testMethodName)
	self.startTime=datetime.datetime.now().strftime('%c')
        try:
            try:
                self.setUp()
            except:
                result.addError(self,self.__exc_info())
                return

            ok = 0
            try:
                testMethod()
                ok = 1
            except self.failureException, e:
                result.addFailure(self,self.__exc_info())
            except:
                result.addError(self,self.__exc_info())

            try:
                self.tearDown()
            except:
                result.addError(self,self.__exc_info())
                ok = 0
	    self.endTime=datetime.datetime.now().strftime('%c')
            if ok: result.addSuccess(self)
        finally:
            result.stopTest(self)
	return self
	    #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
	    #return self
	    #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    def debug(self):
        """Run the test without collecting errors in a TestResult"""
        self.setUp()
        getattr(self, self.__testMethodName)()
        self.tearDown()

    def __exc_info(self):
        """Return a version of sys.exc_info() with the traceback frame
           minimised; usually the top level of the traceback frame is not
           needed.
        """
        exctype, excvalue, tb = sys.exc_info()
        if sys.platform[:4] == 'java': ## tracebacks look different in Jython
            return (exctype, excvalue, tb)
        newtb = tb.tb_next
        if newtb is None:
            return (exctype, excvalue, tb)
        return (exctype, excvalue, newtb)

    def fail(self, msg=None):
        """Fail immediately, with the given message."""
        raise self.failureException, msg

    def failIf(self, expr,assertName=None, msg=None):
        "Fail the test if the expression is true."
	ta=TestAssert(assertName)
	ta.testValue=expr
	ta.testLolim=False
	ta.testHilim=False
	ta.testStatus=not expr
	self.assertItems.append(ta)
	# Add the test result to test Result Table in Data Base
	#engine = create_engine('sqlite:///testResults.db')
	#engine = create_engine('sqlite:///:memory:', echo=True)
	#Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
	#session = Session()
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
	#startTime=datetime.datetime.now().strftime('%c')
	#tr=TestResults(serialNumber=SN,socketId=Socket,sequenceId="%s" %testIndex,testName=testName,testValue=testValue,hiLimit=hiLimit,lowLimit=lowLimit,testType=testType,testStatus=testStatus,startTime=self.startTime,endTime=self.endTime,testDescription=testDescription,sendCommand=sendCommand,reciveMsg=reciveMsg)
	#session.add(tr)
	#session.commit()
        if expr: raise self.failureException, msg

    def failUnless(self, expr,assertName=None, msg=None):
        """Fail the test unless the expression is true."""
	ta=TestAssert(assertName)
	ta.testValue=expr
	ta.testLolim=True
	ta.testHilim=True
	ta.testStatus=expr
	self.assertItems.append(ta)
	# Add the test result to test Result Table in Data Base
	#engine = create_engine('sqlite:///testResults.db')
	#engine = create_engine('sqlite:///:memory:', echo=True)
	#Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
	#session = Session()
	testName="This is a test item for development"
	testDescription="this is Description for test items"
	testValue="V1.00"
	hiLimit="V1.00"
	lowLimit="V1.00"
	testType="Equal"
	testStatus=expr
	sendCommand="ver"
	reciveMsg="V1.00"
	SN="RMS0995122G008"
	Socket="4"
	global testIndex
	testIndex = testIndex +1
	#startTime=datetime.datetime.now().strftime('%c')
	#tr=TestResults(serialNumber=SN,socketId=Socket,sequenceId="%s" %testIndex,testName=testName,testValue=testValue,hiLimit=hiLimit,lowLimit=lowLimit,testType=testType,testStatus=testStatus,startTime=self.startTime,endTime=self.endTime,testDescription=testDescription,sendCommand=sendCommand,reciveMsg=reciveMsg)
	#session.add(tr)
	#session.commit()
        if not expr: raise self.failureException, msg

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
	ta=TestAssert(assertName)
	ta.testValue=first
	ta.testLolim=second
	ta.testHilim=second
	ta.testStatus=(first==second)
	self.assertItems.append(ta)
	# Add the test result to test Result Table in Data Base
	#engine = create_engine('sqlite:///testResults.db')
	#engine = create_engine('sqlite:///:memory:', echo=True)
	#Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
	#session = Session()
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
	#startTime=datetime.datetime.now().strftime('%c')
	#tr=TestResults(serialNumber=SN,socketId=Socket,sequenceId="%s" %testIndex,testName=testName,testValue=testValue,hiLimit=hiLimit,lowLimit=lowLimit,testType=testType,testStatus=testStatus,startTime=self.startTime,endTime=self.endTime,testDescription=testDescription,sendCommand=sendCommand,reciveMsg=reciveMsg)
	#session.add(tr)
	#session.commit()
        if first != second:
            raise self.failureException, (msg or '%s != %s' % (first, second))

    def failIfEqual(self, first, second,assertName, msg=None):
        """Fail if the two objects are equal as determined by the '=='
           operator.
        """
	ta=TestAssert(assertName)
	ta.testValue=first
	ta.testLolim=second
	ta.testHilim=second
	ta.testStatus=(first!=second)
	self.assertItems.append(ta)
	# Add the test result to test Result Table in Data Base
	#engine = create_engine('sqlite:///testResults.db')
	#engine = create_engine('sqlite:///:memory:', echo=True)
	#Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
	#session = Session()
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
	#startTime=datetime.datetime.now().strftime('%c')
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



class TestSuite:
    """A test suite is a composite test consisting of a number of TestCases.

    For use, create an instance of TestSuite, then add test case instances.
    When all tests have been added, the suite can be passed to a test
    runner, such as TextTestRunner. It will run the individual test cases
    in the order in which they were added, aggregating the results. When
    subclassing, do not forget to call the base class constructor.
    """
    def __init__(self, tests=()):
        self._tests = []
        self.addTests(tests)

    def __repr__(self):
        return "<%s tests=%s>" % (self.__class__, self._tests)

    __str__ = __repr__
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        pass

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        pass

    def countTestCases(self):
        cases = 0
        for test in self._tests:
            cases = cases + test.countTestCases()
        return cases

    def addTest(self, test):
        self._tests.append(test)

    def addTests(self, tests):
        for test in tests:
            self.addTest(test)

    def run(self, result):
        return self(result)

    def __call__(self,result):
	# add a set up and teardonw in test suite class
	###################################################
	try:
           self.setUp()
        except:
           result.addError(self,self.__exc_info())
           return
	###################################################

        for test in self._tests:
            if result.shouldStop:
                break
            yield test(result)
	# add a set up and teardonw in test suite class
	###################################################
	try:
            self.tearDown()
        except:
            result.addError(self,self.__exc_info())
	###################################################
	    
        #return result

    def debug(self):
        """Run the tests without collecting errors in a TestResult"""
        for test in self._tests: test.debug()


class FunctionTestCase(TestCase):
    """A test case that wraps a test function.

    This is useful for slipping pre-existing test functions into the
    PyUnit framework. Optionally, set-up and tidy-up functions can be
    supplied. As with TestCase, the tidy-up ('tearDown') function will
    always be called if the set-up ('setUp') function ran successfully.
    """

    def __init__(self, testFunc, setUp=None, tearDown=None,
                 description=None):
        TestCase.__init__(self)
        self.__setUpFunc = setUp
        self.__tearDownFunc = tearDown
        self.__testFunc = testFunc
        self.__description = description

    def setUp(self):
        if self.__setUpFunc is not None:
            self.__setUpFunc()

    def tearDown(self):
        if self.__tearDownFunc is not None:
            self.__tearDownFunc()

    def runTest(self):
        self.__testFunc()

    def id(self):
        return self.__testFunc.__name__

    def __str__(self):
        return "%s (%s)" % (self.__class__, self.__testFunc.__name__)

    def __repr__(self):
        return "<%s testFunc=%s>" % (self.__class__, self.__testFunc)

    def shortDescription(self):
        if self.__description is not None: return self.__description
        doc = self.__testFunc.__doc__
        return doc and string.strip(string.split(doc, "\n")[0]) or None



##############################################################################
# Locating and loading tests
##############################################################################

class TestLoader:
    """This class is responsible for loading tests according to various
    criteria and returning them wrapped in a Test
    """
    testMethodPrefix = 'test'
    sortTestMethodsUsing = cmp
    suiteClass = TestSuite

    def loadTestsFromTestCase(self, testCaseClass):
        """Return a suite of all tests cases contained in testCaseClass"""
        return self.suiteClass(map(testCaseClass,
                                   self.getTestCaseNames(testCaseClass)))
    #add by yong tan to load test from test flow file
    def loadTestFlow(self,testDic,testsuits):
	e=testDic
	if e.has_key("testflow"):
		if len(e["testflow"])>0:
			for li in e["testflow"]:
				module = __import__("listtests")
				c_testStep=getattr(module,li)
				if type(c_testStep)==type({}):
					#"to add the test suite in main test suites"
            				obj = getattr(module, li)
					sub_testsuites=TestSuite()
					self.loadTestFlow(eval(li),sub_testsuites)
					testsuits.addTest(sub_testsuites)
				elif type(c_testStep)==type(TestCase):
					#"to add the case in main test suites"
					#li==type(eval(li))
					testsuits.addTest(makeSuite(c_testStep))

    def loadTestsFromModule(self, module):
        """Return a suite of all tests cases contained in the given module"""
        tests = []
        for name in dir(module):
            obj = getattr(module, name)
	    #print  type(obj) == types.ClassType and issubclass(obj, TestCase)
            if type(obj) == types.ClassType and issubclass(obj, TestCase):
                tests.append(self.loadTestsFromTestCase(obj))
        return self.suiteClass(tests)

    def loadTestsFromName(self, name, module=None):
        """Return a suite of all tests cases given a string specifier.

        The name may resolve either to a module, a test case class, a
        test method within a test case class, or a callable object which
        returns a TestCase or TestSuite instance.

        The method optionally resolves the names relative to a given module.
        """
        parts = string.split(name, '.')
        if module is None:
            if not parts:
                raise ValueError, "incomplete test name: %s" % name
            else:
                parts_copy = parts[:]
                while parts_copy:
                    try:
                        module = __import__(string.join(parts_copy,'.'))
                        break
                    except ImportError:
                        del parts_copy[-1]
                        if not parts_copy: raise
                parts = parts[1:]
        obj = module
        for part in parts:
            obj = getattr(obj, part)

        import unittest
        if type(obj) == types.ModuleType:
            return self.loadTestsFromModule(obj)
        elif type(obj) == types.ClassType and issubclass(obj, unittest.TestCase):
            return self.loadTestsFromTestCase(obj)
        elif type(obj) == types.UnboundMethodType:
            return obj.im_class(obj.__name__)
        elif callable(obj):
            test = obj()
            if not isinstance(test, unittest.TestCase) and \
               not isinstance(test, unittest.TestSuite):
                raise ValueError, \
                      "calling %s returned %s, not a test" % (obj,test)
            return test
        else:
            raise ValueError, "don't know how to make test from: %s" % obj

    def loadTestsFromNames(self, names, module=None):
        """Return a suite of all tests cases found using the given sequence
        of string specifiers. See 'loadTestsFromName()'.
        """
        suites = []
        for name in names:
            suites.append(self.loadTestsFromName(name, module))
        return self.suiteClass(suites)

    def getTestCaseNames(self, testCaseClass):
        """Return a sorted sequence of method names found within testCaseClass
        """
        testFnNames = filter(lambda n,p=self.testMethodPrefix: n[:len(p)] == p,
                             dir(testCaseClass))
        for baseclass in testCaseClass.__bases__:
            for testFnName in self.getTestCaseNames(baseclass):
                if testFnName not in testFnNames:  # handle overridden methods
                    testFnNames.append(testFnName)
        if self.sortTestMethodsUsing:
            testFnNames.sort(self.sortTestMethodsUsing)
        return testFnNames



defaultTestLoader = TestLoader()


##############################################################################
# Patches for old functions: these functions should be considered obsolete
##############################################################################

def _makeLoader(prefix, sortUsing, suiteClass=None):
    loader = TestLoader()
    loader.sortTestMethodsUsing = sortUsing
    loader.testMethodPrefix = prefix
    if suiteClass: loader.suiteClass = suiteClass
    return loader

def getTestCaseNames(testCaseClass, prefix, sortUsing=cmp):
    return _makeLoader(prefix, sortUsing).getTestCaseNames(testCaseClass)

def makeSuite(testCaseClass, prefix='test', sortUsing=cmp, suiteClass=TestSuite):
    return _makeLoader(prefix, sortUsing, suiteClass).loadTestsFromTestCase(testCaseClass)

def findTestCases(module, prefix='test', sortUsing=cmp, suiteClass=TestSuite):
    return _makeLoader(prefix, sortUsing, suiteClass).loadTestsFromModule(module)


##############################################################################
# Text UI
##############################################################################

class _WritelnDecorator:
    """Used to decorate file-like objects with a handy 'writeln' method"""
    def __init__(self,stream):
        self.stream = stream

    def __getattr__(self, attr):
        return getattr(self.stream,attr)

    def writeln(self, *args):
        if args: apply(self.write, args)
        self.write('\n') # text-mode streams translate to \r\n if needed

#nor mal test runner
class NorTestRunner(TestRunner):
    """A test runner class that displays results in textual form.

    It prints out the names of tests as they are run, errors as they
    occur, and a summary of the results at the end of the test run.
    """
    """A test result class that can be stored as any format.

    Used by TextTestRunner.
    """
    separator1 = '=' * 70
    separator2 = '-' * 70

    #from test result
#    def __init__(self, stream, descriptions, verbosity):
#        TestResult.__init__(self)
#        self.stream = stream
#        self.showAll = verbosity > 1
#        self.dots = verbosity == 1
#        self.descriptions = descriptions
#	self.testStepResults=[]
    #for test runner
    def __init__(self, stream=sys.stderr, descriptions=1, verbosity=1,result_queue=None):
        TestRunner.__init__(self,result_queue)
        self.stream = _WritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity
	self.testStepResults=[]
        self.dots = verbosity == 1
        self.showAll = verbosity > 1
#not need to make result when testrunner and test result combine
#    def _makeResult(self):
#        #return _TextTestResult(self.stream, self.descriptions, self.verbosity)
#        return _NorTestResult(self.stream, self.descriptions, self.verbosity)

    def getDescription(self, test):
        if self.descriptions:
            return test.shortDescription() or str(test)
        else:
            return str(test)

    def startTest(self, test):
        TestRunner.startTest(self, test)
        if self.showAll:
            self.stream.write(self.getDescription(test))
            self.stream.write(" ... ")

    def addSuccess(self, test):
        TestRunner.addSuccess(self, test)
	#tsr=TestStepResult(self.getDescription(test))
	#tsr.testStatus="PASS"
	#tsr.assertItems=test.assertItems
	#self.testStepResults.append(tsr)
	#print tsr.assertItems

	#add paser here to store results
        if self.showAll:
            self.stream.writeln("ok")
        elif self.dots:
            self.stream.write('.')

    def addError(self, test, err):
        TestRunner.addError(self, test, err)
	tsr=TestStepResult(self.getDescription(test))
	tsr.testStatus="ERROR"
	tsr.assertItems=test.assertItems
	self.testStepResults.append(tsr)
        if self.showAll:
            self.stream.writeln("ERROR")
        elif self.dots:
            self.stream.write('E')
        if err[0] is KeyboardInterrupt:
            self.shouldStop = 1

    def addFailure(self, test, err):
        TestRunner.addFailure(self, test, err)
	tsr=TestStepResult(self.getDescription(test))
	tsr.testStatus="FAIL"
	tsr.assertItems=test.assertItems
	self.testStepResults.append(tsr)
        if self.showAll:
            self.stream.writeln("FAIL")
        elif self.dots:
            self.stream.write('F')

    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        for test, err in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s: %s" % (flavour,self.getDescription(test)))
            self.stream.writeln(self.separator2)
            for line in apply(traceback.format_exception, err):
                for l in string.split(line,"\n")[:-1]:
                    self.stream.writeln("%s" % l)
    def run(self, test):
        "Run the given test case or test suite."
	#should be not use result and test case not need pass test result as paramater
        #result = self._makeResult()
        #startTime = time.time()
        #test(result)
	#not need to create testresult, and pass self test runner
        startTime = time.time()
        test(self)
        stopTime = time.time()
        timeTaken = float(stopTime - startTime)
        self.printErrors()
        self.stream.writeln(self.separator2)
        run = self.testsRun
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run, run == 1 and "" or "s", timeTaken))
        self.stream.writeln()
        if not self.wasSuccessful():
            self.stream.write("FAILED (")
            failed, errored = map(len, (self.failures, self.errors))
            if failed:
                self.stream.write("failures=%d" % failed)
            if errored:
                if failed: self.stream.write(", ")
                self.stream.write("errors=%d" % errored)
            self.stream.writeln(")")
        else:
            self.stream.writeln("OK")
        #return result

##############################################################################
# Facilities for running tests from the command line
##############################################################################

class TestProgram:
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
    def __init__(self, module='__main__', defaultTest=None,
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
        #self.parseArgs(argv)
        #self.runTests()

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
	#print "XXXXXXXXXXXXXXXXXXXXX %S" %self.testNames
#	print self.testNames
#        self.test = self.testLoader.loadTestsFromNames(self.testNames,
#                                                       self.module)
	self.test=TestSuite()
	self.testLoader.loadTestFlow(Main,self.test)

    def runTests(self):
        if self.testRunner is None:
            self.testRunner = NorTestRunner(verbosity=self.verbosity)
        #result = self.testRunner.run(self.test)
        self.testRunner.run(self.test)
	print "X"*20
	for re in self.testRunner.testStepResults:
		print ("%s" %re.testName).ljust(50) + re.testStatus +"  "
		print re.assertItems[0].assertName
	print "X"*20
        sys.exit(not self.testRunner.wasSuccessful())
    def run(self):
	self.createTests()
	self.runTests()

main = TestProgram


##############################################################################
# Executing this module from the command line
##############################################################################

if __name__ == "__main__":
    main(module=None)
