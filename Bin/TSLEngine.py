import multiprocessing
import os
import sys
#from TS import *
#sys.path.append("E:\Work\MTS\Model")
#sys.path.append("E:\Work\MTS\Apps\Demo")
#sys.path.append("E:\Work\MTS\Apps\Demo\PSL")
#sys.path.append("E:\Work\MTS\Apps\Demo\TestSteps")
#sys.path.append("E:\Work\MTS\Apps\Demo\Base")
#sys.path.append("E:\Work\MTS\Apps\Demo\Configs")
#sys.path.append("E:\Work\MTS\Apps\Demo\Vars")
from E0995122 import *
#import PSL
#import PSL_LN3000


from MulPools import *
from m_TestUUT import *
from m_TestStepResult import *
from MtsInt_StationConfig import *
from Log import *
from globalvar import *
from datetime import *
import time

class TSLModel:
    def __init__(self):
        self.tslName = ""
        self.isLeaf = False
        self.preTSL=()
        self.postTSL=()
        self.tsl = []
        self.recordResults=True
        self.expValue=""

class TSLComponent:
    def __init__(self,tslName):
        self.tslName = tslName
        self.tsl=[]
        self.isLeaf = False
        self.preTSL=()
        self.postTSL=()
        self.tsl = []
        self.recordResults=True
        self.expValue=""
    def Add(self,com):
        pass
    def Run(self,parent):
        self.parent=parent
        pass



class TSLLeaf(TSLComponent):
    def __init__(self,tslName):
        self.tslName = tslName
        self.tslModel= ""
        self.tslClass= ""
        self.recordResults=True
        self.expValue=""
        if len(tslName.split(".")) > 1:
            self.tslModel= tslName.split(".")[0]
            self.tslClass= tslName.split(".")[1]
        
    def Add(self,com):
        pass
    def Run(self,parent):
        self.parent=parent
        global daemonStopSignal,mutex,uutStatusArr

        #get the daemonStopSignal
        test_demonStopSignal=daemonStopSignal.value
        #start tsl test
        tsl=self.tslName
        flag_PrePostTSL=True
        if type(tsl)!=type("") and (tsl.preTSL is not ""):
            flag_PrePostTSL=RunPrePostTSL(tsl.preTSL,self.parent.testUUTs)
        #preTSL fuction detail

        #get the daemonStopSignal
        test_demonStopSignal=daemonStopSignal.value
        #when the all the test stoped.or the stop button pushed. we need to excute the PostTSL function
        if test_demonStopSignal==1:
            if type(tsl)!=type("") and (tsl.postTSL is not ""):
                RunPrePostTSL(tsl.postTSL,self.parent.testUUTs)
            #break
            return
        #when the preTSL return false we will no excute the test item .and the program will quit. and run the Post TSL
        if not flag_PrePostTSL:
            if type(tsl)!=type('') and (tsl.postTSL is not ""):
                RunPrePostTSL(tsl.postTSL,self.parent.testUUTs)
            #break
            return
        TASKS=[]
        #All Sockets test status it will record if there is any passed socket is running. if there is no socket is running all the program will exit
        All_sockets_status=False
        #read the socktes file get sockets
        k=0
        for testUUT in self.parent.testUUTs:
            socket=self.parent.testsockets[testUUT.testIndex]
            #get the daemonStopSignal
            test_demonStopSignal=daemonStopSignal.value
            if test_demonStopSignal==1:
                if tsl.postTSL is not "":
                    RunPrePostTSL(tsl.postTSL,self.parent.testUUTs)
                break
        #set all sockets status to All_sockets_status
        #when all the test sockets failed. the test program will not excute
            All_sockets_status=All_sockets_status or testUUT.testStatus
        #when the test result is false(the uut test failed) the program will not send the task to the mulpool.
                    ###################################################################
                    #please skip below line when relese test program
                    ###################################################################
                    #        testUUT.testStatus=True
            if testUUT.testStatus:
              #o_task=Task(tsl.tsl,(testUUT.log_path+"/"+testUUT.log_filename,socket.ip,str(socket.comPort)),testUUT.testIndex,tsl.tslName,tsl.recordResults,testUUT.sN)
                                #if type(tsl)!=type(""):
                                #    o_task=Task(tsl.tsl,(testUUT.log_path+"/"+testUUT.log_filename,socket.ip,str(socket.comPort)),testUUT.testIndex,tsl.tslName,tsl.recordResults,testUUT)
                                #    TASKS.append(o_task)
                o_task=Task([tsl],(testUUT.log_path+"/"+testUUT.log_filename,socket.ip,str(socket.comPort)),testUUT.testIndex,self.tslName,self.recordResults,testUUT)
                TASKS.append(o_task)

            k=k+1
        #when all the sockets is failed. and the program will exit
                    ###################################################################
                    #please skip below 3 line when relese test program
                    ###################################################################
        if not All_sockets_status:

            #break
            return
        #submit task to multi pool to excute
        self.parent.testEngine.mp.SubmitTasks(TASKS)
        #i=i+1
        

        if type(tsl)!=type('') and (tsl.postTSL is not ""):
            RunPrePostTSL(tsl.postTSL,self.parent.testUUTs)
            #postTSL fuction detail



class TSLComposite(TSLComponent):
    def __init__(self,tslName):
	self.parent=None
        self.tslName = tslName
        self.tsl=[]
    def Add(self,com):
        self.tsl.append(com)
    def Run(self,parent):
	#self.parent=parent
        for tsl in self.tsl: 
            if type(tsl)==type(""):
                pass
            else:
                tsl.Run(parent)

class TSLEngine():
    def __init__(self, maintsldic,parent):
	self.testCount=0
	self.tsldic = maintsldic 
	self.parent=parent
        #self.maintsl = self.CreateTSL(self.tsldic)
        self.testTree=self.CreateTSL(self.tsldic)
        poolmaxcount=10
        poolcount = len(self.parent.testUUTs)<poolmaxcount and len(self.parent.testUUTs) or poolmaxcount
        print "pool count is %s" %poolcount
        self.mp=MulPools(poolcount)
    def CreateTSL(self, tsldic):
        self.parent.tslCreated=True
        #self.testCount=0
        if tsldic.has_key("testflow"):
            currenttsl = TSLComposite(tsldic['tsfName'])
        else:
            currenttsl = TSLLeaf(tsldic['tslName'])
        if tsldic.has_key("tsfName"):
            currenttsl.tslName = tsldic["tsfName"]
        #pre Tsl action
        if tsldic.has_key("setUp"):
            currenttsl.preTSL=tsldic["setUp"]
        else:
            currenttsl.preTSL=()
        #has post Tsl action
        if tsldic.has_key("tearDown"):
            currenttsl.postTSL=tsldic["tearDown"]
        else:
            currenttsl.postTSL=()
        #record results
        if tsldic.has_key("recordResults"):
            currenttsl.recordResults=tsldic["recordResults"]
        else:
            currenttsl.recordResults=True
        if tsldic.has_key("expValue"):
           currenttsl.expValue=tsldic["expValue"]
        else:
           currenttsl.expValue=""
        if tsldic.has_key("testflow"):
            for tstr in tsldic["testflow"]:
                currenttsl.isLeaf = len(tstr.split(".")) > 1
                tslname = currenttsl.isLeaf and tstr.split(".")[1] or tstr.split(".")[0]
                #tsl_model=__import__(str('E0995122'))
            #currenttsl.Add(self.CreateTSL(getattr(tsl_model, tslname)))
            #self.testCount=self.testCount+1

                if not currenttsl.isLeaf: 
                #currenttsl.tsl.append(self.CreateTSL(getattr(self.parent.m_TSLfile, tslname)))
                            #tsl_model=__import__(str(tslname))
                    tsl_model=__import__(str('E0995122'))
                    currenttsl.Add(self.CreateTSL(getattr(tsl_model, tslname)))
                #currenttsl.Add(self.CreateTSL(getattr(self.parent.m_TSLfile, tslname)))
                else:
                        #currenttsl = TSLLeaf(tsldic['tslName'])
                    currenttsl.Add(TSLLeaf(tstr))
                    self.testCount=self.testCount+1
                #currenttsl.tsl.append(currenttsl)
                #self.testCount=self.testCount+1

        return currenttsl
    def Run(self):
        pass
        #self.testTree.Run()
    def CreateTSL2(self, tsldic):
        self.parent.tslCreated=True
        #self.testCount=0
        currenttsl = TSLModel()
        if tsldic.has_key("tsfName"):
            currenttsl.tslName = tsldic["tsfName"]
        #pre Tsl action
        if tsldic.has_key("setUp"):
            currenttsl.preTSL=tsldic["setUp"]
        else:
            currenttsl.preTSL=()
        #has post Tsl action
        if tsldic.has_key("tearDown"):
            currenttsl.postTSL=tsldic["tearDown"]
        else:
            currenttsl.postTSL=()
        #record results
        if tsldic.has_key("recordResults"):
            currenttsl.recordResults=tsldic["recordResults"]
        else:
            currenttsl.recordResults=True
        if tsldic.has_key("expValue"):
           currenttsl.expValue=tsldic["expValue"]
        else:
            currenttsl.expValue=""
            if tsldic.has_key("testflow"):
                for tstr in tsldic["testflow"]:
                        #print tstr
                    currenttsl.isLeaf = len(tstr.split(".")) > 1
#			print currenttsl.isLeaf
                    tslname = currenttsl.isLeaf and tstr.split(".")[1] or tstr.split(".")[0]

                    if not currenttsl.isLeaf: 
#				print self.parent
                #currenttsl.tsl.append(self.CreateTSL(getattr(self.parent.m_TSLfile, tslname)))
	                        #tsl_model=__import__(str(tslname))
                        currenttsl.tsl.append(self.CreateTSL(getattr(self.parent.m_TSLfile, tslname)))
                    else:
                        currenttsl.tsl.append(tstr)
                #currenttsl.tsl.append(currenttsl)
                self.testCount=self.testCount+1
                                #print "tsl cont plus 111111111111111111111111 %s" %self.testCount
            
        return currenttsl
        #print self.maintsl.tsl
    def RunTest(self):
        #print self.testCount
        i=0
        for testUUT in self.parent.testUUTs:
            testUUT.testCount=self.testCount
            self.parent.testUUTs[i]=testUUT
            i=i+1
        
        self.PrepareForEachTest()
#		if self.maintsl.preTSL is not "":
#			RunPrePostTSL(self.maintsl.preTSL,socket,self.parent.testUUTs)
#			print "run mainstl set up"
	#self.parent.daemonStopSignal is the singnal from worker.it indicate the work is stop or not,if the work is stoped,the testengine will stop to run.
        global daemonStopSignal,mutex
        #get the daemonStopSignal
        if mutex.acquire():
            daemonStopSignal.value=0
            mutex.release()
        self.mp.Start()
        #test_demonStopSignal=False
        #print "tsl in main is %s" %self.maintsl.tslName
        #print "tsl in main tsl count is  %s" %len(self.maintsl.tsl)
        self.testTree.Run(self.parent)
        time.sleep(3)
        self.mp.Stop()
       
        pass
    def RunTest2(self):
        #print self.testCount
        i=0
        for testUUT in self.parent.testUUTs:
            testUUT.testCount=self.testCount
            self.parent.testUUTs[i]=testUUT
            i=i+1
        
        self.PrepareForEachTest()
#		if self.maintsl.preTSL is not "":
#			RunPrePostTSL(self.maintsl.preTSL,socket,self.parent.testUUTs)
#			print "run mainstl set up"
	#self.parent.daemonStopSignal is the singnal from worker.it indicate the work is stop or not,if the work is stoped,the testengine will stop to run.
        global daemonStopSignal,mutex
        #get the daemonStopSignal
        if mutex.acquire():
            daemonStopSignal.value=0
            mutex.release()
        self.mp.Start()
        i=0
        #test_demonStopSignal=False
        #print "tsl in main is %s" %self.maintsl.tslName
        #print "tsl in main tsl count is  %s" %len(self.maintsl.tsl)
        for tsl in self.maintsl.tsl:

            #print "sub tsl is %s" %tsl.tslName
            #get the daemonStopSignal
            test_demonStopSignal=daemonStopSignal.value
            #start tsl test
            flag_PrePostTSL=True
            if type(tsl)!=type("") and (tsl.preTSL is not ""):
                flag_PrePostTSL=RunPrePostTSL(tsl.preTSL,self.parent.testUUTs)
            #preTSL fuction detail

            #get the daemonStopSignal
            test_demonStopSignal=daemonStopSignal.value
            #when the all the test stoped.or the stop button pushed. we need to excute the PostTSL function
            if test_demonStopSignal==1:
                if type(tsl)!=type('') and (tsl.postTSL is not ""):
                    RunPrePostTSL(tsl.postTSL,self.parent.testUUTs)
                    #print "break................................"
                break
            #when the preTSL return false we will no excute the test item .and the program will quit. and run the Post TSL
            if not flag_PrePostTSL:
                if type(tsl)!=type('') and (tsl.postTSL is not ""):
                    RunPrePostTSL(tsl.postTSL,self.parent.testUUTs)
                    #print "break................................"
                break
            TASKS=[]
            #All Sockets test status it will record if there is any passed socket is running. if there is no socket is running all the program will exit
            All_sockets_status=False
            #read the socktes file get sockets
            k=0
            for testUUT in self.parent.testUUTs:
                socket=self.parent.testsockets[testUUT.testIndex]
                #get the daemonStopSignal
                test_demonStopSignal=daemonStopSignal.value
                if test_demonStopSignal==1:
                    if tsl.postTSL is not "":
                        RunPrePostTSL(tsl.postTSL,self.parent.testUUTs)
                    break
            #set all sockets status to All_sockets_status
            #when all the test sockets failed. the test program will not excute
                All_sockets_status=All_sockets_status or testUUT.testStatus
            #when the test result is false(the uut test failed) the program will not send the task to the mulpool.
                        ###################################################################3
                        #please skip below line when relese test program
                        ###################################################################3
                        #        testUUT.testStatus=True
                if testUUT.testStatus:
                    #o_task=Task(tsl.tsl,(testUUT.log_path+"/"+testUUT.log_filename,socket.ip,str(socket.comPort)),testUUT.testIndex,tsl.tslName,tsl.recordResults,testUUT.sN)
                                    #print "test step is %s ........................" %type(tsl)
                                    if type(tsl)!=type(""):

                                        o_task=Task(tsl.tsl,(testUUT.log_path+"/"+testUUT.log_filename,socket.ip,str(socket.comPort)),testUUT.testIndex,tsl.tslName,tsl.recordResults,testUUT)
                                        TASKS.append(o_task)

                k=k+1
            #when all the sockets is failed. and the program will exit
                        ###################################################################3
                        #please skip below 3 line when relese test program
                        ###################################################################3
            if not All_sockets_status:
                                #print "break................................333333333333333"
                break
            #submit task to multi pool to excute
            #print TASKS
            self.mp.SubmitTasks(TASKS)
            i=i+1
            

            if type(tsl)!=type('') and (tsl.postTSL is not ""):
                RunPrePostTSL(tsl.postTSL,self.parent.testUUTs)
                #postTSL fuction detail
        self.mp.Stop()
#		time.sleep(1.2)
        #self.PrepareForEachTest()
        if self.maintsl.postTSL is not "":
            RunPrePostTSL(self.maintsl.postTSL,self.parent.testUUTs)
        #self.WriteTestResultToLog()
            #run maintsl.clearup
#			pass
#the failbreak can aviabel if the test code has no change on the RunTest().
#beacause the test RunTrunkTest and RunLeafTest will stop when the test testStatus is false in testUUT model,so the multi_pool add the items in,but when it check the test status is false it will be stop
    def PrepareForEachTest(self):
#		self.logpath="/home/tester/MTS/testlog"
        self.logpath=StationOptions["LogPath"]
        self.StationName=StationOptions["StationName"]
        self.TestDate = datetime.now().strftime("%Y%m%d")
        self.savepath = self.logpath + '/' + self.StationName + '/' + self.TestDate
        if os.path.exists(self.savepath):
            #print self.savepath
            #print "YES"
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

                testUUT.log_filename = testUUT.sN + '_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.log'
                testUUT.log_path = self.savepath
                self.parent.testlogfiles.append(testUUT.log_path + '/' + testUUT.log_filename)
                                #print testUUT.log_path + '/'
                                #print  os.path.exists(testUUT.log_path+'/')
                if not os.path.exists(testUUT.log_path):
                    os.makedirs(testUUT.log_path)
                                #print testUUT.log_path + '/' + testUUT.log_filename
                #testUUT.log = Log(testUUT.log_path + '/' + testUUT.log_filename)
                testUUT.log = Log()
                testUUT.log.Open(testUUT.log_path + '/' + testUUT.log_filename)
                testUUT.log.Print('                                                  ')
                testUUT.log.Print('##################################################')
                testUUT.log.Print('Station : '.rjust(20) + self.StationName)
                testUUT.log.Print('Date : '.rjust(20) + self.TestDate)
                testUUT.log.Print('SerialNumber : '.rjust(20) + testUUT.sN)
                #testUUT.log.PrintNoTime('UUTType : '.rjust(20) + testUUT.pN)
                testUUT.log.Print('UUTType : '.rjust(20) + self.parent.TSLfile)
                #self.TSLfile = str(StationOptions["TestProgram"]).replace(".py","")
                #testUUT.log.PrintNoTime('PDUIP : '.rjust(20) + self.pduip)
                #testUUT.log.PrintNoTime('PDUPort : '.rjust(20) + self.pduport)
                #testUUT.log.PrintNoTime('TSIP : '.rjust(20) + self.tsip)
                testUUT.log.Print('TSIP : '.rjust(20) + socket.ip)
                testUUT.log.Print('TSPort : '.rjust(20) + str(socket.comPort))
                testUUT.log.Print('UUT Index : '.rjust(20) + str(testUUT.testIndex + 1))
                testUUT.log.Print('##################################################')
                testUUT.log.Print('Start Testing: --------------------')
                testUUT.log.Print('##################################################')
                self.parent.testUUTs[k]=testUUT
                k=k+1

    def WriteTestResultToLog(self):
        #print self.parent.testUUTs
        for testUUT in self.parent.testUUTs:
            #strResult="-----------------Test Result:"+(testUUT.testStatus and "PASS" or "FAIL")+"--------------------------"
            #strResult+="\n"
            #strResult+="------------------Test Time:"+str(int(testUUT.testTime))+"s-----------------------------"
            #strResult+="\n"
            strResult='\n'+('Test Result:'+(testUUT.testStatus and "PASS" or "FAIL")).center(60,'-')+'\n'+('Test Time:'+str(int(testUUT.testTime))).center(60,'-')+'\n'
            strResult+="#############################################################################################"+"\n"
            for testItem in testUUT.testItems:
                #check the testItem need to write into log file
                if testItem.recordResults:
                    strResult+=testItem.testGroup.ljust(20)+" => ".rjust(10)+testItem.testName.replace("Section","").ljust(30)+"         "+(testItem.testStatus and "PASS" or "FAIL")
                    strResult+="\n"
            strResult+="#############################################################################################"
            testUUT.log.Open("a")
            testUUT.log.Write(strResult,testUUT.log_path + '/' + testUUT.log_filename)
    def PopResults(self):
        #update the results list
        self.results=self.mp.PopResult()
        for result in self.results:
             i=0
             for testUUT in self.parent.testUUTs:
                if result.testIndex==testUUT.testIndex:
                        #update the test status of testUUT
                    #if not result.testStatus:
                    #    if testUUT.testStatus and result.recordResults:
                    #            testUUT.testStatus=False
		    for assertitem in result.assertItems:

                        if not assertitem.testStatus:
                            if testUUT.testStatus and result.recordResults:
                                testUUT.testStatus=False
                    #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXX test UUT status is : %s" %(testUUT.testStatus)

                    testUUT.testItems.append(result)
                    testUUT.endTime=result.endTime
                    #testUUT.endTime=time.time()
                    testUUT.testTime=testUUT.endTime-testUUT.startTime
                    self.parent.testUUTs[i]=testUUT
                    break
                i=i+1

def RunPrePostTSL(prepostTSL,testUUTs):
    import re
    returnFlag=True
    #print prepostTSL
    for item in prepostTSL:
        #print prepostTSL
        #print item
	#get the expValue
	#if not item:
	#	break
	expValue=""
	funName=""
	ArrayFun=item.split("|")
	if len(ArrayFun)>1:
            expValue=ArrayFun[0]
            item=ArrayFun[1]
	elif len(ArrayFun)==1:
            item=ArrayFun[0]

	#print item
	#time sleep function
	sleep_arg_match=re.search("(?<=time.sleep\()\d+",item)
	if sleep_arg_match:
            sleeptime=sleep_arg_match.group()
            time.sleep(int(sleeptime))
        continue

	#other funtion
	#get the function name
	args=()
	fun_name_match=re.search("[\s\S]+(?=\()",item)
	if fun_name_match:
            funcName=fun_name_match.group()
	else:
            funcName=item
        #print funcName
	#get the function args
	fun_arg_match=re.search("(?<=\()[\s\S]+[^\)]",item)
	if fun_arg_match:
            args=fun_arg_match.group().split(",")
	#item=prepostTSL 
	#testpackage,teststepfile,teststepclass = funcName.split('.')
        if funcName.find('.')<=0:
            continue
	teststepfile,teststepclass = funcName.split('.')
        #m_import=__import__("%s.%s" % ("Instr",teststepfile))
        m_import=__import__("%s" % (teststepfile))
        m_testStep=getattr(m_import,teststepfile)
        o_testStep=m_testStep()
	c_testStep = getattr(o_testStep,teststepclass)
	if not expValue:
            c_testStep(*args)

	else:
            result=c_testStep(*args)
        if expValue == result:
            returnFlag=True
        else:
            returnFlag=False
        
    return returnFlag


if __name__ == "__main__": 

	manager = multiprocessing.Manager()
	testUUTs= manager.list()
	i=0
	snList=["1234","1111"]
	for sn in snList:
            if sn:
                testUUT = TestUUT(i)
                testUUT.sN = sn
                testUUTs.append(testUUT)
#			self.testUUTs.append(TestUUT(i))
            i = i  +  1
#	print len(testUUTs)
	parent = None


	tslengine=TSLEngine(Main,parent)
	#tslengine.RunTest(testUUTs)
#	RunTest(tslengine.maintsl,testUUTs,tslengine.testCount)
	#w=Worker1()
	#w.run()

