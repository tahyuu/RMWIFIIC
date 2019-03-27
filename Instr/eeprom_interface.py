import getpass
import sys
import telnetlib
from optparse import OptionParser
import sys
import time
import paramiko
import os

from sys import argv

'''
Raspberry eeprom fuctioni list
1,  write
    paramaters:  write eeprom_file
    example1: write eeprom_file_to_burn.lua.gz
    return:
        1:write to RF Card
        2:read  from RF card
        3:compare  compare the write and read file
'''
if __name__=="__main__":
    logs=""
    #cmd= argv[1:]
    startTime=time.time()
    cmd=" ".join(["%s" %v for v in argv[1:]])
    ssh= paramiko.SSHClient()
    #ssh.load_system_host_keys() 
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect(hostname,port,username,pkey=key)
    ssh.connect('192.168.1.28', username = 'pi', password='raspberry', timeout = 300)
    #copy the file
    '''
    rm /tmp/eeprom*
    echo 1 > /sys/module/mchp_11xx/parameters/write_enable
    cp /tmp/eeprom_file_to_burn.lua.gz /dev/nvram
    cp /dev/nvram /tmp/eeprom_out.lua.gz
    diff /tmp/eeprom_file_to_burn.lua.gz /tmp/eeprom_out.lua.gz
    '''
    cmd_file_clear="rm /tmp/eeprom*"
    cmd_write_enable="echo 1 > /sys/module/mchp_11xx/parameters/write_enable"
    cmd_cp_to_rf="cp /tmp/eeprom_file_to_burn.lua.gz /dev/nvram"
    cmd_cp_from_rf="cp /dev/nvram /tmp/eeprom_out.lua.gz"
    cmd_scp_to_rasp="scp eeprom_file_to_burn.lua.gz pi@192.168.1.28:/tmp/"
    cmd_diff="diff /tmp/eeprom_file_to_burn.lua.gz /tmp/eeprom_out.lua.gz"
    cmd_query_pass="echo $?"
    cmd_chdir="c:/FTS/"
    #step 0 change the current work folder
    os.chdir(cmd_chdir)

    #step 1 clear all the lua.gz file in raspberry /tmp/*.lua.gz
    #stdin, stdout, stderr = ssh.exec_command(cmd_file_clear)
    stdin, stdout, stderr = ssh.exec_command("%s;echo $?;" %cmd_file_clear)
    result=stdout.read()
    if result.strip()=="0":
        print "PASS"
    else:
        print "FAIL"

    #step 2 scp the eeprom_file_to_burn.lua.gz file from test pc to raspberry
    os.system(cmd_scp_to_rasp)

    #step 3 change the write enalbe file
    #step 4 write the eeprom_file_to_burn.lua.gz to raspberry
    #step 5 read the nvram file
    #step 6 diff the write file and read file
    cmd_list=[]
    #cmd_list=[cmd_write_enable,cmd_cp_to_rf,cmd_cp_from_rf,cmd_diff]
    cmd_list=[cmd_write_enable,cmd_cp_to_rf,cmd_cp_from_rf,cmd_diff]
    for cmd in cmd_list: 
        flag=False
        for i in range(3):
            print cmd
            stdin, stdout, stderr = ssh.exec_command("%s;echo $?;"%cmd)
            result=stdout.read()
            if result.strip()=="0":
                flag=True
                break
            else:
                time.sleep(5)
        if flag:
            print "PASS"
        else:
            print "FAIL"
    #f=open("test.txt",'a')
    print logs
    #f.write(logs)
    ssh.close()

