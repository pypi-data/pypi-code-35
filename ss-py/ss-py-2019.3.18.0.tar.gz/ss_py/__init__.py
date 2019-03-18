from aigpy import cmdHelper
from ss_py.sstool import SSTool

def main(argv=None):
    tool = SSTool()
    status = '未启动'
    if tool.isSSOpen():
        status = '已启动'
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
    print('[状态] ', end='')
    if tool.isSSOpen():
        cmdHelper.myprint('已启动\n',cmdHelper.TextColor.Green)
    else:
        cmdHelper.myprint('停止\n',cmdHelper.TextColor.Red)
    print('======================')
    while True:
        choice = int(cmdHelper.myinput('请输入数字:'))
        if choice == 1:
            status = '未启动'
            if tool.startSS():
                status = '已启动'
            print(' 当前状态: ' + status)
        elif choice == 2:
            tool.stopSS()
            status = '未启动'
            if tool.isSSOpen():
                status = '已启动'
            print(' 当前状态: ' + status)
        elif choice == 3:
            port = cmdHelper.myinput('端口:')
            pwd = cmdHelper.myinput('密码:')
            tool.addDelPort(True, port, pwd)
        elif choice == 4:
            port = cmdHelper.myinput('端口:')
            tool.addDelPort(False, port, None)
        elif choice == 5:
            ports = tool.getPorts()
            for key,value in ports.items():
                print('{key}:{value}'.format(key = key, value = value))

__all__ = ['main']
