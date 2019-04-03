from selenium import webdriver


def create(options):
	"""
	Returns a webdriver based on the passed options
	"""
	assert 'driver' in options
	assert options['driver'] in ('chrome', 'firefox', 'ie', 'edge')
	if options['driver'] == 'chrome':
		o = webdriver.ChromeOptions()
	elif options['driver'] == 'firefox':
		o = webdriver.FirefoxOptions()
	elif options['driver'] == 'ie':
		o = webdriver.IeOptions()
	elif options['driver'] == 'edge':
		o = webdriver.ChromeOptions()

	o.headless = options['headless']

	if options['driver'] == 'chrome':
		driver = webdriver.Chrome(options=o, service_log_path='/dev/null')
	elif options['driver'] == 'firefox':
		driver = webdriver.Firefox(options=o, service_log_path='/dev/null')
	elif options['driver'] == 'ie':
		driver = webdriver.Ie(options=o)
	elif options['driver'] == 'edge':
		driver = webdriver.Edge()

	resolution = tuple(str(options['resolution']).split('x')) if 'resolution' in options and options[
		'resolution'] is not None else (1920, 1080)
	driver.set_window_size(resolution[0], resolution[1])

	return driver
