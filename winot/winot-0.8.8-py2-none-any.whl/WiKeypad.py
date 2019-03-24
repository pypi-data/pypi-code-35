#  Copyright Qantom software private limited - all rights reserved
# No part of this code may be edited or used without the written 
# permission of Qantom's management. 

from WiNoThing import WiThing

__author__ = "raghu"
__date__ = "$April 20, 2018 00:15:57 PM$"

class WiKeypad(WiThing):
  
  def __init__(self, name, host): 
    print "before"; 
    WiThing.__init__(self, name, host);
   
  def keys(self):
    return WiThing.invoke_rest(self, "getKeys") ;