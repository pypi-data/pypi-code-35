import time

import arrow

__all__ = [
    'timeit',
    'derive_hour_from_date',
    'derive_day_from_date',
    'remap_date_formats',
    'seconds_between_times',
    'utc_timestamp',
]


def utc_timestamp() -> str:
    """
    Gets an ISO-8601 complient timestamp of the current UTC time.
    :return:
    """
    return str(arrow.utcnow())


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        return ('%2.2f' % (te - ts), result)

    return timed


def derive_hour_from_date(iso_timestamp:str):
    d = arrow.get(iso_timestamp)
    return {
        "hour_number": int(d.format("H")),
        "hour": d.format("hhA"),
        "timezone": d.format("ZZ")
    }


def derive_day_from_date(iso_timestamp):
    return str(arrow.get(iso_timestamp).date())


def remap_date_formats(date_dict, date_formats, original_format):
    return {
        k: arrow.get(v, original_format).format(date_formats.get(k, original_format))
        for (k, v) in date_dict.items()
    }


def seconds_between_times(arrow_time_a:arrow.Arrow, arrow_time_b:arrow.Arrow) -> float:
    return abs(arrow_time_a.float_timestamp - arrow_time_b.float_timestamp)


# def pick_random_time_between(faker:faker.Generator, start:arrow.Arrow, stop:arrow.Arrow) -> arrow.arrow:
#     return arrow.get(faker.date_time_between(start.datetime, stop.datetime))