# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass  # disable csrf check

    def authenticate_header(self, request):
        return "easy_auth-session"
