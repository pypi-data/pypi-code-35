"""MIT xPro Open edX middlware"""
import re

from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


def redirect_to_login():
    """Returns a response redirecting to the login url"""
    return redirect(settings.MITXPRO_CORE_REDIRECT_LOGIN_URL)


class RedirectAnonymousUsersToLoginMiddleware(MiddlewareMixin):
    """Middleware to redirect anonymous users to login via xpro"""

    def process_request(self, request):
        """Process an incoming request"""
        if settings.MITXPRO_CORE_REDIRECT_ENABLED and (
            not getattr(request, "user", None) or request.user.is_anonymous
        ):
            # if allowed regexes are set, redirect if the path doesn't match any
            allowed_regexes = settings.MITXPRO_CORE_REDIRECT_ALLOW_RE_LIST
            if allowed_regexes and not any(
                [re.match(pattern, request.path) for pattern in allowed_regexes]
            ):
                return redirect_to_login()

            # if denied regexes are set, redirect if the path matches any
            denied_regexes = settings.MITXPRO_CORE_REDIRECT_DENY_RE_LIST
            if denied_regexes and any(
                [re.match(pattern, request.path) for pattern in denied_regexes]
            ):
                return redirect_to_login()

        return None
