# coding=utf-8

import logging, threading
import os, sys, time


# File Level
FILE_LOG_LEVEL = "DEBUG"

# Console Level
CONSOLE_LOG_LEVEL = "INFO"

# logger levels
LEVELS = {"CRITICAL": 50,
          "ERROR": 40,
          "WARNING": 30,
          "INFO": 20,
          "DEBUG": 10,
          "NOTSET": 0,
          }
LOG_FILE_PATH = "./log"
'''
getLogger(name="easyuiautomator", path=None,  saveLogtype=None, unit=None, level="DEBUG")
name :         log tag
path :         log sava path
savelogtype:   logfile sava type :[time, size] split file type
unit       :   by savelogtype time(s) size(Byte)
'''
if(sys.getdefaultencoding() != "utf-8"):
    reload(sys)
    sys.setdefaultencoding('utf-8')

class Logger:
    _instance = None
    _mutex = threading.Lock()
    _debug = False  # False 关闭手机端回复日志
    _Flag = False # 运行日志获取标志位
    _message = "" # 截取日志详细信息
    _FrameWork = "[SYSTEM] " # 系统层标签
    _Fitler_Tag = "[DEBUG]"

    def __init__(self, name=None, logPath=None, saveLogtype=None, unit=None, level="DEBUG"):
        """
        Generate root logger.
        """
        if logPath is None:
            logPath = LOG_FILE_PATH
        logPath = os.path.abspath(logPath)
        self.saveType = ["size", 20*1024*1024]
        if saveLogtype:
            self.saveType = [saveLogtype, unit]
        self._logger = logging.getLogger(name)
        self._logger.setLevel(LEVELS[level])
        self._formatter = logging.Formatter("[%(asctime)s] - %(levelname)s : %(message)s", '%Y-%m-%d %H:%M:%S')
        self.add_console_logger()
        self.add_file_logger(logPath)
        
    @staticmethod
    def getLogger(name="easyuiautomator", path=None,  saveLogtype=None, unit=None, level="DEBUG"):
        if (Logger._instance == None):
            Logger._mutex.acquire()
            if (Logger._instance == None):
                Logger._instance = Logger(name, path, saveLogtype, unit, level)
            Logger._mutex.release()
        return Logger._instance 
           
    @classmethod
    def set_debug(cls, debug=True):
        '''Set the log debug mode '''
        cls._debug = debug
    
    @classmethod
    def set_fitler(cls, tag):
        '''set log filter tag'''
        cls._Fitler_Tag = "[%s]"%tag.upper()

    def add_file_logger(self, logFile=None, level="DEBUG"):
        """
        Generate file writer [RotatingFileHandler].
        """
        if not os.path.exists(logFile):
            os.makedirs(logFile)
        path = os.path.join(logFile,'runntime')
        if self.saveType[0] == "size":
            fh = MyLoggerSizeHandler(path, self.saveType[1])
        elif self.saveType[0] == "time":
            fh = MyLoggerTimeHandler(path, self.saveType[1])
        fh.suffix = "%Y%m%d-%H%M.log"
        fh.setLevel(LEVELS[level])
        fh.setFormatter(self._formatter)
        self._logger.addHandler(fh)

    def add_console_logger(self, level="DEBUG"):
        """
        Generate console writer [StreamHandler].
        """
        ch = logging.StreamHandler()
        ch.setLevel(LEVELS[level])
        ch.setFormatter(self._formatter)
        self._logger.addHandler(ch)
    
    def getMsg(self):
        '''获取运行期间日志内容'''
        return self._message
    
    def setLogOn(self):
        self._Flag = True
        self._message = ""

    def setLogOff(self):
        self._Flag = False
 
    def _format_log(self, logType, msg):
        '''区分上层日志与框架日志'''
        format_msg = str(msg)
        if format_msg.startswith("[FRAMEWORK]"):
            format_msg = format_msg.replace("[FRAMEWORK]","[FRAMEWORK]" + logType )
        elif format_msg.startswith("[UPPER]"):
            format_msg = format_msg.replace("[UPPER]","[UPPER]" + logType )
        else:
            format_msg = self._FrameWork + logType + format_msg
            msg = self._FrameWork + str(msg)
#         if self._Flag == True:
#             if not logType.startswith(self._Fitler_Tag):
#                 self._message += self._format_logPrefix() + format_msg + "\n"
        return msg
        
    def _format_logPrefix(self):
        '''日志前缀''' 
        return str(time.strftime('[%Y.%m.%d-%H.%M.%S] ', time.localtime(time.time())))

    def debug(self, msg):
        msg = self._format_log("[DEBUG] ", msg)
        self._logger.debug(msg)
        
    def info(self, msg):
        msg = self._format_log("[INFO] ", msg)
        self._logger.info(msg)

    def warning(self, msg):
        msg = self._format_log("[WARNING] ", msg)
        self._logger.warning(msg)

    def error(self, msg):
        msg = self._format_log("[ERROR] ", msg)
        self._logger.error(msg)

    def critical(self, msg):
        msg = self._format_log("[CRITICAL] ", msg)
        self._logger.critical(msg)
       
    
class MyLoggerTimeHandler(logging.Handler):
    
    def __init__(self, filePrefix=None, splitTime=2*60*60):
        
        self.filePrefix = filePrefix
        self.last_time = 0
        self.splitTime = splitTime
        self.filePath = ""
        logging.Handler.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        if self.last_time == 0:
            self.last_time = time.time()
        elif time.time() - self.last_time > self.splitTime:
            self.last_time = time.time()
        file_name = time.strftime('%Y%m%d-%H%M%S', time.localtime(self.last_time))
        self.filePath = self.filePrefix + file_name + ".log"
        with open(self.filePath, 'a') as f:
            f.write(msg+"\n")
            f.flush()
            
class MyLoggerSizeHandler(logging.Handler):
    
    def __init__(self, filePrefix=None, splitSize=20*1024*1024):
        
        self.filePrefix = filePrefix
        self.splitSize = splitSize
        self.filePath = None
        logging.Handler.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        file_name = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
        if self.filePath:
            size = os.path.getsize(self.filePath)
            if size > self.splitSize:
                self.filePath = self.filePrefix + file_name + ".log"     
        else:
            self.filePath = self.filePrefix + file_name + ".log"
        with open(self.filePath, 'a') as f:
            f.write(msg+"\n")
            f.flush()
                
