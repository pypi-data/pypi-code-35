#!/usr/bin/env python

from argparse import ArgumentParser

from pgstatus.configuration import DEFAULT_CONFIG_PATH
from pgstatus.server import StatusMonitoringServer


def main():
    parser = ArgumentParser()
    parser.add_argument('-c', '--configuration', default=DEFAULT_CONFIG_PATH, help='Configuration file path')
    parser.add_argument('-d', '--database', help='Database name')
    args = parser.parse_args()

    StatusMonitoringServer(args.database, args.configuration).run()


if __name__ == '__main__':
    main()
