# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

OPTIMIZED_IMAGE_METHOD = getattr(settings, 'OPTIMIZED_IMAGE_METHOD', 'way2enjoy')
WAY2ENJOY_KEY = getattr(settings, 'WAY2ENJOY_KEY', None)
