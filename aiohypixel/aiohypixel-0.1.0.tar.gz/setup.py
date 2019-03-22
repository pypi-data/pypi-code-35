# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiohypixel']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.5,<4.0', 'dataclasses>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'aiohypixel',
    'version': '0.1.0',
    'description': 'An asynchronous Hypixel API Wrapper written in Python',
    'long_description': None,
    'author': 'Tmpod',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
