# coding:utf-8

'''
@author = super_fazai
@File    : gevent_utils.py
@connect : superonesfazai@gmail.com
'''

"""
gevent utils
"""

from gevent import sleep as gevent_sleep
from gevent import joinall as gevent_joinall
from gevent import Timeout as GeventTimeout
from gevent.pool import Pool as GeventPool
from gevent import monkey as gevent_monkey
from gevent import (
    Greenlet,
)