# coding: utf8
from __future__ import absolute_import

from farbox_lite.render.apis.data import get_paginator  #, get_data as _get_data

from farbox_lite.template_system.functions.namespace.html import Html
from farbox_lite.template_system.functions.namespace.data import Data
from farbox_lite.utils.web.cache_for_function import cache_result
from .post import posts
from .image import images


@cache_result
def paginator():
    return get_paginator()

@cache_result
def pager():
    return get_paginator()


@cache_result
def post():
    _posts = posts()
    return _posts.post


def get_post():
    return post()


@cache_result
def image():
    _images = images()
    return _images.image



################# functions starts ##############

def load(source):
    return Html.load(source)


@cache_result
def get_data(*args, **kwargs):
    return Data.get_data(*args, **kwargs)



@cache_result
def _(key, *args): # i18n 专用函数名
    return Html.i18n(key, *args)


@cache_result
def i18n(key, *args): # i18n 专用函数名
    return Html.i18n(key, *args)


