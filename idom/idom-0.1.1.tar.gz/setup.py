# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['idom']

package_data = \
{'': ['*']}

install_requires = \
['sanic>=18.12,<19.0']

setup_kwargs = {
    'name': 'idom',
    'version': '0.1.1',
    'description': 'Control the web with Python',
    'long_description': None,
    'author': 'rmorshea',
    'author_email': 'ryan.morshead@gmail.com',
    'url': 'https://github.com/rmorshea/idom',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
