#!/usr/bin/env python
from __future__ import print_function
import json
import threading
import sys
import os
import re
import time
import calendar
try:  # Python 3 modules
    from urllib.request import urlopen, Request
    from http.server import HTTPServer
    from http.server import BaseHTTPRequestHandler
except ImportError:  # Python 2 modules
    from urllib2 import urlopen, Request
    from BaseHTTPServer import HTTPServer
    from BaseHTTPServer import BaseHTTPRequestHandler

# Fix issues with decoding HTTP responses
reload(sys)
# pylint: disable=no-member
sys.setdefaultencoding('utf8')

class AnduinRestServer(threading.Thread):
    """ Acts as Anduin DB proxy via REST server. """
    def __init__(self, anduinGlobals, port):
        super(AnduinRestServer, self).__init__()
        self.daemon = True
        self.anduinGlobals = anduinGlobals
        self.port = port
        self.testStatus = {
            "testName": None,
            "testUUID": None,
            "state": 'IDLE',
            "progress": 0,
            "passed": None,
            "error": None,
            "timestamp": 0
        }
        self.testProgress = 0
        self.server = None
        return

    def startTest(self, test, address='localhost'):
        try:
            self.setTestStatus({
                "testName": test.get("testName"),
                "testUUID": None,
                "state": 'START_REQUEST',
                "progress": 0,
                "passed": None,
                "error": None
            })
            req = Request('http://{0}:8009/api/v1/test/start'.format(address), json.dumps(test))
            response = urlopen(req)
            if response.code > 299:
                raise Exception('Start test request failed with response: {0}'.format(response.msg))
        except Exception as err:
            self.setTestStatus({
                "state": 'FINISHED',
                "passed": False,
                "error": "{0}".format(err)
            })

    def stopTest(self, test, address='localhost'):
        try:
            self.setTestStatus({
                "state": 'STOP_REQUEST',
                "passed": False,
                "error": "Test killed"
            })
            req = Request('http://{0}:8009/api/v1/test/stop'.format(address), json.dumps(test))
            response = urlopen(req)
            if response.code > 299:
                raise Exception('Stop test request failed with response: {0}'.format(response.msg))
            self.setTestStatus({"state": 'KILLED', "passed": False})
        except Exception as err:
            self.setTestStatus({
                "state": 'KILLED',
                "passed": False,
                "error": "{0}".format(err)
            })

    def getTestStatus(self, handler=None):
        return self.testStatus

    def setTestStatus(self, handler):
        data = handler if isinstance(handler, dict) else handler.get_payload()
        self.testStatus.update(data)
        self.testStatus['timestamp'] = calendar.timegm(time.gmtime())
        return {}

    def getTestResults(self, handler):
        return {}

    def addTestResults(self, handler):
        results = handler.get_payload()
        self.processTestResults(results)
        return {}

    def processTestResults(self, results):
        error = None
        results = results if isinstance(results, list) else [results]
        for result in results:
            try:
                self.processTestResult(result)
            except Exception as err:  # pylint: disable=broad-except
                error = err
        return error

    def processTestResult(self, result):
        anduinGlobals = self.anduinGlobals
        rstType = result.get('type', '').lower()
        rstName = result.get('name', None)
        rstUnit = result.get('unit', None)
        rstValue = result.get('value', None)
        rstDisplay = result.get('display', False)
        if rstType == 'blob':
            value = rstValue.encode() if isinstance(rstValue, str) else rstValue
            anduinGlobals['AddResultBlob'](rstName, rstUnit, value)
        elif rstType == 'text':
            anduinGlobals['AddResultText'](rstName, rstUnit, rstValue, rstDisplay)
        elif rstType == 'scalar':
            anduinGlobals['AddResultScalar'](rstName, rstUnit, rstValue, rstDisplay)
        elif rstType == 'list':
            anduinGlobals['AddResultList'](rstName, rstUnit, rstValue)
        elif rstType == 'file':
            if str(type(rstValue)) == "<type 'unicode'>":
                anduinGlobals['AddResultText'](rstName, 'Link', '{0}'.format(rstValue))
            elif isinstance(rstValue, str):
                anduinGlobals['AddResultText'](rstName, 'Link', '{0}'.format(rstValue))
            elif isinstance(rstValue, dict):
                srcURL = rstValue.get('src')
                dstPath = rstValue.get('dst')
                dstFolder = os.path.dirname(dstPath)
                if not os.path.exists(dstFolder):
                    os.makedirs(dstFolder)
                with open(dstPath, 'wb') as fp:
                    fp.write(urlopen(srcURL).read())
                anduinGlobals['AddResultText'](rstName, 'Link', str.format('{:s}', dstPath))
            else:
                raise Exception('AddResultText: Value must be either string or dict.')
        elif rstType == 'flush':
            anduinGlobals['FlushMetrics']()
        elif rstType == 'channel':
            anduinGlobals['SetChannel'](rstValue)

    def run(self):
        """ Start proxy threaded """
        class RESTRequestHandler(BaseHTTPRequestHandler):
            # pylint: disable=no-self-argument,return-in-init
            def __init__(rself, *args, **kwargs):
                rself.routes = {
                    r'^/$': {'file': 'web/index.html', 'media_type': 'text/html'},
                    r'^/test/results$': {'GET': self.getTestResults, 'POST': self.addTestResults, 'media_type': 'application/json'},
                    r'^/test/status$': {'GET': self.getTestStatus, 'POST': self.setTestStatus, 'media_type': 'application/json'}
                }
                return BaseHTTPRequestHandler.__init__(rself, *args, **kwargs)

            # pylint: disable=no-self-argument
            def do_HEAD(rself):
                rself.handle_method('HEAD')

            # pylint: disable=no-self-argument
            def do_GET(rself):
                rself.handle_method('GET')

            # pylint: disable=no-self-argument
            def do_POST(rself):
                rself.handle_method('POST')

            # pylint: disable=no-self-argument
            def do_PUT(rself):
                rself.handle_method('PUT')

            # pylint: disable=no-self-argument
            def do_DELETE(rself):
                rself.handle_method('DELETE')

            # pylint: disable=no-self-argument
            def get_payload(rself):
                payload_len = int(rself.headers.getheader('content-length', 0))
                payload = rself.rfile.read(payload_len)
                payload = json.loads(payload)
                return payload

            # pylint: disable=no-self-argument
            def handle_method(rself, method):
                route = rself.get_route()
                if route is None:
                    rself.send_response(404)
                    rself.end_headers()
                    rself.wfile.write('Route not found\n')
                else:
                    if method == 'HEAD':
                        rself.send_response(200)
                        if 'media_type' in route:
                            rself.send_header('Content-type', route['media_type'])
                        rself.end_headers()
                        return
                    if method in route:
                        content = route[method](rself)
                        if content is not None:
                            rself.send_response(200)
                            if 'media_type' in route:
                                rself.send_header('Content-type', route['media_type'])
                            rself.end_headers()
                            if method != 'DELETE':
                                rself.wfile.write(json.dumps(content))
                        else:
                            rself.send_response(404)
                            rself.end_headers()
                            rself.wfile.write('Not found\n')
                    else:
                        rself.send_resesponse(405)
                        rself.end_headers()
                        rself.wfile.write(method + ' is not supported\n')

            # pylint: disable=no-self-argument
            def get_route(rself):
                for path, route in rself.routes.iteritems():
                    if re.match(path, rself.path):
                        return route
                return None
        self.server = HTTPServer(('0.0.0.0', self.port), RESTRequestHandler)
        print('Serving from port', self.port)
        self.server.serve_forever()

    def shutdown(self):
        """ Shutdown proxy"""
        if self.server:
            self.server.shutdown()
        self.server = None

if __name__ == '__main__':
    server = None
    try:
        server = AnduinRestServer(anduinGlobals={}, port=8086)
        server.start()
        while server.is_alive():
            time.sleep(2)
        server.shutdown()
    except KeyboardInterrupt:
        server.shutdown()
    except Exception as err:  # pylint: disable=broad-except
        print(err)
        if server:
            server.shutdown()
    finally:
        if server:
            server.join()
