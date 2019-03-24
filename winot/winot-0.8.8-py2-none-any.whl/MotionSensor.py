#  Copyright Qantom software private limited - all rights reserved
# No part of this code may be edited or used without the written 
# permission of Qantom's management. 

from WiNoThing import WiThing

__author__ = "raghu"
__date__ = "$April 20, 2018 00:15:57 PM$"


class WiMotionSensor(WiThing):

    def __init__(self, host, name=None):
      WiThing.__init__(self, host, name);

    def is_there_motion(self):
        # type: () -> bool
        response = WiThing.invoke_rest(self, "checkForMotion");
        is_motion = False
        if (response == "Motion Detected"):
            is_motion = True
        else:
            is_motion = False
        return is_motion
