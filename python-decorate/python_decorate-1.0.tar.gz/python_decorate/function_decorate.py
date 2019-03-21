# coding=utf-8

__author__ = 'songmengyun'

import logging
from functools import wraps

# 函数装饰器
def use_logging(func):
    def wrapper(*args, **kwargs):
        logging.warn("%s is running" % func.__name__)
        return func(*args)
    return wrapper


def use_logging1(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                logging.warn("%s is running" % func.__name__)
            return func(*args)
        return wrapper
    return decorator


def logged(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print (func.__name__ + " was called")
        return func(*args, **kwargs)
    return with_logging


def deco_compare(env=1, db_compare=False, ex='', db_ex='', no_additional=False,
                 ex_only_none=False, is_none_equal_empty=False):
    def deco_resp(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print ('执行用例 %s():' %(func.__name__))
            func_result_one = None
            func_result_two = None

            if env == 1:
                print ('只调用java创建订单接口，不进行任何比对')
            elif env == 2:
                print ('只调用dotnet创建订单接口，不进行任何比对')
            elif env == 3 or env == 4:
                if env == 3:
                    print ('先调用java接口，后调用dontnet接口，并比对返回值')
                elif env == 4:
                    print ('用于query-order中部分接口是从其他服务迁入的情况')
                if db_compare is False:
                    print ('只比对response，不进行数据库对比')
                elif db_compare is True:
                    print ('如果进行数据库比对，先比对response，再对比数据库查询数据')
            return func(*args, **kwargs)
        return wrapper
    return deco_resp






# 类装饰器
class Foo(object):
    def __init__(self, func):
        self._func = func

    def __call__(self):
        print ('class decorator runing')
        self._func()
        print ('class decorator ending')






