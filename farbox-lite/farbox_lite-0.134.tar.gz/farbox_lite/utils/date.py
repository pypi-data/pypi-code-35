#coding: utf8
import datetime, re
from dateutil.parser import parse
import calendar
import time
from flask import g
from .lazy import get_value_from_data, to_float

def date_parse(timestr, parserinfo=None, utc_offset=8, **kwargs): # 分析日期的
    if utc_offset is None: # utc_offset=None， 表示是自动的，尝试从site里获得configs.utc_offset
        try:
            utc_offset = to_float(get_value_from_data(g, 'site.configs.utc_offset', 8))
            if utc_offset>13 or utc_offset<-12: # 要在一个合理的范围内
                utc_offset = 8
        except:
            utc_offset = 8
    if isinstance(utc_offset, (str,unicode)):
        utc_offset = to_float(utc_offset, 8)


    if not isinstance(timestr, (unicode, str)): #非字符串的，不处理
        #if hasattr(timestr, 'tzinfo') and timestr.tzinfo is None:  # 时间格式且无时区
        #    timestr -= datetime.timedelta(0, utc_offset*3600) # 调整时区偏差
        # 不需要调整时区，但这种直接传入的date，需确保是utcnow()获取的
        return timestr
    else:
        timestr = timestr.strip()
        if not timestr: # 空字符不处理
            return timestr

        # 网易邮箱的 Date...
        # Fri, 28 Apr 2017 20:09:08 +0800 (GMT+08:00)
        if ' +' in timestr:
            p1, p2 = timestr.split(' +', 1)
            timezone_str = p2.split(' ')[0]
            timestr = '%s +%s' % (p1, timezone_str)


    if isinstance(timestr, unicode):
        timestr = timestr.replace(u'\uff1a', ':')

    date = parse(timestr, parserinfo, **kwargs)

    date_offset_done = False

    if date.tzinfo is not None: # 保证数据有效性
        try:
            diff = date.utcoffset()
            date = date.replace(tzinfo=None)
            date = date - diff
            date_offset_done = True
        except ValueError: #比如exif中的信息有错，则不处理；但是mongodb又会转化，所以，要保证数据格式可用
            date = date.replace(tzinfo=None)

    # utc_offset now
    if date.tzinfo is None and not date_offset_done: # 如果不包含时区信息，则偏移，比如dropbox api提供的都是有时区信息的
        try:
            date -= datetime.timedelta(0, utc_offset*3600)
        except:
            # 囧, 可能会导致 date 的时间工差 <0 ....
            pass

    return date


def get_utc_timestamp():
    # equal to time.time
    #  function returns the number of seconds since the epoch as seconds in UTC.
    now = datetime.datetime.utcnow()
    return date_to_timestamp(now)


def get_isoformat(timestamp=None):
    '''Format the timestamp according to ISO8601 / RFC3339.'''
    if isinstance(timestamp, datetime.datetime):
        timestamp = date_to_timestamp(timestamp)
    timestamp = timestamp or get_utc_timestamp()
    t = time.gmtime(timestamp)
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', t)

def get_rfcformat(timestamp=None):
    '''Format the timestamp according to RFC822.'''
    if isinstance(timestamp, datetime.datetime):
        timestamp = date_to_timestamp(timestamp)
    timestamp = timestamp or get_utc_timestamp()
    t = time.gmtime(timestamp)
    return time.strftime('%a, %d %b %Y %H:%M:%S GMT', t)


def date_to_timestamp(date, is_int=False):
    # date 应该是UTC时间
    if not isinstance(date, datetime.datetime):
        return date
    else: # 需要用calendar.timegm，不然会用本地的时区获得timestamp
        s = '%s.%s' % (int(calendar.timegm(date.timetuple())), date.microsecond) # 保留微秒
        if is_int:
            s = int(s)
        else:
            s = float(s)
        return s

def timestamp_to_date(timestamp, is_utc=True):
    if isinstance(timestamp, (str, unicode)):
        timestamp = timestamp.lower()
        if re.match(r'^\d+(\.\d+)?$', timestamp):
            timestamp = float(timestamp)
    if not isinstance(timestamp, (int, float)):
        # 数据类型不符合
        return timestamp
    if is_utc:
        return datetime.datetime.utcfromtimestamp(timestamp)
    else: # 当前计算机设定时区内的时间
        return datetime.datetime.fromtimestamp(timestamp)



# 获得图片的日期，exif信息中的优先
def get_image_date(exif, file_date=None, utc_offset=8):
    date = file_date
    try:
        exif_date = exif.get('datetime') or exif.get('datetime_mk')
        if not exif_date:
            return date
        exif_date = exif_date.replace(':', '-', 2)
        date_pat = re.search('([12][0-9]{3,3}-[0-9 :-]+)', exif_date)  # exif信息中可能夹杂了其它不干净的内容
        if date_pat:
            exif_date = date_pat.groups()[0]
        date = date_parse(exif_date, utc_offset=utc_offset)
    except:
        pass
    return date


def get_utc_today():
    return datetime.datetime.utcnow().strftime('%Y-%m-%d')