#!/usr/bin/env python
"""WSGI adaptors version 2 for integrating AuthKit with Django.

This module is based on the ``powerpack_adaptors.py`` extension, and
adds extra customizations for Django.

Copyright (C) 2010-2018 Etienne Robillard <tkadm30@yandex.ru>
All rights reserved

In the AuthKit model permissions are handled by ``Permission`` objects.
Authorization objects are used to check permissions and to raise
``NotAuthenticatedError`` or ``NotAuthorizedError`` if there is no user or the
user is not authorized. The execeptions are converted to HTTP responses which
are then intercepted and handled by the authentication middleware.

The way permissions objects should be checked depends on where abouts in the
application stack the check occurs and so different authorization objects exist
to make checks at different parts of the stack. You can of course create 
your own permission objects to be authorized by the middleware and decorator
defined here. See the permissions docs or the AuthKit manual for more 
information.

Framework implementors might also create their own implementations of AuthKit
authorization objects. For example the ``authkit.pylons_adaptors`` module
contains some Pylons-specific authorization objects which you'll want to use
if you are using AuthKit with Pylons.

For an example of how to use permission objects have a look at the
``AuthorizeExampleApp`` class in the ``authorize.py`` example in the ``examples``
directory or have a look at the AuthKit manual.
"""


import logging
log = logging.getLogger(__name__)

from functools import wraps

from notmm.utils.django_settings import LazySettings
from notmm.utils.wsgilib.exc import (
    HTTPException, HTTPRedirectResponse, HTTPUnauthorized
    )
from authkit.permissions import RemoteUser
from .exc import *

_handleLogin = HTTPRedirectResponse
_settings = LazySettings()

__all__ = ['authorize', 'login_required', 'authorized']

def authorize(perm, errorHandler=NotAuthorizedError):
    def decorator(view_func, **kwargs):
        @wraps(view_func, **kwargs)
        def _wrapper(*args, **kwargs):
            request = args[0]
            environ = request.environ
            def on_authorize(environ, start_response):
                try:
                    result = perm.check(environ, start_response)
                    return result
                except (HTTPException, HTTPUnauthorized) as e:
                    return False
            if on_authorize(environ, view_func):
                return view_func(request, **kwargs)
            else:
                url = "%s?next=%s" % (_settings.OAUTH2_REDIRECT_URL, environ['PATH_INFO'])
                return _handleLogin(url)
        return wraps(view_func)(_wrapper, **kwargs)
    return decorator

def login_required(view_func):
    @wraps(view_func)
    def _wrapper(request, *args, **kwargs):
        @authorize(RemoteUser())
        def _on_authorize(view_func):
            return view_func(request, **kwargs)
        return wraps(view_func)(_on_authorize, **kwargs)
    return _wrapper
