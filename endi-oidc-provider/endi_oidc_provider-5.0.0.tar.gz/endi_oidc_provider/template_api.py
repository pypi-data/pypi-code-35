# -*- coding: utf-8 -*-
from pyramid.renderers import get_renderer


class TemplateApi(object):
    """
    Tempate tools used to make template easier to manage
    """
    def __init__(self, ctx, request):
        self.context = ctx
        self.request = request
