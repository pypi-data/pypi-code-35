# coding=utf-8

"""
Created on 2015年12月25日

@author: hal
"""

from runner.common.log import Logger as Loggerr
from runner.common.runnerlog import RunnerLog as Logger
from runner.common.assertion import Assertion
from .device import DeviceManage
from .builder import TestBuilder
from easyuiautomator.common.ftpDownload import FtpDownLoad


class Model(object):
    """
    Model Functions
    """  
    __phoneNumList = []
    
    def __init__(self, case=None, order=None):
        self.device = DeviceManage.getInstance().getTestDriver(order, case)
        self.order = order
        self.logger = Loggerr.getLogger()
        self.assertion = Assertion(order)
    
    @staticmethod
    def getProjectConfig():
        return TestBuilder.getBuilder().getProjectConfig()

    @classmethod
    def getPhoneNumList(cls):
        if cls.__phoneNumList:
            return cls.__phoneNumList
        phoneNum = None
        project_config = cls.getProjectConfig()
        if project_config:
            phoneNum = project_config.get('phone_num')
        else:
            Logger.warning("get phonenum failue")
        if phoneNum:
            phoneNums = phoneNum.split(",")
            for p in phoneNums:
                cls.__phoneNumList.append(p)
            return cls.__phoneNumList
        
    @staticmethod  
    def downLoadPreResourceFile(remoteFile, localFile):
        '''下载远程服务器资源 文件'''
        ftpconncet = FtpDownLoad()
        ftpconncet.downLoadFile(remoteFile, localFile)
        
    @staticmethod  
    def downLoadPreResourceDir(remoteDir, localdir):
        '''下载远程服务器资源 目录'''
        ftpconncet = FtpDownLoad()
        ftpconncet.downLoadDir(remoteDir, localdir)
        
        
    def startLogcat(self, package=None, filter_b=None, filter_t=None):
        self.device.startLogcat(package=package, filter_b=filter_b, filter_t=filter_t)
        self.device.sleep(3)
        
    def stopLogcat(self):
        self.device.stopLogcat()

