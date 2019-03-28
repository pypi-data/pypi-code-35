import time
from math import floor

import datetime

from swiss_common_utils.utils.json.json_utils import beautify_json


def get_current_time_millis():
    return int(round(time.time() * 1000))


def get_last_hour_in_millis(hours=1):
    now_millis = int(datetime.datetime.now().timestamp()) * 1000
    hours_in_millis = hours_to_millis(hours)
    return now_millis - hours_in_millis


def get_last_minute_in_millis(minutes=0):
    now_millis = int(datetime.datetime.now().timestamp()) * 1000
    minutes_in_millis = minutes_to_millis(minutes)
    return now_millis - minutes_in_millis


def seconds_to_millis(seconds):
    return seconds * 1000


def minutes_to_millis(minutes):
    return seconds_to_millis(minutes * 60)


def hours_to_millis(hours):
    return minutes_to_millis(hours * 60)


def millis_to_datetime(millis):
    return datetime.datetime.fromtimestamp(millis / 1000.0)


def beautify_datetime(date_time):
    date_time_dict = {'Date': str(date_time.date()), 'Time': str(date_time.time().replace(microsecond=0))}
    date_time_pretty = beautify_json(date_time_dict)
    return date_time_pretty


def datetime_to_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return floor((dt - epoch).total_seconds() * 1000)
