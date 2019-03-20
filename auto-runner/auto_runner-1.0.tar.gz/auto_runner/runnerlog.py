# coding=utf-8
'''
Created on 2016年8月23日

@author: Hal
'''
from auto_runner.log import Logger

class RunnerLog(object):
    
    logger = Logger.getLogger()
    upper = "[UPPER] "
 
    @classmethod   
    def debug(cls, msg):
        cls.logger.debug(cls.upper + msg)
        
    @classmethod  
    def error(cls, msg):
        cls.logger.error(cls.upper + msg)
        
    @classmethod     
    def warning(cls, msg):
        cls.logger.warning(cls.upper + msg)
        
    @classmethod     
    def critical(cls, msg):
        cls.logger.critical(cls.upper  + msg)
        
    @classmethod     
    def info(cls, msg):
        cls.logger.info(cls.upper + msg)
        
    @classmethod    
    def check_pass(cls, msg):
        cls.logger.info(cls.upper + '[CHECK_PASS] '+ msg)
            
    @classmethod         
    def check_fail(cls, msg, order = None):
        cls.logger.error(cls.upper + '[CHECK_FAIL] '+ msg + " deviceOrder=%s" %(order if order else 0))
    