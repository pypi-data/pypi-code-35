# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['crafty']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'crafty',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'MasonMcGill',
    'author_email': 'mmcgill@caltech.edu',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
