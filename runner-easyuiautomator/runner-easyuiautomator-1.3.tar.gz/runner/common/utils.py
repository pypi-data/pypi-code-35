# coding=utf-8
"""
Created on 2015年11月27日

@author: thomas.ning
"""
import time,os,sys


def format_time(timesamp, format='%Y.%m.%d-%H.%M.%S'):
    """
    use given format to format timestrap
    """
    return time.strftime(format, time.localtime(timesamp))


def format_time_diff(timediff):
    """
    format time diff to (H M S)
    """
    if timediff > 60 * 60:
        hour = int(timediff / (60 * 60))
        return str(hour) + " H " + format_time_diff(timediff - (hour * 60 * 60))
    elif timediff > 60:
        min = int(timediff / 60)
        return str(min) + ' M ' + format_time_diff(timediff - (min * 60))
    else:
        return str(round(timediff, 3)) + " S"
    
def searchFile(filepath,searchFile):
    """
    by given dir,search file
    """
    if os.path.exists(filepath):
            for dirpath, dirname, files in os.walk(filepath):
                for filename in files:
                    if filename == searchFile:
                        target_path = os.path.join(dirpath, filename)
                        return target_path
    else:
        return None
    
def waitForCondition(method, returnValue, timeout=5, intervalMs=0.5, args=None):
    '''等待条件超时函数，根据函数返回值条件，确认是否跳出
    ：    :Args:
        methon: 函数名
        args: 必须是元组参数传递形式，如（'tt',dd)
        returnValue:对比值
    '''
    end_time = time.time() + timeout
    while True:
        try:
            if args is None:
                tmp = method()
            else:
                tmp = method(*args)
            if tmp == returnValue:
                return True
        except:
            print sys.exc_info()
        if time.time() - end_time>0:
            return None
        time.sleep(intervalMs)     
    
class FileUtil(object):
    '''
    Add File
    '''
    @classmethod
    def writeDataAppend(cls,filename, data):
        cls.writeData(filename, data, "a")
            
    @classmethod
    def writeData(cls, filename, data, mode):
        with open(filename, mode) as f:
            f.write(data)
            