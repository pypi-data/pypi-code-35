# coding=utf-8

import unittest,os,time,json,traceback
from auto_runner.log import Logger
from auto_runner.resultHandler import ResultHandler
from auto_runner.store import Store
from auto_runner.identifykey import IdentifyKey

class TestRunner(object):
    """
    Class for loading test auto_runner
    """

    TEST_Flag = False

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
            ResultHandler.handle(info=content)         
        return func
    return wrap


class _TestResult(unittest.TestResult):
    separator1 = '=' * 70
    separator2 = '-' * 70
    _passNum = 0
    
    def __init__(self, stream=None, descriptions=None, verbosity=None):
        unittest.TestResult.__init__(self)
        self.logger = Logger.getLogger()
        
    @collectResult
    def startTest(self, test):
        unittest.TestResult.startTest(self, test)
        self.logger.debug("startTest".center(50, "*"))
        
    @collectResult
    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        
    @collectResult
    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
       
    @collectResult
    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
       
    @collectResult
    def stopTest(self, test):
        unittest.TestResult.stopTest(self, test)
        
    def getDescription(self, test):
        return test.shortDescription() or str(test)

    def printErrors(self):
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        for test, err in errors:
            self.logger.debug(self.separator1)
            self.logger.debug("%s: %s" % (flavour, self.getDescription(test)))
            self.logger.debug(self.separator2)
            self.logger.debug("%s" % err)


class PYTestRunner(object):
    """
    Implement of text test auto_runner
    """

    def __init__(self, context=None):
        self.logger = Logger.getLogger()
        self.context = context

    def _makeResult(self):
        return _TestResult()

    def run(self, test):
        self.logger.debug('run the testsuite!!')
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
        self.logger.debug(result.separator2)
        # total case number has been ran
        run = result.testsRun
        self.logger.debug("Total ran %d test%s in %.3fs" % (run, run != 1 and "s" or "", timeTaken))
        # space line output
        # If test include failures or errors . special notification for failure and error
        if not result.wasSuccessful():
            self.logger.debug("FAILED (")             
            self.logger.debug("failed=%d" % (run - result._passNum))
            self.logger.debug(")")
        else:
            self.logger.debug("OK")
        return result

def getSuite(case_path):
    testunit = unittest.TestSuite()
    # discover 方法定义
    discover = unittest.defaultTestLoader.discover(case_path, pattern='*.py', top_level_dir=None)
    #discover 方法筛选出来的用例，循环添加到测试套件中
    for test_suite in discover:
        for test_case in test_suite:
            testunit.addTest(test_case)
    return testunit

def setDevice(data):
    serial = data.get('serial') if data.get('serial') else None
    if serial:
        os.environ['ANDROID_SERIAL'] = serial
    else:
        from easyuiautomator.driver.executor.adb import ADB
        adb = ADB(restart=False)
        os.environ['ANDROID_SERIAL'] = adb.serial

def run(data):
    logger = Logger.getLogger()
    try:
        Store.getInstance().init()
        setDevice(data)
        test_suite = getSuite(os.path.abspath(data['case_path']))
        test_runner = TestRunner.getRunner("array_test")
        test_runner.run(test_suite)
    except:
        logger.debug(IdentifyKey.data_prefix + json.dumps({"word":"stop","params":traceback.format_exc()}, ensure_ascii=False))
