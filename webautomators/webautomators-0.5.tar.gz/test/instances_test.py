# -*- coding: utf-8 -*-

from unittest import TestCase
from webautomators import WebChromeDriver
from webdriver_manager.chrome import ChromeDriverManager

class TestInstancesChrome(TestCase):

    def setUp(self):
        self.driver = WebChromeDriver()
    
    def test_get_url(self):
        self.driver.navigate('http://google.com.br')
        self.driver.assert_title('Google')
       
    
    def tearDown(self):
        self.driver.close_browser()
