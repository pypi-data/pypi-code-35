# coding=utf-8

"""
Created on 2015年11月30日

@author: thomas.ning
"""
import os
from runner.common import utils

class Report(object):
    """
    loads local report model to make html
    """

    def __init__(self):
        self.masterReport = None
        self.suiteReport = None
        self.suiteDetail = None
        self.testReport = None
        self.testDetail = None

    def getSuiteContents(self, contents):
        self.suiteReport = SuiteTemplate("runner")
        return self.suiteReport.getContents(contents)

    def getSuiteDetailContents(self,key, casename, total, succ, failure, starttime, endtime):
        self.suiteDetail = SuiteDetailTemplate("runner")
        return self.suiteDetail.getContents(key, casename, total, succ, failure, starttime, endtime)

    def getTestContents(self,key, casename, contents):
        self.testReport = TestTemplate("runner")
        return self.testReport.getContents(key,casename, contents)

    def getTestDetailContents(self,key, casename, order, result, starttime, endtime, runninglog, traceback, screenshot,
                              logpath,acterror):
        self.testDetail = TestDetailTemplate("runner")
        return self.testDetail.getContents(key, casename, order, result, starttime, endtime, runninglog, traceback,
                                           screenshot,
                                           logpath,acterror)

    def getMasterContents(self, custom, project, version, imei, starttime, endtime, total, runned, failed,
                          content):
        self.masterReport = MasterTemplate("runner")
        return self.masterReport.getContents(custom, project, version, imei, starttime, endtime, total,
                                             runned, failed, content)

    def toHtml(self):
        pass


class BaseReportHelper(object):
    TEMPLATE_PATH = 'resources/'

    def __init__(self, mastername, templatename):
        self.mastername = mastername
        self.templatename = templatename

    def getTemplateContents(self):
        template_path = os.path.join(os.path.dirname(__file__), BaseReportHelper.TEMPLATE_PATH)
        f = open(template_path + self.templatename)
        try:
            all_text = f.read()
        finally:
            f.close()
        return all_text

class MasterTemplate(BaseReportHelper):
    def __init__(self, mastername, templatename="AutoRunnerTemplate.html"):
        super(MasterTemplate, self).__init__(mastername, templatename)

    def getContents(self, custom, project, version, imei, starttime, endtime, total, runned, failure,
                    content):
        contents = self.getTemplateContents()
        contents = contents.replace("${customer}", str(custom))
        contents = contents.replace("${project}", str(project))
        contents = contents.replace("${version}", str(version))
        contents = contents.replace("${imei}", str(imei))
        contents = contents.replace("${starttime}", utils.format_time(starttime))
        contents = contents.replace("${endtime}", utils.format_time(endtime))
        contents = contents.replace("${costtime}", utils.format_time_diff(endtime - starttime))
        contents = contents.replace("${total}", str(total))
        contents = contents.replace("${runned}", str(runned))
        contents = contents.replace("${pass}", str(runned - failure))
        contents = contents.replace("${failure}", str(failure))
#         contents = contents.replace("${error}", str(error))
        contents = contents.replace("${rate}", str(round(((runned - failure) / float(total)) * 100, 2)))
        contents = contents.replace("${result}", "Pass" if round((runned - failure) / float(total) * 100,
                                                                 2) >= 90.00 else "Fail")
        # contents = contents.replace("${result}", "Pass" if (failure + error) == 0 else "Fail")
        contents = contents.replace("${content}", content)
        return contents


class SuiteTemplate(BaseReportHelper):
    def __init__(self, mastername, templatename="SuiteTemplate.html"):
        super(SuiteTemplate, self).__init__(mastername, templatename)

    def getContents(self, content):
        contents = self.getTemplateContents()
        contents = contents.replace("${content}", content)
        return contents


class SuiteDetailTemplate(BaseReportHelper):
    def __init__(self, mastername, templatename="SuiteDetailTemplate.html"):
        super(SuiteDetailTemplate, self).__init__(mastername, templatename)

    def getContents(self,key, casename, total, succ, failure, starttime, endtime):
        contents = self.getTemplateContents()
        contents = contents.replace("${key}",str(key)+casename)
        contents = contents.replace("${casename}", casename)
        contents = contents.replace("${total}", str(total))
        contents = contents.replace("${pass}", str(succ))
        contents = contents.replace("${failure}", str(failure))
#         contents = contents.replace("${error}", str(error))
        contents = contents.replace("${rate}", str(round((succ / float(total)) * 100, 2)))
        contents = contents.replace("${starttime}", utils.format_time(starttime))
        contents = contents.replace("${endtime}", utils.format_time(endtime))
        contents = contents.replace("${costtime}", utils.format_time_diff(endtime - starttime))
        return contents


class TestTemplate(BaseReportHelper):
    def __init__(self, mastername, templatename='TestTemplate.html'):
        super(TestTemplate, self).__init__(mastername, templatename)

    def getContents(self, key, casename, content):
        contents = self.getTemplateContents()
        contents = contents.replace("${casename}", str(key)+casename)
        contents = contents.replace("${content}", content)
        return contents


class TestDetailTemplate(BaseReportHelper):
    def __init__(self, mastername, templatename='TestDetailTemplate.html'):
        super(TestDetailTemplate, self).__init__(mastername, templatename)

    def getContents(self,key, casename, order_id, result, starttime, endtime, runninglog, traceback, screenshot, logpath,acterror):
        contents = self.getTemplateContents()
        contents = contents.replace("${casename2order}", str(key) + casename + "_" + str(order_id))
        contents = contents.replace("${order}", str(order_id))
        contents = contents.replace("${result}", result)
        contents = contents.replace("${runninglog}", runninglog)
        contents = contents.replace("${starttime}", utils.format_time(starttime))
        contents = contents.replace("${endtime}", utils.format_time(endtime))
        contents = contents.replace("${costtime}", utils.format_time_diff(endtime - starttime))
        if traceback != "":
            contents = contents.replace("${traceback}", traceback.strip().replace("\r\n", ""))
        else:
            contents = contents.replace("${traceback}", "")
        if screenshot != "":
            contents = contents.replace("${screenshot}", "<img class=\"picture\" src=\"" + screenshot + "\"/>")
        else:
            contents = contents.replace("${screenshot}", "")

        if logpath != "":
            contents = contents.replace("${logpath}", "<a href=" + str(logpath) + "\\>" + "logsPath" + "</a>")
        else:
            contents = contents.replace("${logpath}", "")
        contents = contents.replace("${acterror}", str(acterror))
        return contents