# -*- coding: utf-8 -*-
""" Basic find program, cut-down version of unix 'find'
Walks a file hierarchy

find . -name '*.txt'
find temp -type f
find . -type d
"""

import argparse
from pathlib import Path
import logging

LOGGING_FORMAT = '%(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
logging.basicConfig(format=LOGGING_FORMAT, datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def find_name(path, name):
    """docstring for find_name"""
    for filename in path.rglob(name):
        print(filename)


def type_find(path, args):
    """docstring for type_find"""
    for filename in path.rglob(args.name or '*'):
        if args.type == 'f' and filename.is_file():
            print(filename)
        elif args.type == 'd' and filename.is_dir():
            print(filename)


def find_files(args):
    """docstring for find_files"""
    the_path = Path(args.path)
    if args.name and not args.type:
        find_name(the_path, args.name)
    else:
        type_find(the_path, args)


def parse_args():
    """docstring for parse_args"""
    parser = argparse.ArgumentParser(description='Walk a file hierarchy')
    parser.add_argument('path', type=str, help='Path of search')
    parser.add_argument('-name', type=str, help='Name of file or directory')
    parser.add_argument(
        '-type', choices=['f', 'd'], type=str,
        help='Specify the type, f for files, d for directories')
    args = parser.parse_args()
    LOGGER.debug(args)
    return args


def main():
    """docstring for main"""
    args = parse_args()
    find_files(args)


if __name__ == '__main__':
    main()
