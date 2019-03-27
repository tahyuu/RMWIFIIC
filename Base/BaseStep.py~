#/bin/src
import os
import sys
#from Configs import *
from Vars import *
from m_TestStepResult import *
class BaseStep:
	def __init__(self,stepName="", stepVar=None):
		self.stepName = stepName
		self.gobalVars= gobalVars
#		self.configs= Configs()
		self.stepVar = stepVar
		self.testStepResult  = TestStepResult(stepName)
		pass
	def preStep(self):
		pass
	def postStep(self):
		pass
	def runStep(self):
		# start wirte you code here
		pass
		# end wirte you code here
	def run(self):
		self.preStep()
		self.runStep()
		self.postStep()
		return self.testStepResult


