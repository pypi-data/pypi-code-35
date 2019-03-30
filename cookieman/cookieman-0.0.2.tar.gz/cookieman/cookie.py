# -*- coding: utf-8 -*-

import functools

import six
import werkzeug.http
import werkzeug.datastructures

import cookieman.exceptions


class Cookie(object):
    header = 'Set-Cookie: '
    mapping_class = werkzeug.datastructures.ImmutableDict
    value_types = six.binary_type if six.PY2 else (six.binary_type, memoryview)
    dump_cookie_fnc = staticmethod(werkzeug.http.dump_cookie)
    byteview_fnc = staticmethod(memoryview.tobytes if six.PY2 else memoryview)

    @classmethod
    def default_partition_name_format(cls, name, index):
        return '{}-{:x}'.format(name, index) if index else name

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def options(self):
        return self._options

    @property
    def data(self):
        if self._data is None:
            self._data = self.header + self.dump_cookie_fnc(
                self._name, self._value, max_size=0, **self._options)
        return self._data

    def __init__(self, name, value=b'', options={}):
        '''
        :param name: cookie name
        :type name: str
        :param value: cookie value
        :type value: str
        :param options: cookie options
        :type options: collections.abc.Mapping
        '''
        assert isinstance(value, self.value_types)
        self._data = None
        self._name = name
        self._value = value
        self._options = self.mapping_class(options)

    def __eq__(self, other):
        return self.data == other.data

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.data)

    def partition(self, maxsize, partition_name_fnc=None):
        '''
        Generate multiple cookies by spliting value in chunks.

        :param maxsize: maximum total cookie size (including header)
        :type maxsize: int
        :param fmt_fnc: cookie name formatting
        :type fmt_fnc: Callable[str, int], str]
        :returns: iterator of cookies
        :rtype: Iterator[cookieman.cookie.Cookie]
        '''
        name_fnc = functools.partial(
            self.default_partition_name_format
            if partition_name_fnc is None else
            partition_name_fnc,
            self.name
            )
        byteview = self.byteview_fnc

        if len(self) < maxsize and name_fnc(0) == self.name:
            yield self
            return

        cls = self.__class__
        total = len(self.value)
        buffer = memoryview(self.value)
        bodysize = maxsize - len(cls('k', b'a', self.options)) + 2

        page = 0
        start = 0
        lastsize = 0

        while start < total or lastsize == maxsize:
            name = name_fnc(page)

            # retry on cookie excess due expansions
            for end in range(start + bodysize - len(name), start, -1):
                cookie = cls(name, byteview(buffer[start:end]), self.options)
                lastsize = len(cookie)

                if lastsize <= maxsize:
                    break
            else:
                raise cookieman.exceptions.CookieSizeException(
                    'Unable to paginate cookies by size %d' % maxsize
                    )

            yield cookie
            start = end
            page += 1


class CookieProcessor(object):
    '''
    Compressed-paginated and signed cookie manager.
    '''
    cookie_class = Cookie

    def __init__(self, session_interface):
        '''
        :param session_interface: flask session interface
        :type session_interface: flask.sessions.SessionInterface
        '''
        self.session_interface = session_interface

    def get_cookie_options(self, app, browser):
        '''
        Get cookie options dict as accepted by flask cookie dump methods.

        :param app: flask app object
        :type app: flask.Flask
        :returns: dict with options
        :rtype: dict
        '''
        return {
            'expires': self.session_interface.get_expiration_time(app),
            'path': self.session_interface.get_cookie_path(app),
            'domain': self.session_interface.get_cookie_domain(app),
            'secure': self.session_interface.get_cookie_secure(app),
            'httponly': self.session_interface.get_cookie_httponly(app),
            }

    def iter_request_cookies(self, app, request, browser):
        '''
        Extract data from cookies.

        :param app: flask app object
        :type app: flask.Flask
        :param request: flask request object
        :type request: flask.Request
        :param browser:
        :type browser: cookieman.limits.Browser
        :returns: iterator of paginated cookie objects
        :rtype: Iterable[cookieman.cookie.Cookie]
        '''
        cookies = request.cookies
        cookie_name = app.session_cookie_name
        cookie_prefix = '%s-' % app.session_cookie_name
        cookies = [
            self.cookie_class(key, value.encode('ascii'))
            for key, value in request.cookies.items()
            if key == cookie_name or key.startswith(cookie_prefix)
            ]

        if cookies:
            cookies.sort(key=lambda x: (len(x.name), x.name))

            maxsize = len(cookies[0])
            for cookie in cookies:
                size = len(cookie)

                # spurious cookie
                if size > maxsize:
                    break

                yield cookie

                # paginated cookies have the same size except for the last one
                if size < maxsize:
                    break

    def iter_response_cookies(self, app, data, browser):
        '''
        Split given byte string for cookies.

        :param app: flask app object
        :type app: flask.Flask
        :param data: byte string
        :type data: bytes
        :param browser:
        :type browser: cookieman.limits.Browser
        :returns: iterator of paginated cookie objects
        :rtype: Iterable[cookieman.cookie.Cookie]
        '''
        options = self.get_cookie_options(app, browser)
        cookie = self.cookie_class(app.session_cookie_name, data, options)
        for page in cookie.partition(browser.maxsize):
            yield page
