# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['docparse']

package_data = \
{'': ['*']}

entry_points = \
{'docparse.parsers': ['google_default = docparse.google']}

setup_kwargs = {
    'name': 'docparse',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'jdidion',
    'author_email': 'github@didion.net',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
