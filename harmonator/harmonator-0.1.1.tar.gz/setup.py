# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['harmonator']

package_data = \
{'': ['*'], 'harmonator': ['exceptions/*']}

install_requires = \
['click>=7.0,<8.0']

setup_kwargs = {
    'name': 'harmonator',
    'version': '0.1.1',
    'description': 'Harmontown Downloader',
    'long_description': None,
    'author': 'Chris Read',
    'author_email': 'centurix@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
