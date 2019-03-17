# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['py_ax_s']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'py-ax-s',
    'version': '0.1.2',
    'description': 'A Python client for the ax-s API.',
    'long_description': None,
    'author': 'elliott-maguire',
    'author_email': 'elliott.maguire@ax-s.io',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
