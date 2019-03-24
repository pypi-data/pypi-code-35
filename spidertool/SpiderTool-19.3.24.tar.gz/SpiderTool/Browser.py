#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
File:   Browser.py
Author: Lijiacai(1050518702@qq.com)
Description:
    模拟浏览器的driver(Firefox,Chrome,PhantoJS),user can add other function
"""
import re
import os
import random
import sys
import time
import traceback
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/" % cur_dir)


class Browser(object):
    """browser"""

    def __init__(self, proxies=None, headless=True, timeout=20, executable_path=None,
                 browser_type=None):
        """
        init
        :param proxies: ip代理
        :param headless: 是否使用无界面,boolean类型
        :param timeout: 超时
        :param executable_path: 浏览器驱动器
        :param browser_type: 浏览器类型
        """
        self.proxies = proxies
        self.headless = headless
        self.timeout = timeout
        self.executable_path = executable_path
        if browser_type == "Firefox":
            if not self.executable_path:
                self.executable_path = "geckodriver"
            self.browser = self.FirefoxDriver()
        elif browser_type == "Chrome":
            if not self.executable_path:
                self.executable_path = "chromedriver"
            self.browser = self.ChromeDriver()
        elif browser_type == "PhantomJS":
            if not self.executable_path:
                raise ("*****please add PhantomJS executable_path*****")
            self.browser = self.PhantomJSDriver()
	elif re.findall("Remote-", browser_type):
            _type = browser_type.split("-")[1].upper()
            if not self.executable_path:
                raise ("****please add Remote executable_path****")
            self.browser = self.Remote(_type)
        else:
            raise ("*****please use Firefox or Chrome or PhantomJS for your browser*****")

    def proxy(self):
        """
        get proxy
        如果有其他代理，更改此处函数
        :return: 返回一个ip：12.23.88.23:2345
        """
        if not self.proxies:
            one_proxy = None
        elif type(self.proxies) == list:
            one_proxy = random.choice(self.proxies)
        else:
            one_proxy = None
        if one_proxy == None:
            logging.info("self ip")
        return one_proxy

    def FirefoxDriver(self):
        """
        create a firefox browser
        """
        if self.headless == True:
            options = webdriver.FirefoxOptions()
            options.set_headless()
            options.add_argument('headless')
            options.add_argument('--disable-gpu')
            if self.proxies:
                proxy = Proxy(
                    {
                        'proxyType': ProxyType.MANUAL,
                        'httpProxy': self.proxy()  # 代理ip和端口
                    }
                )
                browser_driver = webdriver.Firefox(firefox_options=options, proxy=proxy)
            else:
                browser_driver = webdriver.Firefox(firefox_options=options)
        else:
            if self.proxies:
                proxy = Proxy(
                    {
                        'proxyType': ProxyType.MANUAL,
                        'httpProxy': self.proxy()  # 代理ip和端口
                    }
                )
                browser_driver = webdriver.Firefox(proxy=proxy)
            else:
                browser_driver = webdriver.Firefox()
        browser_driver.set_page_load_timeout(self.timeout)
        browser_driver.set_script_timeout(self.timeout)
        return browser_driver

    def ChromeDriver(self):
        """
        create a chrome browser
        """
        options = webdriver.ChromeOptions()
        if self.headless == True:
            options.set_headless()
            options.add_argument('headless')
            options.add_argument('--disable-gpu')
        if self.proxies:
            options.add_argument("--proxy-server=http://%s" % self.proxy())
        browser_driver = webdriver.Chrome(chrome_options=options)
        browser_driver.set_page_load_timeout(self.timeout)
        browser_driver.set_script_timeout(self.timeout)
        return browser_driver

    def PhantomJSDriver(self):
        """
        create a phantomjs browser
        """
        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        desired_capabilities["phantomjs.page.settings.userAgent"] = Browser.userAgent()
        desired_capabilities["phantomjs.page.settings.loadImages"] = False
        if self.proxies:
            proxy = webdriver.Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxy.http_proxy = self.proxy()
            proxy.add_to_capabilities(desired_capabilities)
        browser_driver = webdriver.PhantomJS(executable_path=self.executable_path,
                                             desired_capabilities=desired_capabilities,
                                             service_args=['--ignore-ssl-errors=true',
                                                           "--cookies-file=cookie.txt"])
        return browser_driver

    def Remote(self, _type):
        """
        create a remote browser
        """
        desired_capabilities = eval("DesiredCapabilities.%s" % _type)
        desired_capabilities["phantomjs.page.settings.loadImages"] = False
        if self.proxies:
            proxy = webdriver.Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxy.http_proxy = self.proxy()
            proxy.add_to_capabilities(desired_capabilities)
        browser_driver = webdriver.Remote(command_executor=self.executable_path,
                                          desired_capabilities=desired_capabilities)
        browser_driver.set_page_load_timeout(self.timeout)
        browser_driver.set_script_timeout(self.timeout)
        return browser_driver

    def get(self, url):
        """
        driver get request
        """
        self.browser.get(url)

    def click_elem(self, elem):
        """
        :param elem: 元素
        :return:
        """
        ActionChains(self.browser).move_to_element(elem).click().perform()

    def wait_for_element_loaded(self, type_name=None, elem_type=By.CLASS_NAME, wait_time=10):
        """
        等待元素加载
        :param type_name: 元素类型名称
        :param elem_type: 元素类型，By.CLASS_NAME
        :param wait_time: 加载最大时长
        :return:
        """
        WebDriverWait(self.browser, wait_time).until(
            EC.presence_of_element_located((elem_type, type_name))
        )

    def implicitly_wait(self, wait_time=10):
        """
        显示等待
        :param wait_time: 等待时间
        :return:
        """
        self.browser.implicitly_wait(wait_time)

    def sleep_wait(self, wait_time=10):
        """
        睡眠等待
        :param wait_time: 等待时间
        :return:
        """
        time.sleep(wait_time)

    def send_keys(self, elem, value):
        """
        发送text
        :param elem: 元素
        :param value: 文本内容
        :return:
        """
        elem.send_keys(value)

    def find_element(self, value, by):
        """
        查找页面元素
        :param value: 查找的值
        :param by: 查找方式,By.CLASS_NAME
        :return: element
        """
        return self.browser.find_element(by=by, value=value)

    def find_elements(self, value, by):
        """
        查找页面元素s
        :param value: 查找的值
        :param by: 查找方式,By.CLASS_NAME
        :return: element
        """
        return self.browser.find_elements(by=by, value=value)

    def page_source(self):
        """
        页面数据
        """
        return self.browser.page_source

    def keys(self, elem, keyboard=Keys.ENTER):
        """
        键盘操作
        :param elem: 操作元素
        :param keyboard: 键盘按键
        :return:
        """
        elem.send_keys(keyboard)

    def clear(self, elem):
        """
        清楚文本框内容
        :param elem: 元素
        :return:
        """
        elem.clear()

    def close(self):
        """
        手动关闭浏览器
        """
        try:
            self.browser.close()
            try:
                self.browser.quit()
            except:
                pass
            try:
                self.browser.service.stop()
            except:
                pass
            print("browser close successful")
            logging.info("***********关闭成功(close)**********")
        except Exception as e:
            self.__del__()
            logging.exception("***********关闭异常(close)**********")
            pass

    @staticmethod
    def userAgent():
        """
        可以更改此函数
        :return: get random header
        """
        ua_list = [
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/4.0 (compatible; MSIE 8.0;Windows NT 6.0; Trident/4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        ]
        return random.choice(ua_list)

    def __del__(self):
        """
        当消除browser时,会先关闭浏览器
        """
        try:
            self.browser.close()
        except:
            pass
        try:
            self.browser.quit()
        except:
            pass
        try:
            self.browser.service.stop()
        except:
            pass


def test_firefox():
    """unittest"""
    B = Browser(headless=False, browser_type="Firefox")
    B.get(url="https://www.baidu.com")
    elem = B.find_element("kw", By.ID)
    B.clear(elem)
    B.send_keys(elem, "zhoujielun")
    B.keys(elem, Keys.ENTER)
    B.implicitly_wait(10)
    B.sleep_wait(2)
    print(B.page_source())


def test_chrome():
    """unittest"""
    B = Browser(headless=False, browser_type="Chrome")
    B.get(url="https://www.baidu.com")
    elem = B.find_element("kw", By.ID)
    B.clear(elem)
    B.send_keys(elem, "zhoujielun")
    B.keys(elem, Keys.ENTER)
    B.implicitly_wait(10)
    B.sleep_wait(2)
    print(B.page_source())

def test_remote():
    """unittest"""
    driver=Browser(browser_type="Remote-Chrome", headless=False, timeout=100,executable_path="http://127.0.0.1:4444/wd/hub")
    driver.get("https://www.nike.com/cn/launch/t/air-max-95-premium-throwback-future/")
    print(driver.browser.title.encode("utf8"))
    driver.close()

if __name__ == '__main__':
    # test_firefox()
    test_chrome()
