#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Nico

Usage:
    test_job1.py -c file -t topic -g group
    test_job1.py -h

Options:
    -h --help       show this
    -v --version    show version
    -t topic        kafka topic
    -g group        kafka consumer group
    -c file         config file name

config file:
    {
        "jobspath": "",
        "kafka_hosts": ""
    }
"""

import json

from docopt import docopt


def load_settings():
    arguments = docopt(__doc__, version='Nico 0.1')
    filename = arguments['-c']
    json_config = json.load(file(filename))
    settings = {
        'topic': arguments['-t'],
        'consumer_group': arguments['-g'],
        'kafka_hosts': json_config['kafka_hosts'],
        'jobspath': json_config['jobspath']
    }
    return settings
