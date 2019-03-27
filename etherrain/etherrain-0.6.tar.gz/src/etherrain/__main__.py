from __future__ import print_function
import os,sys
import etherrain
import time

def usage():
    print("Usage: {0} <ip addr> <username> <pw>".format(sys.argv[0]))

def test():
    if len(sys.argv) < 3:
        usage()
        return False

    a = sys.argv[1]
    u = sys.argv[2]
    p = sys.argv[3]
    print ("Testing with IP: {0}, User: {1}, Password: {2}".format(a,u,p))

    er = etherrain.EtherRain(a, u, p, timeout=5)

    if er.login() is True:
        print("Login successful")

    if er.update_status() is True:
        print("Was able to get status")
    else:
        print("Was not able to get status")


    print("State is: {0} and Last or current valve is: {1}".format(er.operating_state(), er.last_valve()))
    if 'BZ' in er.operating_state():
        print("ER is busy. Lets try stopping it.")
        er.stop()
        time.sleep(2)
        er.update_status()
        print("State is: {0} and Last or current valve is: {1}".format(er.operating_state(), er.last_valve()))
    if 'RD' in er.operating_state():
        print("Ready. So lets turn on valve 3 for 1 minute")
        er.irrigate(3,1)
        er.update_status()
        # Should be WT now
        if 'WT' in er.operating_state():
            print("ER is waiting......")
            time.sleep(2)
        else:
            print("Operating state should be WT, but is {0}".format(er.operating_state()))
        er.update_status()
        if 'BZ' in er.operating_state():
            print("Watering. Valve: {0}".format(er.last_valve()))
            er.stop()
            time.sleep(2)
            er.update_status()
            print("State is: {0} and Last or current valve is: {1}".format(er.operating_state(), er.last_valve()))
    return True

test()
