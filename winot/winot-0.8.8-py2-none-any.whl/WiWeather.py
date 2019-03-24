#  Copyright Qantom software private limited - all rights reserved
# No part of this code may be edited or used without the written
# permission of Qantom's management.

from WiNoThing import WiThing

__author__ = "raghu"
__date__ = "$February 11th 2019"


class WiWeather(WiThing):

    def __init__(self, host, name=None):
        WiThing.__init__(self, host, name);

    def temperature(self):
        response = WiThing.invoke_rest(self, "weather", "read=temperature");
        if (response.startswith("T=")) :
            return float(response.split("=")[1]);
        else:
            return None ;

    def humidity(self):
        response = WiThing.invoke_rest(self, "weather", "read=humidity");
        response = response.strip()
        if (response.startswith("H=")) :
            return float(response.split("=")[1]);
        else:
            return None ;

    def weather(self):
        response = WiThing.invoke_rest(self, "weather", "read=both");
        response = response.strip()
        if (response.startswith("T=")) :
            tmpArr = response.split("=")
            t=tmpArr[1].strip("+H")
            h=tmpArr[2].strip()
            return (float(t), float(h));
        else:
            return None ;