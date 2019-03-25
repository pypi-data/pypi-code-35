#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Version : python3.6
@Author  : LiuSQ
@Time    : 2019/3/25 9:16
@Describe: 
"""

import paramiko


class SSH:
    """
        ssh方式上传文件至linux工具类
    """

    def __init__(self, ip="", port=22):
        self.transport = paramiko.Transport((ip, port))
        self.ssh = None

    def login(self, username="", password=""):
        """
            登录linux
        :param username:
        :param password:
        """
        self.transport.connect(username=username, password=password)
        self.ssh = paramiko.SFTPClient.from_transport(self.transport)

    def upload_file(self, local_path="", linux_path=""):
        """
            上传文件至linux
        :param local_path:
        :param linux_path:
        """
        self.ssh.remove(linux_path)
        print("移除" + linux_path)
        self.ssh.put(local_path, linux_path)

    def close_ssh(self):
        """
            关闭ssh连接
        """
        self.transport.close()
