# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.conf.urls import url

from easyauth import views, conf

urlpatterns = [
    url(r'^login$', views.LoginView.as_view(), name='easyauth_user-login'),
    url(r'^logout$', views.LogoutView.as_view(), name='easyauth_user-logout'),
    url(r'^password/change$', views.PasswordResetView.as_view(), name='easyauth_user-password_change'),
    url(r'^me$', views.UserMeView.as_view(), name='easy_auth_user-me')
]

if not conf.get_conf(conf.DISABLE_REGISTER):
    urlpatterns = urlpatterns + [url(r'^register$', views.RegisterView.as_view(), name='easyauth_user-register'),]


