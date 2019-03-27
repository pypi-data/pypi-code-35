# -*- coding: utf-8 -*-

import logging
import os

import pytest
import requests

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from promium.assertions import WebDriverSoftAssertion, RequestSoftAssertion
from promium.core.common import get_screenshot
from promium.core.exceptions import PromiumException
from promium.core.support.settings import SettingsDrivers
from promium.device_config import CHROME_DESKTOP_1920_1080
from promium.logger import request_logging, logger_for_loading_page


log = logging.getLogger(__name__)

ENV_VAR = 'SE_DRIVER'
ENV_GRID = 'GRID_HOST'

DRIVERS = {
    'firefox': 'Firefox',
    'chrome': 'Chrome',
    'opera': 'Opera',
    'ie': 'IE',
    'edge': 'Edge'
}


def create_driver(device):
    """
    Examples SE_DRIVER:
        - 'chrome'
        - 'firefox'
        - 'opera'
        - 'ie'
        - 'edge'
    Examples GRID_HOST:
        - http://localhost:4444/wd/hub
        - htpp://se-grid.my:4444/wd/hub
        - htpp://selenoid:4444/wd/hub
    """
    driver = os.environ.get(ENV_VAR)
    grid_host = os.environ.get(ENV_GRID)
    if not driver:
        raise ValueError(
            u'Need choice Selenium WebDriver: {}'.format(DRIVERS.keys())
        )

    settings = SettingsDrivers.get(driver)
    settings.set_device(*device)
    if driver in DRIVERS and not grid_host:
        if driver == "chrome":
            return webdriver.Chrome(
                executable_path=settings.binary_path,
                chrome_options=settings.get_options(),
                desired_capabilities=settings.get_capabilities(),
            )
        elif driver == "firefox":
            return webdriver.Firefox(
                executable_path=settings.binary_path,
                firefox_profile=settings.get_preferences(),
                firefox_options=settings.get_options(),
                capabilities=settings.get_capabilities(),
            )
        elif driver == "opera":
            return webdriver.Opera(
                executable_path=settings.binary_path,
                options=settings.get_options(),
                desired_capabilities=settings.get_capabilities(),
            )
        elif driver == "ie":
            return webdriver.Ie(
                executable_path=settings.binary_path,
                options=settings.get_options(),
                capabilities=settings.get_capabilities(),
            )
        elif driver == "edge":
            return webdriver.Edge(
                executable_path=settings.binary_path,
                capabilities=settings.get_capabilities(),
            )
        return getattr(webdriver, DRIVERS[driver])()

    elif 'http' in grid_host:
        capabilities = settings.get_options().to_capabilities()
        if capabilities is None:
            raise ValueError(u'Unknown client specified: {}'.format(driver))

        capabilities.update(settings.get_capabilities())
        try:
            driver = webdriver.Remote(
                command_executor=grid_host,
                desired_capabilities=capabilities,
                browser_profile=settings.get_preferences()
            )
        except WebDriverException:
            log.warning(u"[SETUP] Second try for remote driver connection.")
            driver = webdriver.Remote(
                command_executor=grid_host,
                desired_capabilities=capabilities,
                browser_profile=settings.get_preferences()
            )
        return driver

    raise ValueError(
        u'Unknown driver specified: "{}", "{}"'.format(driver, grid_host)
    )


class TestCase(object):
    test_case_url = None
    assertion_errors = None
    path_to_test = None

    def get_path_to_test(self, method):
        return u"{path}.py -k {test_name}".format(
            path=u'/'.join(str(self.__module__).split(u'.')[1:]),
            test_name=method.__name__
        )

    def get_failed_test_command(self, name):
        if name == 'pytest':
            command = 'py.test'
        elif name == 'vagga':
            command = 'vagga run-tests --'
        else:
            raise PromiumException('Name must be "pytest" or "vagga"')
        return (
            u"{command} {path_to_test} --fail-debug-info --capturelog".format(
                command=command,
                path_to_test=self.path_to_test
            )
        )


class WebDriverTestCase(TestCase, WebDriverSoftAssertion):
    driver = None
    device = CHROME_DESKTOP_1920_1080  # default data
    excluded_browser_console_errors = []

    @logger_for_loading_page
    def get_url(self, url):
        self.driver.get(url)

    def check_console_errors(self):
        if hasattr(self.driver, "console_errors"):
            if self.driver.console_errors:
                browser_console_errors = self.driver.console_errors
                if self.excluded_browser_console_errors:
                    try:
                        return list(map(
                            lambda x: x, list(filter(
                                lambda x: x if not list(filter(
                                    lambda e: (
                                        True if e["msg"] in x and e["comment"]
                                        else False
                                    ),
                                    self.excluded_browser_console_errors
                                )) else None, browser_console_errors
                            ))
                        ))
                    except Exception as e:
                        raise PromiumException(
                            u"Please check your excluded errors list. "
                            u"Original exception is: %s" % e.message
                        )
                return browser_console_errors
        return []

    def setup_method(self, method):
        self.assertion_errors = []
        self.path_to_test = self.get_path_to_test(method)
        pytest.config.get_fail_debug = self.get_fail_debug
        pytest.config.assertion_errors = self.assertion_errors
        pytest.config.check_console_errors = self.check_console_errors
        if hasattr(method, 'device'):
            self.device = method.device.args[0]
        self.driver = create_driver(self.device)
        self.driver.console_errors = []
        if (
            'ie' not in os.environ['SE_DRIVER'] and
            'opera' not in os.environ['SE_DRIVER']
        ):
            self.driver.set_window_size(self.device.width, self.device.height)

    def teardown_method(self, method):
        self.driver.console_errors = []
        if self.driver:
            self.driver.quit()
        # TODO need fix
        # if not self.test_case_url and CHECK_TEST_CASE:
        #     raise PromiumException("Test don't have a test case url.")

    def get_fail_debug(self):
        """Failed test report generator"""
        alerts = 0
        try:
            while self.driver.switch_to.alert:
                alert = self.driver.switch_to.alert
                print(u'Unexpected ALERT: %s\n' % alert.text)
                alerts += 1
                alert.dismiss()
        except:
            if alerts != 0:
                print(u'')
            pass
        url = self.driver.current_url
        screenshot = get_screenshot(self.driver)
        pytest_failed_test_command = self.get_failed_test_command('pytest')
        vagga_failed_test_command = self.get_failed_test_command('vagga')
        return (
            'webdriver',
            url,
            screenshot,
            self.test_case_url,
            pytest_failed_test_command,
            vagga_failed_test_command
        )


class RequestTestCase(TestCase, RequestSoftAssertion):
    session = None

    def setup_method(self, method):
        self.path_to_test = self.get_path_to_test(method)
        self.session = requests.session()
        self.session.url = (
            u'Use self.get_response(url) for request tests or '
            u'util methods for api tests!'
        )
        self.assertion_errors = []
        pytest.config.assertion_errors = self.assertion_errors
        pytest.config.get_fail_debug = self.get_fail_debug

    def teardown_method(self, method):
        if self.session:
            self.session.close()
        # TODO need fix
        # if not self.test_case_url and CHECK_TEST_CASE:
        #     raise PromiumException("Test don't have a test case url.")

    def get_fail_debug(self):
        """Failed test report generator"""
        if not hasattr(self.session, 'status_code'):
            self.session.status_code = None
        pytest_failed_test_command = self.get_failed_test_command('pytest')
        vagga_failed_test_command = self.get_failed_test_command('vagga')
        return (
            u'request',
            self.session.url,
            self.session.status_code,
            self.test_case_url,
            pytest_failed_test_command,
            vagga_failed_test_command
        )

    def get_response(self, url, timeout=10, **kwargs):
        self.session.url = url
        self.session.status_code = None
        response = self.session.get(
            url,
            timeout=timeout,
            verify=False,
            hooks=dict(response=request_logging),
            **kwargs
        )
        self.session.status_code = response.status_code
        return response
