# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['api_buddy',
 'api_buddy.config',
 'api_buddy.network',
 'api_buddy.network.auth',
 'api_buddy.utils',
 'api_buddy.validation']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==4.2b1',
 'Pygments>=2.3,<3.0',
 'beautifulsoup4>=4.7.1,<5.0.0',
 'colorama>=0.4.1,<0.5.0',
 'docopt>=0.6.2,<0.7.0',
 'requests-oauthlib>=1.2.0,<2.0.0',
 'schema>=0.6.8,<0.7.0',
 'yaspin>=0.14.1,<0.15.0']

entry_points = \
{'console_scripts': ['api = api_buddy.cli:run']}

setup_kwargs = {
    'name': 'api-buddy',
    'version': '0.1.0',
    'description': 'Explore APIs from your console with API Buddy',
    'long_description': None,
    'author': 'Peter Fonseca',
    'author_email': 'peter.nfonseca@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
