from django.urls import path

from .views import *

urlpatterns = [
    path("validate", validate_wx_token),
    path("obtainToken", obtain_token),
    path("bindUserInfo", bind_user_info),
    path("me/phone", bind_phone),
    path("vercode", request_vercode),
    path("wxacode", get_user_wxacode)
]
