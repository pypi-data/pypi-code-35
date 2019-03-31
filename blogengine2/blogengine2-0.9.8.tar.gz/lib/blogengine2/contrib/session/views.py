#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Security views for authentication and authorization of registered users based on their
role and permissions. Custom permissions and roles may be configured using the
Authkit library.
"""

import time
import hashlib
import logging

from notmm.utils.wsgilib.exc     import HTTPUnauthorized, HTTPRedirectResponse
from notmm.utils.django_settings import LazySettings
from notmm.utils import decorators
from notmm.utils.template import direct_to_template
from authkit.authenticate   import valid_password
from authkit.permissions    import RemoteUser
from authkit.authorize      import NotAuthenticatedError
from authkit.authorize.decorators import authorize, login_required 
settings = LazySettings()

log = logging.getLogger(__name__)
#auth_conf = loadconf('development.ini', section='authkit')

__all__ = ['logout', 'login', 'unauthorized']

def logout(request, template_name='auth/logout.html', urlto='/'):
    for key in ('REMOTE_USER', 'USER'):
        if key in request.environ.keys():
            del request.environ[key]
            log.debug('logout: deleted %s' % str(key))
    return HTTPRedirectResponse(urlto)

#@login_required
@authorize(RemoteUser())
def login(request, template_name='auth/login.mako', 
    redirect_field_name='next', login_form=None, ssl=False):
    
    url_to = request.POST.get('next', request.path_url)
    extra_context = {'url_to': url_to}
    #assert 'REMOTE_USER' in request.environ
    return direct_to_template(request, template_name, 
        extra_context=extra_context)

def unauthorized(request):
    '''Denies access middleware to unauthorized users'''
    # Only registered accounts may create blog entries
    message = '''\
<html>
<head>
 <title>Permission denied</title>
</head>
<body>
<h2>Permission denied</h2>
<p>Please <a href="/session_login/">authenticate</a> first. Anonymous blog
posting is not permitted yet. A valid account is required to post new articles.
</p>
<p>Thanks for your understanding and have fun writing stuff... :)</p>
</body>
</html>
    '''
    return HTTPUnauthorized(message , mimetype='text/html')

