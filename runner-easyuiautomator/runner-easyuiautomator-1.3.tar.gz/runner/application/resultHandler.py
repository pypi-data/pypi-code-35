# coding=utf-8
"""
Created on 2015年11月27日

@author: thomas.ning
"""
import shutil, os, traceback,json
from datetime import datetime
from .builder import TestBuilder
from .testcontroller import TestController
from runner.common.log import Logger
from .device import DeviceManage
from .logCollect import LogCollect
from .resultCollect import ResultCollect
from easyuiautomator.driver.executor.adb import ADB
from easyuiautomator.common.exceptions import DriverException

logger = Logger.getLogger()

class ResultHandler(object):
    '''deal case test result by info'''

    @staticmethod
    def handle(info=None, path=None):
        # load test setting
        if info is None:
            return
        if info[0] in ['addFailure', 'addError','addSuccess']:
            DeviceManage.getInstance().stopLogcat()
        if info[0] == "addError":
            if 'self.tearDown()' == traceback.extract_tb(info[1][2][2], 1)[0][-1]:
                logger.warning(traceback.format_exc(3))
                return
        adb_list = []
        device = None
        if info[0] == 'addFailure' or info[0] == 'addError':
            device = getExceptionDevice(info)
        if device is None: # 假如返回的设备id为空，则获取所有连接的设备id
            device = DeviceManage.getInstance().getAllDeviceId()
        if isinstance(device, list): # 假如是列表，全部添加 到_adb_list
            for device_serial in device:
                adb_list.append(ADB(device_serial, restart=False))
        else:
            adb_list.append(ADB(device, restart=False))
        try:
            errImag = _sortTestCaseResult(info, adb_list)
            errImag = errImag[0] if errImag else ""
            ResultCollect.getInstance().addInfo(info, errImag)
        except:
            logger.error(traceback.format_exc(3))
            
def getExceptionDevice(info):
    '''当case发生错误时，返回执行错误时的设备id'''
    device_serial = None
    try:
        caseException = info[1][2][0]
        if caseException.__name__ == "DeviceNotFound":
            TestController.getInstance().setStopFlag()
        elif caseException.__name__ == "AssertionError": # 当是assertionError错误时，获取信息未尾设备序号
            deviceOrder = (info[1][2][1].message)[-1:]
            device_serial = DeviceManage.getInstance().getDeviceId(int(deviceOrder))
        elif isinstance(info[1][2][1], DriverException):
            error_msg = json.loads(info[1][2][1].message)
            device_serial = error_msg.get("device")
    except:
        logger.warning("get Exception device serial failure")
    return device_serial
    

def _sortTestCaseResult(info, adblist):
    """Sort test case result from "all" folder.
    Keyword arguments:
    info -- tuple of test case object description.(should not be none)
    """
    if info[0] == 'startTest':
#         clearCustomLog()
        return
    
    if not info[0] in ['addFailure', 'addError', 'addSuccess']:
        return
    dest = None
    imageName = None
    try:        
        src = info[1][1].store.getWorkDir()
        dest = info[1][1].store.getFailDir()
    except Exception, e:
        logger.warning('case module error: setupclass or teardownclass error' + str(e))
    if info[0] == 'addFailure' or info[0] == 'addError':
        logger.info('Get error screenshot')
        imageName = _takeImage(src, adblist)  # wether all device takeshot,current 
#     saveCustomLog(src) # 保存自定义日志
    if dest:
        _copyFilesToOtherFolder(src, dest)
    return imageName

def saveCustomLog(src):
    '''保存自定义日志'''
    devices = DeviceManage.getInstance().getAllDeviceId()
    adb_list = []
    for device in devices:
        adb_list.append(ADB(device, restart=False))
    logCollect = LogCollect.getInstance()
    if not TestBuilder.getBuilder().getPreTests(): # pre test, not sava log
        logger.info('Get all device log')
        for adb in adb_list:
            logCollect.saveLog(src, adb) 

def clearCustomLog():
    '''清理自定义日志'''
    devices = DeviceManage.getInstance().getAllDeviceId()
    adb_list = []
    for device in devices:
        adb_list.append(ADB(device, restart=False))
    logCollect = LogCollect.getInstance()
    logger.info('clear all device log')
    for adb in adb_list:
        logCollect.clearLog(adb) # clear question file

def _takeImage(target, adblist):
    '''take image to target dir'''
    errimgs =[]
    for adb in adblist:
        try:
            timestr = str(datetime.now()).replace(' ', '=').replace(':', '-')
            erroimg = 'error_img-%s-%s.png'%(adb.serial, timestr)
            logger.info('takshot to %s'%erroimg)
            adb.takeScreenshot(os.path.join(target, erroimg))
            errimgs.append(erroimg)
        except:
            logger.warning(traceback.format_exc(3))
    return errimgs

            
def _copyFilesToOtherFolder(src, dest):
    '''Copy test failures or error case from source folder to destination folder.
    Keyword arguments:
    src -- Path of source folder. (should not be none)
    dest -- Path of destination folder(should not be none)
     '''
    try:
        shutil.copytree(src, dest)
    except:
        logger.warning(traceback.format_exc(3))

