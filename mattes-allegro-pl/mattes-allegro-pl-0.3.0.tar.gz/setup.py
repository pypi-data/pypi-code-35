# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['allegro_pl']

package_data = \
{'': ['*']}

install_requires = \
['allegro-pl-rest-api>=2019.0,<2020.0',
 'oauthlib>=3.0,<4.0',
 'requests-oauthlib>=1.2,<2.0',
 'tenacity>=5.0,<6.0',
 'zeep>=3.3,<4.0']

setup_kwargs = {
    'name': 'mattes-allegro-pl',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Raphael Krupinski',
    'author_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
