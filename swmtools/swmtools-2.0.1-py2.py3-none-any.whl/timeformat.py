"""
常用时间的格式化
create by swm 2019/03/25
"""

from functools import wraps
import time
import datetime


def func_timer(function):
    """
    用装饰器实现函数计时
    :param function: 需要计时的函数
    :return: None
    """

    @wraps(function)
    def function_timer(*args, **kwargs):
        print('[Function: {name} start...]'.format(name=function.__name__))
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print('[Function: {name} finished, spent time: {time:.2f}s]'.format(name=function.__name__, time=t1 - t0))
        return result

    return function_timer


def datetime_str_to_datetime(datetime_str: str):
    """
    将datetime类型的str转换为datetime对象再拿去进行其他操作
    datetime必须是%Y-%m-%d %H:%M:%S格式
    :param datetime_str:
    :return: datetime对象
    datetime可以转换为任意字符串，datetime.strftime("%Y-%m-%d %H:%M:%S")
    """
    datetime_res = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    return datetime_res


def datetime_str_to_unixstr(datetime_str: str, msec=True):
    """
    %Y-%m-%d %H:%M:%S这种时间格式的字符串转换为
    unix的时间
    :param datetime_str:  str类型的时间字符串
    :param msec: 是否取毫秒，默认是取了的
    :return: 返回unix时间的字符串
    """
    mic_res = 1
    timearray = time.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    if msec:
        mic_res = mic_res * 1000
    timestamp = int(time.mktime(timearray) * mic_res)
    return timestamp


def unix_str_to_datetime_str(unix_time: int, msec=True):
    """
    将int型的unix time转换为datetime的str
    :param unix_time: 传入的是unix time
    :param msec: 传入的类型是否为毫秒
    :return: 返回datetime的字符串
    """
    if msec:
        unix_time = unix_time // 1000
    datetime_formate = datetime.datetime.fromtimestamp(unix_time)
    datetime_res = datetime_formate.strftime("%Y-%m-%d %H:%M:%S")
    return datetime_res


def get_now(is_unix=True, msec=True):
    """
    获取当前的时间，有两种结果，一种是int类型的unix time
    还有一种结果是str类型的datetime
    :param is_unix: 是否需要unxitime
    :param msec: 是否需要精确到毫秒
    :return: 返回unixtime或者是datetime
    """
    if is_unix:
        mic_res = 1
        str_time = time.time()
        if msec:
            mic_res *= 1000
        return int(str_time * mic_res)
    else:
        datetime_f = datetime.datetime.now()
        datetime_res = datetime_f.strftime("%Y-%m-%d %H:%M:%S")
        return datetime_res
