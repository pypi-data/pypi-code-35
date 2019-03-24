
import sys
import time
import socket

from WiNoThing import WiNoThing
from WiLed import WiLed

'''
for ip in socket.gethostbyname_ex(socket.gethostname()):
  #print (socket.gethostbyname(ip))
  print ip
  #print ("[" + ip + "]" )

exit() ;
'''

addr = WiNoThing.resolve_address("nodemcu2") ;
if (addr != None) :
  print("Address = " + addr);
addr = WiNoThing.resolve_address("nodemcu2") ;
if (addr != None) :
  print("Address = " + addr);
addr = WiNoThing.resolve_address("nodemcu23") ;
if (addr != None) :
  print("Address = " + addr);
time.sleep(10)
print("----- Trying after cache time -----")
addr = WiNoThing.resolve_address("nodemcu2") ;
if (addr != None) :
  print("Address = " + addr);

if (addr is None) :
  exit() ;

led = WiLed(addr);

def TurnOnLed():
  led.on();

def TurnOffLed():
  led.off();

TurnOnLed() ;
time.sleep(2);
TurnOffLed() ;