# Copyright Qantom software private limited - all rights reserved
# No part of this code may be edited or used without the written
# permission of Qantom's management.

__author__ = "raghu"
__date__ = "$13 Apr, 2018 5:19:56 PM$"


import urllib
import time



from winotwrappers.WiNoThing import WiNoThing
from winotwrappers.WiNoTSwitch import WiNoTSwitch


from winotwrappers.DistanceMeter import WinotDistanceMeter
from winotwrappers.WiLed import WiLed
from winotwrappers.WiBuzzer import WiBuzzer 
from winotwrappers.WiLdr import WiLdr
from winotwrappers.MotionSensor import WiMotionSensor
from winotwrappers.WiPushButton import WiPushButton

if __name__ == "__main__":
  
  #try:
    host="pluggabletrainer.thingsping.in"; 
    
    pb = WiPushButton(host)
    print ("Ispushed = " + str(pb.pushed())); 
    
    pir1 = WiMotionSensor(host); 
    print ("Motion = " + str(pir1.is_there_motion())); 
    
    ldr1 = WiLdr(host); 
    print (str(ldr1.intensity()))
    
    led1 = WiLed(host); 
    led1.on() ; 
    print "Turned on!"
    time.sleep(0.5); 
    led1.off() ; 
    print "Turned off"; 
    
    buzz1 = WiBuzzer(host); 
    buzz1.buzz(500)
    
  
    #scale1 = WinotDistanceMeter("pluggabletrainer.thingsping.in");
    #print "Distance = " + str(scale1.distance()); 
    
    '''
    switch1 = WiNoTSwitch("s1", "wemostest1.thingsping.in");
    switch1.switch() ; 
    nm = switch1.get_name(); 
    print "Switch - " + nm + " is " + switch1.get_status() ; 
    
    motionsensor = WinotMotionSensor.create_sensor("192.168.0.205", "staircasemotion", 13);
    floorswitch = WiNoTSwitch.create_switch("192.168.0.205", "hightrigger", "staircase", 12);
    
    if (motion.sensor.is_there_motion()):
      floorswitch.switch_on() ; 
    else :
      floorswitch.switch_off() ; 
    '''
    
  #except BaseException as e:
  #  print "Error trying to process request - " + e.message


