# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyboom']

package_data = \
{'': ['*']}

install_requires = \
['py-rolldice>=0.3.9,<0.4.0']

entry_points = \
{'console_scripts': ['pyboom = pyboom.__main__:main']}

setup_kwargs = {
    'name': 'pyboom',
    'version': '0.1.0',
    'description': 'Detonador de bombas .. boom!!!',
    'long_description': '# pyboom\n\nDetonador de bombas .. boom!!!\n\nPaquete de ejemplo para el tutorial - [Doom Presenta: Python desde cero](https://geekl0g.wordpress.com/tag/python-para-detonar-bombas).',
    'author': 'constrict0r',
    'author_email': 'constrict0r@protonmail.com',
    'url': 'https://geekl0g.wordpress.com/tag/python-para-detonar-bombas/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
