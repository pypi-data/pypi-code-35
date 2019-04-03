# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['keras_nalu']

package_data = \
{'': ['*']}

install_requires = \
['keras>=2.2,<3.0']

setup_kwargs = {
    'name': 'keras-nalu',
    'version': '1.0.2',
    'description': 'Keras implementation of a NALU layer',
    'long_description': None,
    'author': 'Dennis Torres',
    'author_email': 'djtorres0@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
