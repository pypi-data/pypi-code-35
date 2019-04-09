from django.test import TestCase
from dbcron.calendar import JobCalendar
from dbcron import models
from dbcron.tests.factories import JobFactory


class JobCalendarFormatMonthTest(TestCase):
    factory = JobFactory
    jobs = models.Job.objects.all()

    def test_meth(self):
        self.factory.create_batch(5, min=0, hou=0)
        calendar = JobCalendar(self.jobs)
        for year in range(2000, 2005):
            for month in range(1, 13):
                html = calendar.formatmonth(year, month)


class JobCalendarFormatWeekTest(TestCase):
    factory = JobFactory
    jobs = models.Job.objects.all()

    def test_meth(self):
        self.factory.create_batch(5, min=0, hou=0)
        calendar = JobCalendar(self.jobs)
        for year in range(2000, 2005):
            for week in range(1, 53):
                html = calendar.formatweekofmonth(year, week)
