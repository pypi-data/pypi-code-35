import paramiko
import os,re, sys, traceback
import pprint

SSH_DEBUG=True
HOME = os.getenv("HOME")

class session_manager(object):
    __shared_state = {}
    
    def __init__(self):
        self.__dict__ = self.__shared_state
        if len(self.__dict__)==0:
            self.connections = {}
            self.passwords = {}
            self.machine = None

    def initialize_machine(self,machine):
        self.machine = machine

        # on lit les user par defaut dans .ssh/config
        # la clef de connection elle par contre est en dur : ~/.ssh/id_rsa-hpcportal
        ssh_config = paramiko.SSHConfig()
        try:
            ssh_config.parse(open(os.path.abspath(HOME)+'/.ssh/config'))
            o = ssh_config.lookup(self.machine)
            if SSH_DEBUG:
                print (self.machine,o)
            self.actual_machine = o['hostname']
            #self.actual_default_user = o["user"]
            self.actual_default_port = 22
            try:
                if "port" in o.keys():
                    self.actual_default_port = int(o["port"])
            except:
                print('ZZZZ problem to read port ',o)
    
    
            if SSH_DEBUG:
                print("actual_machine: %s, actual_default_port: %s " % \
                      (self.actual_machine, self.actual_default_port))
            # bug bizzare de lecture du user
            #self.actual_default_user = self.actual_default_user[:-1]
            # avec un blanc sur certaines machines
            # self.actual_ssh = o['identityfile']
            
        except Exception as e:
            print("ssh_authenticator.py : problem to read ssh config for machine %s" %\
                  self.machine, " read from : %s" % \
                  os.path.abspath(HOME)+'/.ssh/config')
            try:
                print("value read from .ssh/config : ",o)
            except:
                print("no value read from .ssh/config....")
            print(e)
            traceback.print_exc(file=sys.stdout)
            print("setting same machine name and port to default ssh port")
            #sys.exit(1)
            self.actual_machine = machine
            self.actual_default_port = 22



    def open(self,machine,login,password):
        if not(self.machine):
            self.initialize_machine(machine)
            
        user_connection_id = "%s_%s" % (self.machine,login)
        
        if SSH_DEBUG:
            print("[AUTHENT] opens new session for  %s/%s" % \
                  (self.machine,login))

        # initialisation du client
        connection = paramiko.SSHClient()
        connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # login utilisateur
        try:
            connection.connect(self.actual_machine, username=login, password=password,
                               port=self.actual_default_port)
            print("[AUTHENT] connection succeeded!!!")
        except Exception as e:
            print("[AUTHENT] connection failed!!!")
            if user_connection_id in self.connections.keys():
                del self.connections[user_connection_id] 
            if user_connection_id in self.passwords.keys():
                del self.passwords[user_connection_id]
            print(e)
            traceback.print_exc(file=sys.stdout)

            return False
            raise ValueError("bad connection")


        if SSH_DEBUG:
            print("[AUTHENT] [%s] opens new connection for user %s : " % \
                (self.machine,login) ,connection)
        # test de la connection
        stdin, stdout, stderr = connection.exec_command("cd; pwd")
        res = stdout.readlines()
        home = res
        if SSH_DEBUG:
            print("[AUTHENT] stdout test : ",res)
            print("[AUTHENT] stderr test ; ",stderr.readlines())
                
        self.connections[user_connection_id] = connection
        self.passwords[user_connection_id] = password

        if SSH_DEBUG:
            print("[AUTHENT] so far connection registered are %s",pprint.pformat(self.connections))

        return connection
        

    def execute(self,login,cmd):
        connection = self.get_session(login)
        if not(connection):
            print("[AUTHENT] session expired for %s/%s " %\
                  (self.machine,login))
            return False
        # test de la connection
        stdin, stdout, stderr = connection.exec_command(cmd)
        res = stdout.readlines()
        home = res
        return home

    def get_session(self,login):
        user_connection_id = "%s_%s" % (self.machine,login)
        if SSH_DEBUG:
            print("[AUTHENT] so far connection registered are %s",pprint.pformat(self.connections))
        if user_connection_id in self.connections.keys():
            if SSH_DEBUG:
                print("[AUTHENT] reutilisation de la session pour ",user_connection_id)
            return self.connections[user_connection_id]
        else:
            print("[AUTHENT] NO session available for ",user_connection_id)
            return False
        
    def close(self,login):
        user_connection_id = "%s_%s" % (self.machine,login)
        if user_connection_id in self.connections.keys():
            if SSH_DEBUG:
                print("[AUTHENT] closing ssh session for ",user_connection_id)
            # closing session
            try:
                if self.machine == "vishnu":
                    session_id = self.connections[user_connection_id]
                    VISHNU.close(session_id)
                else:
                    self.connections[user_connection_id].close()
            except:
                if SSH_DEBUG:
                    print("[AUTHENT] session %s already closed!!!!!" % user_connection_id)
            # cleaning
            del self.connections[user_connection_id]
            if user_connection_id in self.passwords.keys():
                 del self.passwords[user_connection_id]
            return True
        else:
            print("[AUTHENT] asking to close an unexisting  session for  ",user_connection_id)
            return False
        

    def exists(self,login):
        user_connection_id = "%s_%s" % (self.machine,login)
        if SSH_DEBUG:
            print ("[AUTHENT] Checking if sessions ssh exists  pour ",user_connection_id\
                ,user_connection_id in self.connections.keys())
        return (user_connection_id in self.connections.keys())
    





if __name__ == "__main__":

    user_name = "ek"
    slurm_machine = session_manager()
    connection = slurm_machine.open(user_name,"ksl123")

    if not(connection):
        print("[AUTHENT] session failed for %s/%s " %\
              (slurm_machine.machine,user_name))
        sys.exit(1)

    print("".join(slurm_machine.execute(user_name,"ps -edf")))

    connection = slurm_machine.get_session(user_name)
    if not(connection):
        print("[AUTHENT] session expired for %s/%s " %\
              (slurm_machine.machine,user_name))
        sys.exit(1)

    input = """#!/bin/sh
#SBATCH -N 1
#SBATCH -J job
#SBATCH -o job.out
#SBATCH -o job.err
#SBATCH -t 2
echo hello
sleep 10
"""
    cmd = "sbatch"
    stdin, stdout, stderr = connection.exec_command(cmd)
    stdin.write(input)
    stdin.channel.shutdown_write()
    res = stdout.readlines()
    print("[AUTHENT] res for cmd=|||%s||| = %s " %    (cmd,res))
