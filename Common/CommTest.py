
from CommFactory import *

if __name__=="__main__":
    #config = Configure('SFTConfig.txt')
    log = Log()
    log.Open('test.log')
    com=CommFactory.CreateComm("SSHPexpect", log)
    com.SendReturn('tt')
    com.RecvTerminatedBy()
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
