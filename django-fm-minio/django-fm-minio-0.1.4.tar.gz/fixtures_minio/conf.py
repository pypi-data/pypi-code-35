#!env python

from appconf import AppConf

from django.conf import settings

from minio import Minio

class FixturesMinioConf(AppConf):
    URL = 'localhost:9000'
    ACCESS_KEY = 'fixtures'
    SECRET_KEY = 'fixtures'
    SECURE = False

    PREFIX = ''
    BUCKET = 'fixtures'

    class Meta:
        prefix = 'fm_minio'
