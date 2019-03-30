# -*- coding: utf-8 -*-

import unittest
import json
import tempfile

import werkzeug.useragents

import cookieman.cookie
import cookieman.limits
import cookieman.exceptions


class TestLimits(unittest.TestCase):
    module = cookieman.limits

    def test_database(self):
        data = '\n'.join((
            '[::]',
            'maxcookies = 0',
            'maxsize = 1',
            'maxtotal = 1',
            '',
            '[whatever::]',
            'maxcookies = 0',
            'maxsize = 1',
            'maxtotal = 2',
            '',
            '[whatever:randomOS:]',
            'maxcookies = 0',
            'maxsize = 1',
            'maxtotal = 3',
            '',
            '[whatever:randomOS:3]',
            'maxcookies = 0',
            'maxsize = 1',
            'maxtotal = 4',
            ))
        with tempfile.NamedTemporaryFile() as f:
            f.write(data.encode('utf-8'))
            f.flush()

            db = self.module.Limits.load(f.name)

            browser = db.get('somebrowser', 'os', None)
            self.assertEqual(browser.maxtotal, 1)

            browser = db.get('whatever')
            self.assertEqual(browser.maxtotal, 2)

            browser = db.get('whatever', 'randomOS')
            self.assertEqual(browser.maxtotal, 3)

            browser = db.get('whatever', 'randomOS', (2,))
            self.assertEqual(browser.maxtotal, 3)

            browser = db.get('whatever', 'randomOS', (3,))
            self.assertEqual(browser.maxtotal, 4)

            browser = db.get('whatever', 'randomOS', (4,))
            self.assertEqual(browser.maxtotal, 4)

        self.assertEqual(self.module.Limits(), self.module.Limits())
        self.assertNotEqual(db, self.module.Limits())

    def test_browser(self):
        db = self.module.Limits.load()
        ua = werkzeug.useragents.UserAgent(
            'Mozilla/5.0 (X11; Linux x86_64; rv:65.0) '
            'Gecko/20100101 Firefox/65.0'
            )
        browser = db.get(ua.browser, ua.platform, ua.version)
        self.assertEqual(browser.name, 'firefox')
        self.assertEqual(browser.maxcookies, 150)
        self.assertEqual(browser.maxsize, 4097)
        self.assertEqual(browser.maxtotal, 150 * 4097)

    def test_defaults(self):
        db = self.module.Limits()
        default = db.get()
        self.assertEqual(default.name, '')

        db = self.module.Limits.load()
        firefox = db.get('firefox')
        self.assertEqual(firefox.maxcookies, 50)


class TestBrowser(unittest.TestCase):
    module = cookieman.limits

    def test_repr(self):
        browser = self.module.Browser()
        self.assertIsInstance(repr(browser), str)


class TestShrinker(unittest.TestCase):
    module = cookieman.limits

    def serialize(self, payload):
        return [cookieman.cookie.Cookie('session', payload)]

    def dumps(self, data):
        return json.dumps(data).encode('utf-8')

    def get_cookies(self, data):
        return self.serialize(self.dumps(data))

    def total_len(self, cookies):
        return sum(map(len, cookies))

    def test_register(self):
        manager = self.module.ShrinkManager()
        result = self.get_cookies({})
        maxsize = self.total_len(result)
        browser = self.module.Browser(maxcookies=1, maxsize=maxsize)

        @manager.register(['a', 'b'])
        @manager.register('c')
        def shrink(data, last):
            return {}

        serialized = manager.shrink(
            {'a': 1, 'b': 1}, browser, self.dumps, self.serialize)
        self.assertListEqual(serialized, result)

        serialized = manager.shrink(
            {'a': 1}, browser, self.dumps, self.serialize)
        self.assertListEqual(serialized, result)

        serialized = manager.shrink(
            {'b': 1}, browser, self.dumps, self.serialize)
        self.assertListEqual(serialized, result)

        serialized = manager.shrink(
            {'c': 1}, browser, self.dumps, self.serialize)
        self.assertListEqual(serialized, result)

    def test_shrink(self):
        manager = self.module.ShrinkManager()

        @manager.register('a')
        def shrink(data, last):
            if last or len(data['a']) > 2:
                data['a'] = data['a'][:-1]
            return data

        data = {'a': 'abcdef', 'b': True}
        result = self.get_cookies({'a': 'a'})
        maxsize = self.total_len(result)
        print(maxsize)
        browser = self.module.Browser(maxsize=maxsize)
        serialized = manager.shrink(data, browser, self.dumps, self.serialize)
        self.assertListEqual(serialized, result)

    def test_shrink_priority(self):
        class ShrinkManager(self.module.ShrinkManager):
            def _purge(self, key, data):
                calls.append(key)
                return super(ShrinkManager, self)._purge(key, data)

        manager = ShrinkManager()

        @manager.register('a')
        def sa(data, last):
            calls.append('a')
            if last:
                lastcalls.append('a')
            return data

        @manager.register('b')
        def sb(data, last):
            calls.append('b')
            if last:
                lastcalls.append('b')
            del data['b']
            return data

        @manager.register('c')
        def sc(data, last):
            calls.append('c')
            if last:
                lastcalls.append('c')
            return data

        calls = []
        lastcalls = []
        data = {'a': 'abcdef', 'b': True, 'k': 1, 'c': 2}
        result = self.get_cookies({})
        maxsize = self.total_len(result)
        browser = self.module.Browser(maxsize=maxsize)
        serialized = manager.shrink(data, browser, self.dumps, self.serialize)
        self.assertListEqual(serialized, result)
        self.assertEqual(''.join(calls), 'abckacac')
        self.assertEqual(''.join(lastcalls), 'ac')

    def test_multiple_handlers(self):
        manager = self.module.ShrinkManager()

        @manager.register('a')
        def a1(data, last):
            calls.append(1)
            del data['a']
            return data

        @manager.register('a')
        def a2(data, last):
            calls.append(2)
            del data['a']
            return data

        calls = []
        data = {'a': 1, 'b': 2}
        result = self.get_cookies({})
        maxsize = self.total_len(result)
        browser = self.module.Browser(maxsize=maxsize)
        manager.shrink(data, browser, self.dumps, self.serialize)

        self.assertEqual(len(calls), 1)

    def test_side_effects(self):
        manager = self.module.ShrinkManager()

        @manager.register('a')
        def a(data, last):
            return data

        @manager.register('b')
        def b(data, last):
            if 'a' in data:
                del data['a']  # handled
            if 'c' in data:
                del data['c']  # unhandled
            return data

        data = {'a': 1, 'b': 2, 'c': 3}
        result = self.get_cookies({})
        maxsize = self.total_len(result)
        browser = self.module.Browser(maxsize=maxsize)
        data = manager.shrink(data, browser, self.dumps, self.serialize)

        self.assertEqual(data, result)

    def test_unshrinkable(self):
        manager = self.module.ShrinkManager()

        with self.assertRaises(cookieman.exceptions.CookieSizeException):
            browser = self.module.Browser(maxsize=1)
            manager.shrink({}, browser, self.dumps, self.serialize)

        with self.assertRaises(cookieman.exceptions.CookieSizeException):
            browser = self.module.Browser(maxcookies=0)
            manager.shrink({}, browser, self.dumps, self.serialize)
