# -*- coding: utf-8 -*-

# @Date    : 2019-03-11
# @Author  : Peng Shiyu

from __future__ import unicode_literals, print_function
import paramiko


class SSHClient(object):
    """
    简易的ssh 客户端
    """

    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.ssh = None
        self._connect()

    def __del__(self):
        self.ssh.close()

    def _connect(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.hostname, username=self.username, password=self.password)

    def execute_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        stdout = stdout.read().decode("utf-8")
        stderr = stderr.read().decode("utf-8")
        return stdout, stderr


if __name__ == '__main__':
    ssh_client = SSHClient(
        hostname="hostname",
        username="username",
        password="password"
    )
    stdout, stderr = ssh_client.execute_command("cd / && ls")
