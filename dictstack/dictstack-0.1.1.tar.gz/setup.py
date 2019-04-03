# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dictstack']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dictstack',
    'version': '0.1.1',
    'description': 'A multi-level dictionary that can overlay values in layers.',
    'long_description': None,
    'author': 'Lee Braiden',
    'author_email': 'leebraid@gmail.com',
    'url': 'https://github.com/lee-b/dictstack',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>2.7',
}


setup(**setup_kwargs)
