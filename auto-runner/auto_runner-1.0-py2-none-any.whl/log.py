# coding=utf-8
import threading
from easyuiautomator.common.log import Logger as parentlog

class Logger(object):
    _FrameWork = "[FRAMEWORK] "
    _instance = None
    _mutex = threading.Lock()
    
    def __init__(self, name="auto_runner", path=None, saveLogtype=None, unit=None, level="DEBUG"):
        self.logger = parentlog.getLogger(name, path, saveLogtype, unit, level)
        
    @staticmethod
    def getLogger(name="auto_runner", path=None, saveLogtype=None, unit=None, level="DEBUG"):
        if (Logger._instance == None):
            Logger._mutex.acquire()
            if (Logger._instance == None):
                Logger._instance = Logger(name, path, saveLogtype, unit, level)
            Logger._mutex.release()
        return Logger._instance
    
    @staticmethod
    def setDebug(switch=True):
        parentlog.set_debug(switch)
        
    @staticmethod 
    def set_filter(tag):
        '''设置过滤标签，debug,error,info'''
        parentlog.set_fitler(tag)
    
    def getMsg(self):
        '''获取运行期间日志内容'''
        return self.logger.getMsg()
    
    def setLogOn(self):
        self.logger.setLogOn()
       
    def setLogOff(self):
        self.logger.setLogOff()
    
    def debug(self, msg):
        self.logger.debug(self._format_log(msg))

    def warning(self, msg):
        self.logger.warning(self._format_log(msg))

    def error(self, msg):
        self.logger.error(self._format_log(msg))

    def critical(self, msg):
        self.logger.critical(self._format_log(msg))

    def info(self, msg):
        self.logger.info(self._format_log(msg))
            
    def _format_log(self, msg):
        '''区分上层日志与框架日志'''
        msg = str(msg)
        if not msg.startswith("[UPPER]"):
            msg = self._FrameWork + msg
        return msg

                