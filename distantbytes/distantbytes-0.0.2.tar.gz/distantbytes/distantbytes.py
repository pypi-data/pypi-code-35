#!/usr/bin/env python3
import threading
import time
import json
import socket

HOST = "www.distantbytes.com"
PORT = 1337
VERSION = "0.0.1"


class Print():
    """This print object is what is instanciated by the user when they use
    this package. It is a callable object the mimics the behavour of the
    built in python print statement but it also sends prints to the server"""

    #All instaces of this Print class share the same socket client singleton
    #The socket client singleton handles all the interaction with the server
    socket_client_singleton = None

    #this lock is shared between all Print objects and is used to make sure one socket_client_singleton is instanciated
    lock = threading.Lock()

    def __init__(self,terminal_name ,print_local = True, print_remote = True):
        #copy arg variables
        self.terminal_name = terminal_name
        self.print_local = print_local
        self.print_remote = print_remote

        #Check if the socket client exists and create it if it doesn't. Use the lock to ensure only one socket client is created.
        #The lock is only required if users are printing from different threads
        with Print.lock:
            if Print.socket_client_singleton is None:
                Print.socket_client_singleton = SocketClient()


    def __call__(self,*objects):
        """This is callable and mimics the behavour of the normal print function"""

        #if print local is enabled then use the builtin print to print locally
        if self.print_local:
            print(*objects)

        #if print remote is enabled then add the print string to the socket client for sending to the server
        if self.print_remote:
            #convert all the object into srings and concatenate them together with a space
            print_str = " ".join( [str(obj) for obj in objects])

            #add this print string to the socket client which will asyncronously send it to the server some time later
            Print.socket_client_singleton.add_print(self.terminal_name, print_str)



class SocketClient(threading.Thread):
    """This thread safe class accumulate print string for different terminal names
    and periodically asyncronously connects to the server to send it all the
    latest print strings"""

    def __init__(self):
        #call __init__ for the parent Thread class
        super().__init__()

        #create a lock object to protect the terminal dict
        self.lock = threading.Lock()

        #Create a dict to hold all the print strings for each terminal names
        #This dict will be filled with a list of print strings for the given terimal name
        self.terminal_dict = {}

        #flag to note if the loops should keep running
        self.alive = True

        #call the start method inherited from the Thread class.
        #This in turn calls the run method
        self.start()


    def run(self):
        """This is called by start() and will run forever.
        It periodically tries to send all the print strings to the server"""

        #while alive
        while self.alive:

            #sleep for a suitable period of time
            time.sleep(1)

            #since we are using sockets just catch everything and keep trying
            try:
                self._send_to_server()
            except Exception as e:
                print("distantbytes", e)


    #This should be called by the Print class to add new print strings
    def add_print(self,terminal_name,print_str):
        """A thread safe method to add a print string to a given named terimal"""

        #aquire the lock so no other threads modify this dict at the same time
        with self.lock:
            #Try and get the list of prints using the terminal name.
            #Create a empty list if it doesn't exist
            print_list = self.terminal_dict.get(terminal_name,[])

            #this does nothing except when a new terminal print list was just created by the get function above
            self.terminal_dict[terminal_name] = print_list

            #append this print string
            print_list.append(print_str)


    def _send_to_server(self):
        """This function converts the terminal print dict into a json strings
        and repeatedly tries to send it to server. It then waits for a success json
        response before returning"""

        with self.lock:
            #if nothing has be printed lately then just return and do nothing
            if len(self.terminal_dict) == 0:
                return

            #wrap the terminal dict with another dict that incudes a version number and stuff
            send_json_dict = {"version":VERSION,"print_dict":self.terminal_dict}

            #clear the dict
            self.terminal_dict = {}

        #keep looping until we send the json to the server
        while self.alive:
            #since we are using sockets catch any error and keep trying
            try:
                #create a new socket object
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

                    #set the timeout so that it doesnt hang waiting for a response
                    sock.settimeout(60)

                    #connect to the server
                    sock.connect((HOST, PORT))

                    self.send_dict_as_json(sock,send_json_dict)

                    recv_json_dict = self.recv_json_as_dict(sock)

                    #if the dict contains success = True then return
                    if recv_json_dict.get("success",False) == True:
                        pass

                    return

            except Exception as e:
                # print("distantbytes", e)
                #if ther is Exception just wait a bit before retrying
                time.sleep(1)


    def send_dict_as_json(self,sock, json_dict):
        #convert the dict to a json string
        json_str = json.dumps(json_dict)

        #add the null character to the end of the string as a marker
        json_str += chr(0)

        #encode the string into bytes
        json_bytes = json_str.encode("utf-8")

        #send the json as bytes to the server
        sock.sendall(json_bytes)


    def recv_json_as_dict(self,sock):

        #create a empty byte string to buffer the response
        json_bytes = b""

        #keep receiving bytes until null character is received
        while self.alive:
            #append new bytes
            json_bytes += sock.recv(1024)

            #check if the last byte is null then break
            if json_bytes[-1] == 0:
                break

        #decode the bytes into a string
        json_str = json_bytes[:-1].decode("utf-8")

        #convert the json string to python dict object
        json_dict = json.loads(json_str)

        return json_dict


    def join(self):
        """Override the normal thread join to set alive to false then call the parent Thead.join"""
        self.alive = False
        super().join()


    def __del__(self):
        """On destruction call the join to ensure all the loops stop"""
        self.join()
