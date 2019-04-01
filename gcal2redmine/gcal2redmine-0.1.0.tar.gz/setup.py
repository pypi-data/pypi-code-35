# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['gcal2redmine']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'google-api-python-client>=1.7,<2.0',
 'oauth2client>=4.1,<5.0',
 'python-redmine>=2.1,<3.0',
 'tzlocal>=1.5,<2.0']

entry_points = \
{'console_scripts': ['gcal2redmine = gcal2redmine.cli:main']}

setup_kwargs = {
    'name': 'gcal2redmine',
    'version': '0.1.0',
    'description': "Fill Redmine's time tracker from a Google Calendar",
    'long_description': None,
    'author': 'Nicolas KAROLAK',
    'author_email': 'nicolas@karolak.fr',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
