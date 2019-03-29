# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField

from model_utils.models import TimeStampedModel

from .conf import settings


class GenericTypeformFeedback(TimeStampedModel):

    object_id = models.IntegerField(db_index=True, null=True)
    content_type = models.ForeignKey(
        ContentType,
        null=True,
        on_delete=models.CASCADE,
    )
    related_to = GenericForeignKey()
    typeform_url = models.CharField(
        max_length=200,
        blank=True,
    )
    typeform_type = models.CharField(
        max_length=1,
        choices=settings.TYPEFORM_FEEDBACK_TYPE_CHOICES,
    )

    def __str__(self):
        return '{} - {}'.format(self.typeform_url, self.get_typeform_type_display())

    def set_typeform_url(self, url):
        self.typeform_url = url
        self.save(update_fields=['typeform_url', 'modified'])


class UserGenericTypeformFeedback(TimeStampedModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        on_delete=models.CASCADE,
    )
    feedback = models.ForeignKey(
        'GenericTypeformFeedback',
        null=False, blank=False,
        related_name='responses',
        on_delete=models.CASCADE,
    )
    response = JSONField(
        blank=True,
        null=True)
    status = models.CharField(
        max_length=1,
        blank=False, null=False,
        choices=settings.TYPEFORM_FEEDBACK_USER_FEEDBACK_STATUS_CHOICES,
    )

    def __str__(self):
        return '{} - {}'.format(
            self.user, self.feedback,
        )

    def get_project(self):
        return self.feedback.related_to.first().project

    @property
    def typeform_url(self):
        return self.feedback.typeform_url

    def set_typeform_response(self, response):
        self.response = response
        self.status = settings.RATINGS_USER_FEEDBACK_STATUS_DONE
        self.save(update_fields=['response', 'status', 'modified'])
