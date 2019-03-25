# coding=utf-8
"""
Created on 2015年11月5日

@author: thomas.ning

Exceptions that may happen in all the runner code.

"""

class RunnerException(Exception):
    
    """
    Base driver exception.
    """
    pass

    
class TimeoutException(RunnerException):
    """
    Thrown when a command does not complete in enough time.
    """
    pass

class SocketConnectException(RunnerException):
    """
    Thrown when socket does not connect
    """
    pass

class AdbException(RunnerException):
    '''
    Thrown when error occured in ADB.
    '''
    pass

class RunningException(RunnerException):
    '''
    Thrown when running time.
    '''
    pass

class DeviceException(AdbException):
    """
    Thrown when error occured in device state
    """
    pass
    