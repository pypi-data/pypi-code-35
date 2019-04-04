# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mustaching']

package_data = \
{'': ['*']}

install_requires = \
['colorlover>=0.3.0,<0.4.0',
 'pandas>=0.24.2,<0.25.0',
 'python-highcharts>=0.4.2,<0.5.0']

setup_kwargs = {
    'name': 'mustaching',
    'version': '3.1.1',
    'description': 'A Python 3.6+ library inspired by Mr. Money Mustache to summarize and plot personal finance data given in a CSV file of transactions.',
    'long_description': None,
    'author': 'Alex Raichev',
    'author_email': 'alex@raichev.net',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
