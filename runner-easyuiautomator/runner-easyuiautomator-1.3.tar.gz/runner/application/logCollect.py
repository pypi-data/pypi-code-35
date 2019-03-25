#coding=utf-8
'''
Created on 2016年12月19日

@author: Administrator
'''
import threading, os,traceback
from runner.common.log import Logger

class LogCollect(object):
    
    __instance = None
    __mutex = threading.Lock()

    def __init__(self, logCls):
        self.logger = Logger.getLogger()
        if logCls:
            self.logCollect = logCls  
        else:
            self.logCollect = DefaultLog()
    
    @staticmethod
    def getInstance(logCls=None):
        if LogCollect.__instance == None:
            LogCollect.__mutex.acquire()
            LogCollect.__instance = LogCollect(logCls)
            LogCollect.__mutex.release()
        return LogCollect.__instance
    
    def clearLog(self, adb):
        '''clear files of question dir '''
        self.logger.info("***clear %s log***"%adb.serial)
        self.logCollect.clearLog(adb)
    

    def saveLog(self, logpath, adb):
        '''Generate device log in destination folder.'''
        self.logger.info("***save %s log***"%adb.serial)
        self.logCollect.saveLog(logpath, adb)


question_dir = {
            'anr':('/data/anr/','*','trace','start'),
            'tombstone':('/data/tombstones/','tombstone_*','tombstone_','start'),
            'app_crash':('/data/system/dropbox/','*app_crash*','app_crash','search'),
#             'aplog':('/storage/sdcard0/logs/aplog/','*','log','end')
           }
class DefaultLog(object):
   
    def __init__(self):
        self.logger = Logger.getLogger()
        
    def clearLog(self, adb):
        '''clear files of question dir '''
        for key in question_dir.keys():
            if key != "aplog":
                value = question_dir.get(key)
                filefiter = value[0] + value[1]
                try:
                    data = adb.delFile(filefiter)
                    if data:
                        if 'Permission denied' in data[0]:
                            self.logger.warning(data[0])
                except:
                    self.logger.warning(traceback.format_exc(3))
    

    def saveLog(self, logpath, adb):
        '''Generate device log in destination folder.'''
        try:
            for key in question_dir.keys():
                if key == "aplog": 
                    filelist = self.getFileList(key, adb)
                if key == "anr":
                    filelist = self.getFileList(key, adb)
                if key == "tombstone":
                    filelist = self.getFileList(key, adb)
                if key == "app_crash":
                    filelist = self.getFileList(key, adb)
                self.adbPull(key, filelist, logpath + "/" + key + "/" + str(adb.serial), adb)
        except:
            self.logger.warning(traceback.format_exc(3))
    
    
    def adbPull(self, filetype, filenames, targetdir, adb):
        try:
            if filenames:
                if not os.path.exists(targetdir):
                    os.makedirs(targetdir)
                filedir = question_dir.get(filetype)[0]
                self.logger.info("pull files of %s"%filedir)
                for fileName in filenames:
                    adb.pull(filedir + fileName, targetdir) 
        except:
            self.logger.warning(traceback.format_exc(3))
        
    def getFileList(self, filetype, adb, searchType=None):
        ''' get filedir list
        :Args:
        filetype: questtion_dir anr','tombstone','app_crash','aplog
        searchType: start end search
        '''
        filelist = []
        try:
            value = question_dir.get(filetype)
            datas = adb.shell('ls %s'%value[0])
            self.logger.info("get filelist of %s"%value[0])
            if datas:
                if 'Permission denied' in datas[0]\
                or 'No such file or directory' in datas[0]:
                    self.logger.warning(str(datas))
                    return filelist
            if searchType is None:
                searchType = value[3]
            for data in datas:
                if searchType == "start":
                    if data.startswith(value[2]):
                        filelist.append(data)
                if searchType == "end":
                    if data.endswith(value[2]):
                        filelist.append(data)
                if searchType == "search":
                    if data.find(value[2]) > -1:
                        filelist.append(data) 
        except:
            self.logger.warning(traceback.format_exc(3))
        return filelist
    
    