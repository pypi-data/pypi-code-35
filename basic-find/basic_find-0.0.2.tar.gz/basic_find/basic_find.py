# -*- coding: utf-8 -*-
"""
Basic find program, cut-down version of unix 'find'
Walks a file hierarchy

find . -name '*.txt'
find temp -type f
find . -type d

todo:
find . -name '*.rb' -exec rm {} \;
"""

import os
import argparse
from pathlib import Path
from sys import exit
import logging

from pprint import pprint

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def find_name(p, name):
    """docstring for find_name"""
    for f in p.rglob(name):
        print(f)


def type_find(p, args):
    """docstring for type_find"""
    for f in p.rglob(args.name or '*'):
        if args.type == 'f' and f.is_file():
            print(f)
        elif args.type == 'd' and f.is_dir():
            print(f)


def find_files(args):
    """docstring for find_files"""
    p = Path(args.path)
    if args.name and not args.type:
        find_name(p, args.name)
    else:
        type_find(p, args)


def parse_args():
    """docstring for parse_args"""
    parser = argparse.ArgumentParser(description='Walk a file hierarchy')
    parser.add_argument('path', type=str, help='Path of search')
    parser.add_argument('-name', type=str, help='Name of file or directory')
    parser.add_argument(
        '-type', choices=['f', 'd'], type=str, help='Specify the type, f for files, d for directories')
    args = parser.parse_args()
    logger.debug(args)
    return args

def main():
    """docstring for main"""
    args = parse_args()
    find_files(args)



if __name__ == '__main__':
    main()
