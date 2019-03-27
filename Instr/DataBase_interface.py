#coding=utf-8
import MySQLdb
import os
from optparse import OptionParser
import sys
import time
class MySqlHelper:
    def __init__(self):
        self.log="sql_log\%s.log" %time.strftime('%Y-%m-%d',time.localtime(time.time()))
    def connect(self):
        self.conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='siklu')
        self.curs = self.conn.cursor()
    def close(self):
        self.curs.close()
        self.conn.close()
    def addNewCard(self,CardSerialNumber,Type=""):
        self.connect()
        sql=""
        try:
            Type=str(Type)
            if Type:
                sql = "INSERT IGNORE  into `Cards` (`SerialNumber`,`Type`) values ('%s', '%s');" %(CardSerialNumber,Type)
                self.curs.execute(sql)
                self.conn.commit()
                self.close()
                chipId=self.getChipType(CardSerialNumber)
                if chipId==Type:
                    pass
                else:
                    self.updateCardType(CardSerialNumber,Type)
            else:
                sql = "INSERT IGNORE into `Cards` (`SerialNumber`) values ('%s');" %CardSerialNumber
                self.curs.execute(sql)
                self.conn.commit()
                self.close()
        except MySQLdb.Error,e:
            self.conn.rollback()
            log=open(self.log,"a")
            ErrMsg='[{}] Add New Card Error!{}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),e)
            log.write(ErrMsg)
            self.close()
        finally:
            pass

    def getChipType(self,CardSerialNumber):
        chipType=""
        try:
            self.connect()
            sql="Select `Type` from `Cards` Where `SerialNumber`='%s';" %CardSerialNumber
            self.curs.execute(sql)
            data=self.curs.fetchone()
            if data:
                chipType=data[0]
            self.conn.commit()
        except MySQLdb.Error,e:
            self.conn.rollback()
            log=open(self.log,"a")
            ErrMsg='[{}] Get Chip Type Error!{}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),e)
            log.write(ErrMsg)
        finally:
            self.close()
    def updateCardType(self,CardSerialNumber,Type):
        #if True:
        sql="UPDATE IGNORE `Cards` SET `Type` = '%s' where `SerialNumber`='%s'" %(Type, CardSerialNumber)
        try:
            self.connect()
            self.curs.execute(sql)
            self.conn.commit()
            pass
        except MySQLdb.Error,e:
            self.conn.rollback()
            log=open(self.log,"a")
            ErrMsg='[{}] Update Card Type Error!{}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),e)
            log.write(ErrMsg)
        finally:
            self.close()
    def addNewRun(self,ts,boardID,BoardSN):
        if boardID:
            runID=0
            self.connect()
            sql = "INSERT IGNORE into `Runs`" ;
            if (boardID == -1):
                sql += "(`Timestamp`) values ( '" + str(ts) + "');";
            else:
                sql += "(`Timestamp` ,State, `Board ID`) values ( '" + str(ts) + "',0 , " + str(boardID) + ");";
            self.curs.execute(sql)
            runID= self.conn.insert_id()
            self.conn.commit()
            self.close()
            return runID
        if BoardSN:
            self.connect()
            runID=0
            sql= "";
            boardID = -1;
            self.connect()
            sql = "Select ID from `Cards` where `SerialNumber` = \'" + str(BoardSN) + "\';";
            self.curs.execute(sql)
            data=self.curs.fetchone()
            if data:
                boardID=data[0]
            self.conn.commit()
            self.close()
            runID=self.addNewRun(ts,boardID,"")
            #print runID
            return runID
    def addNewExecution(self,RunID, ts, testName, BoardSN,SetupName):
        testID=-1
        boardID=-1
        self.connect()
        sql = "Select ID from `Tests` where `Name` = \'" + testName + "\';";
        self.curs.execute(sql)
        data=self.curs.fetchone()
        if data:
            testID=data[0]
        sql = "Select ID from `Cards` where `SerialNumber` = " + str(BoardSN) + ";";
        self.curs.execute(sql)
        data=self.curs.fetchone()
        if data:
            boardID=data[0]
        self.conn.commit()
        self.close()
        ExecutionID=self.addNewExecution_with_ID(RunID, ts,testID,boardID,SetupName)
        #print ExecutionID
        return ExecutionID
    def addNewExecution_with_ID(self,RunID, ts, testID, boardID,setupName):
        executionID=-1
        sql = "INSERT IGNORE into `Executions` (`Timestamp` , `Test ID` , `Board ID`,`SetupName`, `RunID`) values ( '%s', %d, %d, '%s', %d );"%(str(ts),testID,boardID,setupName,RunID);
        try:
            self.connect()
            self.curs.execute(sql)
            executionID= self.conn.insert_id()
            self.conn.commit()
        except MySQLdb.Error,e:
            self.conn.rollback()
            ErrMsg='[{}] execut add new execution with ID Error!{}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),e)
            log=open(self.log,"a")
            log.write(ErrMsg)
        finally:
            self.close()
            #print executionID
            return executionID
    def updateExecutionDuration(ExecutionID, timestamp, ExecutionDuration,ExecutionNote):
        pass
    def excuteSql(self,sql):
        exectID=-1
        try:
            self.connect()
            self.curs.execute(sql)
            exectID= self.conn.insert_id()
            self.conn.commit()
            #print exectID
        except MySQLdb.Error,e:
            self.conn.rollback()
            log=open(self.log,"a")
            ErrMsg='[{}] execut excuteSql Error!{}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),e)
            log.write(ErrMsg)
        finally:
            self.close()
            return exectID
        pass
            
        

if __name__=="__main__":
        mysql=MySqlHelper()
        #mysql.excuteSql("INSERT INTO `RF TempSensor Calibration` (`Execution ID`,`System Temp`,`RfChip vTemp`,`RFIC Temperature Sensore (volts)`,`RFIC Temperature Sensore Reference (volts)`) VALUES (36,0,1.36613334945,1.36613334945,1.13736307)")
        #mysql.updateCardType('6360001438','001')
        #mysql.addNewExecution(47,'2017-3-14 6:21:04','RF TempSensor Calibration',636001433,'RF TempSensor Calibration')
        log_msg=""
    	parser=OptionParser()
	parser.add_option('-f','--function',\
			action='store',\
			dest='function_name',\
			help='''function name list: addNewCard(CardSerialNumber,Type)\n,addNewRun(Timestamp,boardID,BoardSN)\n,IOut(int CH),VOut(int CH),Output(int 0/1),Status(),IDN()''')
	parser.add_option('-p','--paramaters',\
			action='store',\
			dest='paramaters',\
			help='''function paramaters list: ISet(int CH,int Value),VSet(int CH,int Value),IOut(int CH),VOut(int CH),Output(int 0/1),Status(),IDN()''')
	(options,args)=parser.parse_args()
	if len(args)!=0:
		sys.exit("Usage: MySqlHelper.py [options]")
	func_name=options.function_name
	paramaters=options.paramaters
        logMsg=""
	try:
            if paramaters:
                #print "mysql.%s(%s)" %(func_name,paramaters)
	        returnValue=eval("mysql.%s(%s)" %(func_name,paramaters))
            else:
	        returnValue=eval("mysql.%s()" %(func_name))
            if paramaters:
                logMsg='[{}] Excute {}({}) No Error!\n\t\t\t{}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),func_name,paramaters,returnValue)
            else:
                logMsg='[{}] Excute {}() No Error!\n\t\t\t{}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),func_name,returnValue)
            print str(returnValue).strip()
	except Exception,e:
            if paramaters:
                logMsg='[{}] Excute {}({}) Error Type Error!{}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),func_name,paramaters,e)
            else:
                logMsg='[{}] Excute {}() Error Type Error!{}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),func_name,e)
        finally:
            log=open(mysql.log,"a")
            log.write(logMsg)

            #print ErrMsg
            pass
        #os.system("pause")
		#print  Exception, ":", 
