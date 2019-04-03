#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dappy` package."""


import unittest
import requests_mock
from dappy import API, Endpoint
from dappy.formatters import json_formatter
from dappy.methods import GET, POST
from dappy.exceptions import JSONNotSupportedException


class TestDappy(unittest.TestCase):
    """Tests for `dappy` package."""

    def setUp(self):
        self.TestAPI = API('jsonplaceholder.typicode.com', [
            Endpoint('posts', '/posts', methods=[GET, POST])
        ], formatter=json_formatter)

        # formatter=json_formatter so we can check for exceptions and mocking later
        self.NonJSONAPI = API('www.google.com', [
            Endpoint('home', '/')
        ], formatter=json_formatter)

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_get(self):
        self.assertTrue(self.TestAPI.posts.get() is not None)

    def test_post(self):
        self.assertTrue(self.TestAPI.posts.post({}) is not None)

    def test_json_exception(self):
        self.assertRaises(JSONNotSupportedException, self.NonJSONAPI.home)

    # This test passes if we mock JSON on top of the NonJSONAPI and it doesn't throw
    # a JSONNotSupportedException
    @requests_mock.mock()
    def test_mock(self, mock):
        mock.get('https://www.google.com/', json={'data': 'data'})
        self.assertTrue(self.NonJSONAPI.home() is not None)
