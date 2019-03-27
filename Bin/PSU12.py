from IVMM_DIO import *
import time
class PSU:
	def __init__(self):
		pass
	def PowerOn(self):
		#power on A socket
		Port="PA"
		ivmmdio=IVMM_DIO(4)
		for i_line in range(2):
			Line="0%d" %i_line
			Result=ivmmdio.On(Port,Line)
			if Result:
				print "Turn on the IVMM_DIO sucess!"
			else:
				print "Turn on the IVMM_DIO fail!"
			time.sleep(5)#default 3
		#power on B socket
		#Port="PA"
		#ivmmdio=IVMM_DIO(5)
		#for i_line in range(7):
		#	Line="0%d" %i_line
		#	Result=ivmmdio.On(Port,Line)
		#	if Result:
		#		print "Turn on the IVMM_DIO sucess!"
		#	else:
		#		print "Turn on the IVMM_DIO fail!"
		#	time.sleep(5)
		#power on C socket
		#Port="PA"
		#ivmmdio=IVMM_DIO(6)
		#for i_line in range(7):
		#	Line="0%d" %i_line
		#	Result=ivmmdio.On(Port,Line)
		#	if Result:
		#		print "Turn on the IVMM_DIO sucess!"
		#	else:
		#		print "Turn on the IVMM_DIO fail!"
		#	time.sleep(5)
		#power on D socket
		#ivmmdio=IVMM_DIO(7)
		#for i_line in range(7):
		#	Line="0%d" %i_line
		#	Result=ivmmdio.On(Port,Line)
		#	if Result:
		#		print "Turn on the IVMM_DIO sucess!"
		#	else:
		#		print "Turn on the IVMM_DIO fail!"
		#	time.sleep(5)

	def PowerOff(self):
		#reset sockets A
		ivmmdio=IVMM_DIO(4)
		Result=ivmmdio.Reset()
		time.sleep(5)#default 1
		#reset sockets B
		ivmmdio=IVMM_DIO(5)
		Result=ivmmdio.Reset()
		time.sleep(5)
		#reset sockets C
		ivmmdio=IVMM_DIO(6)
		Result=ivmmdio.Reset()
		time.sleep(5)
		#reset sockets D
		ivmmdio=IVMM_DIO(7)
		Result=ivmmdio.Reset()
if __name__=="__main__":
	psu=PSU()
	#psu.PowerOn()
	#time.sleep(60)
	psu.PowerOff()

