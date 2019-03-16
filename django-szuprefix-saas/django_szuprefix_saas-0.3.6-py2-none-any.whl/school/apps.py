#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:denishuang

from __future__ import unicode_literals

from django.apps import AppConfig


class Config(AppConfig):
    name = 'django_szuprefix_saas.school'
    label = 'school'
    verbose_name = '学校'

    def ready(self):
        super(Config, self).ready()
        from . import receivers