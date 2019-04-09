from datetime import date
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy as reverse
from django.utils.timezone import now
from django.utils.html import mark_safe
from dateutil.relativedelta import relativedelta
from dbcron import calendar


class JobCalendarMixin:
    calendar_class = calendar.JobCalendar

    def get_calendar_class(self):
        return self.calendar_class

    def get_calendar_kwargs(self):
        return {
            'jobs': self.object_list,
        }

    def get_calendar(self, calendar_class=None):
        klass = calendar_class or self.get_calendar_class()
        calendar_kwargs = self.get_calendar_kwargs()
        return klass(**calendar_kwargs)

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        calendar = self.get_calendar()
        data.update({
            'calendar': calendar,
        })
        return data


class JobMonthCalendarRedirectView(RedirectView):
    pattern_name = 'job-calendar-month'

    def get_redirect_url(self, *args, **kwargs):
        now_ = now()
        kwargs['year'] = now_.year
        kwargs['month'] = now_.month
        return super().get_redirect_url(*args, **kwargs)


class JobMonthCalendarMixin(JobCalendarMixin):
    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        calendar_date = date(int(self.kwargs['year']), int(self.kwargs['month']), 1)
        html_calendar = data['calendar']
        month_calendar = html_calendar.formatmonth(calendar_date.year, calendar_date.month)
        today = date.today()
        today_url = reverse('job-calendar-month', kwargs={
            'year': today.year, 'month': today.month
        })
        is_current_calendar = bool(
            calendar_date.year == today.year and
            calendar_date.month == today.month
        )
        next_date = calendar_date + relativedelta(months=1)
        next_url = reverse('job-calendar-month', kwargs={
            'year': next_date.year, 'month': next_date.month
        })
        prev_date = calendar_date - relativedelta(months=1)
        prev_url = reverse('job-calendar-month', kwargs={
            'year': prev_date.year, 'month': prev_date.month
        })
        data.update({
            'calendar': mark_safe(month_calendar),
            'calendar_date': calendar_date,
            'calendar_type': 'monthly',
            'is_current_calendar': is_current_calendar,
            'today_url': today_url,
            'today_date': today,
            'next_url': next_url,
            'next_date': next_date,
            'prev_url': prev_url,
            'prev_date': prev_date,
        })
        return data


class JobWeekCalendarRedirectView(RedirectView):
    pattern_name = 'job-calendar-week'

    def get_redirect_url(self, *args, **kwargs):
        now_ = now()
        kwargs['year'] = now_.year
        kwargs['week'] = now_.date().isocalendar()[1]
        return super().get_redirect_url(*args, **kwargs)


class JobWeekCalendarMixin(JobCalendarMixin):
    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        today = now().date()
        today_week = today.isocalendar()[1]
        week = int(self.kwargs.get('week', today_week))
        year = int(self.kwargs.get('year', today.year))
        html_calendar = data['calendar']
        calendar_date = date(year, 1, 1) + relativedelta(weeks=week-1)
        week_calendar = html_calendar.formatweekofmonth(year, week)
        if calendar_date.year == today.year and today_week == week:
            is_current_calendar = True
        else:
            is_current_calendar = False
        today_url = reverse('job-calendar-week', kwargs={
            'year': today.year, 'week': today_week,
        })
        next_date = calendar_date + relativedelta(weeks=1)
        next_url = reverse('job-calendar-week', kwargs={
            'year': next_date.year, 'week': next_date.isocalendar()[1]
        })
        prev_date = calendar_date - relativedelta(weeks=1)
        prev_url = reverse('job-calendar-week', kwargs={
            'year': prev_date.year, 'week': prev_date.isocalendar()[1]
        })
        data.update({
            'calendar': mark_safe(week_calendar),
            'calendar_date': calendar_date,
            'calendar_type': 'weekly',
            'today_url': today_url,
            'today_week': today_week,
            'is_current_calendar': is_current_calendar,
            'next_url': next_url,
            'next_date': next_date,
            'prev_url': prev_url,
            'prev_date': prev_date,
        })
        return data
