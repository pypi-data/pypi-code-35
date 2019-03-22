#!/usr/bin/env python3

import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, ArgumentTypeError
from datetime import date, datetime, timedelta

# from argcomplete import autocomplete
from dateutil.parser import parse

from pomw.exceptions import (
    ArgumentException,
    EntryFoundException,
    IntervalIDException,
    IntervalModificationException,
    IntervalRangeException,
    IntervalTimeException,
    TaskNotFoundException,
    TimewIntervalNotFoundException,
)
from pomw.tasks import Tasks


class Application:
    def valid_date(self, s):
        try:
            return parse(s).date()
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(s)
            raise ArgumentTypeError(msg)

    def valid_datetime(self, s):
        try:
            return parse(s)
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(s)
            raise argparse.ArgumentTypeError(msg)

    def create_parser(self, program_bin):
        parser = ArgumentParser(
            prog=program_bin, formatter_class=ArgumentDefaultsHelpFormatter
        )
        # autocomplete(parser)
        subparsers = parser.add_subparsers(dest="action")

        plan_parser = subparsers.add_parser(
            "plan",
            help="Plan a pomodoro",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        plan_parser.add_argument("task", help="Task id", type=int)
        plan_parser.add_argument(
            "-q",
            "--quantity",
            default="+1",
            help="The number of pomodoros (default: +1)",
            type=str,
        )
        plan_parser.add_argument(
            "-d", "--date", default=date.today(), help="The date", type=self.valid_date
        )

        complete_parser = subparsers.add_parser(
            "done",
            help="Complete a pomodoro",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        complete_parser.add_argument("task", help="Task id", type=int)
        complete_parser.add_argument(
            "-e",
            "--end_time",
            help="The end time for the pomodoro",
            default=(datetime.now()).strftime("%Y-%m-%dT%H:%M:%S"),
            type=self.valid_datetime,
        )

        void_parser = subparsers.add_parser(
            "void",
            help="Void a pomodoro",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        void_parser.add_argument("task", help="Task id", type=int)
        void_parser.add_argument(
            "-d", "--date", default=date.today(), help="The date", type=self.valid_date
        )

        #       pom interrupt [internal|external] Mark an interruption for the current pomodoro
        interrupt_parser = subparsers.add_parser(
            "interrupt", help="Interrupt the current pomodoro"
        )
        interrupt_parser.add_argument(
            "type",
            default="internal",
            help="The interruption type",
            choices=["internal", "external"],
        )
        interrupt_parser.add_argument("task", help="Task id", type=int)
        interrupt_parser.add_argument(
            "-t",
            "--time",
            default=(datetime.now()).strftime("%Y-%m-%dT%H:%M:%S"),
            help="The interruption time",
            type=self.valid_datetime,
        )
        interrupt_parser.add_argument(
            "-q",
            "--quantity",
            default="+1",
            help="The number of interruptions (default: +1)",
            type=str,
        )

        list_parser = subparsers.add_parser(
            "ls", help="List intervals", formatter_class=ArgumentDefaultsHelpFormatter
        )
        list_parser.add_argument(
            "-d",
            "--date",
            help="The date for entries",
            default=(datetime.now()).strftime("%Y-%m-%d"),
            type=self.valid_date,
        )

        nonpom_parser = subparsers.add_parser(
            "add",
            help="Add a time interval",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        nonpom_parser.add_argument("task", help="Task id", type=int)
        nonpom_parser.add_argument(
            "-s",
            "--start_time",
            help="The start time for the time entry. If both END_TIME and DURATION \
    is given, START_TIME gets ignored",
            type=self.valid_datetime,
        )
        nonpom_parser.add_argument(
            "-e",
            "--end_time",
            help="The end time for the time entry",
            default=(datetime.now()).strftime("%Y-%m-%dT%H:%M:%S"),
            type=self.valid_datetime,
        )
        nonpom_parser.add_argument(
            "-d",
            "--duration",
            help="The duration for the time entry in minutes.",
            default=30,
            type=int,
        )

        modify_parser = subparsers.add_parser(
            "mod",
            help="Modify an interval",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        modify_parser.add_argument("interval", help="Interval id", type=str)
        modify_parser.add_argument(
            "-s",
            "--start_time",
            help="The new start time for the interval",
            type=self.valid_datetime,
        )
        modify_parser.add_argument(
            "-e",
            "--end_time",
            help="The new end time for the interval",
            type=self.valid_datetime,
        )

        move_parser = subparsers.add_parser(
            "mv", help="Move an interval", formatter_class=ArgumentDefaultsHelpFormatter
        )
        move_parser.add_argument("interval", help="Interval id", type=str)
        move_parser.add_argument(
            "-s",
            "--start_time",
            help="The new start time for the interval",
            type=self.valid_datetime,
        )

        remove_parser = subparsers.add_parser(
            "rm",
            help="Remove an interval",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        remove_parser.add_argument("interval", help="Interval id", type=str)

        # start_parser = subparsers.add_parser('start',
        #                                      help='Start a new pomodoro')
        # start_parser.add_argument('task',
        #                           help='Task id',
        #                           type=int)

        tdt_parser = subparsers.add_parser(
            "tdt",
            help="Print To Do Today sheet",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        tdt_parser.add_argument(
            "-d",
            "--date",
            help="Date to print",
            default=datetime.now().strftime("%Y-%m-%d"),
            type=self.valid_date,
        )

        return parser

    def run(self):
        try:
            tasks = Tasks()
            parser = self.create_parser(sys.argv[0])
            args = parser.parse_args(sys.argv[1:])
            action = args.action
            kwargs = vars(args)
            # del kwargs['action']
            if not action:
                parser.print_help(file=None)
            else:
                method_to_call = getattr(tasks, action)
                result = method_to_call(**kwargs)
        except (
            IntervalIDException,
            IntervalModificationException,
            IntervalRangeException,
            IntervalTimeException,
            TaskNotFoundException,
            TimewIntervalNotFoundException,
            EntryFoundException,
            ArgumentException,
        ) as e:
            print("Error: %s" % (e), file=sys.stderr)
            exit(1)
