name = "winot"

## The following imports are required because it will allow us to
## directly refer to the Class names in our python scripts instead of
## having to refer to individual file names.
## For example we can now say
##   from winot import *
##   led = WiLed(addr)
## Without the below import statements, we will have to say
##  import winot
##  from winot.WiBuzzer import WiBuzzer
##  from winot.WiLed import WiLed
##  and so on

from WiBuzzer import WiBuzzer
from WiKeypad import WiKeypad
from WiLdr import WiLdr
from WiLed import WiLed
from WiMotionSensor import WiMotionSensor
from WiNoThing import WiThing
from WiNoTSwitch import WiSwitch
from WiPushButton import WiPushButton
from WiScale import WiScale
from WiWeather import WiWeather
from RemoteWeather import * 