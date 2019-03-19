"""
Dev server used for running a lambda app locally.
"""
from __future__ import print_function
import threading
import time
import uuid
import json
import base64
import functools
import aws_lambda_sls.models as models
from collections import namedtuple
from aws_lambda_sls.compat import to_unicode
from aws_lambda_sls.compat import urlparse, parse_qs
from six.moves.socketserver import ThreadingMixIn
from six.moves.BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

MatchResult = namedtuple('MatchResult', ['route', 'captured', 'query_params'])


class RouteMatcher(object):
    def __init__(self, route_urls):
        self.route_urls = sorted(route_urls)

    def match_route(self, url):
        parsed_url = urlparse(url)
        parsed_qs = parse_qs(parsed_url.query, keep_blank_values=True)
        query_params = {k: v[0] for k, v in parsed_qs.items()}
        path = parsed_url.path
        if path != '/' and path.endswith('/'):
            path = path[:-1]
        parts = path.split('/')
        captured = {}
        for route_url in self.route_urls:
            url_parts = route_url.split('/')
            if len(parts) == len(url_parts):
                for i, j in zip(parts, url_parts):
                    if j.startswith('{') and j.endswith('}'):
                        captured[j[1:-1]] = i
                        continue
                    if i != j:
                        break
                else:
                    return MatchResult(route_url, captured, query_params)
        raise ValueError("No matching route found for: %s" % url)


class LocalGatewayException(Exception):
    CODE = 0

    def __init__(self, headers, body=None):
        self.headers = headers
        self.body = body


class InvalidAuthorizerError(LocalGatewayException):
    CODE = 500


class ForbiddenError(LocalGatewayException):
    CODE = 403


class NotAuthorizedError(LocalGatewayException):
    CODE = 401


class LambdaContext(object):
    def __init__(self, function_name, memory_size,
                 max_runtime_ms=3000, time_source=None):
        if time_source is None:
            time_source = time
        self._time_source = time_source
        self._start_time = self._current_time_millis()
        self._max_runtime = max_runtime_ms
        self.function_name = function_name
        self.function_version = '$LATEST'
        self.invoked_function_arn = ''
        self.memory_limit_in_mb = memory_size
        self.aws_request_id = str(uuid.uuid4())
        self.log_group_name = ''
        self.log_stream_name = ''
        self.identity = None
        self.client_context = None

    def _current_time_millis(self):
        return self._time_source.time() * 1000

    def get_remaining_time_in_millis(self):
        runtime = self._current_time_millis() - self._start_time
        return self._max_runtime - runtime


class LocalGateway(object):
    def __init__(self, app_object, stage):
        self._app_object = app_object
        self._stage = stage
        self._config = self._app_object.config
        self._route_matcher = RouteMatcher(list(app_object.routes))

    def _generate_lambda_context(self, headers):
        context = LambdaContext(
            function_name=self._app_object.get_function_name(self._stage),
            memory_size=self._config["LAMBDA_MEMORY_SIZE"],
            max_runtime_ms=self._config["LAMBDA_TIMEOUT"] * 1000
        )
        if "X-Amz-Client-Context" in headers:
            context.client_context = models.ClientContext(
                **json.loads(to_unicode(base64.b64decode(headers["X-Amz-Client-Context"]))))
        return context

    def _generate_lambda_event(self, method, path, body):
        match_route = self._route_matcher.match_route(path)
        if method not in self._app_object.routes[match_route.route]:
            raise ValueError("No matching route method found for: %s" % path)
        if not body:
            return None
        if isinstance(body, bytes):
            return json.loads(to_unicode(body))
        else:
            return body

    def handle_request(self, method, path, headers, body):
        lambda_context, lambda_event = None, {}
        try:
            lambda_context = self._generate_lambda_context(headers)
            lambda_event = self._generate_lambda_event(method, path, body)
        except ValueError:
            error_headers = {'x-amzn-RequestId': lambda_context.aws_request_id,
                             'x-amzn-ErrorType': 'UnauthorizedException'}
            auth_header = headers.get('authorization')
            if auth_header is None:
                auth_header = headers.get('Authorization')
            if auth_header is not None:
                raise ForbiddenError(
                    error_headers,
                    (b'{"message": "Authorization header requires '
                     b'\'Credential\''
                     b' parameter. Authorization header requires \'Signature\''
                     b' parameter. Authorization header requires '
                     b'\'SignedHeaders\' parameter. Authorization header '
                     b'requires existence of either a \'X-Amz-Date\' or a'
                     b' \'Date\' header. Authorization=%s"}'
                     % auth_header.encode('ascii')))
            raise ForbiddenError(
                error_headers,
                b'{"message": "Missing Authentication Token"}')
        response = self._app_object(lambda_event, lambda_context)
        return response

    def _autogen_options_headers(self, lambda_event):
        route_key = lambda_event['requestContext']['resourcePath']
        route_dict = self._app_object.routes[route_key]
        route_methods = list(route_dict.keys())
        cors_config = route_dict[route_methods[0]].cors
        cors_headers = cors_config.get_access_control_headers()
        route_methods.append('OPTIONS')
        cors_headers.update({
            'Access-Control-Allow-Methods': '%s' % ','.join(route_methods)
        })
        return cors_headers

    def _handle_binary(self, response):
        if response.get('isBase64Encoded'):
            body = base64.b64decode(response['body'])
            response['body'] = body
        return response


class LocalRequestHandler(BaseHTTPRequestHandler):
    """
    A class for mapping raw HTTP events to and from LocalGateway.
    """
    protocol_version = 'HTTP/1.1'

    def __init__(self, request, client_address, server, app_object, stage):
        self.local_gateway = LocalGateway(app_object, stage)
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def _parse_payload(self):
        body = None
        content_length = int(self.headers.get('content-length', '0'))
        if content_length > 0:
            body = self.rfile.read(content_length)
        converted_headers = {key: value for key, value in self.headers.items()}
        return converted_headers, body

    def _generic_handle(self):
        headers, body = self._parse_payload()
        try:
            response = self.local_gateway.handle_request(
                method=self.command,
                path=self.path,
                headers=headers,
                body=body
            )
            status_code = response['statusCode']
            headers = response['headers']
            body = response['body']
            self._send_http_response(status_code, headers, body)
        except LocalGatewayException as e:
            self._send_error_response(e)

    def _send_error_response(self, error):
        code = error.CODE
        headers = error.headers
        body = error.body
        self._send_http_response(code, headers, body)

    def _send_http_response(self, code, headers, body):
        if body is None:
            self._send_http_response_no_body(code, headers)
        else:
            self._send_http_response_with_body(code, headers, body)

    def _send_http_response_with_body(self, code, headers, body):
        self.send_response(code)
        if not isinstance(body, bytes):
            body = body.encode('utf-8')
        self.send_header('Content-Length', str(len(body)))
        content_type = headers.pop(
            'Content-Type', 'application/json')
        self.send_header('Content-Type', content_type)
        for header_name, header_value in headers.items():
            self.send_header(header_name, header_value)
        self.end_headers()
        self.wfile.write(body)

    do_GET = do_PUT = do_POST = do_HEAD = do_DELETE = do_PATCH = do_OPTIONS = \
        _generic_handle

    def _send_http_response_no_body(self, code, headers):
        headers['Content-Length'] = '0'
        self.send_response(code)
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


class LocalDevServer(object):
    def __init__(self, app_object, host, port, stage,
                 handler_cls=LocalRequestHandler,
                 server_cls=ThreadedHTTPServer):
        self.app_object = app_object
        self.host = host
        self.port = port
        self._wrapped_handler = functools.partial(handler_cls, app_object=app_object, stage=stage)
        self.server = server_cls((host, port), self._wrapped_handler)

    def handle_single_request(self):
        self.server.handle_request()

    def serve_forever(self):
        print("Starting development server at http://%s:%s" % (self.host, self.port))
        print("Quit the server with CONTROL-C.")
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


class HTTPServerThread(threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self._server = server
        self.daemon = True

    def run(self):
        self._server.serve_forever()

    def shutdown(self):
        if self._server is not None:
            self._server.shutdown()
