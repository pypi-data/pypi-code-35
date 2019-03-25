# coding=utf-8
"""
Created on 2015年11月27日

@author: thomas.ning
"""
import threading,os
from testdriver import TestDriver as Driver
from runner.common.log import Logger
from .builder import TestBuilder


class DeviceManage(object):
    """
    manage device
    """
    __instance = None
    __mutex = threading.Lock()
    __test_driver = []
    __port = 4724

    def __init__(self):
        self.logger = Logger.getLogger()
        self.testBuilder = TestBuilder.getBuilder()
        self.devices = self.testBuilder.getDeviceSerial()
        self._create_driver(self.devices)
        
    @staticmethod
    def getInstance(devices=None):
        """Return a single instance of TestBuilder object """
        if (DeviceManage.__instance == None):
            DeviceManage.__mutex.acquire()
            if (DeviceManage.__instance == None):
                DeviceManage.__instance = DeviceManage()
            DeviceManage.__mutex.release()
        return DeviceManage.__instance

    def getTestDriver(self, order=None, case=None):
        '''
        To meet the test requirements, add Model layer get device by device serial number 
        '''
        if isinstance(order, str):
            test_driver = Driver.connect_device(order)
        else:
            test_driver = self.__create_driver(order)
        if case != None:
            test_driver.set_store(case.store)
        return test_driver 
    
    def __create_driver(self, order=None):
        '''create test_driver'''
        restart = self.testBuilder.getRestartMode()
        testdriver = None
        if order is None or self.devices is None:
            if len(self.__test_driver) == 1:
                return self.__test_driver[0]
            testdriver = Driver.connect_device(restart=restart)
            self.__test_driver.append(testdriver)
        else:
            if len(self.__test_driver) > order:
                testdriver = self.__test_driver[order]
            else:
                devices = self.devices.split(",")
                testdriver = Driver.connect_device(devices[order],restart=restart)
                self.__test_driver.append(testdriver)
        self.batteryMonitor()
        return testdriver     

    def _create_driver(self, devices=None):
        self.logger.debug('***************************init device************************')
        restart = self.testBuilder.getRestartMode()
        if devices is None:
            serial= os.getenv("ANDROID_SERIAL")
            if serial:
                testdriver = Driver.connect_device(serial, restart=restart)
            else:
                testdriver = Driver.connect_device(restart=restart)
            self.__test_driver.append(testdriver)
        else:
            deviceserials = devices.split(",")
            for deviceid in deviceserials:
                testdriver = Driver.connect_device(deviceid,restart=restart)
                self.__test_driver.append(testdriver)
        self.logger.debug('***************************init device complete************************')
        
    def getDeviceId(self, order=None):
        '''get device serial by order'''
        if order:
            return self.__test_driver[order].serial
        return self.__test_driver[0].serial
    
    def getAllDeviceId(self):
        '''get all device serial'''
        return [test_driver.serial for test_driver in self.__test_driver]
    
    def setStore(self, store):
        '''set current case store path'''
        for test_driver in self.__test_driver:
            test_driver.set_store(store)
    
    def startAllLogcat(self, package=None, filter_b=None, filter_t=None):
        for test_driver in self.__test_driver:
            try:
                test_driver.startLogcat(package, filter_b, filter_t)
            except:
                pass

    def stopLogcat(self):
        '''停止日志并收集日志'''
        for test_driver in self.__test_driver:
            self._closeTestResource(test_driver.stopLogcat)

    def quit(self):
        for test_driver in self.__test_driver:
#             self._closeTestResource(test_driver.stop_battery_monitor) 
            self._closeTestResource(test_driver.quit)
            
    def batteryMonitor(self):
        if self.testBuilder.getBatteryMonitor():
            hight = self.testBuilder.getBatteryHigh()
            low = self.testBuilder.getBatteryLow()
            adbd_monitor = self.testBuilder.getAdbdMonitor()
            adbd_thredhold = self.testBuilder.getAdbdLastTime()
            try:
                self.__test_driver[0].start_battery_monitor(hight,low, \
                    adbd_monitor, adbd_thredhold)
            except:
                pass
        else:
            self.logger.debug('battery monitor state is False')
            
    def cleanCache(self):
        for test_driver in self.__test_driver:
            self._closeTestResource(test_driver.clear_cache)   
                
    def _closeTestResource(self,functionRe):
        '''清理资源，关闭资源'''
        try:
            functionRe()
        except:
            pass
            
