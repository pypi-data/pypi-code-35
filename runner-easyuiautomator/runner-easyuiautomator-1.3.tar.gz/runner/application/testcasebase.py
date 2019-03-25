# coding=utf-8
"""
Created on 2015年11月23日

@author: thomas.ning
"""

import unittest,time
from runner.common.assertion import Assertion
from runner.common.log import Logger
from .device import DeviceManage
from .store import Store
from runner.application.builder import TestBuilder
from easyuiautomator.common.ftpDownload import FtpDownLoad


class TestCaseBase(unittest.TestCase):
        
    logger = Logger.getLogger()
    store = Store.getInstance()
    project = TestBuilder.getBuilder().getProjectConfig()
    
    def setUp(self):
        super(TestCaseBase, self).setUp()
        self.assertion = Assertion()
        self.starttime = time.strftime('%Y.%m.%d-%H.%M.%S', time.localtime(time.time()))
        self.store.createOutDirs(self)
        DeviceManage.getInstance().setStore(self.store)
        DeviceManage.getInstance().startAllLogcat()
    
    def tearDown(self):
        super(TestCaseBase, self).tearDown()
        self.logger.info("tearDown".center(40,"*"))
        DeviceManage.getInstance().cleanCache()
    
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
