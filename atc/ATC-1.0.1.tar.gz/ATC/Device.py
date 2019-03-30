# coding=utf-8

"""
 :Deadb_commandion:    设备类
 :author          80071482/bony
 :@version         V1.1
 :@Date            2017年05月
"""
import os
import re
# import time
# import subprocess
# import threading
# import inspect
# import ctypes
import platform
from ATC.Element import Element
from ATC.Memory import Memory
from ATC.System import SystemInfo
from ATC.ScreenRecord import ScreenRecord
from ATC.Command import Command
# from SurfaceStatsCollector import SurfaceStatsCollector
import xml.etree.cElementTree as ET

PATH = lambda p: os.path.abspath(os.path.join(os.path.dir_NAME(__file__), p))

# 判断系统类型，windows使用findstr，linux使用grep
sys_info = platform.system()
if sys_info is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"


class Device(object):
    def __init__(self, _SERIAL=None, _NAME=None):
        self._DEBUG = False
        self._WIDTH = None
        self._HIGH = None
        self._SERIAL = _SERIAL
        self._NAME = _NAME
        self._SYSTEM = self.system()
        self.ScreenRecord = ScreenRecord(self)
        # self._SurfaceStatsCollector_ = SurfaceStatsCollector(self)

    def init_screen_size(self):
        try:
            wh = self._SYSTEM.get_screen_resolution()
            self._WIDTH = wh[0]
            self._HIGH = wh[1]
            return True
        except Exception as e:
            print(e.message)
            # raise e

    def adb_command(self, cmd):
        return Command(self.make_cmd(cmd)).read()

    def make_cmd(self, cmd):
        if self._SERIAL is not None:
            cmd = 'adb -s ' + self._SERIAL + ' ' + cmd.split('adb')[1]
        if self._DEBUG is True:
            print(cmd)
        return cmd

    def set_debug(self, boolean):
        """
        设置debug值
        """
        self._DEBUG = boolean

    def get_debug(self):
        """
        获取debug值
        """
        return self._DEBUG

    def get_name(self):
        """
        获取设备名称
        """
        return self._NAME

    def get_serial(self):
        """
        获取设备序列号
        """
        return self._SERIAL

    def rm(self, path):
        """
        删除文件
        """
        self.adb_command('adb shell rm -rf ' + path)

    def sdcard_rm(self, path):
        """
        删除sdcard中的文件
        """
        path = '/mnt/sdcard' + path
        self.rm(path)

    def get_layout_xml(self, path):
        self.adb_command('adb shell uiautomator dump --compressed /data/local/tmp/LayoutXml.xml')
        self.adb_command('adb pull /data/local/tmp/LayoutXml.xml ' + PATH(path))
        self.adb_command('adb shell rm -r /data/local/tmp/LayoutXml.xml')

    def get_screencap(self, path=None):
        """
        get screencap
        :param path: 存放文件夹路径
        :return: file <png>
        """
        self.adb_command('adb shell /system/bin/screencap -p /sdcard/screencap.png')
        if path is None:
            self.adb_command('adb pull /sdcard/screencap.png ./screencap.png')
        else:
            self.adb_command('adb pull /sdcard/screencap.png ' + path)
        self.adb_command("adb shell rm /sdcard/screencap.png")

    def click(self, x, y):
        """
        点击坐标
        :param x:横坐标
        :param y:纵坐标
        :return:None
        """
        self.adb_command('adb shell input tap %s %s' % (x, y))

    def click_back(self):
        """
        click Back
        :return:
        """
        self.click_keycode('KEYCODE_BACK')

    def click_star(self):
        """
        click star
        :return:
        """
        self.click_keycode('KEYCODE_STAR')

    def click_enter(self):
        """
        click Enter
        :return:
        """
        self.click_keycode('KEYCODE_ENTER')

    def swipe(self, x, y, x1, y1):
        """
        swipe
        :param x: 起始横坐标
        :param y: 起始纵坐标
        :param x1: 终止横坐标
        :param y1: 终止纵坐标
        :return:
        """
        self.adb_command('adb shell input swipe %s %s %s %s' % (x, y, x1, y1))

    def swipe_to_left(self, proportion):
        """
        向左滑动
        """
        if self._WIDTH is None or self._HIGH is None:
            self.init_screen_size()
        self.swipe(
            self._WIDTH * (0.5 + 0.5 * proportion), self._HIGH * 0.5,
            self._WIDTH * (0.5 - 0.5 * proportion), self._HIGH * 0.5)

    def swipe_to_right(self, proportion):
        """
        向右滑动
        """
        if self._WIDTH is None or self._HIGH is None:
            self.init_screen_size()
        self.swipe(
            self._WIDTH * (0.5 - 0.5 * proportion), self._HIGH * 0.5,
            self._WIDTH * (0.5 + 0.5 * proportion), self._HIGH * 0.5)

    def swipe_to_up(self, proportion):
        """
        向上滑动
        """
        if self._WIDTH is None or self._HIGH is None:
            self.init_screen_size()
        self.swipe(
            self._WIDTH * 0.5, self._HIGH * (0.5 + 0.5 * proportion),
            self._WIDTH * 0.5, self._HIGH * (0.5 - 0.5 * proportion))

    def swipe_to_down(self, proportion):
        """
        向下滑动
        """
        if self._WIDTH is None or self._HIGH is None:
            self.init_screen_size()
        self.swipe(
            self._WIDTH * 0.5, self._HIGH * (0.5 - 0.5 * proportion),
            self._WIDTH * 0.5, self._HIGH * (0.5 + 0.5 * proportion))

    def long_click(self, x, y):
        """
        长按某一位置
        :param x: 横坐标
        :param y: 纵坐标
        :return:
        """
        self.adb_command('adb shell input swipe %s %s %s %s 2000' % (x, y, x, y))

    def input(self, text):
        """
        input txt
        :param text:
        :return:
        """
        self.adb_command('adb shell input text ' + text)

    def click_keycode(self, keycode):
        """
        tap Key code
        :param keycode:
        :return:
        """
        self.adb_command('adb shell input keyevent ' + keycode)

    def long_click_keycode(self, keycode):
        """
        long Press Key code
        :param keycode:
        :return:
        """
        self.adb_command('input keyevent --longpress ' + keycode)

    def install_app(self, apk_path):
        """
        根据app路径安装app
        :param apk_path: app file path
        :return:
        """
        self.adb_command('adb install -r ' + apk_path)

    def stop_app(self, package):
        """
        stop app
        :param package:包名
        :return:
        """
        self.adb_command('adb shell am force-stop ' + package)

    def start_app(self, package, activity):
        """
        Start App
        :param package:包名
        :param activity:主视图
        :return:
        """
        self.adb_command('adb shell am start ' + package + '/' + activity)

    def app_clear_data(self, package):
        """
        Clear App Data
        :param package:包名
        :return:
        """
        self.adb_command('adb shell pm clear ' + package)

    def wifi_stop(self):
        """
        wifi stop
        """
        self.adb_command('adb shell svc wifi disable')

    def wifi_start(self):
        """
        wifi start
        """
        self.adb_command('adb shell svc wifi enable')

    def p_SERIAL(self, package):
        """
        get p_SERIAL
        :param package: 包名
        :return:p_SERIAL
        """
        rtu = self.adb_command("adb shell \"ps |grep " + package + " |grep -v :\"")
        if rtu == "":
            print(package + " Not have start!")
            return None
        else:
            arr = rtu.split(' ')
            arr = filter(lambda x: x != '', arr)
            return arr[1]

    def get_memory(self, package=None):
        """
        get Memory
        :param package:包名
        :return: 内存对象
        """
        return Memory(self, package)

    def get_focused_package_activity(self):
        """
        获取当前应用界面的包名和Activity
        """
        pa = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
        out = self.adb_command("adb shell dumpsys window w | " + find_util + " \/| " + find_util + " _NAME=")
        if len(pa.findall(out)) < 1:
            return out
        else:
            return pa.findall(out)[0]

    def find_elements(self, _type, value):
        """
        同属性多个元素
        """
        element_list = []
        self.get_layout_xml("LayoutXml.xml")
        tree = ET.ElementTree(file=PATH("LayoutXml.xml"))
        xml_elements = tree.iter(tag="node")
        for xmlElement in xml_elements:
            if xmlElement.attrib[_type] == value:
                bounds = xmlElement.attrib["bounds"]
                pattern = re.compile(r"\d+")
                bound = pattern.findall(bounds)
                x = (int(bound[2]) - int(bound[0])) / 2.0 + int(bound[0])
                y = (int(bound[3]) - int(bound[1])) / 2.0 + int(bound[1])
                # 将匹配的元素区域的中心点添加进pointList中
                element = Element(x, y, self)
                element.TEXT = xmlElement.attrib["text"]
                element.BOUND = bound
                element_list.append(element)
        return element_list

    def find_element(self, _type, value):
        """
        获取元素
        """
        if type is "index_path":
            element = self.find_index_path_element(value)
            return element
        else:
            element = self.find_type_element(_type, value)
            return element

    def find_type_element(self, _type, value):
        """
        根据元素属性定位元素
        """
        self.get_layout_xml("LayoutXml.xml")
        tree = ET.ElementTree(file=PATH("LayoutXml.xml"))
        xml_elements = tree.iter(tag="node")
        element = Element(device=self)
        for xmlElement in xml_elements:
            if xmlElement.attrib[_type] == value:
                bounds = xmlElement.attrib["bounds"]
                pattern = re.compile(r"\d+")
                bound = pattern.findall(bounds)
                element.X_COORDINATE = (int(bound[0]) + int(bound[2])) / 2
                element.Y_COORDINATE = (int(bound[1]) + int(bound[3])) / 2
                element.TEXT = xmlElement.attrib["text"]
                element.BOUND = bound
        return element

    def find_index_path_element(self, value):
        """
        根据xpath定位元素
        """
        self.get_layout_xml("LayoutXml.xml")
        tree = ET.ElementTree(file=PATH("LayoutXml.xml"))
        root = tree.getroot()
        for index in value:
            root = root[index]
        bounds = root.attrib["bounds"]
        pattern = re.compile(r"\d+")
        bound = pattern.findall(bounds)
        x = (int(bound[0]) + int(bound[2])) / 2
        y = (int(bound[1]) + int(bound[3])) / 2
        element = Element(x, y, self)
        element.TEXT = root.attrib["text"]
        element.BOUND = bound
        return element

    def system(self):
        """
        返回系统信息操作对象
        """
        return SystemInfo(self)

    # def get_surface_stats_collector(self):
    #     """
    #     :return SurfaceStatsCollector
    #     """
    #     return self._SurfaceStatsCollector_
    #
    # def fps_stats_start(self, focuse__NAME=None):
    #     """
    #     开始收集fps
    #     :param focuse__NAME:包名None or SurfaceView
    #     """
    #     if focuse__NAME is not None:
    #         self._SurfaceStatsCollector_._focuse__NAME = focuse__NAME
    #     self._SurfaceStatsCollector_.DisableWarningAboutEmptyData()
    #     self._SurfaceStatsCollector_.Start()
    #
    # def fps_stats_stop(self, result__NAME=None):
    #     """
    #     结束收集fps，并返回结果
    #     """
    #     self._SurfaceStatsCollector_.Stop()
    #     results = self._SurfaceStatsCollector_.GetResults()
    #     if result__NAME is not None:
    #         for result in results:
    #             if result._NAME in result__NAME:
    #                 return result
    #         return None
    #     else:
    #         return results

    def clear_log(self):
        """
        清除设备日志缓存
        """
        self.adb_command("adb shell logcat -c")

    def get_log(self, grep=None, f_NAME=None):
        """
        获取设备运行缓存日志
        :param f_NAME:日志保存路径
        :param grep:过滤条件，可以是list或字符串
        """
        cmd_text = "adb shell \" logcat -d"
        if isinstance(grep, list):
            for value in grep:
                cmd_text += " |grep \'" + str(value) + "\'"
        else:
            cmd_text += "|grep " + str(grep)
        cmd_text += " \" "
        if f_NAME is not None:
            cmd_text += "> " + f_NAME
            self.adb_command(cmd_text)
        else:
            return self.adb_command(cmd_text)

# def appLog(self, packge_NAME, Path):
#     P_SERIAL = self.getP_SERIAL(packge_NAME)
#     self.getLog("adb shell \"logcat |grep " + str(P_SERIAL) + "\"", Path)

# def getLog(self, adb_command, Path):
#     GG = adb_commandThread(self, adb_command + " >" + Path)
#     GG.start()
#     # ctypes.pythonapi.PyThreadState_SetAsyncExc(GG._SERIALent, ctypes.py_object(SystemExit))
#     # self.stop_thread(GG)
#     return GG
# def _async_raise(self, t_SERIAL, exctype):
#     """raises the exception, performs cleanup if needed"""
#     t_SERIAL = ctypes.c_long(t_SERIAL)
#     if not inspect.isclass(exctype):
#         exctype = type(exctype)
#     res = ctypes.pythonapi.PyThreadState_SetAsyncExc(t_SERIAL, ctypes.py_object(exctype))
#     if res == 0:
#         raise ValueError("inval_SERIAL thread _SERIAL")
#     elif res != 1:
#         # """if it returns a number greater than one, you're in trouble,
#         # and you should call it again with exc=NULL to revert the effect"""
#         ctypes.pythonapi.PyThreadState_SetAsyncExc(t_SERIAL, None)
#         raise SystemError("PyThreadState_SetAsyncExc failed")

# def stop_thread(self, thread):
#     self._async_raise(thread._SERIALent, SystemExit)

# class adb_commandThread(threading.Thread):  # 继承父类threading.Thread
#     def __init__(self, device, adb_command):
#         threading.Thread.__init__(self)
#         self.device = device
#         self.adb_command = adb_command

#     def run(self):
#         try:
#             print(self.device._SERIAL + "　LogCat...")
#             self.device.adb_command(self.adb_command)
#         except Exception, e:
#             print("Not have connected Device!")
