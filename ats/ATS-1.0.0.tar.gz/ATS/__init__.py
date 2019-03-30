# coding=utf-8
import re
from Device import Device
from Command import Command

__version__ = '1.0'
__author__ = 'bony'
# __all__ = ['BAndroidDriver', 'Element']
"""
ATD
"""


def get_device(serial=None, name=None):
    devices = get_devices()
    if len(devices) > 0:
        if serial is None:
            if name is None:
                return devices[0]
            else:
                device = devices[0]
                device._name = name
                return device
        else:
            if get_by_serial_device(serial) is None:
                print(u"未找到匹配设备!")
                return None
            else:
                device = get_by_serial_device(serial)
                if name is None:
                    return device
                else:
                    device._name = name
                    return device
    else:
        print(u"未连接设备!")
        return None


def existence_device(device):
    if device.get_serial() is None:
        return False
    else:
        return True


def get_by_serial_device(serial):
    devices = get_devices()
    for device in devices:
        if device.get_serial() == serial:
            return device
    return None


def get_devices():
    devices = []
    for line in Command("adb devices -l").read_line():
        if "device" in line and "product" in line:
            devices_list = re.compile(r"((?:[a-zA-Z0-9\w]+))").findall(line)
            devices.append(Device(devices_list[0], devices_list[3]))
    return devices
