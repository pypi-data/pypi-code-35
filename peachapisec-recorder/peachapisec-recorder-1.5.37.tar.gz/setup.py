import os
from setuptools import setup, find_packages

cwd = os.getcwd()
try:
	os.chdir(os.path.dirname(os.path.realpath(__file__)))

	setup(
		name = 'peachapisec-recorder',
		description = 'Peach API Security recording tool',
		long_description = open('README.txt').read(),
		author = 'Peach Tech',
		author_email = 'contact@peach.tech',
		url = 'https://peach.tech',
		version = '1.5.37',

		python_requires='~=3.6',

		include_package_data=True,
		packages=find_packages('src'),
		package_dir={'':'src'},
		
		eager_resources = [
			'peachrecorder/har_dump.py',
		],

		# update requirements.txt as well!
		install_requires = [
			'click~=6.7', 
			'mitmproxy~=4.0.4',
			],
		entry_points = {
			'console_scripts': ['peachrecorder=peachrecorder.main:run'],
		},

		license = 'Apache License, Version 2.0',
		keywords = 'peach fuzzing security test rest',

		classifiers = [
			'Development Status :: 5 - Production/Stable',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: Apache Software License',
			'Operating System :: OS Independent',
			'Topic :: Security',
			'Topic :: Software Development :: Quality Assurance',
			'Topic :: Software Development :: Testing',
			'Topic :: Utilities',
			'Programming Language :: Python',
			'Programming Language :: Python :: 3'
		])

finally:
	os.chdir(cwd)

# end
