#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from drummer.sockets.server import SocketServer
from multiprocessing import Process, Queue
from os import getpid as os_getpid


class Listener(Process):
    """ This worker starts socket server """

    def __init__(self, config):

        super().__init__()

        self.config = config

        # queue worker -> master
        self.queue_w2m = Queue(1)
        # queue master -> worker
        self.queue_m2w = Queue(1)


    def get_queues(self):
        return self.queue_w2m, self.queue_m2w


    def run(self):

        # get pid and send to master
        pid = os_getpid()
        self.queue_w2m.put(pid)

        # begin working
        self.work()


    def work(self):

        # run socket server
        server = SocketServer(self.config, self.queue_w2m, self.queue_m2w)

        server.run()
