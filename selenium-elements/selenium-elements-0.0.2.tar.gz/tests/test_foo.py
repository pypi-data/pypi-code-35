from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from selenium_elements.elements import PageElement
from selenium_elements.page import Page


def test_elements():
    browser = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub",
        desired_capabilities=DesiredCapabilities.CHROME,
    )

    class IndexPage(Page):
        path = "/"

        input = PageElement(By.ID, "input")

    index = IndexPage(browser, base_url="http://web:8000")
    assert len(index.declared_elements) == 1
    assert isinstance(index.input, WebElement)
