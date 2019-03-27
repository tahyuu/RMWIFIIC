        engine = create_engine('sqlite:///:memory:', echo=True)
        Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        session = Session()
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
        startTime=datetime.datetime.now().strftime('%c')
        tr=TestResults(serialNumber=SN,socketId=Socket,sequenceId="%s" %testIndex,testName=testName,testValue=testValue,hiLimit=hiLimit,lowLimit=lowLimit,testType=testType,testStatus=testStatus,startTime=self.startTime,endTime=self.endTime,testDescription=testDescription,sendCommand=sendCommand,reciveMsg=reciveMsg)

