#!/usr/bin/python3
# -*- coding: utf-8 -*-
from drummer.utils.clogger import Clogger
from drummer.workers import Runner
from datetime import datetime
import uuid

class TaskManager:
    """ manages tasks to be run """

    def __init__(self, config, **kwargs):

        self.config = config

        # get logger
        self.logger = kwargs.get('logger') or Clogger.get(config)

        # management of runners
        self.execution_data = []


    def run_task(self, queue_tasks_todo):
        """ pick a task from local queue and start runners """

        config = self.config
        logger = self.logger

        max_runners = config['max-runners']

        if not queue_tasks_todo.empty() and len(self.execution_data)<max_runners:

            # pick a task
            task_execution = queue_tasks_todo.get()
            logger.info('Task {0} is going to run with UID {1}'.format(task_execution.task.classname, task_execution.uid))

            # start a new runner for task
            logger.debug('Starting Runner')
            runner = Runner(config, logger, task_execution)

            # get runner queue
            queue_runner_w2m = runner.get_queues()

            # start runner process
            runner.start()

            # get pid
            pid = queue_runner_w2m.get()
            logger.info('Runner successfully started with pid {0}'.format(pid))

            # add task data object
            self.execution_data.append({
                'classname':    task_execution.task.classname,
                'uid':          task_execution.uid,
                'handle':       runner,
                'queue':        queue_runner_w2m,
                'timestamp':    datetime.now(),
                'timeout':      task_execution.task.timeout,
            })

        return queue_tasks_todo


    def load_results(self, queue_tasks_done):
        """ load task result from runners and save to local queue """

        logger = self.logger

        idx_runners_to_terminate = []

        # check tasks executed by runners
        for ii,execution in enumerate(self.execution_data):

            if not execution['queue'].empty():

                # pick the task
                task_result = execution['queue'].get()

                logger.info('Task {0} (UID {1}) ended with result {2}'.format(
                    execution['classname'],
                    execution['uid'],
                    task_result.result.status
                ))

                # update done queue
                queue_tasks_done.put(task_result)

                # prepare runners to clean
                idx_runners_to_terminate.append(ii)

        # clean-up finished runners
        if idx_runners_to_terminate:

            self._cleanup_runners(idx_runners_to_terminate)

        return queue_tasks_done


    def check_timeouts(self):

        logger = self.logger

        for ii,runner_data in enumerate(self.execution_data):

            total_seconds = (datetime.now()-runner_data['timestamp']).total_seconds()

            if (total_seconds > runner_data['timeout']):
                # inserire dati del task
                logger.debug('Timeout exceeded, going to terminate task {0} (UID: {1})'.format(runner_data['classname'], runner_data['uid']))
                self._cleanup_runners([ii])

        return True


    def _cleanup_runners(self, idx_runners_to_terminate):
        """ clean-up: explicitly terminate runner processes and remove their queues """

        # clean handles
        execution_data = []
        for ii,execution in enumerate(self.execution_data):

            if ii in idx_runners_to_terminate:
                execution['handle'].terminate()
                execution['handle'].join()
            else:
                execution_data.append(execution)

        self.execution_data = execution_data

        return


class ManagedTask:
    """ Task instance managed by scheduler """

    def __init__(self, classname, data):

        self.classname = classname
        self.filepath = data['filepath']
        self.timeout = int(data['timeout'])
        self.args = data['args']
        self.on_pipe = data['onPipe']
        self.on_done = data['onSuccess']
        self.on_fail = data['onFail']


class ActiveTask(ManagedTask):
    """ ActiveTask is an active instance of a Task """

    def __init__(self, task, job_name):

        # tasl composition
        self.task = task

        # execution attributes
        self.uid = uuid.uuid4()
        self.related_job = job_name
        self.result = None
