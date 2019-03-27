#! /usr/local/bin/python3
# encoding: utf-8
# Author: LiTing

import os
import sys
import getopt
from utils import *


"""
USAGE
    
    python3 exector.py [-s <string>] [-h]
    e.g.
        python3 exector.py -s 'Hi, LT'
    
    
SUPPORT FUNCTIONS
    
    1. 输入-处理-输出
    
    
SUPPORT OPTIONS
    
    -s, --string
        [Optional] Input msg
    
    -h, --help
        [Optional] Show this USAGE and exit.
"""


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 's:h', ['string', 'help'])
    except getopt.GetoptError:
        warning(__doc__)
        sys.exit(2)

    global out_put

    for opt, arg in opts:
        if opt in {'-s', '--string'}:
            out_put = arg
        elif opt in {'-h', '--help'}:
            usage(__doc__)
            return

    __do_exec()


out_put = 'hello world'


def __do_exec():
    PrintWithColor.black('').fore_green().style_underline().apply(f'{out_put}', end='\n\n')


if __name__ == '__main__':
    main(sys.argv[1:])
