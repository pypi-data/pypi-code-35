#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys

logging.basicConfig(level=logging.INFO)
sys.path.append(os.path.abspath('.'))

from nico.consumer import Consumer
from nico.utils import load_modules
from nico.load_settings import load_settings


def main():
    settings = load_settings()
    topic = settings['topic']
    consumer_group = settings['consumer_group']
    jobspath = settings['jobspath']
    load_modules(jobspath)
    consumer = Consumer(topic, consumer_group, settings)
    consumer.run()


if __name__ == '__main__':
    """ python examples/main.py -t default -g test -c examples/config.json """
    main()
