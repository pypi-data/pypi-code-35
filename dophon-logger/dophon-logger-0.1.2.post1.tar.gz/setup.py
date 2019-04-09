# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dophon_logger']

package_data = \
{'': ['*']}

install_requires = \
['hues>=0.2.2,<0.3.0']

setup_kwargs = {
    'name': 'dophon-logger',
    'version': '0.1.2.post1',
    'description': 'dophon logger module',
    'long_description': None,
    'author': 'CallMeE',
    'author_email': 'ealohu@163.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
