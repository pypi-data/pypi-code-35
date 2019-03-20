# coding=utf-8
'''
Created on 2015年11月5日

@author: thomas.ning
'''
import base64, time, sys, json
from easyuiautomator.driver.common.by import By
from easyuiautomator.common.exceptions import TimeoutException
from easyuiautomator.common.exceptions import InvalidSelectorException
from easyuiautomator.common.exceptions import DeviceNotFound
from easyuiautomator.driver.common.mobilecommand import MobileCommand as Command
from easyuiautomator.driver.executor.command_executor import CommandExecutor
from easyuiautomator.driver.executor.wait import DriverWait
from easyuiautomator.driver.executor.utils import ImageUtil
from easyuiautomator.driver.executor.adb import ADB
from easyuiautomator.common.log import Logger
from easyuiautomator.driver.common.touch_action import TouchAction
from easyuiautomator.driver.common.multi_action import MultiAction
from easyuiautomator.driver.element import Element
from easyuiautomator.driver.common.keyevent import KeyCode
from easyuiautomator.common.view_remote_resource import ViewRemoteResource


# 收集异常信息
def collectException(func):
    def wrap(*args, **argkw):
        try:
            return func(*args, **argkw)
        except DeviceNotFound, e:
            raise DeviceNotFound(e)
        except:
            msg = sys.exc_info()[1].message
            Logger.getLogger().warning("%s is failed [%s]" % (func.__name__, msg))  
            if 'ignoreExp' not in  argkw.keys():
                raise
            if not argkw['ignoreExp']:
                raise  
    return wrap

class Driver(object):
    '''对外提供所有操作接口，统一采用此类输出'''
    
    __deviceMmonitor = []
    
    def __init__(self, device_id=None, port=None, restart=True):
        self.command_executor = CommandExecutor(device_id, port, restart)
        self.adb = self.command_executor._adb
        self.serial = self.adb.serial

    @staticmethod
    def connect_device(device_id=None, port=None, restart=True):
        return Driver(device_id, port, restart)

    @staticmethod
    def set_debug(whether=True):
        '''打开调试日志
        :Args:
            whether:True or False
        :Usage:
            Driver.set_debug()
        '''
        Logger._debug = whether

    @staticmethod
    def set_thinkTime(thinkTime=0.2):
        '''设置全局动作时间，单位秒
        :Args:
            thinkTime
        :Usage:
            Driver.set_thinkTime(2)
        '''
        CommandExecutor._thinkTime = thinkTime
    
    # Timeouts
    def set_timeout(self, time_to_wait):
        """
        Sets a sticky timeout to wait for an element to be found,or a command to complete.
        This method only needs to be called one time per driver
        :Args:
         - time_to_wait: Amount of time to wait (in seconds)
        :Usage:
            driver.set_timeout(30)
        """
        self._execute(Command.SET_TIMEOUT, {'ms': float(time_to_wait)})
    
    @staticmethod
    def addListen(fn):
        Driver.__deviceMmonitor.append(fn)
        
    @staticmethod
    def device_monitor(msg):
        for fn in Driver.__deviceMmonitor:
            if hasattr(fn, '__call__'):
                try:
                    fn(msg)
                except:
                    pass

    def find_element_by_id(self, id_, thinkTime=None, timeOut=None, ignoreExp=False):
        """Finds an element by id.
        :Args:
         - id\_ - The id of the element to be found.
        :Usage:
            driver.find_element_by_id('foo')
        """
        return self.find_element(by=By.ID, value=id_, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_elements_by_id(self, id_, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        Finds multiple elements by id.
        :Args:
         - id\_ - The id of the elements to be found.
        :Usage:
            driver.find_elements_by_id('foo')
        """
        return self.find_elements(by=By.ID, value=id_, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_element_by_xpath(self, xpath, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        Finds an element by xpath.
        :Args:
         - xpath - The xpath locator of the element to find.
        :Usage:
            driver.find_element_by_xpath('//div/td[1]')
        """
        return self.find_element(by=By.XPATH, value=xpath, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_elements_by_xpath(self, xpath, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        Finds multiple elements by xpath.
        :Args:
         - xpath - The xpath locator of the elements to be found.
        :Usage:
            driver.find_elements_by_xpath("//div[contains(@class, 'foo')]")
        """
        return self.find_elements(by=By.XPATH, value=xpath, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_element_by_name(self, name, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        Finds an element by name.
        :Args:
         - name: The name of the element to find.
        :Usage:
            driver.find_element_by_name('foo')
        """
        return self.find_element(by=By.NAME, value=name, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_elements_by_name(self, name, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        Finds elements by name.
        :Args:
         - name: The name of the elements to find.

        :Usage:
            driver.find_elements_by_name('foo')
        """
        return self.find_elements(by=By.NAME, value=name, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_element_by_class_name(self, name, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        Finds an element by class name.
        :Args:
         - name: The class name of the element to find.
        :Usage:
            driver.find_element_by_class_name('foo')
        """
        return self.find_element(by=By.CLASS_NAME, value=name, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_elements_by_class_name(self, name, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        Finds elements by class name.
        :Args:
         - name: The class name of the elements to find.
        :Usage:
            driver.find_elements_by_class_name('foo')
        """
        return self.find_elements(by=By.CLASS_NAME, value=name, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_element_by_uiautomator(self, uia_string, thinkTime=None, timeOut=None, ignoreExp=False):
        """Finds element by uiautomator in Android.
        :Args:
         - uia_string - The element name in the Android UIAutomator library

        :Usage:
            driver.find_element_by_android_uiautomator('.elements()[1].cells()[2]')
        """
        return self.find_element(by=By.ANDROID_UIAUTOMATOR, value=uia_string, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_elements_by_uiautomator(self, uia_string, thinkTime=None, timeOut=None, ignoreExp=False):
        """Finds elements by uiautomator in Android.
        :Args:
         - uia_string - The element name in the Android UIAutomator library

        :Usage:
            driver.find_elements_by_android_uiautomator('.elements()[1].cells()[2]')
        """
        return self.find_elements(by=By.ANDROID_UIAUTOMATOR, value=uia_string, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_element_by_accessibility_id(self, id_, thinkTime=None, timeOut=None, ignoreExp=False):
        """Finds an element by accessibility id.
        :Args:
         - id - a string corresponding to a recursive element search using the
         Id/Name that the native Accessibility options utilize

        :Usage:
            driver.find_element_by_accessibility_id()
        """
        return self.find_element(by=By.ACCESSIBILITY_ID, value=id_, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def find_elements_by_accessibility_id(self, id_, thinkTime=None, timeOut=None, ignoreExp=False):
        """Finds elements by accessibility id.

        :Args:
         - id - a string corresponding to a recursive element search using the
         Id/Name that the native Accessibility options utilize

        :Usage:
            driver.find_elements_by_accessibility_id()
        """
        return self.find_elements(by=By.ACCESSIBILITY_ID, value=id_, thinkTime=thinkTime, timeOut=timeOut, ignoreExp=ignoreExp)

    def create_element(self, element_id):
        """
        Creates a web element with the specified element_id.
        """
        return Element(self, element_id)

    def _wrap_value(self, value):
        if isinstance(value, dict):
            converted = {}
            for key, val in value.items():
                converted[key] = self._wrap_value(val)
            return converted
        elif isinstance(value, Element):
            return {'ELEMENT': value.id}
        elif isinstance(value, list):
            return list(self._wrap_value(item) for item in value)
        else:
            return value

    def _unwrap_value(self, value):
        if isinstance(value, dict) and ('ELEMENT' in value):
            wrapped_id = value.get('ELEMENT', None)
            if wrapped_id:
                return self.create_element(value['ELEMENT'])
        elif isinstance(value, list):
            return list(self._unwrap_value(item) for item in value)
        else:
            return value

    def _execute(self, driver_command, params=None):
        """
        Sends a command to be executed by a command.CommandExecutor.
        :Args:
         - driver_command: The name of the command to execute as a string.
         - params: A dictionary of named parameters to send with the command.
        :Returns:
          The command's JSON response loaded into a dictionary object.  
        """
        result = self.command_executor.execute(driver_command, params)
        # 检查消息体是否满足格式要求
        if result is not None:
            result['value'] = self._unwrap_value(result.get('value', None))
            return result
        return {'success': 0, 'value': None}
    
    @collectException
    def find_element(self, by=By.ID, value=None, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        'Private' method used by the find_element_by_* methods.
        :Usage:
            Use the corresponding find_element_by_* instead of this.
        :rtype: Element
        """
        if not By.is_valid(by) or not isinstance(value, str):
            raise InvalidSelectorException("Invalid locator values passed in")
        if thinkTime is not None :
            thinkTime = float(thinkTime)
        if timeOut is not None:
            timeOut = float(timeOut)
        return self._execute(Command.FIND_ELEMENT,
                             {'using': by, 'value': value, 'thinkTime':thinkTime, 'timeOut':timeOut})['value']
    @collectException
    def find_elements(self, by=By.ID, value=None, thinkTime=None, timeOut=None, ignoreExp=False):
        """
        'Private' method used by the find_element_by_* methods.
        :Usage:
            Use the corresponding find_element_by_* instead of this.

        :rtype: Element
        """
        if not By.is_valid(by) or not isinstance(value, str):
            raise InvalidSelectorException("Invalid locator values passed in")
        if thinkTime is not None :
            thinkTime = float(thinkTime)
        if timeOut is not None:
            timeOut = float(timeOut)
        return self._execute(Command.FIND_ELEMENTS,
                             {'using': by, 'value': value, 'thinkTime':thinkTime, 'timeOut':timeOut})['value']
                             
    def drag(self, start_x, start_y, end_x, end_y, duration=None):
        """Drag the (x,y) to the destination element
        :Args:
         - (x,y) - the position to drag
         - destinationEl - the element to drag to
        """
        opts = {
            "startX": start_x,
            "startY": start_y,
            'endX':end_x,
            'endY':end_y,
            "duration": duration
        }
        self._execute(Command.DRAG, opts)
        return self
    
    def click(self, x, y):
        """Click position (x,y)
        :Args:
         - (x,y) - the position to be click
        """
        opts = {
            "x": x,
            "y": y,
        }
        self._execute(Command.CLICK, opts)
        return self
    
    def longClick(self, x, y, duration=None):
        """LongClick position (x,y)
        :Args:
         - (x,y,duration) - the position to be longClick then holding for a certain time
        """
        opts = {
              'x':x,
              'y':y,
              'duration':duration
              }
        self._execute(Command.LONG_CLICK, opts)
        return self
    
    def tap(self, positions, duration=None):
        """Taps on an particular place with up to five fingers, holding for a
        certain time
        :Args:
         - positions - an array of tuples representing the x/y coordinates of
         the fingers to tap. Length can be up to five.
         - duration - (optional) length of time to tap, in s

        :Usage:
            driver.tap([(100, 20), (100, 60), (100, 100)], 1)
        """
        if len(positions) == 1:
            action = TouchAction(self)
            x = positions[0][0]
            y = positions[0][1]
            if duration:
                action.press(x=x, y=y).wait(duration).release()
            else:
                action.press(x=x, y=y).release()
            action.perform()
        else:
            ma = MultiAction(self)
            for position in positions:
                x = position[0]
                y = position[1]
                action = TouchAction(self)
                if duration:
                    action.press(x=x, y=y).wait(duration).release()
                else:
                    action.press(x=x, y=y).release()
                ma.add(action)

            ma.perform()
        return self

    def swipe(self, start_x, start_y, end_x, end_y, duration=None):
        """Swipe from one point to another point, for an optional duration.
        :Args:
         - start_x - x-coordinate at which to start
         - start_y - y-coordinate at which to start
         - end_x - x-coordinate at which to stop
         - end_y - y-coordinate at which to stop
         - duration - (optional) time to take the swipe, in ms.
        :Usage:
            driver.swipe(100, 100, 100, 400)
        """
        # `swipe` is something like press-wait-moveTo-release, which the server
        # will translate into the correct action
        if duration is None:
            duration = 0
        opts = {
               "startX": start_x,
               "startY": start_y,
               "endX": end_x,
               "endY": end_y,
               "duration":duration
               }
        self._execute(Command.SWIPE, opts)
        return self

    def flick(self, start_x, start_y, end_x, end_y):
        """Flick from one point to another point.
        :Args:
         - start_x - x-coordinate at which to start
         - start_y - y-coordinate at which to start
         - end_x - x-coordinate at which to stop
         - end_y - y-coordinate at which to stop
        :Usage:
            driver.flick(100, 100, 100, 400)
        """
        action = TouchAction(self)
        action \
            .press(x=start_x, y=start_y) \
            .moveTo(x=end_x, y=end_y) \
            .release()
        action.perform()
        return self

    def press_keycode(self, keycode, metastate=None):
        """Sends a keycode to the device. Android only. Possible keycodes can be
        found in http://developer.android.com/reference/android/view/KeyEvent.html.

        :Args:
         - keycode - the keycode to be sent to the device
         - metastate - meta information about the keycode being sent
        """
        data = {
            'keycode': keycode,
            'metastate': metastate
        }
        self._execute(Command.PRESS_KEYCODE, data)["value"]
        return self

    def longpress_keycode(self, keycode, metastate=None, duration=None):
        """
        Sends a long press of keycode to the device. Android only. Possible keycodes can be
        found in http://developer.android.com/reference/android/view/KeyEvent.html.
        :Args:
         - keycode - the keycode to be sent to the device
         - metastate - meta information about the keycode being sent
        """
        data = {
            'keycode': keycode,
            'metastate': metastate,
            'duration' : duration
        }
        self._execute(Command.LONG_PRESS_KEYCODE, data)
        return self
    
    def touch_action(self):
        '''
        collection of a group action
        :Usage:
        driver.touch_action().press(10,10).wait(1).move_to(100,100).wait(2).press(200,200).realease().perform()
        '''
        action = TouchAction(self)
        return action
    
    def multi_action(self):
        '''
        collection of a group touch_action
        :Usage:
        action1 = driver.touch_action().press(10,10).wait(1).move_to(100,100).wait(2).press(200,200)
        action2 = driver.touch_action().press(10,10).wait(1).move_to(100,100).wait(2).press(200,200)
        action3 = driver.touch_action().press(10,10).wait(1).move_to(100,100).wait(2).press(200,200)
        driver.multi_action().add(action1,action2,action3).perform()
        '''
        action = MultiAction(self)
        return action
        
    def pressMenu(self):
        self.press_keycode(KeyCode.KEYCODE_MENU)
        return self
    
    def pressHome(self):
        self.press_keycode(KeyCode.KEYCODE_HOME)
        return self
    
    def pressVolup(self, num=1):
        while num > 0:
            self.press_keycode(KeyCode.KEYCODE_VOLUME_UP)
            num = num - 1    
        return self
    
    def pressVoldown(self, num=1):
        while num > 0:
            self.press_keycode(KeyCode.KEYCODE_VOLUME_DOWN)
            num = num - 1    
        return self
    
    def pressPower(self):
        self.press_keycode(KeyCode.KEYCODE_POWER)
        return self

    def back(self, num=1):
        while num > 0:
            self._execute(Command.PRESS_BACK)
            num = num - 1
        return self

    def wake(self):
        self._execute(Command.WAKE)
        return self

    def compressed_layout_hierarchy(self, compressLayout=False):

        opts = {
            "compressLayout": compressLayout
        }
        self._execute(Command.COMPRESSD_LAYOUT_HIERARCHY, opts)
        return self

    def get_data_dir(self):
        '''get data dir as /data/local/tmp'''
        return self._execute(Command.GET_DATA_DIR)['value']

    def open_notification(self):
        '''Open Notification'''
        self._execute(Command.OPEN_NOTIFICATION)
        return self

    def get_device_size(self):
        '''get device size'''
        opt = {
             "flag":False
             }
        return self._execute(Command.GET_DEVICE_SIZE, opt)['value']

    def get_page_source(self):
        """
        Gets the source of the current page.
        :Usage:
            driver.page_source
        """
        return self._execute(Command.GET_PAGE_SOURCE)['value']

    def get_screenshot_as_file(self, filename, scale=1.0, quality=50):
        """
        Gets the screenshot of the current window. Returns False if there is
           any IOError, else returns True. Use full paths in your filename.
        :Args:
         - filename: The full path you wish to save your screenshot to.
         - scale: The screen size scale,default:1.0.
         - quality: The screen quality,default:50%  0-100.
        :Usage:
            driver.get_screenshot_as_file('/Screenshots/foo.png',0.6,100)
        """
        png = self.get_screenshot_as_png(scale, quality)
        try:
            with open(filename, 'wb') as f:
                f.write(png)
        except IOError:
            return False
        finally:
            del png
        return True

    def get_screenshot_as_png(self, scale=1.0, quality=50):
        """
        Gets the screenshot of the current window as a binary data.
        :Args:
         - scale: The screen size scale,default:1.0.
         - quality: The screen quality,default:50%  0-100.
        :Usage:
            driver.get_screenshot_as_png(0.8,80%)
        """
        return base64.b64decode(self.get_screenshot_as_base64(scale, quality).encode('ascii'))

    def get_screenshot_as_base64(self, scale=1.0, quality=50):
        """
        Gets the screenshot of the current window as a base64 encoded string
           which is useful in embedded images in HTML.
        :Args:
         - scale: The screen size scale,default:1.0.
         - quality: The screen quality,default:50%  0-100.
        :Usage:
            driver.get_screenshot_as_base64()
        """
        opts = {
            "scale": scale,
            "quality": quality
        }
        return self._execute(Command.SCREENSHOT, opts)['value']

    def setOrientation(self, direction):
        '''
        Set device screen orientation
        params: landscape,portrait
        :Usage:
             driver.setOrientation(LANDSCAPE) set screen direction to LANDSCAPE
        '''
        opt = {
             "orientation": direction
             }
        return self._execute(Command.ORIENTAION, opt)['value']

    def getOrientation(self):
        '''Get device screen orientation'''
        opt = {}
        return self._execute(Command.ORIENTAION, opt)['value']

    def pageLeft(self, duration=3):
        """向左翻页
        :Usage:
            driver.pageLeft()
        """
        self.swipe(0.1, 0.5, 0.9, 0.5, duration)
        return self

    def pageRight(self, duration=3):
        """向右翻页
        :Usage:
            driver.pageRight()
        """
        self.swipe(0.9, 0.5, 0.1, 0.5, duration)
        return self

    def pageUp(self, duration=3):
        """向上翻页
        :Usage:
            driver.pageUp()
        """
        self.swipe(0.5, 0.5, 0.5, 0.9, duration)
        return self

    def pageDown(self, duration=3):
        """ 向下翻页
        :Usage:
            driver.pageDown()
        """
        self.swipe(0.5, 0.5, 0.5, 0.1, duration)
        return self
    
    def open_quickSetting(self):
        '''打开快速设置'''
        self._execute(Command.OPEN_QUICK_SETTING)
        return self
    
    def open_recentApps(self):
        '''打开最近运行的app'''
        self._execute(Command.OPEN_RECENT_APPS)
        return self
    
    def freezeRotation(self):
        '''冻结方向传感器  '''
        opts = {
            "status" : True,
        }
        self._execute(Command.ROTATION, opts)
        return self
    
    def unfreezeRotation(self):
        '''解冻方向传感器  '''
        opts = {
            "status" : False,
        }
        self._execute(Command.ROTATION, opts)
        return self
    
    def setText(self, text, replace=True):
        '''输入文本内容'''
        opts = {
              "text" :text,
              "replace":replace
              }
        self._execute(Command.SET_TEXT, opts)
        
    def sendKeys(self, text, replace=True):
        '''输入文本内容'''
        opts = {
              "text" :text,
              "replace":replace
              }
        self._execute(Command.SEND_KEYS, opts)
        
    def waitForIdle(self, timeout=None):
        '''等待设备空闲，默认10s'''
        opts = {
                'timeout': timeout
                }
        self._execute(Command.WAIT_FOR_IDLE, opts)
     
    def startApp(self, package, mode=0):
        '''通过包名启动程序启动界面
        :Args:
           package: 程序包名
           mode:  模式: 0全新启动，1:直接打开，保留上一次打开状态
        '''
        opts = {
              'package':package,
              'mode':mode
              }
        self._execute(Command.START_APP, opts)
        
    def start_battery_monitor(self, high=50, low=15, adbd_status=True, adbdThreshold=20):
        '''
        Start Battery Monitor.

        :Args:
         - high - Charge to specifical percents level.
                  The default is 60 percents.
         - low - if battery level lower than this value,test will pause for a lot of time until the level up to high percents.
                 The default is 20 percents.
        - adbdThreshold adbd monitor time threshold, unit(minutes)

        :Usage:
            driver.start_battery_monitor()
        '''
        opts = {
            "power_status" : True,
            "high" : high,
            "low" : low,
            "adbd_status" : adbd_status,
            "adbdThreshold": adbdThreshold
        }
        return self._execute(Command.MONITOR, opts)

    def stop_battery_monitor(self):
        '''Stop Battery Monitor '''
        opts = {
            "power_status" : False,
            "adbd_status" : False
        }
        return self._execute(Command.MONITOR, opts)

    ################# ADB #########################

    def start_activity(self, package, activity):
        """
        Open the app activities.打开应用活动
        :Args:
         - package - package name of app.
         - activity - activity of app
        :Usage:
            driver.start_activity('net.csdn.app','net.csdn.app.mainactivity')
        """
        opts = {
            'package': package,
            'activity': activity
        }
        self._execute(Command.START_ACTIVITY, opts)
        return self

    def wait_activity(self, activity, timeout, interval=1):
        """Wait for an activity: block until target activity presents
        or time out.
        This is an Android-only method.
        :Args:
         - activity - target activity
         - timeout - max wait time, in seconds
         - interval - sleep interval between retries, in seconds
        """
        try:
            DriverWait(self, timeout, interval).until(
                lambda d: d.get_current_app()[1] == activity)
            return True
        except TimeoutException:
            return False

    def get_current_app(self):
        """Retrieves the current app on the device.获取当前应用
        :Usage:
            driver.get_current_app()
        """
        return self._execute(Command.GET_CURRENT_APP)['value']

    def hide_keyboard(self):
        """
        Hide keyboard if it exists in screen.隐藏手机软键盘
        :Usage:
            driver.hide_keyboard()
        """
        self._execute(Command.HIDE_KEYBOARD)
        return self

    def pull_file(self, srcfile, tarfile):
        """
        Put file from cellphone to PC.将文件从手机放入计算机
        :Args:
         - srcFile - source file
         - targetFile - target file
        :Usage:
            driver.pull_file('/storage/sdcard0/360Download/new.txt','D:/')
        """
        opts = {
            'srcfile': srcfile,
            'tarfile': tarfile
        }
        self._execute(Command.PULL_FILE, opts)
        return self

    def pull_folder(self, remotepath, localpath):
        """
        Put folder from cellphone to PC. 将文件夹从手机放入计算机
        :Args:
         - srcFile - source folder path
         - targetFile - target path
        :Usage:
            driver.pull_folder('/storage/sdcard0/360Download','D:/')
        """
        opts = {
            'localpath': localpath,
            'remotepath': remotepath
        }
        self._execute(Command.PULL_FOLDER, opts)
        return self

    def push_file(self, srcfile, tarfile):
        '''
        Put file or folder from PC to cellphone.将文件或者文件夹从计算机放入手机
        :Args:
         - localpath - local file path in phone
         - remotepath - path in pc
        :Usage:
            driver.push_file('D:/screen.txt','/storage/sdcard0/360Download/')
        '''
        opts = {
            'srcfile': srcfile,
            'tarfile': tarfile
        }
        self._execute(Command.PUSH_FILE, opts)
        return self

    def lock(self):
        """
        Lock the screen.
        :Usage:
            driver.lock()
        """
        self._execute(Command.LOCK)
        return self

    def reset(self, pkg):
        """
        Reset app by clear it.清理应用数据重置应用
        :Args:
         - pkg _ app package.
        :Usage:
            driver.reset('net.csdn.app')
        """
        opts = {
            'pkg': pkg
        }
        self._execute(Command.RESET, opts)
        return self

    def shake(self):
        '''
        Shake cellphone. 手机震动
        :Usage:
            driver.shake()

        :Warning:
            It will be useful in future.
        '''
        self._execute(Command.SHAKE)
        return self

    def background(self, tms):
        '''
        Back to home idle and return to app activity.返回到HOME界面并随后回到应用界面
        :Args:
         - tms - :seconds
        :Usage:
            driver.background(1)
        '''
        opts = {'tms': tms}
        self._execute(Command.BACKGROUND, opts)
        return self

    def is_app_installed(self, apk):
        '''
        Whether the app is installed or not.手机应用是否安装,第三方应用
        :Args:
         - apk - :app package
        :Usage:
            driver.is_app_installed('net.csdn.app')
        '''
        opts = {
            'apk': apk
        }
        return self._execute(Command.IS_APP_INSTALLED, opts)['value']

    def install_app(self, apk, arg=None):
        '''
        Install the app.安装手机应用
        :Args:
         - apk - file.apk
        :Usage:
            driver.install_app('d:/csdn.apk')
        '''
        opts = {
            'apk': apk,
            'arg': arg
        }
        self._execute(Command.INSTALL_APP, opts)
        return self
    
    def install_remote_app(self, apk):
        '''
        Install remote app.安装手机应用
        :Args:
         - apk - file.apk
        :Usage:
            driver.install_remote_app('/data/local/tmp/csdn.apk')
        '''
        opts = {
            'apk': apk
        }
        return self._execute(Command.INSTALL_REMOTE_APP, opts)['value']
       
    def remove_app(self, apk):
        '''
        Uninstall the app.卸载手机应用
        :Args:
         - apk - app package
        :Usage:
            remove_app('net.csdn.app')
        '''
        opts = {
            'apk': apk
        }
        self._execute(Command.REMOVE_APP, opts)
        return self

    def launch_app(self, apk, activity):
        '''
        Launch the app.启动手机应用
        :Args:
         - apk - app package
         - activity - app activity
        :Usage:
            driver.launch_app('net.csdn.app','net.csdn.app.mainactivity')
        :Warning:
            The same with start_activity for the time being
        '''
        opts = {
            'apk': apk,
            'activity': activity
        }
        self._execute(Command.LAUNCH_APP, opts)
        return self

    def close_app(self, apk):
        '''
        exit the app.退出手机应用
        :Args:
         - apk - app package name
        :Usage:
            driver.close_app('net.csdn.app')
        '''
        opts = {
            'apk': apk
        }
        self._execute(Command.CLOSE_APP, opts)
        return self

    def adb_command(self, command):
        '''
        Execute ADB command。执行ADB命令
        :Args:
          - command - ADB command
        :Usage:
            command: "adb -s " + {command}
            driver.adb_command('devices')
        '''
        opts = {
            'command': command
        }
        return self._execute(Command.DO_ADB, opts)['value']
    
    def getAdb(self, restart=True):
        ''''返回adb操作集，restart为错误时，是否重启adb'''
        return ADB(self.serial, restart)

    def sleep(self, seconds):
        '''Sleep several seconds.
        :Args:
         - seconds - seconds
        :Usage:
            driver.sleep(1)
        '''
        time.sleep(seconds)
        
    @collectException
    def clear_cache(self):
        self._execute(Command.CLEAR_CACHE)

############################################################
    def find_img_position(self, query, origin, algorithm='sift', radio=0.75):
        '''
            search picture,return position
        :Args:
         - query: Target file of need search.
         - origin: driver.get_screenshot_as_png or file path
         - algorithm: default sift
        '''
        return ImageUtil.find_image_positon(query, origin, algorithm, radio)
    
    def compare_stream(self, target_file, image_stream):
        '''
        file stream compare
        :Args:
         - strStream: strStrem by driver.get_screenshot_as_png.
         - target_file: need compared target file.
        '''
        return ImageUtil.compare_stream(image_stream, target_file)
    
    def compare(self, image1, image2):
        """
        Calculate the similarity  between f1 and f2
        return similarity  0-100
        """
        return ImageUtil.compare(image1, image2)

    def crop(self, startx, starty, endx, endy, scrfile, destfile):
        """
        cut img by the given coordinates and picture, then make target file
        """
        return ImageUtil.crop(startx, starty, endx, endy, scrfile, destfile)
    
    def quit(self):
        '''disconnect device,then release resource'''
        self.command_executor.stop()
        self.command_executor = None
    
    def reboot(self):
        '''重启手机'''
        return self.adb_command("reboot")
    
    def isOnline(self):
        '''设备是否在线'''
        return self._execute(Command.IS_ONLINE)['value']
    
    def isScreenLocked(self):
        '''屏幕是否锁着'''
        return self._execute(Command.IS_LOCKED)['value']
    
    def startToast(self):
        '''开启后台toast获取'''
        opts = {
              'flag':True
              }
        self._execute(Command.TOAST, opts)
        
    def stopToast(self):
        '''获取toast并关闭监听'''
        opts = {
              'flag':False
              }
        return self._execute(Command.TOAST, opts)['value']
    
    def call(self, num):
        '''拨打电话'''
        self.adb_command("shell am start -a android.intent.action.CALL tel:%s" % num)
    
    def sendMMS(self, to_phone, msg):
        '''发送短信'''
        self.adb_command("shell am start -a android.intent.action.SENDTO -d sms:%s --es sms_body %s" % (to_phone, msg))        
    
    def openWifi(self):
        opts = {
            'type':"set",
            'flag':True
            }
        return self._execute(Command.WIFI, opts)['value']
    
    def closeWifi(self):
        opts = {
            'type':"set",
            'flag':False
            }
        return self._execute(Command.WIFI, opts)['value']
    
    def getWifiStatus(self):
        opts = {
            'type':"get_status",
            }
        return self._execute(Command.WIFI, opts)['value']
    
    def getWifiInfo(self):
        opts = {
            'type':"get_info",
            }
        result = self._execute(Command.WIFI, opts)['value']
        if result:
            return json.loads(result)
        return result
    
    def setWifiConnect(self, hotname, password, ctype):
        opts = {
            'type':"connect",
            'hot':hotname,
            'password':password,
            'ctype':ctype
            }
        self._execute(Command.WIFI, opts)
    
    def disconnectWifi(self):
        opts = {
            'type':"disconnect",
            }
        self._execute(Command.WIFI, opts)
    
    def openBluetooth(self):
        opts = {
             'flag':True
             }
        self._execute(Command.BLUETOOTH, opts)
    
    def closeBluetooth(self):
        opts = {
             'flag':False
             }
        self._execute(Command.BLUETOOTH, opts)
    
    def openGps(self):
        opts = {
             'flag':True
             }
        self._execute(Command.GPS, opts)
    
    def closeGps(self):
        opts = {
             'flag':False
             }
        self._execute(Command.GPS, opts)
    
    def add_call_log(self, phone, num):
        opts = {
             'type':"add",
             'phone':phone,
             'num': num,
             }
        self._execute(Command.CALL_LOG, opts)
    
    def clear_call_log(self):
        opts = {
             'type':"clear"
             }
        self._execute(Command.CALL_LOG, opts)
    
    def add_contact(self, phone, num, name=None):
        '''添加联系人
        :Args:
        -phone: 要添加的联系人姓名
        -num: 一共要添加多少个联系人
        -name: 联系人的姓名，没有时，显示电话号码
        '''
        opts = {
             'type':"add",
             'phone':phone,
             'name':name,
             'num': num,
             }
        self._execute(Command.CONTACT, opts)
    
    def clear_contact(self):
        opts = {
             'type':"clear"
            }
        self._execute(Command.CONTACT, opts)
    
    def getFileList(self, targetDir, mode=1, showtype=0):
        '''sd卡目录下，相关文件及大小'''
        opts = {
             'dir':targetDir,  # 目录名
             'mode':mode,  # 查找模式，1 内置sd卡，2 外置sd卡
             'showtype':showtype,  # 返回数据形式， 0 只返回文件名，1 文件名及大小
            }
        return self._execute(Command.File_List, opts)['value']
    
    def startSetting(self, action):
        opts = {
             'action':action
            }
        self._execute(Command.SettingAction, opts)
    
    def setScreenLightMode(self, mode):
        '''mode 1 为自动调节屏幕亮度,0 为手动调节屏幕亮度 '''
#         opts={
#              'type':"set",
#              'mode':mode
#             }
#         self._execute(Command.LIGHT, opts)
        self.adb.setScreenLightMode(mode)
    
    def getScreenLightMode(self):
        '''mode 1 为自动调节屏幕亮度,0 为手动调节屏幕亮度 '''
        opts = {
             'type':"get",
             'mode':'mode'
            }
        return self._execute(Command.LIGHT, opts)['value']
    
    def setRingMode(self, mode):
        '''mode 0 SILENT,1 VIBRATE 2 NORMAL '''
        opts = {
             'type':"set",
             'mode':mode
            }
        self._execute(Command.AUDIO, opts)
    
    def getRingMode(self):
        '''mode 0 SILENT,1 VIBRATE 2 NORMAL '''
        opts = {
             'type':"get",
             'mode':'mode'
            }
        return self._execute(Command.AUDIO, opts)['value']
    
    def openFlashlight(self):
        '''打开闪光灯 '''
        opts = {
             'type':"open",
            }
        self._execute(Command.CAMARA_LIGHT, opts)
    
    def closeFlashlight(self):
        '''关闭闪光灯'''
        opts = {
             'type':"close",
            }
        return self._execute(Command.CAMARA_LIGHT, opts)
    
    def openData(self):
        '''打开闪光灯 '''
        opts = {
             'type':"open",
            }
        self._execute(Command.DATA, opts)
    
    def closeData(self):
        '''关闭闪光灯'''
        opts = {
             'type':"close",
            }
        return self._execute(Command.DATA, opts)
    
    def getDataStatus(self):
        '''获取移动网数据状态'''
        opts = {
             'type':"get",
            }
        return self._execute(Command.DATA, opts)['value']
    
    def _setConfigurator(self, method, value):
        '''设置测试配置参数
        :Args:
        -method: actionAcknowledgmentTimeout(3 * 1000) keyInjectionDelay(0) 
                 scrollAcknowledgmentTimeout(200) waitForIdleTimeout(10 * 1000)
                 waitForSelectorTimeout(10 * 1000)
        -value(ms): 设置操作等待时间，单位是ms
        '''
        opts = {
             'config': method,
             'value': value
            }
        self._execute(Command.CONFIGURATOR, opts)
    
    def getSimInfo(self, category=0):
        '''获取sim卡信息
        :Args:
        -type: 0 主卡
               1 副卡
        '''
        opts = {
             'type': category
            }
        return json.loads(self._execute(Command.SIM_INFO, opts)['value'])
        
    
    def getDeviceInfo(self, mode=0):
        '''获取设备信息
        :Args:
        -mode: 0 基本数据
               1 详细信息，带sd卡，sim卡信息
        '''
        opts = {
             'mode': mode
            }
        return self._execute(Command.DEVICE_INFO, opts)['value']
    
    def getLocalTmpDir(self):
        ''''返回/data/local/tmp临时目录'''
        return self._getDevicePath(0)
    
    def getInternalSdcard(self):
        ''''内置sd卡目录'''
        return self._getDevicePath(1)
    
    def getExtendSdcard(self):
        '''外置sd卡目录'''
        return self._getDevicePath(2)
    
    def _getDevicePath(self, mode=0):
        '''获取设备目录信息
        :Args:
        -mode: 0 临时数据目录
               1 内置sd卡目录
               2 外置sd卡目录
        '''
        opts = {
             'mode': mode
            }
        return self._execute(Command.DEVICE_PATH, opts)['value']
    
    def queryRemoteSiminfo(self, imsi):
        '''获取设备目录信息
        :Args:
        -imsi: 国际移动用户识别码
        '''
        opts = {
             'imsi': imsi
            }
        return self._execute(Command.REMOTE_SIM_INFO, opts)['value']
    
    def getPhoneNum(self, category=0):
        '''获取电话号码信息'''
        siminfo = self.getSimInfo(category).get("imsi")
        return self.queryRemoteSiminfo(siminfo).get("number")
    
    def clearUiCache(self):
        '''部分界面出现，元素无法找到，可能因为缓存区数据未更新导致，目前原因不能，先用此api处理'''
        self._execute(Command.CLEAR_UI_CACHE)
        
    def registerUiWatcher(self, name, text, packageName=None):
        '''注册界面监听器，用于弹窗点掉机制
        app.registerUiWatcher("ll", "允许","com.huawei.systemmanager")
        :Args:
        -name: 全局唯一指定名称，用于添加，删除时的唯一标识
        -text: 出现弹出后，需要点击的文字
        -packageName: 出现弹出后，弹窗所属包名
        '''
        opt = {
              "flag":"add",
              "name":name,
              "text":text,
              "packageName":packageName
              }
        self._execute(Command.UI_WATCHERS, opt)
    
    def removeUiWatcher(self, name):
        '''移除指定ui监听器'''
        opt = {
              "flag":"remove",
              "name":name,
              }
        self._execute(Command.UI_WATCHERS, opt)
    
    def removeAllUiWatcher(self):
        '''移除所有ui监听器'''
        opt = {
              "flag":"removeall",
              }
        self._execute(Command.UI_WATCHERS, opt)
    
    def openQuickPanel(self, duration=None):
        '''上滑打开部分机子显现的快捷面板'''
        self.swipe(0.5, 0.99, 0.5, 0.5, duration)
    
    def get_device_real_size(self):
        '''get device real size'''
        opt = {
               "flag":True
               }
        return self._execute(Command.GET_DEVICE_SIZE, opt)['value']
    
    def pressSearch(self):
        self.press_keycode(84)
        
    def pressEnter(self):
        self.press_keycode(66)
    
    def getContactNum(self):
        '''获取联系人个数'''
        opt = {
               'type':"get"
               }
        return self._execute(Command.CONTACT, opt)['value']
        
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
        ImageUtil.rmBlackBorder(srcpath, tarpath, thres, diff, shrink, directionMore)
        
    def getWifiHotInfo(self):
        '''获取wifi热点信息'''
        try:
            return ViewRemoteResource.getInstance().getWifiHotInfo()['data']
        except:
            pass
    
    def stop_third_app(self,ignore_filter=[]):
        '''停止第三方app'''
        self.adb.stop_third_app(ignore_filter)
    
