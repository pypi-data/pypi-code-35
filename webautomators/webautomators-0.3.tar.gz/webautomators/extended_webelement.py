# from typing import List # not supported in 3.4

from selenium.webdriver.remote.webelement import WebElement as RemoteWebElement
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select as SeleniumSelect
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webautomators import expected_conditions as wec


class ExtendedWebElement:

    selector_type = None
    selector_value = None
    name = None

    def check(self):
        """Check element if element is checkbox or radiobutton.
        If element is already checked, this is ignored.
        """
        checkbox_or_radio = (self.tag_name == 'input' and
                             self.get_attribute('type') in ['checkbox', 'radio'])
        if checkbox_or_radio:
            if not self.is_selected():
                self.click()
        else:
            msg = 'Element {} is not checkbox or radiobutton'.format(self.name)
            raise ValueError(msg)

    def double_click(self):
        """Double click the element"""
        action_chains = ActionChains(self.parent)
        action_chains.double_click(self).perform()

    def drag_and_drop(self, element, target):
        actionChains = ActionChains(self.parent)
        source_element = self.find(element)
        target_element = self.find(target)
        actionChains.drag_and_drop(source_element, target_element).perform() 


    def focus(self):
        """Give focus to element"""
        self.parent.execute_script('arguments[0].focus();', self)

    def has_attribute(self, attribute):
        """Returns whether element has attribute"""
        return self.get_attribute(attribute) is not None

    def has_focus(self):
        """Returns whether element has focus"""
        script = 'return arguments[0] == document.activeElement'
        return self.parent.execute_script(script, self)

    def javascript_click(self):
        """Click element using Javascript"""
        self.parent.execute_script('arguments[0].click();', self)


    def mouse_click(self):
        """Mouse over element"""
        action_chains = ActionChains(self.parent)
        action_chains.click(self).perform()
    
    def mouse_click_context(self):
        """Mouse over element"""
        action_chains = ActionChains(self.parent)
        action_chains.context_click(self).perform()

    def mouse_over(self):
        """Mouse over element"""
        action_chains = ActionChains(self.parent)
        action_chains.move_to_element(self).perform()

    def press_key(self, key):
        """Press a key on element

        :Usage:
          element.press_key('ENTER')
          element.press_key('TAB')
          element.press_key('LEFT')
        """
        if hasattr(Keys, key):
            key_attr = getattr(Keys, key)
            self.send_keys(key_attr)
        else:
            defined_keys = [name for name in dir(Keys) if
                            not name.startswith('_')]
            error_msg = ('Key {} is invalid\n'
                         'valid keys are:\n'
                         '{}'.format(key, ','.join(defined_keys)))
            raise ValueError(error_msg)

    @property
    def select(self):
        """Return a Select object"""
        return Select(self)

    def uncheck(self):
        """Uncheck element if element is checkbox.
        If element is already unchecked, this is ignored.
        """
        is_checkbox = (self.tag_name == 'input' and
                       self.get_attribute('type') == 'checkbox')
        if is_checkbox:
            if self.is_selected():
                self.click()
        else:
            raise ValueError('Element {} is not checkbox'.format(self.name))

    @property
    def value(self):
        """The value attribute of element"""
        return self.get_attribute('value')

    def wait_displayed(self, timeout=30):
        """Wait for element to be displayed

        :Returns:
          The element
        """
        wait = WebDriverWait(self.parent, timeout)
        message = ('Timeout waiting for element {} to be displayed'
                   .format(self.name))
        wait.until(ec.visibility_of(self), message=message)
        return self

    def wait_enabled(self, timeout=30):
        """Wait for element to be enabled

        :Returns:
          The element
        """
        wait = WebDriverWait(self.parent, timeout)
        message = 'Timeout waiting for element {} to be enabled'.format(self.name)
        wait.until(wec.element_to_be_enabled(self), message=message)
        return self

    def wait_has_attribute(self, attribute, timeout=30):
        """Wait for element to have attribute

        :Returns:
          The element
        """
        wait = WebDriverWait(self.parent, timeout)
        message = ('Timeout waiting for element {} to have attribute {}'
                   .format(self.name, attribute))
        wait.until(wec.element_to_have_attribute(self, attribute), message=message)
        return self

    def wait_has_not_attribute(self, attribute, timeout=30):
        """Wait for element to not have attribute

        :Returns:
          The element
        """
        wait = WebDriverWait(self.parent, timeout)
        message = ('Timeout waiting for element {} to not have attribute {}'
                   .format(self.name, attribute))
        wait.until_not(wec.element_to_have_attribute(self, attribute),
                       message=message)
        return self

    def wait_not_displayed(self, timeout=30):
        """Wait for element to be not displayed

        :Returns:
          The element
        """
        wait = WebDriverWait(self.parent, timeout)
        message = ('Timeout waiting for element {} to be not displayed'
                   .format(self.name))
        wait.until_not(ec.visibility_of(self), message=message)
        return self

    def wait_not_enabled(self, timeout=30):
        """Wait for element to be not enabled

        :Returns:
          The element
        """
        wait = WebDriverWait(self.parent, timeout)
        message = 'Timeout waiting for element {} to be not enabled'.format(self.name)
        wait.until_not(wec.element_to_be_enabled(self), message=message)
        return self

    def wait_text(self, text, timeout=30):
        """Wait for element text to match given text

        :Returns:
          The element
        """
        wait = WebDriverWait(self.parent, timeout)
        message = ('Timeout waiting for element {} text to be \'{}\''
                   .format(self.name, text))
        wait.until(wec.element_text_to_be(self, text), message=message)
        return self

    def wait_text_contains(self, text, timeout=30):
        """Wait for element to contain given text

        :Returns:
          The element
        """
        wait = WebDriverWait(self.parent, timeout)
        message = ('Timeout waiting for element {} text to contain \'{}\''
                   .format(self.name, text))
        wait.until(wec.element_text_to_contain(self, text), message=message)
        return self

    def wait_text_is_not(self, text, timeout=30):
        """Wait fo element text to not match given text

        :Returns:
          The element
        """
        wait = WebDriverWait(self.parent, timeout)
        message = ('Timeout waiting for element {} text not to be \'{}\''
                   .format(self.name, text))
        wait.until_not(wec.element_text_to_be(self, text), message=message)
        return self

    def wait_text_not_contains(self, text, timeout=30):
        """Wait for element text to not contain text

        :Returns:
          The element
        """
        wait = WebDriverWait(self.parent, timeout)
        message = ('Timeout waiting for element {} text to not contain \'{}\''
                   .format(self.name, text))
        wait.until_not(wec.element_text_to_contain(self, text),
                       message=message)
        return self


class Select(SeleniumSelect):

    @property
    def first_selected_option(self):
        """Return the first selected option as a
        ExtendedWebElement"""
        option = super(Select, self).first_selected_option
        return extend_webelement(option)


class ExtendedRemoteWebElement(RemoteWebElement, ExtendedWebElement):
    pass


class ExtendedFirefoxWebElement(FirefoxWebElement, ExtendedWebElement):
    pass


def extend_webelement(web_element) -> ExtendedRemoteWebElement:
    """Extend the selenium WebElement using the
    ExtendedRemoteWebElement or ExtendedFirefoxWebElement class
    """
    if isinstance(web_element.parent, FirefoxDriver):
        web_element.__class__ = ExtendedFirefoxWebElement
    else:
        web_element.__class__ = ExtendedRemoteWebElement
    return web_element

