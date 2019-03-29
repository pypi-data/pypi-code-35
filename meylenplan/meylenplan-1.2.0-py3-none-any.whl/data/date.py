import datetime


class Date(object):

    def __init__(self, day, month):
        self.day = int(day)
        self.month = int(month)
        self.year = datetime.date.today().year
        self.date = datetime.date(self.year, self.month, self.day)

