# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import datetime
Base = declarative_base()
class TestResults(Base):
    __tablename__ = 't_TestResults'
    #id = Column('id',Integer, primary_key=True)
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    serialNumber=Column("serialNumber",String(10))
    socketId=Column("socketId",String(10))
    sequenceId=Column("sequenceId",String(10))
    testName = Column("testName",String(50))
    testValue= Column('testValue',Integer)
    hiLimit = Column("hiLimit",String(20))
    lowLimit = Column("lowLimit",String(20))
    testType= Column("testType",String(20))
    testStatus= Column("testStatus",Boolean)
    startTime =Column("startTime",String(30))
    endTime = Column("endTime",String(30))
    testDescription= Column("testDescription",String(30))
    sendCommand= Column("sendCommand",String(20))
    reciveMsg= Column("reciveMsg",String(20))
if __name__=="__main__":
	#engine = create_engine('sqlite:///Config/%s' %StationOptions["TestProgramDataBase"])
	#engine = create_engine('sqlite:///testResults.db')
	engine = create_engine('sqlite:///:memory:', echo=True)
	Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
	session = Session()
	# to careate the data base tables
	Base.metadata.create_all(engine) 
	testName="This is a test item for development"
	testDescription="this is Description for test items"
	testValue="V1.00"
	hiLimit="V1.00"
	lowLimit="V1.00"
	testType="Equal"
	sendCommand="ver"
	reciveMsg="V1.00"
	SN="RMS0995122G008"
	Socket="4"
	#tr=TestResults(serialNumber=SN,socketId=Socket,sequenceId="%s" %i,testName=testName,testValue=testValue,hiLimit=hiLimit,lowLimit=lowLimit,testType=testType,startTime=startTime,endTime=startTime,testDescription=testDescription,sendCommand=sendCommand,reciveMsg=reciveMsg)

	for i in xrange(10):
		startTime=datetime.datetime.now().strftime('%c')
		tr=TestResults(serialNumber=SN,socketId=Socket,sequenceId="%s" %i,testName=testName,testValue=testValue,hiLimit=hiLimit,lowLimit=lowLimit,testType=testType,testStatus=1,startTime='Sun 08 Apr 2018 02:37:50 PM',endTime='',testDescription=testDescription,sendCommand=sendCommand,reciveMsg=reciveMsg)
		session.add(tr)
		session.commit()
		

		#endTime=datetime.datetime.now().strftime('%c')

