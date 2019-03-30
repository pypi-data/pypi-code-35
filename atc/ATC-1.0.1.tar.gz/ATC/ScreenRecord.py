# coding=utf-8

import time
import subprocess
import threading

"""
 :Deadb_commandion:    录屏操作
 :author          80071482/bony
 :@version         V1.1
 :@Date            2017年05月
"""


class ScreenRecord(threading.Thread):
    def __init__(self, device):
        threading.Thread.__init__(self)
        self._DEVICE = device
        self._SIZE = None
        self._BIT_RATE = None
        self._ROTATE = None
        self._RECORD_PATH = None
        self._RECORD_NAME = None
        self._SP = None
        self._STR_OUT = None
        self._STR_ERR = None

    def run(self):
        cmd = "adb shell screenrecord"
        if self._SIZE is not None:
            cmd += " --size %d" % self._SIZE
        if self._BIT_RATE is not None:
            cmd += " --bit-rate %d" % self._BIT_RATE
        if self._ROTATE is not None:
            cmd += " --rotate %d" % self._ROTATE
        if self._RECORD_PATH is None:
            self._RECORD_PATH = "/sdcard/"
        if self._RECORD_NAME is None:
            self._RECORD_NAME = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".mp4"
        cmd += ("  %s%s" % (self._RECORD_PATH, self._RECORD_NAME))
        self._SP = subprocess.Popen(self._DEVICE.make_cmd(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        self._STR_OUT, self._STR_ERR = self._SP.communicate()
        time.sleep(0.5)

    def start_screen_record(self, size=None, bit_rate=None, rotate=None, record_path=None, record_name=None):
        self._SIZE = size
        self._BIT_RATE = bit_rate
        self._ROTATE = rotate
        self._RECORD_PATH = record_path
        self._RECORD_NAME = record_name
        self.start()

    def stop_screen_record(self, path=None):
        if self._SP is not None:
            self._SP.terminate()
            time.sleep(0.5)
            if path is not None:
                self.get_screen_record_file(path)
            self._SP = None

    def get_screen_record_file(self, path=None):
        if self._RECORD_PATH is not None and self._RECORD_NAME is not None:
            if path is None:
                self._DEVICE.adb_command(
                    "adb pull %s%s ./%s" % (self._RECORD_PATH, self._RECORD_NAME, self._RECORD_NAME))
            else:
                self._DEVICE.adb_command(
                    "adb pull %s%s %s%s" % (self._RECORD_PATH, self._RECORD_NAME, path, self._RECORD_NAME))
        self._RECORD_PATH = None
        self._RECORD_NAME = None
