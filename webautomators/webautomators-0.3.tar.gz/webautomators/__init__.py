from selenium.webdriver import Chrome as SeleniumChromeDriver
from selenium.webdriver import Edge as SeleniumEdgeDriver
from selenium.webdriver import Firefox as SeleniumGeckoDriver
from selenium.webdriver import Ie as SeleniumIeDriver
from selenium.webdriver import Opera as SeleniumOperaDriver
from selenium.webdriver import Remote as SeleniumRemoteDriver

from webautomators.actions import Actions


class WebChromeDriver(SeleniumChromeDriver,Actions):
    pass


class WebEdgeDriver(SeleniumEdgeDriver, Actions):
    pass


class WebGeckoDriver(SeleniumGeckoDriver, Actions):
    pass


class WebIeDriver(SeleniumIeDriver, Actions):
    pass


class WebOperaDriver(SeleniumOperaDriver, Actions):
    pass


class WebRemoteDriver(SeleniumRemoteDriver, Actions):
    pass