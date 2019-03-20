# coding=utf-8

import threading, time, copy
import traceback, json, collections
from auto_runner.identifykey import IdentifyKey
from auto_runner.log import Logger

class ResultCollect(object):
    """
    collect result,and make local html
    """
    _instance = None
    _mutex = threading.Lock()

    def __init__(self):
        self.logger = Logger.getLogger()
        self.module = collections.OrderedDict()  # store single module key value
        self.casesNumber = 0
        self.tid = 0
        self.totalfailed = 0
        self.succnum = 0  # single case
        self.failurenum = 0  # single case
        self.errornum = 0  # single case
        self.casename = None  # caseid name
        self.result = []  # store all module
        self.tests = []  # store all test detail
        self.testcase = {}  # store single case key value
        self.acterror = 0 #anr(1) and tombstone(2) crush error(3)

    @staticmethod
    def getInstance():
        if (ResultCollect._instance == None):
            ResultCollect._mutex.acquire()
            if (ResultCollect._instance == None):
                ResultCollect._instance = ResultCollect()
            ResultCollect._mutex.release()
        return ResultCollect._instance

    def reset(self):
        '''重置当前变量集合 '''
        self.casesNumber = 1
        self.tid = 0
        self.totalfailed = 0
        self.succnum = 0  # single case
        self.failurenum = 0  # single case
        self.errornum = 0  # single case
        self.casename = None  # caseid name
        self.result = []  # store all module
        self.module.clear()  # store single module key value
        self.tests = []  # store all test detail
        self.testcase = {}  # store single case key value

    def addInfo(self, info, image=""):
        if info:
            if info[0] == 'startTest':
                self.testcase.clear()
                self.testcase['cycle'] = 0                
                self.testcase['module'] = type(info[1][1]).__name__
                self.testcase['casename'] = info[1][1]._testMethodName
                if self.casename != self.testcase['casename']:
                    self.tests = []
                    self.casesNumber += 1
                    self.tid = 1
                    self.succnum = 0
                    self.failurenum = 0
                    self.errornum = 0
                    self.casename = self.testcase['casename']
                else:
                    self.tid += 1
                self.testcase['order'] = self.tid
                self.testcase['casenum'] = self.casesNumber
                self.testcase['result'] = None
                self.testcase['casedesc'] = info[1][1]._testMethodDoc.strip() if info[1][1]._testMethodDoc else ""
                self.testcase['starttime'] = int(time.time())
            else:
                loginfopath = info[1][1].store.getWorkDir() 
                if info[0] == 'addSuccess':
                    self.succnum += 1
                    self.testcase['result'] = 'pass'
                    self.testcase['endtime'] = int(time.time())
                    self.testcase['traceback'] = ""
                    self.testcase['screenshot'] = image
                    self.testcase['logpath'] = loginfopath                    
                
                elif info[0] == 'addFailure' or info[0] == 'addError':
                    self.testcase['result'] = 'failed'
                    try:                                                   
                        traceback_message = reduce(\
                            lambda x,y:x+y,\
                            traceback.format_exception(info[1][2][0],info[1][2][1],info[1][2][2], 5))
                        self.testcase['traceback'] = str(time.strftime('[%Y.%m.%d-%H.%M.%S] ', time.localtime(time.time()))) + traceback_message
                    except:
                        self.testcase['traceback'] = ''
                    self.testcase['endtime'] = int(time.time())                    
                    self.testcase['screenshot'] = image
                    self.testcase['logpath'] = loginfopath
   
                elif info[0]=='stopTest': 
                    if self.testcase['result'] != 'pass':
                        self.failurenum += 1
                        self.totalfailed += 1
                    self.testcase['logmessage'] = self.logger.getMsg()
                    self.tests.append(copy.deepcopy(self.testcase))
                    self.module[self.casesNumber] = {
                        'starttime': '',
                        'endtime': '',
                        'pass': self.succnum,
                        'failure': self.failurenum,
                        'tests': copy.deepcopy(self.tests)
                    }
                    Upload.formatInfo(self.logger, self.testcase)
     
class Upload(object):
    
    __Result = {'pass':0,'failed':1,'error':2}
    
    @staticmethod
    def formatInfo(logger, testcase):
        case_result = {
           'module': testcase['module'],
           'case_name': testcase['casename'],
           'case_desc': testcase['casedesc'],
           'cycle': testcase['cycle'],
           'test_cycle': testcase['order'],
           'case_num': testcase['casenum'],
           'total_times': 1,
           'result': Upload.__Result[testcase['result']],
           'beg_time': testcase['starttime'],
           'end_time': testcase['endtime'],
           'image': testcase['screenshot'],
           'trace_back': testcase['traceback'],
           'logpath': testcase['logpath'],
           'run_log': testcase['logmessage'],
        }
        logger.debug(IdentifyKey.data_prefix + json.dumps({"word":"case_result","params":case_result},ensure_ascii=False))