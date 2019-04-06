## binhoUtilities Python Library
## Version 1.0
##
## Jonathan Georgino <jonathan@binho.io>
## Binho Electronics
## www.binho.io

import sys
import glob
import serial
from . import binhoHostAdapter

# Source: https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
# Claims that it is successfully tested on Windows 8.1 x64, Windows 10 x64, Mac OS X 10.9.x / 10.10.x / 10.11.x and Ubuntu 14.04 / 14.10 / 15.04 / 15.10 with both Python 2 and Python 3.

class binhoUtilities:

    def __init__(self):
        self.stuff = "test"

    def listAvailablePorts(self):

        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port, timeout=500)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def listAvailableDevices(self):

        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                hostAdapter = binhoHostAdapter.binhoHostAdapter(port)
                
                resp = hostAdapter.getDeviceID()

                if "-ID" in resp:
                    result.append(port)

            except (OSError, serial.SerialException):
                pass
        return result

    def getPortByDeviceID(self, deviceID):

        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                hostAdapter = binhoHostAdapter.binhoHostAdapter(port)
                resp = hostAdapter.getDeviceID()

                if resp == '-ID ' + deviceID:
                    result.append(port)
                elif resp == '-ID 0x' + deviceID:
                    result.append(port)

            except (OSError, serial.SerialException):
                pass
        return result

    if __name__ == '__main__':
        print(listAvailableDevices())