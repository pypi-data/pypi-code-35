import os
from aigpy import cmdHelper
from aigpy import convertHelper
from ss_py.tool import SSTool
from ss_py.tool import CountTool
from ss_py.tool import HttpTool


def printMenu(tool):
    print('======================')
    cmdHelper.myprint('0.  ',cmdHelper.TextColor.Green)
    print('退出')
    cmdHelper.myprint('1.  ',cmdHelper.TextColor.Green)
    print('启动')
    cmdHelper.myprint('2.  ',cmdHelper.TextColor.Green)
    print('停止')
    cmdHelper.myprint('3.  ',cmdHelper.TextColor.Green)
    print('启动http服务')
    print('-------------')
    cmdHelper.myprint('4.  ',cmdHelper.TextColor.Green)
    print('添加/修改用户')
    cmdHelper.myprint('5.  ',cmdHelper.TextColor.Green)
    print('删除用户')
    cmdHelper.myprint('6.  ',cmdHelper.TextColor.Green)
    print('显示用户')
    cmdHelper.myprint('7.  ',cmdHelper.TextColor.Green)
    print('重置流量')
    print('')
    tool.printStatus()
    print('======================')

def start(tool):
    # 尝试启动，如果启动失败则查看是否后台有其他的ss服务在运行
    if tool.startSS() == False:
        pids = tool.getAnotherSSPID()
        if len(pids) > 0:
            cmdHelper.myprint('关闭其他ss服务(y/n):',cmdHelper.TextColor.Yellow)
            choice = cmdHelper.myinput('')
            # 再次尝试启动
            if choice == 'y' or choice == 'Y':
                tool.killAnotherSSPID()
                tool.startSS()
    tool.printStatus()

def add(tool):
    port  = cmdHelper.myinputInt('端口:', -1)
    pwd   = cmdHelper.myinput('密码:')
    limit = cmdHelper.myinputInt('流量(G):', 1)
    limit = convertHelper.convertStorageUnit(limit, 'gb', 'byte')
    if tool.addDelPort(True, port, pwd, limit):
        cmdHelper.myprint('[提示]',cmdHelper.TextColor.Green)
        print('添加端口成功!')
    else:
        cmdHelper.myprint('[提示]',cmdHelper.TextColor.Red)
        print('添加端口失败!')

def resetUsed(tool):
    while True:
        cmdHelper.myprint('端口(0表示全部,回车返回):',cmdHelper.TextColor.Yellow)
        choice = cmdHelper.myinputInt('',99999)
        if choice == 99999:
            return
        if choice != 0 and not tool.havePort(choice):
            cmdHelper.myprint('[错误]',cmdHelper.TextColor.Red)
            print('端口不存在!')
            continue
        tool.resetPortUser(choice)
        break

def openHttp(tool):
    while True:
        path = cmdHelper.myinput('网站根目录:', -1)
        if not os.path.isdir(path):
            cmdHelper.myprint('[错误]',cmdHelper.TextColor.Red)
            print('路径不存在!')
            continue
        tool.setHttpConfig(path)
        tool.startHttp()
        return


def main(argv=None):
    tool = SSTool()
    if tool.isCountProcess():
        tool = CountTool()
        tool.start()
        return
    if tool.isHttpProcess():
        tool = HttpTool()
        tool.start()
        return

    printMenu(tool)
    while True:
        cmdHelper.myprint('输入选择(3显示菜单):',cmdHelper.TextColor.Yellow)
        choice = cmdHelper.myinputInt('',9999)
        if choice == 0:
            return
        elif choice == 1:
            start(tool)
        elif choice == 2:
            tool.stopSS()
            tool.printStatus()
        elif choice == 3:
            openHttp(tool)
        elif choice == 4:
            add(tool)
        elif choice == 5:
            port = cmdHelper.myinputInt('端口:', -1)
            tool.addDelPort(False, port, None, None)
        elif choice == 6:
            tool.printPorts()
        elif choice == 7:
            resetUsed(tool)
        else:
            printMenu(tool)

__all__ = ['main']
