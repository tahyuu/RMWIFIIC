#server  
import paramiko
import SocketServer, os  
ssh=None

class MyTCPHandler(SocketServer.BaseRequestHandler):  
    def handle(self):  
        global ssh
        if not ssh:
            ssh= paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #ssh.connect(hostname,port,username,pkey=key)
            ssh.connect('192.168.1.28', username = 'pi', password='raspberry', timeout = 300)
            print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        while True:  
            self.data = self.request.recv(1024).strip()  
            print "{}wrote:".format(self.client_address[0])  
            if not self.data:  
                print "clilent %s is dead!" % self.client_address[0]  
                break  
            #cmd_result = os.popen(self.data).read();  
            if self.data.find("exit")>-1:
                break
            cmd = './rfspi.py '+self.data
            stdin, stdout, stderr = ssh.exec_command(cmd)
            cmd_result=stdout.read()
            f=open("log.txt","a+")
            f.write(cmd_result)
            print cmd_result
            if len(cmd_result.strip()) != 0:  
                self.request.sendall(cmd_result)  
            else:  
                self.request.sendall('Not found the command:' + self.data)  
if __name__ == "__main__":  
    HOST, PORT = "127.0.0.1", 3333  
  
    server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)  
  
    server.serve_forever()  
