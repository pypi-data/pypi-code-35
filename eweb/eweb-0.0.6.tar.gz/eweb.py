# -*- coding: utf-8 -*-
"""
eweb is a fast and simple micro-framework for small web applications. Its goal is to enable you to develop
web applications in a simple and understandable way. With it, you don't need to know the HTTP protocol, or how
Python communicates with JavaScript.
"""
__author__ = 'Xiangkui Li'
__license__ = 'MIT'

import json
import os
import random
import time
from urllib import request as req

from bottle import request, Bottle, response, static_file

# route for dispatcher
_ROUTE_DISPATCHER = '/service/<service_name>'
# route for service js
_ROUTE_SERVICE_JS = '/service.js'
# route for static resource
_ROUTE_STATIC = '/<path:path>'
# root dir of static resource
_STATIC_ROOT_DIR = './static'

# service js template
_JS = """/**
* Usage:
* service.call('user.add', {id:1, name:'Tom'}, function(data){console.log(data)});
*/
window.service = {
    baseUrl: '%s://%s/',
    call: function (serviceName, data, successCallback, errorCallback) {
        var data = data || {};
        var formData = new FormData();
        for(var key in data) { formData.append(key, data[key]); }
        successCallback = successCallback || function (data) {};
        errorCallback = errorCallback || function (e) {console.error(e)};

        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                if (xhr.status == 200) {
                    var r = eval('('+xhr.response+')');
                    if(r.code == 200){
                        successCallback(r.data);
                    } else {
                        errorCallback(r.message);
                    }
                } else {
                    errorCallback(xhr.response);
                }
            }
        }
        xhr.open('POST', window.service.baseUrl + 'service/' + serviceName, true);
        xhr.send(formData);
    }
};
"""


class Server(object):
    """
    With this server, you can use the functions defined in the Python module in JavaScript, just like using
    JavaScript functions.

    :param host: Server address to bind to. Pass `0.0.0.0` to listens on all services including the external one.
    :param port: Server port to bind to. Values below 1024 require root privileges. (default: 5000)
        if port is None, server will use a random port.
    :param server: As the server is based on Bottle, please refer to {@link https://www.bottlepy.org/docs/dev/deployment.html}
         for more details of the server adapter.
         (default: `waitress`, others: `paste`/`wsgiref`/`gevent`/`cherrypy`/`gunicorn`.etc)
    :param access_control_allow_origin: default: `*` , allow all request.
    """

    def __init__(self, host='0.0.0.0', port=5000, server='waitress', access_control_allow_origin='*'):
        self._app = Bottle()
        self.host = host
        self.port = port
        if self.port is None:
            self.port = random.randint(5000, 10000)
        self._server = server
        self.access_control_allow_origin = access_control_allow_origin
        # all service collection
        self.services = {}

    def _dispatcher(self, service_name):
        """dispatcher requests to the corresponding functions"""
        if service_name not in self.services:
            return json.dumps({'code': 404, 'message': 'Service "%s" not found!' % service_name}, ensure_ascii=False)

        try:
            service_function = self.services.get(service_name)
            return json.dumps({'code': 200, 'data': service_function(**request.POST)}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'code': 500, 'message': 'Server error: %s' % e}, ensure_ascii=False)

    @staticmethod
    def _static(path):
        return static_file(path, root=_STATIC_ROOT_DIR)

    @staticmethod
    def _service_js():
        js = _JS % (request.urlparts.scheme, request.urlparts.netloc)
        # set content type
        response.headers['Content-Type'] = 'application/javascript'
        return js

    def _enable_cors(self):
        response.headers['Access-Control-Allow-Origin'] = self.access_control_allow_origin

    def run(self, callback=None):
        """
        Start the server instance. This method blocks until the server terminates.

        :param callback: server startup callback
        :return:
        """
        # add route for dispatcher
        self._app.route(_ROUTE_DISPATCHER, method=['POST'], callback=self._dispatcher)
        # service JS
        self._app.route(_ROUTE_SERVICE_JS, callback=self._service_js)
        # add route for static resource
        self._app.route(_ROUTE_STATIC, callback=self._static)
        # allow cross domain request
        self._app.add_hook('after_request', self._enable_cors)

        # server startup callback
        from concurrent.futures import ThreadPoolExecutor
        pool = ThreadPoolExecutor(max_workers=1)
        if callback:
            def on_startup():
                while True:
                    try:
                        req.urlopen('http://127.0.0.1:%s%s' % (self.port, _ROUTE_SERVICE_JS))
                        break
                    except OSError:
                        time.sleep(0.1)
                callback()

            pool.submit(on_startup)

        # startup server
        try:
            self._app.run(host=self.host, port=self.port, server=self._server)
        except Exception as e:
            pool.shutdown(wait=False)
            print(e)

    @staticmethod
    def shutdown():
        """shutdown the server"""
        os._exit(0)
