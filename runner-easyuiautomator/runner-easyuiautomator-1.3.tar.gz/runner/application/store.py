# coding=utf-8
"""
Created on 2015年12月2日

@author: thomas.ning
"""
import os,threading
from .builder import TestBuilder
from .testcontroller import TestController

_DEFAULT_PATH = {'right': './report/right',
                 'all': './report/all',
                 'fail': './report/fail',
                 'error': './report/error'
                 }


class Store(object):
    """store the case result data """
    
    _instance = None
    _mutex = threading.Lock()

    def __init__(self, case=None):
        self.builder = TestBuilder.getBuilder()
        self.testcontroller = TestController.getInstance()
               
    @staticmethod
    def getInstance():
        if (Store._instance == None):
            Store._mutex.acquire()
            if (Store._instance == None):
                Store._instance = Store()
            Store._mutex.release()
        return Store._instance
    
    def createOutDirs(self, case=None):
        if case is None or self.builder.getBuildOption() is None:
            self.outdirs = _DEFAULT_PATH
        else:
            self.outdirs = self.__createOutDirs(case)
            
    def __createOutDirs(self, case):
        dirs = {}
        workspace = self.builder.getWorkspace()
        currentCycle = str(self.testcontroller.getCurrentCycle())
        testCaseOrder = str(self.testcontroller.getTestcaseOrder())               
        foldername = '%s' % (case._testMethodName)
        foldername_with_timestamp = '%s-%s-%s-%s' % (
            foldername,  currentCycle, testCaseOrder, case.starttime)
        dirs['all'] = os.path.join(workspace, 'all', foldername_with_timestamp)
#         dirs['right'] = os.path.join(workspace, 'right', foldername_with_timestamp)
        dirs['fail'] = os.path.join(workspace, 'fail', foldername_with_timestamp)
#         dirs['error'] = os.path.join(workspace, 'error', foldername_with_timestamp)
        for k in ['all']:
            try:
                os.makedirs(dirs[k])
            except:
                pass
        return dirs

    def getWorkDir(self):
        return self.outdirs['all']

    def getRightDir(self):
        return self.outdirs['right']

    def getFailDir(self):
        return self.outdirs['fail']

    def getErrorDir(self):
        return self.outdirs['error']
