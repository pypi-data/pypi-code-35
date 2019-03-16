#!/usr/bin/env python
"""Tests for mechanize.Browser."""

import copy
import os
import re
from io import BytesIO
from unittest import TestCase

import mechanize
import mechanize._response
import mechanize._testcase
from mechanize._gzip import HTTPGzipProcessor, compress_readable_output
from mechanize._response import test_html_response
from mechanize.polyglot import (HTTPConnection, addinfourl, codepoint_to_chr,
                                create_response_info, iteritems, unicode_type)

em_dash = codepoint_to_chr(0x2014)


# XXX these 'mock' classes are badly in need of simplification / removal
# (note this stuff is also used by test_useragent.py and test_browser.doctest)
class MockMethod:
    def __init__(self, meth_name, action, handle):
        self.meth_name = meth_name
        self.handle = handle
        self.action = action

    def __call__(self, *args):
        return self.handle(self.meth_name, self.action, *args)


class MockHeaders(dict):
    def getheaders(self, name):
        name = name.lower()
        return [v for k, v in iteritems(self) if name == k.lower()]

    def __delitem__(self, k):
        kmap = {q.lower(): q for q in self}
        k = kmap.get(k.lower())
        if k is not None:
            dict.__delitem__(self, k)


class MockResponse:
    closeable_response = None

    def __init__(self, url="http://example.com/", data=None, info=None):
        self.url = self._url = url
        if isinstance(data, type(u'')):
            data = data.encode('utf-8')
        self.fp = BytesIO(data)
        if info is None:
            info = {}
        self._info = self._headers = MockHeaders(info)
        self.close_called = False

    def _set_fp(self, fp):
        self.fp = fp

    def info(self):
        return self._info

    def geturl(self):
        return self.url

    def read(self, size=-1):
        return self.fp.read(size)

    def seek(self, whence):
        assert whence == 0
        self.fp.seek(0)

    def close(self):
        self.close_called = True

    def get_data(self):
        pass


def make_mock_handler(response_class=MockResponse):
    class MockHandler:
        processor_order = 500
        handler_order = -1

        def __init__(self, methods):
            self._define_methods(methods)

        def _define_methods(self, methods):
            for name, action in methods:
                if name.endswith("_open"):
                    meth = MockMethod(name, action, self.handle)
                else:
                    meth = MockMethod(name, action, self.process)
                setattr(self.__class__, name, meth)

        def handle(self, fn_name, response, *args, **kwds):
            self.parent.calls.append((self, fn_name, args, kwds))
            if response:
                if isinstance(response, mechanize.HTTPError):
                    raise response
                r = response
                r.seek(0)
            else:
                r = response_class()
            req = args[0]
            r.url = req.get_full_url()
            return r

        def process(self, fn_name, action, *args, **kwds):
            self.parent.calls.append((self, fn_name, args, kwds))
            if fn_name.endswith("_request"):
                return args[0]
            else:
                return args[1]

        def close(self):
            pass

        def add_parent(self, parent):
            self.parent = parent
            self.parent.calls = []

        def __lt__(self, other):
            if not hasattr(other, "handler_order"):
                # Try to preserve the old behavior of having custom classes
                # inserted after default ones (works only for custom user
                # classes which are not aware of handler_order).
                return True
            return self.handler_order < other.handler_order

    return MockHandler


class TestBrowser(mechanize.Browser):
    default_features = []
    default_others = []
    default_schemes = []


class TestBrowser2(mechanize.Browser):
    # XXX better name!
    # As TestBrowser, this is neutered so doesn't know about protocol handling,
    # but still knows what to do with unknown schemes, etc., because
    # UserAgent's default_others list is left intact, including classes like
    # UnknownHandler
    default_features = []
    default_schemes = []


class BrowserTests(TestCase):
    def test_referer(self):
        b = TestBrowser()
        url = "http://www.example.com/"
        r = MockResponse(url, """<html>
<head><title>Title</title></head>
<body>
<form name="form1">
 <input type="hidden" name="foo" value="bar"></input>
 <input type="submit"></input>
 </form>
<a href="http://example.com/foo/bar.html" name="apples"></a>
<a href="https://example.com/spam/eggs.html" name="secure"></a>
<a href="blah://example.com/" name="pears"></a>
</body>
</html>
""", {"content-type": "text/html"})
        b.add_handler(make_mock_handler()([("http_open", r)]))

        # Referer not added by .open()...
        req = mechanize.Request(url)
        b.open(req)
        self.assertTrue(req.get_header("Referer") is None)
        # ...even if we're visiting a document
        b.open(req)
        self.assertTrue(req.get_header("Referer") is None)
        # Referer added by .click_link() and .click()
        b.select_form("form1")
        req2 = b.click()
        self.assertEqual(req2.get_header("Referer"), url)
        b.open(req2)
        req3 = b.click_link(name="apples")
        self.assertEqual(req3.get_header("Referer"), url + "?foo=bar")
        # Referer not added when going from https to http URL
        b.add_handler(make_mock_handler()([("https_open", r)]))
        b.open(req3)
        req4 = b.click_link(name="secure")
        self.assertEqual(
            req4.get_header("Referer"), "http://example.com/foo/bar.html")
        b.open(req4)
        req5 = b.click_link(name="apples")
        self.assertTrue(not req5.has_header("Referer"))
        # Referer not added for non-http, non-https requests
        b.add_handler(make_mock_handler()([("blah_open", r)]))
        req6 = b.click_link(name="pears")
        self.assertTrue(not req6.has_header("Referer"))
        # Referer not added when going from non-http, non-https URL
        b.open(req6)
        req7 = b.click_link(name="apples")
        self.assertTrue(not req7.has_header("Referer"))

        # XXX Referer added for redirect

    def test_encoding(self):
        import mechanize
        # always take first encoding, since that's the one from the real HTTP
        # headers, rather than from HTTP-EQUIV
        b = mechanize.Browser()
        for s, ct in [
            ("", mechanize._html.DEFAULT_ENCODING),
            ("Foo: Bar\r\n\r\n", mechanize._html.DEFAULT_ENCODING),
            ("Content-Type: text/html; charset=UTF-8\r\n\r\n", "UTF-8"),
            ("Content-Type: text/html; charset=UTF-8\r\n"
             "Content-Type: text/html; charset=KOI8-R\r\n\r\n", "UTF-8"),
        ]:
            if not isinstance(s, bytes):
                s = s.encode('ascii')
            msg = create_response_info(BytesIO(s))
            r = addinfourl(BytesIO(b""), msg, "http://www.example.com/")
            b.set_response(r)
            self.assertEqual(b.encoding(), ct)

    def test_history(self):
        import mechanize
        from mechanize import _response

        def same_response(ra, rb):
            return ra.wrapped is rb.wrapped

        class Handler(mechanize.BaseHandler):
            def http_open(self, request):
                r = _response.test_response(url=request.get_full_url())
                # these tests aren't interested in auto-.reload() behaviour of
                # .back(), so read the response to prevent that happening
                r.get_data()
                return r

        b = TestBrowser2()
        b.add_handler(Handler())
        self.assertRaises(mechanize.BrowserStateError, b.back)
        r1 = b.open("http://example.com/")
        self.assertRaises(mechanize.BrowserStateError, b.back)
        b.open("http://example.com/foo")
        self.assertTrue(same_response(b.back(), r1))
        r3 = b.open("http://example.com/bar")
        b.open("http://example.com/spam")
        self.assertTrue(same_response(b.back(), r3))
        self.assertTrue(same_response(b.back(), r1))
        self.assertEqual(b.geturl(), "http://example.com/")
        self.assertRaises(mechanize.BrowserStateError, b.back)
        # reloading does a real HTTP fetch rather than using history cache
        r5 = b.reload()
        self.assertTrue(not same_response(r5, r1))
        # .geturl() gets fed through to b.response
        self.assertEqual(b.geturl(), "http://example.com/")
        # can go back n times
        b.open("spam")
        self.assertEqual(b.geturl(), "http://example.com/spam")
        r7 = b.open("/spam")
        self.assertTrue(same_response(b.response(), r7))
        self.assertEqual(b.geturl(), "http://example.com/spam")
        self.assertTrue(same_response(b.back(2), r5))
        self.assertEqual(b.geturl(), "http://example.com/")
        self.assertRaises(mechanize.BrowserStateError, b.back, 2)
        r8 = b.open("/spam")

        # even if we get an HTTPError, history, .response() and .request should
        # still get updated
        class Handler2(mechanize.BaseHandler):
            def https_open(self, request):
                r = mechanize.HTTPError("https://example.com/bad", 503, "Oops",
                                        MockHeaders(), BytesIO())
                return r

        b.add_handler(Handler2())
        self.assertRaises(mechanize.HTTPError, b.open,
                          "https://example.com/badreq")
        self.assertEqual(b.response().geturl(), "https://example.com/bad")
        self.assertEqual(b.request.get_full_url(),
                         "https://example.com/badreq")
        self.assertTrue(same_response(b.back(), r8))

        # .close() should make use of Browser methods and attributes complain
        # noisily, since they should not be called after .close()
        b.form = "blah"
        b.close()
        for attr in ("form open error retrieve add_handler "
                     "request response set_response geturl reload back "
                     "clear_history set_cookie links forms viewing_html "
                     "encoding title select_form click submit click_link "
                     "follow_link find_link".split()):
            self.assertTrue(getattr(b, attr) is None)

    def test_reload_read_incomplete(self):
        import mechanize
        from mechanize._response import test_response

        class Browser(TestBrowser):
            def __init__(self):
                TestBrowser.__init__(self)
                self.reloaded = False

            def reload(self):
                self.reloaded = True
                TestBrowser.reload(self)

        br = Browser()
        data = "<html><head><title></title></head><body>%s</body></html>"
        data = data % ("The quick brown fox jumps over the lazy dog." * 100)

        class Handler(mechanize.BaseHandler):
            def http_open(self, requst):
                return test_response(data, [("content-type", "text/html")])

        br.add_handler(Handler())

        # .reload() on .back() if the whole response hasn't already been read
        # (.read_incomplete is True)
        r = br.open("http://example.com")
        r.read(10)
        br.open('http://www.example.com/blah')
        self.assertFalse(br.reloaded)
        br.back()
        self.assertTrue(br.reloaded)

        # don't reload if already read
        br.reloaded = False
        br.response().read()
        br.open('http://www.example.com/blah')
        br.back()
        self.assertFalse(br.reloaded)

    def test_viewing_html(self):
        # XXX not testing multiple Content-Type headers
        url = "http://example.com/"

        for allow_xhtml in False, True:
            for ct, expect in [
                (None, False),
                ("text/plain", False),
                ("text/html", True),

                    # don't try to handle XML until we can do it right!
                ("text/xhtml", allow_xhtml),
                ("text/xml", allow_xhtml),
                ("application/xml", allow_xhtml),
                ("application/xhtml+xml", allow_xhtml),
                ("text/html; charset=blah", True),
                (" text/html ; charset=ook ", True),
            ]:
                b = TestBrowser(allow_xhtml=allow_xhtml)
                hdrs = {}
                if ct is not None:
                    hdrs["Content-Type"] = ct
                b.add_handler(make_mock_handler()([("http_open", MockResponse(
                    url, "", hdrs))]))
                b.open(url)
                self.assertEqual(b.viewing_html(), expect)

        for allow_xhtml in False, True:
            for ext, expect in [
                (".htm", True),
                (".html", True),

                    # don't try to handle XML until we can do it right!
                (".xhtml", allow_xhtml),
                (".html?foo=bar&a=b;whelk#kool", True),
                (".txt", False),
                (".xml", False),
                ("", False),
            ]:
                b = TestBrowser(allow_xhtml=allow_xhtml)
                url = "http://example.com/foo" + ext
                b.add_handler(make_mock_handler()([("http_open", MockResponse(
                    url, "", {}))]))
                b.open(url)
                self.assertEqual(b.viewing_html(), expect)

    def test_empty(self):
        import mechanize
        url = "http://example.com/"

        b = TestBrowser()

        self.assertTrue(b.response() is None)

        # To open a relative reference (often called a "relative URL"), you
        # have to have already opened a URL for it "to be relative to".
        self.assertRaises(mechanize.BrowserStateError, b.open, "relative_ref")

        # we can still clear the history even if we've not visited any URL
        b.clear_history()

        # most methods raise BrowserStateError...
        def test_state_error(method_names):
            for attr in method_names:
                method = getattr(b, attr)
                # print attr
                self.assertRaises(mechanize.BrowserStateError, method)
            self.assertRaises(
                mechanize.BrowserStateError, b.select_form, name="blah")
            self.assertRaises(
                mechanize.BrowserStateError, b.find_link, name="blah")

        # ...if not visiting a URL...
        test_state_error(("geturl reload back viewing_html encoding "
                          "click links forms title select_form".split()))
        self.assertRaises(mechanize.BrowserStateError, b.set_cookie, "foo=bar")
        self.assertRaises(mechanize.BrowserStateError, b.submit, nr=0)
        self.assertRaises(mechanize.BrowserStateError, b.click_link, nr=0)
        self.assertRaises(mechanize.BrowserStateError, b.follow_link, nr=0)
        self.assertRaises(mechanize.BrowserStateError, b.find_link, nr=0)
        # ...and lots do so if visiting a non-HTML URL
        b.add_handler(
            make_mock_handler()([("http_open", MockResponse(url, "", {}))]))
        r = b.open(url)
        self.assertTrue(not b.viewing_html())
        test_state_error("click links forms title select_form".split())
        self.assertRaises(mechanize.BrowserStateError, b.submit, nr=0)
        self.assertRaises(mechanize.BrowserStateError, b.click_link, nr=0)
        self.assertRaises(mechanize.BrowserStateError, b.follow_link, nr=0)
        self.assertRaises(mechanize.BrowserStateError, b.find_link, nr=0)

        b = TestBrowser()
        r = MockResponse(url, """<html>
<head><title>Title</title></head>
<body>
</body>
</html>
""", {"content-type": "text/html"})
        b.add_handler(make_mock_handler()([("http_open", r)]))
        r = b.open(url)
        self.assertEqual(b.title(), "Title")
        self.assertEqual(len(list(b.links())), 0)
        self.assertEqual(len(list(b.forms())), 0)
        self.assertRaises(ValueError, b.select_form)
        self.assertRaises(
            mechanize.FormNotFoundError, b.select_form, name="blah")
        self.assertRaises(
            mechanize.FormNotFoundError,
            b.select_form,
            predicate=lambda form: form is not b.global_form())
        self.assertRaises(
            mechanize.LinkNotFoundError, b.find_link, name="blah")
        self.assertRaises(
            mechanize.LinkNotFoundError, b.find_link, predicate=lambda x: True)

    def test_forms(self):
        import mechanize
        url = "http://example.com"

        b = TestBrowser()
        r = test_html_response(
            url=url,
            headers=[("content-type", "text/html")],
            data="""\
<html>
<head><title>Title</title></head>
<body>
<form name="form1">
 <input type="text"></input>
 <input type="checkbox" name="cheeses" value="cheddar"></input>
 <input type="checkbox" name="cheeses" value="edam"></input>
 <input type="submit" name="one"></input>
</form>
<a href="http://example.com/foo/bar.html" name="apples">
<form name="form2">
 <input type="submit" name="two">
</form>
</body>
</html>
""")
        b.add_handler(make_mock_handler()([("http_open", r)]))
        r = b.open(url)

        forms = list(b.forms())
        self.assertEqual(len(forms), 2)
        for got, expect in zip([f.name for f in forms], ["form1", "form2"]):
            self.assertEqual(got, expect)

        self.assertRaises(mechanize.FormNotFoundError, b.select_form, "foo")

        # no form is set yet
        self.assertRaises(AttributeError, getattr, b, "possible_items")
        b.select_form("form1")
        # now unknown methods are fed through to selected mechanize.HTMLForm
        self.assertEqual([i.name for i in b.find_control("cheeses").items],
                         ["cheddar", "edam"])
        b["cheeses"] = ["cheddar", "edam"]
        self.assertEqual(b.click_pairs(), [("cheeses", "cheddar"),
                                           ("cheeses", "edam"), ("one", "")])

        b.select_form(nr=1)
        self.assertEqual(b.name, "form2")
        self.assertEqual(b.click_pairs(), [("two", "")])

    def test_link_encoding(self):
        import mechanize
        from mechanize._rfc3986 import clean_url
        url = "http://example.com/"
        for encoding in ["UTF-8", "latin-1"]:
            encoding_decl = "; charset=%s" % encoding
            b = TestBrowser()
            r = MockResponse(url, """\
<a href="http://example.com/foo/bar&mdash;&#x2014;.html"
   name="name0&mdash;&#x2014;">blah&mdash;&#x2014;</a>
""", {"content-type": "text/html%s" % encoding_decl})
            b.add_handler(make_mock_handler()([("http_open", r)]))
            r = b.open(url)

            Link = mechanize.Link
            mdashx2 = em_dash.encode('utf-8') * 2
            qmdashx2 = clean_url(mdashx2, encoding)
            # base_url, url, text, tag, attrs
            exp = Link(
                url, "http://example.com/foo/bar%s.html" % qmdashx2,
                unicode_type("blah") + (em_dash * 2), "a",
                [("href", unicode_type("http://example.com/foo/bar%s.html") % (
                    em_dash*2)),
                 ("name", unicode_type("name0") + em_dash + em_dash)])
            # nr
            link = b.find_link()
            #             print
            #             print exp
            #             print link
            self.assertEqual(link, exp)

    def test_link_whitespace(self):
        from mechanize import Link
        base_url = "http://example.com/"
        url = "  http://example.com/foo.html%20+ "
        stripped_url = url.strip()
        html = '<a href="%s"></a>' % url
        b = TestBrowser()
        r = MockResponse(base_url, html, {"content-type": "text/html"})
        b.add_handler(make_mock_handler()([("http_open", r)]))
        r = b.open(base_url)
        link = b.find_link(nr=0)
        self.assertEqual(
            link, Link(base_url, stripped_url, "", "a", [("href", url)]))

    def test_links(self):
        import mechanize
        from mechanize import Link
        url = "http://example.com/"

        b = TestBrowser()
        r = MockResponse(url, """<html>
<head><title>Title</title></head>
<body>
<a href="http://example.com/foo/bar.html" name="apples"></a>
<a name="pears"></a>
<a href="spam" name="pears"></a>
<area href="blah" name="foo"></area>
<form name="form2">
 <input type="submit" name="two">
</form>
<iframe name="name" href="href" src="src"></iframe>
<iframe name="name2" href="href" src="src"></iframe>
<a name="name3" href="one">yada yada</a>
<a name="pears" href="two" weird="stuff">rhubarb</a>
<a></a>
<iframe src="foo"></iframe>
</body>
</html>
""", {"content-type": "text/html"})
        b.add_handler(make_mock_handler()([("http_open", r)]))
        r = b.open(url)

        exp_links = [
            # base_url, url, text, tag, attrs
            Link(url, "http://example.com/foo/bar.html", "", "a",
                 [("href", "http://example.com/foo/bar.html"),
                  ("name", "apples")]),
            Link(url, "spam", "", "a", [("href", "spam"), ("name", "pears")]),
            Link(url, "blah", '', "area", [("href", "blah"), ("name", "foo")]),
            Link(url, "src", '', "iframe",
                 [("name", "name"), ("href", "href"), ("src", "src")]),
            Link(url, "src", '', "iframe",
                 [("name", "name2"), ("href", "href"), ("src", "src")]),
            Link(url, "one", "yada yada", "a",
                 [("name", "name3"), ("href", "one")]),
            Link(url, "two", "rhubarb", "a",
                 [("name", "pears"), ("href", "two"), ("weird", "stuff")]),
            Link(url, "foo", '', "iframe", [("src", "foo")]),
        ]
        links = list(b.links())
        for got, expect in zip(links, exp_links):
            self.assertEqual(got, expect)
        self.assertEqual(len(links), len(exp_links))
        # nr
        lnk = b.find_link()
        self.assertEqual(lnk.url, "http://example.com/foo/bar.html")
        lnk = b.find_link(nr=1)
        self.assertEqual(lnk.url, "spam")
        # text
        lnk = b.find_link(text="yada yada")
        self.assertEqual(lnk.url, "one")
        self.assertRaises(
            mechanize.LinkNotFoundError, b.find_link, text="da ya")
        lnk = b.find_link(text_regex=re.compile("da ya"))
        self.assertEqual(lnk.url, "one")
        lnk = b.find_link(text_regex="da ya")
        self.assertEqual(lnk.url, "one")
        # name
        lnk = b.find_link(name="name3")
        self.assertEqual(lnk.url, "one")
        lnk = b.find_link(name_regex=re.compile("oo"))
        self.assertEqual(lnk.url, "blah")
        lnk = b.find_link(name_regex="oo")
        self.assertEqual(lnk.url, "blah")
        # url
        lnk = b.find_link(url="spam")
        self.assertEqual(lnk.url, "spam")
        lnk = b.find_link(url_regex=re.compile("pam"))
        self.assertEqual(lnk.url, "spam")
        lnk = b.find_link(url_regex="pam")
        self.assertEqual(lnk.url, "spam")
        # tag
        lnk = b.find_link(tag="area")
        self.assertEqual(lnk.url, "blah")
        # predicate
        lnk = b.find_link(
            predicate=lambda lnk: dict(lnk.attrs).get("weird") == "stuff")
        self.assertEqual(lnk.url, "two")
        # combinations
        lnk = b.find_link(name="pears", nr=1)
        self.assertEqual(lnk.text, "rhubarb")
        lnk = b.find_link(url="src", nr=0, name="name2")
        self.assertEqual(lnk.tag, "iframe")
        self.assertEqual(lnk.url, "src")
        self.assertRaises(
            mechanize.LinkNotFoundError,
            b.find_link,
            url="src",
            nr=1,
            name="name2")
        lnk = b.find_link(
            tag="a", predicate=lambda lnk: dict(lnk.attrs).get(
                "weird") == "stuff")
        self.assertEqual(lnk.url, "two")

        # .links()
        self.assertEqual(
            list(b.links(url="src")), [
                Link(
                    url,
                    url="src",
                    text='',
                    tag="iframe",
                    attrs=[("name", "name"), ("href", "href"),
                           ("src", "src")]),
                Link(
                    url,
                    url="src",
                    text='',
                    tag="iframe",
                    attrs=[("name", "name2"), ("href", "href"),
                           ("src", "src")]),
            ])

    def test_base_uri(self):
        url = "http://example.com/"

        for html, urls in [
            ("""<base href="http://www.python.org/foo/">
<a href="bar/baz.html"></a>
<a href="/bar/baz.html"></a>
<a href="http://example.com/bar %2f%2Fblah;/baz@~._-.html"></a>
""", [
                "http://www.python.org/foo/bar/baz.html",
                "http://www.python.org/bar/baz.html",
                "http://example.com/bar%20%2f%2Fblah;/baz@~._-.html",
            ]),
            ("""<a href="bar/baz.html"></a>
<a href="/bar/baz.html"></a>
<a href="http://example.com/bar/baz.html"></a>
""", [
                "http://example.com/bar/baz.html",
                "http://example.com/bar/baz.html",
                "http://example.com/bar/baz.html",
            ]),
        ]:
            b = TestBrowser()
            r = MockResponse(url, html, {"content-type": "text/html"})
            b.add_handler(make_mock_handler()([("http_open", r)]))
            r = b.open(url)
            self.assertEqual([link.absolute_url for link in b.links()], urls)

    def test_set_cookie(self):
        class CookieTestBrowser(TestBrowser):
            default_features = list(
                TestBrowser.default_features) + ["_cookies"]

        # have to be visiting HTTP/HTTPS URL
        url = "ftp://example.com/"
        br = CookieTestBrowser()
        r = mechanize.make_response(
            "<html><head><title>Title</title></head><body></body></html>",
            [("content-type", "text/html")],
            url,
            200,
            "OK", )
        br.add_handler(make_mock_handler()([("http_open", r)]))
        handler = br._ua_handlers["_cookies"]
        cj = handler.cookiejar
        self.assertRaises(mechanize.BrowserStateError, br.set_cookie,
                          "foo=bar")
        self.assertEqual(len(cj), 0)

        url = "http://example.com/"
        br = CookieTestBrowser()
        r = mechanize.make_response(
            "<html><head><title>Title</title></head><body></body></html>",
            [("content-type", "text/html")],
            url,
            200,
            "OK", )
        br.add_handler(make_mock_handler()([("http_open", r)]))
        handler = br._ua_handlers["_cookies"]
        cj = handler.cookiejar

        # have to be visiting a URL
        self.assertRaises(mechanize.BrowserStateError, br.set_cookie,
                          "foo=bar")
        self.assertEqual(len(cj), 0)

        # normal case
        br.open(url)
        br.set_cookie("foo=bar")
        self.assertEqual(len(cj), 1)
        self.assertEqual(cj._cookies["example.com"]["/"]["foo"].value, "bar")

    def test_clone_browser(self):
        from mechanize import Browser
        br = Browser()
        br.set_handle_refresh(True, max_time=237, honor_time=True)
        br.set_handle_robots(False)
        cbr = copy.copy(br)
        for h, ch in zip(br.handlers, cbr.handlers):
            self.assertIsNot(h, ch)
            self.assertIs(ch.parent, cbr)
            self.assertIs(h.__class__, ch.__class__)
        self.assertEqual(set(br._ua_handlers), set(cbr._ua_handlers))
        self.assertIs(br._ua_handlers['_cookies'].cookiejar,
                      cbr._ua_handlers['_cookies'].cookiejar)
        self.assertIsNot(br.addheaders, cbr.addheaders)
        self.assertEqual(br.addheaders, cbr.addheaders)
        self.assertIs(br.finalize_request_headers, cbr.finalize_request_headers)
        h = cbr._ua_handlers['_refresh']
        self.assertEqual((h.honor_time, h.max_time), (True, 237))

    def test_gzip(self):
        p = HTTPGzipProcessor()
        url = "https://www.example.com/"
        req = p.https_request(mechanize.Request(url))
        self.assertIsNone(req.get_header('Accept-Encoding'))
        p.request_gzip = True
        req = p.https_request(mechanize.Request(url))
        self.assertEqual(req.get_header('Accept-Encoding'), 'gzip')
        req = mechanize.Request(url)
        req.add_header('Accept-Encoding', 'moo, *')
        req = p.https_request(req)
        self.assertEqual(req.get_header('Accept-Encoding'), 'moo, *, gzip')
        data = os.urandom(1024 * 1024)
        cdata = b''.join(compress_readable_output(BytesIO(data)))
        r = MockResponse(
            url,
            data=cdata,
            info={
                'Content-Encoding': 'gzip',
                'Content-Length': str(len(cdata))
            })
        r = p.https_response(req, r)
        self.assertEqual(r.read(), data)
        h = r.info()
        self.assertFalse(h.getheaders('content-encoding'))
        self.assertFalse(h.getheaders('content-length'))


class ResponseTests(TestCase):
    def test_set_response(self):
        import copy
        from mechanize import response_seek_wrapper

        br = TestBrowser()
        url = "http://example.com/"
        html = b"""<html><body><a href="spam">click me</a></body></html>"""
        headers = {"content-type": "text/html"}
        r = response_seek_wrapper(MockResponse(url, html, headers))
        br.add_handler(make_mock_handler()([("http_open", r)]))

        r = br.open(url)
        self.assertEqual(r.read(), html)
        r.seek(0)
        self.assertEqual(copy.copy(r).read(), html)
        self.assertEqual(list(br.links())[0].url, "spam")

        newhtml = b"""<html><body><a href="eggs">click me</a></body></html>"""

        r.set_data(newhtml)
        self.assertEqual(r.read(), newhtml)
        self.assertEqual(br.response().read(), html)
        br.response().set_data(newhtml)
        self.assertEqual(br.response().read(), html)
        self.assertEqual(list(br.links())[0].url, "spam")
        r.seek(0)

        br.set_response(r)
        self.assertEqual(br.response().read(), newhtml)
        self.assertEqual(list(br.links())[0].url, "eggs")

    def test_select_form(self):
        from mechanize import _response
        br = TestBrowser()
        fp = BytesIO(b'''<html>
            <form name="a"></form>
            <form name="b" data-ac="123"></form>
            <form name="c" class="x"></form>
            </html>''')
        headers = create_response_info(
            BytesIO(b"Content-type: text/html"))
        response = _response.response_seek_wrapper(
            _response.closeable_response(fp, headers, "http://example.com/",
                                         200, "OK"))
        br.set_response(response)
        for i, n in enumerate('abc'):
            br.select_form(nr=i)
            self.assertEqual(br.form.name, n)
            br.select_form(nr=0), br.select_form(name=n)
            self.assertEqual(br.form.name, n)
        br.select_form(data_ac=re.compile(r'\d+'))
        self.assertEqual(br.form.name, 'b')
        br.select_form(class_=lambda x: x == 'x')
        self.assertEqual(br.form.name, 'c')

    def test_str(self):
        from mechanize import _response

        br = TestBrowser()
        self.assertEqual(str(br), "<TestBrowser (not visiting a URL)>")

        fp = BytesIO(b'<html><form name="f"><input /></form></html>')
        headers = create_response_info(
            BytesIO(b"Content-type: text/html"))
        response = _response.response_seek_wrapper(
            _response.closeable_response(fp, headers, "http://example.com/",
                                         200, "OK"))
        br.set_response(response)
        self.assertEqual(str(br), "<TestBrowser visiting http://example.com/>")

        br.select_form(nr=0)
        self.assertEqual(
            str(br), """\
<TestBrowser visiting http://example.com/
 selected form:
 <f GET http://example.com/ application/x-www-form-urlencoded
  <TextControl(<None>=)>>
>""")


class HttplibTests(mechanize._testcase.TestCase):
    def make_browser(self):
        class TestBrowser(mechanize.Browser):
            default_features = []
            default_schemes = ["http"]

        return TestBrowser()

    def monkey_patch_httplib(self, putheader):
        def do_nothing(*args, **kwds):
            return

        def getresponse(self_):
            class Response(object):
                msg = create_response_info(BytesIO(b""))
                status = 200
                reason = "OK"
                fp = BytesIO(b'')

                def read(self__, sz=-1):
                    return b""

                def close(self):
                    self.fp = None

                def readinto(self__, b):
                    pass

            return Response()

        self.monkey_patch(HTTPConnection, "putheader", putheader)
        self.monkey_patch(HTTPConnection, "connect", do_nothing)
        self.monkey_patch(HTTPConnection, "send", do_nothing)
        self.monkey_patch(HTTPConnection, "close", do_nothing)
        self.monkey_patch(HTTPConnection, "getresponse", getresponse)

    def test_add_host_header(self):
        headers = []

        def putheader(self_, header, value):
            headers.append((header, value))

        self.monkey_patch_httplib(putheader)
        browser = self.make_browser()
        request = mechanize.Request("http://example.com/")
        browser.addheaders = [("Host", "myway.example.com")]
        browser.finalize_request_headers = lambda req, headers: headers.__setitem__('Test-Header', 'Yay')
        browser.open(request)
        self.assertIn(("Host", "myway.example.com"), headers)
        self.assertIn(("Test-Header", "Yay"), headers)

    def test_misc_browser_tests(self):

        class TestHttpHandler(mechanize.BaseHandler):
            def http_open(self, request):
                return mechanize._response.test_response(
                        url=request.get_full_url())

        class TestHttpBrowser(TestBrowser2):
            handler_classes = TestBrowser2.handler_classes.copy()
            handler_classes["http"] = TestHttpHandler
            default_schemes = ["http"]

        def response_impl(response):
            return response.wrapped.fp.__class__.__name__

        br = TestHttpBrowser()
        r = br.open("http://example.com")
        self.assertEqual('BytesIO', response_impl(r))
        r2 = br.open("http://example.com")
        self.assertEqual('BytesIO', response_impl(r2))
        self.assertEqual('eofresponse', response_impl(r))
        br.set_response(mechanize._response.test_response())
        self.assertEqual('eofresponse', response_impl(r2))

        br = TestHttpBrowser()
        r = br.open("http://example.com")
        r2 = mechanize._response.test_response(url="http://example.com/2")
        self.assertEqual(response_impl(r2), 'BytesIO')
        br.visit_response(r2)
        self.assertEqual(response_impl(r), 'eofresponse')
        self.assertEqual(br.geturl(), br.request.get_full_url())
        self.assertEqual(br.geturl(), "http://example.com/2")
        br.back()
        self.assertEqual(br.geturl(), br.request.get_full_url())
        self.assertEqual(br.geturl(), "http://example.com")

        class ReloadCheckBrowser(TestHttpBrowser):
            reloaded = False

            def reload(self):
                self.reloaded = True
                return TestHttpBrowser.reload(self)

        br = ReloadCheckBrowser()
        old = br.open("http://example.com")
        br.open("http://example.com/2")
        new = br.back()
        self.assertTrue(br.reloaded)
        self.assertIsNot(new.wrapped, old.wrapped)

        br = TestBrowser2()
        self.assertRaises(ValueError, br.set_response, 'blah')
        self.assertRaises(ValueError, br.set_response, BytesIO())
        self.assertRaises(mechanize.URLError, br.open, "http://example.com")
        self.assertRaises(mechanize.URLError, br.reload)

        br = TestBrowser2()
        br.add_handler(make_mock_handler(mechanize._response.test_response)([("http_open", None)]))

        self.assertIsNone(br.response())
        self.assertEqual(len(br._history._history), 0)
        br.open("http://example.com/1")
        self.assertIsNotNone(br.response())
        self.assertEqual(len(br._history._history), 0)
        br.clear_history()
        self.assertIsNotNone(br.response())
        self.assertEqual(len(br._history._history), 0)
        br.open("http://example.com/2")
        br.response() is not None
        self.assertIsNotNone(br.response())
        self.assertEqual(len(br._history._history), 1)
        br.clear_history()
        self.assertIsNotNone(br.response())
        self.assertEqual(len(br._history._history), 0)

        from test.test_urllib2 import MockHTTPHandler

        def make_browser_with_redirect():
            br = TestBrowser2()
            hh = MockHTTPHandler(302, "Location: http://example.com/\r\n\r\n")
            br.add_handler(hh)
            br.add_handler(mechanize.HTTPRedirectHandler())
            return br

        def test_state(br):
            self.assertIsNone(br.request)
            self.assertIsNone(br.response())
            self.assertRaises(mechanize.BrowserStateError, br.back)

        br = make_browser_with_redirect()
        test_state(br)
        req = mechanize.Request("http://example.com")
        req.visit = False
        br.open(req)
        test_state(br)

        br = make_browser_with_redirect()
        test_state(br)

        req = mechanize.Request("http://example.com")
        self.assertIsNone(req.visit)
        br.open_novisit(req)
        test_state(br)
        self.assertFalse(req.visit)

        def test_one_visit(handlers):
            br = TestBrowser2()
            for handler in handlers:
                br.add_handler(handler)
            req = mechanize.Request("http://example.com")
            req.visit = True
            br.open(req)
            return br

        def test_state(br):
            # XXX the _history._history check is needed because of the weird
            # throwing-away of history entries by .back() where response is
            # None, which makes the .back() check insufficient to tell if a
            # history entry was .add()ed.  I don't want to change this until
            # post-stable.
            self.assertTrue(br.response())
            self.assertTrue(br.request)
            self.assertEqual(len(br._history._history), 0)
            self.assertRaises(mechanize.BrowserStateError, br.back)

        from test.test_urllib2 import HTTPRedirectHandler
        hh = MockHTTPHandler(302, "Location: http://example.com/\r\n\r\n")
        br = test_one_visit([hh, HTTPRedirectHandler()])
        test_state(br)

        class MockPasswordManager:

            def add_password(self, realm, uri, user, password):
                pass

            def find_user_password(self, realm, authuri):
                return '', ''

        ah = mechanize.HTTPBasicAuthHandler(MockPasswordManager())
        hh = MockHTTPHandler(
            401, 'WWW-Authenticate: Basic realm="realm"\r\n\r\n')
        test_state(test_one_visit([hh, ah]))
        ph = mechanize.ProxyHandler(dict(http="proxy.example.com:3128"))
        ah = mechanize.ProxyBasicAuthHandler(MockPasswordManager())
        hh = MockHTTPHandler(
            407, 'Proxy-Authenticate: Basic realm="realm"\r\n\r\n')
        test_state(test_one_visit([ph, hh, ah]))

        from mechanize._response import test_response
        br = TestBrowser2()
        html = b"""\
        <html><body>
        <input type="text" name="a" />
        <form><input type="text" name="b" /></form>
        </body></html>
        """
        response = test_response(html, headers=[("Content-type", "text/html")])
        self.assertRaises(mechanize.BrowserStateError, br.global_form)
        br.set_response(response)
        self.assertEqual(str(br.global_form().find_control(nr=0).name), 'a')
        self.assertEqual(len(list(br.forms())), 1)
        self.assertEqual(str(next(iter(br.forms())).find_control(nr=0).name), 'b')

        from mechanize._response import test_html_response
        br = TestBrowser2()
        br.visit_response(test_html_response(b"""\
<html><head><title></title></head><body>
<input type="text" name="a" value="b"></input>
<form>
    <input type="text" name="p" value="q"></input>
</form>
</body></html>"""))

        def has_a(form):
            try:
                form.find_control(name="a")
            except mechanize.ControlNotFoundError:
                return False
            else:
                return True
        br.select_form(predicate=has_a)
        self.assertEqual(str(br.form.find_control(name="a").value), 'b')


if __name__ == "__main__":
    import unittest
    unittest.main()
