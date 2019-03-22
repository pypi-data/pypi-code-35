# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['tdameritrade_client', 'tdameritrade_client.utils']

package_data = \
{'': ['*']}

install_requires = \
['environs>=4.1,<5.0', 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'tdameritrade-client',
    'version': '0.1.0',
    'description': 'A client for the TDA API',
    'long_description': '[![pipeline status](https://gitlab.com/tdameritrade-tools/tdameritrade-client/badges/master/pipeline.svg)](https://gitlab.com/tdameritrade-tools/tdameritrade-client/commits/master)\n\n# TDAmeritrade Client\n\nA tool that links to the TDA API to perform requests.\n\n## Installation:\nRun `pip install tdameritrade-client` within a virtual environment\n\n## Usage\nThe package has two uses as of now:\n1. Run the oauth flow against a developer app.\n2. Use an access token to request account positions.\n\nTo get started, use the following code snippet:\n\n``` python\nfrom tdameritrade_client.client import TDClient\n\ntd_client = TDClient(acct_number=<your account number>,\n                     oauth_user_id=<the id registered to the TD app you would like to authenticate with>,\n                     redirect_uri=<the redirect URI registered to the TD app>,\n                     token_path=<optional path to an existing access token>)\ntd_client.run_auth()\nacct_info = td_client.get_positions()\n```\n\n## Tests\nThis package uses poetry, which can be installed by running:\n```\ncurl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \n```\nTo run the tests, first install the package by cloning the repo and running `poetry install` from the root of the\nrepository. Then, run `poetry run pytest tests/` from the root directory of this repository.\n',
    'author': 'Joe Castagneri',
    'author_email': 'jcastagneri@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
