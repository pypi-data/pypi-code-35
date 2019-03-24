#  Copyright Qantom software private limited - all rights reserved
# No part of this code may be edited or used without the written 
# permission of Qantom's management. 

from WiNoThing import WiThing

__author__ = "raghu"
__date__ = "$April 20, 2018 00:15:57 PM$"

class WiLed(WiThing):
  
  def __init__(self, host, name=None): 
    WiThing.__init__(self,host,name);
   
  def on(self):
    response =  WiThing.invoke_rest(self, "operateLed",additionalparams="action=ON") ;
    return response;
    
  def off(self):
    response = WiThing.invoke_rest(self, "operateLed",additionalparams="action=OFF") ;
    return response;

  def switch(self):
    response =  WiThing.invoke_rest(self, "operateLed",additionalparams="action=SWITCH") ;
    return response;

  def blink(self, btime):
    response = WiThing.invoke_rest(self, "operateLed",
          additionalparams="action=blink&blinkTime=" + str(btime)) ;