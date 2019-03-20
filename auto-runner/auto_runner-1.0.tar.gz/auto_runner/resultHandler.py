# coding=utf-8

import os, traceback
from datetime import datetime
from auto_runner.log import Logger
from auto_runner.resultCollect import ResultCollect
from easyuiautomator.driver.executor.adb import ADB
from easyuiautomator.common.exceptions import DriverException


class ResultHandler(object):
    '''deal case test result by info'''

    logger = Logger.getLogger()
    
    @classmethod
    def handle(cls, info=None, path=None):
        # load test setting
        if info is None:
            return
        if info[0] == "addError":
            if 'self.tearDown()' == traceback.extract_tb(info[1][2][2], 1)[0][-1]:
                cls.logger.warning(traceback.format_exc(3))
                return
        adb_list = [ADB(os.getenv('ANDROID_SERIAL'), restart=False)]
        try:
            errImag = cls._sortTestCaseResult(info, adb_list)
            errImag = errImag[0] if errImag else ""
            ResultCollect.getInstance().addInfo(info, errImag)
        except:
            cls.logger.error(traceback.format_exc(3))
            
    @classmethod       
    def _sortTestCaseResult(cls,info, adblist):
        """Sort test case result from "all" folder.
        Keyword arguments:
        info -- tuple of test case object description.(should not be none)
        """
        if info[0] == 'startTest' \
                or (not info[0] in ['addFailure', 'addError', 'addSuccess']):
            return
        imageName = None
        try:        
            src = info[1][1].store.getWorkDir()
        except Exception, e:
            cls.logger.warning('case module error: setupclass or teardownclass error' + str(e))
        if info[0] == 'addFailure' or info[0] == 'addError':
            cls.logger.info('Get error screenshot')
            imageName = cls._takeImage(src, adblist)  # wether all device takeshot,current 
        return imageName
    
    @classmethod
    def _takeImage(cls, target, adblist):
        '''take image to target dir'''
        errimgs =[]
        for adb in adblist:
            try:
                timestr = str(datetime.now()).replace(' ', '=').replace(':', '-')
                erroimg = 'error_img-%s-%s.png'%(adb.serial, timestr)
                cls.logger.info('takshot to %s'%erroimg)
                adb.takeScreenshot(os.path.join(target, erroimg))
                errimgs.append(erroimg)
            except:
                cls.logger.warning(traceback.format_exc(3))
        return errimgs