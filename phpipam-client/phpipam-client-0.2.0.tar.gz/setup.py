# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['phpipam_client']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'phpipam-client',
    'version': '0.2.0',
    'description': 'PHPIPAM Python RESP API Client',
    'long_description': "# phpipam-client\n![Pyup Status](https://pyup.io/repos/github/adzhurinskij/phpipam-client/shield.svg) ![Travis (.org)](https://img.shields.io/travis/adzhurinskij/phpipam-client.svg)\n\nPHPIPAM Python RESP API Client. It supports Python 2.7 and 3.4+.\n\n### Example\nBasic usage:\n```python\nfrom phpipam_client import PhpIpamClient, PATCH\n\nipam = PhpIpamClient(\n    url='https://ipam',\n    app_id='myapp',\n    username='mylogin',\n    password='mypassword',\n    user_agent='myapiclient', # custom user-agent header\n)\n\n# read object\nprint(ipam.query('/sections/'))\n\n# update object\nipam.query('/sections/1/', method=PATCH, data={\n    'description': 'example',\n})\n```\nUse encryption:\n```python\nipam = PhpIpamClient(\n    url='https://ipam',\n    app_id='myapp',\n    token='mytoken',\n    encryption=True,\n)\n```\n\n### Other API clients\n- https://github.com/adzhurinskij/phpipam-api-pythonclient (only Python 2.7)\n- https://github.com/efenian/phpipamsdk\n- https://github.com/michaelluich/phpIPAM\n",
    'author': 'Alexandr Dzhurinskij',
    'author_email': 'adzhurinskij@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
