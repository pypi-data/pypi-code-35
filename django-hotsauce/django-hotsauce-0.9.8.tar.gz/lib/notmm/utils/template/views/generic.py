#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import traceback
import logging
import hashlib

from notmm.utils.template import RequestContext
from notmm.utils.wsgilib.response import HTTPResponse
from notmm.utils.wsgilib.exc import (
    HTTPNotModifiedResponse,
    HTTPException
    )
from datetime import datetime
from time import ctime

from .utils import get_template_loader, TemplateException

log = logging.getLogger('notmm.utils.template')

TemplateLoader = get_template_loader()

__all__ = ['direct_to_template', 'render_template']

def render_template(template_name, ctx, charset='UTF-8', disable_unicode=False):
    t = TemplateLoader.get_template(template_name)
    if disable_unicode and t.output_encoding != charset:
        log.debug("Fixing output encoding to %s" % charset)
        setattr(t, 'output_encoding', charset)
    try:
        if charset == 'UTF-8' and not disable_unicode:
            value = t.render_unicode(data=ctx)
        else:
            value = t.render(data=ctx)
    except TemplateException:
        # Template error processing a unicode template
        # with Mako
        exc_type, exc_value, exc_tb = sys.exc_info()
        rawtb = ''.join([item for item in traceback.format_tb(exc_tb)])
        raise TemplateException(content=rawtb)
    return value

def direct_to_template(request, template_name, extra_context={},
    status=200, charset='UTF-8', mimetype='text/html',
    disable_unicode=False):
    """
    Generic view for returning a Mako template inside a simple
    ``HTTPResponse`` instance.

    """
    # Make sure ctx has our stuff
    if not isinstance(extra_context, RequestContext):
        ctx = RequestContext(request, extra_context)
    else:
        ctx = extra_context

    response = render_template(template_name, ctx)
    h = hashlib.md5(response.encode(charset))

    httpheaders = (
        ('Last-Modified', ctime()),
        ('If-None-Match', h.hexdigest())
    )

    return HTTPResponse(response, request=request,
        headers=httpheaders, status=status, mimetype=mimetype)
