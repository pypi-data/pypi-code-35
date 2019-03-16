# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tornado_jsonrpc2']

package_data = \
{'': ['*']}

install_requires = \
['tornado>=5.0']

setup_kwargs = {
    'name': 'tornado-jsonrpc2',
    'version': '0.4',
    'description': 'JSON-RPC request handler for Tornado.',
    'long_description': None,
    'author': 'Niko Wenselowski',
    'author_email': 'der@nik0.de',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
