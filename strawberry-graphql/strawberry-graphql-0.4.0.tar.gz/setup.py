# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['strawberry',
 'strawberry.cli',
 'strawberry.contrib',
 'strawberry.contrib.starlette',
 'strawberry.contrib.starlette.utils',
 'strawberry.utils']

package_data = \
{'': ['*'], 'strawberry.contrib.starlette': ['templates/*']}

install_requires = \
['click>=7.0,<8.0',
 'graphql-core-next>=1.0,<2.0',
 'hupper>=1.5,<2.0',
 'pygments>=2.3,<3.0',
 'starlette>=0.11.3,<0.12.0',
 'uvicorn>=0.4.6,<0.5.0']

entry_points = \
{'console_scripts': ['strawberry = strawberry.cli:run']}

setup_kwargs = {
    'name': 'strawberry-graphql',
    'version': '0.4.0',
    'description': 'A library for creating GraphQL APIs',
    'long_description': None,
    'author': 'Patrick Arminio',
    'author_email': 'patrick.arminio@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
