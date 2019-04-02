from django.conf.urls import url

from comk_django_plugin.views.LogView import GetLog

urlpatterns = [
    url(r'^getlog/(.+)/', GetLog.as_view(), name='获取日志'),
]
