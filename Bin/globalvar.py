import multiprocessing
#from multiprocessing.sharedctypes import Value,Array
from multiprocessing import Process, Value, Array

mutex=multiprocessing.Lock()
#daemonStopSignal=False
daemonStopSignal=Value('i',0)
sn_list=[]
uutStatusArr = Array('i', 100)

