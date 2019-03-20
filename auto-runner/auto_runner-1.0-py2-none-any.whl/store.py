# coding=utf-8

import os,threading,time
from auto_runner import utils

_DEFAULT_PATH = "./report"


class Store(object):
    """store the case result data """
    
    _instance = None
    _mutex = threading.Lock()

    def __init__(self):
        self.TEST_FLAG = False
               
    @staticmethod
    def getInstance():
        if (Store._instance == None):
            Store._mutex.acquire()
            if (Store._instance == None):
                Store._instance = Store()
            Store._mutex.release()
        return Store._instance
    
    def init(self):
        self.report_path = os.path.join(os.path.abspath(_DEFAULT_PATH), utils.format_time(time.time()))
        self.TEST_FLAG = True
        
    def createOutDirs(self, case=None):
        if self.TEST_FLAG:
            self.out_dir = self.__createOutDirs(case)
            
    def __createOutDirs(self, case):         
        foldername = '%s' % (case._testMethodName)
        foldername_with_timestamp = '%s-%s' % (foldername, case.starttime)
        out_dir = os.path.join(self.report_path, foldername_with_timestamp)
        try:
            os.makedirs(out_dir)
        except:
            pass
        return out_dir
        
    def getWorkDir(self):
        return self.out_dir
