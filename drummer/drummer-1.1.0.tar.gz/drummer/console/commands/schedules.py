#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from drummer.utils.validation import InquirerValidation
from drummer.foundation import Request, StatusCode
from drummer.sockets.client import SocketClient
from prettytable import PrettyTable
from .base import RemoteCommand
import inquirer
import json


class ScheduleList(RemoteCommand):

    def __init__(self, config):

        super().__init__(config)


    def execute(self, command_args):

        config = self.config

        # test socket connection
        self.test_socket_connection()

        # init result table
        table = PrettyTable()
        table.field_names = ['ID', 'Name', 'Description', 'Cronexp', 'Enabled']
        table.align['Name'] = 'l'
        table.align['Description'] = 'l'
        table.align['Cronexp'] = 'l'

        # handle command parameters
        # command_args = request.args
        # ...

        # prepare request to listener
        request = Request()
        request.set_classname('ScheduleListEvent')
        request.set_classpath(self.CLASSPATH)

        # send request to listener
        sc = SocketClient(config)
        response = sc.send_request(request)

        if response.status == StatusCode.STATUS_OK:

            schedule_list = response.data['Result']

            print('\nScheduled jobs:')

            for s in schedule_list:

                uid = s.get('id')
                name = s.get('name')
                description = s.get('description')
                cronexp = s.get('cronexp')
                enabled = s.get('enabled')

                table.add_row([uid, name, description, cronexp, enabled])

            print(table)
            print()

        else:
            print('Impossible to execute the command')


class ScheduleAdd(RemoteCommand):

    def __init__(self, config):

        super().__init__(config)


    def execute(self, command_args):

        config = self.config

        # handle command parameters
        # ...

        # test socket connection
        self.test_socket_connection()

        registered_tasks = config['tasks']

        schedulation = self.ask_basics()

        # get schedulation data from the user
        schedulation['parameters'] = self.set_schedulation_parameters(registered_tasks)

        # prepare request to listener
        request = Request()
        request.set_classname('ScheduleAddEvent')
        request.set_classpath(self.CLASSPATH)
        request.set_data(schedulation)

        # send request to listener
        sc = SocketClient(config)
        response = sc.send_request(request)

        print('Result: {0} -> {1}'.format(response.status, response.data))

        return


    def ask_basics(self):

        questions = [
            inquirer.Text(
                'name',
                message = 'Name of schedule'
            ),
            inquirer.Text(
                'description',
                message = 'Description of schedule',
            ),
            inquirer.Text(
                'cronexp',
                message = 'Cron expression',
                validate = InquirerValidation.check_cron,
            ),
            inquirer.Confirm(
                'enabled',
                message = 'Enable the job?',
                default = True,
            )
        ]

        schedulation = inquirer.prompt(questions)

        return schedulation


    def set_task(self, registered_tasks, schedulation_parameters):

        classnames = [tsk['classname'] for tsk in registered_tasks]

        # select a task
        choices = ['{0} - {1}'.format(tsk['classname'], tsk['description']) for tsk in registered_tasks]

        questions = [
            inquirer.List('task',
                  message = 'Select task to execute',
                  choices = choices,
                  carousel = True,
              ),
              inquirer.Text(
                  'timeout',
                  message = 'Timeout',
                  default = '600',
                  validate = InquirerValidation.check_int
              ),
              inquirer.Text(
                  'arg_list',
                  message = 'Arguments (comma-separated list of key=value)',
                  default = None
              ),
        ]

        ans = inquirer.prompt(questions)

        task_idx = choices.index(ans['task'])

        task_to_run = registered_tasks[task_idx]

        classname = task_to_run['classname']

        # set task data
        task = {}
        task['filepath'] = task_to_run['filepath']
        task['timeout'] = ans['timeout']
        task['args'] = InquirerValidation.get_dict_from_args(ans['arg_list'])
        task['onPipe'] = None
        task['onSuccess'] = None
        task['onFail'] = None

        schedulation_parameters['tasklist'][classname] = task

        return schedulation_parameters, classname


    def set_connection(self, registered_tasks, parameters, base_task):

        question_pipe = [
            inquirer.Confirm('onPipe',
                message = '[{0}] Do you want to pipe another task?'.format(base_task),
                default = False,
            )
        ]
        question_success = [
            inquirer.Confirm('onSuccess',
                message = '[{0}] Do you want to execute another task on success?'.format(base_task),
                default = False,
            )
        ]
        question_fail = [
            inquirer.Confirm('onFail',
                message = '[{0}] Do you want to execute another task on fail?'.format(base_task),
                default = False,
            )
        ]

        ans = inquirer.prompt(question_pipe)

        if ans['onPipe']:
            parameters, next_task = self.set_task(registered_tasks, parameters)
            parameters['tasklist'][base_task]['onPipe'] = next_task
            parameters = self.set_connection(registered_tasks, parameters, next_task)

        ans = inquirer.prompt(question_success)

        if ans['onSuccess']:
            parameters, next_task = self.set_task(registered_tasks, parameters)
            parameters['tasklist'][base_task]['onSuccess'] = next_task
            parameters = self.set_connection(registered_tasks, parameters, next_task)

        ans = inquirer.prompt(question_fail)

        if ans['onFail']:
            parameters, next_task = self.set_task(registered_tasks, parameters)
            parameters['tasklist'][base_task]['onFail'] = next_task
            parameters = self.set_connection(registered_tasks, parameters, next_task)

        return parameters


    def set_schedulation_parameters(self, registered_tasks):

        schedulation_parameters = {'tasklist': {}}

        # get a task and set connections
        schedulation_parameters, classname = self.set_task(registered_tasks, schedulation_parameters)

        schedulation_parameters['root'] = classname
        schedulation_parameters = self.set_connection(registered_tasks, schedulation_parameters, classname)

        # serialize to json
        schedulation_parameters = json.dumps(schedulation_parameters)

        return schedulation_parameters


class ScheduleRemove(RemoteCommand):

    def __init__(self, config):

        super().__init__(config)


    def execute(self, command_args):

        config = self.config

        # test socket connection
        self.test_socket_connection()

        # prepare request to listener
        request = Request()
        request.set_classname('ScheduleRemoveEvent')
        request.set_classpath(self.CLASSPATH)
        request.set_data(command_args)

        # send request to listener
        sc = SocketClient(config)
        response = sc.send_request(request)

        print('Result: {0} -> {1}'.format(response.status, response.data))

        return


class ScheduleEnable(RemoteCommand):

    def __init__(self, config):

        super().__init__(config)


    def execute(self, command_args):

        config = self.config

        # test socket connection
        self.test_socket_connection()

        # prepare request to listener
        request = Request()
        request.set_classname('ScheduleEnableEvent')
        request.set_classpath(self.CLASSPATH)
        request.set_data(command_args)

        # send request to listener
        sc = SocketClient(config)
        response = sc.send_request(request)

        print('Result: {0} -> {1}'.format(response.status, response.data))

        return


class ScheduleDisable(RemoteCommand):

    def __init__(self, config):

        super().__init__(config)


    def execute(self, command_args):

        config = self.config

        # test socket connection
        self.test_socket_connection()

        # prepare request to listener
        request = Request()
        request.set_classname('ScheduleDisableEvent')
        request.set_classpath(self.CLASSPATH)
        request.set_data(command_args)

        # send request to listener
        sc = SocketClient(config)
        response = sc.send_request(request)

        print('Result: {0} -> {1}'.format(response.status, response.data))

        return


class ScheduleExec(RemoteCommand):

    def __init__(self, config):

        super().__init__(config)


    def execute(self, command_args):

        config = self.config

        # test socket connection
        self.test_socket_connection()

        # prepare request to listener
        request = Request()
        request.set_classname('ScheduleExecEvent')
        request.set_classpath(self.CLASSPATH)
        request.set_data(command_args)

        # send request to listener
        sc = SocketClient(config)
        response = sc.send_request(request)

        print('Result: {0} -> {1}'.format(response.status, response.data))

        return


class ScheduleGet(RemoteCommand):

    def __init__(self, config):

        super().__init__(config)


    def execute(self, command_args):

        config = self.config

        # test socket connection
        self.test_socket_connection()

        # init overview table
        table_overview = PrettyTable()
        table_overview.field_names = ['ID', 'Name', 'Description', 'Cronexp', 'Enabled']
        table_overview.align['Name'] = 'l'
        table_overview.align['Description'] = 'l'
        table_overview.align['Cronexp'] = 'l'

        # init task table
        table_task = PrettyTable()
        table_task.field_names = ['No.', 'Task', 'Filepath', 'Timeout', 'Args', 'onPipe', 'onSuccess', 'onFail']
        table_task.align = 'l'

        # prepare request to listener
        request = Request()
        request.set_classname('ScheduleGetEvent')
        request.set_classpath(self.CLASSPATH)
        request.set_data(command_args)

        # send request to listener
        sc = SocketClient(config)
        response = sc.send_request(request)

        if response.status == StatusCode.STATUS_OK:

            schedule_info = response.data['Result']

            uid = schedule_info.get('id')
            name = schedule_info.get('name')
            description = schedule_info.get('description')
            cronexp = schedule_info.get('cronexp')
            enabled = schedule_info.get('enabled')

            table_overview.add_row([uid, name, description, cronexp, enabled])

            print()
            print('Job overview:')
            print(table_overview)
            print()

            job_parameters = json.loads(schedule_info.get('parameters'))

            for ii,(task_name,task_params) in enumerate(job_parameters['tasklist'].items()):

                if (task_name==job_parameters['root']): task_name = task_name+'*'

                filepath = task_params['filepath']
                timeout = task_params['timeout']
                args = task_params['args']
                onPipe = task_params['onPipe']
                onSuccess = task_params['onSuccess']
                onFail = task_params['onFail']

                table_task.add_row([ii, task_name, filepath, timeout, args, onPipe, onSuccess, onFail])

            print('Job tasks:')
            print(table_task)
            print(' *Root task')
            print()

        else:
            print('Impossible to get schedule info')
