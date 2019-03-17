# coding=utf-8
from __future__ import print_function
from datetime import datetime
from datetime import timedelta


class BeautifulDatetime(object):

    @property
    def now(self):
        '''
        :return: 返回此刻
        '''
        return datetime.now()

    @property
    def tomorrow_now(self):
        '''
        :return: 返回明天此时此刻
        '''
        return datetime.now() + timedelta(days=1)

    @property
    def yesterday_now(self):
        '''
        :return: 返回今天此时此刻
        '''
        return datetime.now() - timedelta(days=1)

    @staticmethod
    def get_time_span(dt1, dt2):
        '''
        :param dt1: datetime 1
        :param dt2: datetime 2
        :return: 返回一个元组（天数，分钟数，秒数，毫秒数）
        '''
        if isinstance(dt1, datetime) and isinstance(dt2, datetime):
            if dt1 > dt2:
                time_span = dt1 - dt2
                days = time_span.days
                seconds = time_span.seconds
                minutes = int(seconds / 60)
                seconds = seconds % 60
                microseconds = time_span.microseconds
                return days, minutes, seconds, microseconds
            else:
                raise RuntimeError('参数一必须落后与参数二!')
        else:
            raise RuntimeError('参数dt1,dt2必须为datetime类型的！')

    @staticmethod
    def get_friendly_timespan(dt1, dt2):
        '''
        :param dt1: datetime 1
        :param dt2: datetime 2
        :return: 返回一个较为友好的字符串描述两个日期时间的差
        '''
        days, minutes, seconds, microseconds = BeautifulDatetime.get_time_span(dt1, dt2)
        if days > 0:
            if days == 1:
                return '昨天'
            elif days == 2:
                return '前天'
            elif 2 < days <= 7:
                return '%s天前' % days
            elif 7 < days < 28:
                weeks = int(days / 7)
                return '%s周前' % weeks
            elif 28 <= days < 336:
                months = int(days / 28)
                return '%s个月前' % months
            else:
                years = int(days / 336)
                return '%s年前' % years
        else:
            if minutes > 0:
                if minutes < 10:
                    return '刚刚%s分钟前' % minutes
                elif 10 <= minutes < 60:
                    return '最近%s分钟前' % minutes
                elif minutes >= 60:
                    hours = int(minutes / 60)
                    return '最近%s小时前' % hours
            else:
                if seconds > 0:
                    if seconds < 60:
                        return '刚刚%s秒前' % seconds
                    elif seconds >= 60:
                        minutes = int(seconds / 60)
                        return '刚刚%s分钟前' % minutes
                else:
                    return '刚刚'

    @staticmethod
    def get_date_string(dt):
        '''
        :param dt: datetime object
        :return: 返回日期字符串 'year-month-day'
        '''
        if isinstance(dt, datetime):
            return '%s-%s-%s' % (dt.year, dt.month, dt.day)
        else:
            raise RuntimeError('参数dt必须为datetime类型的！')

    @staticmethod
    def get_time_string(dt):
        '''
        :param dt: datetime object
        :return: 返回时间字符串 'hour:minute:second'
        '''
        if isinstance(dt, datetime):
            return '%s:%s:%s' % (dt.hour, dt.minute, dt.second)
        else:
            raise RuntimeError('参数dt必须为datetime类型的！')

    @staticmethod
    def get_date_time_string(dt):
        '''
        :param dt: datetime object
        :return: 返回日期时间组合字符串 'year-month-day hour:minute:second'
        '''
        return BeautifulDatetime.get_date_string(dt) + ' ' + BeautifulDatetime.get_time_string(dt)

    @staticmethod
    def get_object_from_string(datetime_string):
        '''
        :param datetime_string: 传入一个日期时间字符串 'year-month-day hour:minute:second'
        :return: 返回一个标准的datetime对象
        '''
        if datetime_string is None:
            datetime_string = BeautifulDatetime.get_date_time_string(datetime.now())
        if isinstance(datetime_string, str):
            try:
                datetime_string = datetime_string.strip()
                year, month, day = map(int, datetime_string.split(' ')[0].split('-'))
                hour, minute, second = map(int, datetime_string.split(' ')[1].split(':'))
                return datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
            except:
                raise RuntimeError('传入的字符串格式为："year-month-day hour:minute:second" , 请检查传入的字符串格式。')
