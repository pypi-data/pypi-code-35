#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nico.register import on
from nico.consts import DEFAULT_TOPIC


@on('MESSAGE2', DEFAULT_TOPIC)
def test(data):
    print('test', data)


@on('MESSAGE2', DEFAULT_TOPIC)
def test2(data):
    print('test2', data)


@on('MESSAGE2', DEFAULT_TOPIC)
def test3(data):
    return 1 / 0
