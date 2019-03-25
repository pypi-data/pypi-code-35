from .shelly import (Shelly, Wifi_sta)
import logging
import json
from .helpers import (Call_shelly_api, Get_item_safe, Rssi_to_percentage)

logging.basicConfig(level=logging.DEBUG)

shelly81 = Shelly("192.168.1.81")
shelly82 = Shelly("192.168.1.82", "admin", "admin")

# i = 1
# while i < 60:
#   x = shelly82.update_data()
#   print(x)
#   x = shelly81.update_data()
#   print(x)
#   i += 1

# x = Shelly("192.168.1.81").update_data()
# print(len(x.relays))
# print(x.relays[0].__dict__)
# print(x)
# print(type(x))
# x.update_data()
# print (x.__dict__)