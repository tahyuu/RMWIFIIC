#
# Simple example which uses a pool of workers to carry out some tasks.
#
# Notice that the results will probably not come out of the output
# queue in the same in the same order as the corresponding tasks were
# put on the input queue.  If it is important to get the results back
# in the original order then consider using `Pool.map()` or
# `Pool.imap()` (which will save on the amount of code needed anyway).
#
# Copyright (c) 2006-2008, R Oudkerk
# All rights reserved.
import time
import random
import os
import sys
import copy
import Queue

#from TS import TS
from Log import Log
#from PDU import PDU

#from DiagP import DiagP
from Consumer import *

from multiprocessing import Process,Pool, JoinableQueue, current_process, freeze_support
from multiprocessing import Queue as MultiprocessingQueue
from multiprocessing import Lock
#from TestStepDemo1 import *

class MulPools():
	def __init__(self,NUMBER_OF_PROCESSES):

	    self.NUMBER_OF_PROCESSES = NUMBER_OF_PROCESSES
	    self.TASK_COUNT = 0
	    # Create queues
	    self.task_queue = JoinableQueue()
	    self.done_queue = MultiprocessingQueue()
	    self.lock=Lock()

	    # Submit tasks
	def SubmitTasks(self, TASKS):
	    # Enqueue jobs
            self.TASK_COUNT = len(TASKS)
#	    for i in range(self.TASK_COUNT):
#       		 self.task_queue.put()
	    for task in TASKS:
		time.sleep(0.1)
		self.task_queue.put(task)
	    self.task_queue.join()
	    #tasks.join()
        
    	# Start worker processes
	def Start(self):
	    #num_consumers = multiprocessing.cpu_count()
	    #print ('Creating %d consumers' % self.NUMBER_OF_PROCESSES)
	    consumers = [ Consumer(self.task_queue, self.done_queue)
                  for i in range(self.NUMBER_OF_PROCESSES) ]
	    for w in consumers:
       		 w.start()

	def PrintResult(self):
	   for i in range(self.TASK_COUNT):
	         print '\t', self.done_queue.get()

	def PopResult(self):
	    results=[]
	    while True:
	        try:
	             queue_data = self.done_queue.get_nowait()
		     results.append(queue_data)
	    	except Queue.Empty:
	       	     if self.done_queue.qsize() < 1:
		        break
	    return results

        # Tell child processes to stop
 	def Stop(self): 
	    # Add a poison pill for each consumer
	    for i in range(self.NUMBER_OF_PROCESSES):
	        self.task_queue.put(None)
                
	    # Wait for all of the tasks to finish
	    self.task_queue.join()
	def Term(self):
		pass



if __name__ == '__main__':
    freeze_support()
    #TASKS1 = [("DiagE", (i, "","test")) for i in range(20)]
    #TASKS2 = [("DiagE", (i, "","test")) for i in range(10)]
    TASKS1=[] 
    TASKS2=[] 
    log=Log('abc.txt')
    log.Open('a')
    #ts=TS(log,"192.168.42.220","1")
    #ts.Connect("1") 

    lock=Lock()
    #ts=TS(log,"192.168.42.220","1")
    #ts.Connect("1") 
    #args(logpath,tsip,tsport)
    args1=("abc1.txt","192.168.42.220","1") 
    args2=("abc2.txt","192.168.42.220","2") 
    args3=("abc3.txt","192.168.42.220","3") 
    args4=("abc4.txt","192.168.42.220","4") 
    args5=("abc5.txt","192.168.42.220","5") 
    args6=("abc6.txt","192.168.42.220","6") 
    args7=("abc7.txt","192.168.42.220","7") 
    args8=("abc8.txt","192.168.42.220","8") 
    args9=("abc9.txt","192.168.42.220","9") 
    #args=("","","")
   # args1=(log,ts) 
    #args=(log,"",ts)

    #pdu1 = PDU(log, "192.168.42.230", "1")
    #pdu2 = PDU(log, "192.168.42.230", "2")
    #pdu1.OFF()
    #pdu2.OFF()
    #time.sleep(2)
    #pdu1.ON()
    #pdu2.ON()
   # for i in xrange(1):
   #    TASKS1.append(Task(["BootIntoBootMode.BootIntoBootMode","DiagReadEEP.DiagReadEEP","DiagP.DiagP","DiagE.DiagE","BootJunOS.BootJunOS","DPI_IPD.DPI_IPD","JunSFPInfo.JunSFPInfo","SFP8GetMAC.SFP8GetMAC","SFP8SetJITCFGAndReboot.SFP8SetJITCFGAndReboot","JITTest.JITTest"],args,1))

#    TASKS1.append(Task(["BootIntoBootMode.BootIntoBootMode","DiagReadEEP.DiagReadEEP","DiagP.DiagP","DiagE.DiagE","BootJunOS.BootJunOS","DPI_IPD.DPI_IPD","JunSFPInfo.JunSFPInfo","SFP8GetMAC.SFP8GetMAC","SFP8SetJITCFGAndReboot.SFP8SetJITCFGAndReboot","JITTest.JITTest"],args1,1))
    TASKS1.append(Task(["BootIntoBootMode.BootIntoBootMode","DiagReadEEP.DiagReadEEP","DiagP.DiagP","DiagE.DiagE"],args1,1,))
    TASKS1.append(Task(["BootIntoBootMode.BootIntoBootMode","DiagReadEEP.DiagReadEEP","DiagP.DiagP","DiagE.DiagE"],args2,2,))
    TASKS1.append(Task(["BootIntoBootMode.BootIntoBootMode","DiagReadEEP.DiagReadEEP","DiagP.DiagP","DiagE.DiagE"],args3,3,))
    TASKS1.append(Task(["BootIntoBootMode.BootIntoBootMode","DiagReadEEP.DiagReadEEP","DiagP.DiagP","DiagE.DiagE"],args4,4,))
    TASKS1.append(Task(["BootIntoBootMode.BootIntoBootMode","DiagReadEEP.DiagReadEEP","DiagP.DiagP","DiagE.DiagE"],args5,5,))
    TASKS1.append(Task(["BootIntoBootMode.BootIntoBootMode","DiagReadEEP.DiagReadEEP","DiagP.DiagP","DiagE.DiagE"],args6,6,))
    TASKS1.append(Task(["BootIntoBootMode.BootIntoBootMode","DiagReadEEP.DiagReadEEP","DiagP.DiagP","DiagE.DiagE"],args7,7,))
    TASKS1.append(Task(["BootIntoBootMode.BootIntoBootMode","DiagReadEEP.DiagReadEEP","DiagP.DiagP","DiagE.DiagE"],args8,8,))
    TASKS1.append(Task(["BootIntoBootMode.BootIntoBootMode","DiagReadEEP.DiagReadEEP","DiagP.DiagP","DiagE.DiagE"],args1,1,))
    TASKS1.append(Task(["BootIntoBootMode.BootIntoBootMode","DiagReadEEP.DiagReadEEP","DiagP.DiagP","DiagE.DiagE"],args9,9,))
    #TASKS1.append(Task(["BootIntoBootMode.BootIntoBootMode","DiagReadEEP.DiagReadEEP","DiagP.DiagP","DiagE.DiagE","BootJunOS.BootJunOS","DPI_IPD.DPI_IPD","JunSFPInfo.JunSFPInfo","SFP8GetMAC.SFP8GetMAC","SFP8SetJITCFGAndReboot.SFP8SetJITCFGAndReboot","JITTest.JITTest"],args2,2))
    #for i in xrange(15):
    #   TASKS1.append(Task("DiagE.DiagE",args))
       #TASKS2.append(Task(3,i))
    mw =MulPools(9)
    mw.Start()
    mw.SubmitTasks(TASKS1)
#    print mw.PopResult()
#    mw.SubmitTasks(TASKS2)
#    print mw.PopResult()
    mw.Stop()
    #pdu1.OFF()
    #pdu2.OFF()


