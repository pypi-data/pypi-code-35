# -*- conding:utf-8 -*-
"""日期助手"""
import re
import time


def parse(txt):
    """解析日期字符串
    支持格式：2019-03-26 12:34:56
        2019-03-26 12:34
        2019-03-26
    """

    if txt:
        if re.match(r'^\d{4}(\-\d{1,2}){2}\s\d{1,2}(:\d{1,2}){2}$', txt):
            return time.strptime(txt, r'%Y-%m-%d %H:%M:%S')
        elif re.match(r'^\d{4}(\-\d{1,2}){2}\s\d{1,2}:\d{1,2}$', txt):
            return time.strptime(txt, r'%Y-%m-%d %H:%M')
        elif re.match(r'^\d{4}(\-\d{1,2}){2}$', txt):
            return time.strptime(txt, r'%Y-%m-%d')


def format(date, formatstr=None):
    """日期格式化"""

    if not formatstr:
        formatstr = r'%Y-%m-%d'

    if date:
        return time.strftime(formatstr, date)




