# -*- coding: utf-8 -*-
import sys, getopt

from WiNoThing import WiThing
from WiScale import WiScale
from WiBuzzer import WiBuzzer
from WiLdr import WiLdr
from WiPushButton import WiPushButton
from WiNoTSwitch import WiSwitch
from WiWeather import WiWeather
from WiMotionSensor import WiMotionSensor
from WiLed import WiLed
from WiBuzzer import WiBuzzer

def test_all() :
    devices = WiThing.get_all_winotdevices()

    if (len(devices) == 0):
        print ("No WiNoT Devices found!")
    else:
        cnt = 0;
        sel_device = 1;  # type: int
        for device in devices.keys():
            cnt = cnt + 1
        if (cnt > 1):
            idx = 1;
            for device in devices.keys():
                print ("%r. Device name = %-15s| Address = %s" % (idx, device.strip(), devices[device]))
                idx = idx + 1
            sel_device = int(raw_input("Choose a device from the above list(0 to exit) - "))
        if (sel_device == 0):
            exit(0)
        else:
            sel_device = sel_device - 1;
            dev_name = devices.keys()[sel_device];
            dev_ip = devices[dev_name];
            thing = WiThing(dev_ip)
            cmds = thing.get_all_commands().values()

            if (len(cmds) == 8 and  cmds.__contains__("buzz") and cmds.__contains__("getDistance")
                    and cmds.__contains__("checkForMotion") and cmds.__contains__("operateLed")
                    and cmds.__contains__("Switch") and cmds.__contains__("isPushed")
                    and cmds.__contains__("intensity") and cmds.__contains__("weather")):
                # It means that this is a trainer.

                # print "Selected device is " + dev_name + " whose address is " + dev_ip
                # print ("%s %s(%s) %" ("", dev_name, dev_ip, "------------------"))
                print ("\nRunning trainer tests for %s(%s)" % (dev_name, dev_ip))

                ms = WiMotionSensor(dev_ip)
                isMotion = ms.is_there_motion();
                weather = WiWeather(dev_ip)
                temperature = weather.temperature();
                humidity = weather.humidity();
                distance = WiScale(dev_ip).distance();
                intensity = WiLdr(dev_ip).intensity();
                WiBuzzer(dev_ip).buzz();
                WiLed(dev_ip).switch();
                WiSwitch(dev_ip).switch();

                print ("Test Completed. If you observed the following then " \
                       "your WiNoT® device is working fine.  \n" \
                       "1. The buzzer should have beeped for 3 seconds \n" \
                       "2. The LED status should have changed \n" \
                       "3. The Relay status should have changed (You would have heard a small click)\n" \
                       "4. The following values shown by the sensors match the actual values in your room:\n"
                       "Values from onboard sensors:")

                print ("%-35s %r" % ("Has motion been detected?", isMotion))
                print ("%-35s %r %s" % ("Distance from nearest object", distance, "cms"))
                print ("%-35s %r %s" % ("Ambient temperature", temperature, "degree C"))
                print ("%-35s %r %s" % ("Ambient humidity", humidity, "%"))
                print ("%-35s %r\n" % ("Ambient light intensity level", intensity))
            else:
                print ("Device " + dev_name, " has these things - ", cmds)
            # print sel_dev_commands

def show_devices() :
    devices = WiThing.get_all_winotdevices()

    if (len(devices) == 0):
        print ("No WiNoT Devices found!")
    else:
        cnt = 0;
        sel_device = 1;  # type: int
        for device in devices.keys():
            cnt = cnt + 1
            print ("%r. Device name = %-15s| Address = %s" % (cnt, device.strip(), devices[device]))


if __name__ == '__main__':
    if (len(sys.argv) == 1 ):
        print "Usage : python -m winot <option> [local_bind_address]\n" \
            "Where options can be one of :\n" \
            "test -  Test a WiNoT board\n" \
            "list -  List all the WiNoT devices in your network\n" \
            "If your computer has more than one network interfaces, then " \
            "provide the IP Address of the required interface as the 2nd argument\n"
    else :
        arg = sys.argv[1]
        bindaddr = "" 
        if (len(sys.argv) >= 3):
            bindaddr=sys.argv[2]
            WiThing.bind_local(bindaddr)    
        if (arg == "test"):
            test_all()
        elif (arg == "list") :
            show_devices()


