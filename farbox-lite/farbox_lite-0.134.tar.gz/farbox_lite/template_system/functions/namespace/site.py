# coding: utf8
from __future__ import absolute_import
from flask import g, request
import datetime
from jinja2.runtime import Undefined

from farbox_lite.render.apis.data import get_doc, has_doc
from farbox_lite.render.apis.site import get_site_from_request

from farbox_lite.utils.functional import cached_property
from farbox_lite.utils.web.cache_for_function import cache_result
from farbox_lite.template_system.functions.namespace.parts.social import get_social_items, get_social_links






class Site(object):
    def __init__(self):
        raw_site = get_site_from_request()
        raw_site = raw_site or {}

        self.raw = raw_site
        self.id = raw_site.get('id') or raw_site.get('_id') or ''



    def __getattr__(self, item):
        if item in self.raw:
            return self.raw.get(item)
        else:
            extra_data = self.raw.get('_', {})
            if item.startswith("_") and item.lstrip("_") in extra_data:
                return extra_data.get(item.lstrip("_"))
        return self.__dict__.get(item, Undefined())


    @cached_property
    def socials(self):
        socials_html = get_social_links()
        return socials_html

    @cached_property
    def social_items(self):
        return get_social_items()

    @cached_property
    def just_socials(self):
        return get_social_links()




@cache_result
def site():
    # 当前网站的数据对象
    return Site()
