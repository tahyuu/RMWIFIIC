#!/usr/bin/env python
import os,  subprocess, time, sys
currentDir = os.getcwd()
#import the base py file
sys.path.append(currentDir +"/Common")

from Log import *
import ConfigParser	
from optparse import OptionParser
import pexpect
import commands
import random
import shutil
if 'linux' in sys.platform:
    my_os = 'linux'
    pass
    #from  pexpect import *
elif 'win32' in sys.platform:
    my_os = 'win32'
    from Color import *
    #from  winpexpect import *
from Configure import *
from Comm232 import *
import re
modelName=""

class TestItemResult:
    def __init__(self):
        self.testName=""
        self.lowValue=""
        self.HighValue=""
        self.testValue=""

class bcolors:
    def __init__(self):
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
    def print_blue_text(self,s):
        print "%s%s%s" %(self.OKBLUE,s,self.ENDC)
    def print_green_text(self,s):
        print "%s%s%s" %(self.OKGREEN,s,self.ENDC)
    def print_red_text(self,s):
        #return "%s%s%s" %(self.FAIL,s,self.ENDC)
        print "%s%s%s" %(self.FAIL,s,self.ENDC)

class RFWIFIIC():
    modelName=''
    def __init__(self,index):
        self.GetModelList()
        self.ErrorList=[]
        self.testItemResultList=[]
        self.cf = ConfigParser.ConfigParser()
        print RFWIFIIC.modelName
        self.cf.read('Model/'+RFWIFIIC.modelName)
        #print 'Model\\'+RFWIFIIC.modelName
        if my_os=='win32':
            self.color=Color()
        else:
            self.color=bcolors()
        #self.log_path = os.getcwd()
        self.testIndex=index
        #station config
        self.sn_re=self.cf.get("Station_Config", "sn_re")
        self.log_path =self.cf.get("Station_Config", "log_path")
        #print self.log_path
        self.station_name =self.cf.get("Station_Config", "station_name")
        self.fail_break=self.cf.get("Station_Config", "fail_break")
        #serial config
        self.uut_serial_port=self.cf.get("Serial_Config", "uut_port")
        self.gld_serial_port=self.cf.get("Serial_Config", "gld_port")
        self.PROMPT = self.cf.get("Serial_Config", "PROMPT")
        self.baudrate=self.cf.get("Serial_Config", "baudrate")
        self.bytesize=self.cf.get("Serial_Config", "bytesize")
        self.parity=self.cf.get("Serial_Config", "parity")
        self.stopbits=self.cf.get("Serial_Config", "stopbits")
        self.timeout=self.cf.get("Serial_Config", "timeout")
        self.xonxoff=self.cf.get("Serial_Config", "xonxoff")
        self.rtscts=self.cf.get("Serial_Config", "rtscts")
        #TX Critiera
        self.test_sequences=self.cf.get("TX_CRITIERA", "test_sequences")
        self.current_max_1m_low=self.cf.get("TX_CRITIERA", "current_max_1m_low")
        self.current_max_1m_high=self.cf.get("TX_CRITIERA", "current_max_1m_high")
        self.current_avg_1m_low=self.cf.get("TX_CRITIERA", "current_avg_1m_low")
        self.current_avg_1m_high=self.cf.get("TX_CRITIERA", "current_avg_1m_high")
        self.power_1m_low=self.cf.get("TX_CRITIERA", "power_1m_low")
        self.power_1m_high=self.cf.get("TX_CRITIERA", "power_1m_high")
        self.current_max_6m_low=self.cf.get("TX_CRITIERA", "current_max_6m_low")
        self.current_max_6m_high=self.cf.get("TX_CRITIERA", "current_max_6m_high")
        self.current_avg_6m_low=self.cf.get("TX_CRITIERA", "current_avg_6m_low")
        self.current_avg_6m_high=self.cf.get("TX_CRITIERA", "current_avg_6m_high")
        self.power_6m_low=self.cf.get("TX_CRITIERA", "power_6m_low")
        self.power_6m_high=self.cf.get("TX_CRITIERA", "power_6m_high")
        self.current_max_54m_low=self.cf.get("TX_CRITIERA", "current_max_54m_low")
        self.current_max_54m_high=self.cf.get("TX_CRITIERA", "current_max_54m_high")
        self.current_avg_54m_low=self.cf.get("TX_CRITIERA", "current_avg_54m_low")
        self.current_avg_54m_high=self.cf.get("TX_CRITIERA", "current_avg_54m_high")
        self.power_54m_low=self.cf.get("TX_CRITIERA", "power_54m_low")
        self.power_54m_high=self.cf.get("TX_CRITIERA", "power_54m_high")
        self.serial_number=self.cf.get("DEBUG", "serial_number")
        #debug
        self.test_sequences=self.cf.get("TX_CRITIERA", "test_sequences")
        self.debug_flag=self.cf.get("DEBUG", "debug")

        
        self.PASS = '\n \
  ***************************************************\n \
    #########       ##        #########   #########  \n \
    ##      ##    ##  ##     ##          ##          \n \
    ##      ##   ##    ##    ##          ##          \n \
    #########   ## #### ##    ########    ########   \n \
    ##          ##      ##           ##          ##  \n \
    ##          ##      ##           ##          ##  \n \
    ##          ##      ##   #########   #########   \n \
  ***************************************************\n'

        self.FAIL = '\n \
  ***************************************************\n \
    ##########      ##         ######    ##          \n \
    ##            ##  ##         ##      ##          \n \
    ##           ##    ##        ##      ##          \n \
    ########    ## #### ##       ##      ##          \n \
    ##          ##      ##       ##      ##          \n \
    ##          ##      ##       ##      ##          \n \
    ##          ##      ##     ######    #########   \n \
  ***************************************************\n'
        self.log=Log()




    def GetModelList(self):
        modelList=[]
        if RFWIFIIC.modelName!='':
            return
        p_ini_file=re.compile('^\S+ini$')
        p=re.compile('^\d+$')
        models = os.listdir('Model')
        print "Model List as below:" 
        print
        i=1
        for model in models:
            if p_ini_file.match(model):
                modelList.append(model)
                print " %s  :  %s" %(i,model)
                i=i+1
        print
        while True:
            self.modelIndex= raw_input("Please select the Model : ")
            if p.match(self.modelIndex) and 0<int(self.modelIndex)<i:
                break
        RFWIFIIC.modelName=modelList[int(self.modelIndex)-1]
        print 'You select Model is : %s' %RFWIFIIC.modelName
        
    def ScanData(self):
        ########################################
        #to create test log and ask SN
        ########################################
        if self.debug_flag=='True':
            a = raw_input("Please Input Enter to continue [%s] : " %RFWIFIIC.modelName.replace('.ini',''))
            return
        while True:
            self.serial_number = raw_input("Please Input Serial Number [%s] : "  %RFWIFIIC.modelName.replace('.ini',''))
            p = re.compile(self.sn_re)
            if p.match(self.serial_number):
                break

    def InitLog(self):
        self.testDate = datetime.now().strftime("%Y/%m/%d")
        self.testStartTime = datetime.now().strftime("%Y/%m/%d %H:%M")
        self.log_filename = self.serial_number + \
         '-' + datetime.now().strftime("%Y%m%d%H%M%S") + '.log'
        #to check if log_path is exist or not
        isExists = os.path.exists(self.log_path+'/TMP/')
        if not isExists: 
            os.makedirs(self.log_path+'/TMP/')
        isExists = os.path.exists(self.log_path+'/PASS/')
        if not isExists: 
            os.makedirs(self.log_path+'/PASS/')
        isExists = os.path.exists(self.log_path+'/FAIL/')
        if not isExists: 
            os.makedirs(self.log_path+'/FAIL/')

        self.log.Open(self.log_path + '//TMP//' + self.log_filename)
        self.log.PrintNoTime('')
        self.log.PrintNoTime('#########################################################')
        self.log.PrintNoTime('Station : %s' %self.station_name)
        self.log.PrintNoTime('Model   : ' + RFWIFIIC.modelName)
        self.log.PrintNoTime('Date    : ' + self.testDate)
        self.log.PrintNoTime('SN      : %s' %self.serial_number)
        self.log.PrintNoTime('#########################################################')
        self.log.PrintNoTime('')
    def TxTest(self):
        ########################################
        #to to TX Test
        #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        #1,open serial and set the 38400.
	#2,Pump out a window to ask operator to push the reset button.
	#3,receive the radiotool@CC3220: and send out 2 to enter the Tx task options
	#4,set tx interval to 10. input 7, -->10
	#5,set txframe amount to 200. input 9 -->200.
	#6,set txrate to 1M. 3 -->1
	#7,set txpower to 6. 4 -->6
        #option1 1Mbps, 6 6Mbps, 13 54Mbps
        ########################################
        rate_list=['1','6','54']
        rate_index=0
        self.config = Configure('Config.txt')
        for rate in ['1','6','13']: #(1:1Mbps, 6:6Mbps, 13:54Mbps)
            #self.uut_comm = Comm232(self.config, self.log, self.uut_serial_port)
            #self.uut_comm.setTimeout(2)              
            #self.uut_comm.SendReturn('')             # Enter
            #line = self.uut_comm.RecvTerminatedBy()  # |
            #self.uut_comm.SendReturn('2')            # 2  ---  to select Tx task options
            #line = self.uut_comm.RecvTerminatedBy()  # |
            #self.uut_comm.SendReturn('7')            # 7  ---  set tx interval value(7) to 10
            #line = self.uut_comm.RecvTerminatedBy()  # |
            #self.uut_comm.SendReturn('10')           # 10  ---- set tx interval 10.
            #line = self.uut_comm.RecvTerminatedBy()  # |
            #self.uut_comm.SendReturn('9')            # 9   ----   set tx fram amount(9) to 200
            #line = self.uut_comm.RecvTerminatedBy()  # |
            #self.uut_comm.SendReturn('200')          # 200 ---- set fram amount 200.
            #line = self.uut_comm.RecvTerminatedBy()  # |
            #self.uut_comm.SendReturn('3')            # 3  ----  set tx rate(3) to xMbps
            #line = self.uut_comm.RecvTerminatedBy()  # |
            #self.uut_comm.SendReturn('%s' %rate)     # 1  ---- set tx rate to 1Mbps.  (1:1Mbps, 6:6Mbps, 13:54Mbps)
            #line = self.uut_comm.RecvTerminatedBy()  # |
            #self.uut_comm.SendReturn('4')            # 4   ---   set tx power (4) to 6
            #line = self.uut_comm.RecvTerminatedBy()  # |
            #self.uut_comm.SendReturn('6')            # 6  ---- set tx power to  6
            #line = self.uut_comm.RecvTerminatedBy()  # |
            ############################################################
            # to push the reset(restart) button on N9010A signal analyzer
            ############################################################
    
            ############################################################
            # to push the Run/Stop button and set the DC Power analyzer Time/Div to 50ms/d
            ############################################################
    
            #self.uut_comm.SendReturn('5')            # 5  ---- start tx task
            #line = self.uut_comm.RecvTerminatedBy()  # |
    
            ############################################################
            # to push the Run/Stop button 
            ############################################################
    
            ############################################################
            # to fintune the DC power analyzer offset got get Current Max
            ############################################################
            while True:
                currentMax= raw_input("\nPlease input the DC Power Max Current for rate(%sMbps) : " %rate_list[rate_index])
                p = re.compile('^(\-|\+)?\d+(\.\d+)?$')
                if p.match(currentMax):
                    currentMax=float(currentMax)
                    break
                else:
                    print "the input Current Max [%s] is not in correct format. please try again"
            lowValue=float(eval('self.current_max_%sm_low' %rate_list[rate_index]))
            highValue=float(eval('self.current_max_%sm_high' %rate_list[rate_index]))
            testName="current_max_%sm_test" %rate_list[rate_index]
            tir=TestItemResult()
            tir.testName=testName
            tir.lowValue=lowValue
            tir.highValue=highValue
            tir.testValue=currentMax
            self.testItemResultList.append(tir)
            if lowValue<=currentMax<=highValue:
                pass
            else:
                self.ErrorList.append("current_max_%sm_test" %rate_list[rate_index])
                if self.fail_break=="True":
                    return

    
            ############################################################
            # to fintune the DC power analyzer offset got get Current Avg
            ############################################################
            while True:
                currentAvg= raw_input("\nPlease input the DC Power Avg Current for rate(%sMbps) : " %rate_list[rate_index])
                p = re.compile('^(\-|\+)?\d+(\.\d+)?$')
                if p.match(currentAvg):
                    currentAvg=float(currentAvg)
                    break
                else:
                    print "the input Current Avg [%s] is not in correct format. please try again" %rate_list[rate_index]
            lowValue=float(eval('self.current_avg_%sm_low' %rate_list[rate_index]))
            highValue=float(eval('self.current_avg_%sm_high' %rate_list[rate_index]))
            testName="current_avg_%sm_test" %rate_list[rate_index]
            tir=TestItemResult()
            tir.testName=testName
            tir.lowValue=lowValue
            tir.highValue=highValue
            tir.testValue=currentAvg
            self.testItemResultList.append(tir)
            if lowValue<=currentAvg<=highValue:
                pass
            else:
                self.ErrorList.append("current_avg_%sm_test" %rate_list[rate_index])
                if self.fail_break=="True":
                    return
    
            ############################################################
            # to get the Power on N9010A signal analyzer
            ############################################################
            while True:
                signalPower= raw_input("\nPlease input the Signal Power for rate(%sMbps) : " %rate_list[rate_index])
                p = re.compile('^(\-|\+)?\d+(\.\d+)?$')
                if p.match(signalPower):
                    signalPower=float(signalPower)
                    break
                else:
                    print "the input signal Power [%s] is not in correct format. please try again"
            lowValue=float(eval('self.power_%sm_low' %rate_list[rate_index]))
            highValue=float(eval('self.power_%sm_high' %rate_list[rate_index]))
            testName="power_%sm_test" %rate_list[rate_index]
            tir=TestItemResult()
            tir.testName=testName
            tir.lowValue=lowValue
            tir.highValue=highValue
            tir.testValue=signalPower
            self.testItemResultList.append(tir)
            if lowValue<=signalPower<=highValue:
                pass
            else:
                self.ErrorList.append("power_%sm_test" %rate_list[rate_index])
                if self.fail_break=="True":
                    return

            rate_index=rate_index+1

    def RxTest(self):
        #print line
        #return
        #self.gld_comm = Comm232(self.config, self.log, self.gld_serial_port)
        #self.gld_comm.setTimeout(2)
        #self.gld_comm.SendReturn('lspci')
        #line = self.gld_comm.RecvTerminatedBy()
        #self.gld_comm.SendReturn('lspci')
        #line = self.gld_comm.RecvTerminatedBy()
        #self.gld_comm.SendReturn('lspci')
        #line = self.gld_comm.RecvTerminatedBy()
        #self.gld_comm.SendReturn('lspci')
        #line = self.gld_comm.RecvTerminatedBy()
        #print line
        tx_rates=[1,6,13] 
        for tx_rate in tx_rates:
            pass
        
    def Run(self):
        self.ErrorList=[]
        self.testItemResultList=[]
        self.TxTest()
        
        if len(self.ErrorList)==0:
            self.testStatus=True
            self.log.PrintNoTime("")
            self.log.PrintNoTime("")
            self.log.Print("********************************************************")
            self.log.Print("ALL PASSED")
            self.log.Print("********************************************************")
            self.color.print_green_text('#########################################################')
            self.color.print_green_text('Station : %s' %self.station_name)
            self.color.print_green_text('Model   : ' + RFWIFIIC.modelName)
            self.color.print_green_text('Date    : ' + self.testDate)
            self.color.print_green_text('SN      : %s' %self.serial_number)
            self.color.print_green_text('#########################################################')
            print "Test Name".ljust(25)+ "Except Value".ljust(20)+"Test Value".ljust(10)
            self.log.Print("Test Name".ljust(25)+ "Except Value".ljust(20)+"Test Value".ljust(10))
            for item in self.testItemResultList:
                print item.testName.ljust(25)+("%s <= X <= %s" %(str(item.lowValue).rjust(5),item.highValue)).ljust(20)+str(item.testValue).rjust(10)
                self.log.Print(item.testName.ljust(25)+("%s <= X <= %s" %(str(item.lowValue).rjust(5),item.highValue)).ljust(20)+str(item.testValue).rjust(10))
            self.color.print_green_text(self.PASS)
            #movePASS='mv ' + self.log_path + '/TMP/' + self.log_filename + \
            #       ' ' + self.log_path + '/PASS/' + self.log_filename
            #print self.bc.BGPASS(self.log_path + '/PASS/' + self.log_filename)
            self.color.print_blue_text(self.log_path + '/FAIL/' + self.log_filename)
            self.log.Close()
            shutil.move(self.log_path + '/TMP/' + self.log_filename,self.log_path + '/PASS/' + self.log_filename)
            #os.system(movePASS)
        else:
            self.testStatus=False
            self.log.PrintNoTime("")
            self.log.PrintNoTime("")
            self.log.Print("********************************************************")
            self.log.Print("Test FAILED. %s HAS/HAVE ERROR" %(",".join(self.ErrorList)))
            self.log.Print("********************************************************")
            #print self.bc.BGFAIL(self.FAIL)
            self.color.print_red_text('#########################################################')
            self.color.print_red_text('Station : %s' %self.station_name)
            self.color.print_red_text('Model   : ' + RFWIFIIC.modelName)
            self.color.print_red_text('Date    : ' + self.testDate)
            self.color.print_red_text('SN      : %s' %self.serial_number)
            self.color.print_red_text('#########################################################')
            print "Test Name".ljust(25)+ "Except Value".ljust(20)+"Test Value".ljust(10)
            self.log.Print("Test Name".ljust(25)+ "Except Value".ljust(20)+"Test Value".ljust(10))
            for item in self.testItemResultList:
                print item.testName.ljust(25)+("%s <= X <= %s" %(str(item.lowValue).rjust(5),item.highValue)).ljust(20)+str(item.testValue).rjust(10)
                self.log.Print(item.testName.ljust(25)+("%s <= X <= %s" %(str(item.lowValue).rjust(5),item.highValue)).ljust(20)+str(item.testValue).rjust(10))
            self.color.print_red_text(self.FAIL)
            #print self.bc.BGPASS(self.log_path + '/FAIL/' + self.log_filename)
            self.color.print_blue_text(self.log_path + '/FAIL/' + self.log_filename)
            #moveFAIL='mv ' + self.log_path + '/TMP/' + self.log_filename + \
            #       ' ' + self.log_path + '/FAIL/' + self.log_filename
            #self.bc.BGFAIL(self.log_path + '/FAIL/' + self.log_filename)
            #print self.bc.BGFAIL(self.log_path + '/FAIL/' + self.log_filename)
            self.log.Close()
            shutil.move(self.log_path + '/TMP/' + self.log_filename,self.log_path + '/FAIL/' + self.log_filename)
            #os.system(moveFAIL)
    def Wait(self,seconds):
        count=0
        while (count < seconds):
            ncount = seconds - count
            sys.stdout.write("\r            %d " % ncount)
            sys.stdout.flush()
            time.sleep(1)
            count += 1
        while True:
            yes_no= raw_input("\nDo you want to start test[y/n]? : ")
            if str.upper(yes_no)=="Y" or str.upper(yes_no)=="YES":
                break
            else:
                pass
            

    def AMBTest(self,amb_index,askInput):
        #commmand for get AMB0 
        if amb_index==0:
            amb_address="92"
        elif amb_index==1:
            amb_address="94"
        elif amb_index==4:
            amb_address="90"
        else:
            return False
            self.log.Print("wrong AMB index, it should be 0,1,4")
        self.log.PrintNoTime("")
        self.log.PrintNoTime("")
        self.log.Print("********************************************************")
        self.log.Print("AMB_%s test section" %amb_index)
        self.log.Print("********************************************************")
        amb_cmd="raw 0x06 0x52 0x0d 0x%s 0x02 0x00" %amb_address
        if askInput:
            while True:
                str_amb_temp= raw_input("Please input AMB %s Sensor Temperature : " %amb_index)
                p = re.compile("^(\-|\+)?\d+(\.\d+)?$")
                if p.match(str_amb_temp):
		    if float(str_amb_temp)<=self.input_temp_high and self.input_temp_low<=float(str_amb_temp):
                    	break
		    else:
            	    	print self.bc.BGFAIL("input temp not in range [%s, %s]" %(self.input_temp_low,self.input_temp_high))
		else:
            	    print self.bc.BGFAIL("please input correct digital")
        else:
            str_amb_temp="30"

        test=""
        i=0
        while i<5:
            command=self.bmc_command_header %(self.bmc_ip,self.bmc_username,self.bmc_password,amb_cmd)
            self.SendReturn(command)
            test=self.RecvTerminatedBy().strip()
            if test.find("Communicate timeout")>=0:
                continue
            else:
                break
        try:
            real_temp=float(int(test.replace(" ","")[:3],16))/16
        except:
            real_temp="NA"
            test="NA"
        self.amb_sensores["amb%s_read_raw_data" %amb_index]=test
        self.amb_sensores["amb%s_read_temp" %amb_index]=real_temp
        self.amb_sensores["amb%s_real_temp" %amb_index]=str_amb_temp
        if not askInput:
            return True
        self.log.Print("SYS_AMB_TEMP_%s raw data is[ %s ]; temperature in IC is [ %s degrees C ]; temperature sensor read value is [%s degrees C]" %(amb_index,test,real_temp,str_amb_temp))
        amb_temp=float(str_amb_temp)
        if amb_temp-int(self.pass_qut) <= real_temp and real_temp<=amb_temp+int(self.pass_qut):
            self.log.Print("SYS_AMB_TEMP_%s temperature [ %s degrees C] is in range [ %s degrees C,%s degrees C]" %(amb_index,real_temp,amb_temp-int(self.pass_qut),amb_temp+int(self.pass_qut)))
            self.log.Print("AMB_%s test PASSED" %amb_index)
            print self.bc.BGPASS("PASSED: SYS_AMB_TEMP_%s temperature [ %s degrees C] is in range [ %s degrees C,%s degrees C]" %(amb_index,real_temp,amb_temp-int(self.pass_qut),amb_temp+int(self.pass_qut)))
            return True
        else:
            self.log.Print("SYS_AMB_TEMP_%s temperature [ %s degrees C] is out of range [ %s degrees C,%s degrees C]" %(amb_index,real_temp,amb_temp-int(self.pass_qut),amb_temp+int(self.pass_qut)))
            self.log.Print("AMB_%s test FAILED" %amb_index)
            self.ErrorList.append("SYS_AMB_TEMP_%s" %amb_index)
            print self.bc.BGFAIL("FAILED: SYS_AMB_TEMP_%s temperature [ %s degrees C] is out of range [ %s degrees C,%s degrees C]" %(amb_index,real_temp,amb_temp-int(self.pass_qut),amb_temp+int(self.pass_qut)))
            return False
        
if __name__=="__main__":
    while True:
        if True:
            cre=RFWIFIIC(1)
            cre.ScanData()
            #cre.Wait(cre.wait_time)
            #cre.Wait(4)
            cre.InitLog()
            cre.Run()
            write_str=""
            #write_str="serial_number,amb_0_ic_raw,amb_0_ic_read_temp,amb_0_ic_real_temp,amb_0_differ,amb_1_ic_raw,amb_1_ic_read_temp,amb_1__ic_real_temp,amb_1_differ,amb_4_ic_raw,amb_4_ic_read_temp,amb_4_ic_real_temp,amb_4_differ\n"
            write_str=write_str+cre.testStartTime+","
            write_str=write_str+cre.serial_number+","
        try:
            pass
        except:
            pass
            #print "Error"
        #for amb_index in [0,1,4]:
        #    write_str=write_str+str(cre.amb_sensores["amb%s_read_raw_data" %amb_index])+","
        #    write_str=write_str+str(cre.amb_sensores["amb%s_read_temp" %amb_index])+","
        #    write_str=write_str+str(cre.amb_sensores["amb%s_real_temp" %amb_index])+","
        #    write_str=write_str+str(float(cre.amb_sensores["amb%s_real_temp" %amb_index])-float(cre.amb_sensores["amb%s_read_temp" %amb_index]))+","
        #write_str=write_str+(cre.testStatus and "pass" or "fail")
        #log=Log()
        #log.Open3('data.csv')
        #log.PrintNoTime(write_str.strip(","))
            
