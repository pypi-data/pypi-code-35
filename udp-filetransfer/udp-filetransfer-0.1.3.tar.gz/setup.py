# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['udp_filetransfer']

package_data = \
{'': ['*']}

install_requires = \
['tqdm>=4.31,<5.0']

setup_kwargs = {
    'name': 'udp-filetransfer',
    'version': '0.1.3',
    'description': 'Reliable filetransfer over UDP',
    'long_description': None,
    'author': 'golyalpha',
    'author_email': 'golyalpha@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
