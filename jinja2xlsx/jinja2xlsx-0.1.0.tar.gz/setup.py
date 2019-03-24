# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jinja2xlsx']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.10,<3.0', 'openpyxl>=2.6,<3.0', 'requests-html>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'jinja2xlsx',
    'version': '0.1.0',
    'description': 'Convert jinja2-html to xlsx',
    'long_description': None,
    'author': 'potykion',
    'author_email': 'potykion@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
