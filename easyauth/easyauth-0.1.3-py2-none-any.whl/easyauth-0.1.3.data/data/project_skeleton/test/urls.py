
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework import routers

from easyauth import urls as auth_urls
from easyauth import admin_urls as user_admin_urls

router = routers.DefaultRouter(trailing_slash=False)

# app apis: register apis for your own app
# router.register(r'api/view_path', view_class, base_name='view_name')

urlpatterns = router.urls
urlpatterns += [
    # url(r'^admin/', admin.site.urls),
    # auth apis including login, password reset
    url(r'^api-auth/', include(auth_urls)),
    # user crud apis - only used by administrator
    url(r'^api/', include(user_admin_urls)),
] 

