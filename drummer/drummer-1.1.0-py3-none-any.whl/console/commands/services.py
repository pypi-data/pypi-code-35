#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from drummer.drummered import Drummered
from sys import path as sys_path
from .base import BaseCommand


class ServiceStart(BaseCommand):

    def __init__(self, config):

        super().__init__(config)


    def execute(self, args):

        config = self.config

        print('Starting Drummer service...')

        try:

            sys_path.append(config['taskdir'])

            drummered = Drummered(config)
            drummered.start()

        except Exception as err:
            print('Impossible to start Drummer service: {0}'.format(str(err)))
