# coding=utf-8
'''
Created on 2016年6月28日

@author: Administrator
'''
import time, os
from easyuiautomator.driver.executor.adb import ADB
from runner.common.log import Logger

class Logcat(object):
    '''
    get logcat by curstom
    '''
    _default_log = "realtime.log"
    _default_save_log = "/data/local/tmp/"
    
    filter_buffer={"all":"-b all",
                    "radio":"-b radio",
                    'default':"-b main -b system",   #-b crash
                    'events': "-b events"  
                  }
    
    filter_tag = {'warning':'*:W',
                  'error':'*:E',
                  'debug':'*:D',
                  'fatal':'*:F',
                  'verbose':'*:V',
                  'silent':'*:S',
                  }

    def __init__(self, serial, package=None, store=None,\
                 filter_b='default', filter_t='debug', log_format="time"):
        '''
        :Args:
            serial: device serial
            log_path: dir of logcat make
            filter_b: buffer area default:default
            filter_t: tag filter default: debug
            format: logcat output format default:time
        
        '''
        self.logcatProcess = None # logcat realtime process
        self.adb = ADB(serial, False)
        self.logger = Logger.getLogger()
        b_tag = filter_b if filter_b else 'default'
        t_tag = filter_t if filter_t else 'debug';
        self.filter_b =  self.filter_buffer.get(b_tag)
        self.filter_t = self.filter_tag.get(t_tag)
        if package:
            self.setFiltert(package, filter_t)
        self.format = log_format
        self.logname = time.time()
        if store:
            self.logpath = os.path.join(store.getWorkDir(),"%s-%s-%s-%s"%(serial, b_tag, t_tag, self._default_log))
        else:
            self.logpath = os.path.join(os.getcwd(), "%s-%s-%s-%s"%(serial, b_tag, t_tag, self._default_log))
            
    
    def setFilterb(self, filter_b='default'):
        ''' set log filter b'''
        if filter_b is None:
            filter_b = 'default'
        self.filter_b = self.filter_buffer.get(filter_b)
        
    def setFiltert(self, package=None, filter_t='debug'):
        ''' set log filter tag '''
        if filter is None:
            filter_t = 'debug'
        filter_get = self.filter_tag.get(filter_t)
        if package:
            filter_get = filter_get.replace("*", package)  
        self.filter_t = filter_get
    
    def _getLogcatCmd(self):
        logcatcmd = "logcat -v %s %s %s"%(self.format,self.filter_b,self.filter_t)        
        finalcmd = "shell \"cd " + self._default_save_log + ";" \
        + logcatcmd  + ">" + str(self.logname)+".log &\""
        return finalcmd
    
    def _clear_logcat(self):
        self.adb.killProcessesByName('logcat')
        self.adb.shell("logcat -c")
    
    def startRecorder(self):
        '''recoder log'''
        self.logger.debug("start recorder logcat")
        self._clear_logcat()
        self._recorder_log()
    
    def _recorder_log(self):
        '''recorder realtime logcat'''
        self.logcatProcess = self.adb.cmd(self._getLogcatCmd())
        time.sleep(2)
        self.logcatProcess.terminate()
               
    def stopRecorder(self):
        '''stop recorder'''
        self.logger.debug("stop recorder logcat")
        self.adb.killProcessesByName('logcat')
        file_name = self._default_save_log + str(self.logname)+'.log'
        self.adb.pull(file_name, self.logpath)
        self.adb.shell("rm -rf " + file_name)

if __name__ == "__main__":
    
    log = Logcat('3297b469',filter_b="all",filter_t="debug") 
    log.startRecorder()
    time.sleep(10)
    log.stopRecorder()
        
        