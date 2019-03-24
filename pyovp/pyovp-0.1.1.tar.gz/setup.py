# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyovp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyovp',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Shogo',
    'author_email': 'shogo@example.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
