#!usr/bin/env python
from E0995122 import *
class TSLComponent:
    def __init__(self,tslName):
        self.tslName = tslName
        self.tsl=[]
        #self.isLeaf = False
        #self.preTSL=()
        #self.postTSL=()
        #self.tsl = []
        #self.recordResults=True
        #self.expValue=""
    def Add(self,com):
        pass
    def Run(self):
        pass



class TSLLeaf(TSLComponent):
    def __init__(self,tslName):
        self.tslName = tslName
        self.tslModel= ""
        self.tslClass= ""
        if len(tslName.split(".")) > 1:
            self.tslModel= tslName.split(".")[0]
            self.tslClass= tslName.split(".")[1]
        
    def Add(self,com):
        print "leaf can't add xxxxxxxxx"
    def Run(self):
        print "in leaf",
        print self.tslName


class TSLComposite(TSLComponent):
    def __init__(self,tslName):
        self.tslName = tslName
        self.tsl=[]
    def Add(self,com):
        self.tsl.append(com)
    def Run(self):
        for tsl in self.tsl: 
            print "--",
            if type(tsl)==type(""):
                print tsl
            else:
                tsl.Run()



class TSLEngine():
    def __init__(self):
        self.testCount=0
        pass
    def CreateTSL(self, tsldic):
        #self.parent.tslCreated=True
    	#self.testCount=0
        #print tsldic
        #print type(tsldic)
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
                #print tstr
    		currenttsl.isLeaf = len(tstr.split(".")) > 1
#			print currenttsl.isLeaf
    		tslname = currenttsl.isLeaf and tstr.split(".")[1] or tstr.split(".")[0]
                #tsl_model=__import__(str('E0995122'))
    		#currenttsl.Add(self.CreateTSL(getattr(tsl_model, tslname)))
    		#self.testCount=self.testCount+1

    		if not currenttsl.isLeaf: 
#				print self.parent
    			#currenttsl.tsl.append(self.CreateTSL(getattr(self.parent.m_TSLfile, tslname)))
                            #tsl_model=__import__(str(tslname))
                        tsl_model=__import__(str('E0995122'))
    			currenttsl.Add(self.CreateTSL(getattr(tsl_model, tslname)))
    			#currenttsl.Add(self.CreateTSL(getattr(self.parent.m_TSLfile, tslname)))
    		else:
    	                #currenttsl = TSLLeaf(tsldic['tslName'])
    			currenttsl.Add(TSLLeaf(tstr))
    			#currenttsl.tsl.append(currenttsl)
    			#self.testCount=self.testCount+1
                        #print "tsl cont plus 111111111111111111111111 %s" %self.testCount

    	return currenttsl
    def Run(self):
        self.testTree=self.CreateTSL(Main)
        self.testTree.Run()
			



if __name__=="__main__":
    #p=TSLComposite("Father")
    #p.Add(TSLLeaf("son1"))
    #son2=TSLComposite("son2")
    #son2.Add(TSLLeaf("son2_1"))
    #p.Add(son2)
    #p.Run()
    engine=TSLEngine()
    engine.Run()
