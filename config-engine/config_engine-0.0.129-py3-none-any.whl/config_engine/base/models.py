import datetime

from django.db import models


class TimeStampedEntity(models.Model):
    """ Abstract Base Class with repeated timestamp fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FiniteDurationEntity(models.Model):
    """ Abstract Base Class for models associated with some finite duration period"""
    start = models.DateTimeField(null=True)
    termination = models.DateTimeField(null=True)

    def is_within_window(self, reference_dt=None):
        if not reference_dt:
            reference_dt = datetime.datetime.now()
        has_started = True
        if self.start and reference_dt < self.start:
            has_started = False
        if reference_dt < self.termination and has_started:
            return True
        else:
            return False

    def is_after_window_termination(self, reference_dt=None):
        if not reference_dt:
            reference_dt = datetime.datetime.now()
        if reference_dt < self.termination:
            return True
        else:
            return False

    class Meta:
        abstract = True
