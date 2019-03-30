# coding=utf-8

"""
 :Decmdion:    命令类
 :author          80071482/bony
 :@version         V1.1
 :@Date            2019年04月
"""

import subprocess
import threading
import queue
import os
import time


class Command(threading.Thread):
    def __init__(self, cmd=None):
        threading.Thread.__init__(self)
        self.result_callback = None
        self.result_queue = queue.Queue()
        if cmd is None:
            self.sp = None
        else:
            self.sp = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, close_fds=True)
        self.exitFlag = True
        self.start()

    def run(self):
        """
        发送结果获取，线程主方法
        :return:
        """
        while self.exitFlag:
            if self.sp is not None:
                try:
                    line = self.sp.stdout.readline().decode("utf-8")
                    if not line:
                        break
                    if not self.result_queue.full():
                        self.result_queue.put(line)
                    if self.result_callback is not None:
                        self.result_callback(line)
                except Exception as e:
                    break
            # print("1:"+str(line))
            # print("2:"+str(self.result_queue.full()))
            # print("3:"+str(self.result_callback))
            # print("4:"+str(self.sp.pid))
        self.close()
        self.exitFlag = False
        self.sp.wait()

    def close(self):
        self.sp.send_signal(subprocess.signal.SIGTERM)
        self.sp.send_signal(subprocess.signal.CTRL_C_EVENT)
        self.sp.send_signal(subprocess.signal.CTRL_BREAK_EVENT)
        while self.sp.poll() is None:
            try:
                self.sp.terminate()
            except Exception as e:
                print(e.args)
        if self.sp.stdin:
            self.sp.stdin.close()
        if self.sp.stdout:
            self.sp.stdout.close()
        if self.sp.stderr:
            self.sp.stderr.close()
        try:
            self.sp.terminate()
            self.sp.kill()
        except OSError:
            pass

    def stop(self):
        """
        停止命令交互
        :return:
        """
        self.exitFlag = False
        self.close()
        self.sp.communicate()

    def read(self):
        """
        读取结果
        :return:结果
        """
        result = ""
        while not self.result_queue.empty() or self.exitFlag:
            # print("5:"+str(self.result_queue.empty()))
            # print("6:"+str(self.exitFlag))
            if not self.result_queue.empty():
                line = self.result_queue.get()
                if line != "\r\n":
                    result += line
        return result

    def read_line(self):
        """
        读取结果
        :return:结果
        """
        result = []
        while not self.result_queue.empty() or self.exitFlag:
            # print("5:"+str(self.result_queue.empty()))
            # print("6:"+str(self.exitFlag))
            if not self.result_queue.empty():
                line = self.result_queue.get()
                if line != "\r\n":
                    result.append(line.replace("\r\n", ""))
        return result

    def close_read(self):
        """
        结束命令线程并读取结果
        :return:读取的命令结果
        """
        self.close()
        return self.read()

    def close_read_line(self):
        """
        结束命令线程并读取结果
        :return:读取的命令结果
        """
        self.close()
        return self.read_line()

    def send(self, cmd):
        """
        发送系统命令
        :param cmd:  命令
        :return: 无
        """
        if self.sp is None:
            self.sp = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, close_fds=True)
        else:
            cmd = (cmd + "\r\n").encode("utf-8")
            self.sp.stdin.write(cmd)
            self.sp.stdin.flush()

    def send_read(self, cmd):
        """
        发送系统命令并获取结果
        :param cmd:  命令
        :return: 命令结果
        """
        if self.sp is None:
            self.sp = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, close_fds=True)
        else:
            cmd = (cmd + "\r\n").encode("utf-8")
            self.send(cmd)
        return self.read()

    def set_callback(self, func):
        """
        回调函数设置
        :param func: 回调函数
        :return: 无
        """
        self.result_callback = func
