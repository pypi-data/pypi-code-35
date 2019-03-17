# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['inv']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'inv',
    'version': '0.1.0',
    'description': 'PyInv - A modular python inventory and asset management system',
    'long_description': None,
    'author': 'Dan Trickey',
    'author_email': 'dan@trickey.io',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
