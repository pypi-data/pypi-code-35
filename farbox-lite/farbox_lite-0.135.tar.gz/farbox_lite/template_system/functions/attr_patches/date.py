# coding: utf8
from __future__ import absolute_import
import datetime
from farbox_lite.template_system.functions.attr_patches.models.date import Date

def date(obj):
    if isinstance(obj, datetime.datetime):
        return Date(obj)
    else:
        return obj
