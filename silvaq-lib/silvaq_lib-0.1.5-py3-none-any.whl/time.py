import datetime, time

DEFAULT_FORMATTER = "%Y-%m-%d %H:%M:%S"


def now():
    """
    time.time()
    :return:
    """
    return time.time()


def localtime(secs):
    """
    time.localtime(secs)
    :param secs:
    :return:
    """
    return time.localtime(secs)


def format(timestamp, format_str=DEFAULT_FORMATTER):
    """
    datetime.datetime.fromtimestamp(timestamp).strftime(format_str)
    :param timestamp:
    :param format_str:
    :return:
    """
    return datetime.datetime.fromtimestamp(timestamp).strftime(format_str)


def timestamp2time(timestamp):
    """
    time.mktime(time.localtime(timestamp))
    :param timestamp:
    :return:
    """
    return time.mktime(time.localtime(timestamp))


def str2time(date_string, format_str=DEFAULT_FORMATTER):
    """
    format_str 格式的date_string字符串转换成时间戳
    :param date_string: 要转换的时间字符串
    :param format_str:  要转换的时间字符串的格式
    :return:
    """
    return time.mktime(time.strptime(date_string, format_str))
