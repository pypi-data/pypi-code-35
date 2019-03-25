# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tdameritrade_cli', 'tdameritrade_cli.tools']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'pyexcel-ods>=0.5.6,<0.6.0',
 'tdameritrade-client>=0.1.0,<0.2.0']

entry_points = \
{'console_scripts': ['tda-cli = tdameritrade_cli.cli:driver']}

setup_kwargs = {
    'name': 'tdameritrade-cli',
    'version': '0.1.0',
    'description': 'A CLI on top of the TDAmeritrade-client API library',
    'long_description': "[![pipeline status](https://gitlab.com/tdameritrade-tools/tdameritrade-cli/badges/master/pipeline.svg)](https://gitlab.com/tdameritrade-tools/tdameritrade-cli/commits/master)\n\n\n# TDAmeritrade CLI\n\nA CLI that makes requests of TDA using the TDA API via the TDA client. \n\n## Installation:\nRun `pip install tdameritrade-cli` from a virtual environment. I also suggest you add the\npackage's cli to your path. To do this, navigate to your virtual environment's `bin` folder\n(which can be found by running `which python` from within an activated virtual environment),\nand create a symbolic link.\n\nE.g., `ln -s <PATH TO VENV BIN>/tda-cli ~/.local/bin/tda-cli`\n\nNow you can run the tool (in a new shell) with `tda-cli`.\n\nSee `tda-cli --help` for functionality.",
    'author': 'Joe Castagneri',
    'author_email': 'jcastagneri@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
