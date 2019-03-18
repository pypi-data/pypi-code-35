from setuptools import setup

setup(
	name='dctdevtools',
	version='0.3',
	description='DCT Development Tools',
	url='',
	author='Max Dinh',
	author_email='max.dinh@dctsolutions.io',
	license='MIT',
	packages=['dctdevtools'],
	scripts=['bin/dctdevtools'],
	
	zip_safe=False,
	entry_points={
		'console_scripts':[
		'dctdevtools=dctdevtools.__main__:run'
		]
	}
	)