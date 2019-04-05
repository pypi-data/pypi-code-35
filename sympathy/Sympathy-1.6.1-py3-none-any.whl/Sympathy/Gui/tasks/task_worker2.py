# This file is part of Sympathy for Data.
# Copyright (c) 2016 System Engineering Software Society
#
# Sympathy for Data is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sympathy for Data is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sympathy for Data.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import absolute_import, unicode_literals, print_function
import logging
import os
import signal
import json
import base64
import threading
import psutil
import time
import socket


core_logger = logging.getLogger('core')
(NEW_TASK, NEW_QUIT_TASK, UPDATE_TASK, QUIT_TASK, ABORT_TASK,
 DONE_TASK, SET_WORKERS_TASK, WORKER_CONNECTED) = range(8)


def readlines_fd(fd, bufl):
    return datalines(os.read(fd, 2048), bufl)


def setup_socket(sock):
    if sock:
        try:
            sock.setsockopt(
                socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        except AttributeError:
            pass
        try:
            sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        except AttributeError:
            pass


class CommunicationHelper(object):

    def __init__(self, port, pid, socket, taskid):
        # Port and pid might be useful to format temporary debug messages.
        self._port = port
        self._pid = pid
        self._socket = socket
        self._taskid = taskid

    @property
    def socket(self):
        return self._socket

    def output_func(self, msg):
        """
        Format an update message for sending to output socket.
        """
        return encode_json([self._taskid, UPDATE_TASK, msg.to_dict()]) + b'\n'

    def result_func(self, msg):
        """
        Format a done message for sending to output socket.
        """
        return encode_json([self._taskid, DONE_TASK, msg.to_dict()]) + b'\n'


def killer(ppid):
    while True:
        if not psutil.pid_exists(ppid):
            os.kill(os.getpid(), signal.SIGTERM)
        time.sleep(0.2)


def _conn_func(pid, prev_taskid):
    return encode_json([prev_taskid, WORKER_CONNECTED, pid]) + b'\n'


def worker(function, port, ppid, nocapture):
    ipipebuf = []
    taskid = -1
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    pid = os.getpid()
    quit_after = [False]

    def get_msgs():
        lines = readlines_fd(0, ipipebuf)
        return [decode_json(line) for line in lines]

    def read_task(file_obj):
        line = file_obj.readline().rstrip()
        msg = decode_json(line)
        return msg

    killer_thread = threading.Thread(target=killer, args=(ppid,))
    killer_thread.daemon = True
    killer_thread.start()

    quit_after = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", port))
    setup_socket(sock)

    while not quit_after:

        msg_in = None
        try:
            sock.setblocking(True)
            sock.send(_conn_func(pid, taskid))
            msg_in = sock.makefile(mode='rb')

            # Get new task, discarding any other messages.
            taskid_new, cmd, data = read_task(msg_in)
            while cmd not in [NEW_TASK, NEW_QUIT_TASK]:
                taskid_new, cmd, data = read_task(msg_in)

            quit_after = cmd == NEW_QUIT_TASK
            taskid = taskid_new
            io_bundle = CommunicationHelper(port, pid, sock, taskid)
            function(io_bundle, nocapture, *data)
        finally:
            if msg_in is not None:
                msg_in.close()
                msg_in = None


def datalines(data, bufl):
    i = data.rfind(b'\n')
    if i >= 0:
        bufl.append(data[:i])
        sdata = b''.join(bufl)
        bufl[:] = [data[i + 1:]]
        lines = sdata.split(b'\n')
        return [line.strip() for line in lines]
    else:
        bufl.append(data)
    return []


def get_msgs(lines):
    return [decode_json(line) for line in lines]


def decode_json(str_):
    return json.loads(base64.b64decode(str_).decode('ascii'))


def encode_json(dict_):
    return base64.b64encode(json.dumps(dict_).encode('ascii'))


def main():
    import argparse
    from Gui.tasks import task_worker_subprocess
    from Gui import log
    task_worker_subprocess.set_high_dpi_unaware()
    task_worker_subprocess.set_shared_opengl_contexts()

    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int)
    parser.add_argument('parent_pid', type=int)
    parser.add_argument('loglevel', type=int)
    parser.add_argument('node_loglevel', type=int)
    parser.add_argument('nocapture', type=int)
    (parsed, _) = parser.parse_known_args()
    log.setup_loglevel(parsed.loglevel, parsed.node_loglevel)

    worker(
        task_worker_subprocess.worker, parsed.port, parsed.parent_pid,
        parsed.nocapture)


if __name__ == '__main__':
    main()
