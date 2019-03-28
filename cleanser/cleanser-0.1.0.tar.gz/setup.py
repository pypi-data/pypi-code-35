# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cleanser', 'cleanser.core']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cleanser',
    'version': '0.1.0',
    'description': 'Cleaning data for NLP tasks.',
    'long_description': None,
    'author': 'Michael Holtzscher',
    'author_email': 'mholtz@protonmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
