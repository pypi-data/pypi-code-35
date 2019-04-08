#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 jack <jack@iOSTdeMacBook-Pro.local>
#
# Distributed under terms of the MIT license.

"""
test
"""

import boto3, sys
import time,click

from idevops import aws
from idevops.utils import *

name = 'example'


def main():
    data = [
        {
            'a': 1,
            'b': 2,
            'c': 3,
        },
        {
            'a': 4,
            'b': 5,
            'c': 6
        }]

    with click.progressbar(data, label='Gathering ec2 info:'.ljust(25)) as bar:
        for ec in bar:
            time.sleep(1)

    sys.stdout.write('\033[F\033[K')
    print_table(data, ['a','b','c'])

if __name__ == "__main__":
    main()
