#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from drummer.utils.classloader import ClassLoader
from multiprocessing import Process, Queue
from os import getpid as os_getpid
from os import path

class Runner(Process):
    """ This worker executes commands and tasks """

    def __init__(self, config, logger, task_execution):

        # worker init
        super().__init__()

        # queue worker -> master
        self.queue_w2m = Queue(1)

        self.config = config
        self.logger = logger

        self.task_execution = task_execution


    def get_queues(self):
        #return self.queue_w2m, self.queue_m2w
        return self.queue_w2m


    def run(self):

        # get pid and send to master
        pid = os_getpid()
        self.queue_w2m.put(pid)

        # begin working
        self.work()


    def work(self):

        config = self.config
        logger = self.logger

        # get shared queues
        queue_w2m = self.queue_w2m

        # get the task to exec
        task_execution = self.task_execution

        # load class to exec
        classname = task_execution.task.classname
        filepath = task_execution.task.filepath

        timeout = task_execution.task.timeout
        args = task_execution.task.args

        # loading task class
        RunningTask = ClassLoader().load(filepath, classname)

        # task execution
        running_task = RunningTask(config, logger)
        task_result = running_task.run(args)

        task_execution.result = task_result

        # queue_done
        queue_w2m.put(task_execution)

        return
