# -*- coding: utf-8 -*-

__version__ = '0.0.2'

import datetime

import flask.sessions
import flask.helpers

import cookieman.cookie
import cookieman.serializer
import cookieman.session
import cookieman.limits


class CookieMan(flask.sessions.SessionInterface):
    '''
    Compressed-paginated and signed session cookie manager.
    '''

    limits_class = cookieman.limits.Limits
    shrink_class = cookieman.limits.ShrinkManager
    cookie_processor_class = cookieman.cookie.CookieProcessor
    serializer_class = cookieman.serializer.CookieManSerializer
    session_class = cookieman.session.LazySession

    def __init__(self, salt='session-cookie'):
        self._cookie_processor = self.cookie_processor_class(self)
        self._cookie_shrink = self.shrink_class()
        self._limits_cache = {}
        self.salt = salt

    def register(self, key_or_keys, shrink_fnc=None):
        '''
        Register session shrink function for specific session key or
        keys. Can be used as decorator.

        Usage:
        >>> @app.session_interface.register('my_session_key')
        ... def my_shrink_fnc(data):
        ...     del data['my_session_key']
        ...     return data

        :param key_or_keys: key or iterable of keys would be affected
        :type key_or_keys: Union[str, Iterable[str]]
        :param shrink_fnc: shrinking function (optional for decorator)
        :type shrink_fnc: cookieman.abc.ShrinkFunction
        :returns: either original given shrink_fnc or decorator
        :rtype: cookieman.abc.ShrinkFunction
        '''
        return self._cookie_shrink.register(key_or_keys, shrink_fnc)

    def get_browser(self, app, request):
        '''
        Get browser limit object based on app and request.

        :param app: flask app object
        :type app: flask.Flask
        :returns: limits object
        :rtype: cookieman.limits.Browser
        '''
        limits_file = app.config.get('COOKIEMAN_LIMITS_PATH', None)
        if limits_file not in self._limits_cache:
            self._limits_cache[limits_file] = \
                self.limits_class.load(limits_file)
        return self._limits_cache[limits_file].get(
            request.user_agent.browser,
            request.user_agent.platform,
            request.user_agent.version,
            )

    def get_signing_serializer(self, app):
        '''
        Get signing serializer class instance for given app.

        :param app: application instance
        :type app: flask.Flask
        :returns: instance if app has secret key else None
        :rtype: None or serializer class
        '''
        if not app.secret_key:
            return None
        return self.serializer_class(app.secret_key, self.salt)

    def get_expiration_time(self, app, session=None):
        '''
        Get expiration time for a new cookie based on app config

        :param app: flask app
        :type app: flask.Flask
        :param session: unused
        ;returns: expiration time
        :rtype:
        '''
        return datetime.datetime.utcnow() + app.permanent_session_lifetime

    def open_session(self, app, request):
        '''
        Create a lazy session from request cookies.

        :param app: flask app object
        :type app: flask.Flask
        :param request: request object to extract
        :type request: werkzeug.Request
        :returns: session dict-like object
        :rtype: CookieManSession
        '''
        def extract_cookie_data():
            try:
                data = b''.join(
                    cookie.value
                    for cookie in self._cookie_processor.iter_request_cookies(
                        app,
                        request,
                        self.get_browser(app, request),
                        )
                    )
                if not data:
                    return {}
                max_age = flask.helpers.total_seconds(
                    app.permanent_session_lifetime
                    )
                return serializer.loads(data, max_age=max_age)
            except self.serializer_class.bad_sicnature_exception:
                return {}

        serializer = self.get_signing_serializer(app)
        if serializer:
            return self.session_class(extract_cookie_data, request)
        return None

    def save_session(self, app, session, response):
        '''
        Update response with session cookies.

        :param app: flask app object
        :type app: flask.Flask
        :param session: cookieman session object
        :type session: cookieman.session.LazySession
        :param response: flask response object
        :type response: werkzeug.Response
        :returns: given response object (with cookie changes)
        :rtype: werkzeug.Response
        '''
        request = getattr(session, '_request', None) or flask.request
        browser = self.get_browser(app, request)
        cookies = self._cookie_processor

        if session.modified and not session:
            options = cookies.get_cookie_options(app, browser)
            response.delete_cookie(
                app.session_cookie_name,
                domain=options['domain'],
                path=options['path'],
                )
            return

        if session.accessed and session:
            response.vary.add('Cookie')

        if not self.should_set_cookie(app, session):
            return

        iter_cookies = cookies.iter_response_cookies
        cookies = self._cookie_shrink.shrink(
            dict(session),
            browser,
            self.get_signing_serializer(app).dumps,
            lambda payload: iter_cookies(app, payload, browser)
            )

        for cookie in cookies:
            response.set_cookie(cookie.name, cookie.value, **cookie.options)
