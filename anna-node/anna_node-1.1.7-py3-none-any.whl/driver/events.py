import time

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from . import util


def send_keys(driver, event):
	if wait(driver, event):
		if 'target' in event and not isinstance(event['target'], dict):
			event['target'] = {'type': 'css', 'value': event['target']}
		element = util.get_element(driver=driver, target=event['target']['value'], type=event['target']['type'])
		v = event['value'].encode('ascii', 'ignore').decode("utf-8")
		element.send_keys(v)


def submit(driver, event):
	if wait(driver, event):
		if 'target' in event and not isinstance(event['target'], dict):
			event['target'] = {'type': 'css', 'value': event['target']}
		element = util.get_element(driver=driver, target=event['target']['value'], type=event['target']['type'])
		element.submit()


def click(driver, event):
	if wait(driver, event):
		if 'target' in event and not isinstance(event['target'], dict):
			event['target'] = {'type': 'css', 'value': event['target']}
		element = util.get_element(driver=driver, target=event['target']['value'], type=event['target']['type'])
		if element not in (None, False) and element.tag_name == 'option':
			element.click()
		else:
			action = ActionChains(driver)
			action.move_to_element(element)
			action.click(element)
			action.perform()


def hover(driver, event):
	if wait(driver, event):
		if 'target' in event and not isinstance(event['target'], dict):
			event['target'] = {'type': 'css', 'value': event['target']}
		element = util.get_element(driver=driver, target=event['target']['value'], type=event['target']['type'])
		action = ActionChains(driver)
		action.move_to_element(element)
		action.perform()


def get(driver, event):
	if 'target' in event and not isinstance(event['target'], dict):
		event['target'] = {'type': 'css', 'value': event['target']}
	driver.get(event['target'])


def wait(driver, event):
	"""
	Wait for an element to appear
	:param driver:
	:param event:
	:return:
	"""
	if 'target' in event and not isinstance(event['target'], dict):
		event['target'] = {'type': 'css', 'value': event['target']}
	try:
		if event['type'] == 'click':
			if event['target']['type'] == 'css':
				WebDriverWait(driver, 16).until(ec.element_to_be_clickable((By.CSS_SELECTOR, event['target']['value'])))
			elif event['target']['type'] == 'xpath':
				WebDriverWait(driver, 16).until(ec.element_to_be_clickable((By.XPATH, event['target']['value'])))
		else:
			if event['target']['type'] == 'css':
				WebDriverWait(driver, 16).until(
					ec.presence_of_element_located((By.CSS_SELECTOR, event['target']['value'])))
			elif event['target']['type'] == 'xpath':
				WebDriverWait(driver, 16).until(ec.presence_of_element_located((By.XPATH, event['target']['value'])))
	except TimeoutException as e:
		if 'required' in event and not event['required']:
			return False
		else:
			raise e
	return True


def sleep(driver, event):
	time.sleep(event['value'])


def switch_to(driver, event):
	if 'target' in event and not isinstance(event['target'], dict):
		event['target'] = {'type': 'css', 'value': event['target']}
	scroll_to(driver, event)
	element = util.get_element(driver=driver, target=event['target']['value'], type=event['target']['type'])
	driver.switch_to.frame(element)


def scroll_to(driver, event):
	if 'target' in event and not isinstance(event['target'], dict):
		event['target'] = {'type': 'css', 'value': event['target']}
	driver.execute_script('arguments[0].scrollIntoView(true);', util.get_element(driver=driver, target=event['target']['value'], type=event['target']['type']))
