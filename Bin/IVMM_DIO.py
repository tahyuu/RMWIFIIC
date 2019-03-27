import serial
import sys
import time
import re
from NumberC import *
class IVMM_DIO():
	def __init__(self,port=4):
		self.ser=serial.Serial(port=port,baudrate=9600,parity='N',stopbits=1,timeout=10,xonxoff=0,rtscts=0,dsrdtr=0)
		self.cmd_reset="830000000069"
	def hexShow(self,arv):
		result=''
		hLen=len(arv)
		for i in xrange(hLen):
			hvol=ord(arv[i])
			hhex='%02x' %hvol
			result+=hhex+''
		return result
	def On(self,Port,Line):
		#wholecmd="838741000169"
		cmd="8387"
		if Port.upper()=="PA":
			cmd=cmd+"41"
		elif Port.upper()=="PB":
			cmd=cmd+"42"
		elif Port.upper()=="PC":
			cmd=cmd+"43"
		elif Port.upper()=="PD":
			cmd=cmd+"44"
		cmd=cmd+Line+"0169"
		results= self.SendCommand(cmd)
		self.showStatus(results, Port)
		if len(results)==12:
			return True
		else:
			return False
	def Off(self,Port,Line):
		#cmd="838741000069"
		cmd="8387"
		if Port.upper()=="PA":
			cmd=cmd+"41"
		elif Port.upper()=="PB":
			cmd=cmd+"42"
		elif Port.upper()=="PC":
			cmd=cmd+"43"
		elif Port.upper()=="PD":
			cmd=cmd+"44"
		cmd=cmd+Line+"0069"
		results= self.SendCommand(cmd)
		self.showStatus(results, Port)
		if len(results)==12:
			return True 
		else:
			return True
	def Reset(self):
		results=self.SendCommand(self.cmd_reset)
		if len(results)== 12: 
			return True
		else:
			return False
	def showStatus(self, ins, Port):
		print ""
		print "Recived from DIO:"+ins
		
		if len(ins)==12:
			status= ins[8:10]
		print "Status:"+status
		status=hex2bin(status)
		#print status
		rt=''
		
		for i in range(len(status)-1,-1,-1):#10100001 to 1000001010
			rt+=status[i]
		if len(rt)<8:
			rt=rt+(8-len(rt))*"0"
		print "ReverseBits:"+rt
		i = 0
		print ""
		print "Line			Status"
		print "--------------------------------"
		for ch in rt:
			if ch   == "1":  
				print Port +str(i) +  "	 		ON"
				i=i+1
			elif ch   == "0":  
				print Port +str(i) +  "	 		OFF"
				i=i+1
		print "--------------------------------"

		
	def SendCommand(self,cmd):
		self.ser.write(cmd.decode("hex"))
		time.sleep(0.2)
		bufferamount=self.ser.inWaiting()
		readstr=self.ser.read(bufferamount)
		#if len(readstr)>0:
			#readstr=readstr.decode("hex")
			#readstr=readstr[0:-1]+'0'+readstr[-1]
		return self.hexShow(readstr)
 
	def Close(self):
		self.ser.close()
def Usage():
	print	
	print	
	print " Usage:python IVMM_DIO.py Port Line"
	print " Port:PA,PB,PC,PD"
	print " Line:00,01,02,03,04,05,06,07"
	print	
	print " Example: python IVMM_DIO.py [on|off] PA 07"
	print " "	
	print " "	
	print " "	
	print " "	
	print " "	

if __name__=="__main__":

	args=sys.argv
	if args[-1].lower()=="reset":
		ivmmdio=IVMM_DIO()
		Result=ivmmdio.Reset()
		if Result:
			print "Reset the IVMM_DIO sucess!"
		else:
			print "Reset the IVMM_DIO fail!"
		ivmmdio.Close()
	else:
		if len(args)>3:
			args=args[-3:]
		
		if len(args)<3 or type(args[0])!=type("PA") or type(args[1])!=type("01"):
			Usage()
		else:
			Function = str(args[0])
			Port=str(args[1])
			Line=str(args[2])

			#P_Flag=(args[0]).upper()=='PA' or (args[0]).upper()=='PB' or (args[0]).upper()=='PC' or (args[0]).upper()=='PD'
			#L_Flag=args[1]=="01" or args[1]=="02" or args[1]=="03" or args[1]=="04" or args[1]=="05" or args[1]=="06" or args[1]=="07"
			F_Flag = re.match('on|off|reset', Function.lower())
			P_Flag=re.match('PA|PB|PC|PD', Port.upper())
			L_Flag=re.match('00|01|02|03|04|05|06|07', Line)
		
			if F_Flag and P_Flag and L_Flag:
				ivmmdio=IVMM_DIO()
				if Function.lower()=="on":
					Result=ivmmdio.On(Port,Line)
					
					if Result:
						print "Turn on the IVMM_DIO sucess!"
					else:
						print "Turn on the IVMM_DIO fail!"
				elif Function.lower()=="off":
					Result=ivmmdio.Off(Port,Line)
					if Result:
						print "Turn off the IVMM_DIO sucess!"
					else:
						print "Turn off the IVMM_DIO fail!"
				elif Function.lower()=="reset":
					Result=ivmmdio.Reset()
					if Result:
						print "Reset the IVMM_DIO sucess!"
					else:
						print "Reset the IVMM_DIO fail!"
				ivmmdio.Close()
			else:
				Usage()
