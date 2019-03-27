import getpass
import sys
import telnetlib
from optparse import OptionParser
import sys
import time
import paramiko

from sys import argv

'''
Raspberry spi fuctioni list
1,spi_write 
    paramaters: reg1=val1,reg2=val2 
    example1: spi_write 0x00=0x01
    example2: spi_write 0x00=0x01,0x01=0x00,0x03=0x00
2,spi_read
    paramaters: reg1,reg2
    example1: spi_read 0x00
    example2: spi_read 0x00,0x01,0x03,0x04
3,initRFIC
    paramaters: NONE
    example1: initRFIC
4,initRFICasTX
    paramaters: NONE
    example1: initRFICasTX
5,initRFICasRX
    paramaters: NONE
    example1: initRFICasRX
6,chip_off
    paramaters: NONE
    example1: chip_off
6,spi_read_all
    paramaters: NONE
    example1: spi_read_all
'''
if __name__=="__main__":
    #cmd= argv[1:]
    startTime=time.time()
    cmd=" ".join(["%s" %v for v in argv[1:]])
    ssh= paramiko.SSHClient()
    #ssh.load_system_host_keys() 
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect(hostname,port,username,pkey=key)
    ssh.connect('192.168.1.28', username = 'pi', password='raspberry', timeout = 300)
    cmd = './rfspi.py '+cmd
    stdin, stdout, stderr = ssh.exec_command(cmd)
    logs=stdout.read()
    print "%s\n%s" %(cmd,logs)
    f=open("test.txt",'a')
    f.write(logs)
    ssh.close()

