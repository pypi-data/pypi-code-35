#  Copyright Qantom software private limited - all rights reserved
# No part of this code may be edited or used without the written
# permission of Qantom's management.

import urllib
import socket
import time

__author__ = "raghu"
__date__ = "$April 20, 2018 00:15:57 PM$"
## Look up https://github.com/dbader/schedule

WIRARP_PORT = 9219
ARP_STALETIME = 60*.1 # Max time for which cached values should be used.
ARP_TIMEOUT = 5
WINOTARPREQ = "WiNoTWho"
WINOTARPFORALL = "WiNoTAll" 

class WiThing:

  # Create Dictionary with keys set to device names and 
  # value set to a set of device IP with epochtime
  devtable = {} # Format {dev_name : {dev_ip, epochtime}}
  bindaddress = "" 

  def __init__(self, host, name=None):
    # type: (object, object) -> object
    self._name = name;
    self._address = "http://" + host;

  @staticmethod 
  def bind_local(local_ip) :
    WiThing.bindaddress = local_ip 

  @staticmethod
  def get_all_winotdevices() :
    #First of all clear the device table dictionary.
    #as we will be finding the values fresh!
    WiThing.devtable.clear();
    t = int(time.time());
    arpmsg = WINOTARPREQ + "\n"
    arpmsg = arpmsg + WINOTARPFORALL + "\n"
    arpmsg = arpmsg + str(t) + "\n"

    clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSock.bind((WiThing.bindaddress, 0))
    clientSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clientSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    clientSock.sendto(arpmsg, ('<broadcast>', WIRARP_PORT))

    try:
      # declare our serverSocket upon which
      # we will be listening for UDP messages
      serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

      # One difference is that we will have to bind our declared IP address
      # and port number to our newly declared serverSock
      serverSock.bind(("0.0.0.0", WIRARP_PORT))
      serverSock.settimeout(ARP_TIMEOUT)
      while True:
        data, addr = serverSock.recvfrom(1024)
        #print "Recd. data = " + data
        recdArp = data.split("\n")
        if (recdArp[0] == "WiNoTMe"):
          recdName = recdArp[1]
          recdUid = recdArp[2]
          if (recdUid == str(t)):
            recdIp = recdArp[3]
            WiThing.devtable[recdName] = [recdIp, t]
          else:
            print ("Recd response doesn't match with sent request" + data)
        else:
          print ("Unknown response received - " + data)
      serverSock.settimeout(None)
    except Exception as e:
      pass # In this case, if there is an exception doesn'tnecessarily mean an error.

    retList = {}
    for devname in WiThing.devtable.keys():
      tmpVal = WiThing.devtable[devname]
      retList[devname] =  tmpVal[0]
    return retList

  @staticmethod
  def resolve_address(device_name):
    t = int(time.time());
    toResolve = True ;
    recdIp = ""
    if device_name in WiThing.devtable:
      storetime = WiThing.devtable[device_name][1]
      if ((t - storetime) > ARP_STALETIME):
        toResolve = True
      else :
        recdIp = WiThing.devtable[device_name][0]
        print("Using cached value : " + recdIp)
        toResolve = False

    if(toResolve == True):
      arpmsg = WINOTARPREQ + "\n"
      arpmsg = arpmsg + device_name + "\n"
      arpmsg = arpmsg + str(t) + "\n"
      # No need to send IP address

      clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      clientSock.bind((WiThing.bindaddress, 0))
      clientSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      clientSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
      clientSock.sendto(arpmsg, ('<broadcast>', WIRARP_PORT))

      try:
        # declare our serverSocket upon which
        # we will be listening for UDP messages
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # One difference is that we will have to bind our declared IP address
        # and port number to our newly declared serverSock
        serverSock.bind(("", WIRARP_PORT))
        serverSock.settimeout(ARP_TIMEOUT)
        data, addr = serverSock.recvfrom(1024)
        serverSock.settimeout(None)
        recdArp = data.split("\n")
        if (recdArp[0] == "WiNoTMe") :
          recdUid = recdArp[1]
          if (recdUid == str(t)) :
            recdIp = recdArp[2]
            WiThing.devtable[device_name] = [recdIp, t]
          else :
            print ("Recd response doesn't match with sent request" + data)
        else:
          print ("Unknown response received - " + data)
      except Exception as e:
        print("Could not resolve device address for " + device_name)
        recdIp = None ;
    return recdIp

  def get_name(self) :
    return self._name ;

  def invoke_rest(self, command, additionalparams=None):
    fullcommand = "/" + str(command) ;
    try :
      if (self._name is not None) :
        fullcommand = fullcommand + "?thingname=" + self._name ;
        if(additionalparams):
          fullcommand = fullcommand + "&" + additionalparams ;
      elif (additionalparams):
        fullcommand = fullcommand + "?" + additionalparams ;
      
      response = urllib.urlopen(self._address + fullcommand) ;

    except Exception as e:
      raise BaseException("Could not connect to WiNoT device @ " + self._address + fullcommand);
    return response.read().strip();

  def set_name(self, newname):
    result = self.invoke_rest("setName", "&name=" + newname) ;
    if (result.startswith("FAIL")):
      result = result[5:] ;
      raise BaseException("Error while trying to set name. Message = " + result);
    self._name = newname ;

  def get_all_commands(self):
    response = self.invoke_rest("getAllCommands");
    name_command_pairs = response.split(",")
    cmd_dict = {}
    for pair in name_command_pairs:
      ncsplit =  pair.split(":")
      cmd_dict[ncsplit[0].strip()] = ncsplit[1].strip()
    return cmd_dict

  def analog_read(self):
    response = self.invoke_rest("analogRead")
    return int(response) 

  def digital_read(self, pin):
    response = self.invoke_rest("digitalRead", "pin=" + str(pin))
    return int(response)

  def digital_write(self, pin, state):
    response = self.invoke_rest("digitalWrite", "pin=" +str(pin) + "&state=" +str(state))