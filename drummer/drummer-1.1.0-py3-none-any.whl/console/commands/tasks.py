#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from drummer.utils.validation import InquirerValidation
from drummer.utils import ClassLoader, Clogger
from prettytable import PrettyTable
from sys import path as sys_path
from .base import BaseCommand
import inquirer


class TaskExec(BaseCommand):

    def execute(self, command_args):

        config = self.config

        verbosity = command_args['verbosity']

        if verbosity == 0:
            level = 'ERROR'
        elif verbosity == 1:
            level = 'WARNING'
        elif verbosity == 2:
            level = 'INFO'
        else:
            level = 'DEBUG'

        logger = Clogger.get(config, streaming=True, level=level)

        logger.debug('Starting task execution command')

        # add task folder to syspath
        sys_path.append(config['taskdir'])

        # init result table
        result_table = PrettyTable()
        result_table.field_names = ['Response', 'Data']
        result_table.align = 'l'

        # read tasks
        try:
            registered_tasks = config['tasks']

        except:
            msg = 'Unable to read task list'
            logger.error('msg')

        try:

            # task choice
            choices = ['{0} - {1}'.format(tsk['classname'], tsk['description']) for tsk in registered_tasks]

            questions = [
                inquirer.List('task',
                      message = 'Select task to execute',
                      choices = choices,
                      carousel = True,
                  ),
                  inquirer.Text(
                      'arg_list',
                      message = 'Arguments (comma-separated list of key=value)',
                      default = None
                  ),
            ]

            ans = inquirer.prompt(questions)

            # chosen task
            choice_idx = choices.index(ans['task'])

            task_to_run = registered_tasks[choice_idx]

            classname = task_to_run['classname']
            filepath = task_to_run['filepath']

            # task arguments
            task_args = InquirerValidation.get_dict_from_args(ans['arg_list'])

            # loading task class
            RunningTask = ClassLoader().load(filepath, classname)

            # task execution
            running_task = RunningTask(config, logger)
            response = running_task.run(task_args)

        except Exception as err:
            logger.error('Impossible to execute task: {0}'.format(str(err)))

        else:

            logger.debug('Task has terminated')

            result_table.add_row(['Status', response.status])

            for k,v in response.data.items():

                result_table.add_row([k, v])

            print(result_table)
            print()

        return


class TaskList(BaseCommand):

    def execute(self, command_args):

        config = self.config

        # add task folder to syspath
        sys_path.append(config['taskdir'])

        table = PrettyTable()
        table.field_names = ['No.', 'Name', 'Description']
        table.align['Name'] = 'l'
        table.align['Description'] = 'l'

        try:
            registered_tasks = config['tasks']

            print('\nList of registered tasks:')

            for ii,tsk in enumerate(registered_tasks):
                table.add_row([ii, tsk['classname'], tsk['description']])
            print(table)
            print()

        except:
            raise Exception('unable to load task list')

        return None
