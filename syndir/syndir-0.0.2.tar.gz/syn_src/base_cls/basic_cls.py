# coding:utf-8
"""
author: sixi
datetime: 
python version: 3.x
summary: 
install package:
"""
import traceback


class BaseCls(object):
    def __init__(self):
        pass

    @staticmethod
    def exec_func(func, *args, **kwargs) -> tuple:
        """执行函数，如果成功则返回True/msg，否则返回False/msg"""
        try:
            func(*args, **kwargs)
            return True, ""
        except Exception as _:
            return False, traceback.format_exc()
