# coding=utf-8

"""
Created on 2015年11月6日

@author: thomas.ning
"""
import time,math,utils,copy,os,re
from adb import ADB
from uiautomator import Uiautomator
from easyuiautomator.common.exceptions import DriverException
from easyuiautomator.common.exceptions import TimeoutException
from easyuiautomator.common.exceptions import AdbException
from easyuiautomator.common.exceptions import UiautomatorException
from easyuiautomator.driver.common.mobilecommand import MobileCommand as Command
from easyuiautomator.common.log import Logger
from easyuiautomator.common.view_remote_resource import ViewRemoteResource
from easyuiautomator.common.exceptions import RemoteServiceException

ip_match = "^\d+\.\d+\.\d+\.\d+$"

class CommandExecutor(object):

    """命令执行器，用来执行adb命令及远程uiautomator命令字"""
    _thinkTime = 0.5  #命令执行前等待时间，已启用
    _timeOut = None # 命令执行超时时长，未启用

    def __init__(self, device_id=None, port=None, restart=True):
        self.logger = Logger.getLogger()
#         if re.match(ip_match, device_id) == False:
        self._adb = ADB(device_id, restart)
        self.sdk_version = self._adb.getApiLevel()
        self.logger.debug("sdk version %s on %s"%(self.sdk_version, self._adb.serial))
        self._uiautomator = Uiautomator(adb=self._adb, sdk_version=self.sdk_version, local_port=port)
        self._uiautomator.start()  # 启动uiautomator远程服务
        # 电量监控相关参数
        self.powerMonitor = PowerMonitor(self._adb)
        self._controller = Controller(self._adb, self._uiautomator, self._timeOut)
        # commandExecutor support all command word
        self._commands = {
            Command.FIND_ELEMENT: self._controller.findElement,
            Command.FIND_ELEMENTS: self._controller.findElements,
            Command.FINE_CHILD_ELEMNT: self._controller.findChildElement,
            Command.FINE_CHILD_ELEMNTS: self._controller.findChildElements,
            Command.ZOOM: self._controller.zoom,
            Command.PINCH: self._controller.pinch,
            Command.SET_TIMEOUT: self._controller.setTimeout,
            Command.CLICK: self._controller.click,
            Command.LONG_CLICK: self._controller.longclick,
            Command.WIFI: self._controller.wifi,
            Command.CLEAR_ELEMENT: self._controller.clear,
            Command.IS_EXIST: self._controller.isExist,
            Command.GET_TEXT: self._controller.getText,
            Command.SET_TEXT: self._controller.setText,
            Command.GET_SIZE: self._controller.getSize,
            Command.GET_LOCATION: self._controller.getLocation,
            Command.GET_ATTRIUBTE: self._controller.getAttribute,
            Command.LOCK: self._controller.lock,
            Command.WAKE: self._controller.wake,
            Command.GET_DEVICE_SIZE: self._controller.getDeviceSize,
            Command.COMPRESSD_LAYOUT_HIERARCHY: self._controller.compressedLayoutHierarchy,
            Command.OPEN_NOTIFICATION: self._controller.openNotification,
            Command.GET_DATA_DIR: self._controller.getDataDir,
            Command.GET_PAGE_SOURCE: self._controller.source,
            Command.GET_PARENT: self._controller.getParent,
            Command.START_APP: self._controller.startApp,
#             Command.SCREENSHOT: self._controller.takeScreenshot,
            Command.TOUCH_ACTION: self._controller.touchAction,
            Command.MULTI_ACTION: self._controller.multiAction,
            Command.PRESS_KEYCODE: self._controller.pressKeyCode,
            Command.LONG_PRESS_KEYCODE: self._controller.longPressKeyCode,
            Command.PRESS_BACK: self._controller.goBack,
            Command.SCROLL_TO: self._controller.scrollTo,
            Command.SCROLL_ORIENTAION: self._controller.scrollOrientation,
            Command.SWIPE : self._controller.swipe,
            Command.SWIPE_ORIENTAION : self._controller.swipeOrientation,
            Command.ORIENTAION : self._controller.orientation,
            Command.DRAG : self._controller.drag,
            Command.SCROLL_ORIENTAION:self._controller.swipeDirection,
            Command.MONITOR:self._controller.monitor,
            Command.CLEAR_CACHE:self._controller.clearCache,
            Command.OPEN_QUICK_SETTING:self._controller.openQuickSetting,
            Command.OPEN_RECENT_APPS:self._controller.openRecentApp,
            Command.ROTATION:self._controller.roatation,
            Command.TOAST: self._controller.toast,
            Command.WAIT_FOR_IDLE: self._controller.waitForIdle,
            Command.CALL_LOG: self._controller.call_log,
            Command.CONTACT: self._controller.contact,
            Command.BLUETOOTH: self._controller.bluetooth,
            Command.GPS: self._controller.gps,
            Command.SettingAction: self._controller.settingAction,
            Command.File_List: self._controller.fileList,
            Command.LIGHT: self._controller.light,
            Command.AUDIO: self._controller.audio,
            Command.CAMARA_LIGHT: self._controller.flashLight,
            Command.DATA: self._controller.data,
            Command.CONFIGURATOR: self._controller.configurator,
            Command.DEVICE_INFO: self._controller.device_info,
            Command.DEVICE_PATH: self._controller.device_path,
            Command.SIM_INFO: self._controller.sim_info,
            Command.CLEAR_UI_CACHE: self._controller.clearUiCache,
            Command.UI_WATCHERS: self._controller.uiWatcher,
            Command.SEND_KEYS: self._controller.sendKeys,
            
            #############remote######################
            Command.REMOTE_SIM_INFO: self._controller.remote_sim_info,

            ####### ADB #######
            Command.START_ACTIVITY: self._controller.startActivity,
#             Command.SCREENSHOT: self._controller.takeScreenshot_adb,
             Command.SCREENSHOT: self._controller.takeScreenshot,
            Command.GET_CURRENT_APP: self._controller.getCurrentApp,
            Command.HIDE_KEYBOARD: self._controller.hideKeyboard,
            Command.PULL_FILE: self._controller.pullFile,
            Command.PULL_FOLDER: self._controller.pullFolder,
            Command.PUSH_FILE: self._controller.pushFile,
            Command.RESET: self._controller.reset,
            Command.SHAKE: self._controller.shake,
            Command.BACKGROUND: self._controller.background,
            Command.IS_APP_INSTALLED: self._controller.isAppInstalled,
            Command.INSTALL_APP: self._controller.installApp,
            Command.INSTALL_REMOTE_APP: self._controller.installRemoteApp,
            Command.REMOVE_APP: self._controller.removeApp,
            Command.LAUNCH_APP: self._controller.lanuchApp,
            Command.CLOSE_APP: self._controller.closeApp,
            Command.DO_ADB: self._controller.doAdb,
            Command.IS_ONLINE: self._controller.isOnline,
            Command.IS_LOCKED: self._controller.isScreenLocked
        }

    def execute(self, driver_command, params):
        """
        Sends a command to be executed by a command.CommandExecutor.
        :Args:
         - driver_command: The name of the command to execute as a string.
         - params: A dictionary of named parameters to send with the command.
        :Returns:
          The command's JSON response loaded into a dictionary object.
        """
        command_info = self._commands.get(driver_command)
        assert command_info is not None, 'Unrecognised command %s' % driver_command
        if params is not None:
            if params.get("thinkTime"):
                time.sleep(params.get("thinkTime"))
            elif self._thinkTime:
                time.sleep(self._thinkTime)
        elif self._thinkTime:
            time.sleep(self._thinkTime)
        self.logger.info("[%s exec %s params:%s]" % (self._adb.serial, driver_command, utils.dump_json(params, ensure_ascii=False)))
        if driver_command == Command.MONITOR:
            power_status = params["power_status"]
            height = params["high"] if params.get("high") else 40
            low = params["low"] if params.get("low") else 10
            self.powerMonitor.setMonitorParams(power_status, height, low)
            return
        self.powerMonitor.waitPowerStatus() # 查看手机电量情况
        reponse = command_info(params)
        return reponse

    def stop(self):
        self._adb.restart = False
        self._uiautomator.stop()

class PowerMonitor:
    
    def __init__(self, adb):
        self.logger = Logger.getLogger()
        self.adb = adb
        self.charging = False
        self.power_monitor = False
        self.power_high = 40
        self.power_low = 10
        self.current_power_level = 0
        self.lastCheckTime = 0
        
    def setMonitorParams(self,power_monitor, power_high, power_low):
        self.power_monitor = power_monitor
        self.power_high = power_high
        self.power_low = power_low
        
    def waitPowerStatus(self):
        if time.time() - self.lastCheckTime < 5*60: # 电量正常时，每隔5分钟读取电量一次
            return
        while self.power_monitor:
            if self.checkPowerLevelThresold():
                time.sleep(5*60)
            else:
                break
        self.lastCheckTime = time.time()
        
    def checkPowerLevelThresold(self):
        '''true: 充电  false: 未充电'''
        self._setPowerLevel()
        if self.current_power_level > self.power_high:
            self.charging = False
            return False
        if self.current_power_level < self.power_low:
            self.charging = True
            self.logger.warning("%s 正在充电中，当前电量%s"%(self.adb.serial,self.current_power_level))
            return True
        if self.current_power_level < self.power_high \
        and self.current_power_level > self.power_low:
            if self.charging:
                self.logger.warning("%s 正在充电中，当前电量%s"%(self.adb.serial,self.current_power_level))
                return True
            return False

    def _setPowerLevel(self):
        current_power_level = self.adb.get_battery()
        if current_power_level is None:
            self.current_power_level = 100
            self.logger.warning("电量无法正常获取,电量监控功能失效")
            return
        if current_power_level > 0:
            try:
                self.current_power_level = int(current_power_level)
            except:
                pass


class Controller(object):
    """    
    Controller provide all basic action routing
    """
    
    def __init__(self, adb, uiautomator, timeout):
        self.timeout = timeout  # 查找元素超时时长
        self.steps = 20  # 默认滑动步长
        self._adb = adb
        self._uiautomator = uiautomator

    def compressedLayoutHierarchy(self, params):
        result = self._uiautomator.sendActon("compressedLayoutHierarchy", params)
        return self._deal_result(result)

    def getDataDir(self, params):
        result = self._uiautomator.sendActon("getDataDir", params)
        return self._deal_result(result)

    def source(self, params):
        result = self._uiautomator.sendActon("source", params)
        return self._deal_result(result)

    def getDeviceSize(self, params):
        result = self._uiautomator.sendActon("getDeviceSize", params)
        return self._deal_result(result)

    def openNotification(self, params):
        result = self._uiautomator.sendActon("openNotification", params)
        return self._deal_result(result)

    def takeScreenshot(self, params):
        opts = {
              "scale": params["scale"] if params.get("scale") else 1.0,
              "quality": params["quality"] if params.get("quality") else 50
              }
        if params.get("id"):
            opts["elementId"] = params["id"]
            result = self._uiautomator.sendActon("element:takeScreenshot", opts)
        else:
            result = self._uiautomator.sendActon("takeScreenshot", opts)
        return self._deal_result(result)

    def findElements(self, params):
        params["multiple"] = True
        result = self._find(params)
        return self._deal_result(result)

    def findElement(self, params):
        params['multiple'] = False
        result = self._find(params)
        return self._deal_result(result)

    def findChildElement(self, params):
        params['multiple'] = False
        result = self._find(params)
        return self._deal_result(result)

    def findChildElements(self, params):
        params['multiple'] = True
        result = self._find(params)
        return self._deal_result(result)

    def _find(self, params):
        opts = {
            'strategy': params["using"],
            'selector': params["value"],
            'multiple': params['multiple'],
            'context': params["id"] if params.get("id") else ""
        }
        if opts['strategy'] == "xpath" \
                and opts['context'] != "":
            raise DriverException("Cannot use xpath locator strategy from an element."
                                  "It can only be used from the root element")
        if params['timeOut'] is not None or self.timeout is not None:
            return self._waitForCondition(self._uiautomator.sendActon, ("find", opts), params['timeOut'])
        return self._uiautomator.sendActon("find", opts)
        

    def _waitForCondition(self, method, args, timeout=None, intervalMs=0.5):
        if timeout is None:
            timeout = self.timeout
        end_time = time.time() + timeout
        while True:
            response = method(args[0], args[1])
            if response != None and response['status'] == 0 and response['value'] is not None:
                return response
            elif time.time() - end_time > 0:
                raise TimeoutException(utils.formatExceptionStr(self._adb.serial, response['value'] if response else None))
            time.sleep(intervalMs)

    def setTimeout(self, params):
        ms = params['ms']
        self.timeout = ms

    def click(self, params):
        opts = {}
        opts['x'] = params["x"] if params.get("x") else 1
        opts["y"] = params["y"] if params.get("y") else 1
        if params.get("id"):
            opts["elementId"] = params["id"]
            result = self._uiautomator.sendActon("element:click", opts)
        else:
            result = self._uiautomator.sendActon("click", opts)
        return self._deal_result(result)

    def longclick(self, params):
        opts = {}
        opts['x'] = params["x"] if params.get("x") else 1
        opts["y"] = params["y"] if params.get("y") else 1
        if params.get("duration") is not None:
            opts["duration"] = params["duration"]
        if params.get("id"):
            opts["elementId"] = params["id"]
            result = self._uiautomator.sendActon("element:touchLongClick", opts)
        else:
            result = self._uiautomator.sendActon("touchLongClick", opts)
        return self._deal_result(result)

    def touchDown(self, params):
        opts = {}
        if params.get('id'): opts["elementId"] = params["id"]
        opts['x'] = params["x"] if params.get("x") else 1
        opts["y"] = params["y"] if params.get("y") else 1
        result = self._uiautomator.sendActon("element:touchDown", opts)
        return self._deal_result(result)

    def touchMove(self, params):
        opts = {}
        if params.get("id"): opts["elementId"] = params["id"]
        opts['x'] = params["x"] if params.get("x") else 1
        opts["y"] = params["y"] if params.get("y") else 1
        result = self._uiautomator.sendActon("element:touchMove", opts)
        return self._deal_result(result)

    def touchUp(self, params):
        opts = {}
        if params.get("id"): opts["elementId"] = params["id"]
        opts['x'] = params["x"] if params.get("x") else 1
        opts["y"] = params["y"] if params.get("y") else 1
        result = self._uiautomator.sendActon("element:touchUp", opts)
        return self._deal_result(result)

    def touchAction(self, params):
        command = {
            'tap': self.touchDown,
            'press': self.touchDown,
            'release': self.touchUp,
            'moveTo': self.touchMove,
            'wait': self._wait,
            'longPress': self.longclick,
        }
        actions = params.get('actions')
        for tmpaction in actions:
            action = tmpaction.get('action', None)
            opts = tmpaction.get('options')
            command_info = command[action]
            command_info(opts)
        return utils.formatReturnStr(0, "")


    def multiAction(self, params):
        actions = params.get('actions')
        touch_list = []
        for action in actions:
            touch_list.append(self._gesture(action))
        actions = {'actions': touch_list}
        result = self._uiautomator.sendActon("performMultiPointerGesture", actions)
        return self._deal_result(result)

    def _gesture(self, actions):
        '''处理多点触控行为，返回uiautomator识别的指令'''
        opts = []
        tmp = {}
        touch_action = ['press', 'moveTo', 'tap', 'longPress']
        offset = 0.0
        for action in actions:
            if action.get('action') == 'release':
                offset = 0.0
                continue
            if action.get('action') in touch_action:
                offset += 0.005
                options = action.get("options")
                tmp = copy.copy(options)
                touch = {
                    'action': action.get('action'),
                    'touch': options,
                    'time': round(offset, 3)
                }
                opts.append(touch)
            elif action.get('action') == 'wait':
                options = action.get("options")
                tmp['ms'] = options['ms']
                offset += options['ms'] / 1000.0
                touch = {
                    'action': 'wait',
                    'touch': tmp,
                    'time': round(offset, 3),
                }
                opts.append(touch)
        return opts
    
    def wifi(self,params):
        result = self._uiautomator.sendActon("wifi", params)
        return self._deal_result(result)
    
    def settingAction(self,params):
        result = self._uiautomator.sendActon("settingAction", params)
        return self._deal_result(result)
    
    def call_log(self,params):
        result = self._uiautomator.sendActon("calllog", params)
        return self._deal_result(result)
    
    def gps(self,params):
        result = self._uiautomator.sendActon("gps", params)
        return self._deal_result(result)
    
    def bluetooth(self,params):
        result = self._uiautomator.sendActon("bluetooth", params)
        return self._deal_result(result)
    
    def contact(self,params):
        result = self._uiautomator.sendActon("contact", params)
        return self._deal_result(result)
    
    def light(self,params):
        result = self._uiautomator.sendActon("light", params)
        return self._deal_result(result)
    
    def audio(self,params):
        result = self._uiautomator.sendActon("audio", params)
        return self._deal_result(result)
    
    def flashLight(self,params):
        result = self._uiautomator.sendActon("camaraLight", params)
        return self._deal_result(result)
    
    def data(self,params):
        result = self._uiautomator.sendActon("data", params)
        return self._deal_result(result)
    
    def configurator(self,params):
        result = self._uiautomator.sendActon("configurator", params)
        return self._deal_result(result)
    def device_info(self,params):
        result = self._uiautomator.sendActon("deviceinfo", params)
        return self._deal_result(result)
    
    def device_path(self,params):
        result = self._uiautomator.sendActon("devicepath", params)
        return self._deal_result(result)
    
    def sim_info(self,params):
        result = self._uiautomator.sendActon("sim_info", params)
        return self._deal_result(result)
    
    def _wait(self, secs):
        if isinstance(secs, int):
            ms = secs
        elif isinstance(secs, dict):
            ms = secs.get('ms', None)
        time.sleep(ms)
        
    def isExist(self, params):
        opts = {
            "elementId": params["id"],
        }
        result = self._uiautomator.sendActon("element:isExist", opts)
        return self._deal_result(result)

    def zoom(self, params):
        opts = {
            "direction": 'out',
            "elementId": params["id"],
            "percent": params["percent"],
            "steps": params["steps"]
        }
        result = self._uiautomator.sendActon("element:pinch", opts)
        return self._deal_result(result)

    def pinch(self, params):
        opts = {
            "direction": 'in',
            "elementId": params["id"],
            "percent": params["percent"],
            "steps": params["steps"]
        }
        result = self._uiautomator.sendActon("element:pinch", opts)
        return self._deal_result(result)

    def longPressKeyCode(self, params):
        result = self._uiautomator.sendActon("longPressKeyCode", params)
        return self._deal_result(result)

    def pressKeyCode(self, params):
        result = self._uiautomator.sendActon("pressKeyCode", params)
        return self._deal_result(result)
#         self.pressKeyCode_adb(params['keycode'])

    def goBack(self, params):
        result = self._uiautomator.sendActon("pressBack", params)
        return self._deal_result(result)

    def clear(self, params):
        opts = {
            'elementId': params['id']
        }
        result = self._uiautomator.sendActon("element:clear", opts)
        return self._deal_result(result)
    
    def startApp(self,params):
        opts = {
            'packageName': params['package'],
            'mode':params['mode']
        }
        result = self._uiautomator.sendActon("startApp", opts)
        return self._deal_result(result)

    def drag(self, params):
        opts = {
            "elementId": params["id"] if params.get("id") else None,
            "destElId":params["destElId"] if params.get("destElId") else None,
            "startX": params["startX"] if params.get("startX") else 1,
            "startY": params["startY"] if params.get("startY") else 1,
            "endX": params["endX"] if params.get("endX") else 1,
            "endY": params["endY"] if params.get("endY") else 1,
            "steps":(int)(math.ceil(params["duration"] * 20)) if params.get("duration") else self.steps
        }
        if params.get('id'):
            result = self._uiautomator.sendActon("element:drag", opts)
        else:
            result = self._uiautomator.sendActon("drag", opts)
        return self._deal_result(result)

    def swipe(self, params):
        opts = {
            "startX": params["startX"],
            "startY": params["startY"],
            "endX": params["endX"],
            "endY": params["endY"],
            "steps": (int)(math.ceil(params["duration"] * 20)) if params.get("duration") else self.steps
        }
        if params.get('id'):
            result = self._uiautomator.sendActon("element:swipe", opts)
        else:
            result = self._uiautomator.sendActon("swipe", opts)
        return self._deal_result(result)

    def swipeOrientation(self, params):
        '''
        :Args:
            keyword    : swipeOrientation
            params     : direction(UP, DOWN, LEFT, RIGHT)
                        steps(int)
        '''
        opts = {
                "elementId": params["id"],
                "direction": params["direction"],
                "steps": (int)(math.ceil(params["duration"] * 20)) if params.get("duration") else self.steps,
                }
        result = self._uiautomator.sendActon("element:swipeOrientation", opts)
        return self._deal_result(result)

    def flick(self, params):
        opts = {
            "startX": params["x"],
            "startY": params["y"],
            "endX": params["x"],
            "endY": params["y"],
            "steps": (int)(math.ceil(params["duration"] * 20)) if params.get("duration") else self.steps
        }

        if params.get('id'):
            result = self._uiautomator.sendActon("element:swipe", opts)
        else:
            result = self._uiautomator.sendActon("swipe", opts)
        return self._deal_result(result)

    def scrollTo(self, params):
        """
        instead of the elementId as the element to be scrolled too,
        it's the scrollable view to swipe until the uiobject that has the text is found.
        """
        opts = {
            "elementId": params["id"],
            "text": params['text'],
            "direction": params["direction"],
        }
        result = self._uiautomator.sendActon("element:scrollTo", opts)
        return self._deal_result(result)

    def scrollOrientation(self, params):
        opts = {
            "elementId": params["id"],
            "direction": params["direction"],
            "steps" : params['steps']
        }
        result = self._uiautomator.sendActon("element:scrollOrientation", opts)
        return self._deal_result(result)

    def getAttribute(self, params):
        opts = {
            "elementId": params["id"],
            "attribute": params["attribute"]
        }
        result = self._uiautomator.sendActon("element:getAttribute", opts)
        if result:
            if result['status'] == 0: 
                if result[u'value'] == 'false':
                    result[u'value'] = False
                elif result[u'value'] == 'true':
                    result[u'value'] = True
                return result
        raise UiautomatorException(utils.formatExceptionStr(self._adb.serial, result))

    def setText(self, params):
        opts = {
            "elementId": params["id"] if params.get("id") else None,
            "text": params["text"],
            "replace": params["replace"]
        }
        if params.get("id"):
            result = self._uiautomator.sendActon("element:setText", opts)
        else:
            result = self._uiautomator.sendActon("setText", opts)
        return self._deal_result(result)

    def getText(self, params):
        result = self._uiautomator.sendActon("getText", params)
        return self._deal_result(result)
    

    def getSize(self, params):
        opts = {
            'elementId': params['id']
        }
        result = self._uiautomator.sendActon("element:getSize", opts)
        return self._deal_result(result)

    def getLocation(self, params):
        opts = {
            'elementId': params['id']
        }
        result = self._uiautomator.sendActon("element:getLocation", opts)
        return self._deal_result(result)

    def wake(self, params=None):
        result = self._uiautomator.sendActon("wake", params)
        return self._deal_result(result)
    
    def waitForIdle(self,params):
        result = self._uiautomator.sendActon("waitForIdle", params)
        return self._deal_result(result)

    def orientation(self, params):
        '''
        ROTATION_0(0), ROTATION_90(1), ROTATION_180(2), ROTATION_270(3)
        params: landscape,portrait
        '''
        opts = {}
        orientation = params.get('orientation')
        if orientation:
            opts['orientation'] = orientation
        result = self._uiautomator.sendActon("orientation", opts)
        return self._deal_result(result)
    
    def fileList(self,params):
        result = self._uiautomator.sendActon("fileList", params)
        return self._deal_result(result)

    def clearCache(self, params):
        result = self._uiautomator.sendActon("clearCache", params)
        return self._deal_result(result)
    
    def clearUiCache(self,params):
        result = self._uiautomator.sendActon("clearUiCache", params)
        return self._deal_result(result)
    
    def uiWatcher(self,params):
        result = self._uiautomator.sendActon("uiWatcher", params)
        return self._deal_result(result)

    #####################################################################################################
    ############################################   NEW PLUS    ##########################################
    #####################################################################################################

    def swipeDirection(self, params):
        opts = {
            "elementId": params["id"],
            "steps": (int)(math.ceil(params["duration"] * 20)) if params.get("duration") else 10,
            "direction": params["direction"],
        }
        result = self._uiautomator.sendActon("element:scrollOrientation", opts)
        return self._deal_result(result)

    def lock(self, params=None):
        result = self._uiautomator.sendActon("lock", params)
        time.sleep(1)
        return self._deal_result(result)
    
    def openQuickSetting(self,params):
        result = self._uiautomator.sendActon("openQuickSetting", params)
        return self._deal_result(result)
    
    def openRecentApp(self,params):
        result = self._uiautomator.sendActon("openRecentApp", params)
        return self._deal_result(result)
    
    def roatation(self, params):
        opts = {}
        roatation = params.get('status')
        if roatation == True:
            opts['status'] = 'freeze'    
        else:
            opts['status'] = 'unfreeze'
        result = self._uiautomator.sendActon("rotation", opts)
        return self._deal_result(result)
    
    def monitor(self, params):
        '''
        power monitor and adbd monitor  
        :Args:
        "power_status": Open if true, or shut down 
        "height": power monitor height threshold
        "low": power monitor low threshold
        "adbd_status": Open if true, or shut down
        "adbThreshold": adbd monitor duration time
        '''
        opts = {
            "power_status": params["power_status"],
            "height": params["high"] if params.get("high") else 40,
            "low": params["low"] if params.get("low") else 10,
            "adbd_status": params["adbd_status"],
            "adbdThreshold": params["adbdThreshold"] if params.get("adbdThreshold") else 20
        }
        result = self._uiautomator.sendActon("monitor", opts)
        return self._deal_result(result)
    
    def toast(self,params):
        result = self._uiautomator.sendActon("toast", params)
        return self._deal_result(result)
    
    def getParent(self,params):
        opts = {
            "elementId": params["id"],
        }
        result = self._uiautomator.sendActon("element:getParent", opts)
        return self._deal_result(result)
    
    def sendKeys(self, params):
        opts = {
            "text": params["text"],
            "replace": params["replace"]
        }
        result = self._uiautomator.sendActon("sendKeys", opts)
        return self._deal_result(result)
    
    def _deal_result(self,result):
        if result:
            if result['status'] == 0:
                return result
        raise UiautomatorException(utils.formatExceptionStr(self._adb.serial, result))
        
        
    ################################################################
    ####                          ADB                           ####
    ################################################################
    
    def takeScreenshot_adb(self, params):
        png = self._adb.takeScreenshot()
        if png is not None:
            return utils.formatReturnStr(0, png)
        raise AdbException(utils.formatExceptionStr(self._adb.serial, "not png"))

    def startActivity(self, params):
        if type(params['package']) != str or type(params['activity']) != str:
            raise AdbException(str(utils.formatReturnStr(1, 'type of args must be string')))
        if params['package'] == '' or params['activity'] == '':
            raise AdbException(utils.formatExceptionStr(self._adb.serial, 'args cannot be null'))
        value = self._adb.startActivity('%s/%s' % (params['package'], params['activity']))
        if 'Error' not in str(value):
            return utils.formatReturnStr(0, value)
        raise AdbException(utils.formatExceptionStr(self._adb.serial, value))
    
    def getCurrentApp(self, params=None):
        return utils.formatReturnStr(0, self._adb.getCurrentApp())

    def lanuchApp(self, params):  ################未能通过包名获取LAUNCHER活动，暂时需要传全值
        if type(params['apk']) != str or type(params['activity']) != str:
            raise AdbException(utils.formatExceptionStr(self._adb.serial, 'type of args must be string'))
        if params['apk'] == '' or params['activity'] == '':
            raise AdbException(utils.formatExceptionStr(self._adb.serial, 'args cannot be null'))
        value = self._adb.startActivity('%s/%s' % (params['apk'], params['activity']))
        if 'Error' not in str(value):
            return utils.formatReturnStr(0, value)
        raise AdbException(utils.formatExceptionStr(self._adb.serial, value))

    def closeApp(self, params):
        if self._adb.forceStop(params['apk']) == []:
            return utils.formatReturnStr(0, 'close app success')
        else:
            raise AdbException(utils.formatExceptionStr(self._adb.serial, 'close app failed'))

    def lock_adb(self, params=None):
        self._adb.lock()
        time.sleep(1)
        if self.isLocked() == True:
            return utils.formatReturnStr(0, 'Lock Success')
        else:
            raise AdbException(utils.formatExceptionStr(self._adb.serial, 'Fail To Unlock'))

    def reset(self, params):
        value = self._adb.reset(params['pkg'])
        if 'Success' in str(value):
            return utils.formatReturnStr(0, value)
        raise AdbException(utils.formatExceptionStr(self._adb.serial, value))

    def shake(self, params=None):
        self._adb.shake()
        raise AdbException(utils.formatExceptionStr(self._adb.serial, 'not implement'))

    def unlock(self, params=None):
        self._adb.unlock()
        if self.isLocked() == False:
            return utils.formatReturnStr(0, 'Unlock Success')
        else:
            raise AdbException(utils.formatExceptionStr(self._adb.serial, 'Fail To Unlock'))

    def isLocked(self):
        return self._adb.isScreenLocked()

    def input_adb(self, context):
        self._adb.type(context)

    def hideKeyboard(self, params=None):
        value = self._adb.hideKeyboard()
        if value == 'keyboard is not visible':
            return utils.formatReturnStr(0, value)
        raise AdbException(utils.formatExceptionStr(self._adb.serial, value))

    def pullFile(self, params):
        values = self._adb.pull(params['srcfile'], params['tarfile'])
        for value in values:
            if '100%' in value:
                return utils.formatReturnStr(0, value)
        else:
            raise AdbException (utils.formatExceptionStr(self._adb.serial, values))

    def pullFolder(self, params):
        folderName = params['remotepath'].split("/")[-1]
        target_path = os.path.join(params['localpath'], folderName)
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        values = self._adb.pull(params['remotepath'], target_path)
        for value in values:
            if '100%' in value:
                return utils.formatReturnStr(0, value)
        else:
            raise AdbException (utils.formatExceptionStr(self._adb.serial, values))

    def pushFile(self, params):
        values = self._adb.push(params['srcfile'], params['tarfile'])
        for value in values:
            if '100%' in value:
                return utils.formatReturnStr(0, value)
        else:
            raise AdbException (utils.formatExceptionStr(self._adb.serial, values))

    def background(self, params):
        if type(params['tms']) != int:
            raise AdbException(utils.formatExceptionStr(self._adb.serial, 'Canshu Wrong'))
        return utils.formatReturnStr(0, self._adb.background(params['tms']))

    def pressKeyCode_adb(self, keycode):
        self._adb.press(keycode)

    def longPressKeyCode_adb(self, keycode):
        self._adb.longPress(keycode)

    def installApp(self, params):
        result = self._adb.install(params['apk'],params['arg'])
        if 'Success' in str(result):
            return utils.formatReturnStr(0, result)
        raise AdbException(utils.formatExceptionStr(self._adb.serial, result))
    
    def installRemoteApp(self, params):
        result = self._adb.installRemote(params['apk'])
        if 'Success' in str(result):
            return utils.formatReturnStr(0, result)
        raise AdbException(utils.formatExceptionStr(self._adb.serial, result))
        
    def removeApp(self, params):
        result = self._adb.uninstallApk(params['apk'])
        if 'Success' in str(result):
            return utils.formatReturnStr(0, result)
        raise AdbException(utils.formatExceptionStr(self._adb.serial, result))
    
    def isAppInstalled(self, params):
        result = self._adb.isAppinstalled(params['apk'])
        if result == True:
            return utils.formatReturnStr(0, True)
        return utils.formatReturnStr(1, False)

    def doAdb(self, params):
        return utils.formatReturnStr(0, self._adb.exec_adb(params['command']))
    
    def isOnline(self,params=None):
        flag = self._adb.isOnline()
        return utils.formatReturnStr(0, flag)
      
    def isScreenLocked(self, params=None):
        flag = self._adb.isScreenLocked()
        return utils.formatReturnStr(0, flag)
    
    #####remote信息#################
    def remote_sim_info(self,parames=None):
        iccid = parames['imsi']
        data = ViewRemoteResource.getInstance().getSimInfo(iccid)
        if data['data']:
            return utils.formatReturnStr(0, data['data'])
        else:
            raise RemoteServiceException(utils.formatReturnStr(1, "not available data"))
