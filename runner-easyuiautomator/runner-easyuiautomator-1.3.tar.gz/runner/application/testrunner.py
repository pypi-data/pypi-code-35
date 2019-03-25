# coding=utf-8
"""
Created on 2015年11月23日

@author: thomas.ning
"""
import time,traceback
from unittest import TestResult
from runner.common.log import Logger
from .resultHandler import ResultHandler
from .builder import TestBuilder
from .testcontroller import TestController
from runner.common.exceptions import RunnerException
logger = Logger.getLogger()

class TestRunner(object):
    """
    Class for loading test runner
    """

    @staticmethod
    def getRunner(options=None):
        if not options is None:
            return PYTestRunner(options)
        else:
            return None


def collectResult(func):
    def wrap(*args, **argkw):
        func(*args, **argkw)
        if True:
            content = (func.__name__, args)
            if TestBuilder.getBuilder().getBuildOption() is None:
                return      
            ResultHandler.handle(info=content)
            if TestController.getInstance().getStopFlag():
                raise RunnerException('device not found')            
        return func

    return wrap


class _TestResult(TestResult):
    separator1 = '=' * 70
    separator2 = '-' * 70
    _passNum = 0
    
    def __init__(self, stream=None, descriptions=None, verbosity=None):
        TestResult.__init__(self)
        
    @collectResult
    def startTest(self, test):
        TestResult.startTest(self, test)
        logger.setLogOn()
        TestController.getInstance().setTestcaseOrder(test)
        # need to add write and writln method for terminal output
        logger.info("start test".center(20,"*"))
        logger.info(self.getDescription(test))
        logger.info("START: %s" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))+" || Current Cycle:" + str(TestController.getInstance().getCurrentCycle()) +" || Current Order:"+ str(TestController.getInstance().getCurrentcaseOrder()))

    @collectResult
    def addSuccess(self, test):
        TestResult.addSuccess(self, test)
        logger.info("PASS".center(20,"*"))
        logger.setLogOff()
        self._passNum += 1
        
    @collectResult
    def addFailure(self, test, err):
        TestResult.addFailure(self, test, err)
        logger.setLogOff()
        logger.error("FAIL".center(20,"*"))
        logger.error("error: %s\ncause: %s"%(err[0].__name__,err[1].message))
        logger.error("FAIL".center(20,"*"))
       
    @collectResult
    def addError(self, test, err):
        TestResult.addError(self, test, err)
        logger.setLogOff()
        logger.error("ERROR".center(20,"*"))
        logger.error(traceback.format_exc(5))                                              
        logger.error("ERROR".center(20,"*"))
       
    @collectResult
    def stopTest(self, test):
        TestResult.stopTest(self, test)
        logger.setLogOff()
        logger.info("Stop Test".center(20,"*"))
        logger.info(self.getDescription(test))
        logger.info("STOP: %s" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))+" || Current Cycle:" + str(TestController.getInstance().getCurrentCycle()) +" || Current Order:"+ str(TestController.getInstance().getCurrentcaseOrder()))
        
    def getDescription(self, test):
        return test.shortDescription() or str(test)

    def printErrors(self):
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        for test, err in errors:
            logger.debug(self.separator1)
            logger.debug("%s: %s" % (flavour, self.getDescription(test)))
            logger.debug(self.separator2)
            logger.debug("%s" % err)


class PYTestRunner(object):
    """
    Implement of text test runner
    """

    def __init__(self, context=None):
        logger = Logger.getLogger()
        self.context = context

    def _makeResult(self):
        return _TestResult()

    def run(self, test):
        logger.debug('run the testsuite!!')
        # result output terminal
        result = self._makeResult()
        # test start time
        startTime = time.time()
        # if test is instance of TestSuite:for t in test: i(result)
        # run test/testsuite
        test(result)  
        # test stop time
        stopTime = time.time()
        # test duration
        timeTaken = stopTime - startTime
        # if not self.verbosity:
        # print all erros during test
#         result.printErrors()
        # ----------------
        logger.debug(result.separator2)
        # total case number has been ran
        run = result.testsRun
        logger.debug("Total ran %d test%s in %.3fs" % (run, run != 1 and "s" or "", timeTaken))
        # space line output
        # If test include failures or errors . special notification for failure and error
        if not result.wasSuccessful():
            logger.debug("FAILED (")             
            logger.debug("failed=%d" % (run - result._passNum))
            logger.debug(")")
        else:
            logger.debug("OK")
        return result
