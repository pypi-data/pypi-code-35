# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['riberry_ldap']

package_data = \
{'': ['*']}

install_requires = \
['ldap3>=2.6,<3.0', 'riberry>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'riberry-ldap',
    'version': '0.2.0',
    'description': 'LDAP authentication for Riberry',
    'long_description': None,
    'author': 'Shady Rafehi',
    'author_email': 'shadyrafehi@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
