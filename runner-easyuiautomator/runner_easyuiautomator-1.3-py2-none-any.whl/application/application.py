# coding=utf-8
"""
Created on 2015年11月23日

@author: thomas.ning
"""

import time,traceback,sys,json
from runner.common.log import Logger
from runner.common.identifykey import IdentifyKey
from .builder import TestBuilder
from .testcontroller import TestController
from .testrunner import TestRunner
from .device import DeviceManage


class Application(object):
    """
    init logger builder runner before test
    """
    
    def __init__(self, options=None,):
        """
        init logger,builder,and DeviceManager before testing start
        """   
        self.builder = TestBuilder.getBuilder(options)
        self.logger = Logger.getLogger()
        self.runner = TestRunner.getRunner(self.builder)
        self.testController = TestController.getInstance()
        try:
            self.testsuites = self.builder.loadTestSuites()
            self.deviceManage = DeviceManage.getInstance()
        except:
            self.logger.error("test framework resource failure".center(40,"*"))        
            self.exceptLog(traceback.format_exc())
            sys.exit()
        self.logger.debug("test framework resource init completed".center(40,"*"))

    def run(self):
        try:
            for cycle in range(self.builder.getCycle()):
                self.logger.debug('start cycle:' + str(cycle + 1))
                self.testController.setCurrentCycle(cycle + 1)
                self.runner.run(self.testsuites)
                self.logger.debug('end cycle:' + str(cycle + 1))
                time.sleep(1)
        except: 
            self.exceptLog(traceback.format_exc())
        finally:
            self.logger.debug('clear test resouce'.center(40,"*"))
            self.testController.stopTest()
            self.logger.error(IdentifyKey._normalstop_prefix + 'case exec completed')
 
    def exceptLog(self, traceback):
        self.logger.error(IdentifyKey._erroresult_prefix +json.dumps({"task_id":self.builder.getTaskId(), "params":traceback}, ensure_ascii=False))
        raise 
        