#  Copyright Qantom software private limited - all rights reserved
# No part of this code may be edited or used without the written 
# permission of Qantom's management. 

import urllib
import socket

__author__ = "raghu"
__date__ = "$April 20, 2018 00:15:57 PM$"

class WinotDisplay:
  def __init__(self, name, host=0): 
    self._name = name
    if (host == 0) :
      domainname = self._name  ; 
      try :
        self._address = "http://" + socket.gethostbyname(domainname)
      except : 
        raise BaseException("Could not determine address for " + name)
    else :
      self._address = "http://" + host
      
  def display(self, line1, line2=""):
    fulladdr = self._address + "/displayText?line1=" +  line1 + "&line2=" + line2
    urllib.urlopen(fulladdr)
      
  def lighton(self):
    fulladdr = self._address + "/displayText?backlight=on"
    print fulladdr
    urllib.urlopen(fulladdr)
    
  def lightoff(self):
    fulladdr = self._address + "/displayText?backlight=off"
    urllib.urlopen(fulladdr)
