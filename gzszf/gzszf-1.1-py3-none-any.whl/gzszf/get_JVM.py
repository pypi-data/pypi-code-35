# -*- coding: utf-8 -*- 
# @Time : 2019/4/4 15:46 
# @Author : Allen 
# @Site :  打开jvm，调用jar包
import jpype
from gzszf.config import JVMPath


class JRun(object):
    def __init__(self):
        self.JVMPath = self.get_JVM_path()

    def get_JVM_path(self):
        try:
            _JVMPath = jpype.getDefaultJVMPath()
        except:
            _JVMPath = JVMPath
        return _JVMPath

    def startJVM(self, jar_path):
        jpype.startJVM(self.JVMPath, "-Xms32m", "-Xmx256m", "-mx256m", "-Djava.class.path={}".format(jar_path))

    def shutdownJVM(self):
        jpype.shutdownJVM()

    def get_jclass(self, class_path):
        jClass = jpype.JClass(class_path)
        return jClass
