# -*- coding: utf-8 -*-
# Copyright 2018-2019 Mateusz Klos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
Test settings for django integration
"""
from __future__ import absolute_import, unicode_literals


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '07s#p@ol!&7$et@@yh=q^r42qr74pjes!sosahjszt#g1yaqyz'
SITE_ID = 1

DEBUG = False
ALLOWED_HOSTS = []


STATIC_URL = '/static/'
STATIC_ROOT = 'static'
# devserver will only serve static files from the first directory below.
STATICFILES_DIRS = []
ROOT_URLCONF = 'fake.urls'

INSTALLED_APPS = (
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
