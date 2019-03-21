from functools import partial
from unittest import TestCase

from stackifyapm.utils import get_name_from_path
from stackifyapm.utils import get_name_from_func
from stackifyapm.utils import build_name_with_http_method_prefix
from stackifyapm.utils import get_url_data
from stackifyapm.utils import get_method_name


class GetNameFromPathTest(TestCase):
    def test_should_return_normal_path(self):
        path = 'somepath'

        res = get_name_from_path(path)

        assert res == 'somepath'

    def test_should_return_normalized_path(self):
        path = '/somepath'

        res = get_name_from_path(path)

        assert res == 'somepath'


class GetNameFromFunctionTest(TestCase):
    def test_should_return_name_from_function(self):
        def foo():
            pass

        res = get_name_from_func(foo)

        assert res == 'stackifyapm.utils.tests.test_init.foo'

    def test_should_return_name_from_function_class(self):
        class Bar(object):
            def foo(self):
                pass

        res = get_name_from_func(Bar.foo)

        assert res == 'stackifyapm.utils.tests.test_init.foo'

    def test_should_return_name_from_function_class_instance(self):
        class Bar(object):
            def foo(self):
                pass

        res = get_name_from_func(Bar().foo)

        assert res == 'stackifyapm.utils.tests.test_init.foo'

    def test_should_return_name_from_partial(self):
        def foo(bar):
            pass

        res = get_name_from_func(partial(foo, "bar"))

        assert res == 'partial(stackifyapm.utils.tests.test_init.foo)'

    def test_should_return_name_from_lambda(self):
        res = get_name_from_func(lambda x: x)

        assert res == 'stackifyapm.utils.tests.test_init.<lambda>'


class Request(object):
    method = 'METHOD'


class BuildNameWithHTTPMethodPrefixTest(TestCase):
    def test_should_return_name(self):
        request = Request()
        name = 'somename'

        res = build_name_with_http_method_prefix(name, request)

        assert res == 'METHOD somename'

    def test_should_return_empty_name(self):
        request = Request()
        name = ''

        res = build_name_with_http_method_prefix(name, request)

        assert res == ''


class GetURLDataTest(TestCase):
    def test_should_return_url_data_http(self):
        url = 'http://some.url.com'

        res = get_url_data(url)

        assert res['full'] == 'http://some.url.com'
        assert res['hostname'] == 'some.url.com'
        assert res['protocol'] == 'http:'

    def test_should_return_url_data_https(self):
        url = 'https://some.url.com'

        res = get_url_data(url)

        assert res['full'] == 'https://some.url.com'
        assert res['hostname'] == 'some.url.com'
        assert res['protocol'] == 'https:'


class GetMethodName(TestCase):
    def test_should_return_string_method_name(self):
        method_string = 'METHOD'

        res = get_method_name(method_string)

        assert res == 'METHOD'

    def test_should_return_method_bane(self):
        def foo():
            pass

        res = get_method_name(foo)

        assert res == 'foo'

    def test_should_return_class_method_bane(self):
        class Bar(object):
            def foo(self):
                pass

        res = get_method_name(Bar.foo)

        assert res == 'foo'
