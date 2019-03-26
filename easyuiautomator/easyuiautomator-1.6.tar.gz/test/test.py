# coding=utf-8
from easyuiautomator.driver.driver import Driver
app = Driver.connect_device()
app.stop_third_app()
