# .-. encoding: utf-8
import sys
import fnmatch
import datetime
import os
import traceback
import mimetypes
import re
import hashlib
import base64
import socketserver
import io
import abc
import typing
import collections


DHTTP_VERSION = '0.1.2-post3'

DHTTPCallback = collections.namedtuple('DHTTPCallback', ('headers', 'callback'))


class DHTTPLog(abc.ABC):
    def __init__(self):
        self.when = datetime.datetime.utcnow()

    @abc.abstractmethod
    def log_type(self):
        pass

    @abc.abstractmethod
    def log_data(self):
        pass

    def __str__(self):
        return f'[{self.when.strftime("%Y-%m-%d %H:%M:%S")}] {{{self.log_type()}}} {self.log_data()}'

    def __iter__(self):
        return iter((self.log_type(), self.log_data()))


class DHTTPGenericLog(DHTTPLog):
    def __init__(self, kind, message):
        super().__init__()

        self.kind = kind
        self.message = message

    def log_type(self):
        return self.kind

    def log_data(self):
        return self.message


class DHTTPRequestLog(DHTTPLog):
    def __init__(self, method, ip, request_path, request):
        super().__init__()

        self.method = method
        self.ip = ip
        self.request_path = request_path
        self.request = request

    def log_type(self):
        return 'HTTP: ' + self.method

    def log_data(self):
        return f'{self.ip} @ {self.request_path}'


class DHTTPRequest(object):
    def __init__(self, app, ip: str, method: str, request_path: str, headers: typing.Dict[str, str], content: bytes):
        self.method = method
        self.headers = headers
        self.content = content
        self.ip = ip
        self.app = app
        self.path = request_path

    def resolve_path(self):
        path = self.path

        while path in self.app.aliases:
            path = self.app.aliases[path]

        return path

    def get_log(self) -> DHTTPRequestLog:
        return DHTTPRequestLog(self.method, self.ip, self.path, self)

    def get_header(self, name):
        return self.headers.get(name.upper(), None)

class DHTTPResponse(object):
    def __init__(self, app, request: DHTTPRequest, headers: typing.Dict[str, str], write: typing.Callable):
        self.app = app
        self.headers = headers
        self.request = request
        self._write = self.catch_error(write)
        self.content = io.BytesIO()
        self._status = None

        self._on_close = set()
        self._on_error = set()
        self.closed = False

        self._properties = {}

    def status(self, status):
        self._status = status

    def on_error(self, func):
        self._on_error.add(func)
        return func

    def on_close(self, func):
        self._on_close.add(func)
        return func

    def __setitem__(self, key, value):
        self._properties[key] = value

    def __getitem__(self, key):
        return self._properties[key]

    def set(self, name: str, value: str):
        self.headers[name] = value

    def write_bytes(self, data: bytes):
        if self.closed:
            raise BaseException("DHTTPResponse object is already closed!")

        self.content.write(data)

    def write(self, string: str):
        if self.closed:
            raise BaseException("DHTTPResponse object is already closed!")

        self.content.write(string.encode('utf-8'))

    def _error(self):
        if self.closed:
            raise BaseException("DHTTPResponse object is already closed!")

        self.close()
        self._write(b'HTTP/1.1 500 INTERNAL SERVER ERROR\n')

    def close(self, end_data: str = b''):
        self.closed = True

        if isinstance(end_data, str):
            end_data = end_data.encode('utf-8')

        self._write(end_data)

        for f in self._on_close:
            self.catch_error(f)()

    def catch_error(self, func):
        def __inner__(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except BrokenPipeError:
                pass

            except BaseException as err:
                call_str = func.__name__ + '('
                call_str += ', '.join(type(x).__name__ for x in args)

                if len(kwargs) > 0:
                    call_str += ', ' + ', '.join(f'{x[0]} = {type(x[1]).__name__}' for x in kwargs.items())

                call_str += ')'

                for f in self._on_error | self.app._on_error:
                    try:
                        f((func, args, kwargs, call_str), err)

                    except BaseException:
                        traceback.print_exc()
                        continue

                return None

        return __inner__

    def end(self, end_data: str = ''):
        if self.closed:
            raise BaseException("DHTTPResponse object is already closed!")

        if isinstance(end_data, str):
            end_data = end_data.encode('utf-8')

        self.write_bytes(end_data)
        self.close()

        self.content.seek(0)
        size_length = len(self.content.read())
        self.headers['Content-Length'] = size_length

        # finish up and send response headers
        if self._status is None:
            self._write(b'HTTP/1.1 200 OK\r\n')

        else:
            self._write(f'HTTP/1.1 {self._status}\r\n'.encode('utf-8'))

        self.content.seek(0)
        h = hashlib.md5()
        h.update(self.content.read())
        self.headers.setdefault('Content-MD5', base64.b64encode(h.digest()).decode('utf-8'))
        self.headers.setdefault('Content-Type', 'text/html; encoding=utf-8')

        for name, value in self.headers.items():
            self._write('{name}: {value}\r\n'.format(name = name, value = value).encode('utf-8'))

        # send response content
        self._write(b'\r\n')
        self.content.seek(0)
        self._write(self.content.read())
        self._write(b'\r\n')

class HTTPHandler(object):
    def __init__(self, dhttp):
        self.dhttp = dhttp
        http_handler = self

        class WrappedHTTPHandler(socketserver.StreamRequestHandler):
            def setup(self):
                super().setup()
                self.dhttp_reset()

            def dhttp_reset(self, status_data: typing.Optional[str] = None):
                if status_data is not None:
                    self.wfile.write(status_data)

                self.method = None
                self.path = None
                self.headers = {}
                self.content = io.BytesIO()

            def finish(self):
                super().finish()
                self.dhttp_reset()

            def handle(self):
                try:
                    start_line = self.rfile.readline().strip().decode('utf-8')

                    if start_line == '':
                        return

                    start_line = start_line.split(' ')

                    # B: make sure it has 3 space-separated parts
                    if len(start_line) != 3:
                        self.dhttp_reset(b'HTTP/1.1 400 BAD REQUEST\r\n\r\n')

                    else:
                        (self.method, self.path, version) = start_line

                        # C: ensure parseable version
                        match = re.match(r'^([A-Z]+)/(\d+)\.(\d+)$', version)

                        if match is None:
                            self.dhttp_reset(b'HTTP/1.1 400 BAD REQUEST\r\n\r\n')

                        else:
                            # D: ensure version is HTTP/1.0
                            (protocol, major, minor) = match.groups()

                            if protocol != 'HTTP' or major != '1':
                                self.dhttp_reset(b'HTTP/1.1 505 HTTP VERSION NOT SUPPORTED\r\n\r\n')

                            else:
                                while True:
                                    header_line = self.rfile.readline().decode('utf-8').strip()

                                    # E: check if empty line (header-terminating CRLF)
                                    if len(header_line) == 0:
                                        # F: check if the 'Content-Length' header is not null
                                        try:
                                            if int(self.headers.get('CONTENT-LENGTH', 0)) <= 0:
                                                http_handler.handle_http_request(self, self.wfile.write)

                                                break

                                            else:
                                                self.content.write(self.rfile.read(self.headers['CONTENT-LENGTH']))
                                                http_handler.handle_http_request(self, self.wfile.write)

                                                break

                                        except ValueError:
                                            self.dhttp_reset(b'HTTP/1.1 400 BAD REQUEST\r\n\r\n')

                                            break

                                    else:
                                        match = re.match(r'^([^\s:]+): (.+)$', header_line)

                                        # G: check if header matches format
                                        if match is None:
                                            self.dhttp_reset(b'HTTP/1.1 400 BAD REQUEST\r\n\r\n')

                                            break

                                        else:
                                            (name, value) = match.groups()
                                            self.headers[name.upper()] = value

                except BrokenPipeError:
                    return


        self.handler_type = WrappedHTTPHandler

    def handle_http_request(self, wrapped, write: typing.Callable):
        wrapped.content.seek(0)
        self.dhttp._receive_request(DHTTPRequest(self.dhttp, wrapped.client_address[0], wrapped.method, wrapped.path, wrapped.headers, wrapped.content.read()), write)

class DHTTPServer(object):
    def __init__(self, port = 8187):
        self.pathes = {}
        self.aliases = {}

        self.event_log = []
        self.middleware = []
        self.port = port
        self.log_handlers = set()

        self.handler = HTTPHandler(self).handler_type
        self._server = None
        self._on_error = set()

    def on_error(self, func):
        self._on_error.add(func)
        return func

    def catch_error(self, func):
        def __inner__(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except BrokenPipeError:
                pass

            except BaseException as err:
                call_str = func.__name__ + '('
                call_str += ', '.join(type(x).__name__ for x in args)

                if len(kwargs) > 0:
                    call_str += ', ' + ', '.join(f'{x[0]} = {type(x[1]).__name__}' for x in kwargs.items())

                call_str += ')'

                for f in self._on_error:
                    try:
                        f((func, args, kwargs, call_str), err)

                    except BaseException:
                        traceback.print_exc()
                        continue

                return None

        return __inner__

    def run_forever(self, callback):
        self._server = socketserver.TCPServer(('0.0.0.0', self.port), self.handler)

        if callback is not None:
            callback()

        try:
            self._server.serve_forever()

        except KeyboardInterrupt:
            self._server.shutdown()

    def on_log(self, func):
        self.log_handlers.add(func)
        return func

    def _receive_request(self, req: DHTTPRequest, write: typing.Callable):
        try:
            log = req.get_log()
            self.event_log.append(log)

            for log_handler in self.log_handlers:
                log_handler(log)

            path = req.resolve_path()
                
            headers = {}

            if req.method in self.pathes:
                for (cbpath, cbs) in self.pathes[req.method].items():
                    if fnmatch.fnmatch(path, cbpath):
                        for request_handler in cbs:
                            for header in request_handler.headers:
                                headers[header[0]] = headers[1]

            res = DHTTPResponse(self, req, headers, write)

            for (mpath, mw) in self.middleware:
                if mpath is None or mpath == path:
                    flag = mw(req, res)

                    if flag is None:
                        continue

                    elif flag == 'STOP':
                        return

                    elif flag == 'BREAK':
                        break

                    else:
                        print(DHTTPGenericLog('WARN', f'Unknown middleware return flag: {repr(flag)}\n    Expected either of: nothing/None (to continue), STOP, BREAK.\n    Ignoring and continuing...'))
                        continue

            if req.method in self.pathes:
                for (cbpath, cbs) in self.pathes[req.method].items():
                    if fnmatch.fnmatch(path, cbpath):
                        for request_handler in cbs:
                            try:
                                request_handler.callback(req, res)

                            except BaseException as e:
                                traceback.print_exc()
                                res._error()

            else:
                res.close(b'HTTP/1.1 404 NOT FOUND\r\n\r\n')


        except BrokenPipeError:
            return

    def on(self, method, path, headers = []):
        def __decorator__(callback):
            callback = self.catch_error(callback)
            self.pathes.setdefault(method, {})
            self.pathes[method].setdefault(path, []).append(DHTTPCallback(headers, callback))

        return __decorator__

    def use(self, path = None):
        def __decorator__(callback):
            self.middleware.append((path, callback))
            return callback

        return __decorator__

    def get(self, path, headers = []):
        def __decorator__(callback):
            self.on('GET', path, headers)(callback)
            return callback

        return __decorator__

    def post(self, path, headers = []):
        def __decorator__(callback):
            self.on('POST', path, headers)(callback)
            return callback

        return __decorator__

    def put(self, path, headers = []):
        def __decorator__(callback):
            self.on('PUT', path, headers)(callback)
            return callback

        return __decorator__

    def serve(self, path, filename, headers = []):
        @self.get(path, headers)
        def __callback__(req: DHTTPRequest, res: DHTTPResponse):
            res.set('Content-Type', mimetypes.guess_type(filename))

            with open(filename, 'rb') as fp:
                res.write_bytes(fp.read())

            res.end()

    def static(self, path, folder_path, headers = []):
        @self.get(os.path.join(path, '*'))
        def __callback__(req, res):
            fpath = os.path.join(folder_path, os.path.relpath(req.path, path))

            if os.path.isfile(fpath):
                res.set('Content-Type', mimetypes.guess_type(fpath))

                with open(fpath, 'rb') as fp:
                    res.write_bytes(fp.read())

                res.end()

            else:
                res.close(b'HTTP/1.1 404 NOT FOUND\r\n\r\n')

    def alias(self, path, new_path):
        self.aliases[path] = new_path