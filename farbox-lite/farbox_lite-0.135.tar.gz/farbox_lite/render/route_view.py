#coding: utf8
from __future__ import absolute_import
import io
import os
import re
from flask import abort, request, send_file
from flask.ctx import HTTPException
from jinja2.exceptions import TemplateNotFound

from farbox_lite.template_system.env import farbox_lite_env
from farbox_lite.render.apis.site import get_site_from_request, get_sites
from farbox_lite.render.apis.all_docs import get_doc_by_path
from farbox_lite.utils import smart_str, smart_unicode
from farbox_lite.utils.mime import guess_type
from farbox_lite.utils.web.path import get_path
from farbox_lite.utils.error import capture_error




def render_template_static_file():
    path = request.path.strip('/')
    if not path.startswith('template/'):
        return # ignore
    if path.endswith('.jade'):
        return
    site = get_site_from_request()
    if not site:
        return
    site_root = site['filepath']
    prefix, ext = os.path.splitext(path)
    if ext in ['.scss', '.less']:
        path = prefix + '.css'
    elif ext == '.coffee':
        path = prefix + '.js'
    mime_type = guess_type(path) or 'application/octet-stream'
    template_resources = site.get('template_resources')
    if not template_resources or not isinstance(template_resources, dict):
        return
    template_path = path.replace('template/', '', 1).strip('/').lower()
    abs_filepath = os.path.join(site_root, path)
    if template_path not in template_resources:
        return
    if os.path.isfile(abs_filepath):
        return send_file(abs_filepath, mimetype=mime_type)
    else:
        raw_content = smart_str(template_resources.get(template_path))
        file_response = send_file(io.BytesIO(raw_content), mimetype=mime_type)
        return file_response



def render_common_static_file(html_after_render_func=None):
    path = request.path.strip('/').lower()
    raw_path = request.path.strip('/')
    if request.path.endswith('/'):
        raw_path = request.path + 'index.html'
    raw_path = raw_path.strip('/')
    if not raw_path:
        raw_path = 'index.html'
    site = get_site_from_request()
    if not site:
        return
    site_root = site['filepath']
    abs_filepath = os.path.join(site_root, raw_path)
    if os.path.isfile(abs_filepath):
        mime_type = guess_type(raw_path) or 'application/octet-stream'
        if html_after_render_func and re.search(r'\.html?$', raw_path, flags=re.I):
            with open(abs_filepath, 'rb') as f:
                raw_html_content = f.read()
            raw_html_content = smart_unicode(raw_html_content)
            html_content = html_after_render_func(raw_html_content)
            return send_file(io.BytesIO(smart_str(html_content)), mimetype=mime_type)
        else:
            return send_file(abs_filepath, mimetype=mime_type)
    else:
        file_doc = get_doc_by_path(path, root=site_root)
        if file_doc:
            mime_type = guess_type(path) or 'application/octet-stream'
            filepath = file_doc.get('filepath')
            file_type = file_doc.get('type')
            if file_type in ['file', 'image'] and filepath and os.path.isfile(filepath):
                return send_file(filepath, mimetype=mime_type)



def web_route_view(after_render_func=None, static_html_after_render_func=None):
    # step1, 先处理 template 下的静态资源
    template_static_file_response = render_template_static_file()
    if template_static_file_response:
        return template_static_file_response

    request_path = get_path() # also set g.page
    try:
        template = farbox_lite_env.get_template(request_path)
        if template:
            html = template.render()
            if after_render_func and hasattr(after_render_func, '__call__'):
                html = after_render_func(html)
            return html
        else:
            abort(404)
    except TemplateNotFound:
        static_file_response = render_common_static_file(html_after_render_func=static_html_after_render_func)
        if static_file_response:
            return static_file_response
        else:
            sites = get_sites()
            sites_count = len(sites) if sites else 0
            abort(404, 'TemplateNotFound  or no static file matched, sites: %s' % sites_count)
    except HTTPException, e:
        raise e
    except:
        capture_error()
        abort(500)