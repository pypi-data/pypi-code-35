# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['pyramid_hybridauth', 'pyramid_hybridauth.services']

package_data = \
{'': ['*']}

install_requires = \
['pyramid>=1.10,<2.0', 'requests_oauthlib>=1.2,<2.0']

setup_kwargs = {
    'name': 'pyramid-hybridauth',
    'version': '1.0.0',
    'description': 'It provides Pyramid authentication in conjunction with external services  using OAuth.',
    'long_description': 'pyramid_hybridauth README\n=========================\n\nGetting Started\n---------------\n\n- pip install pyramid_hybridauth\n',
    'author': 'Yoshimitsu Kokubo',
    'author_email': 'yoshi@unplus.net',
    'url': 'https://github.com/unplus/pyramid_hybridauth',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
