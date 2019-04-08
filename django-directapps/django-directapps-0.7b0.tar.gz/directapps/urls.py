#
# Copyright (c) 2016, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from django.urls import path, re_path, include
from directapps.views import director, version

app_name = 'directapps'

relation_patterns = [
    path('', director, name='relation'),
    re_path(r'^_(?P<action>\w+)/$', director, name='relation_action'),
    re_path(r'^(?P<relation_object>\w+)/$', director, name='relation_object'),
    re_path(r'^(?P<relation_object>[-\w ]+)/_(?P<action>\w+)/$', director,
            name='relation_object_action'),
]

object_patterns = [
    path('', director, name='object'),
    re_path(r'^_(?P<action>\w+)/$', director, name='object_action'),
    re_path(r'^(?P<relation>\w+)/', include(relation_patterns)),
    re_path(r'^(?P<relation>\w+)\.(?P<relation_using>\w+)/',
            include(relation_patterns)),
]

model_patterns = [
    path('', director, name='model'),
    re_path(r'^_(?P<action>\w+)/$', director, name='model_action'),
    re_path(r'^(?P<object>[-\w ]+)/', include(object_patterns)),
]

app_patterns = [
    path('', director, name='app'),
    re_path(r'^(?P<model>\w+)/', include(model_patterns)),
    re_path(r'^(?P<model>\w+)\.(?P<model_using>\w+)/',
            include(model_patterns)),
]

urlpatterns = [
    path('', director, name='apps'),
    path('_version/', version, name='version'),
    re_path(r'^(?P<app>\w+)/', include(app_patterns)),
]
