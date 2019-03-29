# -*- coding: utf-8 -*-
"""
License boilerplate should be used here.
"""
# python 3 imports
from __future__ import absolute_import, unicode_literals

# python imports
import logging

# 3rd. libraries imports
from appconf import AppConf

# django imports
from django.conf import settings  # noqa

logger = logging.getLogger(__name__)


class TypeformFeedbackConfig(AppConf):
    TYPEFORM_CH_WEEKLY = 'S'

    TYPE_CHOICES = (
        (TYPEFORM_CH_WEEKLY, 'Weekly'),
    )

    USER_FEEDBACK_STATUS_NONE = 'N'
    USER_FEEDBACK_STATUS_PENDING = 'P'
    USER_FEEDBACK_STATUS_DONE = 'D'

    USER_FEEDBACK_STATUS_CHOICES = (
        (USER_FEEDBACK_STATUS_NONE, 'Not available'),
        (USER_FEEDBACK_STATUS_PENDING, 'Pending'),
        (USER_FEEDBACK_STATUS_DONE, 'Done'),
    )
