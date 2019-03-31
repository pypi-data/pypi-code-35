# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['synapse_p2p', 'synapse_p2p.tests']

package_data = \
{'': ['*']}

install_requires = \
['loguru', 'msgpack']

setup_kwargs = {
    'name': 'synapse-p2p',
    'version': '0.1.0',
    'description': 'A rapid RPC framework for building p2p networks',
    'long_description': None,
    'author': 'Daniel van Flymen',
    'author_email': 'vanflymen@gmail.com',
    'url': 'https://github.com/dvf/synapse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
