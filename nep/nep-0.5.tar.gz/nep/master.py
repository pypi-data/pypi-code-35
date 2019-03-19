# coding = utf-8
#!/usr/bin/env python

# ------------------------------- Master -----------------------------------
# Description: Low-level Master class
# --------------------------------------------------------------------------
# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.
# Autor: Luis Enrique Coronado Zuniga


import zmq
import time
import nep
import sys, os
import signal


if sys.version_info[0] == 3:
    import _thread as thread
else:
    import thread
    
# ---------------------------------- Static ports ------------------------------------ :
# master port 7000

# ----------------------------------- Topic format ----------------------------------- :
# topic_name: [port,mode,ip] 

class master:

    def __signal_handler(self, signal, frame):
        import os


        print('Signal Handler, you pressed Ctrl+C! to close the node')
        if not os.environ.get('OS','') == 'Windows_NT': # Windows
            time.sleep(.5)
            os.system('kill %d' % os.getpid())
            sys.exit(0)
        else:
            """Signal handler used to close when user press Ctrl+C"""
            time.sleep(.5)
            import os
            pid = os.getpid()
            print (pid)
            import subprocess as s
            s.Popen('taskkill /F /PID {0}'.format(pid), shell=True)
            sys.exit(0)

    
    def __init__(self, IP = '127.0.0.1' , port = 7000, initial_port_number = 9000):

        """
        Creates a new master object for service discovery

        Parameters
        ----------

        IP : string
            IP value of server

        port : int
            Port used to connect the socket
            
        initial_port_number : int
            Port numbers will be registered starting from the value of this parameter

        """

        # Start master server
        self.s = nep.server(IP,port)
        self.IP = IP

        # Ports configuration
        self.current_port = initial_port_number
        self.topic_register = {}


    def __onMany2Many(self,port):
        """
        Cretates a  many2many XPUB/XSUB broker in a new thread

        Parameters
        ----------

        port : int
            Number of the port to set the broker. Ther brokers is made using port and port + 1. Therefore use only pairs numbers in this parameter
            
        """
        b = nep.broker(self.IP, port+1, port)



    def __onNewTopic(self,node_request):
        """
        Register and return connection parameters for requested topics

        Parameters
        ----------

        node_request : dictionary
            Request parameters of the topic. This parameters are: topic (i.e the topic name), node (i.e. name of the module), socket (e.g. publisher, subscriber, server, client, surveyor, ...) and mode (only for publish and subscriber and can be many2one, one2many and many2many). 
        """

        topic = str(node_request['topic'])

        if node_request["socket"] == "publisher" or node_request["socket"] == "subscriber":
            if node_request["mode"] == "many2many":
                thread.start_new_thread ( self.__onMany2Many, (self.current_port,))
                time.sleep(.5)
            
            self.topic_register.update({topic:{"port":self.current_port,"socket":node_request["socket"], "mode":node_request["mode"]}})
            msg = {'topic':topic, 'port': self.current_port, 'mode':node_request["mode"],  'ip': self.IP, 'socket':node_request["socket"], "state":"success"}

        elif node_request["socket"] == "surveyor" or node_request["socket"] == "respondent":
            self.topic_register.update({topic:{"port":self.current_port,"socket":node_request["socket"]}})
            msg = {'topic':topic, 'port': self.current_port,  'ip': self.IP, 'socket':node_request["socket"], "state":"success"}
            pass

        elif node_request["socket"] == "client" or node_request["socket"] == "server":
            self.topic_register.update({topic:{"port":self.current_port,"socket":node_request["socket"]}})
            msg = {'topic':topic, 'port': self.current_port,  'ip': self.IP, 'socket':node_request["socket"],"state":"success"}
            pass
        
        self.s.send_info(msg)
        self.topic_register[topic]["nodes"] = []
        data =  {'node':node_request['node'],'socket':node_request["socket"]}
        self.topic_register[topic]["nodes"].append(data)
        self.current_port = self.current_port + 2


        #print (self.topic_register)

    def __onRegisteredTopic(self,topic, node_request):
        """ 
        Send topic info to the node

        Parameters
        ----------

        topic : string
            Topic name

        node_request : dictionary
            Request parameters of the topic. This parameters are: topic (i.e the topic name), node (i.e. name of the module), socket (e.g. publisher, subscriber, server, client, surveyor, ...) and mode (only for publish and subscriber and can be many2one, one2many and many2many). 
        
        """
        
        port = self.topic_register[topic]["port"]
        socket_= self.topic_register[topic]["socket"]

        if "mode" in self.topic_register[topic]:
            mode = self.topic_register[topic]["mode"]
            msg = {'topic':topic, 'port': port, 'mode':mode, 'ip': self.IP, 'socket':socket_ , "state":"success"}
        else:
            msg = {'topic':topic, 'port': port, 'ip': self.IP, 'socket':socket_, "state":"success"}

        self.s.send_info(msg)
        data =  {'node':node_request['node'],'socket':node_request["socket"]}
        self.topic_register[topic]["nodes"].append(data)
        
        #print (self.topic_register)

    def run(self):
        """ Run master node until Ctrl+C is pressed
        """
        # Enable to kill the node using Ctrl + C
        signal.signal(signal.SIGINT, self.__signal_handler)

        while True:
            time.sleep(.01)
            node_request = self.s.listen_info()
            print ("Request: " + str(node_request))

            # Service discovery
            if 'topic' in node_request:
                topic = str(node_request['topic'])
                
            
                if topic in self.topic_register:
                    self.__onRegisteredTopic(topic, node_request)
                else:
                    self.__onNewTopic(node_request)
            

            # Get avaliable topic list
            elif 'topic_list' in node_request: 
                msg = self.topic_register
                self.s.send_info(msg)  

if __name__ == "__main__":
    import doctest
    doctest.testmod()
