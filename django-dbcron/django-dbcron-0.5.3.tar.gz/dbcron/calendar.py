from datetime import date, timedelta, datetime
from calendar import HTMLCalendar
from django.utils.translation import ugettext_lazy as _
from dateutil.relativedelta import relativedelta
from dbcron import models

DAYS = {
    6: _("Sunday"),
    0: _("Monday"),
    1: _("Tuesday"),
    2: _("Wednesday"),
    3: _("Thursday"),
    4: _("Friday"),
    5: _("Saturday"),
}


class JobCalendar(HTMLCalendar):
    table_class = ""
    month_table_class = ""
    day_outside_class = ""
    month_today_class = ""
    day_of_month_class = ""
    ul_class = ""
    active_job_class = ""
    disactive_job_class = ""

    def __init__(self, jobs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jobs = jobs

    def get_table_class(self):
        return self.table_class

    def get_job_class(self, job):
        return self.active_job_class if job.is_active else self.disactive_job_class

    def formatweekday(self, day):
        return '<th class="%s">%s</th>' % (self.cssclasses[day], self._format_weekday(day))

    def formatmonth(self, theyear, themonth, withyear=True):
        v = []
        month_weeks = self.monthdays2calendar(theyear, themonth)
        days_before = len([i for i in month_weeks[0] if i[0] == 0])
        dates = self.jobs.get_next_planned_by_hour(
            from_=datetime(theyear, themonth, 1) - timedelta(days=days_before),
            until=date(theyear, themonth, 1) + relativedelta(months=1) + timedelta(days=7)
        )
        a = v.append
        a('<table class="%s">' % (
            self.month_table_class,
        ))
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week_num, week in enumerate(month_weeks):
            a('<tr>')
            for day_id, weekday in week:
                day_klasses = []
                if day_id == 0:  # Out of month
                    if week_num == 0:
                        delta = len([i for i in week if i[1] >= weekday and not i[0]])
                        day = date(theyear, themonth, 1) - timedelta(days=delta)
                    elif week_num == len(month_weeks) - 1:
                        delta = len([i for i in week if i[1] <= weekday and not i[0]])
                        day = self.get_lastdateofmonth(theyear, themonth) + timedelta(days=delta)
                    day_klasses.append(self.day_outside_class)
                else:
                    day = date(theyear, themonth, day_id)
                if day == date.today():
                    day_klasses.append(self.month_today_class)
                a('<td class="%s">' % ' '.join(day_klasses))
                a('<div class="%s">%s</div>' % (
                    self.day_of_month_class,
                    day.day
                ))
                self._format_month_jobs(v, day, dates)
                a('</td>')
            a('</tr>')
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def itermonthweekdays(self, theyear, themonth, theweek):
        for day_ in self.itermonthdates(theyear, themonth):
            if day_.isocalendar()[1] != theweek:
                continue
            yield day_

    def get_firstdateofweek(self, theyear, theweek):
        year_date = date(theyear, 1, 1)
        week_date = year_date + relativedelta(weeks=theweek-1)
        first_day = week_date - timedelta(days=week_date.isocalendar()[2]-1)
        return first_day

    def get_lastdateofmonth(self, theyear, themonth):
        month_after = date(theyear, themonth, 1) + relativedelta(months=1)
        current_month = month_after - timedelta(days=1)
        return current_month

    def _format_weekday(self, day):
        return str(DAYS[day])

    def _format_hour(self, hour):
        if hour == 0:
            return str(_("Midnight"))
        elif hour == 12:
            return str(_("Noon"))
        return '%d' % hour

    def _format_month_day_job(self, v, job, jobtime):
        a = v.append
        a('<li class="%s">' % self.get_job_class(job))
        if hasattr(job, 'get_absolute_url'):
            a('%s - <a href="%s">%s</a>' % (jobtime.strftime("%H:%M"),
                                            job.get_absolute_url(),
                                            job.name))
        else:
            a('%s - %s' % (jobtime.strftime("%H:%M"), job.name))
        a('</li>')

    def _format_month_jobs(self, v, day, dates):
        a = v.append
        a('<ul class="%s">' % self.ul_class)
        offset = date(day.year, day.month, day.day)
        for hour in dates[offset]:
            for job, jobtime in dates[offset][hour]:
                self._format_month_day_job(v, job, jobtime)
            offset += timedelta(days=1)
            a('\n')
        a('</ul>')

    def _format_day_job(self, v, job, jobtime):
        a = v.append
        if hasattr(job, 'get_absolute_url'):
            a('%s - <a href="%s">%s</a>' % (jobtime.strftime("%M"),
                                            job.get_absolute_url(),
                                            job.name))
        else:
            a('%s - %s' % (jobtime.strftime("%H:%M"), job.name))

    def _format_day_jobs(self, v, first_day, dates):
        a = v.append
        for hour in range(0, 24):
            day = first_day
            a('<tr>')
            a('<th>')
            a(self._format_hour(hour))
            a('</th>')
            for i in range(7):
                a('<td>')
                a('<ul class="%s">' % self.ul_class)
                for job, jobtime in dates[day][hour]:
                    a('<li class="%s">' % self.get_job_class(job))
                    self._format_day_job(v, job, jobtime)
                    a('</li>')
                a('</ul>')
                a('</td>')
                day += timedelta(days=1)
            a('</tr>')
            a('\n')

    def _format_weekdays_header(self, v, start_day):
        a = v.append
        day = start_day
        for i in range(7):
            a('<th>%s %s</th>' % (
                self._format_weekday(i),
                day.day,
            ))
            day += timedelta(days=1)

    def formatweekofmonth(self, theyear, theweek, withyear=True):
        v = []
        a = v.append
        day = self.get_firstdateofweek(theyear, theweek)
        a('<table class="%s">' % (
            self.get_table_class()
        ))
        a('\n')
        a('<tr>')
        a('<th>%s</th>' % _("UTC"))
        self._format_weekdays_header(v, day)
        a('</tr>')
        dates = self.jobs.get_next_planned_by_hour(
            from_=datetime(theyear, day.month, day.day) - timedelta(days=1),
            until=day+timedelta(days=7))
        a('<tr>')
        self._format_day_jobs(v, day, dates)
        a('<tr>')
        a('</table>')
        a('\n')
        return ''.join(v)
