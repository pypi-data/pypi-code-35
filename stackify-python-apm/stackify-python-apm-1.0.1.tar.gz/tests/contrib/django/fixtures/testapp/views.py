from __future__ import absolute_import

from django.http import HttpResponse


def index(request):
    return HttpResponse("")


def exception(request):
    1 // 0
    return HttpResponse("")
