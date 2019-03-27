#!/usr/bin/python 
from SSHParamiko import *
from SSHPexpect import *
from Subprocess import *

class CommFactory():
    @staticmethod
    def CreateComm(type,log):
        if type == 'SSHParamiko':
            return SSHParamiko(log)
        elif type == 'SSHPexpect':
            return SSHPexpect(log)
	elif type =='Subprocess':
	    return Subprocess(log)
	elif type =='comm232':
	    return Comm232(log)




if __name__=="__main__":
    #home_dir = os.environ['FT']	    
    config = Configure('SFTConfig.txt')
    log = Log()
    log.Open('test.log')
    #eventManager = EventManager()
    #com=CommFactory.CreateComm("Subprocess",config)
    #com.SendReturn('lspci -vvn')
    #com.RecvTerminatedBy()
    #com=CommFactory.CreateComm("SSHPexpect",config)
    #com.SendReturn('lspci -vvn')
    #com.RecvTerminatedBy()
    com=CommFactory.CreateComm("Comm232",log)
    com.log=log
    com.SendReturn('lspci -vvn')
    com.RecvTerminatedBy()
     
	

