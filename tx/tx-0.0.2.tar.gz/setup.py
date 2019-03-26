# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tx', 'tx.ext']

package_data = \
{'': ['*']}

install_requires = \
['Twisted>=18.9,<19.0']

setup_kwargs = {
    'name': 'tx',
    'version': '0.0.2',
    'description': 'An extension base for twisted based projects',
    'long_description': None,
    'author': 'Yehuda Deutsch',
    'author_email': 'yeh@uda.co.il',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
