# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['contenders']

package_data = \
{'': ['*']}

install_requires = \
['dash-bootstrap-components>=0.3.5,<0.4.0',
 'dash-table>=3.6,<4.0',
 'dash>=0.40.0,<0.41.0',
 'docopt>=0.6.2,<0.7.0',
 'pandas>=0.24.2,<0.25.0']

entry_points = \
{'console_scripts': ['contenders = contenders:main']}

setup_kwargs = {
    'name': 'contenders',
    'version': '0.1.1',
    'description': 'A self-hosted programming challenge framework.',
    'long_description': "# Contenders\nA self-hosted programming challenge framework, powered by [Dash](https://dash.plot.ly).\n\n## Setup\n```\n$ pip install contenders\n\n$ contenders --help\nContenders: Self-hosted programming challenge framework.\n\nUsage:\n    contenders -h | --help\n    contenders [--host=<host>] [--port=<port>]\n\nOptions:\n    -h --help      Show this help message.\n    --host=<host>  Specify the flask webserver's host.\n    --port=<port>  Specify the port for the flask webserver.\n```\n",
    'author': 'Jeremiah Boby',
    'author_email': 'mail@jeremiahboby.me',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
