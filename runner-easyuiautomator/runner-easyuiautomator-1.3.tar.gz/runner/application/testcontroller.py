# coding=utf-8
"""
Created on 2015年11月23日

@author: thomas.ning
"""
import threading, time
from runner.application.builder import TestBuilder

class TestController(object):
    """store test procedure"""
    __instance = None
    __mutex = threading.Lock()
    __STOP_FLAG = False
    __CURRENT_CYCLE = 1
    __CYCLE_START_TIME = None
    __CaseLine = 0
    __TEST_ORDER = 1
    __CASE_NAME = None

    def __init__(self):
        pass
    
    @staticmethod
    def getInstance():
        """Return a single instance of TestBuilder object """
        if (TestController.__instance == None):
            TestController.__mutex.acquire()
            if (TestController.__instance == None):
                TestController.__instance = TestController()
            TestController.__mutex.release()
        return TestController.__instance
    
    def getStopFlag(self):
        return self.__STOP_FLAG
    
    def setStopFlag(self,flag=True):
        self.__STOP_FLAG = flag

    def stopTest(self):
        self.__STOP_FLAG = True
        from .device import DeviceManage
        DeviceManage.getInstance().quit()

    def getCurrentCycle(self):
        return self.__CURRENT_CYCLE

    def setCurrentCycle(self, cycle):
        self.__CURRENT_CYCLE = cycle
        from .resultCollect import ResultCollect
        ResultCollect.getInstance().reset()
        self.setCycleStartTime(time.time())
        self.clearCaseLine()

    def getTestcaseOrder(self):
        return self.__TEST_ORDER

    def setTestcaseOrder(self, case):
        casename = case._testMethodName
        caseCyc = TestBuilder.getBuilder().getTestNumByName(casename)
        if self.__CASE_NAME != casename:
            self.__CASE_NAME = casename
            self.__TEST_ORDER = 1
            self.__CaseLine += 1
        else:
            self.__TEST_ORDER += 1
            if self.__TEST_ORDER > caseCyc:
                self.__TEST_ORDER = self.__TEST_ORDER - caseCyc
                self.__CaseLine += 1

    def getCycleStartTime(self):
        return self.__CYCLE_START_TIME

    def setCycleStartTime(self, timestamp):
        self.__CYCLE_START_TIME = timestamp
        
    def getRunningState(self):
        runningState = {"caseLineNum": self.__CaseLine, "caseName":self.__CASE_NAME, "currentCaseCycle":self.__TEST_ORDER, "currentCycle":self.__CURRENT_CYCLE}
        return runningState
    
    def getCurrentcaseOrder(self):
        return self.__TEST_ORDER
    
    def clearCaseLine(self):
        """
        clearCaseLine 清理case行数计数，用于统计plan计划中case执行总数
        """
        self.__CaseLine = 0        
