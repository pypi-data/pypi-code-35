# coding=utf-8
'''
Created on 2015年11月5日

@author: thomas.ning
'''

class MobileCommand(object):

    CONTEXTS = 'getContexts',
    GET_CURRENT_CONTEXT = 'getCurrentContext',
    SWITCH_TO_CONTEXT = 'switchToContext'
    GET_NETWORK_CONNECTION = 'getNetworkConnection'
    SET_NETWORK_CONNECTION = 'setNetworkConnection'
    GET_AVAILABLE_IME_ENGINES = 'getAvailableIMEEngines'
    IS_IME_ACTIVE = 'isIMEActive'
    ACTIVATE_IME_ENGINE = 'activateIMEEngine'
    DEACTIVATE_IME_ENGINE = 'deactivateIMEEngine'
    GET_ACTIVE_IME_ENGINE = 'getActiveEngine'
    TOGGLE_LOCATION_SERVICES = 'toggleLocationServices'
    LOCATION_IN_VIEW = 'locationInView'
    SET_IMMEDIATE_VALUE = 'setImmediateValue'
    REPLACE_KEYS = 'replaceKeys'
    GET_SETTINGS = 'getSettings'
    UPDATE_SETTINGS = 'updateSettings'


#################################################################################################

    '''
    drive uiautomator action
    '''
    FIND_ELEMENT = "findElement"
    FIND_ELEMENTS = "findElements"
    GET_PARENT = "getParent"
    IS_EXIST = "isExist"
    PRESS_KEYCODE = 'pressKeyCode'
    PRESS_BACK = "pressBack"
    LONG_PRESS_KEYCODE = 'longPressKeyCode'
    TOUCH_ACTION = 'touchAction'
    MULTI_ACTION = 'multiAction'
    WAKE = "wake"
    ZOOM = "zoom"
    PINCH = "pinch"
    DRAG = "drag"
    FLICK = "flick"
    SWIPE = "swipe"
    SWIPE_ORIENTAION = "swipeOrientation"
    SCROLL_TO = "scrollTo"
    SCROLL_ORIENTAION = "scrollOrientation"
    GET_DATA_DIR = "getDataDir"
    SCREENSHOT = "screenshot"
    COMPRESSD_LAYOUT_HIERARCHY = "compressedLayoutHierarchy"
    GET_DEVICE_SIZE = "getDeviceSize"
    OPEN_NOTIFICATION = "openNotification"
    OPEN_RECENT_APPS = "openRecentApp"
    OPEN_QUICK_SETTING = "openQuickSetting"
    ROTATION = "rotation"
    START_APP = "startApp"
    UPDATE_STRINGS = "updateStrings"
    GET_PAGE_SOURCE = "getPageSource"
    LOCK = 'lock'
    UNLOCK = "unlock"
    WAIT_FOR_IDLE = "waitForIdle"
    ORIENTAION = "orientation"
    SHUTDOWN = "shutdown"
    PING = "ping"
    CLEAR_CACHE="clearCache"
    CLICK = "click"
    LONG_CLICK = "touchLongClick"
    
    '''
    element action
    '''
    FINE_CHILD_ELEMNT = "findChildElement"
    FINE_CHILD_ELEMNTS = "findChileElements"
    CLEAR_ELEMENT = "clearElement"

    GET_ATTRIUBTE = "getAttribute"
    GET_LOCATION = "getLocation"
    GET_SIZE = "getSize"
    GET_TEXT = "getText"
    SET_TEXT = "setText"
    GET_NAME = "getName"
    GET_BOUNDS = "getBounds"
    SET_LOCATION = 'setLocation'
    
    '''
    common
    '''
    TAKE_SCREEN_SHOT = "takeScreenshot"
    SET_TIMEOUT = "setTimout"
    SET_THINKTIME = "setThinktime"
    BATTERY_CTRL = "batteryCtrl"
    MONITOR = "monitor" # 监听电量 adbd
    
    '''
    driver adb
    '''
    START_ACTIVITY = 'startActivity'
    GET_CURRENT_APP = 'getCurrentAPP'
    HIDE_KEYBOARD = 'hideKeyboard'
    PULL_FILE = 'pullFile'
    PULL_FOLDER = 'pullFolder'
    PUSH_FILE = 'pushFile'
    SHAKE = 'shake'
    RESET = 'reset'
    BACKGROUND = 'background'
    IS_APP_INSTALLED = 'isAppInstalled'
    INSTALL_APP = 'installApp'
    INSTALL_REMOTE_APP = 'installRemoteApp'
    REMOVE_APP = 'removeApp'
    LAUNCH_APP = 'launchApp'
    CLOSE_APP = 'closeApp'
    DO_ADB = 'doAdb'
    IS_ONLINE = 'is_online'
    IS_LOCKED = 'is_locked'
    TOAST = "toast"
    WIFI = "wifi"
    BLUETOOTH = "bluetooth"
    CONTACT = "contact"
    CALL_LOG = "calllog"
    GPS = "gps"
    SettingAction = "settingAction"
    File_List = "fileList"
    LIGHT = "light"
    AUDIO = "audio"
    CAMARA_LIGHT = "camaraLight"
    DATA = "data"
    CONFIGURATOR = "configurator"
    DEVICE_INFO = "deviceinfo"
    DEVICE_PATH = "devicepath"
    SIM_INFO = "sim_info"
    REMOTE_SIM_INFO = "remote_sim_info"
    CLEAR_UI_CACHE = "clearUiCache"
    UI_WATCHERS = "ui_watcher"
    SEND_KEYS = "sendKeys"
    
