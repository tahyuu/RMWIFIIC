#class TestItemResult:
	#def __init__(self, Name, Desc, Value, HLimit, LLimit):
#	def __init__(self, Name): 
#		self._Name = Name
#		self._Desc = Desc
#		self._Value = Value
#		self.HLimit = HLimit
#		self.LLimit = LLimit
#please update the name to TestCaseResult in future
class TestStepResult:
#	def __init__(self,testName,testDescription,testUnit,testValue,testHilim,testLolim,testStatus,testRule,testTarget,testType):
#	def __init__(self,testName,testValue,testHilim,testLolim,testStatus):
	def __init__(self,testName, testStatus="passed"):
	
		self.testName=testName
		#self.testDescription=testDescription
		self.testDescription=""
#		self.testUnit=testUnit
		#self.testValue=""
		#self.testHilim=""
		#self.testLolim=""
		self.testStatus=testStatus
		#self.testLog = ""
		#self.testRule=""
		#self.errorMsg=""
		#self.errorCode=""
#		self.testTarget=testTarget
#		self.testType=testTyp
class TestAssert:
	def __init__(self,assertName):
		self.assertName=assertName
		#self.testValue=0
		self.testValue=""
		self.testHilim=""
		self.testLolim=""
		self.expValue=""
		self.testStatus=True
		self.testRule=""
		self.errorCode=""
		self.errorMsg=""
		self.testLog = ""
#	def Update(self):
		
		#update the expvalue for 
		#self.expValue="X=%s"
