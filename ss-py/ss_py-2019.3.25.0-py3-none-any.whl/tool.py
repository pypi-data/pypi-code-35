import os
import sys
import time
import subprocess

from aigpy import cmdHelper
from aigpy import fileHelper
from aigpy import convertHelper
from aigpy import systemHelper

from ss_py.ssprofile   import SSProfile
from ss_py.flowprofile import FlowProfile
from ss_py.iptable     import IPTable

PATH_BASE          = '/etc/ss_py/'
FILE_PROFILE       = PATH_BASE + 'profile.json'
FILE_SSERVER_PID   = PATH_BASE + 'ssserverpid.txt'
FILE_COUNT_PID     = PATH_BASE + 'countpid.txt'
FILE_FLOW          = PATH_BASE + 'flow.json'
FLAG_COUNT_PROCESS = 'FLAG_COUNT'

class SSTool(object):
    def __init__(self):
        self.profile = SSProfile(FILE_PROFILE)
        self.flow    = FlowProfile(FILE_FLOW)
   

    def _checkPortRanges(self, port):
        port = int(port)
        if port > 0 and port <= 65536:
            return True
        return False

    def __getPidByFile(self, isCountFile = False):
        if isCountFile:
            pid = fileHelper.getFileContent(FILE_COUNT_PID)
        else:
            pid = fileHelper.getFileContent(FILE_SSERVER_PID)
        if pid == "":
            return -1
        pid.strip()
        pid.strip('\n')
        pid = int(pid)
        return pid

    def __startCount(self):
        pass
        # os.system('ss-py ' + FLAG_COUNT_PROCESS + ' & echo $! > '+FILE_COUNT_PID)
    
    def __stopCount(self):
        # pid = self.__getPidByFile(True)
        # if pid == -1:
        #     return False
        # array = systemHelper.getProcessID('ss-py')
        # if pid in array:
        #     systemHelper.killProcess(pid)
        #     os.remove(FILE_COUNT_PID)
        #     table = IPTable()
        #     table.initChain()
        #     table.delChain()
        #     return True
        return False

    def startSS(self):
        if self.isSSOpen():
            return True
        cmd = 'ssserver -qq -c ' + FILE_PROFILE + ' 2>/dev/null >/dev/null & echo $! > ' + FILE_SSERVER_PID
        res = subprocess.call(cmd, shell=True)
        # 等待一下,要给上面的进程一段时间判断启动是否正常
        time.sleep(0.5)
        if self.isSSOpen() == False:
            return False
        self.__startCount()
        return True

    def stopSS(self):
        pid = self.__getPidByFile()
        if pid == -1:
            return False
        array = systemHelper.getProcessID('`basename ssserver`')
        if pid in array:
            systemHelper.killProcess(pid)
            os.remove(FILE_SSERVER_PID)
            self.__stopCount()
            return True
        return False
    
    def isSSOpen(self):
        pid = self.__getPidByFile()
        if pid == -1:
            return False
        array = systemHelper.getProcessID('`basename ssserver`')
        if pid in array:
            return True
        return False

    def getAnotherSSPID(self):
        array = systemHelper.getProcessID('`basename ssserver`')
        if len(array) == 0:
            return []
        pid = self.__getPidByFile()
        if pid == -1:
            return array
        if str(pid) in array:
            array.remove(str(pid))
        return array
    
    def killAnotherSSPID(self):
        array = self.getAnotherSSPID()
        for item in array:
            systemHelper.killProcess(item)

    def addDelPort(self, isAdd, port, pwd, limit):
        if self._checkPortRanges(port) == False:
            return False
        if isAdd:
            self.profile.addPort(port, pwd)
            self.flow.addPort(port, limit)
        else:
            self.profile.delPort(port)
            self.flow.delPort(port)

        self.profile.save(FILE_PROFILE)
        self.flow.save(FILE_FLOW)
        if self.isSSOpen():
            self.stopSS()
            self.startSS()
    
    def printPorts(self):
        if len(self.profile.ports) <= 0:
            cmdHelper.myprint('[错误] ',cmdHelper.TextColor.Red)
            print('未设置端口')
            return

        self.flow = FlowProfile(FILE_FLOW)
        cols =['Port','Password','Limit','Remaining']
        rows = []
        for port, pwd in self.profile.ports.items():
            limit = self.flow.profile[port]['limit']
            used  = self.flow.profile[port]['used']
            rema  = limit - used
            if rema < 0:
                rema = 0
            limit = convertHelper.convertStorageUnitToString(limit, 'byte')
            rema  = convertHelper.convertStorageUnitToString(rema, 'byte')
            rows.append([port, pwd, limit, rema])
        cmdHelper.showTable(cols, rows, cmdHelper.TextColor.Red, cmdHelper.TextColor.Green)
           
    def printStatus(self):
        print('[状态] ', end='')
        if self.isSSOpen():
            cmdHelper.myprint('已启动\n',cmdHelper.TextColor.Green)
        else:
            cmdHelper.myprint('停止\n',cmdHelper.TextColor.Red)

    def isCountProcess(self):
        return cmdHelper.findInArgv(FLAG_COUNT_PROCESS) != None
    


class CountTool(object):
    def __init__(self):
        self.flow    = FlowProfile(FILE_FLOW)
        self.iptable = IPTable()
        self.iptable.initChain()
        for port in self.flow.profile:
            self.iptable.addPortRule(int(port))
        
    def start(self):
        tmpNum = 0
        timeOfCount = 0.5
        while True:
            # 计算增加的流量,更新增量到self.flow.profile中
            increase = self.iptable.getPortsFlowIncrease()
            for port in increase:
                if port in self.flow.profile:
                    self.flow.profile[port]['used'] = increase[port]
            # 休眠
            time.sleep(timeOfCount)
            # 重载流量文件,判断SSTool有没有修改流量文件
            # 检查流量,查看是否封闭端口或启动端口
            tmpNum = tmpNum + 1
            if tmpNum*timeOfCount >= 10:
                tmpNum = 0
                self.flow.reload(FILE_FLOW)
                self.flow.save(FILE_FLOW)
                for port in self.flow.profile:
                    rema = self.flow.profile[port]['limit'] - self.flow.profile[port]['used']
                    if rema > 0:
                        self.iptable.addPortRule(port)
                        self.iptable.deletePortRule(port, True)
                    else:
                        self.iptable.addPortRule(port,True)
                        self.iptable.deletePortRule(port, False)