import time
import re
class TestStepResult():
	def __init__(self,testIndex):
		self.testIndex=testIndex
		self.stepName=""
		self.testStatus=True
		self.testResult=""
		#self.startTime=time.strftime('%d/%m/%Y %H:%M:%S')
		self.startTime=time.time()
		self.endTime=0
		self.testTime=0
		self.expendVar={}
		self.highLimit=0
		self.lowLimit=0
		self.log=""
		self.logformatstr=""
		self.recordResults=True
		self.testGroup=""
	def getValue(self,ss):
		result=""
		try:
			try:
				result=eval("self.%s" %ss)
			except:
				result=eval("self.expendVar[\"%s\"]" %ss)
		except:
			pass
		return result
	def Format(self):
		itemArray=[]
		formatstr=self.logformatstr
		result = re.findall("(?<=\$)\w+(?=\$)", formatstr)
		i=0
		for rr in result:
			i=i+1
			itemvalue=self.getValue(rr)
			if itemvalue:
				itemArray.append(itemvalue)
			else:
				itemArray.append("")
			formatstr=formatstr.replace("$"+rr+"$","%s")

		self.log=formatstr %tuple(itemArray)
	def Submit(self):
		self.endTime=time.time()
		self.testTime=self.endTime-self.startTime
		if self.testStatus:
			self.testResult="PASS"
		else:
			self.testResult="FAIL"

		self.Format()
