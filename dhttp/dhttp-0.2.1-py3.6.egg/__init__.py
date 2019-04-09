# .-. encoding: utf-8
import urllib
import asyncio
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


DHTTP_VERSION = '0.2.1'

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
    def __init__(self, app, ip: str, method: str, path: str, query: typing.List[typing.Tuple[str, str]], headers: typing.Dict[str, str], content: bytes):
        """
            An object representing an HTTP request serviced by dhttp.
        
        Arguments:
            app {DHTTPServer} -- The app coordinating the servicing of this request.
            ip {str} -- The IP the request came from.
            method {str} -- The method of the request, e.g. 'GET' or 'POST'.
            path {str} -- The path of the request, e.g. '/index.html'.
            query {typing.List[typing.Tuple[str, str]]} -- The query contents of the path, e.g. [('myname', 'JohnDoe'), ('spaces', 'false')]
            headers {typing.Dict[str, str]} -- The headers of the HTTP request.
            content {bytes} -- The body, in bytes, of the HTTP request.
        """
        self.method = method
        self.headers = headers
        self.content = content
        self.ip = ip
        self.app = app
        self.path = path
        self.query = query
        self.query_dict = {a: b for i, (a, b) in enumerate(query) if [x[0] for x in query].index(a) == i}

    def resolve_path(self):
        path = self.path

        while path in self.app.aliases:
            path = self.app.aliases[path]

        return path

    def get_log(self) -> DHTTPRequestLog:
        return DHTTPRequestLog(self.method, self.ip, self.path, self)

    def get_header(self, name):
        """
            Grabs a header from the request, by name.
        Ignores case.
        
        Arguments:
            name {str} -- The header's name.
        
        Returns:
            str -- The header's content.
        """
        return self.headers.get(name.upper(), None)

class DHTTPResponse(object):
    def __init__(self, app, request: DHTTPRequest, headers: typing.Dict[str, str], write: typing.Callable):
        """
            A DHTTP response 'accumulation' object,  used to write to
        the response's body and set headers before sending the actual
        response back.
        """
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
        """
            Sets the HTTP status of this response, as a string defined
        as '<status number> <status code>'>

            For example:

                res.status('404 NOT FOUND')
                res.end('Look again, pal!')
        
        Arguments:
            status {str} -- The status string.
        """
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
        """
            Sets a response header.
        
        Arguments:
            name {str} -- The name of the header.
            value {str} -- The value of the header.
        """
        self.headers[name] = value

    def write(self, string: typing.Union[str, bytes]):
        """
            Write data into the response body.
        
        Arguments:
            string {str|bytes} -- Data to be written.
        
        Raises:
            BaseException --        Raised if  the response itself was
                                already sent over when data is written
                                to the accumulator's content buffer.
        """


        if self.closed:
            raise BaseException("DHTTPResponse object is already closed!")

        if isinstance(string, bytes):
            self.content.write(string)

        else:
            self.content.write(string.encode('utf-8'))

    def _error(self):
        if not self.closed:
            self.status('500 INTERNAL SERVER ERROR')
            self.end()

    def close(self):
        for f in self._on_close:
            self.catch_error(f)()

        self.closed = True

    def catch_error(self, func):
        def __inner__(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except (BrokenPipeError, ConnectionResetError):
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
        """
            Closes this request, optionally writing
        the given data to  the content accumulation
        buffer first.   End data is appended to the
        body of the actual respnse.
        
        Keyword Arguments:
            end_data {str} --       Data appended to the
                                response body.
                                (default: {''})
        
        Raises:
            BaseException --        Raised if the response was already
                                ended, sent and closed.
        """

        if self.closed:
            raise BaseException("DHTTPResponse object is already closed!")

        if isinstance(end_data, str):
            end_data = end_data.encode('utf-8')

        self.write(end_data)
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
                        (self.method, path, version) = start_line

                        self.path = path.split('?')[0]
                        self.query = urllib.parse.parse_qsl(path.split('?')[-1])

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
                                                self.content.write(self.rfile.read(int(self.headers['CONTENT-LENGTH'])))
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

                except (BrokenPipeError, ConnectionResetError):
                    return

        self.handler_type = WrappedHTTPHandler

    def handle_http_request(self, wrapped, write: typing.Callable):
        wrapped.content.seek(0)
        self.dhttp._receive_request(DHTTPRequest(self.dhttp, wrapped.client_address[0], wrapped.method, wrapped.path, wrapped.query, wrapped.headers, wrapped.content.read()), write)

class DHTTPServer(object):
    def __init__(self, port = 8187):
        """
            A DHTTP server application. Similar to
        Node.js's express(),   you can use this to
        serve  a multitude of  different kinds  of
        documents, media and multimedia via simple
        HTTP.
        
        Keyword Arguments:
            port {int} --
                            The port on the which to listen.
                            (default: {8187})
        """
        self.paths = {}
        self.aliases = {}

        self.event_log = []
        self.middleware = []
        self.port = port
        self.source_addr = '0.0.0.0'
        self.log_handlers = set()

        self.handler = HTTPHandler(self).handler_type
        self._server = None
        self.running_forever = False
        self._on_error = set()
        self._on_service_error = set()

    def on_service_error(self, func):
        """
            Decorator to be  used  to  handle
        an error emerging from  your own HTTP
        handling callbacks,   i.e. those that
        were registered via app.get, app.post
        or app.put (generalizing, app.on).
        
        Arguments:
            func {Function} --      A callback, i.e.
                                the decorated function.
        """
        self._on_service_error.add(func)
        return func

    def on_response_error(self, func):
        """
            Decorator  to be  used  to  handle
        an error emerging from a DHTTPResponse
        object (i.e. a 'res').
        
        Arguments:
            func {Function} --      A callback, i.e.
                                the decorated function.
        """
        self._on_error.add(func)
        return func
        
    def stop(self):
        """
            Stops a server which is running from either
        the  start or  the run_forever  methods.    The
        server object can  still be reused  and started
        again later on, if kept.
        
        Returns:
            int --          A status number; larger than 0
                        if the server was actually stopped
                        (2  if  the  server  was  'running
                        forever'  otherwise  1),  0  if it
                        was not running to begin with.
        """
        if self._server is not None:
            status = 1

            if self.running_forever:
                self._server.shutdown()
                self.running_forever = False

                status = 2

            self._server.server_close()
            self._server = None
            return status

        return 0

    def run_forever(self, callback = None, source_addr = '0.0.0.0'):
        """
            Handles HTTP requests until the stop method is called explicitly.
        Only use if there is no other loop used;   since this is blocking and
        synchronous,   making this method  NOT recommended   (unless one uses
        multithreading to circumvent such restrictions).
        
        Keyword Arguments:
            callback {Function} --      A callback to be ran right before
                                    running forever.
                                    (default: {None})
            source_addr {str}   --      The hostname to bind to.
                                    (default: {'0.0.0.0'})
        """
        self.source_addr = source_addr
        self.start(callback, source_addr)

        try:
            self.running_forever = True
            self._server.serve_forever()

        except KeyboardInterrupt:
            self.shutdown()

    def start(self, callback = None, source_addr = '0.0.0.0'):
        """
            Starts this server's TCPServer, without actually
        handling any requests. To do the latter,  please see
        run_forever and handle_once.
        
        Keyword Arguments:
            callback {Function} --      Callback to be ran once
                                    the server is started.
                                    (default: {None})
            source_addr {str}   --      The hostname to bind to.
                                    (default: {'0.0.0.0'})
        """
        self.source_addr = source_addr
        self._server = socketserver.TCPServer((source_addr, self.port), self.handler)

        if callback is not None:
            callback()

    def handle_once(self):
        """
            Handles only a single request. Internally, this calls
        TCPServer.handle_request(). See Python 3's 'socketserver'
        docs for more.
        
        Returns:
            bool --     Whether the server was started, or, in
                    other words, whether there was a TCPServer
                    instance    on    the    which   to   call
                    handle_request.
        """
        if self._server != None:
            self._server.handle_request()

        return self._server != None

    def on_log(self, func):
        """
            Adds a log handler, called everytime a request is
        to be logged.   One  may  also  use  a  middleware if
        preferred.
        
        Arguments:
            func {Function} --      This function is a decorator,
                                thus it takes a    function as an
                                argument. Use it like this:

                                    @app.on_log
                                    def logger(dhlog):
                                        print("> " + str(dhlog))
        """
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

            if req.method in self.paths:
                for (cbpath, request_handler) in self.paths[req.method]:
                    if fnmatch.fnmatch(path, cbpath):
                        for header in request_handler.headers:
                            headers[header[0]] = headers[1]

            res = DHTTPResponse(self, req, headers, write)

            for (mpath, mw) in self.middleware:
                if mpath is None or mpath == path:
                    flag = mw(req, res)

                    if flag is None:
                        continue

                    elif flag == 'STOP':
                        if res.closed:
                            return

                        else:
                            break

                    elif flag == 'BREAK':
                        break

                    else:
                        print(DHTTPGenericLog('WARN', f'Unknown middleware return flag: {repr(flag)}\n    Expected either of: nothing/None (to continue), STOP, BREAK.\n    Ignoring and continuing...'))
                        continue

            found = False

            if req.method in self.paths:
                for (cbpath, request_handler) in self.paths[req.method]:
                    if fnmatch.fnmatch(path, cbpath):
                        found = True

                        try:
                            request_handler.callback(req, res)

                            if res.closed:
                                break

                        except BaseException as e:
                            traceback.print_exc()
                            send_500 = True

                            for e in self._on_service_error:
                                send_500 = send_500 and not bool(e(req, res))

                            if send_500:
                                res._error()

            if not found or not res.closed:
                res.status('404 NOT FOUND')
                res.end()

        except (BrokenPipeError, ConnectionResetError):
            return

    def set_port(self, new_port, callback = None):
        status = self.stop()

        self.port = new_port

        if status == 2:
            self.run_forever(callback, self.source_addr)

        elif status == 1:
            self.start(callback, self.source_addr)

    def remove(self, method):
        """
            Removes all HTTP request handlers whose callback
        is the given function argument.
        
        Arguments:
            method {Function} -- The callback to remove.
        
        Returns:
            set --        All handlers found that contained  this
                      callback  that  were  removed.   Since  the
                      callback part of the handlers is always the
                      same, the list contains  only  the paths of
                      such handlers.
        """
        removed = set()

        for key, callbacks in self.paths.items():
            self.paths[key] = [(i, m) for (i, m) in callbacks if m is not method]
            found = set(i for (i, m) in callbacks if m is method)
            removed |= found

        return removed

    def on(self, method, path, headers = []):
        """
            Generic HTTP request handler decorator. Use
        only if   you want to listen to  a non-standard
        (i.e.   other than GET, POST or  PUT)   request
        method.
        
        Arguments:
            method {str} --         The HTTP method to listen to
            path {str} --           An fnmatch mask of all HTTP paths to handle.
        
        Keyword Arguments:
            headers {list} --       A list of default response headers. Will
                                be overriden if res.set is called. (default:
                                {[]})
        
        Returns:
            function --             The inner decorator function. Returning
                                another decorator   instead of   the  inner
                                function   directly   is a   way to  supply
                                arguments  to the  actual  inner  function,
                                like so:

                                    def decor1(func_arg):
                                        def decor2(callback):
                                            def __inner__(*args):
                                                return func_arg(*[callback(a) for a in args])

                                            return __inner__

                                        return __decor2__

                                    def sum(a, b):
                                        print(a + b)

                                    @decor1(sum)
                                    def double_sum(a):
                                        return a * 2

                                    double_sum(3, 4) # returns 14 (2*3 + 2*4 = 2(3 + 4) = 2*7 = 14)
        """

        def __decorator__(callback):
            self.paths.setdefault(method, []).append((path, DHTTPCallback(headers, callback)))

        return __decorator__

    def use(self, path = None):
        """
            The standard middleware handler decorator.

            Use to handle every (or a specific kind of) HTTP
        request (with a corresponding response object,  i.e.
        res), before it is even processed by  an actual GET,
        POST or PUT handler.  Useful for things like loggers
        and modifiers. Inspired by Express.

            For example:

                @app.use()
                def set_time(req, res):
                    res['time'] = datetime.datetime.utcnow().strftime('%H:%M:%S')

                SIMULATE_POST = True

                @app.use('/api/*')
                def api_filter(req, res):
                    if req.method == 'GET':
                        if SIMULATE_POST:
                            req.method = 'POST'

                        else:
                            res.status('400 BAD REQUEST')
                            res.end('The API can only be accessed via POST methods! :/')

            Keep in mind that a response object can keep any
        kind of property as a dict:

                res['my_prop'] = 5
                res['data'] = {"John Doe": req.content.read().decode('utf-8')}
        
        Keyword Arguments:
            path {str} -- An fnmatch mask of all HTTP paths to preprocess.
                          (default: {None} -- Preprocess everything!)
        """
        def __decorator__(callback):
            self.middleware.append((path, callback))
            return callback

        return __decorator__

    def unuse(self, func):
        """
            Removes a middleware callback, by removing every
        request preprocessing handler whose callback  is the
        func, a la 'func1 is func2'.
        
        Arguments:
            func {Function} -- The middleware handler to remove.
        """
        new_mw = []

        for (i, middle) in enumerate(self.middleware):
            if middle[1] is not func:
                new_mw.append(middle)

        self.middleware = new_mw

    def get(self, path, headers = []):
        """
            Decorated functions serve any GET requests whose
        path matches the fnmatch mask argument 'path'.

            For example:
                
                @app.get('/time')
                def http__utc_time(req, res):
                    res.end("Right now in the UTC it is {}. Thank you.".format(
                        datetime.datetime.utcnow().strftime('%H:%M:%S')
                    ))

            The function can still be supplied as an argument
        to the 'remove' method, to disable it:

                app.remove(http__utc_time)
        
        Arguments:
            path {str} --           An fnmatch mask of all HTTP paths to handle.
        
        Keyword Arguments:
            headers {list} --       A list of default response headers. Will
                                be overriden if res.set is called. (default:
                                {[]})
        
        Returns:
            Function --   What Python sees as the actual decorator.
        """

        def __decorator__(callback):
            self.on('GET', path, headers)(callback)
            return callback

        return __decorator__

    def post(self, path, headers = []):
        """
            Decorated functions serve any POST requests whose
        path matches the fnmatch mask argument 'path'.

            For example:
                
                import time

                @app.post('/unixtime')
                def http__unix_time(req, res):
                    res.end(time.time())

            The function can still be supplied as an argument
        to the 'remove' method, to disable it:

                app.remove(http__unix_time)
        
        Arguments:
            path {str} --           An fnmatch mask of all HTTP paths to handle.
        
        Keyword Arguments:
            headers {list} --       A list of default response headers. Will
                                be overriden if res.set is called. (default:
                                {[]})
        
        Returns:
            Function --   What Python sees as the actual decorator.
        """

        def __decorator__(callback):
            self.on('POST', path, headers)(callback)
            return callback

        return __decorator__

    def put(self, path, headers = []):
        """
            Decorated functions serve any POST requests whose
        path matches the fnmatch mask argument 'path'.

            For example:

                id = 0

                @app.put('/giveimage')
                def http__put_image(req, res):
                    image_id = id
                    id += 1

                    #   NEVER FORGET YOUR SECURITY AND SANITY CHECKS!!
                    # Don't write to your filesystem random files that
                    # people give you. This is a MERE ILLUSTRATIVE
                    # EXAMPLE.
                    open('{}.png'.format(image_id), 'wb').write(req.content)

                    res.end(str(image_id))

            The function can still be supplied as an argument
        to the 'remove' method, to disable it:

                app.remove(http__put_image)
        
        Arguments:
            path {str} --           An fnmatch mask of all HTTP paths to handle.
        
        Keyword Arguments:
            headers {list} --       A list of default response headers. Will
                                be overriden if res.set is called. (default:
                                {[]})
        
        Returns:
            Function --   What Python sees as the actual decorator.
        """

        def __decorator__(callback):
            self.on('PUT', path, headers)(callback)
            return callback

        return __decorator__

    def serve(self, path, filename, headers = []):
        """
            Serves a single file as a GET request
        handler, e.g. for download.

            http__boring_document = app.serve('/serious_business.pdf', 'I_hope_my_boss_doesn't_see_this_filename.pdf')
        
        Arguments:
            path {str} -- The HTTP path at the which to serve this file.
            filename {[type]} -- The path to the file to serve.
        
        Keyword Arguments:
            headers {list} --       A list of default response headers. Will
                                be overriden if res.set is called. (default:
                                {[]})
        
        Returns:
            Function --         The actual callback, which internally
                            is itself decorated via the 'get' method.
                            Thus,   you can use  the return value  to
                            remove a 'serve' handler:

                                app.remove(http__boring_document)
        """

        @self.get(path, headers)
        def __callback__(req: DHTTPRequest, res: DHTTPResponse):
            if os.path.isfile(filename):
                res.set('Content-Type', mimetypes.guess_type(filename))

                with open(filename, 'rb') as fp:
                    res.end(fp.read())

        return __callback__

    def static(self, path, folder_path, headers = []):
        """
            Serves a folder as a single,  masked GET request
        handler, e.g. to host a bunch of CSS and JS files at
        once.

            http__pictures_folder = 
        
        Arguments:
            path {str} -- The root HTTP path at the which to serve this folder.
            folder_path {[type]} -- The path of the folder to be served.
        
        Keyword Arguments:
            headers {list} --       A list of default response headers. Will
                                be overriden if res.set is called. (default:
                                {[]})
        
        Returns:
            Function --         The actual callback, which internally
                            is itself decorated via the 'get' method.
                            Thus,   you can use  the return value  to
                            remove a 'serve' handler:

                                app.remove(http__pictures_folder)
        """

        @self.get(os.path.join(path, '*'))
        def __callback__(req, res):
            fpath = os.path.join(folder_path, os.path.relpath(req.path, path))

            if os.path.isfile(fpath):
                res.set('Content-Type', mimetypes.guess_type(fpath))

                with open(fpath, 'rb') as fp:
                    res.end(fp.read())

        return __callback__

    def alias(self, path, new_path):
        """
            Aliases an HTTP path to another one, so you can
        visit the same document via both paths,   or merely
        replace an existing path by  aliasing it to another
        one.
        
        Arguments:
            path {str} --     The path to alias.
            new_path {str} -- The path to be aliased to.
        """
        self.aliases[path] = new_path