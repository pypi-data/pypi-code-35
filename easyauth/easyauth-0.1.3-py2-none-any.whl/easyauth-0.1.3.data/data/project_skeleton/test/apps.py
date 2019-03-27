# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os.path import abspath, basename, dirname
from django.apps import AppConfig


APP_NAME = basename(dirname(abspath(__file__)))


class MyAppConfig(AppConfig):
    name = '%s' % APP_NAME
