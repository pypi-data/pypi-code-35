# coding=utf-8
"""
Created on 2016年1月3日

@author: thomas.ning
"""
import threading, os, time, copy, re
import traceback, json, collections
from runner.common.identifykey import IdentifyKey
from runner.common.log import Logger
from runner.common.fileUtil import FileUtil
from .builder import TestBuilder
from .report import Report
from .testcontroller import TestController


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
                self.testcase['cycle'] = TestController.getInstance().getCurrentCycle()                
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
                    self.testcase['acterror'] = self.acterr_check(self.testcase['logpath'])
                    self.tests.append(copy.deepcopy(self.testcase))
                    self.module[self.casesNumber] = {
                        'starttime': '',
                        'endtime': '',
                        'pass': self.succnum,
                        'failure': self.failurenum,
                        'tests': copy.deepcopy(self.tests)
                    }
                    Upload.formatInfo(self.logger, self.testcase)
                    LocalHtml.getInstance().makeHtml(self.module, info[1][0].testsRun, self.totalfailed) 
                    
    def acterr_check(self, path):
        '''检查anr crash tomestone'''
        errlist = "has "
        if os.path.exists(path+'/anr'):
            if os.listdir(path+'/anr'):
                errlist = errlist + 'anr '
        if os.path.exists(path+'/tombstone'):
            if os.listdir(path+'/tombstone'):
                errlist = errlist + 'tombstone '
        if os.path.exists(path+'/app_crash'):
            if os.listdir(path+'/app_crash'):
                errlist = errlist + 'app_crash '  
        if errlist == "has ":
            return 'no anr or crush or tombstone '         
        return errlist + 'error'
     
class Upload(object):
    
    __Result = {'pass':0,'failed':1,'error':2}
    
    @staticmethod
    def formatInfo(logger, testcase):
        case_result = {'task_id': TestBuilder.getBuilder().getTaskId(),
                       'module': testcase['module'],
                       'case_name': testcase['casename'],
                       'case_desc': testcase['casedesc'],
                       'cycle': testcase['cycle'],
                       'test_cycle': testcase['order'],
                       'case_num': testcase['casenum'],
                       'total_times': TestBuilder.getBuilder().getTestNumByName(testcase['casename']),
                       'result': Upload.__Result[testcase['result']],
                       'beg_time': testcase['starttime'],
                       'end_time': testcase['endtime'],
                       'image': testcase['screenshot'],
                       'trace_back': testcase['traceback'],
                       'logpath': testcase['logpath'],
                       'run_log': testcase['logmessage'],
                       'acterror': testcase['acterror']
                       }
        logger.debug(IdentifyKey._casereuslt_prefix + json.dumps(case_result,ensure_ascii=False))
        csv_file_name = os.path.join(TestBuilder.getBuilder().getWorkspace(),'FullData')
        _data = _deal_data(case_result,testcase['result'])
        
        if not os.path.exists(csv_file_name + ".txt"):
            FileUtil.writeData(csv_file_name,'task_id@module@case_name@case_desc@cycle@test_cycle@case_num@total_times@result@beg_time@end_time@image@trace_back@logpath@run_log@acterror\n')
        FileUtil.writeData(csv_file_name,_data)

def _deal_data(case_result,result):        
    data = copy.deepcopy(case_result['trace_back'])
    trace_back = str(re.sub('\\s+', "  ", data))
    data2 = copy.deepcopy(case_result['logpath'])
    logpath = str(re.sub('\\s+', "  ", data2))
    data3 = copy.deepcopy(case_result['run_log'])
    run_log = str(re.sub('\\s+', "  ", data3))
    data4 = copy.deepcopy(case_result['acterror'])
    acterror = str(re.sub('\\s+', "  ", data4))
    t1 = time.localtime(case_result['beg_time'])
    beg_time = str(time.strftime('%Y-%m-%d %H:%M:%S',t1))
    t2 = time.localtime(case_result['beg_time'])
    end_time = str(time.strftime('%Y-%m-%d %H:%M:%S',t2))
    dataStr = ""
    dataStr= dataStr + str(case_result['task_id'])+'@'
    dataStr= dataStr + str(case_result['module'])+'@'
    dataStr= dataStr + str(case_result['case_name'])+'@'
    dataStr= dataStr + str(case_result['case_desc'])+'@'
    dataStr= dataStr + str(case_result['cycle'])+'@'
    dataStr= dataStr + str(case_result['test_cycle'])+'@'
    dataStr= dataStr + str(case_result['case_num'])+'@'
    dataStr= dataStr + str(case_result['total_times'])+'@'
    dataStr= dataStr + str(result)+'@'
    dataStr= dataStr + beg_time+'@'
    dataStr= dataStr + end_time+'@'
    dataStr= dataStr + trace_back+'@'
    dataStr= dataStr + str(case_result['image'])+'@'
    dataStr= dataStr + logpath+'@'
    dataStr= dataStr + run_log+'@'
    dataStr= dataStr + acterror+'@'
    return dataStr


            
class LocalHtml(object):
    '''收集结果数据，并生成本地html报告'''
    _instance = None
    _mutex = threading.Lock()
    
    def __init__(self):
        self.report = Report()
        self.project = TestBuilder.getBuilder().getProjectConfig()
    
    @staticmethod
    def getInstance():
        if (LocalHtml._instance == None):
            LocalHtml._mutex.acquire()
            if (LocalHtml._instance == None):
                LocalHtml._instance = LocalHtml()
            LocalHtml._mutex.release()
        return LocalHtml._instance
        
    def makeHtml(self, module, runned, totalfailed):
        result = ""
        stop_time = ""
        custom = self.project.get('custom')
        project = self.project.get('project')
        version = self.project.get('version')
        imei = self.project.get('imei')

        for key in module.keys():  # case modules
            testdetail = ""
            starttime = ""
            endtime = ""
            currentTestCase = module[key]['tests'][0]['casename']
            for test in module[key]['tests']:
                
                if starttime == "":
                    starttime = test['starttime']
                endtime = test['endtime']
                stop_time = endtime
                logpath = './all/' + os.path.basename(test['logpath'])
                testdetail += self.report.getTestDetailContents(key,test['casename'], test['order'], test['result'],
                                                                test['starttime'], test['endtime'],
                                                                test['logmessage'], test['traceback'],
                                                                logpath + "/"  + test['screenshot'],
                                                                logpath, test['acterror'])           
            test = self.report.getTestContents(key,currentTestCase, testdetail)
            tmp = self.report.getSuiteDetailContents(key, currentTestCase, TestBuilder.getBuilder().getTestNumByName(currentTestCase),
                                                     module[key]['pass'],
                                                     module[key]['failure'], starttime,
                                                     endtime) + test
            result += tmp
        starttime = TestController.getInstance().getCycleStartTime()
        total = TestBuilder.getBuilder().getTestsNum()
        result = self.report.getMasterContents(custom, project, version, imei, starttime, stop_time,
                                               total, runned, totalfailed,
                                               self.report.getSuiteContents(result))
        html_file_name = os.path.join(TestBuilder.getBuilder().getWorkspace(),
                                      str(TestController.getInstance().getCurrentCycle()))
        with open(html_file_name + ".html", "w") as f:
            f.write(result)
    
