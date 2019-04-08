#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sys import exit as sys_exit
from sys import argv as sys_argv
import argparse

class ArgParser:

    def process(self, sys_argv):

        if len(sys_argv)==1:
            print('Command missing. See -h for usage.')
            sys_exit()

        parser = self.define_parsers()
        args = vars(parser.parse_args(sys_argv[1:]))

        classname = args.get('classname')
        del args['classname']

        return classname, args


    def define_parsers(self):

        # create the top-level parser
        parser = argparse.ArgumentParser(prog='Drummer')

        # add subparsers
        subparsers = parser.add_subparsers(help='command help', title='Commands', description='Console operations', metavar='')

        # service:start
        parser_00 = subparsers.add_parser('service:start', help='Start drummer service')
        parser_00.set_defaults(classname='ServiceStart')

        # task:list
        parser_01 = subparsers.add_parser('task:list', help='List available tasks')
        parser_01.set_defaults(classname='TaskList')

        # task:exec
        parser_02 = subparsers.add_parser('task:exec', help='Execute a task')
        parser_02.add_argument('-v', '--verbosity', help = 'increase output verbosity', action = 'count', default = 0)
        parser_02.set_defaults(classname='TaskExec')

        # schedule:list
        parser_03 = subparsers.add_parser('schedule:list', help='List aviable schedules')
        parser_03.set_defaults(classname='ScheduleList')

        # schedule:add
        parser_04 = subparsers.add_parser('schedule:add', help='Add a new schedule')
        parser_04.set_defaults(classname='ScheduleAdd')

        # schedule:remove
        parser_05 = subparsers.add_parser('schedule:remove', help='Remove a schedule')
        parser_05.add_argument('schedule_id', action='store', help='ID of schedule to remove')
        parser_05.set_defaults(classname='ScheduleRemove')

        # schedule:enable
        parser_06 = subparsers.add_parser('schedule:enable', help='Enable a schedule')
        parser_06.add_argument('schedule_id', action='store', help='ID of schedule to enable')
        parser_06.set_defaults(classname='ScheduleEnable')

        # schedule:disable
        parser_07 = subparsers.add_parser('schedule:disable', help='Disable a schedule')
        parser_07.add_argument('schedule_id', action='store', help='ID of schedule to disable')
        parser_07.set_defaults(classname='ScheduleDisable')

        # schedule:exec
        parser_08 = subparsers.add_parser('schedule:exec', help='Execute immediately a schedule')
        parser_08.add_argument('schedule_id', action='store', help='ID of schedule to execute')
        parser_08.set_defaults(classname='ScheduleExec')

        # schedule:get
        parser_09 = subparsers.add_parser('schedule:get', help='Get information about a schedule')
        parser_09.add_argument('schedule_id', action='store', help='ID of schedule to get info about')
        parser_09.set_defaults(classname='ScheduleGet')

        return parser
