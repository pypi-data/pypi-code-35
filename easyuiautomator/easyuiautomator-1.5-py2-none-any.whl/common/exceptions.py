# coding=utf-8
"""
Created on 2015年11月5日

@author: thomas.ning

"""

"""
Exceptions that may happen in all the driver code.

"""

class DriverException(Exception):
    
    """
    Base driver exception.
    """
    pass

        
class NoSuchElementException(DriverException):
    """
    Thrown when element could not be found.

    If you encounter this exception, you may want to check the following:
        * Check your selector used in your find_by...
        * Element may not yet be on the screen at the time of the find operation,
        (webpage is still loading) see selenium.webdriver.support.wait.WebDriverWait() 
        for how to write a wait wrapper to wait for an element to appear.
    """
    pass


class InvalidSelectorException(NoSuchElementException):
    """
    Thrown when the selector which is used to find an element does not return
    a WebElement. Currently this only happens when the selector is an xpath
    expression and it is either syntactically invalid (i.e. it is not a
    xpath expression) or the expression does not select WebElements
    (e.g. "count(//input)").
    """
    pass


class TimeoutException(DriverException):
    """
    Thrown when a command does not complete in enough time.
    """
    pass


class SocketConnectException(DriverException):
    """
    Thrown when socket does not connect
    """

    pass


class AdbException(DriverException):
    '''
    Thrown when error occured in ADB.
    '''
    pass

class DeviceNotFound(AdbException):
    '''
    Thrown when error occured in ADB.
    '''
    pass


class UiautomatorException(DriverException):
    '''
    Throm when uiautumator return fault value.
    '''
    pass

class RemoteServiceException(DriverException):
    '''
    Throm when resource server return fault value.
    '''
    pass

class FileNotFound(DriverException):
    '''
    Throm when file not exist.
    '''
    pass