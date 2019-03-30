import ATC
import time
from Command import Command
import threading
import subprocess


device = ATC.get_device()
# device.set_debug(True)
device.ScreenRecord.start_screen_record(record_path=None, record_name=u"a大武当.mp4")
for i in range(3):
    device.click(500, 500)
    device.click_back()
for i in range(3):
    device.swipe_to_left(0.8)
    device.swipe_to_right(0.8)
device.ScreenRecord.stop_screen_record("./")