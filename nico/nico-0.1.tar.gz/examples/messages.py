#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time


def test_message1(a='a', b=1):
    return {
        'type': 'MESSAGE1',
        'data': {
            'a': a,
            'b': b
        },
        'created': int(time.time())
    }


def test_message2(a='a', b=1):
    return {
        'type': 'MESSAGE2',
        'data': {
            'a': a,
            'b': b
        },
        'created': int(time.time())
    }
