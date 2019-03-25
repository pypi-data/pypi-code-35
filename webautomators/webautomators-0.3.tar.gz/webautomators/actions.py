from webautomators.extended_driver import WebExtendedDriver
import requests
import time
from webautomators.extended_find import FindElemennt
class Actions(WebExtendedDriver,FindElemennt):
    
    def assert_alert_not_present(self):
        assert not self.alert_is_present(), 'an alert was present'

    def assert_alert_present(self):
        """Assert an alert is present"""
        assert self.alert_is_present(), 'an alert was not present'

    def assert_alert_text(self,text):
        """Assert alert text
        This will fail if there is no alert present.

        Parameters:
        text : value
        """
        alert_text = self.switch_to.alert.text
        error_msg = "expected alert text to be '{}' but was '{}'".format(text, alert_text)
        assert alert_text == text, error_msg

    def assert_alert_text_is_not(self,text):
        """Assert alert text is not `text`
        This will fail if there is no alert present.

        Parameters:
        text : value
        """
        alert_text = self.switch_to.alert.text
        error_msg = "expected alert text not to be '{}'".format(text)
        assert alert_text != text, error_msg


    def assert_amount_of_windows(self,amount):
        """Assert the amount of open windows/tabs

        Parameters:
        amount : value
        """
        actual_amount = len(self.get_window_handles())
        error_msg = 'expected {} windows but got {}'.format(amount, actual_amount)
        assert actual_amount == amount, error_msg


    def assert_cookie_present(self,name):
        """Assert a cookie exists in the current session.
        The cookie is found by its name.

        Parameters:
        name: value
        """
        cookie = self.get_cookie(name)
        assert cookie, "cookie '{}' was not found".format(name)


    def assert_cookie_value(self,name, value):
        """Assert the value of a cookie.
        This will fail if the cookie does not exist.

        Parameters:
        name: value
        value: value
        """
        cookie = self.get_cookie(name)
        if not cookie:
            raise Exception('Cookie "{}" was not found'.format(name))
        elif not 'value' in cookie:
            raise Exception('Cookie "{}" did not have "value" key'.format(name))
        else:
            msg = ("expected cookie '{}' value to be '{}' but was '{}'".format(name, value, cookie['value']))
            assert cookie['value'] == value, msg


    def assert_element_attribute(self,element, attribute, value):
        """Assert value of element attribute

        Parameters:
        element : element
        attribute : value
        value : value
        """
        element = self.find(element, timeout=0)
        attr_value = element.get_attribute(attribute)
        msg = ("expected element {} attribute {} value to be '{}' was '{}'"
                .format(element.name, attribute, value, attr_value))
        assert attr_value == value, msg


    def assert_element_attribute_is_not(self,element, attribute, value):
        """Assert the value of element attribute is not `value`

        Parameters:
        element : element
        attribute : value
        value : value
        """
        element = self.find(element, timeout=0)
        attr_value = element.get_attribute(attribute)
        msg = ('expected element {} attribute {} value to not be {}'
                .format(element.name, attribute, value))
        assert attr_value != value, msg


    def assert_element_checked(self,element):
        """Assert element is checked.
        This applies to checkboxes and radio buttons.

        Parameters:
        element : element
        """
        element = self.find(element, timeout=0)        
        assert element.is_selected(), 'element {} is not checked'.format(element.name)        


    def assert_element_displayed(self,element):
        """Assert element is displayed (visible to the user)

        Parameters:
        element : element
        """
        element = self.find(element, timeout=0, wait_displayed=False)
        assert element.is_displayed(), 'element {} is not displayed'.format(element.name)

    def assert_element_enabled(self,element):
        """Assert element is enabled.

        Parameters:
        element : element
        """
        element = self.find(element, timeout=0)
        assert element.is_enabled(), 'element {} is not enabled'.format(element.name)


    def assert_element_has_attribute(self,element, attribute):
        """Assert element has attribute

        Parameters:
        element : element
        attribute : value
        """
        element = self.find(element, timeout=0)
        error_msg = 'element {} does not have attribute {}'.format(element.name, attribute)
        assert element.has_attribute(attribute), error_msg


    def assert_element_has_focus(self,element):
        """Assert element has focus

        Parameters:
        element : element
        """
        element = self.find(element, timeout=0)
        error_msg = 'element {} does not have focus'.format(element.name)
        assert element.has_focus(), error_msg


    def assert_element_has_not_attribute(self,element, attribute):
        """Assert element has not attribute

        Parameters:
        element : element
        attribute : value
        """
        element = self.find(element, timeout=0)
        error_msg = 'element {} has attribute {}'.format(element.name, attribute)
        assert not element.has_attribute(attribute), error_msg


    def assert_element_has_not_focus(self,element):
        """Assert element does not have focus

        Parameters:
        element : element
        """
        element = self.find(element, timeout=0)
        error_msg = 'element {} has focus'.format(element.name)
        assert not element.has_focus(), error_msg


    def assert_element_not_checked(self,element):
        """Assert element is not checked.
        This applies to checkboxes and radio buttons.

        Parameters:
        element : element
        """
        element = self.find(element, timeout=0)
        assert not element.is_selected(), 'element {} is checked'.format(element.name)


    def assert_element_not_displayed(self,element):
        """Assert element is not displayed (visible to the user)

        Parameters:
        element : element
        """
        element = self.find(element, timeout=0, wait_displayed=False)
        assert not element.is_displayed(), 'element {} is displayed'.format(element.name)
        

    def assert_element_not_enabled(self,element):
        """Assert element is not enabled.

        Parameters:
        element : element
        """
        element = self.find(element, timeout=0)
        assert not element.is_enabled(), 'element {} is enabled'.format(element.name)
        


    def assert_element_not_present(self,element):
        """Assert element is not present in the DOM

        Parameters:
        element : element
        """
        msg = 'element {} is present'.format(element)
        assert not self.element_is_present(element), msg


    def assert_element_present(self,element):
        """Assert element is present in the DOM

        Parameters:
        element : element
        """
        msg = 'element {} is not present'.format(element)
        assert self.element_is_present(element), msg


    def assert_element_text(self,element, text):
        """Assert the text of the element

        Parameters:
        element : element
        text : value
        """
        element = self.find(element, timeout=0)
        msg = ("expected element {} text to be '{}' but was '{}'"
                .format(element.name, text, element.text))
        assert element.text == text, msg


    def assert_element_text_contains(self,element, text):
        """Assert element contains text

        Parameters:
        element : element
        text : value
        """
        element = self.find(element, timeout=0)
        msg = ("expected element {} text '{}' to contain '{}'"
                .format(element.name, element.text, text))
        assert text in element.text, msg


    def assert_element_text_is_not(self,element, text):
        """Assert the text of the element is not `text`

        Parameters:
        element : element
        text : value
        """
        element = self.find(element, timeout=0)
        msg = "expected element {} text to not be '{}'".format(element.name, text)
        assert element.text != text, msg


    def assert_element_text_not_contains(self,element, text):
        """Assert the text of the element does not contain `text`

        Parameters:
        element : element
        text : value
        """
        element = self.find(element, timeout=0)
        msg = "element {} text '{}' contains text '{}'".format(element.name, element.text, text)
        assert text not in element.text, msg

    def assert_page_contains_text(self,text):
        """Assert the given text is present anywhere in the page source

        Parameters:
        text : value
        """
        assert text in self.page_source, "text '{}' not found in the page".format(text)
        

    def assert_page_not_contains_text(self,text):
        """Assert the given text is not present anywhere in the page source

        Parameters:
        text : value
        """
        assert text not in self.page_source, "text '{}' was found in the page".format(text)
        


    def assert_response_status_code(self,response, status_code):
        """Assert the response status code.

        Parameters:
        response : value
        status_code : value
        """
        if isinstance(status_code, str):
            if status_code.isdigit():
                status_code = int(status_code)
        msg = ('expected response status code to be {} but was {}'
                .format(status_code, response.status_code))
        assert response.status_code == status_code, msg


    def assert_selected_option_by_text(self,element, text):
        """Assert an element has a selected option by the option text

        Parameters:
        element : element
        text : value
        """
        element = self.find(element)
        selected_option_text = element.select.first_selected_option.text
        error_msg = ("expected selected option in element {} to be '{}' but was '{}'"
                        .format(element.name, text, selected_option_text))
        assert selected_option_text == text, error_msg


    def assert_selected_option_by_value(self,element, value):
        """Assert an element has a selected option by the option value

        Parameters:
        element : element
        value : value
        """
        element = self.find(element)
        selected_option_value = element.select.first_selected_option.value
        error_msg = ('expected selected option in element {} to be {} but was {}'
                        .format(element.name, value, selected_option_value))
        assert selected_option_value == value, error_msg
        


    def assert_title(self,title):
        """Assert the page title

        Parameters:
        title : value
        """
        error_msg = ("expected title to be '{}' but was '{}'"
                        .format(title, self.title))
        assert self.title == title, error_msg


    def assert_title_contains(self,partial_title):
        """Assert the page title contains partial_title

        Parameters:
        partial_title : value
        """
        error_msg = "expected title to contain '{}'".format(partial_title)
        assert partial_title in self.title, error_msg
        


    def assert_title_is_not(self,title):
        """Assert the page title is not the given value

        Parameters:
        title : value
        """
        error_msg = "expected title to not be '{}'".format(title)
        assert self.title != title, error_msg


    def assert_title_not_contains(self,text):
        """Assert the page title does not contain text

        Parameters:
        text : value
        """
        error_msg = "title contains '{}'".format(text)
        assert text not in self.title, error_msg
        


    def assert_true(self,condition):
        """DEPRECATED
        Assert condition is true
        Parameters:
        condition : value
        """
        assert condition, 'expected {} to be true'.format(condition)


    def assert_url(self,url):
        """Assert the current URL

        Parameters:
        url : value
        """
        error_msg = ("expected URL to be '{}' but was '{}'"
                        .format(url, self.current_url))
        assert self.current_url == url, error_msg
        


    def assert_url_contains(self,partial_url):
        """Assert the current URL contains partial_url

        Parameters:
        partial_url : value
        """
        error_msg = "expected URL to contain '{}'".format(partial_url)
        assert partial_url in self.current_url, error_msg
        


    def assert_url_is_not(self,url):
        """Assert the current URL is not `url`

        Parameters:
        url : value
        """
        error_msg = "expected URL to not be '{}'".format(url)
        assert self.current_url != url, error_msg
        


    def assert_url_not_contains(self,partial_url):
        """Assert the current URL does not contain partial_url

        Parameters:
        partial_url : value
        """
        actual_url = self.current_url
        error_msg = ("expected URL '{}' to not contain '{}'"
                        .format(actual_url, partial_url))
        assert partial_url not in actual_url, error_msg
        


    def assert_window_present_by_partial_title(self,partial_title):
        """Assert there is a window/tab present by partial title

        Parameters:
        partial_title : value
        """
        error_msg = "There is no window present with partial title '{}'".format(partial_title)
        window_titles = self.get_window_titles()
        assert any(partial_title in t for t in window_titles), error_msg


    def assert_window_present_by_partial_url(self,partial_url):
        """Assert there is a window/tab present by partial URL

        Parameters:
        partial_url : value
        """
        urls = self.get_window_urls()
        error_msg = "There is no window present with partial URL '{}'".format(partial_url)
        assert any(partial_url in url for url in urls), error_msg


    def assert_window_present_by_title(self,title):
        """Assert there is a window/tab present by title

        Parameters:
        title : value
        """
        error_msg = "There is no window present with title '{}'".format(title)
        assert title in self.get_window_titles(), error_msg


    def assert_window_present_by_url(self,url):
        """Assert there is a window/tab present by URL

        Parameters:
        url : value
        """
        error_msg = "There is no window present with URL '{}'".format(url)
        assert url in self.get_window_urls(), error_msg
        


    def http_get(self,url, headers={}, params={}, verify_ssl_cert=True):
        """Perform an HTTP GET request to the given URL.
        Headers and params are optional dictionaries.
        Store response in data.last_response
        Returns the response

        Parameters:
        url : value
        headers (optional, dict) : value
        params (optional, dict) : value
        verify_ssl_cert (optional, True) : value
        """
        response = requests.get(url, headers=headers, params=params,
                                verify=verify_ssl_cert)
        return response


    def http_post(self,url, headers={}, data={}, verify_ssl_cert=True):
        """Perform an HTTP POST request to the given URL.
        Headers and data are optional dictionaries.
        Stores the response in data.last_response
        Returns the response

        Parameters:
        url : value
        headers (optional, dict) : value
        data (optional, dict) : value
        verify_ssl_cert (optional, default is True) : value
        """
        response = requests.post(url, headers=headers, data=data,
                                verify=verify_ssl_cert)
        return response


    def select_option_by_index(self,element, index):
        """Select an option from a select dropdown by index.

        Parameters:
        element : element
        index : value
        """
        element = self.find(element)
        element.select.select_by_index(index)

    def select_option_by_text(self,element, text):
        """Select an option from a select dropdown by text.

        Parameters:
        element : element
        text : value
        """
        element = self.find(element)
        element.select.select_by_visible_text(text)


    def select_option_by_value(self,element, value):
        """Select an option from a select dropdown by value.

        Parameters:
        element : element
        value : value
        """
        element = self.find(element)
        element.select.select_by_value(value)

    def wait(self,seconds):
        """Wait for a fixed amount of seconds.

        Parameters:
        seconds (int or float) : value
        """
        try:
                to_float = float(seconds)
        except:
                raise ValueError('seconds value should be a number')
        time.sleep(to_float)