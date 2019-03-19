from django.contrib.auth.models import User
from django.db import models

from djangoldp.models import Model


class Circle(Model):
    name = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, default='')
    team = models.ManyToManyField(User, blank=True)
    owner = models.ForeignKey(User, related_name="owned_circles", on_delete=models.DO_NOTHING)
    jabberID = models.CharField(max_length=255, blank=True, null=True)
    jabberRoom = models.BooleanField(default=True)

    class Meta:
        auto_author = 'owner'
        nested_fields = 'team'

    def __str__(self):
        return self.name
