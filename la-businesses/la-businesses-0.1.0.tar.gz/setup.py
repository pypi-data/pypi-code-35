# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['la_businesses']

package_data = \
{'': ['*'],
 'la_businesses': ['.git/objects/08/*',
                   '.git/objects/4b/*',
                   '.git/objects/58/*',
                   '.git/objects/b5/*',
                   '.git/objects/d8/*']}

install_requires = \
['pandas>=0.24.2,<0.25.0',
 'pytz>=2018.9,<2019.0',
 'requests>=2.21,<3.0',
 'simplekml>=1.3,<2.0']

entry_points = \
{'console_scripts': ['la-businesses = la_businesses:main']}

setup_kwargs = {
    'name': 'la-businesses',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Manuel Ochoa',
    'author_email': 'dev@manuelochoa.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
