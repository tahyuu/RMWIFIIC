import getpass
import sys
import telnetlib
from optparse import OptionParser
import sys
import time

class N9020A:
    def __init__(self):
        self.Host='192.168.1.3'
        self.port='5023'
    def Open(self):
        self.tn = telnetlib.Telnet(self.Host,port=self.port,timeout=3)
        self.tn.read_until("SCPI>")
    def WriteRead(self,cmd):
        self.Open()
        self.tn.write("%s\n" %cmd)
        Response=self.tn.read_until("SCPI>")
        self.tn.close()
        return Response.split('\r')[0].strip()
    def Reset(self):
        'reset'
        self.Open()
        self.tn.write("*RST\n")
        Response=self.tn.read_until("SCPI>")
        self.tn.close()
        return Response.split('\r')[0].strip()
    def enableHarmonicMixer(self,vw):
        '''"Init spectrum to use external mixer and setup the type of Harmonic mixer to use:
        V  11970V
        W  11970W"'''
        self.Open()
        self.tn.write("*RST\n")
        Response=self.tn.read_until("SCPI>")
        self.tn.write(":INPUT:MIX EXT;:SENS:MIX:BAND %s;:SENS:MIX:BIAS:STATE ON\n" %vw)
        #self.tn.write(":INPUT:MIX EXT;:SENS:MIX:BAND V;:SENS:MIX:BIAS:STATE ON\n")
        Response=self.tn.read_until("SCPI>")
        #self.tn.write(":INPUT:MIX EXT;\n")
        #Response=self.tn.read_until("SCPI>")
        #self.tn.write(":SENS:MIX:BAND %s;\n" %Value)
        #Response=self.tn.read_until("SCPI>")
        #self.tn.write(":SENS:MIX:BIAS:STATE ON\n")
        #Response=self.tn.read_until("SCPI>")
        self.tn.close()
        return Response.split('\r')[0].strip()
    def setSweepMode(self,Status):
        '''set Single/continuous sweep of the SA
        sigle:If used need to wait for sweep to end
        continuous:continuous sweep of the SA'''
        self.Open()
        if Status=="Continuous":
            self.tn.write(":INITiate:CONTinuous ON\n" )
        else:
            self.tn.write(":INITiate:CONTinuous OFF\n" )
        Response=self.tn.read_until("SCPI>")
        self.tn.close()
        return Response.split('\r')[0].strip()
    def getSweepTime(self):
        '''get sweep time'''
        #self.Open()
        self.tn.write(":SWEep:TIME?\n")
        Response=self.tn.read_until("SCPI>")
        #self.tn.close()
        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        print Response
        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        return Response.split('\r')[0].strip()
    def setCenterFrequency(self,centerFrequency):
        'set center frequency'
        self.Open()
        self.tn.write(":FREQuency:CENTer %sHZ\n" %centerFrequency)
        #self.tn.write(":FREQuency:CENTer %s\n" %centerFrequency)
        Response=self.tn.read_until("SCPI>")
        self.tn.close()
        return Response.split('\r')[0].strip()
    def getCenterFrequency(self):
        'get center frequency'
        self.Open()
        self.tn.write(":FREQuency:CENTer?\n")
        Response=self.tn.read_until("SCPI>")
        self.tn.close()
        return Response.split('\r')[0].strip()
    def setReferenceLevel(self,refLevel):
        'set reference level'
        self.Open()
        self.tn.write(":DISPlay:WINDow:TRACe:Y:SCALe:RLEVel %s\n" %refLevel)
        Response=self.tn.read_until("SCPI>")
        self.tn.close()
        return Response.split('\r')[0].strip()
    def setSpan(self,span):
        'set span'
        self.Open()
        self.tn.write(":FREQuency:SPAN %s\n" %span)
        Response=self.tn.read_until("SCPI>")
        self.tn.close()
        return Response.split('\r')[0].strip()
    def setResolutionBW(self,rbw):
        'set resolution bw'
        self.Open()
        self.tn.write(":BANDwidth:RESolution %s\n" %span)
        Response=self.tn.read_until("SCPI>")
        self.tn.close()
        return Response.split('\r')[0].strip()
    def setVideoBW(self,vbw):
        'set video bw'
        self.Open()
        self.tn.write(":BANDwidth:VIDeo %s\n" %span)
        Response=self.tn.read_until("SCPI>")
        self.tn.close()
        return Response.split('\r')[0].strip()
    def amplitudeGetScale(self):
        'amplitude get scale'
        self.Open()
        self.tn.write(":DISPlay:WINDow:TRACe:Y:SCALe:PDIVision?\n")
        Response=self.tn.read_until("SCPI>")
        self.tn.close()
        return Response.split('\r')[0].strip()
    def peakSearch(self,markerId=1):
        'search Peak'
        self.Open()
        self.tn.write(":CALCulate:MARKer%s:MAXimum\n" %markerId)
        Response=self.tn.read_until("SCPI>")
        self.tn.close()
        return Response.split('\r')[0].strip()
    def getFrequency(self,markerId=1):
        'search Peak'
        self.Open()
        self.tn.write(":CALCulate:MARKer%s:X?\n" %markerId)
        Response=self.tn.read_until("SCPI>")
        self.tn.close()
        return Response.split('\r')[0].strip()
    def getLevel(self,markerId=1):
        'search Peak'
        self.Open()
        self.tn.write(":CALCulate:MARKer%s:Y?\n" %markerId)
        Response=self.tn.read_until("SCPI>")
        self.tn.close()
        return Response.split('\r')[0].strip()
    def moveToCenterFrequency(self,markerId=1):
        'move marker to center frequency'
        self.Open()
        self.tn.write(":CALCulate:MARKer%s:SET:CENTer\n" %markerId)
        Response=self.tn.read_until("SCPI>")
        self.tn.close()
        return Response.split('\r')[0].strip()
    def measurePeak(self,sweepMode,markerId=1):
        self.Open()
        f=-1000
        p=-1000
        #if sweepMode=='SINGLE':
        #    self.waitUntilSweepCompleted(True)
        self.tn.write(":INITiate:IMMediate;*OPC?\n")
        #self.tn.write(":INITiate:IMMediate;*OPC?")
        Response=self.tn.read_until("SCPI>")
        #print Response
	#self.peakSearch(markerId);
        self.tn.write(":CALCulate:MARKer1:MAXimum;:CALCulate:MARKer%s:X?;:CALCulate:MARKer%s:Y?\n" %(markerId,markerId))
        Response=self.tn.read_until("SCPI>")
        f,p=map(float, Response.split('\r')[0].strip().split(';'))
	#f=(self.getFrequency());
	#p=(self.getLevel());
        #print self.getScale()
	#self.setReferenceLevel(float(p) + float(self.getScale()));
	self.setReferenceLevel(float(p) + float(self.getScale()));
	#return "%s,%s" %(f,p);
	return Response.split('\r')[0].replace(';',',');
    def getScale(self):
        return 10
    def getScale_old(self):
        'get Scale'
        self.Open()
        self.tn.write(":DISPlay:WINDow:TRACe:Y:SCALe:PDIVision?\n")
        Response=self.tn.read_until("SCPI>")
        self.tn.close()
        return Response.split('\r')[0].strip()
    def takeSweep(self):
        'take Sweep'
        #self.Open()
        self.tn.write(":INITiate:IMMediate\n")
        Response=self.tn.read_until("SCPI>")
        #self.tn.close()
        return Response.split('\r')[0].strip()
    def waitUntilSweepCompleted(self,readSweepTime):
       	estimatedSweepTime = 0;
        if readSweepTime:
            estimatedSweepTime = float(self.getSweepTime());
	self.takeSweep();
	#more than second
        if estimatedSweepTime>1: #in miliseconds
		time.sleep(int(1000*float(estimatedSweepTime))); 
        if readSweepTime:
            self.waitUntilDone(estimatedSweepTime+5000);
            #self.waitUntilDone(estimatedSweepTime*1000+5);
    def waitUntilDone(self,timeout):
        read = ""
	endTime = 0
	#endTime = System.currentTimeMillis() + timeout;
	endTime = time.time()*1000.0 + timeout;
        while(time.time()*1000.0 <= endTime):
                #self.Open()
                self.tn.write("*OPC?\n")
                read=self.tn.read_until("SCPI>")
                #self.tn.close()
		#read = self.WriteRead("*OPC?");
                #if (not read.index("1")>-1):
                #    return;
                if read.find("1") >-1:
                    return
	#throw new TimeoutException();
    def configureSA(self,centerFreq,span,rbw,vbw,HMtype):
        self.Reset()
        self.enableHarmonicMixer(HMtype)
        self.setSpan(20e6)
        self.setReferenceLevel(-50)
        self.setCenterFrequency(centerFreq)
        sig = self.measurePeak('SINGLE')
        f,p = map(float, sig.split(','))
        self.moveToCenterFrequency(1)
        self.setReferenceLevel(p+self.getScale())
        self.setSpan(span)
        self.setResolutionBW(rbw)
        self.setVideoBW(vbw)
        sig = self.measurePeak('SINGLE',1)
        self.moveToCenterFrequency(1)
        return sig
    def Close(self):
        self.tn.close()


if __name__=="__main__":
	parser=OptionParser()
	parser.add_option('-f','--function',\
			action='store',\
			dest='function_name',\
			help='''function name list: ISet(int CH,int Value),VSet(int CH,int Value),IOut(int CH),VOut(int CH),Output(int 0/1),Status(),IDN()''')
	parser.add_option('-p','--paramaters',\
			action='store',\
			dest='paramaters',\
			help='''function paramaters list: ISet(int CH,int Value),VSet(int CH,int Value),IOut(int CH),VOut(int CH),Output(int 0/1),Status(),IDN()''')
	(options,args)=parser.parse_args()
	if len(args)!=0:
		sys.exit("Usage: N9020A.py [options]")
	func_name=options.function_name
	paramaters=options.paramaters
	n9020a=N9020A()
	try:
            if paramaters:
	        print eval("n9020a.%s(%s)" %(func_name,paramaters)).strip()
            else:
	        print eval("n9020a.%s()" %(func_name))
	except Exception,e:
		print  Exception, ":", e


#if __name__=="__main__":
#    n=N9020A()
#    n.Open()
#    print n.WriteRead("*IDN?")
#    n.Close()
#HOST = "192.168.1.3"
#user = raw_input("Enter your remote account: ")
#password = getpass.getpass()

#tn = telnetlib.Telnet(HOST,port=5023,timeout=2)

#tn.read_until("login: ")
#tn.write(user + "\n")
#if password:
#    tn.read_until("Password: ")
#    tn.write(password + "\n")

#tn.read_until("SCPI>")
#tn.write("*IDN?\n")
#print tn.read_until("SCPI>")
#tn.close()
#tn.write("exit\n")

#print tn.read_all()
