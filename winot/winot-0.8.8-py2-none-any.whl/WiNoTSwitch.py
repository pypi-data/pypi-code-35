#  Copyright Qantom software private limited - all rights reserved
# No part of this code may be edited or used without the written
# permission of Qantom's management.

__author__ = "raghu"
__date__ = "$April 20, 2018 00:15:57 PM$"

from WiNoThing import WiThing

class WiSwitch(WiThing):

  def __init__(self, host, name=None):
    WiThing.__init__(self, host, name);
    #super(name, host).__init__();

  @classmethod
  def create_switch(self, address, type, name, pin):
    wiswitch = WiSwitch(name, address);
    if (type.lower() == "lowtrigger" or type.lower() == "low") :
      WiSwitch.invoke_rest("addThing", "type=lowtrigger&pin=" +pin)
    else :
      WiSwitch.invoke_rest("addThing", "type=hightrigger&pin=" +pin)
    return wiswitch ;

  def switch(self):
    WiThing.invoke_rest(self, "Switch", "action=switch") ;

  def on(self):
    WiThing.invoke_rest(self, "Switch", "action=on") ;

  def off(self):
    WiThing.invoke_rest(self, "Switch", "action=off") ;

  def status(self):
    return WiThing.invoke_rest(self, "Switch");
