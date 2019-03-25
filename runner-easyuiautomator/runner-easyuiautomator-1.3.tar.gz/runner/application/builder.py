# coding=utf-8
"""
Created on 2015年11月23日

@author: thomas.ning
"""

import os,time
import threading
import unittest
from runner.common.cofingparser import ConfigParser
from runner.common import utils
from runner.common.log import Logger

_Default_path = "./report"

class TestBuilder(object):
    """Class for store test session properties"""
    __instance = None
    __mutex = threading.Lock()
    __buildOption = {}

    def __init__(self, options=None):
        self.__buildOption = options      
        self.reportStartTime = time.time()
        self.logger = Logger.getLogger()
        self.deepPath = 0
        try:
            if self.__buildOption is None:
                self.logger.warning("project or plan config init failure")
                project = ConfigParser.readProject(self.searchProject())
                self.__buildOption = project
            else:
                project = ConfigParser.readProject(self.__buildOption.get("project"))
                self.__buildOption = dict(options, **project)
            self.workspace_path = self._init_workspace()
            self.plan = os.path.abspath(self.__buildOption.get('plan'))
        except:
            self.logger.warning("project or plan config init failure")
        
    def searchProject(self):
        path = self.__getTestCasePath(os.getcwd())
        if path:
            return os.path.join(path, "project")
          
    def __getTestCasePath(self, path):
        if self.deepPath > 10:
            return
        if os.path.basename(path) == "testcase":
            return path
        else:
            self.deepPath = self.deepPath + 1
            return self.__getTestCasePath(os.path.dirname(path))
            
    @staticmethod
    def getBuilder(option=None):
        """Return a single instance of TestBuilder object """
        if (TestBuilder.__instance == None):
            TestBuilder.__mutex.acquire()
            if (TestBuilder.__instance == None):
                TestBuilder.__instance = TestBuilder(option)
            TestBuilder.__mutex.release()
        return TestBuilder.__instance

    def setBuildOption(self, option):
        """Set an instance of CommandOption object which represent user commandline input"""
        self.__buildOption = option

    def getBuildOption(self):
        """:return build option"""
        return self.__buildOption
    
    def getDevicePort(self):
        '''assign port to device'''
        return self.__buildOption['port']
    
    def getStartTime(self):
        """Return the test session start time"""
        return self.reportStartTime
    
    def getTaskId(self):
        """return the taskid no."""
        return self.__buildOption.get('taskid')    
    
    def getProjectAddr(self):
        """return the project path"""
        return self.__buildOption.get('project_addr')
    
    def getPreTests(self):
        """Return the pretests state"""
        preTests = eval(self.__buildOption.get('pre_test'))
        if preTests:
            return True
        return False
    
    def getProjectConfig(self):
        """ get project config """
        return self.__buildOption
    
    def _init_workspace(self):
        '''初始化报告路径'''
        workspace = _Default_path
        if not os.path.exists(workspace):
            os.makedirs(workspace)
        report_folder_name = ('%s-%s' % ('result', utils.format_time(self.getStartTime())))
        report_path = os.path.join(workspace, report_folder_name)
        if not os.path.exists(report_path):
            os.makedirs(report_path)
        return os.path.abspath(report_path)   
        
    def getWorkspace(self):
        """Return the test session's report workspace """
        return self.workspace_path

    def getDeviceSerial(self):
        """Return the device serial number """
        if self.__buildOption:
            deviceSerial = self.__buildOption.get('device_serial')
            if deviceSerial.lower() != 'none':
                return deviceSerial

    def getCycle(self):
        """Return the cycle count of test session"""
        return int(self.__buildOption.get('cycle'))
    
    def getBatteryMonitor(self):
        """Return the battery monitor state"""
        if self.__buildOption is None:
            return False
        state = eval(self.__buildOption.get('power_monitor'))
        if state:
            return True
        return False
        
    def getAdbdMonitor(self):
        """Return the adbd monitor state"""  
        state = eval(self.__buildOption.get('adbd_monitor'))
        if state:
            return True
        return False
    
    def getBatteryHigh(self):
        """get battery high level"""
        batteryLevel = self.__buildOption.get('power_high')
        if batteryLevel:
            return int(batteryLevel)
        return 50
        
    def getBatteryLow(self):
        """get battery lower level"""
        batteryLevel = self.getProjectConfig().get('power_low')
        if batteryLevel:
            return int(batteryLevel)
        return 10
        
    def getAdbdLastTime(self):
        """get adbd last time"""
        adbdThreshold =  self.__buildOption.get('adbd_threshold')
        if adbdThreshold:
            return int(adbdThreshold)
        return 10

    def isUploadResult(self):
        """Return true if the session support uploading result to server feature"""
        uploadResult = self.__buildOption.get('upload_result')
        if uploadResult:
            if eval(uploadResult):
                return True
        return False

    def isLocalResult(self):
        """Return true if the session support to save test result in local"""
        localResult = eval(self.__buildOption.get('local_result'))
        if localResult:
            return True
        return False
    
    def getRestartMode(self):
        '''To determine whether mobile phone restart '''
        if self.__buildOption is None:
            return True
        restart = self.__buildOption.get('restart')
        if restart is None:
            return True
        return eval(restart)
        
    def getTestNumByName(self, name):
        """
        return testcase exec num by name
        """
        tests = self.getTests()
        t = None
        if type(tests) is type({}):
            t = tests.items()
        elif type(tests) is type([]):
            t = tests
        for (k, v) in t:
            if k.endswith(name):
                return v
        return 1

    def getTestsNum(self):
        """
        return tests exec total num
        """
        tests = self.getTests()
        totalcase = 0
        t = None
        if type(tests) is type({}):
            t = tests.items()
        elif type(tests) is type([]):
            t = tests
        for (k, v) in t:
            totalcase += v
        return totalcase

    def getTests(self):
        """Return the test case list specified by plan file """
        tests = ConfigParser.readTests(self.plan)
        return tests

    def loadTestSuites(self):
        '''载入测试计划，并转化为有效测试项'''
        return self._loadTestingTestSuites(self.getTests())

    def _loadTestingTestSuites(self, tests):
        '''转化测试计划到有效测试项'''
        names = []
        t = None
        if type(tests) is type({}):
            t = tests.items()
        elif type(tests) is type([]):
            t = tests
        for (k, v) in t:
            for i in range(int(v)):
                names.append(k)
        suite = unittest.TestLoader().loadTestsFromNames(names)
        return suite 
