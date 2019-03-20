# coding=utf-8

"""
Created on 2015年11月4日

@author: thomas.ning
"""
from easyuiautomator.common.log import Logger
from easyuiautomator.driver.common.keyevent import KeyCode
from easyuiautomator.driver.common.setting_action import SettingAction
from easyuiautomator.common.exceptions import DeviceNotFound
import subprocess,tempfile,base64,os,time,re


class ADB(object):
    """
    adb provides the connection and basic actions for Android Device
    """ 
    
    def __init__(self, serial=None, restart=True, server_host=None, server_port=None):
        self.logger = Logger.getLogger()
        self.server_host = str(server_host if server_host else '127.0.0.1')
        self.server_port = str(server_port if server_port else '5037')
        self.serial = None
        self.restart = restart # after adb command execution failed, Whether to restart
        self.sdk_version = 0
        serial = serial or os.getenv('ANDROID_SERIAL')
        if serial is None:
            self.serial = self.getConnectedDevices()[0]['udid']
            self.logger.debug("bind device on serial " + self.serial)
        else:
            self.serial = serial
        
    def setRestartMode(self,flag):
        '''true:adb server重启，false: adb server不重启'''
        self.restart = flag

    def exec_adb(self, cmd):
        '''
        Execute adb command,if something wrong,adb will restart one time.
        while adb command failed or timeout ,it will break and raise Error.
                        执行ADB命令，如果出错，将会重启ADB服务，如果仍然报错或者超时，命令将会中断并抛出异常
        :Args:
         - cmd - command
        :Usage:
            exec_adb('device')
        :Return:
            error : exec_adb('device')
        '''
        out = self.cmd(cmd).communicate()[0]
        lines = []
        for line in out.strip().splitlines():
            if line.strip() == "":
                continue
            if 'not found' in line and 'system/bin/sh' not in line:
                if self._adbRecovery() is True:
                    return self._exec_adb_retry(cmd)
                else:
                    raise DeviceNotFound("[%s] %s"%(self.serial,line)) 
            lines.append(str.strip(line))
        return lines

    def _exec_adb_retry(self, cmd):
        self.logger.debug("{ %s }Retry Adb Command %s"%(self.serial,cmd))
        out = self.cmd(cmd).communicate()[0]
        lines = []
        for line in out.strip().splitlines():
            if line.strip() == "":
                continue
            if 'not found' in line and 'system/bin/sh' not in line:
                # case错误停止,异常处理
                raise DeviceNotFound("[%s] %s"%(self.serial,line))
            lines.append(str.strip(line))
        return lines

    def _adbRecovery(self):
        ''' Restart adb server three times.重启ADB服务3次'''
        self.logger.debug("adb restart")
        for tmp in range(3):
            self.logger.debug("Restart Adb Server %d" % (tmp + 1))
            if self.restart:
                os.system("adb kill-server")
                time.sleep(2)
                os.system("adb start-server")
            time.sleep(5)
            if tmp == 2:
                status_device = self.adbDevices()
                if status_device == True:
                    return True
                elif status_device == "offline":
                    self.logger.debug("%s device offline" %self.serial)
                    flag = self._pause_device()
                    if flag:
                        return True
                    raise DeviceNotFound("[%s] offline"%self.serial)
                else:
                    raise DeviceNotFound("[%s] not connected device"%self.serial)
            else: 
                if self._getConnectedDevices() == True:
                    return True
    
    def _pause_device(self, timeout=20):
        '''pause device 2 minutes, wait server interrupt adbd, then reconnect''' 
        time_unit = 5
        while time_unit <  timeout:
            time.sleep(5)
            time_unit += 5
            if self.adbDevices() == True:
                return True
        return False
            
    def adbDevices(self):
        out = self.raw_cmd('devices').communicate()[0]
        lines = [str(line).strip() for line in out.strip().splitlines()]
        if 'error' in lines:
            return False
        for line in lines:
            if line != "" \
            and "List of devices" not in line\
            and '* daemon' not in line\
            and 'offline' not in line:
                if self.serial is None:
                    return True
                elif self.serial in line:
                    return True
            if self.serial\
            and self.serial in line\
            and 'offline' in line:
                return "offline"
        return False 
    
    def _getConnectedDevices(self):
        '''by given serial or not given, Judgment connected device '''
        out = self.raw_cmd('devices').communicate()[0]
        lines = [str(line).strip() for line in out.strip().splitlines()]
        if 'error' in lines:
            return False
        for line in lines:
            if line != "" and "List of devices" not in line\
                    and '* daemon' not in line and 'offline' not in line:
                if self.serial is None:
                    return True
                elif self.serial in line:
                    return True
        return False
    
    def getConnectedDevices(self):
        '''Get connected devices and return it'''
        self.logger.debug("Get connect devices")
        lines = self.exec_adb('devices')
        devices = []
        if 'error' in lines:
            self.logger.error(lines)
            if self._adbRecovery() == True:
                lines = self._exec_adb_retry('devices')
                return self._deal_devicelist(lines)
            else:
                raise DeviceNotFound("not connected device")
        else:
            devices = self._deal_devicelist(lines)
            if len(devices) == 0:
                raise DeviceNotFound("not connected device")
        self.logger.debug("device list " + str(devices))
        return devices
    
    def _deal_devicelist(self, lines):
        '''deal adb devices list'''
        devices = []
        for line in lines:
            if line != ""\
            and "List of devices" not in line\
            and '* daemon'not in line and 'offline' not in line:
                line = line.split('\t')
                devices.append({'udid': line[0], 'state': line[1]})
        return devices

    def shell(self, cmd):
        '''
        Execute adb shell command执行ADB SHELL命令
        :Args:
         - cmd -  command
        :Usage:
            shell('dumpsys window')
        '''
        return self.exec_adb('shell ' + cmd)
    
    def cmd(self, args):
        '''adb command, add -s serial by default. return the subprocess.Popen object.'''
        serial = self.serial
        if serial:
            if " " in serial:  # TODO how to include special chars on command line
                serial = "'%s'" % serial
            return self.raw_cmd("-s %s %s" % (serial, args))
        else:
            return self.raw_cmd(args)
        
    def raw_cmd(self, cmd):
        '''adb command. return the subprocess.Popen object.'''
        cmd_line = 'adb ' + cmd
        os.system("adb start-server")
        self.logger.debug("exec {" + cmd_line + "}") 
        return subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        

    def push(self, localPath, remotePath):
        '''
        Put file or folder from PC to cellphone.将文件或者文件夹从计算机放入手机
        :Args:
         - localpath -
         - remotepath -
        :Usage:
            push('D:/screen.txt','/storage/sdcard0/360Download/')
        :Return:
            ['344 KB/s (27845 bytes in 0.079s)']
        :Raise:
            - return - ["cannot stat 'D:/scree': No such file or directory"]
        '''
        cmd = 'push -p "%s" "%s"' % (localPath, remotePath)
        return self.exec_adb(cmd)

    def pull(self, srcFile, targetFile):
        '''
        Put file or folder from cellphone to PC.将文件或者文件夹从手机放入计算机
        :Args:
         - srcFile -
         - targetFile -
        :Usage:
            pull('/storage/sdcard0/360Download/new.txt','D:/')
        :Return:
            ['344 KB/s (27845 bytes in 0.079s)']
        :Raises:
            - return - ["cannot stat 'D:/scree': No such file or directory"]
        '''
        cmd = 'pull -p "%s" "%s"' % (srcFile, targetFile)
        return self.exec_adb(cmd)

    def install(self, apk, arg):
        '''
        Install the app.安装手机应用
        :Args:
         - apk - file.apk
        :Usage:
            install('d:/csdn.apk')
        :Return:
            ['Success']
        :Raises:
            - return - ['Invalid APK file: aaaa.apk'],['Missing APK file'],etc
        '''
        if arg:
            cmd='install ' +arg+ ' "' + apk + '"'
        else:
            cmd='install "' + apk + '"'
        return self.exec_adb(cmd)
    
    def installrt(self, apk):
        '''
        Install the app.安装手机应用
        :Args:
         - apk - file.apk
        :Usage:
            install('d:/csdn.apk')
        :Return:
            ['Success']
        :Raises:
            - return - ['Invalid APK file: aaaa.apk'],['Missing APK file'],etc
        '''
        return self.exec_adb(cmd='install -r -t "' + apk + '"')

    def uninstallApk(self, apk, keep=False):
        '''
        Uninstall the app.卸载手机应用
        :Args:
         - apk - app package
        :Usage:
            uninstallApk('net.csdn.app')
        :Return:
            ['Success']
        :Raises:
            - return - ['Failure [DELETE_FAILED_INTERNAL_ERROR]']
        '''
        self.forceStop(apk)
        if keep == True:
            return self.shell(cmd="pm uninstall -k " + apk) 
        return self.shell(cmd="pm uninstall " + apk)

    def isAppinstalled(self, apk):
        '''
        Whether the app is installed or not.手机应用是否安装
        :Args:
         - apk - app package
        :Usage:
            isAppinstalled('net.csdn.app')
        '''
#         command = '-3' if self.getApiLevel() > 15 else''
#         listpkgcmd = 'pm list packages ' + command + ' ' + apk
        listpkgcmd = 'pm list packages ' + apk
        package = self.shell(listpkgcmd)
        if package:
            if package[0] == 'package:' + apk:
                return True
        return False

    def lock(self):
        '''
        Lock the screen锁屏
        :Usage:
            lock()
        '''
        return self.keyevent(26)

    def unlock(self):
        '''
        Unlock the screen解锁屏
        :Usage:
            unlock()
        '''
        if self.isScreenLocked():
            return self.keyevent(26)

    def isScreenLocked(self):
        '''
        Whether screen is locked or not.是否锁屏
        :Usage:
            isScreenLocked()
        :Return:
            ['Success']
        '''
        cmd = "dumpsys window"
        for line in self.shell(cmd):
            if 'mShowingLockscreen=true' in line or 'mScreenOnFully=false' in line:
                return True
        return False

    def forceStop(self, pkg):
        '''
        Force to exit the app.强制退出手机应用
        :Args:
         - pkg - app package
        :Usage:
            forceStop('net.csdn.app')
        :Return:
            ['Success']
        '''
        cmd = 'am force-stop ' + pkg
        return self.shell(cmd)

    def stopAndClear(self, pkg):
        return self.forceStop(pkg)

    def clear(self, pkg):
        '''
        Clear the app data.清理手机应用数据
        :Args:
         - pkg - app package
        :Usage:
            clear('net.csdn.app')
        :Return:
            ['Success']
        '''
        return self.shell(cmd='pm clear ' + pkg)

    def startActivity(self, pkg):
        '''
        Open the app activities.打开应用活动
        :Args:
         - pkg - App package and activity
        :Usage:
            startActivity(net.csdn.app/net.csdn.app.mainactivity)
        :Return:
            ['Starting: Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] cmp=com.example.uibestpractice/.MainActivity }']
        :Raises:
            'Error' in Returns
        '''
        return self.shell('am start %s' % pkg)

    def getRunningAppInfo(self, package):
        return self.shell(cmd='dumpsys package %s' % package)

    
    def getCurrentApp(self):
        '''
        Get current app activity 获取当前手机应用活动
        :Usage:
            getCurrentApp()
        :Return:
            com.example.uibestpractice/.MainActivity
        '''
        cmd = 'dumpsys window windows'
        for line in self.shell(cmd):
            if 'mCurrentFocus' in line:
                current_info = line[:-1].split(" ")[2]
                if "/" in current_info:
                    return (current_info.split('/')[0],current_info.split('/')[1])
                else:
                    return (current_info.split('/')[0],None)
                    

    def hideKeyboard(self):
        '''
        Hide the keyboard.隐藏手机软键盘
        :Usage:
            hideKeyboard()
        '''
        cmd = 'dumpsys input_method'
        for line in self.shell(cmd):
            if 'mWindowVisible=true mWindowWasVisible=true' in line:
                self.back()
                return self.hideKeyboard()
            elif 'mWindowVisible=false mWindowWasVisible=false' in line:
                return 'keyboard is not visible'
        return 'Unknow Error'

    def shake(self):
        '''Shake cellphone手机震动'''
        pass  # 暂未实现

    def takeScreenshot(self, path=None):
        '''
        Take screen shot and return picture or base64code 截图并获取图片或返回base码
        :Args:
         - path - where you will put picture or base64code in
        :Usage:
            takeScreenshot('/storage/sdcard0/')
        '''
        png = "/data/local/tmp/screenshot.png";
        cmd = " ".join(['/system/bin/rm', png + ';', '/system/bin/screencap -p',
                        png]);
        self.shell('"' + cmd + '"')
        if not path:
            tmpScreenshot = os.path.join(tempfile.gettempdir(), "easyuiautomator.png")
            if os.path.exists(tmpScreenshot):
                os.remove(tmpScreenshot)
            self.pull(png, tmpScreenshot)
            tmp = ""
            for line in open(tmpScreenshot, 'rb').readlines():
                tmp += line
            return base64.b64encode(tmp)
        else:
            self.pull(png, path)

    def uiautoTakeshot(self, path=None):
        png = "/data/local/tmp/screenshot.png";
        tmpScreenshot = os.path.join(tempfile.gettempdir(), "easyuiautomator.png")
        if os.path.exists(tmpScreenshot):
            os.remove(tmpScreenshot)
        if path is None:
            self.pull(png, tmpScreenshot)
        else:
            self.pull(path, tmpScreenshot)
        tmp = ""
        for line in open(tmpScreenshot, 'rb').readlines():
            tmp += line
        return base64.b64encode(tmp)


    def background(self, tms):
        '''
        Back to home idle and return to app activity.返回到HOME界面并随后回到应用界面
        :Args:
         - tms - seconds
        :Usage:
            background(1)
        '''
        cmd = 'dumpsys window windows'
        for line in self.shell(cmd):
            if 'name' in line and '/' in line:
                activity = line.split('name=')[1][:-1]
        self.keyevent(KeyCode.KEYCODE_HOME)
        time.sleep(tms)
        return self.startActivity(activity)

    def reset(self, pkg):
        '''
        Reset app by clear it.清理应用数据重置应用
        :Args:
         - pkg - app package
        :Usage:
            reset('net.csdn.app')
        '''
        self.forceStop(pkg)
        return self.clear(pkg)

    def isExistFile(self, path):
        '''
        Whether file is exist.
                          判断是否文件存在
        :Args:
         - path - filepath
        :Usage:
            isExistFile('storage/sdcard0/')
        '''
        if "." in path and "/" in path:
            file_name = os.path.basename(path)
            dir_name = os.path.dirname(path)
            dirs = self.shell("cd %s ; ls" % dir_name)
            if file_name in dirs:
                return True
            else:
                return False
        else:
            dirs = self.shell("cd %s" % path)
            if dirs == []:
                return True
            else:
                return False
            
    def forward(self, system_port, device_port):
        '''Switch port.转换端口'''
        cmd = "forward tcp:" + str(system_port) + " tcp:" + str(device_port)
        return self.exec_adb(cmd)
    
    def forwardlist(self):
        '''view connect port list'''
        cmd = "forward --list"
        lines = self.exec_adb(cmd)
        return [line.strip().split() for line in lines]

    def forwardAbstractPort(self, system_port, device_port):
        self.exec_adb(cmd="forward tcp:" + system_port + " localabstract:" + device_port)

    def _execNoReturn(self, cmd):
        '''No return execute command.无返回执行命令'''
        os.system(cmd)

    def isDeviceConnected(self):
        devices = self.getConnectedDevices()
        if len(devices) > 0:
            return True
        return False

    def broadcast(self, intent):
        self.shell(cmd="am broadcast -a " + intent)

    def broadcastAirplaneMode(self, on):
        cmd = 'am broadcast -a android.intent.action.AIRPLANE_MODE --ez state '
        + (True if on == 1 else False)
        self.shell(cmd)
    
    def setAirplaneMode(self,on):
        self.shell(cmd= 'settings get global airplane_mode_on ' + on)

    def isAirplaneModeOn(self):
        result = self.shell(cmd='settings get global airplane_mode_on')
        try:
            if int(result[0]) == 1:
                return True
            else:
                return False
        except:
            pass

    def isWifiOn(self):
        result = self.shell(cmd='settings get global wifi_on')
        try:
            if int(result[0]) != 0:
                return True
            else:
                return False
        except:
            pass

    def setWifi(self, on):  # on= 'on'  or  on = 'off'
        cmd = 'am start -n io.appium.settings/.Settings -e wifi ' + on;
        self.shell(cmd)

    def isDataOn(self):
        result = self.shell(cmd='settings get global mobile_data')
        try:
            if int(result[0]) == 0:
                return False
            else:
                return True
        except:
            pass

    def setData(self, on):
        cmd = 'am start -n io.appium.settings/.Settings -e data ' + on
        self.shell(cmd)
    
    def availableIMEs(self):
        cmd = "ime list -s"
        return self.shell(cmd)

    def defaultIME(self):
        return self.shell(cmd='settings get secure default_input_method')

    def enableIME(self, imeId):
        self.shell(cmd='ime enable ' + imeId)

    def disableIME(self, imeId):
        self.shell(cmd='ime disable ' + imeId)

    def setIME(self, imeId):
        self.shell(cmd='ime set ' + imeId)

    def killProcessesByName(self, name):
        pids = self.getPidsByName(name)
        for pid in pids:
            self.killProcessByPid(pid)

    def killProcessByPid(self, pid):
        cmd = "kill -9 " + pid
        self.shell(cmd)

    def getPidsByName(self, name):
        cmd = "ps"
        pids = []
        result = self.shell(cmd)
        for line in result:
            if line.endswith(name):
                pids.append(re.split("\s+", line)[1])
        return pids
   
    def back(self):
        return self.keyevent(KeyCode.KEYCODE_BACK)

    def goToHome(self):
        return self.keyevent(KeyCode.KEYCODE_HOME)
    
    def delFile(self, filepath):
        return self.shell(cmd='rm -rf ' + filepath)

    def mkdir(self, remotePath):
        return self.shell(cmd='mkdir -p ' + remotePath)

    def installRemote(self, remoteApk):
        return self.shell(cmd='pm install -r ' + remoteApk)

    def keyevent(self, keycode):
        cmd = 'input keyevent ' + str(keycode)
        return self.shell(cmd)
    
    def press(self, keycode):
        cmd = 'input keyevent ' + str(keycode)
        return self.shell(cmd)
    
    def longPress(self, keycode):
        cmd = 'input keyevent --longpress ' + str(keycode)
        return self.shell(cmd)

    def getApiLevel(self):  
        sdk_version = 0
        try:
            sdk_version = int(self.shell('getprop ro.build.version.sdk')[0])
        except:
            pass
        return sdk_version

    def get_battery(self):
        for info in self.shell(cmd='dumpsys battery'):
            if info.strip().startswith("level:"):
                return info.replace("level:","").strip()
            
    def isOnline(self):
        '''检查设备是否在线'''
        flag = self.adbDevices()
        if flag == "offline":
            return False
        return flag
    
    def getVersionCode(self,packageName):
        versionCode = ""
        for line in self.shell(cmd="dumpsys package " + packageName):
            tmp = line.strip()
            if tmp.startswith("versionCode="):
                versionCode = tmp.split(" ")[0].split("=")[1]
                break
        return 0 if versionCode == "" else int(versionCode)
    
    def putSystemSetting(self,params):
        opt={
             'key':params['key'],
             'value':params['value']
             }
        self.shell("settings put system %s %s"%(opt['key'],opt['value']))
    
    def getSystemSetting(self,key):
        return self.shell("settings get system %s"%key)
    
    def stop_third_app(self, ignore_filter=[]):
        ignore_filter_target = ['com.github.uiautomator','com.github.uiautomator.test','com.testguard.uiautomator2','com.testguard.uiautomator2.test']
        ignore_filter_target += ignore_filter
        cmd = 'pm list package -3'
        for line in self.shell(cmd):
            if 'package:' in line:
                package_name = line[len('package:'):]
                if not package_name in ignore_filter_target:
                    self.forceStop(package_name)
                    
                
#-------------------------------SettingAction START-----------------------------------        
    def settingAction(self,SettingCode):
        cmd = 'am start -a '+SettingCode+' -f 0x10000000'
        self.shell(cmd)
    
    def intoWifiPage(self):
        self.settingAction(SettingAction.ACTION_WIFI_SETTINGS)
    
    def intoBtPage(self):
        self.settingAction(SettingAction.ACTION_BLUETOOTH_SETTINGS)
    
    def intoDataPage(self):
        self.settingAction(SettingAction.ACTION_DATA_ROAMING_SETTINGS)
        
    def intoAirplanePage(self):
        self.settingAction(SettingAction.ACTION_AIRPLANE_MODE_SETTINGS)
        
    def intoGpsPage(self):
        self.settingAction(SettingAction.ACTION_LOCATION_SOURCE_SETTINGS)
    
    def intoNfcPage(self): 
        self.settingAction(SettingAction.ACTION_NFC_SETTINGS)
     
    def intoHotpotPage(self):
        self.settingAction(SettingAction.ACTION_WIRELESS_SETTINGS)
        
    def intoDisplayPage(self):
        self.settingAction(SettingAction.ACTION_DISPLAY_SETTINGS)
        
    def intoSoundPage(self):
        self.settingAction(SettingAction.ACTION_SOUND_SETTINGS)
    
    def setScreenLightMode(self,mode):
        '''设置屏幕亮度模式'''
        opt={
             'key':'screen_brightness_mode',
             'value':mode
             }
        self.putSystemSetting(opt)
    
    def setScreenOff(self,time):
        '''设置屏幕休眠时间 单位s'''
        opt={
             'key':'screen_off_timeout',
             'value':time * 1000
             }
        self.putSystemSetting(opt)
#----------------------------------SettingAction END-----------------------------------        

if __name__ == '__main__':
    a = ADB()
    m =  a.getCurrentApp()
    print m[0],m[1]
    
   

  
    
