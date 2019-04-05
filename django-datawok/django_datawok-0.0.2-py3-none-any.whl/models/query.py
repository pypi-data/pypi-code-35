from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q

from .get_models import models as datawok_models


class Query(models.Model):
    """
    Meta information about your other models.
    """

    datawok_model = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(
            model__in=[model.__name__.lower() for model in datawok_models]
        ),
    )

    creator = models.ForeignKey(User, on_delete=models.PROTECT)

    code = models.CharField(max_length=1000, blank=True, null=True)
    title = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.title
