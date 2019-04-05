import os
import pytest
import logging
import time
import uuid
import threading
import requests
import traceback
import asyncio

from urllib.parse import urlsplit
from mitmproxy import proxy, options
from pylons import config
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.opera.options import Options as OperaOptions
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.remote.remote_connection import RemoteConnection

from promium.assertions import (
    WebDriverSoftAssertion,
    RequestSoftAssertion
)
from promium.core.exceptions import PromiumException
from promium.device_config import CHROME_DESKTOP_1920_1080
from promium.logger import (
    request_logging,
    logger_for_loading_page
)
from promium.core.common import upload_screenshot
from promium.kibana_search import get_kibana_link_for_one_test

from promium.proxy_config import (
    MyServer, IntrospectionMaster, ALL_SKIPPED_HOSTS, _get_port, _get_addr
)


TEST_PROJECT = os.environ.get('TEST_PROJECT')
FREEZE_TEST_STATE = os.environ.get('FREEZE_TEST_STATE')
DOMAIN_NAME = config.get("domain_name").lower().split('.')[0]

log = logging.getLogger(__name__)

ENV_VAR = 'SE_DRIVER'

DRIVERS = {
    'firefox': 'Firefox',
    'chrome': 'Chrome',
    'safari': 'Safari',
    'opera': 'Opera',
    'ie': 'Ie',
}

MAX_LOAD_TIME = 10
PARENT_PROXY_HOST = "172.18.30.222"
PARENT_PROXY_PORT = 3128

DOWNLOAD_PATH = "/tmp"


RemoteConnection.set_timeout(timeout=180)


def is_freeze():
    return True if FREEZE_TEST_STATE in ("true", "t", "True", "1") else False


def get_chrome_opera_options(options, device, proxy_server, is_headless=False):
    if proxy_server:
        options.add_argument(f"--proxy-server={proxy_server}")
    # options.add_argument("--allow-running-insecure-content")
    if is_headless:
        options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--no-first-run")
    options.add_argument("--verbose")
    options.add_argument("--enable-logging --v=1")
    options.add_argument("--test-type")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-gpu")
    options.add_argument(f"--window-size={device.width},{device.height}")
    prefs = {
        "download.default_directory": DOWNLOAD_PATH,
        "download.directory_upgrade": True,
        'prompt_for_download': False
    }
    options.add_experimental_option("prefs", prefs)
    if device.user_agent:
        options.add_argument(f"--user-agent={device.user_agent}")
        if device.device_name:
            mobile_emulation = {"deviceName": device.device_name}
            options.add_experimental_option(
                "mobileEmulation", mobile_emulation
            )
    return options


def get_chrome_options(device, proxy_server=None, is_headless=False):
    options = ChromeOptions()
    chrome_options = get_chrome_opera_options(
        options, device, proxy_server, is_headless
    )
    return chrome_options


def get_opera_options(device, proxy_server=None):
    options = OperaOptions()
    opera_options = get_chrome_opera_options(options, device, proxy_server)
    opera_options.add_extension("/work/uaprom/res/WebSigner_v1.0.8.crx")
    opera_options.binary_location = '/usr/bin/opera'
    return opera_options


def get_firefox_profile(device):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.startup.homepage", "about:blank")
    profile.set_preference("startup.homepage_welcome_url", "about:blank")
    profile.set_preference(
        "startup.homepage_welcome_url.additional", "about:blank"
    )
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", DOWNLOAD_PATH)
    profile.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        "application/zip"
    )
    profile.set_preference("pdfjs.disabled", True)

    FIREBUG_PATH = os.environ.get("FIREBUG_PATH")
    if FIREBUG_PATH and os.path.exists(FIREBUG_PATH):
        profile.add_extension(FIREBUG_PATH)
        profile.set_preference("extensions.firebug.allPagesActivation", "on")
        profile.set_preference("extensions.firebug.console.enableSites", "on")
        profile.set_preference(
            "extensions.firebug.defaultPanelName", "console"
        )
        profile.set_preference(
            "extensions.firebug.console.defaultPersist", "true"
        )
        profile.set_preference(
            "extensions.firebug.consoleFilterTypes", "error"
        )
        profile.set_preference("extensions.firebug.showFirstRunPage", False)
        profile.set_preference("extensions.firebug.cookies.enableSites", True)
    if device.user_agent:
        profile.set_preference("general.useragent.override", device.user_agent)
    profile.update_preferences()
    return profile


def get_firefox_options(device):
    """Function available if selenium version > 2.53.0"""
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("-no-remote")
    firefox_options.add_argument(f"-width {device.width}")
    firefox_options.add_argument(f"-height {device.height}")
    return firefox_options


def create_driver(device, proxy_server=None, env_var=ENV_VAR, default=None):
    """
    Examples:

        - 'chrome://'
        - 'firefox://'
        - 'opera://'
        - 'http+chrome://host:port/wd/hub'

    """
    is_headless = True if os.environ.get("HEADLESS") == "Enabled" else False
    browser_profile = None
    proxy_capabilities = Proxy(
        {
            "proxyType": ProxyType.DIRECT  # for debug besida tests
        }
    )
    certs = {
        'acceptSslCerts': True,
        'acceptInsecureCerts': True
    }

    driver_dsn = os.environ.get(env_var) or default
    if not driver_dsn:
        raise RuntimeError(f'Selenium WebDriver is not set in the {env_var} '
                           f'environment variable')

    try:
        scheme, netloc, url, _, _ = urlsplit(driver_dsn)
    except ValueError:
        raise ValueError(f'Invalid url: {driver_dsn}')

    if scheme in DRIVERS:
        if scheme == "chrome":
            chrome_options = get_chrome_options(
                device, proxy_server, is_headless
            )
            return webdriver.Chrome(
                chrome_options=chrome_options,
                desired_capabilities=certs if is_headless else None
            )
        elif scheme == "firefox":
            return webdriver.Firefox(
                firefox_profile=get_firefox_profile(device),
                firefox_options=get_firefox_options(device)
            )
        elif scheme == "opera":
            return webdriver.Opera(options=get_opera_options(device))
        return getattr(webdriver, DRIVERS[scheme])()
    elif scheme.startswith('http+'):
        proto, _, client = scheme.partition('+')
        if not netloc:
            raise ValueError(f'Network address is not specified: {driver_dsn}')

        capabilities = getattr(DesiredCapabilities, client.upper(), None)
        capabilities["loggingPrefs"] = {
            "performance": "ALL", "server": "ALL", "client": "ALL",
            "driver": "ALL", "browser": "ALL"
        }
        if capabilities is None:
            raise ValueError(f'Unknown client specified: {client}')

        remote_url = f'{proto}://{netloc}{url}'
        command_executor = RemoteConnection(
            remote_url, keep_alive=False, resolve_ip=False
        )
        if client == "chrome":
            chrome_options = get_chrome_options(
                device, proxy_server, is_headless
            )
            chrome_options.add_argument("--disable-dev-shm-usage")
            capabilities.update(chrome_options.to_capabilities())
            if is_headless:
                capabilities.update(certs)
        elif client == "firefox":
            capabilities.update(get_firefox_options(device).to_capabilities())
            browser_profile = get_firefox_profile(device)
        elif client == "opera":
            capabilities.update(get_opera_options(device).to_capabilities())
            capabilities["browserName"] = "opera"
        if proxy_server:
            proxy_capabilities = Proxy(
                {
                    "httpProxy": proxy_server,
                    'sslProxy': proxy_server,
                    'noProxy': None,
                    "proxyType": ProxyType.MANUAL
                }
            )
        try:
            driver = webdriver.Remote(
                proxy=proxy_capabilities,
                command_executor=command_executor,
                desired_capabilities=capabilities,
                browser_profile=browser_profile
            )
        except WebDriverException:
            log.warning("[SETUP] Second attempt for remote driver connection.")
            driver = webdriver.Remote(
                proxy=proxy_capabilities,
                command_executor=command_executor,
                desired_capabilities=capabilities,
                browser_profile=browser_profile
            )
        return driver

    raise ValueError(f'Unknown driver specified: {driver_dsn}')


class TDPException(Exception):

    def __init__(self, *args):
        self.message = (
            "exception caught during execution test data preparing.\n"
            "Look at the original traceback:\n\n%s\n"
        ) % ("".join(traceback.format_exception(*args)))

    def __str__(self):
        return self.message


class TDPHandler:
    """
    TDP - Test Data Preparation
    context manager for handling any exception
    during execution test data preparing.
    We need to raise a specific custom exceptions.
    """

    def __init__(self):
        pass

    def __enter__(self):
        log.info("[TDP] Start test data preparing...")
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        log.info("[TDP] Finish test data preparing")
        if exc_type:
            raise TDPException(exc_type, exc_value, exc_tb)
        return


class TestCase(object):
    xrequestid = None
    test_case_url = None
    assertion_errors = None
    use_russian_blocked_sites = False

    def tdp_handler(self):
        """
        Use this context manager for prepare of test data only,
        not for business logic!
        """
        return TDPHandler()

    @property
    def freeze(self):
        return is_freeze()

    def get_random_16byte_string(self):
        txid = str(uuid.uuid4())
        log.info("[SETUP] txid: %s" % txid)
        return txid

    def get_kibana_link(self):
        attempts = 16  # 8 seconds
        while attempts:
            result = get_kibana_link_for_one_test(self.xrequestid)
            if result:
                self.xrequestid = None
                return result
            time.sleep(.5)
            attempts -= 1
        self.xrequestid = None

    def get_path_to_test(self, method):
        path = '/'.join(str(self.__class__).split('.')[1:-1])
        return f"{path}.py -k {method.__name__}"

    def get_failed_test_command(self):
        if TEST_PROJECT:
            enviroment = TEST_PROJECT
            local = '-local'
            if TEST_PROJECT in [
                'ua-trunk', 'ru-trunk', 'kz-trunk',
                'ua-stable', 'ru-stable', 'kz-stable'
            ]:
                local = ''
        else:
            if DOMAIN_NAME in ['tiu', 'satu', 'prom', 'deal']:
                enviroment = DOMAIN_NAME
                local = '-production'
                if self.path_to_test.split('/')[2] == 'bigl':
                    enviroment = 'bigl'
        return (
            f"vagga se --{enviroment}{local} "
            f"-- uaprom/{self.path_to_test} --capturelog --fail-debug-info"
        )


class WebDriverTestCase(TestCase, WebDriverSoftAssertion):
    driver = None
    device = CHROME_DESKTOP_1920_1080  # default data
    excluded_browser_console_errors = []

    use_proxy = False
    not_use_proxy_anyway = False
    proxy_server = None
    proxy_master = None
    lock = threading.Lock()

    ALLOWED_HOSTS = []
    SKIPPED_HOSTS = []

    def start_proxy(self):
        try:
            self.lock.acquire()
            port = _get_port()
            addr = _get_addr()
            self.proxy_server = f"{addr}:{port}"

            opts = options.Options(
                listen_port=port,
                listen_host=addr,
                showhost=True,
                ssl_insecure=True
            )
            config = proxy.config.ProxyConfig(opts)
            current_skipped_hosts = (
                self.SKIPPED_HOSTS if self.SKIPPED_HOSTS else ALL_SKIPPED_HOSTS
            )
            server = MyServer(config, disabled_addresses=frozenset(
                (x, 443) for x in current_skipped_hosts
                if x not in self.ALLOWED_HOSTS
            ))

            loop = asyncio.new_event_loop()
            self._loop = loop
            self.proxy_master = IntrospectionMaster(
                opts, server,
                allowed_hosts=self.ALLOWED_HOSTS,
                skipped_hosts=current_skipped_hosts,
                xrequestid=self.xrequestid
            )
            self.proxy_master.channel.loop = loop

            def proxy_thread():
                asyncio.set_event_loop(self.proxy_master.channel.loop)
                self.proxy_master.run()

            self.proxy_thread = threading.Thread(target=proxy_thread)
            self.proxy_thread.start()

        except Exception as e:
            print(f"[WARNING] Could not start proxy because of {e}")
            log.info("[SETUP] Caught Exception: %s" % str(e))
            log.info("[SETUP] It can't start proxy :(")
            pass
        finally:
            self.lock.release()

    @logger_for_loading_page
    def get_url(self, url, cleanup=True):
        self.driver.get(url)
        if cleanup:
            try:
                self.driver.execute_script(
                    'localStorage.clear()'
                )
            except WebDriverException:
                pass
        # TODO uncomment if proxy will not set cookie
        # add_xrequestid_in_cookie(self.driver)
        return url

    def check_console_errors(self):

        if hasattr(self.driver, "console_errors"):
            if self.driver.console_errors:
                browser_console_errors = self.driver.console_errors
                if self.excluded_browser_console_errors:
                    try:
                        return list(map(
                            lambda x: x, filter(
                                lambda x: x if not filter(
                                    lambda e: (
                                        True if e["msg"] in x and e["comment"]
                                        else False
                                    ),
                                    self.excluded_browser_console_errors
                                ) else None, browser_console_errors
                            )
                        ))
                    except Exception as e:
                        raise PromiumException(
                            "Please check your excluded errors list. "
                            "Original exception is: %s" % e
                        )
                return browser_console_errors
        return []

    def setup_method(self, method):
        self.xrequestid = self.get_random_16byte_string()
        self.assertion_errors = []
        self.path_to_test = self.get_path_to_test(method)
        pytest.config.get_fail_debug = self.get_fail_debug
        pytest.config.assertion_errors = self.assertion_errors
        pytest.config.check_console_errors = self.check_console_errors
        pytest.config.get_kibana_link = self.get_kibana_link
        pytest.config.get_screenshot_png = self.get_screenshot_png

        if os.environ.get("USE_PROXY") == "Enabled" and (
                not self.not_use_proxy_anyway):
            self.use_proxy = True
            self.start_proxy()

        if hasattr(method, 'device'):
            self.device = method.device.args[0]

        try:
            self.driver = create_driver(
                self.device, proxy_server=self.proxy_server
            )
            self.driver.xrequestid = self.xrequestid
            self.driver.console_errors = []
        except WebDriverException as e:
            msg_exited_abnormally = (
                "failed to start: exited abnormally"
            )
            if msg_exited_abnormally in e.msg:
                pytest.xfail(msg_exited_abnormally)
            else:
                raise e

    def teardown_method(self, method):

        self.xrequestid = None
        self.driver.console_errors = []

        if self.driver:
            self.driver.xrequestid = None
            try:
                self.driver.quit()
            except WebDriverException as e:
                log.error(
                    "[PROMIUM] Original webdriver exception: %s" % e
                )
        if self.use_proxy and self.proxy_master:
            self.proxy_master.shutdown()
            self.proxy_thread.join()
            self._loop.close()

        if not self.test_case_url:
            raise PromiumException("Test don't have a test case url.")

    def get_screenshot_png(self):
        return self.driver.get_screenshot_as_png()

    def get_fail_debug(self, only_info=False):
        """Failed test report generator"""

        failed_test_command = self.get_failed_test_command()

        if only_info:
            return (self.test_case_url, self.xrequestid, failed_test_command)

        alerts = 0
        try:
            while self.driver.switch_to.alert:
                alert = self.driver.switch_to.alert
                print('Unexpected ALERT: %s\n' % alert.text)
                alerts += 1
                alert.dismiss()
        except Exception:
            if alerts != 0:
                print('')
            pass
        url = self.driver.current_url
        screenshot = upload_screenshot(self.driver)
        # node_id = get_grid_node_id(
        #     self.driver.session_id,
        #     self.driver.command_executor._url
        # )
        return (
            url,
            screenshot,
            self.test_case_url,
            # node_id,
            self.xrequestid,
            failed_test_command
        )


class RequestTestCase(TestCase, RequestSoftAssertion):
    session = None
    proxies = {}

    def setup_method(self, method):
        if self.use_russian_blocked_sites:
            proxy = f"http://{PARENT_PROXY_HOST}:{PARENT_PROXY_PORT}"
            self.proxies = {"http": proxy, "https": proxy}
        self.xrequestid = self.get_random_16byte_string()
        self.session = requests.session()
        self.session.url = (
            'Use self.get_response(url) for request tests or '
            'util methods for api tests!'
        )
        self.path_to_test = self.get_path_to_test(method)
        self.assertion_errors = []
        pytest.config.assertion_errors = self.assertion_errors
        pytest.config.get_fail_debug = self.get_fail_debug
        pytest.config.get_kibana_link = self.get_kibana_link

    def teardown_method(self, method):

        if self.session:
            self.session.close()

        if not self.test_case_url:
            raise Exception("Test don't have a test case url.")

        self.xrequestid = None

    def get_fail_debug(self):
        if not hasattr(self.session, 'status_code'):
            self.session.status_code = None

        failed_test_command = self.get_failed_test_command()
        """Failed test report generator"""
        return (
            self.session.url,
            self.session.status_code,
            self.test_case_url,
            self.xrequestid,
            failed_test_command
        )

    def get_response(self, url, method="GET", timeout=10, **kwargs):
        self.session.url = url
        self.session.status_code = None
        response = self.session.request(
            method=method,
            url=url,
            timeout=timeout,
            verify=False,
            cookies=dict(xrequestid=self.xrequestid),
            hooks=dict(response=request_logging),
            **kwargs,
        )
        self.session.status_code = response.status_code
        return response
