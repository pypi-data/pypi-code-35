# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cred_encryption']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.7.2,<0.8.0', 'cryptography>=2.6,<3.0']

entry_points = \
{'console_scripts': ['encryption = cred_encryption:run']}

setup_kwargs = {
    'name': 'cred-encryption',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Chris Davies',
    'author_email': 'christopher.davies@asg-worldwide.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
