from aigpy import cmdHelper
from ss_py.sstool import SSTool

def main(argv=None):
    tool = SSTool()
    print('======================')
    cmdHelper.myprint('1.  ',cmdHelper.TextColor.Green)
    print('启动')
    cmdHelper.myprint('2.  ',cmdHelper.TextColor.Green)
    print('停止')
    print('-------------')
    cmdHelper.myprint('3.  ',cmdHelper.TextColor.Green)
    print('添加用户')
    cmdHelper.myprint('4.  ',cmdHelper.TextColor.Green)
    print('删除用户')
    cmdHelper.myprint('5.  ',cmdHelper.TextColor.Green)
    print('显示用户')
    print('')
    tool.printStatus()
    print('======================')
    while True:
        cmdHelper.myprint('输入选择:',cmdHelper.TextColor.Yellow)
        choice = cmdHelper.myinputInt('',9999)
        if choice == 1:
            tool.startSS()
            tool.printStatus()
        elif choice == 2:
            tool.stopSS()
            tool.printStatus()
        elif choice == 3:
            port = cmdHelper.myinput('端口:')
            pwd  = cmdHelper.myinput('密码:')
            tool.addDelPort(True, port, pwd)
        elif choice == 4:
            port = cmdHelper.myinput('端口:')
            tool.addDelPort(False, port, None)
        elif choice == 5:
            tool.printPorts()

__all__ = ['main']
