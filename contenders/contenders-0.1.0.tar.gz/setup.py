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
 'pandas>=0.24.2,<0.25.0']

entry_points = \
{'console_scripts': ['contender = contenders:main']}

setup_kwargs = {
    'name': 'contenders',
    'version': '0.1.0',
    'description': 'A self-hosted programming challenge framework.',
    'long_description': '# Contenders\nA self-hosted programming challenge framework, powered by [Dash](https://dash.plot.ly).\n\n## Setup\n```bash\n$ pip install contenders\n\n$ contenders\n```\n',
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
