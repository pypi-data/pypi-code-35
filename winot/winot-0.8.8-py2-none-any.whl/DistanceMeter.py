#  Copyright Qantom software private limited - all rights reserved
# No part of this code may be edited or used without the written 
# permission of Qantom's management. 

import WiNoThing

__author__ = "raghu"
__date__ = "$April 20, 2018 00:15:57 PM$"

class WinotDistanceMeter(WiNoThing):
  
  def __init__(self, host, name=None): 
    WiNoThing.__init__(self,host,name);
   
  def distance(self):
    response =  WiNoThing.invoke_rest(self, "getDistance") ; 
    return float(response);