from automatic_test_tool._util import Util
from automatic_test_tool._base_page import BasePage
from automatic_test_tool._custom_logger import custom_logger


class PageTestCase:

    def __init__(self, selenium):
        self.page = BasePage(selenium)

    def set_url(self, url):
        return self.page.set_url(url)

    def custom_logger(self, log_level):
        return custom_logger(log_level)

    def sleep(self, sec, info):
        return Util.sleep(sec, info)

    def get_alpha_numeric(self, length, type):
        return Util.get_alpha_numeric(length, type)

    def get_unique_name(self, char_count):
        return Util.get_unique_name(char_count)

    def get_unique_name_list(self, list_size, item_length):
        return Util.get_unique_name_list(list_size, item_length)

    def verify_text_contains(self, actual_text, expected_text):
        return Util.verify_text_contains(actual_text, expected_text)

    def verify_text_match(self, actual_text, expected_text):
        return Util.verify_text_match(actual_text, expected_text)

    def verify_list_match(self, expected_list, actual_list):
        return Util.verify_list_match(expected_list, actual_list)

    def verify_list_contains(self, expected_list, actual_list):
        return Util.verify_list_contains(expected_list, actual_list)

    def screenshot(self, result_message):
        return self.page.screenshot(result_message)

    def get_title(self):
        return self.page.get_title()

    def get_by_type(self, locator_type):
        return self.page.get_by_type(locator_type)

    def get_element(self, locator, locator_type):
        return self.page.get_element(locator, locator_type)

    def get_element_list(self, locator, locator_type):
        return self.page.get_element_list(locator, locator_type)

    def element_click(self, locator, locator_type, element=None):
        return self.page.element_click(locator, locator_type, element)

    def send_keys(self, data, locator, locator_type, element=None):
        return self.page.send_keys(data, locator, locator_type, element)

    def clear_field(self, locator, locator_type):
        return self.page.clear_field(locator, locator_type)

    def get_text(self, locator, locator_type, element, info):
        return self.page.get_text(locator, locator_type, element, info)

    def is_element_present(self, locator, locator_type, element):
        return self.page.is_element_present(locator, locator_type, element)

    def is_element_displayed(self, locator, locator_type, element):
        return self.page.is_element_displayed(locator, locator_type, element)

    def is_element_enabled(self, locator, locator_type, element):
        return self.page.is_element_enabled(locator, locator_type, element)

    def element_presence_check(self, locator, by_type):
        return self.page.element_presence_check(locator, by_type)

    def wait_for_element(self, locator, locator_type, timeout, poll_frequency):
        return self.page.wait_for_element(locator, locator_type, timeout, poll_frequency)

    def wait_for_element_present(self, locator, locator_type, timeout, poll_frequency):
        return self.page.wait_for_element_present(locator, locator_type, timeout, poll_frequency)

    def wait_for_element_not_present(self, locator, locator_type, timeout, poll_frequency):
        return self.page.wait_for_element_not_present(locator, locator_type, timeout, poll_frequency)

    def web_scroll(self, direction):
        return self.page.web_scroll(direction)