# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import region, provincia, distrito

urlpatterns = (
    url(r'^region/json/$', region, name='ubigeo-region-json'),
    url(r'^provincia/json/$', provincia, name='ubigeo-provincia-json'),
    url(r'^distrito/json/$', distrito, name='ubigeo-distrito-json'),
)
