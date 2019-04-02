# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pcapfilter']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'scapy>=2.4,<3.0']

entry_points = \
{'console_scripts': ['pcapfilter = pcapfilter.cli:main']}

setup_kwargs = {
    'name': 'pcapfilter',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Nahuel Defossé',
    'author_email': 'nahuel.defosse@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
