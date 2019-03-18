#coding: utf8
from __future__ import absolute_import
from flask import request, abort, g
from farbox_lite.utils.web.response import force_redirect
from farbox_lite.render.apis.site import get_site_from_request
from farbox_lite.utils.lazy import to_int


def set_basic_vars():
    g.site = get_site_from_request()

    # patch request
    is_ssl = False
    if request.environ.get('HTTP_X_PROTOCOL') == 'https':
        is_ssl = True
        request.url = request.url.replace('http://', 'https://')
        request.url_root = request.url_root.replace('http://', 'https://')
    if request.method in ['HEAD']:
        abort(405)

    g.page = None # 分页的数int型
    if request.view_args and 'page' in request.view_args:
        # 当前第几页，这个是一个全局的机制
        g.page = to_int(request.view_args.get('page'), 0)