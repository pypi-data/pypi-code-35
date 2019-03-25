# coding=utf-8
"""
Created on 2015年11月27日

@author: thomas.ning
"""
from runner.common.log import Logger
from easyuiautomator.driver.driver import Driver
from easyuiautomator.driver.common.by import By
from runner.application.element import TestElement
from runner.application.logcat import Logcat
from runner.common import utils
import os

class TestDriver(object):
    """
    TestDriver
    """
    
    def __init__(self, device_id=None, port=None, restart=True):
        """
        __init__ 初始化TestDriver，提供log信息
        """
        self.logger = Logger.getLogger()     
        self.device = Driver.connect_device(device_id, port, restart=restart)
        self.adb = self.device.adb
        self.serial = self.device.serial
        self.store = None
        self.logcat = []  # 多个实时日志集合

    @staticmethod
    def connect_device(device_id=None, port=None, restart=True):
        return TestDriver(device_id, port, restart)
    
    @staticmethod
    def set_debug(flag=False):
        Driver.set_debug(flag)    
    
    @staticmethod
    def set_thinkTime(thinkTime=0.2):
        Driver.set_thinkTime(thinkTime)

    def set_store(self, store=None):
        self.store = store
    
    def start_battery_monitor(self, high=40, low=10, adbd_status=True, adbdThreshold=5):
        self.logger.info("start battery monitor")
        return self.device.start_battery_monitor(high, low, adbd_status, adbdThreshold)
    
    def stop_battery_monitor(self):
        self.logger.info("stop battery monitor")
        return self.device.stop_battery_monitor()
        
    def startLogcat(self, package=None, filter_b=None, filter_t=None):
        if self.store:
            logcat = Logcat(self.serial, package, self.store, filter_b, filter_t)
            logcat.startRecorder()
            self.logcat.append(logcat)
            
    def stopLogcat(self):
        for logcat in self.logcat: 
            logcat.stopRecorder()
        self.logcat = []
           
    def find_element(self, by=By.ID, value=None, thinkTime=None, timeOut=None, ignoreExp=False):
        self.logger.info("find element by %s" % value)
        ele = self.device.find_element(by, value, thinkTime, timeOut, ignoreExp=ignoreExp)
        if ele:
            return TestElement(self.device, ele.id)
        
    def find_elements(self, by=By.ID, value=None, thinkTime=None, timeOut=None, ignoreExp=False):
        self.logger.info("find elements by %s" % value)
        els = self.device.find_elements(by, value, thinkTime, timeOut, ignoreExp=ignoreExp)
        if els:
            elements = []
            for ele in els:
                elements.append(TestElement(self.device, ele.id))
            return elements

    def find_element_by_id(self, id_, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        find_element_by_id 通过ID查找元素
        id_ 元素Id
        thinkTime 响应时间
        timeOut 超时时间
        """
        return self.find_element(By.ID, id_, thinkTime, timeOut, ignoreExp)
    
    def find_elements_by_id(self, id_, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        find_elements_by_id 通过ID查找元素s
        id_ 元素Id
        thinkTime 响应时间
        timeOut 超时时间
        """
        return self.find_elements(By.ID, id_, thinkTime, timeOut, ignoreExp)
    
    def find_element_by_class_name(self, name, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        find_element_by_class_name 通过类名查找元素
        name 类名
        thinkTime 响应时间
        timeOut 超时时间
        """
        return self.find_element(By.CLASS_NAME, name, thinkTime, timeOut, ignoreExp)
    
    def find_elements_by_class_name(self, name, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        find_elements_by_class_name 通过类名查找元素s
        name 类名
        thinkTime 响应时间
        timeOut 超时时间
        """
        return self.find_elements(By.CLASS_NAME, name, thinkTime, timeOut, ignoreExp)
    
    def find_element_by_name(self, name, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        find_emement_by_name 通过文本查找元素
        name 文本内容
        thinkTime 响应时间
        timeOut 超时时间
        """
        return self.find_element(By.NAME, name, thinkTime, timeOut, ignoreExp)
    
    def find_elements_by_name(self, name, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        find_elements_by_name 通过文本显示查找元素s
        name 文本内容
        thinkTime 响应时间
        timeOut 超时时间
        """
        return self.find_elements(By.NAME, name, thinkTime, timeOut, ignoreExp)
    
    def find_element_by_xpath(self, xpath, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        find_element_by_xpath 通过层级路径查找元素  
        xpath 层级路径   层级为class内容并以"//"表示层级   如"android.widget.RelativeLayout//android.view.View"
        thinkTime 响应时间
        timeOut 超时时间
        """
        return self.find_element(By.XPATH, xpath, thinkTime, timeOut, ignoreExp)
    
    def find_elements_by_xpath(self, xpath, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        find_elements_by_xpath 通过层级路径查找元素s  
        xpath 层级路径   层级为class内容并以"//"表示层级   如"android.widget.RelativeLayout//android.view.View"
        thinkTime 响应时间
        timeOut 超时时间
        """
        return self.find_elements(By.XPATH, xpath, thinkTime, timeOut, ignoreExp)
    
    def find_element_by_accessibility_id(self, id_, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        find_element_by_accessibility_id 通过accessibilityId查找元素
        id_ content_desc信息
        thinkTime 响应时间
        timeOut 超时时间
        """
        return self.find_element(By.ACCESSIBILITY_ID, id_, thinkTime, timeOut, ignoreExp)
    
    def find_elements_by_accessibility_id(self, id_, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        find_elements_by_accessibility_id 通过accessibilityId查找元素s
        id_ content_desc信息
        thinkTime 响应时间
        timeOut 超时时间
        """
        return self.find_elements(By.ACCESSIBILITY_ID, id_, thinkTime, timeOut, ignoreExp)
    
    def find_element_by_uiautomator(self, uia_string, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        find_element_by_uiautomator 通过uiautomator查找元素
        uia_string uiautomator名称
        thinkTime 响应时间
        timeOut 超时时间
        """
        return self.find_element(By.ANDROID_UIAUTOMATOR, uia_string, thinkTime, timeOut, ignoreExp)
    
    def find_elements_by_uiautomator(self, uia_string, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        find_elements_by_uiautomator 通过uiautomator查找元素s
        uia_string uiautomator名称
        thinkTime 响应时间
        timeOut 超时时间
        """
        return self.find_elements(By.ANDROID_UIAUTOMATOR, uia_string, thinkTime, timeOut, ignoreExp)
    
    def set_timeout(self, time_to_wait):
        """
        set_timeout 设置超时时间
        time_to_wait 时间
        """
        self.logger.info('set command timeout=%s' % time_to_wait)
        self.device.set_timeout(time_to_wait)
           
    def drag(self, start_x, start_y, end_x, end_y, duration=None):
        """Drag the (x,y) to the destination element
        :Args:
         - (start_x, start_y) - the position to drag
         - (end_x, end_y)     - target position to drag to
        """
        self.device.drag(start_x, start_y, end_x, end_y, duration)
        return self
         
    def click(self, x, y):
        """Click position (x,y)"""
        self.logger.info('click positions (%s,%s)' % (x, y))
        self.device.click(x, y)
        return self
    
    def longClick(self, x, y, duration=1):
        """LongClick position (x,y)"""
        self.logger.info('longClick positions (%s,%s) and hold %ss' % (x, y, duration))
        self.device.longClick(x, y, duration)
        return self
    
    def tap(self, positions, duration=None):
        """
        tap 点击
        positions 坐标点
        duration 时长
        remark self.device.tap([(x,y)])
        """
        self.logger.info('tap positions %s' % positions)
        self.device.tap(positions, duration=duration)
        return self
    
    def touch_action(self):
        '''
        collection of a group action
        :Usage:
        driver.touch_action().press(10,10).wait(1).move_to(100,100).wait(2).press(200,200).realease().perform()
        '''
        return self.device.touch_action()
        
    def multi_action(self):
        '''
        collection of a group touch_action
        :Usage:
        action1 = driver.touch_action().press(10,10).wait(1).move_to(100,100).wait(2).press(200,200)
        action2 = driver.touch_action().press(10,10).wait(1).move_to(100,100).wait(2).press(200,200)
        action3 = driver.touch_action().press(10,10).wait(1).move_to(100,100).wait(2).press(200,200)
        driver.multi_action().add(action1,action2,action3).perform()
        '''
        return self.device.multi_action()
    
    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        """
        swipe 滑动
        start_x,start_y 起始坐标
        end_x,end_y 终止坐标
        duration 步长
        """
        self.logger.info('Swipe from (%s,%s)  to (%s,%s)' % (start_x, start_y, end_x, end_y))
        self.device.swipe(start_x, start_y, end_x, end_y, duration=duration)
        return self
    
    def flick(self, start_x, start_y, end_x, end_y):
        """
        flick 滑动
        start_x,start_y 起始坐标
        end_x,end_y 终止坐标
        """
        self.logger.info('flick from (%s,%s)  to (%s,%s)' % (start_x, start_y, end_x, end_y))
        self.device.flick(start_x, start_y, end_x, end_y)
        return self
    
    def freezeRotation(self):
        """
        freezeRotation 冻结方向传感器  
        """
        self.logger.info("freeze rotation")
        self.device.freezeRotation()
        return self
    
    def unfreezeRotation(self):
        """
        unfreezeRotation 解冻方向传感器
        """
        self.logger.info("unfreeze rotation")
        self.device.unfreezeRotation()
        return self
    
    def press_keycode(self, keycode, metastate=None):
        """
        press_keycode 点击keycode
        keycode  数字
        metastate keycode信息
        """
        self.logger.info('press %s' % keycode)
        self.device.press_keycode(keycode, metastate=metastate)
        return self
    
    def longpress_keycode(self, keycode, metastate=None, duration=None):
        """
        press_keycode 点击keycode
        keycode  数字
        metastate keycode信息
        """
        self.logger.info("long press %s" % keycode)
        self.device.longpress_keycode(keycode, metastate=metastate, duration=duration)
        return self    
        
    def back(self, count=1):
        """
        back 返回
        count 返回次数
        """
        self.logger.info("go back %d times" % count)
        while count > 0:
            self.device.back()
            count -= 1
        return self
    
    def pressHome(self):
        """
        home 返回主界面
        """
        self.logger.info("go home")
        self.device.pressHome()
        return self
    
    def pressMenu(self):
        """
        menu 菜单按钮
        """
        self.logger.info("press menu")
        self.device.pressMenu()
        return self
    
    def pressVolup(self, count=1):
        """
        volup 音量加键
        count 次数
        """
        self.logger.info("press volup")
        self.device.pressVolup(count)
        return self
    
    def pressVoldown(self, count=1):
        """
        voldown 音量减键
        count 次数
        """
        self.logger.info("press voldown")
        self.device.pressVoldown(count)
        return self
    
    def pressPower(self):
        """
        power 电源按键
        """
        self.logger.info("press power")
        self.device.pressPower()
        return self
        
            
    def wake(self):
        """
        wake 唤醒
        """
        self.logger.info("wake up")
        self.device.wake()
        return self
    
    def pageLeft(self, duration=3):
        """
        pageLeft 左翻页
        duration 时长，默认为None
        """
        self.logger.info("page left")
        self.device.pageLeft(duration)
        return self
    

    def pageRight(self, duration=3):
        """
        pageRight 右翻页
        duration 时长，默认为None
        """
        self.logger.info("page right")
        self.device.pageRight(duration)
        return self
    
    def pageUp(self, duration=3):
        """
        pageUp 上翻页
        duration 时长，默认为None
        """
        self.logger.info("page up")
        self.device.pageUp(duration)
        return self
    
    def pageDown(self, duration=3):
        """
        pageDown 下翻页
        duration 时长，默认为None
        """
        self.logger.info("page down")
        self.device.pageDown(duration)
        return self
    
    def reboot(self):
        '''重启手机'''
        self.logger.info("reboot device")
        return self.device.reboot()
    
    def isOnline(self):
        '''设备是否在线'''
        self.logger.info("check device isonline?")
        return self.device.isOnline()

    def do_adb(self, command):
        """
        do_adb 运行adb命令
        :Usage:
            command: "adb -s " + {command}
        """
        self.logger.info("do adb %s" % command)
        return self.device.adb_command(command)
    
    def setText(self, text, replace=True):
        '''输入文本'''
        self.device.setText(text, replace)
        
    def sendKeys(self, text, replace=True):
        '''输入文本'''
        self.device.sendKeys(text, replace)
    
    def open_notification(self):
        """
        open_notification 打开状态栏
        """
        self.logger.info("open notification")
        self.device.open_notification()
    
    def get_device_size(self):
        """
        get_device_size 获取手机尺寸
        """
        self.logger.info("get device size")
        return self.device.get_device_size()
    
    def get_page_source(self):
        """
        get_page_source 获取当前界面信息
        """
        self.logger.info("get page source")
        return self.device.get_page_source()
    
    def get_screenshot_as_file(self, filename, remark=False):
        """
        get_screenshot_as_file 获取当前界面截图
        filename 保存文件径及文件名
        remark 获取当前界面图片并保存到*** 
        """
        if not remark:
            if self.store:
                filename = os.path.join(self.store.getWorkDir(), filename)
        self.logger.info("get screenshot as file %s" % filename)
        return self.device.get_screenshot_as_file(filename)
    
    def get_screenshot_as_png(self):
        """
        get_screenshot_as_png 获取当前界面截图
        """
        self.logger.info("get screenshot as png")
        return self.device.get_screenshot_as_png()
    
    def get_screenshot_as_base64(self):
        """
        get_screenshot_as_base64 获取当前界面截图
        remark 不常用
        """
        self.logger.info("get screenshot as base64")
        return self.device.get_screenshot_as_base64()
    
    def quit(self):
        """
        quit 退出（断开连接）
        """
        self.logger.info("quit")        
#             self.device.quit()
    
    def clear_cache(self):
        """
        cleanCache 清空缓存
        """
        self.logger.info("clear cache")
        return self.device.clear_cache()
    
    def start_activity(self, package, activity):
        """
        start_activity 启动应用
        package 包名
        activity 应用组界面
        """
        self.logger.info("start %s/%s" % (package, activity))
        self.device.start_activity(package, activity)
        return self
    
    def wait_activity(self, activity, timeout, interval=1):
        """
        wait_activity 等待应用响应
        activity 目标应用界面
        timeout 超时次数
        """
        self.logger.info("wait %d %s" % (timeout, activity))
        return self.device.wait_activity(activity, timeout, interval=interval)
    
    def get_current_activity(self):
        """
        get_current_activity 获取当前应用
        """
        self.logger.info("get current activity")
        return self.device.get_current_activity()    
    
    def hide_keyboard(self):
        """
        hide_keyboard 隐藏软键盘
        """
        self.logger.info("hide keyboard")
        self.device.hide_keyboard()
        return self
    
    def pull_file(self, srcfile, tarfile):
        """
        pull_fill 手机文件复制到目标路径下
        srcfile 源文件
        tarfile 目标文件
        """
        self.logger.info("pull %s to %s" % (srcfile, tarfile))
        self.device.pull_file(srcfile, tarfile)
        return self
    
    def pull_folder(self, remotepath, localpath):
        """
        pull_fill 手机文件夹复制到目标路径下
        localpath 本地路径
        remotepath 远程路径
        """
        self.logger.info("pull %s to %s" % (remotepath, localpath))
        self.device.pull_folder(remotepath, localpath)
        return self
    
    def setOrientation(self, direction="landscape"):
        """
        setOrientation 设置屏幕横/竖屏
        direction landscape(横屏),portrait(竖屏)
        """
        self.logger.info("set orientation as %s" % direction)
        self.device.setOrientation(direction)
        return self
        
    def getOrientation(self):
        """
        getOrientation 获取屏幕横/竖屏
        """
        self.logger.info("get orientation")
        return self.device.getOrientation()
    
    def push_file(self, srcfile, tarfile):
        """
        push_file 拷贝文件
        srcfile 资源文件
        tarfile 目标文件
        """
        self.logger.info("push %s to %s" % (srcfile, tarfile))
        self.device.push_file(srcfile, tarfile)
        return self
    
    def lock(self):
        """
        lock 锁屏
        """
        self.logger.info("lock")
        self.device.lock()
        return self
    
    def reset(self, pkg):
        """
        reset 重置应用（效果清空并退出应用）
        """
        self.logger.info("reset %s" % pkg)
        self.device.reset(pkg)
        return self
    
    def waitForCondition(self, method, returnValue, timeout=5, intervalMs=0.5, args=None):
        '''等待方法返回，增加超时控制
          :Args:
            methon: 函数名
            args: 必须是元组参数传递形式，如（'tt',dd)
            returnValue:对比值
        '''
        return utils.waitForCondition(method, returnValue, timeout, intervalMs, args)
    
    def startApp(self, packageName, mode=0):
        '''启动a应用
          :Args:
            packageName: 包名
           mode:  模式: 0全新启动，1:直接打开，保留上一次打开状态
        '''
        return self.device.startApp(packageName, mode)
    
    def waitForIdle(self, timeout=None):
        '''等待设备空闲
          :Args:
            timeout: 默认10秒
        '''
        self.device.waitForIdle(timeout)
        
    def startToast(self):
        '''监控toast
        '''
        self.device.startToast()
        
    def stopToast(self):
        '''停止监控toast，并获取相应的值
        '''
        return self.device.stopToast()
        
#     def shake(self):
#         """
#         shake 震动
#         """
#         self.logger.info("shake")
#         Driver.shake(self)
#         return self
    
    def background(self, tms=1):
        """
        background 返回到HOME界面并随后回到应用界面
        tms 时间
        """
        self.logger.info("background")
        return self.device.background(tms)
    
    def open_recentApps(self):
        """
        open_recentApps 打开最近使用的app
        """
        self.logger.info("open recent apps")
        return self.device.open_recentApps()
    
    def open_quickSetting(self):
        """
        open_quickSetting 打开快速开关
        """
        self.logger.info("open quick setting")
        return self.device.open_quickSetting()
            
    def is_app_installed(self, apk):
        """
        is_app_installed 检查应用是否安装
        apk 应用包名
        """
        self.logger.info("is %s installed" % apk)
        return self.device.is_app_installed(apk)
    
    def install_app(self, apk, arg=None):
        """
        install_app 安装应用
        apk 应用绝对路径/相对路径
        """
        self.logger.info("install %s" % apk)
        self.device.install_app(apk, arg)
        return self
    
    def install_remote_app(self, apk):
        """
        install_remote_app 安装应用
        apk sd卡相对路径
        """
        self.logger.info("install remote %s" % apk)
        self.device.install_remote_app(apk)
        return self
    
    def remove_app(self, apk):
        """
        remove_app 卸载应用
        apk 应用包名
        """
        self.logger.info("remove %s" % apk)
        self.device.remove_app(apk)
        return self
    
    def launch_app(self, apk, activity):
        """
        launch_app 打开应用
        apk 应用包名
        activity 应用住界面
        """
        self.logger.info("launch %s/%s" % (apk, activity))
        self.device.launch_app(apk, activity)
        return self
    
    def close_app(self, apk):
        """
        close_app 关闭应用
        apk 应用包名
        """
        self.logger.info("close %s" % apk)
        self.device.close_app(apk)
        return self
    
    def sleep(self, seconds=1):
        """
        sleep 等待时间
        seconds 时间
        """
        self.logger.info("sleep %d" % seconds)
        self.device.sleep(seconds)
         
    def compare_stream(self, target_file, image_stream):
        '''
        compare 对比图片以流方式
        target_file 资源图片
        image_stream: strStrem by driver.get_screenshot_as_png
        '''
        self.logger.info("compare picture by stream")
        return self.device.compare_stream(target_file, image_stream)
    
    def compare(self, image1, image2):
        """
        compare 对比图片以文件方式
        image1 资源图片
        image2 手机当前截图
        """
        self.logger.info("compare picture by file")
        return self.device.compare(image1, image2)
     
    def crop(self, startx, starty, endx, endy, scrfile, destfile):
        """
        crop 截取部分图片
        startx,starty 起点x,y坐标
        endx,endy 终点x,y坐标
        scrfile 资源文件
        destfile 保存文件
        """
        self.logger.info("crop %s part start at (%d,%d) end at (%d,%d)" % (scrfile, startx, starty, endx, endy))
        return self.device.crop(startx, starty, endx, endy, scrfile, destfile) 
    
    def find_img_position(self, query, origin, algorithm='sift', radio=0.75):
        """
        find_img_position 查找图片元素坐标
        origin 手机当前界面
        query 目标图片
        algorthm 默认参数‘sift’
        """
        self.logger.info("find img and get position")
        return self.device.find_img_position(query, origin, algorithm, radio)
    
    def openWifi(self):
        return self.device.openWifi()
    
    def closeWifi(self):
        return self.device.closeWifi()
    
    def getWifiStatus(self):
        return self.device.getWifiStatus()
    
    def getWifiInfo(self):
        return self.device.getWifiInfo()
    
    def setWifiConnect(self, hotname, password, ctype):
        self.device.setWifiConnect(hotname, password, ctype)
    
    def disconnectWifi(self):
        self.device.disconnectWifi()
    
    def openBluetooth(self):
        self.device.openBluetooth()
    
    def closeBluetooth(self):
        self.device.closeBluetooth()
    
    def openGps(self):
        self.device.openGps()
    
    def closeGps(self):
        self.device.closeGps()
    
    def add_call_log(self, phone, num):
        self.device.add_call_log(phone, num)
    
    def clear_call_log(self):
        self.device.clear_call_log()
    
    def add_contact(self, phone, num, name=None):
        self.device.add_contact(phone, num, name)
    
    def clear_contact(self):
        self.device.clear_contact()
    
    def getFileList(self, targetDir):
        return self.device.getFileList(targetDir)
    
    def startSetting(self, action):
        self.device.startSetting(action)
    
    def setScreenLightMode(self, mode):
        '''mode 1 为自动调节屏幕亮度,0 为手动调节屏幕亮度 '''
        self.device.setScreenLightMode(mode)
    
    def getScreenLightMode(self):
        '''mode 1 为自动调节屏幕亮度,0 为手动调节屏幕亮度 '''
        return self.device.getScreenLightMode()
    
    def setRingMode(self, mode):
        '''mode 0 SILENT,1 VIBRATE 2 NORMAL '''
        self.device.setRingMode(mode)
    
    def getRingMode(self):
        '''mode 0 SILENT,1 VIBRATE 2 NORMAL '''
        return self.device.getRingMode()
    
    def openFlashlight(self):
        '''打开闪光灯 '''
        self.device.openFlashlight()
    
    def closeFlashlight(self):
        '''关闭闪光灯'''
        return self.device.closeFlashlight()
    
    def openData(self):
        '''打开数据 '''
        self.device.openData()
    
    def closeData(self):
        '''关闭数据'''
        return self.device.closeData()
    
    def getDataStatus(self):
        '''获取移动网数据状态'''
        return self.device.getDataStatus()
    
    def call(self, num):
        '''拨打电话'''
        self.device.call(num)
    
    def sendMMS(self, to_phone, msg):
        '''发送短信'''
        self.device.sendMMS(to_phone, msg)
        
    def getSimInfo(self, category=0):
        '''获取sim卡信息
        :Args:
        -category: 0 主卡
               1 副卡
        '''
        return self.device.getSimInfo(category)
    
    def getDeviceInfo(self, mode=0):
        '''获取设备信息
        :Args:
        -mode: 0 基本数据
               1 详细信息，带sd卡，sim卡信息
        '''
        return self.device.getDeviceInfo(mode)
    
    def getLocalTmpDir(self):
        ''''返回/data/local/tmp临时目录'''
        return self.device.getLocalTmpDir()
    
    def getInternalSdcard(self):
        ''''内置sd卡目录'''
        return self.device.getInternalSdcard()
    
    def getExtendSdcard(self):
        '''外置sd卡目录'''
        return self.device.getExtendSdcard()
    
    def queryRemoteSiminfo(self, imsi):
        '''获取远程sim卡信息
        :Args:
        -imsi: 国际移动用户识别码
        '''
        return self.device.queryRemoteSiminfo(imsi)
 
    def getPhoneNum(self, category=0):
        '''获取电话号码信息
        :Args:
        -category: 0 主卡
               1 副卡
        '''
        return  self.device.getPhoneNum(category)
    
    def clearUiCache(self):
        '''部分界面出现，元素无法找到，可能因为缓存区数据未更新导致，目前原因不能，先用此api处理'''
        self.device.clearUiCache()
        
    def registerUiWatcher(self, name, text, packageName=None):
        '''注册界面监听器，用于弹窗点掉机制
        app.registerUiWatcher("ll", "允许","com.huawei.systemmanager")
        :Args:
        -name: 全局唯一指定名称，用于添加，删除时的唯一标识
        -text: 出现弹出后，需要点击的文字
        -packageName: 出现弹出后，弹窗所属包名
        '''
        self.device.registerUiWatcher(name, text, packageName)
    
    def removeUiWatcher(self, name):
        '''移除指定ui监听器
        :Args:
        -name: 监听器的标识
        '''
        self.device.removeUiWatcher(name)
    
    def removeAllUiWatcher(self):
        '''移除所有ui监听器'''
        self.device.removeUiWatcher()
    
    def openQuickPanel(self, duration=None):
        '''上滑打开部分机子显现的快捷面板'''
        self.device.openQuickPanel(duration)
    
    def get_device_real_size(self):
        '''get device real size'''
        return self.device.get_device_real_size()
    
    def pressSearch(self):
        self.device.pressSearch()
        
    def pressEnter(self):
        self.device.pressEnter()
    
    def rmBlackBorder(self, srcpath, tarpath, thres, diff, shrink, directionMore):
        '''图片黑边处理
        app.rmBlackBorder("src.png","result.png" , 50,1000,0,0)
        :Args:
        -srcpath: 源图片路径
        -tarpath: 结果图片路径
        -thres: threshold for cropping: sum([r,g,b] - [0,0,0](black))图像阈值
        -diff: max tolerable difference between black borders on two side
        -shrink: number of pixels to shrink after the blackBorders removed
        -directionMore: 哪个方向上多出不对称的内容，0：正常，1：上，2：下,3：左，4：右
        '''        
        self.device.rmBlackBorder(srcpath, tarpath, thres, diff, shrink, directionMore)
    
    def getWifiHotInfo(self):
        '''获取区域归属热点信息'''
        return self.device.getWifiHotInfo()
        
class SettingUtil(object):
    '''手机setting操作部分'''
    def __init__(self, testDriver):
        pass
