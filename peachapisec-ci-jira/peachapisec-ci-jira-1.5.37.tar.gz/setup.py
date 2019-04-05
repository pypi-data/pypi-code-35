import os
from setuptools import setup, find_packages

cwd = os.getcwd()
try:
	os.chdir(os.path.dirname(os.path.realpath(__file__)))

	setup(
		name = 'peachapisec-ci-jira',
		description = 'Peach API Security JIRA CI Integration',
		long_description = open('README.rst').read(),
		author = 'Peach Tech',
		author_email = 'contact@peach.tech',
		url = 'https://peach.tech',
		version = '1.5.37',

		include_package_data=True,
		packages=find_packages('src'),
		package_dir={'':'src'},
		
		eager_resources = [
			'peach2jira/settings.json',
			'peach2jira/comment.mustache',
			'peach2jira/description.mustache'
		],

		# update requirements.txt as well!
		install_requires = [
			'click~=6.7', 
			'peachapisec-api==1.5.37', 
			'requests>=2.18.4',
			'pystache',
			'hexdump'],

		entry_points = {
			'console_scripts': ['peach2jira=peach2jira:run'],
		},

		license = 'Apache License, Version 2.0',
		keywords = 'peach fuzzing security test rest jira',

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
			'Programming Language :: Python :: 2',
			'Programming Language :: Python :: 3'
		])

finally:
	os.chdir(cwd)

# end
