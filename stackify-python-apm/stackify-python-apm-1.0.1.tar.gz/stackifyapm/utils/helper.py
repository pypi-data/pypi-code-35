import time


def get_current_time_in_millis():
    return time.time() * 1000


def get_current_time_in_string():
    return str(int(get_current_time_in_millis()))
