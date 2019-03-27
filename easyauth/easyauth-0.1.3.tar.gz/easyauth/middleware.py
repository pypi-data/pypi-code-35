# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import json
import logging

from django.utils import translation
import conf
from permissions import AuthenticatedChecker

logger = logging.getLogger(__name__)


class SwitchLanguageMiddleware(object):

    def process_request(self, request):
        lang = request.GET.get(conf.get_conf(conf.LANG_PARAM), '')

        if not lang:
            lang = request.META.get("HTTP_%s" % conf.get_conf(conf.LANG_PARAM).upper(), '')

        if not lang:
            lang = request.COOKIES.get(conf.get_conf(conf.LANG_PARAM), '')

        if lang:
            translation.activate(lang)
            request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
            request.session['django_language'] = translation.get_language()
            if 'Content-Language' not in response:
                response['Content-Language'] = translation.get_language()
            translation.deactivate()

            return response


class RequestLoggingMiddleware(object):

    def process_request(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            from_host = "%s -> %s" % (request.META['HTTP_X_FORWARDED_FOR'], request.META['REMOTE_ADDR'])
        else:
            from_host = request.META['REMOTE_ADDR']
        querystr = request.GET.urlencode()
        querystr = ("?%s" % querystr) if querystr else ""
        logger.info("[%s] %s '%s%s'", from_host, request.method, request.path, querystr)
        logger.info("Request: ('Content-Type': '%s', ('Content-Length': '%s')",
                     request.META['CONTENT_TYPE'], request.META['CONTENT_LENGTH'])
        if AuthenticatedChecker.is_authenticated(request):
            logger.info("operating by user [%s]", request.user.id)

    def process_response(self, request, response):
        if 'content-type' in response._headers:
            logger.info("Response: %s, ('Content-Length': '%s')",
                         response._headers['content-type'], len(response.content))
        logger.info("Response status: %s", response.status_code)
        return response


