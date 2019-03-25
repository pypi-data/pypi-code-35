# coding: utf-8
JWT_TOKEN_KEY = 'jwt'
JWT_EXPIRE_TIME = 3600
JWT_AUTH_SECRET_KEY = 'JWT_AUTH_SECRET_KEY'
JWT_USER_PK = 'id'
JWT_REDIS_KEY = 'user:jwt:{user_id}'

from django.conf.global_settings import *
