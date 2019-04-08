import os

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q

from datawok.conf import settings

from .meta_category import MetaCategory
from .get_models import models as datawok_models


class Meta(models.Model):
    """
    Meta information about your other models.
    """

    datawok_model = models.OneToOneField(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=Q(
            model__in=[model.__name__.lower() for model in datawok_models]
        ),
    )
    category = models.ForeignKey(MetaCategory, on_delete=models.PROTECT)

    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True, blank=True)
    query_alias = models.CharField(max_length=50)
    publish_path = models.CharField(max_length=500)

    created_date = models.DateTimeField(auto_now_add=True)
    last_published = models.DateTimeField(null=True, blank=True)

    def get_publish_path(self):
        date_path = self.created_date.strftime("%Y%m%d")
        publish_path = self.publish_path

        if publish_path[0] == "/":
            publish_path = publish_path[1:]

        if publish_path[-1] == "/":
            publish_path = publish_path[:-1]

        return os.path.join(
            settings.S3_UPLOAD_ROOT, publish_path, date_path, "data.json"
        )

    def get_publish_link(self):
        publish_path = self.get_publish_path()

        if publish_path[0] == "/":
            publish_path = publish_path[1:]

        if publish_path[-1] == "/":
            publish_path = publish_path[:-1]

        return os.path.join(settings.AWS_PUBLIC_ROOT, publish_path)

    def get_model_name(self):
        return self.datawok_model.model

    def __str__(self):
        return self.title if self.title else self.datawok_model.model

    class Meta:
        unique_together = ("category", "query_alias")
