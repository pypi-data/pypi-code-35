# -*- coding: utf-8 -*-

import unittest

import flask

import cookieman
import cookieman.limits
import cookieman.exceptions
import cookieman.cookie


class TestCookie(unittest.TestCase):
    module = cookieman.cookie
    cookie_class = module.Cookie

    def test_partition(self):
        name = 'cookie'
        results = {
            b'asdfg': [
                self.cookie_class(name, b'asdf'),
                self.cookie_class('%s-1' % name, b'g'),
                ],
            b'asdfgh': [
                self.cookie_class(name, b'asdf'),
                self.cookie_class('%s-1' % name, b'gh'),
                self.cookie_class('%s-2' % name),
                ],
            b'asdfgh j': [
                self.cookie_class(name, b'asdfgh'),
                self.cookie_class('%s-1' % name, b' j'),
                self.cookie_class('%s-2' % name),
                ],
            b'asdfgh jk': [
                self.cookie_class(name, b'asdfgh'),
                self.cookie_class('%s-1' % name, b' j'),
                self.cookie_class('%s-2' % name, b'k'),
                ],
            }

        for value, result in results.items():
            cookie = self.cookie_class(name, value)
            maxsize = max(len(r) for r in result) if result else 0
            partitions = list(cookie.partition(maxsize))
            self.assertListEqual(partitions, result)

        with self.assertRaises(cookieman.exceptions.CookieSizeException):
            cookie = self.cookie_class('session', b'asdf')
            list(cookie.partition(5))

        with self.assertRaises(cookieman.exceptions.CookieSizeException):
            cookie = self.cookie_class('session', b' ')
            list(cookie.partition(len(cookie) - 2))

    def test_repr(self):
        cookie = self.cookie_class('name', b'value', {'path': '/res'})
        self.assertEqual(
            repr(cookie),
            "<Cookie 'Set-Cookie: name=value; Path=/res'>"
            )


class TestCookieProcessor(unittest.TestCase):
    class FakeRequest(object):
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

    module = cookieman.cookie
    cookie_class = module.Cookie
    processor_class = module.CookieProcessor
    request_class = FakeRequest

    def request(self, **kwargs):
        return self.request_class(**kwargs)

    def setUp(self):
        self.app = flask.Flask('myapp')
        self.app.session_cookie_name = 'session'
        self.app.session_interface = cookieman.CookieMan()
        self.browser = cookieman.limits.Browser()
        self.processor = self.processor_class(self.app.session_interface)

    def test_partial_cookies(self):
        request = self.request(
            cookies={
                'session': 'asdf',
                'session-1': 'gh',
                'session-2': 'j',
                }
            )
        cookies = list(
            self.processor.iter_request_cookies(
                self.app, request, self.browser))
        self.assertListEqual(cookies, [
            self.cookie_class('session', b'asdf'),
            self.cookie_class('session-1', b'gh'),
            self.cookie_class('session-2', b'j'),
            ])

    def test_bad_partial_cookie_size(self):
        request = self.request(
            cookies={
                'session': 'asdf',
                'session-1': 'asdfasdfasdf',
                },
            )
        cookies = list(
            self.processor.iter_request_cookies(
                self.app, request, self.browser))
        self.assertListEqual(cookies, [self.cookie_class('session', b'asdf')])
