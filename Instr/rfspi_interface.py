#client  
  
import socket  
import time
from sys import argv
start=time.time()
HOST = "127.0.0.1"  
PORT = 3333  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
s.connect((HOST, PORT))  
#while 1:  
cmd=" ".join(["%s" %v for v in argv[1:]])
#cmd = raw_input('Your command:').strip()  
s.sendall(cmd)  
result = s.recv(1024)  
print result
#print time.time()-start
#print result  
s.close()  
