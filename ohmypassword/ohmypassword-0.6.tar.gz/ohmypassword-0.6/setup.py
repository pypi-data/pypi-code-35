from setuptools import setup

setup(
	name="ohmypassword",
	version="0.6",
	description="Package to generate strong, hardly bruteforcable passwords",
	scripts=['bin/ohmypassword'],
	install_requires=[
          'pycrypto',
      ],

)		
