from django.db import models

from datawok.mixins import DatawokModelMixin
from postgres_copy import CopyManager


class DatawokModel(models.Model):
    objects = CopyManager()

    class Meta(DatawokModelMixin.Meta):
        abstract = True
