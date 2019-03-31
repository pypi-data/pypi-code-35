# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import home, incident_detail, remove_incident

urlpatterns = (
    url(r'^$', home, name='home'),
    url(r'^incident/(?P<incident_id>\d+)$',
        incident_detail,
        name='incident_detail'),
    url(r'^incident/(?P<incident_id>\d+)/remove/$',
        remove_incident,
        name='remove_incident'),
)
