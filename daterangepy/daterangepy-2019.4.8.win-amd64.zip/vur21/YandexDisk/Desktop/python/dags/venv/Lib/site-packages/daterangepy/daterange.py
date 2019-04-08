# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta

import pandas as pd
import pendulum
from dateutil import parser


def _to_datetime(dt):
    if type(dt) is type(pendulum.now()):
        dt = dt.to_datetime_string()

    if type(dt) is type(pendulum.now().date()):
        dt = dt.to_date_string()
        
    if type(dt) is str:
        dt = parser.parse(dt)

    if type(dt) == type(datetime.now().date()):
        # Если тип date, то в datetime.
        dt = datetime.combine(dt, datetime.min.time())

    if type(dt) == type(pd.Timestamp(1)):
        dt = dt.to_pydatetime()

    return dt


def date_range(start_date,
               end_date=None,
               num=None,
               delta=None,
               mandatory_end_date=True,
               return_string_format=False,
               string_format='%Y-%m-%d'):
    """

    :param start_date: datetime or str (От даты)
    :param end_date: datetime or str (До даты)
    :param delta: int (интервал кол-во дней, между датами)
    :param return_string_format: bool (вернуть в даты в виду строки)
    :param string_format: str (формат выводимых дат в виде строки)
    :param mandatory_end_date: bool (сделать end_date конечной датой, если заданный интервал превысит её)
    :return: list
    """
    try:
        # Преобразование в datetime формат.

        start_date = _to_datetime(start_date)
        end_date = _to_datetime(end_date)

        if type(delta) is int:
            delta = timedelta(delta)

        if not delta:
            return []
        if end_date and start_date > end_date:
            raise Exception("Wait. start_date needs to be before end_date")
        if end_date and num:
            raise Exception("Wait. Either specify end_date OR num")
        if not end_date and not num:
            end_date = datetime.now().date()

        l = []
        if end_date:
            while start_date <= end_date:
                l.append(start_date)
                start_date += delta
            if mandatory_end_date and end_date > l[-1]:
                # Если с выбранным интервалом конечная дата получается больше чем end_date, она не добавляеся,
                # поэтому добавляется end_date.
                l.append(end_date)
        else:
            for i in range(abs(num)):
                l.append(start_date)
                if num > 0:
                    start_date += delta
                else:
                    start_date -= delta

        if return_string_format:
            l = [i.strftime(string_format) for i in l]

        return sorted(l)
    except Exception as e:
        logging.error('Входящие параметры:')
        [logging.error('{} = {}', format(k, str(v))) for k, v in locals().items()]
        raise


def frequency_dates(date, frequency):
    frequency = frequency.lower()
    date = _to_datetime(date)

    pd_frequency_dict = {
        'week': 'W',
        'month': 'M',
        'quarter': 'Q',
        'year': 'A',
    }

    if frequency in ('day', 'date'):
        return {'start': date, 'end': date}
    else:
        period = pd.Timestamp(date) \
            .to_period(freq=pd_frequency_dict[frequency])

        return {
            'start': period.start_time.to_pydatetime(warn=False)
                .replace(microsecond=0),
            'end': period.end_time.to_pydatetime(warn=False)
                .replace(microsecond=0)
        }


def period_range(start_date, end_date=None, num=0,
                 frequency='day', delta=1,
                 start_date_adjustment_by_frequency=True,
                 end_date_adjustment_by_frequency=False,
                 add_string_date=True,
                 return_type='dict', string_format='%Y-%m-%d'):
    """
    Генерирует интервалы дат по выбранной частоте.

    :param start_date:
    :param end_date:
    :param frequency: day | date | week | month | quarter | year ;
        Частота интервалов. Можно в разных регистрах указывать.
    :param start_date_adjustment_by_frequency: сделать началом периода выбранной частоты.
        Например если выбран месяц, то start_date будет переведен в дату начала месяца.
    :param end_date_adjustment_by_frequency: сделать конец периода выбранной частоты.
        Например если выбран месяц, то end_date будет переведен в дату конца месяца.
    :param add_string_date: Добавить в словарь даты в формате строки.
    :param return_type: 'dict' | 'tuple' ;
        dict вернет интервалы как [..., dict(date1=dt, date2=dt)]
        tuple вернет интервалы как [..., (dt, dt)]
    :param string_format: формат возвращаемой строки, если return_string_format == True
    :return: [..., dict(date1=dt, date2=dt, date1_str=str, date2_str=str)] | [..., (dt, dt, str, str)]
    """

    try:
        if delta < 1:
            raise Exception('delta должна быть больше 0')

        frequency = frequency.lower()

        # Преобразование в datetime формат.
        start_date = _to_datetime(start_date)
        end_date = _to_datetime(end_date)

        # Определение end_date, если он не указан.
        if end_date is None:
            end_date = start_date+timedelta(num or 0)
            if frequency not in ('day', 'date'):
                end_date = frequency_dates(start_date, frequency)['end']

        if start_date > end_date:
            raise Exception('start_date больше end_date')

        start_dates = []
        end_dates = []

        first_date = frequency_dates(start_date, frequency)['start']

        if frequency in ('day', 'date'):
            while first_date <= end_date:
                start_dates.append(first_date)
                end_dates.append(first_date+pd.offsets.Day(delta-1))

                first_date = first_date+pd.offsets.Day(delta)

        elif frequency == 'week':
            while first_date <= end_date:
                start_dates.append(first_date)
                end_dates.append(first_date+pd.offsets.Week(delta)-timedelta(1))

                first_date = first_date+pd.offsets.Week(delta)

        elif frequency == 'month':
            while first_date <= end_date:
                start_dates.append(first_date)
                end_dates.append(first_date+pd.offsets.MonthEnd(delta))

                first_date = first_date+pd.offsets.MonthBegin(delta)

        elif frequency == 'quarter':
            while first_date <= end_date:
                start_dates.append(first_date)
                end_dates.append(first_date+pd.offsets.QuarterEnd(delta))

                first_date = first_date+pd.offsets.QuarterBegin(delta)

        elif frequency == 'year':
            while first_date <= end_date:
                start_dates.append(first_date)
                end_dates.append(first_date+pd.offsets.YearEnd(delta))

                first_date = first_date+pd.offsets.YearBegin(delta)

        else:
            raise ValueError('Неизвестное значение frequence')

        if start_date_adjustment_by_frequency is False:
            # Дата начала frequence у start_date.
            start_dates[0] = start_date

        if end_date_adjustment_by_frequency is False:
            # last_date всегда превышает end_dates.
            end_dates[-1] = end_date

        start_dates = [_to_datetime(i) for i in start_dates]
        end_dates = [_to_datetime(i) for i in end_dates]

        if return_type == 'dict':
            dates = []
            for i, i2 in zip(start_dates, end_dates):
                date_ = dict(date1=i, date2=i2)
                if add_string_date:
                    date_.update(date1_str=i.strftime(string_format),
                                 date2_str=i2.strftime(string_format))
                dates.append(date_)

        elif return_type == 'tuple':
            dates = []
            for i, i2 in zip(start_dates, end_dates):
                if add_string_date:
                    date_ = (i, i2, i.strftime(string_format),
                             i2.strftime(string_format))
                else:
                    date_ = (i, i2)
                dates.append(date_)
        else:
            raise ValueError('Неверной значение в return_type '
                             'допускается "dict" или "tuple"')

        return dates

    except Exception:
        logging.info('Входящие параметры:')
        for k, v in locals().items():
            logging.info('{} = {}'.format(k, str(v)))
        raise


def days_ago(days,
             from_date=datetime.now().replace(
                 hour=0, minute=0, second=0, microsecond=0),
             return_string=False,
             format='%Y-%m-%d'):
    if type(from_date) is str:
        from_date = parser.parse(from_date)

    dt = from_date-timedelta(days)

    return dt.strftime(format) if return_string else dt


def yesterday_date(return_string=False, format='%Y-%m-%d'):
    return days_ago(1, return_string=return_string, format=format)


def today_date(return_string=False, format='%Y-%m-%d'):
    return days_ago(0, return_string=return_string, format=format)
