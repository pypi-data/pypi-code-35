# -*- coding: utf-8 -*-

"""
    apimaticcalculatorpythonv7Demo

    This file was automatically generated for testing by APIMATIC v2.0 ( https://apimatic.io ).
"""

import unittest
from ..http_response_catcher import HttpResponseCatcher
from apimaticcalculatorpythonv7Demo.apimaticcalculatorpythonv7_demo_client import Apimaticcalculatorpythonv7DemoClient
from apimaticcalculatorpythonv7Demo.configuration import Configuration

class ControllerTestBase(unittest.TestCase):

    """All test classes inherit from this base class. It abstracts out
    common functionality and configuration variables set up."""

    @classmethod
    def setUpClass(cls):
        """Class method called once before running tests in a test class."""
        cls.api_client = Apimaticcalculatorpythonv7DemoClient()
        cls.request_timeout = 30
        cls.assert_precision = 0.01


    def setUp(self):
        """Method called once before every test in a test class."""
        self.response_catcher = HttpResponseCatcher()
        self.controller.http_call_back =  self.response_catcher

    