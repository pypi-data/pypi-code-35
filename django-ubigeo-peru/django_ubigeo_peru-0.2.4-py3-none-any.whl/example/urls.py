# -*- coding: utf-8 -*-

from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = (
    url(r'^ubigeo/', include('ubigeo.urls')),
    url(r'^', include('ubigeo_example.urls')),
)
