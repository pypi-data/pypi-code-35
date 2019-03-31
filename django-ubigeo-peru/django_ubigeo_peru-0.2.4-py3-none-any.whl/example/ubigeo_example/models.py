# -*- coding: utf-8 -*-

from django.db import models
# from ubigeo.models import Ubigeo


class Incident(models.Model):

    location = models.ForeignKey(
        'ubigeo.Ubigeo', related_name='location', blank=True, null=True, on_delete=models.CASCADE
    )

    def __unicode__(self):
        return "id: %s | location: %s" % (self.pk, self.location)
