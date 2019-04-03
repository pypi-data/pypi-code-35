import pytz

from datetime import datetime, timedelta


class Misc:
    """docstring for Misc"""

    def __init__(self):
        pass

    def last_modified_date(day):

        sinceday = datetime.now() - timedelta(days=day)

        calculate_date = datetime(
            sinceday.year,
            sinceday.month,
            sinceday.day,
            sinceday.hour,
            sinceday.minute,
            sinceday.second,
            tzinfo=pytz.utc)

        return str(calculate_date.isoformat()).replace('+00:00', 'Z')
