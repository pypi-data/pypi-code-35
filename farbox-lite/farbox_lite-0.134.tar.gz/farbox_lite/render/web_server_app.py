#coding: utf8
from __future__ import absolute_import
from .web_app import app, web_route_view
from farbox_lite.render.apis.site import create_sites, get_sites



# todo create sites first...

# at last
@app.route('/', methods=['POST', 'GET'])
@app.route('/<path:web_path>', methods=['POST', 'GET'])
def web_route(web_path=''):
    return web_route_view()